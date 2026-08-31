#!/usr/bin/env python3
"""Phase 65B0 source-only preflight.

This program freezes external source identities and the already-preregistered
P25 label loci. It intentionally contains no image/text association metric,
no DINO inference, no string-distance implementation, no correlation, and no
permutation test.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import tempfile
import urllib.request
from pathlib import Path
from typing import Any

from PIL import Image

CIPHER_REPO = "https://github.com/matthewdgreen/cipher_benchmark.git"
CIPHER_COMMIT = "315f0cad4de3d021bd4185765c037cf2a28d341c"
ZL3B_BLOB = "2a4533ab9bdfa85db9bad602d590978953055df1"
IT2A_URL = "https://www.voynich.nu/data/IT2a-n.txt"

DINO_REPO = "https://github.com/facebookresearch/dinov2.git"
DINO_COMMIT = "7764ea0f912e53c92e82eb78a2a1631e92725fc8"
DINO_MODEL = "dinov2_vits14"
DINO_WEIGHTS_URL = (
    "https://dl.fbaipublicfiles.com/dinov2/"
    "dinov2_vits14/dinov2_vits14_pretrain.pth"
)

YALE_IMAGES = {
    "f100v": {
        "image_id": "1006249",
        "catalog_url": "https://collections.library.yale.edu/catalog/2002046?child_oid=1006249",
        "retrieval_url": "https://collections.library.yale.edu/iiif/2/1006249/full/full/0/default.jpg",
        "note": "Yale child image is the combined f100v + f101r scan; later crop freeze isolates f100v text-blindly.",
    },
    "f102v2": {
        "image_id": "1006252",
        "catalog_url": "https://collections.library.yale.edu/catalog/2002046?child_oid=1006252",
        "retrieval_url": "https://collections.library.yale.edu/iiif/2/1006252/full/full/0/default.jpg",
        "note": "Yale child image containing f102v2.",
    },
}

# Frozen from Phase65A physical row order, before any Phase65B content score.
# f102v2 top row L1 is intentionally absent because Phase65A rejected it for
# external object-label assignment ambiguity.
P25_LOCI = {
    "f100v": [
        ("T.1", 1), ("T.2", 2), ("T.3", 3), ("T.4", 4),
        ("M.1", 5), ("M.2", 6), ("M.3", 7), ("M.4", 8), ("M.5", 9),
        ("B.1", 10), ("B.2", 11), ("B.3", 12), ("B.4", 13),
    ],
    "f102v2": [
        ("L2.1", 10), ("L2.2", 11), ("L2.3", 12), ("L2.4", 13),
        ("L2.5", 14), ("L2.6", 15), ("L2.7", 16),
        ("L3.1", 25), ("L3.2", 26), ("L3.3", 27), ("L3.4", 28),
        ("L3.5", 29),
    ],
}

UA = "LETSGO-Voynich-Phase65B0-source-freeze/1.0 (+https://github.com/daito-dot/LETSGO-Voynich)"


def run(cmd: list[str], cwd: Path | None = None) -> str:
    proc = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return proc.stdout.strip()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fetch_bytes(url: str, *, timeout: int = 180) -> tuple[bytes, str, str | None]:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": UA, "Accept": "*/*"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read()
        final_url = resp.geturl()
        content_type = resp.headers.get("Content-Type")
    if not data:
        raise RuntimeError(f"empty response from {url}")
    return data, final_url, content_type


def fetch_to_file(url: str, dest: Path, *, timeout: int = 300) -> dict[str, Any]:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    h = hashlib.sha256()
    total = 0
    with urllib.request.urlopen(req, timeout=timeout) as resp, dest.open("wb") as out:
        final_url = resp.geturl()
        content_type = resp.headers.get("Content-Type")
        while True:
            chunk = resp.read(1024 * 1024)
            if not chunk:
                break
            out.write(chunk)
            h.update(chunk)
            total += len(chunk)
    if total == 0:
        raise RuntimeError(f"empty response from {url}")
    return {
        "requested_url": url,
        "final_url": final_url,
        "content_type": content_type,
        "byte_size": total,
        "sha256": h.hexdigest(),
    }


def checkout_exact(repo_url: str, commit: str, dest: Path) -> str:
    run(["git", "init", "-q", str(dest)])
    run(["git", "remote", "add", "origin", repo_url], cwd=dest)
    run(["git", "fetch", "-q", "--depth=1", "origin", commit], cwd=dest)
    run(["git", "checkout", "-q", "--detach", "FETCH_HEAD"], cwd=dest)
    head = run(["git", "rev-parse", "HEAD"], cwd=dest)
    if head != commit:
        raise RuntimeError(f"commit mismatch for {repo_url}: expected {commit}, got {head}")
    return head


def locate_zl3b(root: Path) -> Path:
    candidates = [p for p in root.rglob("ZL3b-n.txt") if ".git" not in p.parts]
    if len(candidates) != 1:
        raise RuntimeError(f"expected exactly one ZL3b-n.txt, found {len(candidates)}: {candidates}")
    return candidates[0]


def strip_ivtff_inline_comments(payload: str) -> str:
    return re.sub(r"<[^>]*>", "", payload).strip()


def extract_selected_labels(zl_path: Path) -> list[dict[str, Any]]:
    lines = zl_path.read_text(encoding="utf-8").splitlines()
    index: dict[tuple[str, int], tuple[str, str]] = {}
    pat = re.compile(r"^<(?P<page>f100v|f102v2)\.(?P<num>\d+),(?P<locator>[^>]*)>\s*(?P<payload>.*)$")
    for line in lines:
        m = pat.match(line)
        if not m:
            continue
        key = (m.group("page"), int(m.group("num")))
        index[key] = (m.group("locator"), m.group("payload"))

    selected: list[dict[str, Any]] = []
    for page, specs in P25_LOCI.items():
        for object_id, locus_num in specs:
            key = (page, locus_num)
            if key not in index:
                raise RuntimeError(f"missing frozen locus {page}.{locus_num} for {object_id}")
            locator, payload = index[key]
            transcription_raw = strip_ivtff_inline_comments(payload)
            has_unreadable = "?" in transcription_raw
            has_alternative = bool(re.search(r"\[[^\]]*\]", transcription_raw))
            confidence_eligible = not (has_unreadable or has_alternative)
            selected.append(
                {
                    "page": page,
                    "object_id": object_id,
                    "zl3b_locus": f"{page}.{locus_num}",
                    "ivtff_locator": locator,
                    "source_payload": payload,
                    "transcription_raw": transcription_raw,
                    "confidence_flags": {
                        "contains_question_mark": has_unreadable,
                        "contains_bracket_alternative": has_alternative,
                        "phase63b_65b_confidence_eligible": confidence_eligible,
                    },
                }
            )
    if len(selected) != 25:
        raise RuntimeError(f"expected 25 frozen P25 loci, got {len(selected)}")
    return selected


def ivtff_header(text: str) -> str | None:
    for line in text.splitlines():
        if "IVTFF" in line.upper():
            return line.strip()
    return None


def yale_record(page: str, spec: dict[str, str], out_dir: Path) -> dict[str, Any]:
    dest = out_dir / f"yale_{page}_{spec['image_id']}.jpg"
    meta = fetch_to_file(spec["retrieval_url"], dest)
    with Image.open(dest) as im:
        im.verify()
    with Image.open(dest) as im:
        width, height = im.size
        image_format = im.format
        mode = im.mode
    if image_format not in {"JPEG", "JPG"}:
        raise RuntimeError(f"unexpected Yale format for {page}: {image_format}")
    meta.update(
        {
            "authority": "Yale Beinecke Library digital collections",
            "catalog_url": spec["catalog_url"],
            "image_id": spec["image_id"],
            "width_px": width,
            "height_px": height,
            "decoded_format": image_format,
            "decoded_mode": mode,
            "artifact_filename": dest.name,
            "note": spec["note"],
        }
    )
    return meta


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default="phase65b-preflight-artifact")
    args = ap.parse_args()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="phase65b0-") as td:
        tmp = Path(td)

        cipher_root = tmp / "cipher_benchmark"
        cipher_head = checkout_exact(CIPHER_REPO, CIPHER_COMMIT, cipher_root)
        zl_path = locate_zl3b(cipher_root)
        zl_blob = run(["git", "hash-object", str(zl_path)], cwd=cipher_root)
        if zl_blob != ZL3B_BLOB:
            raise RuntimeError(f"ZL3b blob mismatch: expected {ZL3B_BLOB}, got {zl_blob}")
        zl_bytes = zl_path.read_bytes()
        selected_labels = extract_selected_labels(zl_path)

        it2a_data, it2a_final, it2a_type = fetch_bytes(IT2A_URL)
        it2a_text = it2a_data.decode("utf-8")
        it2a_path = out_dir / "IT2a-n.source.txt"
        it2a_path.write_bytes(it2a_data)

        dino_root = tmp / "dinov2"
        dino_head = checkout_exact(DINO_REPO, DINO_COMMIT, dino_root)
        dino_weights_path = tmp / "dinov2_vits14_pretrain.pth"
        dino_weights = fetch_to_file(DINO_WEIGHTS_URL, dino_weights_path)

        yale = {
            page: yale_record(page, spec, out_dir)
            for page, spec in YALE_IMAGES.items()
        }

        confidence_excluded = [
            x["object_id"] for x in selected_labels
            if not x["confidence_flags"]["phase63b_65b_confidence_eligible"]
        ]
        eligible_by_page: dict[str, int] = {}
        for page in P25_LOCI:
            eligible_by_page[page] = sum(
                1 for x in selected_labels
                if x["page"] == page
                and x["confidence_flags"]["phase63b_65b_confidence_eligible"]
            )

        manifest = {
            "schema": "phase65b-source-manifest-v1",
            "phase": "65B0",
            "mode": "SOURCE_ONLY_PREFLIGHT",
            "project_commit": os.environ.get("GITHUB_SHA"),
            "normative_plan": "experiments/phase65/PLAN_B.md",
            "anti_leak": {
                "p25_visual_text_association_computed": False,
                "dino_embeddings_computed": False,
                "text_distance_computed": False,
                "correlation_computed": False,
                "permutation_statistic_computed": False,
            },
            "sources": {
                "zl3b": {
                    "repository": "matthewdgreen/cipher_benchmark",
                    "repository_url": CIPHER_REPO,
                    "commit": cipher_head,
                    "relative_path": str(zl_path.relative_to(cipher_root)),
                    "git_blob_sha1": zl_blob,
                    "byte_size": len(zl_bytes),
                    "sha256": sha256_bytes(zl_bytes),
                },
                "it2a": {
                    "requested_url": IT2A_URL,
                    "final_url": it2a_final,
                    "content_type": it2a_type,
                    "byte_size": len(it2a_data),
                    "sha256": sha256_bytes(it2a_data),
                    "ivtff_header": ivtff_header(it2a_text),
                    "artifact_filename": it2a_path.name,
                },
                "dinov2": {
                    "repository": "facebookresearch/dinov2",
                    "repository_url": DINO_REPO,
                    "commit": dino_head,
                    "model": DINO_MODEL,
                    "weights": dino_weights,
                    "weights_loaded_for_inference": False,
                },
                "yale_images": yale,
            },
            "p25_locus_freeze": {
                "mapping_authority": (
                    "Phase65A VIB/Stolfi physical row order and object-label localization; "
                    "no Phase65B score used"
                ),
                "f102v2_top_row_excluded_before_science": True,
                "units": selected_labels,
                "selected_count": len(selected_labels),
                "confidence_excluded_before_science": confidence_excluded,
                "confidence_eligible_count_by_page": eligible_by_page,
            },
        }

        if not all(value is False for value in manifest["anti_leak"].values()):
            raise RuntimeError("anti-leak invariant failed")

        manifest_path = out_dir / "SOURCE_MANIFEST_B.generated.json"
        manifest_path.write_text(
            json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

        print(json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False))
        print(
            "SOURCE PREFLIGHT PASS: no P25 visual-text association, DINO embedding, "
            "text distance, correlation or permutation statistic was computed."
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
