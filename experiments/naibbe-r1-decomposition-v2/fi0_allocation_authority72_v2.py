#!/usr/bin/env python3
"""Issue #72 V2 Stage C1 FI0: target-blind final-token allocation authority.

Generate the exact preregistered FI-G/FI-M allocation population without
loading any Voynich target or computing Q/Z/R1.

Usage:
  python fi0_allocation_authority72_v2.py CREMMA_ROOT NAIBBE_ROOT OUTPUT_JSON
"""
from __future__ import annotations

import collections
import hashlib
import json
import random
import subprocess
import sys
from pathlib import Path
from typing import Mapping, Sequence

HERE = Path(__file__).resolve()
EXPERIMENTS = HERE.parents[1]
for rel in ("phase62", "phase64", "issue26-music"):
    p = EXPERIMENTS / rel
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import phase62b_n0 as p62b  # noqa: E402
import phase64b_naibbe as n64  # noqa: E402
import issue26e_core as e  # noqa: E402

EXPECTED_CREMMA = "292525969ad98380b398e6606a9c2a36d51913ae"
EXPECTED_NAIBBE = "f2675ec5dd275268bc64dd48ea64fc0e0e9827a2"
EXPECTED_ENCODER_BLOB = "b566ad82e4b6ff0782ecdddebf77718dac44f292"
EXPECTED_TABLE_BLOB = "5cd34fb81d80faf3b4d57dbf1719c05ffde25302"
EXPECTED_DECODER_BLOB = "b56a1e6e615a7b2e31ad386efdf7e6f2ef2b9d7b"
B0_PATH = HERE.parent / "stage_b0_support.json"
B0_SHA256 = "96b2865496306b48a4d843b590da32b06684520e4db6a21dd0ed0b859ca27d58"
PLAN_COMMIT = "a053efd9803b6c0f74614986289c54a8add7d904"
MANUSCRIPTS = ("BIS193", "CLM13027", "Mazarine915", "UBL758")
N_PERM = 199
EXPECTED_IDENTITY_SURFACE_SHA256 = "47d52d28d4e2ac126bb8681c881ec339cb339c9b1bb329fb48263e6c1e9758bd"
EXPECTED_VISIBLE = 33574
EXPECTED_ACCEPTED = 29759
EXPECTED_DISTINCT = 7146


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def verify_git_head(root: Path, expected: str, label: str) -> None:
    got = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    if got != expected:
        raise RuntimeError(f"{label} commit mismatch: {got} != {expected}")


def verify_authority(cremma_root: Path, naibbe_root: Path) -> dict:
    verify_git_head(cremma_root, EXPECTED_CREMMA, "CREMMA")
    verify_git_head(naibbe_root, EXPECTED_NAIBBE, "Naibbe")
    checks = {
        "naibbe_v2.py": (naibbe_root / "naibbe_v2.py", EXPECTED_ENCODER_BLOB),
        "references/naibbe_tables.csv": (naibbe_root / "references" / "naibbe_tables.csv", EXPECTED_TABLE_BLOB),
        "decrypt_naibbe.py": (naibbe_root / "decrypt_naibbe.py", EXPECTED_DECODER_BLOB),
    }
    blobs = {}
    for label, (path, expected) in checks.items():
        got = git_blob_sha1(path.read_bytes())
        if got != expected:
            raise RuntimeError(f"{label} blob mismatch: {got} != {expected}")
        blobs[label] = got
    return {"CREMMA_commit": EXPECTED_CREMMA, "Naibbe_commit": EXPECTED_NAIBBE, "Naibbe_blobs": blobs}


def load_b0() -> dict:
    got = sha256_file(B0_PATH)
    if got != B0_SHA256:
        raise RuntimeError(f"B0 SHA mismatch: {got} != {B0_SHA256}")
    obj = json.loads(B0_PATH.read_text(encoding="utf-8"))
    if obj["status"] != "UNCHANGED_NAIBBE_REP0_REP4_SURFACES_FROZEN":
        raise RuntimeError("B0 status changed")
    if any(obj["target_access"].values()):
        raise RuntimeError("B0 target firewall not clean")
    return obj


def canonical_payload(records: Sequence[Mapping]) -> bytes:
    obj = [
        {
            "item_id": r["item_id"],
            "document": r["document"],
            "leaf": r["leaf"],
            "lines": r["lines"],
        }
        for r in records
    ]
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def json_digest(obj) -> str:
    return sha256_bytes(json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def seed_from_namespace(namespace: str) -> int:
    # Frozen deterministic mapping. Python Random(int) + shuffle is used only to
    # materialize the preregistered target-independent allocation namespaces.
    return int.from_bytes(hashlib.sha256(namespace.encode("utf-8")).digest(), "big")


def build_identity(cremma_root: Path, naibbe_root: Path, b0: Mapping) -> dict:
    mod = n64.load_naibbe(naibbe_root)
    original_map = dict(mod.placeholder_to_glyph)
    sources = {
        name: p62b.parse_latin_manuscript(cremma_root, name, rel)
        for name, rel in p62b.PRIMARY_MANUSCRIPTS.items()
    }
    parser = e.SlotParser()
    e.validate_parser(parser)
    frozen = b0["reps"]["rep0"]

    records = []
    slots = []
    pooled_items = []
    token_stream = []
    per_ms_tokens = {m: [] for m in MANUSCRIPTS}
    per_ms_accepted = collections.Counter()
    identity_accepted = 0

    for fold, manuscript in enumerate(MANUSCRIPTS):
        expected = frozen["per_manuscript"][manuscript]
        seed = 6480000 + 100 * fold
        if expected["seed"] != seed:
            raise RuntimeError(f"frozen rep0 seed mismatch {manuscript}")
        primary, _raw, _diag = n64.encrypt_manuscript(mod, sources[manuscript], manuscript, original_map, seed)

        # Verify exact per-manuscript surface before exposing any FI operation.
        pobj = [
            {"item_id": it.item_id, "document": it.document, "leaf": it.leaf,
             "lines": [["".join(tok) for tok in line] for line in it.lines]}
            for it in primary
        ]
        psha = sha256_bytes(json.dumps(pobj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"))
        if psha != expected["primary_surface_sha256"]:
            raise RuntimeError(f"rep0 manuscript surface mismatch {manuscript}: {psha}")
        pooled_items.extend(primary)

        for it in primary:
            rec = {"fold": fold, "item_id": it.item_id, "document": it.document, "leaf": it.leaf, "lines": []}
            for line_index, line in enumerate(it.lines):
                toks = ["".join(tok) for tok in line]
                rec["lines"].append(toks)
                n_visible = len(toks)
                for token_index, tok in enumerate(toks):
                    slot = {
                        "fold": fold,
                        "manuscript": manuscript,
                        "item_id": it.item_id,
                        "leaf": it.leaf,
                        "line_index": int(line_index),
                        "token_index": int(token_index),
                        "line_visible_tokens": int(n_visible),
                    }
                    slots.append(slot)
                    token_stream.append(tok)
                    per_ms_tokens[manuscript].append(tok)
                    if parser.pick(tok, "min") is not None:
                        identity_accepted += 1
                        per_ms_accepted[manuscript] += 1
            records.append(rec)

    identity_surface = sha256_bytes(canonical_payload(records))
    if identity_surface != EXPECTED_IDENTITY_SURFACE_SHA256:
        raise RuntimeError(f"identity pooled surface mismatch: {identity_surface}")
    if len(token_stream) != EXPECTED_VISIBLE:
        raise RuntimeError(f"identity visible mismatch: {len(token_stream)}")
    if identity_accepted != EXPECTED_ACCEPTED:
        raise RuntimeError(f"identity accepted mismatch: {identity_accepted}")
    if len(set(token_stream)) != EXPECTED_DISTINCT:
        raise RuntimeError(f"identity distinct mismatch: {len(set(token_stream))}")

    # The slot skeleton deliberately excludes token identity.
    slot_layout_sha = json_digest(slots)
    token_stream_sha = json_digest(token_stream)
    global_multiset_sha = json_digest(sorted(collections.Counter(token_stream).items()))
    per_ms_multiset_sha = {
        m: json_digest(sorted(collections.Counter(per_ms_tokens[m]).items())) for m in MANUSCRIPTS
    }
    line_counts = [r["line_visible_tokens"] for r in slots if r["token_index"] == 0]
    line_counts_sha = json_digest(line_counts)

    return {
        "records": records,
        "slots": slots,
        "token_stream": token_stream,
        "per_ms_tokens": per_ms_tokens,
        "parser": parser,
        "identity": {
            "surface_sha256": identity_surface,
            "visible_tokens": len(token_stream),
            "accepted_tokens": identity_accepted,
            "distinct_complete_tokens": len(set(token_stream)),
            "coverage": identity_accepted / len(token_stream),
            "token_stream_sha256": token_stream_sha,
            "global_multiset_sha256": global_multiset_sha,
            "slot_layout_sha256": slot_layout_sha,
            "line_token_counts_sha256": line_counts_sha,
            "per_manuscript_visible": {m: len(per_ms_tokens[m]) for m in MANUSCRIPTS},
            "per_manuscript_accepted": {m: int(per_ms_accepted[m]) for m in MANUSCRIPTS},
            "per_manuscript_multiset_sha256": per_ms_multiset_sha,
        },
    }


def allocate(identity: Mapping, family: str, index: int) -> tuple[list[str], str, int]:
    if family not in ("G", "M") or not (0 <= index < N_PERM):
        raise ValueError((family, index))
    namespace = f"issue72v2:C1:FI-{family}:allocation:{index}"
    seed = seed_from_namespace(namespace)
    rng = random.Random(seed)
    base = list(identity["token_stream"])
    if family == "G":
        assigned = base[:]
        rng.shuffle(assigned)
    else:
        # Sequential independent uniform shuffles in fixed manuscript order,
        # driven by the single preregistered FI-M allocation namespace.
        pools = {m: list(identity["per_ms_tokens"][m]) for m in MANUSCRIPTS}
        for m in MANUSCRIPTS:
            rng.shuffle(pools[m])
        cursor = {m: 0 for m in MANUSCRIPTS}
        assigned = []
        for slot in identity["slots"]:
            m = slot["manuscript"]
            assigned.append(pools[m][cursor[m]])
            cursor[m] += 1
        if any(cursor[m] != len(pools[m]) for m in MANUSCRIPTS):
            raise RuntimeError("FI-M allocation cursor mismatch")
    return assigned, namespace, seed


def allocated_records(identity: Mapping, assigned: Sequence[str]) -> list[dict]:
    if len(assigned) != len(identity["slots"]):
        raise RuntimeError("allocated token count mismatch")
    out = []
    cursor = 0
    for r in identity["records"]:
        nr = {"item_id": r["item_id"], "document": r["document"], "leaf": r["leaf"], "lines": []}
        for line in r["lines"]:
            n = len(line)
            nr["lines"].append(list(assigned[cursor:cursor+n]))
            cursor += n
        out.append(nr)
    if cursor != len(assigned):
        raise RuntimeError("allocated record cursor mismatch")
    return out


def case_metadata(identity: Mapping, family: str, index: int) -> dict:
    assigned, namespace, seed = allocate(identity, family, index)
    parser = identity["parser"]
    per_ms_visible = collections.Counter()
    per_ms_accepted = collections.Counter()
    accepted = 0
    changed = 0
    for slot, base_tok, tok in zip(identity["slots"], identity["token_stream"], assigned):
        m = slot["manuscript"]
        per_ms_visible[m] += 1
        if tok != base_tok:
            changed += 1
        if parser.pick(tok, "min") is not None:
            accepted += 1
            per_ms_accepted[m] += 1
    if accepted != EXPECTED_ACCEPTED:
        raise RuntimeError(f"pooled accepted changed {family}{index}: {accepted}")
    if json_digest(sorted(collections.Counter(assigned).items())) != identity["identity"]["global_multiset_sha256"]:
        raise RuntimeError(f"global multiset changed {family}{index}")
    if family == "M":
        for m in MANUSCRIPTS:
            toks = [tok for slot, tok in zip(identity["slots"], assigned) if slot["manuscript"] == m]
            if json_digest(sorted(collections.Counter(toks).items())) != identity["identity"]["per_manuscript_multiset_sha256"][m]:
                raise RuntimeError(f"FI-M manuscript multiset changed {index} {m}")
            if per_ms_accepted[m] != identity["identity"]["per_manuscript_accepted"][m]:
                raise RuntimeError(f"FI-M manuscript accepted changed {index} {m}")
    recs = allocated_records(identity, assigned)
    surface_sha = sha256_bytes(canonical_payload(recs))
    return {
        "family": family,
        "index": index,
        "allocation_namespace": namespace,
        "allocation_seed_decimal": str(seed),
        "surface_sha256": surface_sha,
        "baseline_identical_surface": surface_sha == EXPECTED_IDENTITY_SURFACE_SHA256,
        "changed_slot_instances": changed,
        "changed_slot_fraction": changed / EXPECTED_VISIBLE,
        "visible_tokens": EXPECTED_VISIBLE,
        "accepted_tokens": accepted,
        "coverage": accepted / EXPECTED_VISIBLE,
        "per_manuscript_visible": {m: int(per_ms_visible[m]) for m in MANUSCRIPTS},
        "per_manuscript_accepted": {m: int(per_ms_accepted[m]) for m in MANUSCRIPTS},
    }


def main(argv: Sequence[str]) -> int:
    if len(argv) != 4:
        raise SystemExit(f"usage: {argv[0]} CREMMA_ROOT NAIBBE_ROOT OUTPUT_JSON")
    crem = Path(argv[1]).resolve()
    nai = Path(argv[2]).resolve()
    out = Path(argv[3]).resolve()
    auth = verify_authority(crem, nai)
    b0 = load_b0()
    identity = build_identity(crem, nai, b0)

    cases = []
    for family in ("G", "M"):
        for index in range(N_PERM):
            cases.append(case_metadata(identity, family, index))

    if len(cases) != 2 * N_PERM:
        raise RuntimeError("FI population size mismatch")
    result = {
        "schema": "issue72-v2-stage-c1-fi0-allocation-authority-v1",
        "status": "FI_G_M_398_ALLOCATION_POPULATION_FROZEN_TARGET_BLIND",
        "scientific_role": "PRETARGET_FINAL_TOKEN_ALLOCATION_AUTHORITY",
        "preregistered_plan_commit": PLAN_COMMIT,
        "authority": auth,
        "n_perm_per_family": N_PERM,
        "families": ["G", "M"],
        "seed_mapping": "seed=int.from_bytes(SHA256(allocation_namespace UTF-8).digest(),'big'); random.Random(seed).shuffle",
        "identity": identity["identity"],
        "cases": cases,
        "selection_policy": {
            "baseline_identical_surfaces_retained": True,
            "rerolls": 0,
            "drops": 0,
            "coverage_gate": False,
            "target_dependent_selection": False,
        },
        "target_access": {
            "Voynich_target_loaded": False,
            "slot_pair_Q_computed": False,
            "residual_Z_computed": False,
            "R1_topology_computed": False,
            "R1_rank_or_pvalue_computed": False,
        },
    }
    raw = json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(raw)
    print(json.dumps({
        "status": result["status"],
        "cases": len(cases),
        "identity": result["identity"],
        "G_baseline_identical": sum(c["baseline_identical_surface"] for c in cases if c["family"] == "G"),
        "M_baseline_identical": sum(c["baseline_identical_surface"] for c in cases if c["family"] == "M"),
        "G_changed_fraction_range": [min(c["changed_slot_fraction"] for c in cases if c["family"] == "G"), max(c["changed_slot_fraction"] for c in cases if c["family"] == "G")],
        "M_changed_fraction_range": [min(c["changed_slot_fraction"] for c in cases if c["family"] == "M"), max(c["changed_slot_fraction"] for c in cases if c["family"] == "M")],
        "output_sha256": sha256_bytes(raw),
    }, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
