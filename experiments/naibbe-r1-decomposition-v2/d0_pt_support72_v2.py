#!/usr/bin/env python3
"""Issue #72 V2 Stage D0: target-blind PT full-pipeline support freeze.

Generate exactly one prospectively frozen PT assignment x historical RNG block
across the four frozen CREMMA manuscripts.  PT permutes effective plaintext
character instances within each line, then reruns the unchanged published
Naibbe pipeline from the same historical initial seed as the paired unchanged
baseline.

This executable MUST NOT load Voynich target residuals or compute pair-Q,
residual Z, E/W, target topology/sign agreement, or any R1 target statistic.

Usage:
    python d0_pt_support72_v2.py CREMMA_ROOT NAIBBE_ROOT J REP OUTPUT_JSON
"""
from __future__ import annotations

import collections
import hashlib
import json
import random
import sys
from pathlib import Path
from typing import Dict, Mapping, Sequence, Tuple

HERE = Path(__file__).resolve()
if str(HERE.parent) not in sys.path:
    sys.path.insert(0, str(HERE.parent))

import b0_support72_v2 as b0  # noqa: E402

EXPECTED_B0_SUPPORT_SCRIPT_BLOB = "ef3144591839395c18e1bdf308311bf99562bf9a"
EXPECTED_B0_RAW_SHA256 = "96b2865496306b48a4d843b590da32b06684520e4db6a21dd0ed0b859ca27d58"
STAGE_D_PLAN_COMMIT = "c45c67a665a7e4ad24c1d2706f83c65931d950a9"
J_VALUES = tuple(range(31))
REPS = tuple(range(5))
MANUSCRIPTS = ("BIS193", "CLM13027", "Mazarine915", "UBL758")
PT_NAMESPACE = "issue72v2:stageD:PT"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def canonical_json_bytes(obj) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def counter_payload(text: str) -> list:
    return [[ch, int(n)] for ch, n in sorted(collections.Counter(text).items())]


def line_inventory_sha(text: str) -> str:
    return sha256_bytes(canonical_json_bytes({"length": len(text), "counter": counter_payload(text)}))


def pt_order(cleaned: str, j: int, manuscript: str, item_id: str, line_index: int) -> Tuple[str, dict]:
    """Apply the exact prospectively frozen hash-order PT law."""
    keyed = []
    for source_position, ch in enumerate(cleaned):
        label = (
            f"{PT_NAMESPACE}:{j}:{manuscript}:{item_id}:"
            f"{line_index}:{source_position}"
        )
        keyed.append((hashlib.sha256(label.encode("utf-8")).digest(), source_position, ch))
    keyed.sort(key=lambda x: (x[0], x[1]))
    transformed = "".join(ch for _digest, _pos, ch in keyed)

    same_length = len(transformed) == len(cleaned)
    same_multiset = collections.Counter(transformed) == collections.Counter(cleaned)
    if not same_length or not same_multiset:
        raise RuntimeError(
            f"PT invariant failed {manuscript} {item_id} line {line_index}: "
            f"length={same_length} multiset={same_multiset}"
        )
    return transformed, {
        "item_id": item_id,
        "line_index": int(line_index),
        "effective_length_before": int(len(cleaned)),
        "effective_length_after": int(len(transformed)),
        "inventory_sha256_before": line_inventory_sha(cleaned),
        "inventory_sha256_after": line_inventory_sha(transformed),
        "same_length": bool(same_length),
        "same_multiset": bool(same_multiset),
        "textually_changed": bool(transformed != cleaned),
    }


def encrypt_pt_manuscript(
    module,
    source_items,
    manuscript: str,
    glyph_map: Mapping[str, str],
    seed: int,
    j: int,
):
    """Literal Phase64B published-view encryption with one upstream PT transform."""
    b0.n64.set_glyph_map(module, dict(glyph_map))
    random.seed(seed)
    module.ambiguity_retries = 0

    primary = []
    raw = []
    line_invariants = []
    source_units = 0
    published_clean_chars = 0
    effective_chars = 0
    dropped_unsupported_chars = 0
    dropped_types = set()
    nonempty_effective_lines = 0
    changed_nonempty_lines = 0
    primary_tokens = 0
    raw_tokens = 0

    for item in source_items:
        p_lines = []
        r_lines = []
        for line_index, line in enumerate(item.lines):
            source = b0.n64.string_line(line)
            source_units += sum(len(tok) for tok in line)
            published_cleaned = module.clean_line(source)
            published_clean_chars += len(published_cleaned)
            cleaned, dropped = b0.n64.project_effective_plaintext(published_cleaned)
            effective_chars += len(cleaned)
            dropped_unsupported_chars += len(dropped)
            dropped_types.update(dropped)

            transformed, invariant = pt_order(
                cleaned, j, manuscript, item.item_id, line_index
            )
            line_invariants.append(invariant)

            if cleaned:
                nonempty_effective_lines += 1
                changed_nonempty_lines += int(invariant["textually_changed"])
                encrypted = module.encrypt_naibbe(
                    transformed,
                    module.naibbe_tables,
                    dict(glyph_map),
                    use_78=module.USE_78_CARD_DECK,
                    pre_plaintext_file=None,
                )
                line_out = " ".join(encrypted)
                respaced = module.respace_line(line_out, module.SPACE_REMOVAL_RATE)
                rline = b0.n64.glyph_line(encrypted)
                pline = b0.n64.glyph_line(respaced.split())
            else:
                rline = []
                pline = []

            raw_tokens += len(rline)
            primary_tokens += len(pline)
            r_lines.append(rline)
            p_lines.append(pline)

        raw.append(b0.b.Item(item.item_id, manuscript, r_lines, None))
        primary.append(b0.b.Item(item.item_id, manuscript, p_lines, None))

    if not all(x["same_length"] and x["same_multiset"] for x in line_invariants):
        raise RuntimeError("PT line inventory invariant aggregate failed")
    if any(x["inventory_sha256_before"] != x["inventory_sha256_after"] for x in line_invariants):
        raise RuntimeError("PT line inventory digest mismatch")

    invariant_digest = sha256_bytes(canonical_json_bytes(line_invariants))
    return primary, raw, {
        "seed": int(seed),
        "pt_assignment": int(j),
        "pt_namespace": PT_NAMESPACE,
        "effective_plaintext_characters": int(effective_chars),
        "source_graphematic_units": int(source_units),
        "published_clean_line_characters": int(published_clean_chars),
        "dropped_unsupported_after_clean_line": int(dropped_unsupported_chars),
        "dropped_unsupported_character_types": sorted(dropped_types),
        "line_invariants_checked": int(len(line_invariants)),
        "line_invariants_all_true": True,
        "line_invariant_records_sha256": invariant_digest,
        "nonempty_effective_lines": int(nonempty_effective_lines),
        "changed_nonempty_lines": int(changed_nonempty_lines),
        "changed_nonempty_line_fraction": (
            float(changed_nonempty_lines / nonempty_effective_lines)
            if nonempty_effective_lines else None
        ),
        "primary_cipher_tokens": int(primary_tokens),
        "raw_cipher_tokens": int(raw_tokens),
        "ambiguity_retries": int(module.ambiguity_retries),
        "downstream_path_frozen": False,
        "downstream_path_divergence_is_part_of_total_effect": True,
    }


def load_b0_authority() -> dict:
    path = HERE.parent / "stage_b0_support.json"
    got = sha256_file(path)
    if got != EXPECTED_B0_RAW_SHA256:
        raise RuntimeError(f"Stage B0 authority SHA changed: {got} != {EXPECTED_B0_RAW_SHA256}")
    obj = json.loads(path.read_text(encoding="utf-8"))
    if obj["status"] != "UNCHANGED_NAIBBE_REP0_REP4_SURFACES_FROZEN":
        raise RuntimeError("Stage B0 authority status changed")
    if set(obj["reps"]) != {f"rep{i}" for i in REPS}:
        raise RuntimeError("Stage B0 historical rep population changed")
    if any(obj["target_access"].values()):
        raise RuntimeError("Stage B0 target firewall was not clean")
    return obj


def verify_baseline(
    module,
    sources,
    original_map: Mapping[str, str],
    parser,
    rep: int,
    b0_authority: Mapping,
) -> dict:
    frozen_rep = b0_authority["reps"][f"rep{rep}"]
    pooled_primary = []
    pooled_raw = []
    per_ms = {}
    for mi, manuscript in enumerate(MANUSCRIPTS):
        seed = 6480000 + 100 * mi + rep
        frozen = frozen_rep["per_manuscript"][manuscript]
        if frozen["seed"] != seed:
            raise RuntimeError(f"B0 seed mismatch rep{rep} {manuscript}")
        primary, raw, diag = b0.n64.encrypt_manuscript(
            module, sources[manuscript], manuscript, dict(original_map), seed
        )
        psha = b0.surface_sha(primary)
        rsha = b0.surface_sha(raw)
        support = b0.parser_support(primary, parser)
        if psha != frozen["primary_surface_sha256"]:
            raise RuntimeError(f"baseline primary mismatch rep{rep} {manuscript}: {psha}")
        if rsha != frozen["raw_surface_sha256"]:
            raise RuntimeError(f"baseline raw mismatch rep{rep} {manuscript}: {rsha}")
        if support["visible_tokens"] != frozen["support"]["visible_tokens"]:
            raise RuntimeError(f"baseline visible mismatch rep{rep} {manuscript}")
        if support["accepted_tokens"] != frozen["support"]["accepted_tokens"]:
            raise RuntimeError(f"baseline accepted mismatch rep{rep} {manuscript}")
        if int(diag["ambiguity_retries"]) != int(frozen["generation_diagnostics"]["ambiguity_retries"]):
            raise RuntimeError(f"baseline retry mismatch rep{rep} {manuscript}")
        pooled_primary.extend(primary)
        pooled_raw.extend(raw)
        per_ms[manuscript] = {
            "seed": int(seed),
            "primary_surface_sha256": psha,
            "raw_surface_sha256": rsha,
            "visible_tokens": int(support["visible_tokens"]),
            "accepted_tokens": int(support["accepted_tokens"]),
            "coverage": float(support["coverage"]),
            "ambiguity_retries": int(diag["ambiguity_retries"]),
        }

    pooled_psha = b0.surface_sha(pooled_primary)
    pooled_rsha = b0.surface_sha(pooled_raw)
    pooled_support = b0.parser_support(pooled_primary, parser)
    if pooled_psha != frozen_rep["primary_pooled_surface_sha256"]:
        raise RuntimeError(f"baseline pooled primary mismatch rep{rep}")
    if pooled_rsha != frozen_rep["raw_pooled_surface_sha256"]:
        raise RuntimeError(f"baseline pooled raw mismatch rep{rep}")
    if pooled_support["visible_tokens"] != frozen_rep["support"]["visible_tokens"]:
        raise RuntimeError(f"baseline pooled visible mismatch rep{rep}")
    if pooled_support["accepted_tokens"] != frozen_rep["support"]["accepted_tokens"]:
        raise RuntimeError(f"baseline pooled accepted mismatch rep{rep}")
    return {
        "rep": int(rep),
        "primary_pooled_surface_sha256": pooled_psha,
        "raw_pooled_surface_sha256": pooled_rsha,
        "support": pooled_support,
        "per_manuscript": per_ms,
        "exact_stage_b0_replay": True,
    }


def main(argv: Sequence[str]) -> int:
    if len(argv) != 6:
        raise SystemExit(f"usage: {argv[0]} CREMMA_ROOT NAIBBE_ROOT J REP OUTPUT_JSON")
    crem = Path(argv[1]).resolve()
    nai = Path(argv[2]).resolve()
    j = int(argv[3])
    rep = int(argv[4])
    output = Path(argv[5]).resolve()
    if j not in J_VALUES:
        raise SystemExit("J must be 0..30")
    if rep not in REPS:
        raise SystemExit("REP must be 0..4")
    output.parent.mkdir(parents=True, exist_ok=True)

    b0_script = HERE.parent / "b0_support72_v2.py"
    got_b0_blob = git_blob_sha1(b0_script.read_bytes())
    if got_b0_blob != EXPECTED_B0_SUPPORT_SCRIPT_BLOB:
        raise RuntimeError(f"Stage B0 helper changed: {got_b0_blob}")

    auth = b0.authority(crem, nai)
    b0_authority = load_b0_authority()
    module = b0.n64.load_naibbe(nai)
    original_map = dict(module.placeholder_to_glyph)
    parser = b0.e.SlotParser()
    parser_validation = b0.e.validate_parser(parser)
    sources = {
        name: b0.b.parse_latin_manuscript(crem, name, rel)
        for name, rel in b0.b.PRIMARY_MANUSCRIPTS.items()
    }

    baseline = verify_baseline(
        module, sources, original_map, parser, rep, b0_authority
    )

    pooled_primary = []
    pooled_raw = []
    per_ms: Dict[str, dict] = {}
    total_effective_chars = 0
    total_invariant_lines = 0
    total_nonempty = 0
    total_changed = 0

    for mi, manuscript in enumerate(MANUSCRIPTS):
        seed = 6480000 + 100 * mi + rep
        primary, raw, diag = encrypt_pt_manuscript(
            module, sources[manuscript], manuscript, original_map, seed, j
        )
        support = b0.parser_support(primary, parser)
        psha = b0.surface_sha(primary)
        rsha = b0.surface_sha(raw)
        pooled_primary.extend(primary)
        pooled_raw.extend(raw)
        total_effective_chars += int(diag["effective_plaintext_characters"])
        total_invariant_lines += int(diag["line_invariants_checked"])
        total_nonempty += int(diag["nonempty_effective_lines"])
        total_changed += int(diag["changed_nonempty_lines"])
        per_ms[manuscript] = {
            "seed": int(seed),
            "primary_surface_sha256": psha,
            "raw_surface_sha256": rsha,
            "support": support,
            "generation_diagnostics": diag,
            "changed_from_paired_baseline_primary": bool(
                psha != baseline["per_manuscript"][manuscript]["primary_surface_sha256"]
            ),
        }

    pooled_support = b0.parser_support(pooled_primary, parser)
    pooled_psha = b0.surface_sha(pooled_primary)
    pooled_rsha = b0.surface_sha(pooled_raw)

    result = {
        "schema": "issue72-v2-stage-d0-pt-support-v1",
        "status": "STAGE_D0_PT_ASSIGNMENT_SUPPORT_FROZEN_TARGET_BLIND",
        "scientific_role": "TOTAL_EFFECT_THROUGH_FULL_PUBLISHED_PIPELINE_TARGET_BLIND_SUPPORT",
        "stage_d_plan_commit": STAGE_D_PLAN_COMMIT,
        "authority": auth,
        "implementation_authority": {
            "b0_support72_v2.py_git_blob": got_b0_blob,
            "stage_b0_support_json_sha256": EXPECTED_B0_RAW_SHA256,
        },
        "assignment": {
            "j": int(j),
            "rep": int(rep),
            "pt_namespace": PT_NAMESPACE,
            "hash_order_law": (
                'ascending (SHA256("issue72v2:stageD:PT:{j}:{manuscript}:{item_id}:'
                '{line_index}:{source_position}"), source_position)'
            ),
            "cipher_seed_rule": "6480000 + 100*manuscript_index + rep",
            "no_rerolls": True,
        },
        "paired_baseline": baseline,
        "pt_surface": {
            "primary_pooled_surface_sha256": pooled_psha,
            "raw_pooled_surface_sha256": pooled_rsha,
            "support": pooled_support,
            "per_manuscript": per_ms,
            "total_effective_plaintext_characters": int(total_effective_chars),
            "line_invariants_checked": int(total_invariant_lines),
            "line_invariants_all_true": True,
            "nonempty_effective_lines": int(total_nonempty),
            "changed_nonempty_lines": int(total_changed),
            "changed_nonempty_line_fraction": (
                float(total_changed / total_nonempty) if total_nonempty else None
            ),
            "changed_from_paired_baseline_primary": bool(
                pooled_psha != baseline["primary_pooled_surface_sha256"]
            ),
        },
        "coverage_policy": "CONTINUOUS_DESCRIPTIVE_NO_HARD_CUTOFF",
        "selection_policy": "ALL_31_X_5_ASSIGNMENTS_PROCEED_NO_DROPS_NO_REROLLS",
        "parser_validation": parser_validation,
        "target_access": {
            "Voynich_target_file_loaded": False,
            "ZL3b_or_IT2a_target_vector_loaded": False,
            "slot_pair_Q_computed": False,
            "residual_Z_computed": False,
            "E_or_W_computed": False,
            "target_topology_or_sign_computed": False,
            "R1_target_rank_or_pvalue_computed": False,
        },
        "intervention_generation": {
            "PT_surface_generated": True,
            "full_published_pipeline_rerun": True,
            "published_codebook_unchanged": True,
            "downstream_path_allowed_to_diverge": True,
        },
    }

    raw = canonical_json_bytes(result) + b"\n"
    output.write_bytes(raw)
    print(json.dumps({
        "status": result["status"],
        "j": j,
        "rep": rep,
        "output_sha256": sha256_bytes(raw),
        "baseline_sha": baseline["primary_pooled_surface_sha256"],
        "pt_sha": pooled_psha,
        "pt_visible": pooled_support["visible_tokens"],
        "pt_accepted": pooled_support["accepted_tokens"],
        "pt_coverage": pooled_support["coverage"],
        "changed_nonempty_line_fraction": result["pt_surface"]["changed_nonempty_line_fraction"],
        "retries": {
            ms: per_ms[ms]["generation_diagnostics"]["ambiguity_retries"]
            for ms in MANUSCRIPTS
        },
        "target_access": result["target_access"],
    }, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
