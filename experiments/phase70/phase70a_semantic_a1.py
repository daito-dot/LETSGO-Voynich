#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import math
import random
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PHASE61 = ROOT / "experiments" / "phase61"
PHASE64 = ROOT / "experiments" / "phase64"
PHASE69 = ROOT / "experiments" / "phase69"
for p in (PHASE61, PHASE64, PHASE69):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import phase61c_joint_model as a1  # noqa: E402
import phase64b_naibbe as core  # noqa: E402
import phase69a_adaptive_naibbe as p69  # noqa: E402

REPS = 5
BASE_SEED = 7000000
TIE_EPS = 1e-12


class ModelBlocked(RuntimeError):
    pass


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def candidate_distribution(rows: Sequence[Tuple[str, float]], multiplier=None):
    out = []
    for glyph, base_weight in rows:
        w = float(base_weight)
        if multiplier is not None:
            w *= float(multiplier(glyph))
        out.append((glyph, w))
    return out


def max_share(rows: Sequence[Tuple[str, float]]) -> float:
    if not rows:
        return 0.0
    den = sum(w for _g, w in rows)
    return max(w for _g, w in rows) / den if den else 0.0


def encrypt_pair_for_fold(
    module,
    source_items: Sequence[core.b.Item],
    manuscript: str,
    fold: int,
    mi: int,
    rep: int,
    catalog: Dict[str, List[Tuple[str, float]]],
    inverse: Dict[str, set],
    shape_scores: dict,
    entry_strength: float,
    local_p: float,
):
    base = BASE_SEED + 100000 * fold + 100 * mi + rep
    seg_rng = random.Random(base)
    sc0_rng = random.Random(base + 10000)
    sc1_rng = random.Random(base + 20000)
    space0_rng = random.Random(base + 30000)
    space1_rng = random.Random(base + 30000)
    local_rng = random.Random(base + 40000)

    primary0: List[core.b.Item] = []
    primary1: List[core.b.Item] = []
    raw0: List[core.b.Item] = []
    raw1: List[core.b.Item] = []

    diag = {
        "fold": fold,
        "base_seed": base,
        "entry_strength": entry_strength,
        "local_p": local_p,
        "plaintext_units": 0,
        "entry_units": 0,
        "body_units": 0,
        "local_candidate_opportunities": 0,
        "local_activations": 0,
        "local_activation_with_opportunity": 0,
        "selected_local_hits": 0,
        "sc0_decode_correct": 0,
        "sc1_decode_correct": 0,
        "decode_total_each_arm": 0,
        "entry_base_max_share_sum": 0.0,
        "entry_a1_max_share_sum": 0.0,
        "entry_selected_positive_shape_score": 0,
        "entry_selected_score_sum": 0.0,
    }

    def entry_multiplier(glyph: str) -> float:
        score = shape_scores.get(a1.shape(glyph), 0.0)
        return math.exp(entry_strength * score)

    for item in source_items:
        recent1: List[str] = []
        p0_lines = []
        p1_lines = []
        r0_lines = []
        r1_lines = []

        for li, line in enumerate(item.lines):
            source = core.string_line(line)
            published_cleaned = module.clean_line(source)
            cleaned, _dropped = core.project_effective_plaintext(published_cleaned)
            units = p69.segment_plaintext(cleaned, seg_rng, module.RESPACING) if cleaned else []
            diag["plaintext_units"] += len(units)
            out0: List[str] = []
            out1: List[str] = []

            for unit in units:
                rows = catalog.get(unit)
                if not rows:
                    raise ModelBlocked(f"missing candidate set for {unit!r}")

                g0 = p69.weighted_choice(rows, sc0_rng)

                if li == 0:
                    diag["entry_units"] += 1
                    erows = candidate_distribution(rows, entry_multiplier)
                    diag["entry_base_max_share_sum"] += max_share(rows)
                    diag["entry_a1_max_share_sum"] += max_share(erows)
                    g1 = p69.weighted_choice(erows, sc1_rng)
                    selected_score = shape_scores.get(a1.shape(g1), 0.0)
                    diag["entry_selected_score_sum"] += selected_score
                    diag["entry_selected_positive_shape_score"] += int(selected_score > 0)
                else:
                    diag["body_units"] += 1
                    local_rows = [
                        (glyph, weight)
                        for glyph, weight in rows
                        if any(p69.lev1_str(glyph, prev) for prev in recent1[-10:])
                    ]
                    if local_rows:
                        diag["local_candidate_opportunities"] += 1
                    activated = local_rng.random() < local_p
                    if activated:
                        diag["local_activations"] += 1
                    if activated and local_rows:
                        diag["local_activation_with_opportunity"] += 1
                        g1 = p69.weighted_choice(local_rows, sc1_rng)
                        if not any(p69.lev1_str(g1, prev) for prev in recent1[-10:]):
                            raise AssertionError("selected SC1 local candidate is not edit1 to recent history")
                        diag["selected_local_hits"] += 1
                    else:
                        g1 = p69.weighted_choice(rows, sc1_rng)

                out0.append(g0)
                out1.append(g1)
                recent1.append(g1)
                if len(recent1) > 10:
                    recent1 = recent1[-10:]

                diag["decode_total_each_arm"] += 1
                diag["sc0_decode_correct"] += int(inverse.get(g0) == {unit})
                diag["sc1_decode_correct"] += int(inverse.get(g1) == {unit})

            r0_lines.append(p69.glyph_line(out0))
            r1_lines.append(p69.glyph_line(out1))
            p0_lines.append(p69.glyph_line(p69.respace_tokens(out0, space0_rng, module.SPACE_REMOVAL_RATE)))
            p1_lines.append(p69.glyph_line(p69.respace_tokens(out1, space1_rng, module.SPACE_REMOVAL_RATE)))

        raw0.append(core.b.Item(item.item_id, manuscript, r0_lines, None))
        raw1.append(core.b.Item(item.item_id, manuscript, r1_lines, None))
        primary0.append(core.b.Item(item.item_id, manuscript, p0_lines, None))
        primary1.append(core.b.Item(item.item_id, manuscript, p1_lines, None))

    n = diag["decode_total_each_arm"]
    diag["sc0_decode_accuracy"] = diag["sc0_decode_correct"] / n if n else None
    diag["sc1_decode_accuracy"] = diag["sc1_decode_correct"] / n if n else None
    diag["local_opportunity_fraction_body"] = (
        diag["local_candidate_opportunities"] / diag["body_units"] if diag["body_units"] else 0.0
    )
    diag["local_activation_fraction_body"] = (
        diag["local_activations"] / diag["body_units"] if diag["body_units"] else 0.0
    )
    diag["local_selected_hit_fraction_body"] = (
        diag["selected_local_hits"] / diag["body_units"] if diag["body_units"] else 0.0
    )
    diag["entry_base_mean_max_share"] = (
        diag["entry_base_max_share_sum"] / diag["entry_units"] if diag["entry_units"] else 0.0
    )
    diag["entry_a1_mean_max_share"] = (
        diag["entry_a1_max_share_sum"] / diag["entry_units"] if diag["entry_units"] else 0.0
    )
    diag["entry_selected_mean_shape_score"] = (
        diag["entry_selected_score_sum"] / diag["entry_units"] if diag["entry_units"] else 0.0
    )
    diag["entry_selected_positive_shape_fraction"] = (
        diag["entry_selected_positive_shape_score"] / diag["entry_units"] if diag["entry_units"] else 0.0
    )

    if diag["local_activation_with_opportunity"] != diag["selected_local_hits"]:
        raise AssertionError("local activation/opportunity hit mismatch")
    if diag["sc0_decode_accuracy"] != 1.0 or diag["sc1_decode_accuracy"] != 1.0:
        raise ModelBlocked("raw reversibility failure")

    return {
        "SC0": {"primary": primary0, "raw": raw0},
        "SC1": {"primary": primary1, "raw": raw1},
        "diagnostics": diag,
    }


def aggregate_fold_arm(per_ms: Dict[str, Dict[str, dict]], label: str):
    ms_aggs = {
        ms: core.aggregate_realizations(reps, f"{label}:{ms}")
        for ms, reps in per_ms.items()
    }
    return {
        "per_manuscript": ms_aggs,
        "aggregate": core.aggregate_manuscripts(ms_aggs, f"{label}:equal-manuscript"),
    }


def strict_wins(a, b):
    return sum(x + TIE_EPS < y for x, y in zip(a, b))


def evaluate_fold_specific(fold_aggregates, contexts, phase63a, label):
    rows = []
    for ctx in contexts:
        fi = ctx["fold"]
        agg = fold_aggregates[str(fi)]["aggregate"]
        cand = {
            "S1": agg["S1_by_fold"][str(fi)],
            "S2": agg["S2"],
            "S3": agg["S3"],
        }
        comp = {
            "D_profile": core.p.profile_distance(agg["H62P1"], ctx["target_H62P1"]),
            "abs_C_short_diff": core.p.c_short_diff(agg["H62P1"], ctx["target_H62P1"]),
        }
        rows.append({
            "fold": fi,
            "test_leaves": ctx["test_leaves"],
            "target_exposed": ctx["target_exposed"],
            "candidate_exposed": cand,
            "candidate_exposed_ratios": {
                k: cand[k] / ctx["target_exposed"][k] for k in ("S1", "S2", "S3")
            },
            "candidate_H62_comparison": comp,
            "baseline_H62_comparisons": ctx["baseline_H62"],
        })

    target_mean = {
        k: float(np.mean([r["target_exposed"][k] for r in rows])) for k in ("S1", "S2", "S3")
    }
    candidate_mean = {
        k: float(np.mean([r["candidate_exposed"][k] for r in rows])) for k in ("S1", "S2", "S3")
    }
    ratios = {k: candidate_mean[k] / target_mean[k] for k in candidate_mean}
    exposed_gate = {k: 0.5 <= ratios[k] <= 2.0 for k in ratios}

    d = [r["candidate_H62_comparison"]["D_profile"] for r in rows]
    cs = [r["candidate_H62_comparison"]["abs_C_short_diff"] for r in rows]
    h62 = {
        "mean_D_profile": float(np.mean(d)),
        "median_D_profile": float(statistics.median(d)),
        "mean_abs_C_short_diff": float(np.mean(cs)),
        "D_profile_fold_values": d,
        "abs_C_short_diff_fold_values": cs,
    }

    base_summary = phase63a["across_fold"]["committed_H62P1_baseline_summaries"]
    viability_means = {}
    viability_wins = {}
    for base in ("N0", "C0"):
        bd = [r["baseline_H62_comparisons"][base]["D_profile"] for r in rows]
        bc = [r["baseline_H62_comparisons"][base]["abs_C_short_diff"] for r in rows]
        viability_means[base] = {
            "lower_mean_D_profile": h62["mean_D_profile"] + TIE_EPS < base_summary[base]["mean_D_profile"],
            "lower_mean_abs_C_short_diff": h62["mean_abs_C_short_diff"] + TIE_EPS < base_summary[base]["mean_abs_C_short_diff"],
        }
        viability_wins[base] = {
            "D_profile_wins": strict_wins(d, bd),
            "abs_C_short_diff_wins": strict_wins(cs, bc),
        }

    h62_viable = (
        all(v["lower_mean_D_profile"] and v["lower_mean_abs_C_short_diff"] for v in viability_means.values())
        and all(v["D_profile_wins"] >= 3 and v["abs_C_short_diff_wins"] >= 3 for v in viability_wins.values())
    )

    a1_d = [r["baseline_H62_comparisons"]["A1_R1"]["D_profile"] for r in rows]
    a1_c = [r["baseline_H62_comparisons"]["A1_R1"]["abs_C_short_diff"] for r in rows]
    a1_summary = phase63a["across_fold"]["A1_R1_H62P1_summary"]
    a1_reference = {
        "mean_D_profile": a1_summary["mean_D_profile"],
        "median_D_profile": a1_summary["median_D_profile"],
        "mean_abs_C_short_diff": a1_summary["mean_abs_C_short_diff"],
        "candidate_lower_mean_D": h62["mean_D_profile"] + TIE_EPS < a1_summary["mean_D_profile"],
        "candidate_D_fold_wins": strict_wins(d, a1_d),
        "candidate_lower_mean_C_short_error": h62["mean_abs_C_short_diff"] + TIE_EPS < a1_summary["mean_abs_C_short_diff"],
        "candidate_C_short_fold_wins": strict_wins(cs, a1_c),
    }

    return {
        "label": label,
        "folds": rows,
        "target_exposed_mean": target_mean,
        "candidate_exposed_mean": candidate_mean,
        "ratio_of_means_to_voynich": ratios,
        "exposed_gate_0.5_to_2.0": exposed_gate,
        "exposed_gate_pass": all(exposed_gate.values()),
        "H62P1_summary": h62,
        "H62_viability_mean_superiority": viability_means,
        "H62_viability_fold_wins": viability_wins,
        "H62_viable_vs_N0_C0": h62_viable,
        "A1_R1_reference_only": a1_reference,
        "broad_regime_pass": bool(all(exposed_gate.values()) and h62_viable),
    }


def compute(voynich_path: Path, cremma_root: Path, naibbe_root: Path):
    module = core.load_naibbe(naibbe_root)
    glyph_map = dict(module.placeholder_to_glyph)
    core.set_glyph_map(module, glyph_map)
    catalog, inverse, cardinality = p69.build_candidate_catalog(module, glyph_map)
    if any(len(v) != 1 for v in inverse.values()):
        raise ModelBlocked("candidate catalog is not uniquely reversible")

    phase61 = load_json(PHASE61 / "phase61c_results.json")
    phase62c = load_json(core.PHASE62 / "phase62c_c0_a1_results.json")
    phase63a = load_json(core.PHASE63 / "phase63a_training_vocab_results.json")
    contexts, _vitems = core.fold_contexts(voynich_path, phase62c, phase63a)

    paragraphs, _headers = a1.parse(str(voynich_path))
    a1_folds = a1.physical_leaf_folds(paragraphs)
    if len(a1_folds) != 5:
        raise RuntimeError("Phase61 parser did not produce five folds")

    candidate_glyphs = sorted(inverse)
    raw_sources = {
        name: core.b.parse_latin_manuscript(cremma_root, name, rel)
        for name, rel in core.b.PRIMARY_MANUSCRIPTS.items()
    }

    fold_outputs = {"SC0": {}, "SC1": {}}
    diagnostics = {}

    for fi, ctx in enumerate(contexts):
        if sorted(a1_folds[fi]) != sorted(ctx["test_leaves"]):
            raise RuntimeError(f"fold leaf mismatch at {fi}")
        frozen = phase61["folds"][fi]
        if sorted(frozen["test_leaves"] if "test_leaves" in frozen else ctx["test_leaves"]) != sorted(ctx["test_leaves"]):
            raise RuntimeError(f"Phase61 result fold mismatch at {fi}")
        entry_strength = float(frozen["selected"]["entry_strength"])
        local_p = float(frozen["selected"]["local_family_p"])
        if entry_strength != 0.5 or local_p not in (0.2, 0.3):
            raise RuntimeError(f"unexpected historical A1 parameter at fold {fi}")

        train = a1.subset(paragraphs, a1_folds[fi], include=False)
        shape_scores = a1.learn_shape_scores(train, candidate_glyphs)

        per_arm = {
            "SC0": {"primary": {}, "raw": {}},
            "SC1": {"primary": {}, "raw": {}},
        }
        diagnostics[str(fi)] = {}

        for mi, manuscript in enumerate(core.MANUSCRIPTS):
            diagnostics[str(fi)][manuscript] = {}
            for r in range(REPS):
                pair = encrypt_pair_for_fold(
                    module,
                    raw_sources[manuscript],
                    manuscript,
                    fi,
                    mi,
                    r,
                    catalog,
                    inverse,
                    shape_scores,
                    entry_strength,
                    local_p,
                )
                diagnostics[str(fi)][manuscript][f"rep{r}"] = pair["diagnostics"]
                primary_label = f"Phase70:paired:fold{fi}:{manuscript}:rep{r}:primary"
                raw_label = f"Phase70:paired:fold{fi}:{manuscript}:rep{r}:raw"
                for arm in ("SC0", "SC1"):
                    per_arm[arm]["primary"].setdefault(manuscript, {})[f"rep{r}"] = core.output_metrics(
                        pair[arm]["primary"], primary_label, contexts
                    )
                    per_arm[arm]["raw"].setdefault(manuscript, {})[f"rep{r}"] = core.output_metrics(
                        pair[arm]["raw"], raw_label, contexts
                    )

        for arm in ("SC0", "SC1"):
            fold_outputs[arm][str(fi)] = {
                "primary": aggregate_fold_arm(per_arm[arm]["primary"], f"Phase70:{arm}:fold{fi}:primary"),
                "raw": aggregate_fold_arm(per_arm[arm]["raw"], f"Phase70:{arm}:fold{fi}:raw"),
                "frozen_A1_parameters": {
                    "entry_strength": entry_strength,
                    "local_family_p": local_p,
                },
            }

    evaluations = {}
    for arm in ("SC0", "SC1"):
        evaluations[arm] = {
            "primary": evaluate_fold_specific(
                {f: row["primary"] for f, row in fold_outputs[arm].items()},
                contexts,
                phase63a,
                f"Phase70:{arm}:primary",
            ),
            "raw": evaluate_fold_specific(
                {f: row["raw"] for f, row in fold_outputs[arm].items()},
                contexts,
                phase63a,
                f"Phase70:{arm}:raw",
            ),
        }

    sc0 = evaluations["SC0"]["primary"]
    sc1 = evaluations["SC1"]["primary"]
    paired = {
        "S1_abs_ratio_error_lower": abs(sc1["ratio_of_means_to_voynich"]["S1"] - 1.0) + TIE_EPS < abs(sc0["ratio_of_means_to_voynich"]["S1"] - 1.0),
        "S2_abs_ratio_error_lower": abs(sc1["ratio_of_means_to_voynich"]["S2"] - 1.0) + TIE_EPS < abs(sc0["ratio_of_means_to_voynich"]["S2"] - 1.0),
        "mean_D_profile_lower": sc1["H62P1_summary"]["mean_D_profile"] + TIE_EPS < sc0["H62P1_summary"]["mean_D_profile"],
        "mean_abs_C_short_diff_lower": sc1["H62P1_summary"]["mean_abs_C_short_diff"] + TIE_EPS < sc0["H62P1_summary"]["mean_abs_C_short_diff"],
    }
    paired["pass"] = all(paired.values())

    counts = Counter()
    entry_base_shares = []
    entry_a1_shares = []
    for ff in diagnostics.values():
        for mm in ff.values():
            for d in mm.values():
                for k in (
                    "plaintext_units", "entry_units", "body_units",
                    "local_candidate_opportunities", "local_activations",
                    "local_activation_with_opportunity", "selected_local_hits",
                    "sc0_decode_correct", "sc1_decode_correct", "decode_total_each_arm",
                ):
                    counts[k] += d[k]
                entry_base_shares.append(d["entry_base_mean_max_share"])
                entry_a1_shares.append(d["entry_a1_mean_max_share"])

    decode_n = counts["decode_total_each_arm"]
    if counts["sc0_decode_correct"] != decode_n or counts["sc1_decode_correct"] != decode_n:
        raise ModelBlocked("aggregate reversibility failure")

    if sc1["broad_regime_pass"] and paired["pass"]:
        classification = "P70-SC1 REVERSIBLE SEMANTIC COMPATIBILITY DEMONSTRATED"
    elif sc1["broad_regime_pass"]:
        classification = "P70-SC1 COMPATIBILITY PASS BUT A1-SURFACE CAUSALITY UNCLEAR"
    elif paired["pass"]:
        classification = "P70-SC1 PARTIAL COMPATIBILITY"
    else:
        classification = "P70-SC1 NOT COMPATIBLE UNDER THIS CONSTRUCTION"

    return {
        "phase": "70A",
        "hypothesis": "P70-SC1 frozen A1 surface over uniquely reversible meaningful plaintext",
        "classification": classification,
        "inputs": {
            "cremma_commit": core.b.verify_cremma_commit(cremma_root),
            "naibbe_commit": core.NAIBBE_COMMIT,
            "candidate_catalog_units": len(catalog),
            "candidate_cipher_tokens": len(inverse),
            "candidate_cardinality_min": min(cardinality.values()),
            "candidate_cardinality_max": max(cardinality.values()),
            "realizations_per_manuscript_per_fold": REPS,
            "phase61_fold_parameters": [row["selected"] for row in phase61["folds"]],
        },
        "reversibility_and_utilization": {
            "aggregate_counts": dict(counts),
            "SC0_decode_accuracy": counts["sc0_decode_correct"] / decode_n,
            "SC1_decode_accuracy": counts["sc1_decode_correct"] / decode_n,
            "local_opportunity_fraction_body": counts["local_candidate_opportunities"] / counts["body_units"],
            "local_activation_fraction_body": counts["local_activations"] / counts["body_units"],
            "selected_local_hit_fraction_body": counts["selected_local_hits"] / counts["body_units"],
            "mean_entry_base_max_candidate_share": float(np.mean(entry_base_shares)),
            "mean_entry_A1_weighted_max_candidate_share": float(np.mean(entry_a1_shares)),
            "per_fold_manuscript_realization": diagnostics,
        },
        "fold_outputs": fold_outputs,
        "evaluations": evaluations,
        "paired_A1_surface_causal_check": paired,
        "claim_limit": "semantic compatibility construction only; it deliberately borrows frozen A1 training-side parameters and is not an independent historical cipher hypothesis",
    }


def main() -> int:
    if len(sys.argv) != 4:
        print(f"usage: {sys.argv[0]} ZL3b-n.txt /path/to/CREMMA /path/to/naibbe", file=sys.stderr)
        return 2
    captured = io.StringIO()
    with contextlib.redirect_stdout(captured):
        out = compute(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve())
    stdout = captured.getvalue()
    out["execution_stdout_audit"] = {
        "captured_characters": len(stdout),
        "sha256": hashlib.sha256(stdout.encode("utf-8")).hexdigest(),
        "used_for_scoring": False,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
