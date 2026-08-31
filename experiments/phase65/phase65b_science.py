#!/usr/bin/env python3
"""Phase 65B frozen scientific executable.

This file is used unchanged for the f102v2 primary reveal and f100v replication.
It implements the frozen PLAN_B.md statistic and predeclared sensitivities.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import itertools
import json
import math
import os
import re
import sys
import urllib.request
from collections import defaultdict
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.stats import rankdata


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def download(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "LETSGO-Voynich-Phase65B/1.0"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read()


def png_bytes(image: Image.Image) -> bytes:
    buf = io.BytesIO()
    image.save(buf, format="PNG", optimize=False, compress_level=9)
    return buf.getvalue()


def parse_eva_label(raw: str, view: str = "W1") -> list[str]:
    if view not in {"W1", "W2"}:
        raise ValueError(view)
    if "?" in raw or "[" in raw or "]" in raw:
        raise ValueError("uncertain label is ineligible")
    s = raw.replace("<->", "|").replace("<~>", "|")
    s = re.sub(r"<[^>]*>", "", s).replace("{", "").replace("}", "")
    atoms: dict[str, str] = {}

    def protect(m: re.Match[str]) -> str:
        key = f"\uE000{len(atoms)}\uE001"
        atoms[key] = m.group(0)
        return key

    s = re.sub(r"@[0-9]+;", protect, s)
    if view == "W1":
        s = s.replace(".", "|").replace(",", "|")
    else:
        s = s.replace(".", "|").replace(",", "")
    s = re.sub(r"\s+", "|", s)
    out: list[str] = []
    keys = sorted(atoms, key=len, reverse=True)
    i = 0
    while i < len(s):
        if s[i] == "|":
            if out and out[-1] != "|":
                out.append("|")
            i += 1
            continue
        matched = False
        for key in keys:
            if s.startswith(key, i):
                out.append(atoms[key])
                i += len(key)
                matched = True
                break
        if matched:
            continue
        c = s[i]
        if c.isascii() and c.isalpha():
            out.append(c.lower())
            i += 1
            continue
        raise ValueError(f"unexpected EVA character: {c!r}")
    while out and out[-1] == "|":
        out.pop()
    if not out:
        raise ValueError("empty parsed label")
    return out


def levenshtein(a: list[str], b: list[str]) -> int:
    prev = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        cur = [i]
        for j, y in enumerate(b, 1):
            cur.append(min(cur[-1] + 1, prev[j] + 1, prev[j - 1] + (x != y)))
        prev = cur
    return prev[-1]


def normalized_levenshtein(a: list[str], b: list[str]) -> float:
    if not a or not b:
        raise ValueError("nonempty sequences required")
    return levenshtein(a, b) / max(len(a), len(b))


def distance_matrix_text(seqs: list[list[str]]) -> list[list[float]]:
    n = len(seqs)
    out = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            d = normalized_levenshtein(seqs[i], seqs[j])
            out[i][j] = out[j][i] = d
    return out


def distance_matrix_length(seqs: list[list[str]]) -> list[list[float]]:
    n = len(seqs)
    out = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            a, b = len(seqs[i]), len(seqs[j])
            d = abs(a - b) / max(a, b)
            out[i][j] = out[j][i] = d
    return out


def pairs(n: int) -> list[tuple[int, int]]:
    return [(i, j) for i in range(n) for j in range(i + 1, n)]


def spearman(x: list[float], y: list[float]) -> float:
    if len(x) != len(y) or len(x) < 2:
        raise ValueError("bad vectors")
    rx = rankdata(np.asarray(x, float), method="average")
    ry = rankdata(np.asarray(y, float), method="average")
    if np.all(rx == rx[0]) or np.all(ry == ry[0]):
        return float("nan")
    return float(np.corrcoef(rx, ry)[0, 1])


def row_rho(v: list[list[float]], t: list[list[float]]) -> float:
    ij = pairs(len(v))
    return spearman([v[i][j] for i, j in ij], [t[i][j] for i, j in ij])


def permute_matrix(m: list[list[float]], p: tuple[int, ...]) -> list[list[float]]:
    return [[m[p[i]][p[j]] for j in range(len(p))] for i in range(len(p))]


def exact_page_stat(rows: list[dict]) -> dict:
    observed_rows = []
    for row in rows:
        rho = row_rho(row["visual"], row["text"])
        if not math.isfinite(rho):
            raise RuntimeError(f"non-finite observed Spearman in row {row['row']}")
        observed_rows.append((row["row"], len(pairs(len(row["visual"]))), rho))
    denom = sum(w for _, w, _ in observed_rows)
    observed = sum(w * rho for _, w, rho in observed_rows) / denom

    perms = [list(itertools.permutations(range(len(row["visual"])))) for row in rows]
    n_perm = math.prod(len(p) for p in perms)
    if n_perm > 5_000_000:
        raise RuntimeError(f"exact null too large: {n_perm}")
    stats: list[float] = []
    ge = 0
    for joint in itertools.product(*perms):
        total = 0.0
        for row, perm in zip(rows, joint):
            rho = row_rho(row["visual"], permute_matrix(row["text"], perm))
            if not math.isfinite(rho):
                raise RuntimeError(f"non-finite permutation Spearman in row {row['row']}")
            total += len(pairs(len(row["visual"]))) * rho
        stat = total / denom
        stats.append(stat)
        if stat >= observed - 1e-15:
            ge += 1
    q = np.quantile(np.asarray(stats, float), [0, 0.01, 0.025, 0.05, 0.5, 0.95, 0.975, 0.99, 1]).tolist()
    return {
        "T_observed": observed,
        "p_exact_one_sided": ge / n_perm,
        "n_permutations": n_perm,
        "page_pass": bool(observed >= 0.20 and ge / n_perm <= 0.05),
        "row_rho": {name: rho for name, _, rho in observed_rows},
        "row_pair_counts": {name: w for name, w, _ in observed_rows},
        "permutation_quantiles": {
            "min": q[0], "q01": q[1], "q025": q[2], "q05": q[3], "median": q[4],
            "q95": q[5], "q975": q[6], "q99": q[7], "max": q[8]
        },
    }


def preprocess(im: Image.Image, torch, grayscale: bool = False):
    im = im.convert("RGB")
    if grayscale:
        g = im.convert("L")
        im = Image.merge("RGB", (g, g, g))
    side = max(im.size)
    sq = Image.new("RGB", (side, side), (255, 255, 255))
    sq.paste(im, ((side - im.width) // 2, (side - im.height) // 2))
    sq = sq.resize((518, 518), resample=Image.Resampling.BICUBIC)
    arr = np.asarray(sq, dtype=np.float32) / 255.0
    x = torch.from_numpy(arr).permute(2, 0, 1)
    mean = torch.tensor([0.485, 0.456, 0.406])[:, None, None]
    std = torch.tensor([0.229, 0.224, 0.225])[:, None, None]
    return ((x - mean) / std).unsqueeze(0)


def load_dino(repo: Path, weights: Path):
    sys.path.insert(0, str(repo))
    import torch
    from dinov2.models.vision_transformer import vit_small
    model = vit_small(patch_size=14, img_size=518, init_values=1.0, block_chunks=0)
    model.load_state_dict(torch.load(weights, map_location="cpu", weights_only=True), strict=True)
    model.eval()
    return torch, model


def embed_images(images: list[Image.Image], torch, model, grayscale: bool) -> list[np.ndarray]:
    vecs = []
    with torch.inference_mode():
        for im in images:
            z = model.forward_features(preprocess(im, torch, grayscale))["x_norm_clstoken"][0]
            z = z / torch.linalg.vector_norm(z)
            vecs.append(z.cpu().numpy().astype(float))
    return vecs


def distance_matrix_visual(vecs: list[np.ndarray]) -> list[list[float]]:
    n = len(vecs)
    out = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            d = float(1.0 - np.dot(vecs[i], vecs[j]))
            out[i][j] = out[j][i] = d
    return out


def parse_it2a_loci(text: str) -> dict[str, str]:
    out = {}
    pat = re.compile(r"^<(f(?:100v|102v2)\.\d+),@Lf>\s+(.*?)\s*$")
    for line in text.splitlines():
        m = pat.match(line)
        if m:
            out[m.group(1)] = m.group(2)
    return out


def materialize_page_crops(page: str, crop_manifest: dict) -> tuple[list[dict], list[Image.Image], dict]:
    src = crop_manifest["source_images"][page]
    raw = download(src["requested_url"])
    if sha256_bytes(raw) != src["sha256"]:
        raise RuntimeError(f"Yale source hash mismatch for {page}")
    im = Image.open(io.BytesIO(raw)).convert("RGB")
    if list(im.size) != [src["width_px"], src["height_px"]]:
        raise RuntimeError(f"Yale dimensions mismatch for {page}")
    units = [u for u in crop_manifest["units"] if u["page"] == page and u["retained_for_science"]]
    images = []
    for u in units:
        x, y, w, h = u["rect"]
        crop = im.crop((x, y, x + w, y + h))
        encoded = png_bytes(crop)
        if sha256_bytes(encoded) != u["crop_png_sha256"]:
            raise RuntimeError(f"crop PNG hash mismatch: {u['object_id']}")
        images.append(crop)
    return units, images, {"sha256": sha256_bytes(raw), "byte_size": len(raw), "dimensions": list(im.size)}


def build_labels(page: str, source_manifest: dict, crop_units: list[dict], view: str, source: str, it_loci: dict[str, str] | None = None):
    by_object = {u["object_id"]: u for u in source_manifest["p25_locus_freeze"]["units"] if u["page"] == page}
    out = {}
    exclusions = []
    for cu in crop_units:
        oid = cu["object_id"]
        su = by_object[oid]
        raw = su["transcription_raw"] if source == "ZL3b" else (it_loci or {}).get(su["zl3b_locus"])
        if raw is None:
            exclusions.append({"object_id": oid, "reason": "missing IT2a locus"})
            continue
        try:
            seq = parse_eva_label(raw, view)
        except ValueError as e:
            exclusions.append({"object_id": oid, "reason": str(e), "raw": raw})
            continue
        out[oid] = {"raw": raw, "sequence": seq, "locus": su["zl3b_locus"]}
    return out, exclusions


def assemble_rows(crop_units: list[dict], visual_by_object: dict[str, list[list[float]]] | dict[str, int], text_labels: dict, text_kind: str, visual_matrix: list[list[float]]):
    index = {u["object_id"]: i for i, u in enumerate(crop_units)}
    grouped = defaultdict(list)
    for u in crop_units:
        if u["object_id"] in text_labels:
            grouped[u["row"]].append(u["object_id"])
    rows = []
    matrices = {}
    for row, ids in grouped.items():
        if len(ids) < 3:
            continue
        vi = [[visual_matrix[index[a]][index[b]] for b in ids] for a in ids]
        seqs = [text_labels[a]["sequence"] for a in ids]
        ti = distance_matrix_length(seqs) if text_kind == "length" else distance_matrix_text(seqs)
        rows.append({"row": row, "ids": ids, "visual": vi, "text": ti})
        matrices[row] = {"ids": ids, "visual_distance": vi, "text_distance": ti}
    return rows, matrices


def run_variant(name: str, crop_units: list[dict], visual_matrix: list[list[float]], labels: dict, text_kind: str = "levenshtein") -> dict:
    rows, matrices = assemble_rows(crop_units, {}, labels, text_kind, visual_matrix)
    if not rows:
        return {"variant": name, "status": "NO_USABLE_ROWS", "matrices": matrices}
    result = exact_page_stat(rows)
    result.update({"variant": name, "status": "OK", "retained_ids": [u["object_id"] for u in crop_units if u["object_id"] in labels], "matrices": matrices})
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--page", choices=["f102v2", "f100v"], required=True)
    ap.add_argument("--role", choices=["primary", "replication"], required=True)
    ap.add_argument("--source-manifest", required=True)
    ap.add_argument("--crop-manifest", required=True)
    ap.add_argument("--dinov2-repo", required=True)
    ap.add_argument("--weights", required=True)
    ap.add_argument("--it2a-file", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    if (args.page, args.role) not in {("f102v2", "primary"), ("f100v", "replication")}:
        raise RuntimeError("page/role chronology violation")

    source_manifest = json.loads(Path(args.source_manifest).read_text(encoding="utf-8"))
    crop_manifest = json.loads(Path(args.crop_manifest).read_text(encoding="utf-8"))
    weights_sha = sha256_file(Path(args.weights))
    expected_weights = source_manifest["sources"]["dinov2"]["weights"]["sha256"]
    if weights_sha != expected_weights:
        raise RuntimeError("DINO weight hash mismatch")
    it_bytes = Path(args.it2a_file).read_bytes()
    if sha256_bytes(it_bytes) != source_manifest["sources"]["it2a"]["sha256"]:
        raise RuntimeError("IT2a hash mismatch")
    it_loci = parse_it2a_loci(it_bytes.decode("utf-8"))

    crop_units, images, yale_prov = materialize_page_crops(args.page, crop_manifest)
    torch, model = load_dino(Path(args.dinov2_repo), Path(args.weights))
    rgb_vecs = embed_images(images, torch, model, grayscale=False)
    gray_vecs = embed_images(images, torch, model, grayscale=True)
    rgb_matrix = distance_matrix_visual(rgb_vecs)
    gray_matrix = distance_matrix_visual(gray_vecs)

    zl_w1, zl_w1_ex = build_labels(args.page, source_manifest, crop_units, "W1", "ZL3b")
    zl_w2, zl_w2_ex = build_labels(args.page, source_manifest, crop_units, "W2", "ZL3b")
    it_w1, it_w1_ex = build_labels(args.page, source_manifest, crop_units, "W1", "IT2a", it_loci)
    it_w2, it_w2_ex = build_labels(args.page, source_manifest, crop_units, "W2", "IT2a", it_loci)

    primary = run_variant("primary_rgb_zl_w1", crop_units, rgb_matrix, zl_w1)
    variants = {
        "primary": primary,
        "grayscale_zl_w1": run_variant("grayscale_zl_w1", crop_units, gray_matrix, zl_w1),
        "rgb_zl_w2": run_variant("rgb_zl_w2", crop_units, rgb_matrix, zl_w2),
        "rgb_zl_length_only": run_variant("rgb_zl_length_only", crop_units, rgb_matrix, zl_w1, text_kind="length"),
        "rgb_it2a_w1": run_variant("rgb_it2a_w1", crop_units, rgb_matrix, it_w1),
        "rgb_it2a_w2": run_variant("rgb_it2a_w2", crop_units, rgb_matrix, it_w2),
    }

    out = {
        "schema": "phase65b-scientific-result-v1",
        "phase": "65B3" if args.role == "primary" else "65B4",
        "page": args.page,
        "role": args.role,
        "frozen_thresholds": {"T_min": 0.20, "p_exact_max": 0.05},
        "primary_page_pass": primary.get("page_pass", False),
        "variants": variants,
        "label_exclusions": {"zl_w1": zl_w1_ex, "zl_w2": zl_w2_ex, "it2a_w1": it_w1_ex, "it2a_w2": it_w2_ex},
        "input_provenance": {
            "source_manifest_sha256": sha256_file(Path(args.source_manifest)),
            "crop_manifest_sha256": sha256_file(Path(args.crop_manifest)),
            "science_executable_sha256": sha256_file(Path(__file__)),
            "dinov2_commit_expected": source_manifest["sources"]["dinov2"]["commit"],
            "dinov2_weights_sha256": weights_sha,
            "it2a_sha256": sha256_bytes(it_bytes),
            "yale": yale_prov,
            "github_sha": os.environ.get("GITHUB_SHA"),
            "python": sys.version,
            "numpy": np.__version__,
            "scipy": __import__("scipy").__version__,
            "pillow": __import__("PIL").__version__,
            "torch": torch.__version__,
        },
        "claim_boundary": "A pass establishes only local covariance between attached label form and independently measured drawing morphology under the frozen representation; it is not decipherment, plaintext, plant-name identification, language identification, or cipher-key recovery.",
    }
    Path(args.out).write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"page": args.page, "role": args.role, "T": primary.get("T_observed"), "p": primary.get("p_exact_one_sided"), "pass": primary.get("page_pass")}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
