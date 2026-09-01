#!/usr/bin/env python3
"""Aggregate the preregistered Issue #72 V2 FI-G/FI-M first-reveal population."""
from __future__ import annotations

import glob
import json
import math
import statistics
import sys
from pathlib import Path
from typing import Mapping, Sequence

FAMILIES = ("FI-G", "FI-M")
N_PERM = 199
EXPECTED = {(f, i) for f in FAMILIES for i in range(N_PERM)}
FI_PLAN_COMMIT = "a053efd9803b6c0f74614986289c54a8add7d904"
IDENTITY_T = 0.8830282501011794
IDENTITY_R = {"ZL3b": 0.8830282501011794, "IT2a": 0.9000974100381157}
IDENTITY_E = 3.1784043855151296
IDENTITY_COVERAGE = 0.886370405671055
IDENTITY_ACCEPTED_BY_MS = {"BIS193": 11346, "CLM13027": 9716, "Mazarine915": 6659, "UBL758": 2038}
B1_T_RANGE = [0.857780, 0.883028]


def quantile(xs, p):
    ys = sorted(float(x) for x in xs)
    z = (len(ys) - 1) * p
    lo = int(math.floor(z))
    hi = int(math.ceil(z))
    if lo == hi:
        return ys[lo]
    return ys[lo] * (hi - z) + ys[hi] * (z - lo)


def mad(xs):
    med = statistics.median(xs)
    return float(statistics.median(abs(float(x) - med) for x in xs))


def summary(xs):
    ys = [float(x) for x in xs]
    return {
        "n": len(ys),
        "mean": float(statistics.fmean(ys)),
        "median": float(statistics.median(ys)),
        "MAD": mad(ys),
        "min": min(ys),
        "q25": quantile(ys, 0.25),
        "q75": quantile(ys, 0.75),
        "max": max(ys),
        "sd_population": float(statistics.pstdev(ys)),
    }


def holm_two(raw: Mapping[str, float]) -> dict[str, float]:
    ordered = sorted(raw, key=lambda f: (raw[f], f))
    first, second = ordered
    first_adj = min(1.0, 2.0 * raw[first])
    second_adj = min(1.0, max(first_adj, raw[second]))
    return {first: float(first_adj), second: float(second_adj)}


def validate(r: Mapping, key: tuple[str, int]) -> None:
    family, index = key
    if r.get("schema") != "issue72-v2-stage-c1-fi-r1-score-v1":
        raise RuntimeError(f"bad score schema {key}")
    if r.get("status") != "FI_RANDOMIZATION_R1_FIRST_REVEAL_ASSIGNMENT_SCORED":
        raise RuntimeError(f"bad score status {key}")
    if r.get("fi_plan_commit") != FI_PLAN_COMMIT:
        raise RuntimeError(f"FI plan authority changed {key}")
    if r.get("family") != family or int(r.get("index", -1)) != index:
        raise RuntimeError(f"FI assignment identity changed {key}")
    if r.get("allocation", {}).get("allocation_namespace") != f"issue72v2:C1:{family}:allocation:{index}":
        raise RuntimeError(f"allocation namespace changed {key}")
    if r.get("reference_namespace") != f"issue72v2:C1:{family}:reference:{index}":
        raise RuntimeError(f"reference namespace changed {key}")
    if int(r.get("n_reference", -1)) != 1000:
        raise RuntimeError(f"reference count changed {key}")
    if float(r.get("T_identity")) != IDENTITY_T:
        raise RuntimeError(f"identity T changed {key}")
    if r.get("target_readings_averaged") is not False or r.get("identity_rescored_here") is not False:
        raise RuntimeError(f"FI measurement policy changed {key}")
    if r.get("hard_topology_threshold_applied") is not False:
        raise RuntimeError(f"FI hard threshold applied {key}")
    ia = r["identity_audit"]
    if ia["primary_pooled_surface_sha256"] != "47d52d28d4e2ac126bb8681c881ec339cb339c9b1bb329fb48263e6c1e9758bd":
        raise RuntimeError(f"identity surface changed {key}")
    if ia["visible_tokens"] != 33574 or ia["accepted_tokens"] != 29759 or ia["distinct_complete_tokens"] != 7146:
        raise RuntimeError(f"identity population changed {key}")
    sa = r["surface_audit"]
    if sa["visible_tokens"] != 33574 or sa["accepted_tokens"] != 29759:
        raise RuntimeError(f"FI pooled support changed {key}")
    if float(sa["coverage"]) != IDENTITY_COVERAGE:
        raise RuntimeError(f"FI pooled coverage changed {key}")
    if family == "FI-M":
        if sa.get("FI_M_per_manuscript_accepted_count_invariance") is not True:
            raise RuntimeError(f"FI-M invariance flag changed {key}")
        got = {m: int(sa["per_manuscript"][m]["accepted_tokens"]) for m in IDENTITY_ACCEPTED_BY_MS}
        if got != IDENTITY_ACCEPTED_BY_MS:
            raise RuntimeError(f"FI-M accepted counts changed {key}: {got}")
    T = float(r["T"])
    rz = float(r["measurement"]["topology"]["ZL3b"]["pearson"])
    ri = float(r["measurement"]["topology"]["IT2a"]["pearson"])
    if not all(math.isfinite(x) for x in (T, rz, ri)) or abs(T - min(rz, ri)) > 1e-15:
        raise RuntimeError(f"FI T mismatch {key}")


def main(argv: Sequence[str]) -> int:
    if len(argv) != 4:
        raise SystemExit(f"usage: {argv[0]} INPUT_DIR OUTPUT_JSON SCIENTIFIC_HEAD")
    inp = Path(argv[1]).resolve()
    out = Path(argv[2]).resolve()
    scientific_head = argv[3].strip()
    paths = sorted(glob.glob(str(inp / "FI-*_*.json")))
    if len(paths) != 2 * N_PERM:
        raise RuntimeError(f"need exactly 398 FI results, found {len(paths)}")
    rows = {}
    target_authority = None
    for p in paths:
        r = json.loads(Path(p).read_text(encoding="utf-8"))
        key = (str(r.get("family")), int(r.get("index", -1)))
        if key not in EXPECTED or key in rows:
            raise RuntimeError(f"unexpected/duplicate FI result {key}")
        validate(r, key)
        if target_authority is None:
            target_authority = r["target_authority"]
        elif r["target_authority"] != target_authority:
            raise RuntimeError("FI target authority differs across assignments")
        rows[key] = r
    if set(rows) != EXPECTED:
        raise RuntimeError("FI complete population mismatch")

    family_results = {}
    raw_p = {}
    for family in FAMILIES:
        rs = [rows[(family, i)] for i in range(N_PERM)]
        Ts = [float(r["T"]) for r in rs]
        n_ge = sum(t >= IDENTITY_T for t in Ts)
        raw = float((1 + n_ge) / 200)
        raw_p[family] = raw
        fam = {
            "n_perm": N_PERM,
            "T_identity": IDENTITY_T,
            "T_randomization": summary(Ts),
            "n_T_ge_identity": int(n_ge),
            "raw_p": raw,
            "identity_upper_tail_rank_with_plus_one": int(1 + n_ge),
            "identity_percentile_vs_randomizations": float(100.0 * sum(t <= IDENTITY_T for t in Ts) / N_PERM),
            "Delta_T_identity_minus_randomization_median": float(IDENTITY_T - statistics.median(Ts)),
            "R_ZL3b": summary([r["measurement"]["topology"]["ZL3b"]["pearson"] for r in rs]),
            "R_IT2a": summary([r["measurement"]["topology"]["IT2a"]["pearson"] for r in rs]),
            "sign_ZL3b": summary([r["measurement"]["topology"]["ZL3b"]["sign_agreement"] for r in rs]),
            "sign_IT2a": summary([r["measurement"]["topology"]["IT2a"]["sign_agreement"] for r in rs]),
            "residual_energy": summary([r["measurement"]["residual_energy"] for r in rs]),
            "pooled_coverage": summary([r["surface_audit"]["coverage"] for r in rs]),
            "changed_token_slot_fraction": summary([r["allocation"]["changed_token_slot_fraction"] for r in rs]),
        }
        if family == "FI-G":
            fam["accepted_tokens_by_manuscript"] = {
                m: summary([r["surface_audit"]["per_manuscript"][m]["accepted_tokens"] for r in rs])
                for m in IDENTITY_ACCEPTED_BY_MS
            }
        else:
            fam["per_manuscript_accepted_count_invariance"] = {
                "all_199_exact": all(
                    {m: int(r["surface_audit"]["per_manuscript"][m]["accepted_tokens"]) for m in IDENTITY_ACCEPTED_BY_MS}
                    == IDENTITY_ACCEPTED_BY_MS
                    for r in rs
                ),
                "identity_counts": IDENTITY_ACCEPTED_BY_MS,
            }
        family_results[family] = fam

    adjusted = holm_two(raw_p)
    for family in FAMILIES:
        family_results[family]["holm_adjusted_p"] = adjusted[family]
        family_results[family]["supported_at_FWER_0_05"] = adjusted[family] <= 0.05

    g = family_results["FI-G"]["supported_at_FWER_0_05"]
    m = family_results["FI-M"]["supported_at_FWER_0_05"]
    if g and m:
        classification = "WITHIN_MANUSCRIPT_PLACEMENT_CONTRIBUTES_BEYOND_MANUSCRIPT_INVENTORY"
    elif g and not m:
        classification = "MANUSCRIPT_INVENTORY_ALLOCATION_CONTRIBUTES_WITHOUT_DETECTED_EXTRA_WITHIN_MANUSCRIPT_PLACEMENT"
    elif not g and not m:
        classification = "FINAL_COMPLETE_TOKEN_INVENTORY_SUFFICIENT_UNDER_TESTED_FI_CONTROLS"
    else:
        classification = "ALLOCATION_DECOMPOSITION_INCONCLUSIVE"

    result = {
        "schema": "issue72-v2-stage-c1-fi-aggregate-v1",
        "status": "FI_COMPLETE_RANDOMIZATION_POPULATION_AGGREGATED",
        "scientific_head": scientific_head,
        "fi_plan_commit": FI_PLAN_COMMIT,
        "population": {
            "families": list(FAMILIES),
            "n_perm_per_family": N_PERM,
            "total_results": 398,
            "complete_population": True,
            "no_drops": True,
            "no_rerolls": True,
        },
        "identity": {
            "T": IDENTITY_T,
            "R_ZL3b": IDENTITY_R["ZL3b"],
            "R_IT2a": IDENTITY_R["IT2a"],
            "E": IDENTITY_E,
            "coverage": IDENTITY_COVERAGE,
        },
        "target_authority": target_authority,
        "families": family_results,
        "multiplicity": {
            "method": "Holm step-down across exactly FI-G and FI-M",
            "family_wise_alpha": 0.05,
            "raw_p": raw_p,
            "adjusted_p": adjusted,
        },
        "classification": classification,
        "B1_unchanged_Naibbe_context": {
            "T_range_descriptive_only": B1_T_RANGE,
            "decision_boundary": False,
        },
        "guardrails": {
            "coverage_gate_applied": False,
            "arbitrary_T_gate_applied": False,
            "global_R1_PASS_FAIL_assigned": False,
            "target_readings_averaged": False,
            "post_reveal_family_added": False,
        },
    }
    raw = json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(raw, encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "scientific_head": scientific_head,
        "raw_p": raw_p,
        "adjusted_p": adjusted,
        "classification": classification,
        "T_median": {f: family_results[f]["T_randomization"]["median"] for f in FAMILIES},
        "Delta_T": {f: family_results[f]["Delta_T_identity_minus_randomization_median"] for f in FAMILIES},
    }, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
