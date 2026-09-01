#!/usr/bin/env python3
"""Issue #72 V2 Stage B0: target-blind unchanged-Naibbe support freeze.

Generate exactly the historical Phase64B published Naibbe rep0..rep4 surfaces
and freeze their identities, parser support, and generation diagnostics.

Forbidden here: slot-pair Q, residual Z, E/W, target topology/sign agreement,
R1 p-values, and every Issue72 intervention surface.

Usage:
    python experiments/naibbe-r1-decomposition-v2/b0_support72_v2.py \
        CREMMA_ROOT NAIBBE_ROOT OUTPUT_JSON
"""
from __future__ import annotations

import collections
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, Sequence

HERE = Path(__file__).resolve()
EXPERIMENTS = HERE.parents[1]
for rel in ("phase62", "phase64", "issue26-music"):
    p = EXPERIMENTS / rel
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import phase62b_n0 as b  # noqa: E402
import phase64b_naibbe as n64  # noqa: E402
import issue26e_core as e  # noqa: E402

PARENT_MAIN = "98a04953aabe9e228a17fa5808adf506a0833362"
EXPECTED_CREMMA = "292525969ad98380b398e6606a9c2a36d51913ae"
EXPECTED_NAIBBE = "f2675ec5dd275268bc64dd48ea64fc0e0e9827a2"
EXPECTED_ENCODER_BLOB = "b566ad82e4b6ff0782ecdddebf77718dac44f292"
EXPECTED_TABLE_BLOB = "5cd34fb81d80faf3b4d57dbf1719c05ffde25302"
EXPECTED_DECODER_BLOB = "b56a1e6e615a7b2e31ad386efdf7e6f2ef2b9d7b"
MANUSCRIPTS = tuple(n64.MANUSCRIPTS)
REPS = tuple(range(5))
EXPECTED_REP0_BY_MS = {
    "BIS193": "fbf275e179297b947ccd2de5686e02340ea15d6ab9ca4b73a26dd9448b286805",
    "CLM13027": "da43249442db277a367bb8171b7228a9bf4b63b055924e9efd06240452d4ad77",
    "Mazarine915": "2ebecc4d281df810f57ec370cd1ba0d4708be0391d8185d3ed2ccb588df1f33d",
    "UBL758": "5c6649425d9be84f8b9ce04c257cc6fb308e9b8a59191320fcf1a63c86affa89",
}
EXPECTED_REP0_POOLED = "47d52d28d4e2ac126bb8681c881ec339cb339c9b1bb329fb48263e6c1e9758bd"
EXPECTED_REP0_VISIBLE = 33574
EXPECTED_REP0_ACCEPTED = 29759


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def verify_git_head(root: Path, expected: str, label: str) -> str:
    got = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    if got != expected:
        raise RuntimeError(f"{label} commit mismatch: {got} != {expected}")
    return got


def canonical_items_payload(items: Sequence[b.Item]) -> bytes:
    obj = [
        {
            "item_id": it.item_id,
            "document": it.document,
            "leaf": it.leaf,
            "lines": [["".join(tok) for tok in line] for line in it.lines],
        }
        for it in items
    ]
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def surface_sha(items: Sequence[b.Item]) -> str:
    return sha256_bytes(canonical_items_payload(items))


def parser_support(items: Sequence[b.Item], parser: e.SlotParser) -> dict:
    visible = accepted = 0
    by_document = collections.Counter()
    by_document_ok = collections.Counter()
    for it in items:
        for line in it.lines:
            for tok_units in line:
                tok = "".join(tok_units)
                if not tok:
                    continue
                visible += 1
                by_document[it.document] += 1
                if parser.pick(tok, "min") is not None:
                    accepted += 1
                    by_document_ok[it.document] += 1
    return {
        "visible_tokens": int(visible),
        "accepted_tokens": int(accepted),
        "coverage": float(accepted / visible) if visible else 0.0,
        "stage_b0_role": "CONTINUOUS_POSITIVE_CONTROL_SUPPORT_NO_HARD_CUTOFF",
        "by_document": {
            doc: {
                "visible": int(by_document[doc]),
                "accepted": int(by_document_ok[doc]),
                "coverage": float(by_document_ok[doc] / by_document[doc]) if by_document[doc] else 0.0,
            }
            for doc in sorted(by_document)
        },
    }


def authority(cremma_root: Path, naibbe_root: Path) -> dict:
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
    return {
        "CREMMA_commit": EXPECTED_CREMMA,
        "Naibbe_commit": EXPECTED_NAIBBE,
        "Naibbe_blobs": blobs,
    }


def main(argv: Sequence[str]) -> int:
    if len(argv) != 4:
        raise SystemExit(f"usage: {argv[0]} CREMMA_ROOT NAIBBE_ROOT OUTPUT_JSON")
    crem = Path(argv[1]).resolve()
    nai = Path(argv[2]).resolve()
    output = Path(argv[3]).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    auth = authority(crem, nai)
    module = n64.load_naibbe(nai)
    original_map = dict(module.placeholder_to_glyph)
    parser = e.SlotParser()
    parser_validation = e.validate_parser(parser)
    sources = {
        name: b.parse_latin_manuscript(crem, name, rel)
        for name, rel in b.PRIMARY_MANUSCRIPTS.items()
    }

    reps: Dict[str, dict] = {}
    for rep in REPS:
        pooled_primary = []
        pooled_raw = []
        per_ms = {}
        for mi, manuscript in enumerate(MANUSCRIPTS):
            seed = 6480000 + 100 * mi + rep
            primary, raw, diag = n64.encrypt_manuscript(
                module, sources[manuscript], manuscript, original_map, seed
            )
            psha = surface_sha(primary)
            rsha = surface_sha(raw)
            support = parser_support(primary, parser)
            if rep == 0 and psha != EXPECTED_REP0_BY_MS[manuscript]:
                raise RuntimeError(f"rep0 frozen surface mismatch {manuscript}: {psha}")
            pooled_primary.extend(primary)
            pooled_raw.extend(raw)
            per_ms[manuscript] = {
                "seed": int(seed),
                "primary_surface_sha256": psha,
                "raw_surface_sha256": rsha,
                "support": support,
                "generation_diagnostics": diag,
            }

        psha = surface_sha(pooled_primary)
        rsha = surface_sha(pooled_raw)
        support = parser_support(pooled_primary, parser)
        if rep == 0:
            if psha != EXPECTED_REP0_POOLED:
                raise RuntimeError(f"rep0 pooled frozen surface mismatch: {psha}")
            if support["visible_tokens"] != EXPECTED_REP0_VISIBLE or support["accepted_tokens"] != EXPECTED_REP0_ACCEPTED:
                raise RuntimeError(f"rep0 support mismatch: {support}")
        reps[f"rep{rep}"] = {
            "rep": int(rep),
            "primary_pooled_surface_sha256": psha,
            "raw_pooled_surface_sha256": rsha,
            "support": support,
            "per_manuscript": per_ms,
        }

    result = {
        "schema": "issue72-v2-stage-b0-unchanged-naibbe-support-v1",
        "status": "UNCHANGED_NAIBBE_REP0_REP4_SURFACES_FROZEN",
        "parent_main": PARENT_MAIN,
        "scientific_role": "TARGET_BLIND_POSITIVE_CONTROL_SUPPORT_FREEZE",
        "authority": auth,
        "historical_population": {
            "source": "Phase64B CIPHER_REPS=5 pre-Issue68 frozen family",
            "reps": list(REPS),
            "manuscripts": list(MANUSCRIPTS),
            "seed_rule": "6480000 + 100*manuscript_index + rep",
        },
        "parser_validation": parser_validation,
        "coverage_policy": "CONTINUOUS_DESCRIPTIVE_NO_HARD_CUTOFF",
        "target_access": {
            "slot_pair_Q_computed": False,
            "residual_Z_computed": False,
            "E_or_W_computed": False,
            "ZL3b_or_IT2a_target_loaded": False,
            "topology_or_sign_computed": False,
            "R1_pvalue_computed": False,
            "Issue72_intervention_surface_generated": False,
            "Issue72_intervention_R1_computed": False,
        },
        "reps": reps,
    }
    raw = json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"
    output.write_bytes(raw)
    print(json.dumps({
        "status": result["status"],
        "output_sha256": sha256_bytes(raw),
        "reps": {
            name: {
                "primary_pooled_surface_sha256": row["primary_pooled_surface_sha256"],
                "visible": row["support"]["visible_tokens"],
                "accepted": row["support"]["accepted_tokens"],
                "coverage": row["support"]["coverage"],
                "ambiguity_retries": {
                    ms: row["per_manuscript"][ms]["generation_diagnostics"]["ambiguity_retries"]
                    for ms in MANUSCRIPTS
                },
            }
            for name, row in reps.items()
        },
    }, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
