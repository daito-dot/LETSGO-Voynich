#!/usr/bin/env python3
"""Phase 65B1 text-blind crop freeze.

This program intentionally has no text parser, DINO code, string-distance code,
correlation code, or permutation code. It reads only the Yale image identities
from SOURCE_MANIFEST_B.json and the already-frozen geometric rectangles from
CROP_SPEC_B.json, then downloads, verifies, crops, hashes, and audits coverage.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
import urllib.request
from collections import Counter
from pathlib import Path

from PIL import Image


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def download(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "LETSGO-Voynich-Phase65B/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def png_bytes(image: Image.Image) -> bytes:
    buf = io.BytesIO()
    image.save(buf, format="PNG", optimize=False, compress_level=9)
    return buf.getvalue()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-manifest", required=True)
    ap.add_argument("--crop-spec", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--manifest-out", required=True)
    args = ap.parse_args()

    source_path = Path(args.source_manifest)
    spec_path = Path(args.crop_spec)
    out_dir = Path(args.out_dir)
    crops_dir = out_dir / "crops"
    crops_dir.mkdir(parents=True, exist_ok=True)

    source = json.loads(source_path.read_text(encoding="utf-8"))
    spec = json.loads(spec_path.read_text(encoding="utf-8"))

    # Deliberately access only non-text source fields. The P25 transcription
    # payload in SOURCE_MANIFEST_B is not read during crop freezing.
    yale = source["sources"]["yale_images"]
    if source.get("anti_leak", {}).get("p25_visual_text_association_computed") is not False:
        raise RuntimeError("source manifest anti-leak state is not clean")

    decoded: dict[str, Image.Image] = {}
    source_audit: dict[str, dict] = {}
    for page in sorted({u["page"] for u in spec["units"]}):
        meta = yale[page]
        raw = download(meta["requested_url"])
        actual_hash = sha256_bytes(raw)
        if actual_hash != meta["sha256"]:
            raise RuntimeError(f"{page}: Yale image hash changed: {actual_hash}")
        if len(raw) != int(meta["byte_size"]):
            raise RuntimeError(f"{page}: Yale image byte size changed")
        im = Image.open(io.BytesIO(raw)).convert("RGB")
        if im.size != (int(meta["width_px"]), int(meta["height_px"])):
            raise RuntimeError(f"{page}: decoded dimensions changed: {im.size}")
        decoded[page] = im
        source_audit[page] = {
            "image_id": meta["image_id"],
            "requested_url": meta["requested_url"],
            "sha256": actual_hash,
            "byte_size": len(raw),
            "width_px": im.width,
            "height_px": im.height,
        }

    units_out = []
    counts_page = Counter()
    counts_row = Counter()
    for u in spec["units"]:
        page = u["page"]
        row = u["row"]
        oid = u["object_id"]
        x, y, w, h = map(int, u["rect"])
        im = decoded[page]
        if min(x, y, w, h) < 0 or w <= 0 or h <= 0 or x + w > im.width or y + h > im.height:
            raise RuntimeError(f"{oid}: crop rectangle out of bounds")
        flags = dict(u["quality_flags"])
        forbidden = ["label_glyphs", "other_plant", "scan_damage", "mapping_ambiguous"]
        if any(flags.get(k) for k in forbidden):
            raise RuntimeError(f"{oid}: crop spec contains exclusion flag")
        crop = im.crop((x, y, x + w, y + h))
        raw_png = png_bytes(crop)
        filename = f"{page}__{oid.replace('.', '_')}.png"
        (crops_dir / filename).write_bytes(raw_png)
        units_out.append({
            "page": page,
            "row": row,
            "object_id": oid,
            "source_image_sha256": source_audit[page]["sha256"],
            "rect": [x, y, w, h],
            "quality_flags": flags,
            "crop_png": filename,
            "crop_png_byte_size": len(raw_png),
            "crop_png_sha256": sha256_bytes(raw_png),
            "crop_width_px": w,
            "crop_height_px": h,
            "retained_for_science": True,
        })
        counts_page[page] += 1
        counts_row[f"{page}/{row}"] += 1

    total = len(units_out)
    coverage = {
        "total_retained": total,
        "by_page": dict(sorted(counts_page.items())),
        "by_row": dict(sorted(counts_row.items())),
        "requirements": {
            "total_retained_gte_20": total >= 20,
            "f102v2_total_gte_8": counts_page["f102v2"] >= 8,
            "f102v2_L2_gte_4": counts_row["f102v2/L2"] >= 4,
            "f102v2_L3_gte_4": counts_row["f102v2/L3"] >= 4,
            "f100v_total_gte_8": counts_page["f100v"] >= 8,
            "f100v_T_gte_3": counts_row["f100v/T"] >= 3,
            "f100v_M_gte_3": counts_row["f100v/M"] >= 3,
            "f100v_B_gte_3": counts_row["f100v/B"] >= 3,
        },
    }
    coverage["coverage_firewall_pass"] = all(coverage["requirements"].values())
    if not coverage["coverage_firewall_pass"]:
        raise RuntimeError("Phase65B coverage firewall failed before science")

    manifest = {
        "schema": "phase65b-crop-manifest-v1",
        "phase": "65B1",
        "mode": "TEXT_BLIND_CROP_FREEZE",
        "normative_plan": spec["normative_plan"],
        "source_manifest": spec["source_manifest"],
        "source_manifest_git_blob": spec["source_manifest_git_blob"],
        "crop_spec_sha256": sha256_bytes(spec_path.read_bytes()),
        "pillow_version": __import__("PIL").__version__,
        "source_images": source_audit,
        "confidence_excluded_before_crop": spec["confidence_excluded_before_crop"],
        "units": units_out,
        "coverage": coverage,
        "anti_leak": {
            "label_text_read_for_crop_choice": False,
            "p25_visual_text_association_computed": False,
            "dino_embeddings_computed": False,
            "text_distance_computed": False,
            "correlation_computed": False,
            "permutation_statistic_computed": False,
        },
        "next_gate": "Synthetic-only implementation preflight; do not compute a P25 image-text association yet.",
    }
    out_path = Path(args.manifest_out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"CROP FREEZE PASS: retained={total}; manifest={out_path}")
    print("ANTI-LEAK PASS: no label text, DINO embedding, text distance, correlation, or permutation statistic used.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
