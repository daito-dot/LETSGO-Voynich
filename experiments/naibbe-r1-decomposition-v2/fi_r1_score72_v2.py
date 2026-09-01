#!/usr/bin/env python3
"""Issue #72 V2 preregistered FI complete-token allocation R1 scorer.

For one FI-G or FI-M allocation index, replay the exact frozen Stage-A/Issue68
rep0 primary surface, allocate unchanged complete token instances according to
the preregistered family, prove all declared invariants, and only then (unless
--verify-only) compute the frozen R1 measurement against ZL3b and IT2a.

Usage:
  python fi_r1_score72_v2.py CREMMA_ROOT NAIBBE_ROOT FAMILY INDEX OUTPUT_JSON [--verify-only]
"""
from __future__ import annotations

import collections
import hashlib
import json
import random
import sys
from pathlib import Path
from typing import Mapping, Sequence

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import b1_r1_calibration72_v2 as b1  # noqa: E402
import d1_pt_r1_score72_v2 as d1  # noqa: E402
import trace_audit72_v2 as stagea  # noqa: E402

FI_PLAN_COMMIT = "a053efd9803b6c0f74614986289c54a8add7d904"
FI_PLAN_PATH = HERE / "STAGE_C1_FI_PLAN.md"
FI_PLAN_BLOB = "f051c1a4530c96b2945bdb5b59cb4eb166561895"
B0_SHA256 = "96b2865496306b48a4d843b590da32b06684520e4db6a21dd0ed0b859ca27d58"
IDENTITY_SURFACE_SHA256 = "47d52d28d4e2ac126bb8681c881ec339cb339c9b1bb329fb48263e6c1e9758bd"
IDENTITY_VISIBLE = 33574
IDENTITY_DISTINCT = 7146
IDENTITY_ACCEPTED = 29759
IDENTITY_COVERAGE = 0.886370405671055
IDENTITY_E = 3.1784043855151296
IDENTITY_R = {"ZL3b": 0.8830282501011794, "IT2a": 0.9000974100381157}
IDENTITY_SIGN = {"ZL3b": 60, "IT2a": 61}
IDENTITY_T = 0.8830282501011794
IDENTITY_BY_MS = {
    "BIS193": {"visible": 12804, "accepted": 11346},
    "CLM13027": {"visible": 10918, "accepted": 9716},
    "Mazarine915": {"visible": 7536, "accepted": 6659},
    "UBL758": {"visible": 2316, "accepted": 2038},
}
MANUSCRIPTS = tuple(stagea.MANUSCRIPTS)
FAMILIES = ("FI-G", "FI-M")
N_PERM = 199
N_REF = 1000
FLOAT_TOL = 1e-15


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def token_counter(items_by_ms: Mapping[str, Sequence]) -> collections.Counter:
    c = collections.Counter()
    for ms in MANUSCRIPTS:
        for it in items_by_ms[ms]:
            for line in it.lines:
                for tok in line:
                    text = stagea.token_text(tok)
                    if not text:
                        raise RuntimeError("identity surface contains empty visible token")
                    c[text] += 1
    return c


def line_shape(items_by_ms: Mapping[str, Sequence]) -> tuple:
    return tuple(
        (ms, it.item_id, it.leaf, li, len(line))
        for ms in MANUSCRIPTS
        for it in items_by_ms[ms]
        for li, line in enumerate(it.lines)
    )


def per_ms_counter(items_by_ms: Mapping[str, Sequence]) -> dict[str, collections.Counter]:
    return {
        ms: collections.Counter(
            stagea.token_text(tok)
            for it in items_by_ms[ms]
            for line in it.lines
            for tok in line
        )
        for ms in MANUSCRIPTS
    }


def replay_identity(crem: Path, nai: Path) -> tuple[dict, object, dict]:
    if stagea.git_blob_sha1(FI_PLAN_PATH.read_bytes()) != FI_PLAN_BLOB:
        raise RuntimeError("FI preregistration blob changed")
    if b1.sha256_file(b1.B0_PATH) != B0_SHA256:
        raise RuntimeError("Stage B0 authority changed")
    frozen_b0 = b1.load_b0()
    authority = stagea.check_external_authority(crem, nai)
    module = stagea.n64.load_naibbe(nai)
    original_map = dict(module.placeholder_to_glyph)
    parser = stagea.e.SlotParser()
    parser_validation = stagea.e.validate_parser(parser)
    sources = {
        name: stagea.b.parse_latin_manuscript(crem, name, rel)
        for name, rel in stagea.b.PRIMARY_MANUSCRIPTS.items()
    }

    out = {}
    per_ms = {}
    for mi, ms in enumerate(MANUSCRIPTS):
        seed = 6480000 + 100 * mi
        primary, _raw, diag = stagea.n64.encrypt_manuscript(
            module, sources[ms], ms, original_map, seed
        )
        psha = stagea.surface_sha(primary)
        if psha != stagea.EXPECTED_PRIMARY_SURFACE_SHA[ms]:
            raise RuntimeError(f"identity Stage-A surface changed for {ms}: {psha}")
        frozen = frozen_b0["reps"]["rep0"]["per_manuscript"][ms]
        if psha != frozen["primary_surface_sha256"]:
            raise RuntimeError(f"identity B0 surface changed for {ms}: {psha}")
        support = stagea.parser_support(primary, parser)
        exp = IDENTITY_BY_MS[ms]
        if int(support["visible_tokens"]) != exp["visible"] or int(support["accepted_tokens"]) != exp["accepted"]:
            raise RuntimeError(f"identity support changed for {ms}: {support}")
        out[ms] = primary
        per_ms[ms] = {
            "seed": seed,
            "primary_surface_sha256": psha,
            "visible_tokens": int(support["visible_tokens"]),
            "accepted_tokens": int(support["accepted_tokens"]),
            "coverage": float(support["coverage"]),
            "ambiguity_retries": int(diag["ambiguity_retries"]),
        }

    pooled = [it for ms in MANUSCRIPTS for it in out[ms]]
    psha = stagea.surface_sha(pooled)
    if psha != IDENTITY_SURFACE_SHA256:
        raise RuntimeError(f"identity pooled surface changed: {psha}")
    support = stagea.parser_support(pooled, parser)
    counter = token_counter(out)
    if sum(counter.values()) != IDENTITY_VISIBLE or len(counter) != IDENTITY_DISTINCT:
        raise RuntimeError("identity complete-token population changed")
    if int(support["accepted_tokens"]) != IDENTITY_ACCEPTED:
        raise RuntimeError("identity parser-accepted population changed")
    if abs(float(support["coverage"]) - IDENTITY_COVERAGE) > FLOAT_TOL:
        raise RuntimeError("identity coverage changed")

    audit = {
        "fi_plan_commit": FI_PLAN_COMMIT,
        "fi_plan_blob": FI_PLAN_BLOB,
        "stage_b0_sha256": B0_SHA256,
        "authority": authority,
        "parser_validation": parser_validation,
        "primary_pooled_surface_sha256": psha,
        "visible_tokens": IDENTITY_VISIBLE,
        "distinct_complete_tokens": IDENTITY_DISTINCT,
        "accepted_tokens": IDENTITY_ACCEPTED,
        "coverage": IDENTITY_COVERAGE,
        "per_manuscript": per_ms,
        "identity_measurement_frozen_from_stage_b1": {
            "E": IDENTITY_E,
            "R_ZL3b": IDENTITY_R["ZL3b"],
            "R_IT2a": IDENTITY_R["IT2a"],
            "sign_ZL3b": IDENTITY_SIGN["ZL3b"],
            "sign_IT2a": IDENTITY_SIGN["IT2a"],
            "T_identity": IDENTITY_T,
            "rescored_here": False,
        },
    }
    return out, parser, audit


def _rebuild_from_flat(identity_by_ms: Mapping[str, Sequence], flat_by_ms: Mapping[str, Sequence[str]]) -> dict:
    out = {ms: [] for ms in MANUSCRIPTS}
    cursor = {ms: 0 for ms in MANUSCRIPTS}
    for ms in MANUSCRIPTS:
        flat = flat_by_ms[ms]
        for it in identity_by_ms[ms]:
            lines = []
            for line in it.lines:
                n = len(line)
                vals = list(flat[cursor[ms]:cursor[ms] + n])
                cursor[ms] += n
                if len(vals) != n:
                    raise RuntimeError(f"allocation underflow for {ms}")
                lines.append(stagea.glyph_line(vals))
            out[ms].append(stagea.b.Item(it.item_id, ms, lines, it.leaf))
        if cursor[ms] != len(flat):
            raise RuntimeError(f"allocation refill cursor mismatch for {ms}")
    return out


def allocate(identity_by_ms: Mapping[str, Sequence], family: str, index: int) -> tuple[dict, dict]:
    if family not in FAMILIES or not 0 <= index < N_PERM:
        raise RuntimeError("FI family/index outside preregistered population")
    namespace = f"issue72v2:C1:{family}:allocation:{index}"
    rng = random.Random(stagea.stable_seed(namespace))

    before_global = token_counter(identity_by_ms)
    before_by_ms = per_ms_counter(identity_by_ms)
    identity_shape = line_shape(identity_by_ms)
    identity_flat_by_ms = {
        ms: [
            stagea.token_text(tok)
            for it in identity_by_ms[ms]
            for line in it.lines
            for tok in line
        ]
        for ms in MANUSCRIPTS
    }

    if family == "FI-G":
        global_flat = [tok for ms in MANUSCRIPTS for tok in identity_flat_by_ms[ms]]
        shuffled = list(global_flat)
        rng.shuffle(shuffled)
        cursor = 0
        flat_by_ms = {}
        for ms in MANUSCRIPTS:
            n = len(identity_flat_by_ms[ms])
            flat_by_ms[ms] = shuffled[cursor:cursor + n]
            cursor += n
        if cursor != len(shuffled):
            raise RuntimeError("FI-G global refill mismatch")
    else:
        flat_by_ms = {}
        for ms in MANUSCRIPTS:
            vals = list(identity_flat_by_ms[ms])
            rng.shuffle(vals)
            flat_by_ms[ms] = vals

    allocated = _rebuild_from_flat(identity_by_ms, flat_by_ms)
    after_global = token_counter(allocated)
    after_by_ms = per_ms_counter(allocated)
    if after_global != before_global:
        raise RuntimeError("FI global whole-token instance multiset changed")
    if line_shape(allocated) != identity_shape:
        raise RuntimeError("FI manuscript/item/line token-count skeleton changed")
    if family == "FI-M" and any(after_by_ms[ms] != before_by_ms[ms] for ms in MANUSCRIPTS):
        raise RuntimeError("FI-M manuscript token inventory changed")

    before_flat = [tok for ms in MANUSCRIPTS for tok in identity_flat_by_ms[ms]]
    after_flat = [tok for ms in MANUSCRIPTS for tok in flat_by_ms[ms]]
    changed = sum(a != b for a, b in zip(before_flat, after_flat))
    return allocated, {
        "family": family,
        "index": index,
        "allocation_namespace": namespace,
        "allocation_seed": stagea.stable_seed(namespace),
        "global_whole_token_instance_multiset_preserved": True,
        "manuscript_item_line_visible_token_counts_preserved": True,
        "per_manuscript_whole_token_instance_multisets_preserved": family == "FI-M",
        "visible_tokens": len(before_flat),
        "distinct_complete_tokens": len(before_global),
        "changed_token_slots": int(changed),
        "changed_token_slot_fraction": float(changed / len(before_flat)),
    }


def audit_allocated(allocated_by_ms: Mapping[str, Sequence], parser, family: str) -> tuple[list, dict, dict]:
    pooled = [it for ms in MANUSCRIPTS for it in allocated_by_ms[ms]]
    support = stagea.parser_support(pooled, parser)
    if int(support["visible_tokens"]) != IDENTITY_VISIBLE:
        raise RuntimeError("FI pooled visible token count changed")
    if int(support["accepted_tokens"]) != IDENTITY_ACCEPTED:
        raise RuntimeError("FI pooled parser-accepted token count changed")
    if abs(float(support["coverage"]) - IDENTITY_COVERAGE) > FLOAT_TOL:
        raise RuntimeError("FI pooled parser coverage changed")
    by_ms = {
        ms: {
            "surface_sha256": stagea.surface_sha(allocated_by_ms[ms]),
            "visible_tokens": int(support["by_document"][ms]["visible"]),
            "accepted_tokens": int(support["by_document"][ms]["accepted"]),
            "coverage": float(support["by_document"][ms]["coverage"]),
        }
        for ms in MANUSCRIPTS
    }
    if family == "FI-M":
        for ms in MANUSCRIPTS:
            exp = IDENTITY_BY_MS[ms]
            if by_ms[ms]["visible_tokens"] != exp["visible"] or by_ms[ms]["accepted_tokens"] != exp["accepted"]:
                raise RuntimeError(f"FI-M per-manuscript support changed for {ms}")
    dataset = d1.dataset_from_primary(pooled, parser, 0)
    if dataset["visible"] != IDENTITY_VISIBLE or dataset["parsed"] != IDENTITY_ACCEPTED:
        raise RuntimeError("FI dataset support disagrees with allocated surface")
    return pooled, dataset, {
        "primary_pooled_surface_sha256": stagea.surface_sha(pooled),
        "visible_tokens": IDENTITY_VISIBLE,
        "accepted_tokens": IDENTITY_ACCEPTED,
        "coverage": IDENTITY_COVERAGE,
        "fold_parsed_tokens": list(dataset["fold_counts"]),
        "line_count_with_parsed_token": int(dataset["line_count"]),
        "per_manuscript": by_ms,
        "FI_M_per_manuscript_accepted_count_invariance": family == "FI-M",
        "coverage_gate_applied": False,
    }


def main(argv: Sequence[str]) -> int:
    if len(argv) not in (6, 7):
        raise SystemExit(f"usage: {argv[0]} CREMMA_ROOT NAIBBE_ROOT FAMILY INDEX OUTPUT_JSON [--verify-only]")
    crem = Path(argv[1]).resolve()
    nai = Path(argv[2]).resolve()
    family = argv[3]
    index = int(argv[4])
    output = Path(argv[5]).resolve()
    verify_only = len(argv) == 7 and argv[6] == "--verify-only"
    if len(argv) == 7 and not verify_only:
        raise SystemExit("only optional flag is --verify-only")
    if family not in FAMILIES or index not in range(N_PERM):
        raise SystemExit("FAMILY must be FI-G/FI-M and INDEX must be 0..198")

    identity_by_ms, parser, identity_audit = replay_identity(crem, nai)
    allocated_by_ms, allocation = allocate(identity_by_ms, family, index)
    _pooled, dataset, surface_audit = audit_allocated(allocated_by_ms, parser, family)

    common = {
        "fi_plan_commit": FI_PLAN_COMMIT,
        "family": family,
        "index": index,
        "identity_audit": identity_audit,
        "allocation": allocation,
        "surface_audit": surface_audit,
        "T_identity": IDENTITY_T,
        "coverage_policy": "EXACT_INVARIANCE_DIAGNOSTIC_NO_HARD_SELECTION_GATE",
    }
    if verify_only:
        result = {
            "schema": "issue72-v2-stage-c1-fi-surface-preflight-v1",
            "status": "FI_ALLOCATION_SURFACE_VERIFIED_TARGET_BLIND",
            "scientific_role": "TARGET_BLIND_FI_ALLOCATION_REPLAY_PREFLIGHT",
            **common,
            "target_access": {
                "target_references_loaded": False,
                "slot_pair_Q_computed": False,
                "residual_Z_computed": False,
                "target_topology_computed": False,
                "FI_T_computed": False,
                "FI_randomization_pvalue_computed": False,
            },
        }
    else:
        targets, target_authority = b1.t68.load_target_references()
        real_q = b1.t68.q_views_candidate(dataset, dataset["X"], True)
        reference_namespace = f"issue72v2:C1:{family}:reference:{index}"
        measurement = b1.calibration(dataset, real_q, targets, reference_namespace)
        T = float(min(
            measurement["topology"]["ZL3b"]["pearson"],
            measurement["topology"]["IT2a"]["pearson"],
        ))
        result = {
            "schema": "issue72-v2-stage-c1-fi-r1-score-v1",
            "status": "FI_RANDOMIZATION_R1_FIRST_REVEAL_ASSIGNMENT_SCORED",
            "scientific_role": "FINAL_COMPLETE_TOKEN_ALLOCATION_R1_RANDOMIZATION_MEASUREMENT",
            **common,
            "target_authority": target_authority,
            "measurement": measurement,
            "T": T,
            "reference_namespace": reference_namespace,
            "n_reference": N_REF,
            "target_readings_averaged": False,
            "identity_rescored_here": False,
            "hard_topology_threshold_applied": False,
        }

    raw = json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(raw)
    print(json.dumps({
        "status": result["status"],
        "family": family,
        "index": index,
        "verify_only": verify_only,
        "identity_surface": identity_audit["primary_pooled_surface_sha256"],
        "allocated_surface": surface_audit["primary_pooled_surface_sha256"],
        "coverage": surface_audit["coverage"],
        "fold_parsed_tokens": surface_audit["fold_parsed_tokens"],
        "T": None if verify_only else result["T"],
        "R_ZL3b": None if verify_only else result["measurement"]["topology"]["ZL3b"]["pearson"],
        "R_IT2a": None if verify_only else result["measurement"]["topology"]["IT2a"]["pearson"],
        "output_sha256": sha256_bytes(raw),
    }, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
