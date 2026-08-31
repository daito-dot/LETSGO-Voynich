#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import re
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

SOURCE_COMMIT = "31819c914061cc6b63bbf4983e33d643ede52e46"
SOURCE_URL = (
    "https://raw.githubusercontent.com/Aspect-Research/voynich-autoexploration/"
    + SOURCE_COMMIT
    + "/data/transcriptions/eva_zl3b.txt"
)
EXPECTED_GIT_BLOB = "2a4533ab9bdfa85db9bad602d590978953055df1"
EXPECTED_HEADER = "# Version 3b of 13/05/2025"
UNCERTAIN = set("?[]{}@:<>")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha(data: bytes) -> str:
    hdr = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(hdr + data).hexdigest()


def fetch_source() -> tuple[str, dict]:
    with urllib.request.urlopen(SOURCE_URL, timeout=60) as r:
        data = r.read()
    text = data.decode("utf-8")
    blob = git_blob_sha(data)
    if EXPECTED_HEADER not in text[:1000]:
        raise RuntimeError("unexpected ZL3b version header")
    if blob != EXPECTED_GIT_BLOB:
        raise RuntimeError(f"unexpected transcription blob: {blob}")
    return text, {
        "url": SOURCE_URL,
        "commit": SOURCE_COMMIT,
        "git_blob_sha1": blob,
        "version_header": EXPECTED_HEADER,
        "bytes": len(data),
    }


def parse_locus_lines(source: str) -> dict[str, dict]:
    out = {}
    pat = re.compile(r"^<([^,>]+),([^>]+)>\s+(.*)$")
    for line in source.splitlines():
        m = pat.match(line)
        if not m:
            continue
        locus, locus_type, payload = m.groups()
        out[locus] = {"type": locus_type, "payload": payload}
    return out


def strip_leading_comment_markers(payload: str) -> str:
    s = payload.strip()
    while True:
        m = re.match(r"^<![^>]*>", s)
        if not m:
            return s
        s = s[m.end():].lstrip()


def conservative_tokens(text: str) -> list[str]:
    text = text.replace("<->", " ")
    parts = re.split(r"[.,\s]+", text)
    out = []
    for tok in parts:
        if not tok:
            continue
        if any(ch in tok for ch in UNCERTAIN):
            continue
        if re.fullmatch(r"[a-z]+", tok):
            out.append(tok)
    return out


def extract_label_table(manifest: dict, source: str):
    loci = parse_locus_lines(source)
    records = []
    for block in manifest["blocks"]:
        objects = []
        for obj in block["fragment_objects"]:
            toks = []
            locus_records = []
            for loc in obj["loci"]:
                if loc not in loci:
                    raise KeyError(f"missing locus {loc}")
                rec = loci[loc]
                if "Lf" not in rec["type"]:
                    raise ValueError(f"frozen fragment locus is not Lf: {loc} {rec['type']}")
                cleaned_payload = strip_leading_comment_markers(rec["payload"])
                tt = conservative_tokens(cleaned_payload)
                toks.extend(tt)
                locus_records.append({
                    "locus": loc,
                    "locus_type": rec["type"],
                    "raw_payload": rec["payload"],
                    "valid_tokens": tt,
                })
            objects.append({
                "object_id": obj["object_id"],
                "loci": locus_records,
                "valid_tokens": toks,
            })
        records.append({
            "block_id": block["block_id"],
            "folio": block["folio"],
            "objects": objects,
            "valid_label_tokens": [t for o in objects for t in o["valid_tokens"]],
        })
    return records


def clean_body_line(raw: str) -> list[str]:
    s = raw.replace("<%>", " ").replace("<$>", " ").replace("<->", " ")
    return conservative_tokens(s)


def lev1(a: str, b: str) -> bool:
    if a == b or abs(len(a) - len(b)) > 1:
        return False
    if len(a) == len(b):
        return sum(x != y for x, y in zip(a, b)) == 1
    if len(a) > len(b):
        a, b = b, a
    i = j = d = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            i += 1
            j += 1
        else:
            d += 1
            j += 1
        if d > 1:
            return False
    return True


def build_body_tables(manifest: dict, text_table: dict):
    text_by = {r["block_id"]: r for r in text_table["records"]}
    history = defaultdict(list)
    retained = {}
    all_clean = {}
    diag = {}
    for block in manifest["blocks"]:
        bid = block["block_id"]
        folio = block["folio"]
        hist = history[folio]
        keep = []
        clean_all = []
        n_entry = n_local = 0
        for li, raw in enumerate(text_by[bid]["raw_lines"]):
            toks = clean_body_line(raw)
            for tok in toks:
                clean_all.append(tok)
                if li == 0:
                    n_entry += 1
                elif any(lev1(tok, prev) for prev in hist[-10:]):
                    n_local += 1
                else:
                    keep.append(tok)
                hist.append(tok)
                if len(hist) > 10:
                    del hist[:-10]
        retained[bid] = keep
        all_clean[bid] = clean_all
        diag[bid] = {
            "cleaned_tokens": len(clean_all),
            "entry_masked": n_entry,
            "local_edit1_masked": n_local,
            "innovation_retained": len(keep),
            "retained_fraction": len(keep) / len(clean_all) if clean_all else 0.0,
        }
    return retained, all_clean, diag


def token_hit(label: str, body_tokens: list[str], mode: str) -> bool:
    if mode == "exact":
        return any(label == t for t in body_tokens)
    if mode == "closed_edit1":
        return any(label == t or lev1(label, t) for t in body_tokens)
    raise ValueError(mode)


def block_hit_score(labels: list[str], body_tokens: list[str], mode: str):
    if not labels:
        return None, 0, 0
    hits = sum(token_hit(lab, body_tokens, mode) for lab in labels)
    return hits / len(labels), hits, len(labels)


def inferential_blocks(manifest: dict):
    counts = Counter(b["folio"] for b in manifest["blocks"])
    return [b for b in manifest["blocks"] if counts[b["folio"]] >= 2]


def assignment_space(blocks):
    folios = [b["folio"] for b in blocks]
    groups = []
    for f in dict.fromkeys(folios):
        idx = [i for i, ff in enumerate(folios) if ff == f]
        groups.append((idx, list(itertools.permutations(idx))))
    for choices in itertools.product(*(g[1] for g in groups)):
        perm = list(range(len(blocks)))
        for (idx, _), chosen in zip(groups, choices):
            for dest, src in zip(idx, chosen):
                perm[dest] = src
        yield perm


def statistic(labels_by, bodies_by, block_ids, perm, mode="closed_edit1", pooled=False):
    block_scores = []
    total_hits = total_labels = 0
    for i, bid in enumerate(block_ids):
        labels = labels_by[bid]
        body = bodies_by[block_ids[perm[i]]]
        score, hits, nlab = block_hit_score(labels, body, mode)
        if score is not None:
            block_scores.append(score)
            total_hits += hits
            total_labels += nlab
    if pooled:
        return total_hits / total_labels if total_labels else 0.0
    return sum(block_scores) / len(block_scores) if block_scores else 0.0


def exact_test(labels_by, bodies_by, blocks, mode="closed_edit1", pooled=False):
    block_ids = [b["block_id"] for b in blocks]
    obs_perm = list(range(len(blocks)))
    obs = statistic(labels_by, bodies_by, block_ids, obs_perm, mode, pooled)
    vals = []
    identity = False
    for perm in assignment_space(blocks):
        if perm == obs_perm:
            identity = True
        vals.append(statistic(labels_by, bodies_by, block_ids, perm, mode, pooled))
    expected = math.prod(math.factorial(v) for v in Counter(b["folio"] for b in blocks).values())
    if len(vals) != expected or expected != 1152:
        raise AssertionError((len(vals), expected))
    if not identity:
        raise AssertionError("identity missing")
    p = sum(v >= obs - 1e-15 for v in vals) / len(vals)
    return {
        "observed": obs,
        "exact_p": p,
        "tail_count": int(sum(v >= obs - 1e-15 for v in vals)),
        "n_assignments": len(vals),
        "null_mean": sum(vals) / len(vals),
        "null_q95": float(sorted(vals)[math.ceil(0.95 * len(vals)) - 1]),
        "null_max": max(vals),
    }


def run(manifest, text_table):
    source, source_meta = fetch_source()
    label_records = extract_label_table(manifest, source)
    labels_by = {r["block_id"]: r["valid_label_tokens"] for r in label_records}
    retained, all_clean, body_diag = build_body_tables(manifest, text_table)
    blocks = inferential_blocks(manifest)
    block_ids = [b["block_id"] for b in blocks]

    available = [bid for bid in block_ids if labels_by[bid]]
    total_labels = sum(len(labels_by[bid]) for bid in block_ids)
    gate = len(available) >= 10 and total_labels >= 50

    primary = exact_test(labels_by, retained, blocks, "closed_edit1", pooled=False)
    s1 = exact_test(labels_by, retained, blocks, "exact", pooled=False)
    s2 = exact_test(labels_by, all_clean, blocks, "closed_edit1", pooled=False)
    s3 = exact_test(labels_by, retained, blocks, "closed_edit1", pooled=True)

    if primary["exact_p"] <= 0.05 and gate:
        classification = "CANDIDATE Lf↔FORMAL-RESIDUAL BODY FAMILY RELATION — INDEPENDENT REPLICATION REQUIRED"
    elif primary["exact_p"] <= 0.05 and not gate:
        classification = "UNDERPOWERED / COVERAGE-LIMITED"
    else:
        classification = "NOT SUPPORTED"

    per_block_obs = {}
    for bid in block_ids:
        sc, hits, nlab = block_hit_score(labels_by[bid], retained[bid], "closed_edit1")
        per_block_obs[bid] = {
            "valid_label_tokens": labels_by[bid],
            "n_valid_label_tokens": nlab,
            "retained_body_tokens": retained[bid],
            "n_retained_body_tokens": len(retained[bid]),
            "primary_hits": hits,
            "primary_block_score": sc,
        }

    return {
        "schema": "phase68a-result-v1",
        "source": source_meta,
        "population": {
            "all_blocks": len(manifest["blocks"]),
            "inferential_blocks": len(blocks),
            "inferential_folios": sorted(set(b["folio"] for b in blocks)),
            "blocks_with_valid_labels": len(available),
            "valid_label_token_occurrences": total_labels,
            "coverage_gate_pass": gate,
        },
        "body_mask_diagnostics": body_diag,
        "primary_block_balanced_retained_closed_edit1": primary,
        "secondary_exact_only_retained": s1,
        "secondary_all_clean_body_closed_edit1": s2,
        "secondary_pooled_label_retained_closed_edit1": s3,
        "classification": classification,
        "per_block_observed": per_block_obs,
        "label_extraction": label_records,
    }


def main():
    here = Path(__file__).parent
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", type=Path, default=here.parent / "phase67" / "BLOCK_MANIFEST_A.json")
    ap.add_argument("--text", type=Path, default=here.parent / "phase67" / "TEXT_TABLE_A.json")
    ap.add_argument("--out", type=Path, default=here / "RESULT_A.json")
    args = ap.parse_args()
    result = run(load_json(args.manifest), load_json(args.text))
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "classification": result["classification"],
        "source_blob": result["source"]["git_blob_sha1"],
        "inferential_blocks": result["population"]["inferential_blocks"],
        "valid_label_tokens": result["population"]["valid_label_token_occurrences"],
        "primary": result["primary_block_balanced_retained_closed_edit1"],
        "S1_exact": result["secondary_exact_only_retained"],
        "S2_all_clean": result["secondary_all_clean_body_closed_edit1"],
        "S3_pooled": result["secondary_pooled_label_retained_closed_edit1"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
