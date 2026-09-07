#!/usr/bin/env python3
"""Issue #172 historical-anchor first-reveal scorer.

This file is the scorer-only commit required by the frozen Stage0 chronology.
It contains a score-free runtime preflight and the complete first-reveal scoring
path for the two promotion-relevant historical anchors, A1/A1-R1 and Naibbe
C1-E0.  No workflow is defined here.

The scientific contract is FIRST_REVEAL_TARGET_PLAN.md.  Existing historical
results are reused only where that plan explicitly permits carry-forward (R2,
R9 and frozen target reference bands).  New candidate-surface responsibilities
are evaluated from the immutable primary surfaces without refitting generation.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import math
import subprocess
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Mapping, Sequence

import numpy as np

HERE = Path(__file__).resolve()
ROOT = HERE.parents[2]
EXP = ROOT / "experiments"
JMD = EXP / "joint-mechanism-discrimination"
JCT = EXP / "joint-constraint-tournament"
P4A_DIR = EXP / "predictive-information" / "phase4a"
EDGE_DIR = EXP / "predictive-information" / "common-eva-edge"
CURRIER_DIR = EXP / "predictive-information" / "common-eva-currier"
PRED_DIR = EXP / "predictive-information"
P2B_DIR = PRED_DIR / "phase2b"

for p in (JCT, P4A_DIR, EDGE_DIR, CURRIER_DIR, P2B_DIR, PRED_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import preflight68 as P68  # noqa: E402
import phase4a_boundary_first_reveal as R1A  # noqa: E402
import issue145_common_eva_first_reveal as E145  # noqa: E402
import issue155_common_eva_currier_gate0 as G155  # noqa: E402
import issue155_common_eva_currier_first_reveal as S155  # noqa: E402
import issue161_outcome_factor_gate0 as G161  # noqa: E402
import issue161_outcome_factor_first_reveal as S161  # noqa: E402
import issue167_sparse_currier_gate0 as G167  # noqa: E402
import issue167_sparse_currier_first_reveal as S167  # noqa: E402
import phase2b_boundary_localization as B2  # noqa: E402
import source_order_authority as SOURCE_ORDER  # noqa: E402

# ---- frozen Issue172 authority ------------------------------------------------
STAGE0_PLAN_PATH = JMD / "STAGE0_AUTHORITY_PLAN.md"
STAGE0_MANIFEST_PATH = JMD / "authority_manifest_v1.json"
STAGE0_CHECKER_PATH = JMD / "stage0_gate.py"
TARGET_PLAN_PATH = JMD / "FIRST_REVEAL_TARGET_PLAN.md"

EXPECTED_BLOBS = {
    "stage0_plan": "638e212e22aaa313fd85ab80103528ce4cfada9f",
    "stage0_manifest": "ce72238107e95f3ed88152a943041d3a827ae945",
    "stage0_checker": "396b0ae7245015bc199f52a139cee20713afb54a",
    "target_plan": "e1caf3bf6b70fb85c00fc91c621d7e823f72f4d9",
    "preflight68": "e569ce30ec2bf50680c5576c2d9f2c666cd09f19",
    "phase62b": "e0ada366845c7a6c5a5dd75de91fe262b72a94b6",
    "slotparser": "8bafba7f2bce4cf77c9001c729936c1ce619759b",
    "phase62c": "de6eb1b829ef43fcc23cb3ba85d3640a2e9b7c87",
    "phase62p": "69c2b8cd078200c7de5d9cd59aafb23510680d75",
    "phase64b": "03e7dad20338132dc2b476a91c210142137d3b95",
    "issue81": "227f2a6b412de64716c067e3b7354188f56c2df8",
    "r1_phase4a_first_reveal": "774e80895609b3e895d6a579bd21184fd26e3a25",
    "r5_issue145": "ce8a167c607fbcf2807f567439ab6837471f4f07",
    "r7_issue155_gate": "f5ab4fa31a92b3c303401da33611ffd5f77b402d",
    "r7_issue155_scorer": "0d57fdd32d298773b5ee38f97c9f104d29fa8377",
    "r7_issue158_gate": "4dbc919f3e9ededa17d2e10f56de46c98456cdea",
    "r7_issue161_gate": "00e5bddc0484b9472bb4fce9dadb89dd52bf578f",
    "r7_issue161_scorer": "d24149977770118505f2147c5aa2bb727631906f",
    "r7_issue167_gate": "5b3aac1a03ef087340f6e0ffd241a4909476c815",
    "r7_issue167_scorer": "5e67cecc312b431791c6623d1077ac46533fce0a",
    "r8_phase2b": "3f5878f5c7121d9fbd5ba1db3b500d5232927b21",
    "source_order": "bb3aab054e98390f4aa24be750ba2d123b6e5227",
}
EXPECTED_STAGE0_GATE_SHA256 = "76080227ad683d620a4888da05f8aef9a1dba0453125e740279dcbdcf9c28a10"
EXPECTED_BASE_MAIN = "53961dbe3a72ebb1c026079987d9a194ad0f0935"
EXPECTED_TARGET_PLAN_HEAD = "43f5e573d2ae0b621b1eba4495e29b3a4fb73bae"
EXPECTED_NAIBBE_COMMIT = "f2675ec5dd275268bc64dd48ea64fc0e0e9827a2"
EXPECTED_CREMMA_COMMIT = "292525969ad98380b398e6606a9c2a36d51913ae"

A1_SEEDS = (6195200, 6295200, 6395300, 6495300, 6595200)
A1_SURFACE_SHA = (
    "be20405db3d8ee240b70f5b00bbbcba785f2af1b84bdcec849330162870bd142",
    "a62c1ed31ef1d2fde42c858e137ffd49e998743b3ddc54ede132ea8c0606890b",
    "173b991e9a2374f1c0b545e91b478e6312d0b93cd3340c43c10ad5e807786cf0",
    "ec2c06bb6ac3aca33eb09aa7386d8f84ea1b55710c689e0b89d246c8899e0c15",
    "c17bbcd9d68718c8823798b27d97db46fb060c635a46f340b748d5d28b1e6927",
)
A1_POOLED_SHA = "4ce8eaad33414feb4351825a228a1a865480c31bb41bf9e467c3b76fc6dc6fd3"
NAIBBE_MANUSCRIPTS = ("BIS193", "CLM13027", "Mazarine915", "UBL758")
NAIBBE_SEEDS = (6480000, 6480100, 6480200, 6480300)
NAIBBE_SURFACE_SHA = (
    "fbf275e179297b947ccd2de5686e02340ea15d6ab9ca4b73a26dd9448b286805",
    "da43249442db277a367bb8171b7228a9bf4b63b055924e9efd06240452d4ad77",
    "2ebecc4d281df810f57ec370cd1ba0d4708be0391d8185d3ed2ccb588df1f33d",
    "5c6649425d9be84f8b9ce04c257cc6fb308e9b8a59191320fcf1a63c86affa89",
)
NAIBBE_POOLED_SHA = "47d52d28d4e2ac126bb8681c881ec339cb339c9b1bb329fb48263e6c1e9758bd"

R3_D_MAX = 0.7665018009178945
R3_C_MAX = 0.11767986235112631
R5_TARGET = {"ZL3b": 0.1336232955274749, "IT2a": 0.16184998339508744}
R7_TARGET = {
    "A": (0.0632767341, 0.0678261662),
    "B": (0.1012061293, 0.1045681122),
}
R8_BAND = (0.02072935, 0.0829174)
N_FOLDS = 5
LN2 = math.log(2.0)

# Historical complete-66 authority (#68) carried forward only after identity checks.
HISTORICAL_R2 = {
    "A1": {
        "pass": False,
        "disposition": "FAIL_REPRESENTATION_COMPATIBILITY",
        "coverage": {"supported": 12650, "total": 32570, "rate": 0.3883942278170095},
        "coverage_gate": 0.60,
    },
    "Naibbe_C1_E0": {
        "pass": True,
        "coverage": {"supported": 29759, "total": 33574, "rate": 0.886370405671055},
        "E": 3.1784043855151296,
        "W": 0.954726539114345,
        "p_exist": 1.0 / 1001.0,
        "targets": {
            "ZL3b": {"pearson_r": 0.8830282501011794, "sign_agreement": 60, "p_pearson": 1.0 / 1001.0, "p_sign": 1.0 / 1001.0},
            "IT2a": {"pearson_r": 0.9000974100381157, "sign_agreement": 61, "p_pearson": 1.0 / 1001.0, "p_sign": 1.0 / 1001.0},
        },
        "authority_result_sha256": "5cef35e9df56149fb1db5edff8d52fad9291208476b0d4ac64bd9c8782faa471",
        "authority_scorer_blob": "e94a24fbdfbb922099407313f23a1b87859130b6",
        "authority_first_scientific_head": "65e020cb2827a28670005da6d5d02bd6a6c1e51a",
    },
}
HISTORICAL_R9 = {
    "A1": {"applicable": False, "pass": None, "disposition": "NOT_APPLICABLE_SURFACE_GENERATOR"},
    "Naibbe_C1_E0": {
        "applicable": True,
        "pass": False,
        "unique_exact_lines": 1167,
        "total_lines": 1778,
        "unique_exact_fraction": 0.656355455568054,
        "required_fraction": 1.0,
    },
}


def canonical_json(obj) -> str:
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n"


def sha256_obj(obj) -> str:
    return hashlib.sha256(canonical_json(obj).encode("utf-8")).hexdigest()


def git_blob(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def require_blob(path: Path, expected: str, label: str) -> str:
    got = git_blob(path)
    if got != expected:
        raise RuntimeError(f"{label} blob changed: {got} != {expected}")
    return got


def git_head(path: Path) -> str:
    return subprocess.check_output(["git", "-C", str(path), "rev-parse", "HEAD"], text=True).strip()


def require_ancestor(commit: str, label: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(ROOT), "merge-base", "--is-ancestor", commit, "HEAD"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"{label} is not an ancestor of scorer runtime HEAD: {commit}")
    return commit


def token_text(tok) -> str:
    return tok if isinstance(tok, str) else "".join(str(x) for x in tok)


def item_fold_hash(item_ids: Sequence[str]) -> str:
    return hashlib.sha256("\n".join(item_ids).encode("utf-8")).hexdigest()


def stability(values: Sequence[float]) -> dict:
    vals = [float(x) for x in values]
    return {
        "values": vals,
        "mean": float(np.mean(vals)),
        "positive_folds": int(sum(x > 0.0 for x in vals)),
        "pass_positive_4_of_5": bool(float(np.mean(vals)) > 0.0 and sum(x > 0.0 for x in vals) >= 4),
    }


def ratio_band(value: float, references: Sequence[float]) -> bool:
    return all(0.5 * float(r) <= float(value) <= 2.0 * float(r) for r in references)


# ---- immutable primary surface regeneration ----------------------------------
def load_phase62_authorities():
    first = P68.load_phase62c_first_reveal()
    p62path = EXP / "phase62" / "phase62p_h62p1_results.json"
    if P68.sha256_file(p62path) != P68.PHASE62P_SHA:
        raise RuntimeError("Phase62P authority SHA mismatch")
    p62p = json.loads(p62path.read_text(encoding="utf-8"))
    phase64 = json.loads((EXP / "phase64" / "phase64b_science_results.json").read_text(encoding="utf-8"))
    if phase64["inputs"]["naibbe_commit"] != EXPECTED_NAIBBE_COMMIT:
        raise RuntimeError("Phase64 Naibbe commit changed")
    if phase64["inputs"]["cremma_commit"] != EXPECTED_CREMMA_COMMIT:
        raise RuntimeError("Phase64 CREMMA commit changed")
    return first, p62p, phase64


def generate_a1(zl_path: Path, parser, phase62c_first: dict, phase62p: dict):
    b, c, h62 = P68.b, P68.c, P68.h62
    if b.git_blob_sha1(zl_path.read_bytes()) != P68.EXPECTED_ZL_BLOB:
        raise RuntimeError("A1 ZL3b source blob mismatch")
    vitems = b.parse_voynich(zl_path)
    folds = b.physical_leaf_folds(vitems)
    p61 = c.load_phase61_module()
    paragraphs, _ = p61.parse(str(zl_path))
    p61_folds = p61.physical_leaf_folds(paragraphs)
    if [sorted(x) for x in folds] != [sorted(x) for x in p61_folds]:
        raise RuntimeError("A1 Phase61/62 fold mismatch")
    vocab = sorted(set(p61.all_tokens(paragraphs)))
    neighbors = p61.build_neighbors(vocab)
    by_fold = []
    pooled = []
    for fi, leaves in enumerate(folds):
        strength, local_p = c.A1_PARAMS[fi]
        seed = 6190000 + fi * 100000 + int(strength * 10) * 1000 + int(local_p * 100) * 10
        if seed != A1_SEEDS[fi]:
            raise RuntimeError(f"A1 seed changed fold {fi}: {seed}")
        train = p61.subset(paragraphs, leaves, include=False)
        test = p61.subset(paragraphs, leaves, include=True)
        shape_scores = p61.learn_shape_scores(train, vocab)
        entry_cum = p61.entry_cumulative(vocab, shape_scores, strength)
        generated = p61.generate_layout(test, vocab, neighbors, entry_cum, local_p, seed)
        items = c.convert_p61_paragraphs(generated)
        digest = P68.surface_digest(items)
        if digest != A1_SURFACE_SHA[fi]:
            raise RuntimeError(f"A1 primary surface changed fold {fi}: {digest}")
        # Historical identity guard only; no Issue172 classification is derived here.
        old = phase62p["folds"][fi]["A1_realizations"]["rep0"]
        if h62.raw_profile(items, f"A1:fold{fi}:rep0") != old:
            raise RuntimeError(f"A1 historical rep0 H62 identity changed fold {fi}")
        by_fold.append(items)
        pooled.extend(items)
    if P68.surface_digest(pooled) != A1_POOLED_SHA:
        raise RuntimeError("A1 pooled primary surface changed")
    return {"vitems": vitems, "physical_folds": folds, "items_by_fold": by_fold, "items": pooled}


def generate_naibbe(cremma_root: Path, naibbe_root: Path, phase64: dict):
    b, n64 = P68.b, P68.n64
    if b.verify_cremma_commit(cremma_root) != EXPECTED_CREMMA_COMMIT:
        raise RuntimeError("CREMMA authority mismatch")
    if git_head(naibbe_root) != EXPECTED_NAIBBE_COMMIT:
        raise RuntimeError("Naibbe repository HEAD mismatch")
    module = n64.load_naibbe(naibbe_root)
    if n64.NAIBBE_COMMIT != EXPECTED_NAIBBE_COMMIT:
        raise RuntimeError("Naibbe code pin changed")
    sources = {name: b.parse_latin_manuscript(cremma_root, name, rel) for name, rel in b.PRIMARY_MANUSCRIPTS.items()}
    original_map = dict(module.placeholder_to_glyph)
    frozen_diag = phase64["published_mapping"]["generation"]["encryption_diagnostics"]
    by_manuscript = {}
    pooled = []
    for mi, manuscript in enumerate(NAIBBE_MANUSCRIPTS):
        seed = 6480000 + 100 * mi
        if seed != NAIBBE_SEEDS[mi]:
            raise RuntimeError("Naibbe seed changed")
        primary, _raw, diag = n64.encrypt_manuscript(module, sources[manuscript], manuscript, original_map, seed)
        if diag != frozen_diag[manuscript]["rep0"]:
            raise RuntimeError(f"Naibbe generation diagnostics changed: {manuscript}")
        digest = P68.surface_digest(primary)
        if digest != NAIBBE_SURFACE_SHA[mi]:
            raise RuntimeError(f"Naibbe primary surface changed: {manuscript}")
        by_manuscript[manuscript] = primary
        pooled.extend(primary)
    if P68.surface_digest(pooled) != NAIBBE_POOLED_SHA:
        raise RuntimeError("Naibbe pooled primary surface changed")
    ordered = [it for manuscript in NAIBBE_MANUSCRIPTS for it in by_manuscript[manuscript]]
    ids=[it.item_id for it in ordered]
    if len(ids)!=len(set(ids)):
        raise RuntimeError("Naibbe candidate-native item ids are not globally unique")
    fold_map = {it.item_id: i % N_FOLDS for i, it in enumerate(ordered)}
    return {"items": pooled, "ordered_items": ordered, "fold_map": fold_map, "by_manuscript": by_manuscript}


# ---- candidate adapters -------------------------------------------------------
def clean_atom_token(raw: str):
    atoms, _reasons = E145.GATE.clean_atoms(raw)
    return atoms


def candidate_runs(items: Sequence, fold_map: Mapping[str, int], group_map: Mapping[str, object] | None = None):
    """Issue145 common-EVA clean runs from immutable candidate Items."""
    parser = E145.GATE.E.SlotParser()
    E145.GATE.E.validate_parser(parser)
    out = []
    for it in items:
        fold = int(fold_map[it.item_id])
        group = group_map[it.item_id] if group_map is not None else (it.leaf if it.leaf is not None else it.document)
        for li, line in enumerate(it.lines):
            run = []
            run_no = 0
            for ti, tok in enumerate(line):
                raw = token_text(tok)
                atoms = clean_atom_token(raw)
                if atoms is None:
                    if run:
                        out.append((fold, group, f"{it.item_id}:line{li}:run{run_no}", li, tuple(run)))
                        run_no += 1
                        run = []
                    continue
                run.append({
                    "raw": raw,
                    "atoms": tuple(atoms),
                    "slotparser_accepted": bool(parser.parses(raw)),
                    "segment_index": ti,
                    "item_id": it.item_id,
                    "line_index": li,
                })
            if run:
                out.append((fold, group, f"{it.item_id}:line{li}:run{run_no}", li, tuple(run)))
    return tuple(out)


def a1_fold_map(a1) -> dict[str, int]:
    out = {}
    for f, items in enumerate(a1["items_by_fold"]):
        for it in items:
            if it.item_id in out:
                raise RuntimeError(f"duplicate A1 item id: {it.item_id}")
            out[it.item_id] = f
    return out


def atomized_tokens_by_fold(items, fold_map):
    by_fold = {f: [] for f in range(N_FOLDS)}
    for it in items:
        f = int(fold_map[it.item_id])
        for line in it.lines:
            row = []
            for tok in line:
                atoms = R1A.G.atomize_clean(token_text(tok))
                row.append(tuple(atoms) if atoms is not None else None)
            by_fold[f].append(row)
    return by_fold


# ---- R1 production boundary --------------------------------------------------
def score_r1(items, fold_map) -> dict:
    by_fold = atomized_tokens_by_fold(items, fold_map)
    all_train_tokens = {f: [] for f in range(N_FOLDS)}
    fold_events = {}
    for f in range(N_FOLDS):
        mids, boundaries, p2 = [], [], []
        for line in by_fold[f]:
            for atoms in line:
                if atoms is None:
                    continue
                all_train_tokens[f].append(atoms)
                if len(atoms) >= 4:
                    cut = len(atoms) // 2
                    if cut >= 2 and len(atoms) - cut >= 2:
                        mids.append((atoms[:cut], atoms[cut:]))
            for left, right in zip(line, line[1:]):
                if left is None or right is None:
                    continue
                if len(left) >= 2 and len(right) >= 2:
                    boundaries.append((left, right))
                if len(left) >= 3 and len(right) >= 3:
                    p2.append((left, right))
        fold_events[f] = {"mid": mids, "boundary": boundaries, "p2": p2}
        if not boundaries or not mids or not p2:
            raise RuntimeError(f"R1 fold {f} lacks required score support")

    outer = []
    pooled_real, pooled_mid, pooled_left, pooled_right = [], [], [], []
    for f in range(N_FOLDS):
        train_sequences = [atoms for g in range(N_FOLDS) if g != f for atoms in all_train_tokens[g]]
        model = R1A.AtomV2(train_sequences)
        real = [float(R1A.score_p1(model, l, r)["advantage"]) for l, r in fold_events[f]["boundary"]]
        mid = [float(R1A.score_p1(model, l, r)["advantage"]) for l, r in fold_events[f]["mid"]]
        left = []
        right = []
        for l, r in fold_events[f]["p2"]:
            row = R1A.score_p2(model, l, r)
            left.append(float(row["observed_minus_shift_left"]))
            right.append(float(row["observed_minus_shift_right"]))
        d_reset = float(np.mean(real) - np.mean(mid))
        mleft = float(np.mean(left))
        mright = float(np.mean(right))
        outer.append({
            "fold": f,
            "n_boundary": len(real),
            "n_mid": len(mid),
            "n_p2": len(left),
            "D_RESET": d_reset,
            "OBSERVED_minus_SHIFT_LEFT": mleft,
            "OBSERVED_minus_SHIFT_RIGHT": mright,
        })
        pooled_real.extend(real); pooled_mid.extend(mid); pooled_left.extend(left); pooled_right.extend(right)

    pooled = {
        "D_RESET": float(np.mean(pooled_real) - np.mean(pooled_mid)),
        "OBSERVED_minus_SHIFT_LEFT": float(np.mean(pooled_left)),
        "OBSERVED_minus_SHIFT_RIGHT": float(np.mean(pooled_right)),
    }
    pass_reset = pooled["D_RESET"] > 0 and sum(r["D_RESET"] > 0 for r in outer) >= 4
    pass_left = pooled["OBSERVED_minus_SHIFT_LEFT"] < 0 and sum(r["OBSERVED_minus_SHIFT_LEFT"] < 0 for r in outer) >= 4
    pass_right = pooled["OBSERVED_minus_SHIFT_RIGHT"] < 0 and sum(r["OBSERVED_minus_SHIFT_RIGHT"] < 0 for r in outer) >= 4
    return {"pass": bool(pass_reset and pass_left and pass_right), "outer": outer, "pooled": pooled}


# ---- R3 / R4 Phase62 surface responsibilities -------------------------------
def score_r3_r4_a1(a1, phase62c_first: dict, phase62p: dict) -> tuple[dict, dict]:
    b, h62 = P68.b, P68.h62
    r3_rows, r4_cand, r4_target = [], [], []
    for f, leaves in enumerate(a1["physical_folds"]):
        c_s2 = float(phase62c_first["folds"][f]["A1_replicates"][0]["S2"])
        t_s2 = float(phase62c_first["folds"][f]["heldout_voynich"]["S2"])
        cp = phase62p["folds"][f]["A1_realizations"]["rep0"]
        tp = phase62p["folds"][f]["voynich"]
        cs1 = float(phase62c_first["folds"][f]["A1_replicates"][0]["S1"])
        ts1 = float(phase62c_first["folds"][f]["heldout_voynich"]["S1"])
        r3_rows.append({
            "fold": f,
            "candidate_S2": c_s2, "target_S2": t_s2,
            "S2_ratio": float(c_s2 / t_s2) if t_s2 > 0 else None,
            "candidate_abs_excess_sum": float(cp["abs_excess_sum"]),
            "target_abs_excess_sum": float(tp["abs_excess_sum"]),
            "raw_H62_ratio": float(cp["abs_excess_sum"] / tp["abs_excess_sum"]),
            "D_profile": h62.profile_distance(cp, tp),
            "abs_C_short_diff": h62.c_short_diff(cp, tp),
            "historical_rep0_metric_identity_reused": True,
        })
        r4_cand.append(cs1); r4_target.append(ts1)
    s2_ratio = float(np.mean([x["candidate_S2"] for x in r3_rows]) / np.mean([x["target_S2"] for x in r3_rows]))
    raw_ratio = float(np.mean([x["candidate_abs_excess_sum"] for x in r3_rows]) / np.mean([x["target_abs_excess_sum"] for x in r3_rows]))
    mean_d = float(np.mean([x["D_profile"] for x in r3_rows]))
    mean_c = float(np.mean([x["abs_C_short_diff"] for x in r3_rows]))
    r3 = {
        "pass": bool(0.5 <= s2_ratio <= 2.0 and raw_ratio >= 0.5 and mean_d <= R3_D_MAX and mean_c <= R3_C_MAX),
        "outer": r3_rows,
        "summary": {"S2_ratio_of_means": s2_ratio, "raw_H62_ratio_of_means": raw_ratio, "mean_D_profile": mean_d, "mean_abs_C_short_diff": mean_c},
    }
    cm, tm = float(np.mean(r4_cand)), float(np.mean(r4_target))
    ratio = float(cm / tm) if tm != 0 else None
    r4 = {"pass": bool(cm * tm > 0 and ratio is not None and 0.5 <= ratio <= 2.0), "candidate_by_fold": r4_cand, "target_by_fold": r4_target, "candidate_mean": cm, "target_mean": tm, "ratio_of_means": ratio, "historical_rep0_S1_identity_reused": True}
    return r3, r4

def score_r3_r4_naibbe(naibbe, a1) -> tuple[dict, dict]:
    b, h62 = P68.b, P68.h62
    per_ms_s2 = {}
    per_ms_h62 = {}
    for ms in NAIBBE_MANUSCRIPTS:
        label = f"Phase64B:published:{ms}:rep0:published-view"
        per_ms_s2[ms] = float(b.s2_locality(naibbe["by_manuscript"][ms], label)["excess"])
        per_ms_h62[ms] = h62.raw_profile(naibbe["by_manuscript"][ms], label)
    c_s2 = float(np.mean(list(per_ms_s2.values())))
    cp = h62.aggregate_excess(per_ms_h62, "Phase64B:published:rep0:equal-manuscript-E", "manuscript")
    rows, cand_s1, target_s1 = [], [], []
    for f, leaves in enumerate(a1["physical_folds"]):
        target = b.by_leaves(a1["vitems"], leaves, include=True)
        train = b.by_leaves(a1["vitems"], leaves, include=False)
        sd = b.training_sd(train)
        direction = np.mean(b.contrasts(train, sd), axis=0)
        direction /= float(np.linalg.norm(direction))
        cs1, _n, _d = b.s1_projection(naibbe["items"], sd, direction)
        ts1, _n2, _d2 = b.s1_projection(target, sd, direction)
        tp = h62.raw_profile(target, f"Voynich:fold{f}")
        t_s2 = b.s2_locality(target, f"Voynich:fold{f}")["excess"]
        rows.append({
            "fold": f,
            "candidate_S2": c_s2, "target_S2": float(t_s2),
            "S2_ratio": float(c_s2 / t_s2) if t_s2 > 0 else None,
            "candidate_abs_excess_sum": float(cp["abs_excess_sum"]), "target_abs_excess_sum": float(tp["abs_excess_sum"]),
            "raw_H62_ratio": float(cp["abs_excess_sum"] / tp["abs_excess_sum"]),
            "D_profile": h62.profile_distance(cp, tp), "abs_C_short_diff": h62.c_short_diff(cp, tp),
        })
        cand_s1.append(float(cs1)); target_s1.append(float(ts1))
    s2_ratio = float(c_s2 / np.mean([x["target_S2"] for x in rows]))
    raw_ratio = float(cp["abs_excess_sum"] / np.mean([x["target_abs_excess_sum"] for x in rows]))
    mean_d = float(np.mean([x["D_profile"] for x in rows])); mean_c = float(np.mean([x["abs_C_short_diff"] for x in rows]))
    r3 = {"pass": bool(0.5 <= s2_ratio <= 2.0 and raw_ratio >= 0.5 and mean_d <= R3_D_MAX and mean_c <= R3_C_MAX), "outer": rows, "summary": {"S2_ratio_of_means": s2_ratio, "raw_H62_ratio_of_means": raw_ratio, "mean_D_profile": mean_d, "mean_abs_C_short_diff": mean_c}, "candidate_equal_manuscript_S2": per_ms_s2}
    cm, tm = float(np.mean(cand_s1)), float(np.mean(target_s1)); ratio = float(cm / tm) if tm else None
    r4 = {"pass": bool(cm * tm > 0 and ratio is not None and 0.5 <= ratio <= 2.0), "candidate_by_fold": cand_s1, "target_by_fold": target_s1, "candidate_mean": cm, "target_mean": tm, "ratio_of_means": ratio}
    return r3, r4


# ---- R5/R6 common-EVA same-line edge + line-break reset ---------------------
def score_same_line_edge(runs) -> dict:
    outer = []
    all_folds = set(range(N_FOLDS))
    for f in range(N_FOLDS):
        model = E145.CommonEdgeModel(runs, all_folds - {f})
        row = E145.score_fold(model, runs, f)
        outer.append({"fold": f, **row, "training_diagnostics": model.diagnostics()})
    gains = [float(x["G_common"]) for x in outer]
    return {"outer": outer, "gain": stability(gains)}


def k2_logp_stream(model, atoms, history):
    ll = 0.0
    for sym in E145.token_symbols(atoms):
        ll += model.logp(history[-E145.FIXED_K:], sym)
        history.append(sym)
    return float(ll)


def prepared_candidate_lines(items, ordered_items):
    parser = E145.GATE.E.SlotParser(); E145.GATE.E.validate_parser(parser)
    wanted = {it.item_id: it for it in items}
    out = []
    for oit in ordered_items:
        it = wanted[oit.item_id]
        lines = []
        for line in it.lines:
            rec = []
            for tok in line:
                raw = token_text(tok); atoms = clean_atom_token(raw)
                rec.append((raw, tuple(atoms) if atoms is not None else None, bool(parser.parses(raw))))
            lines.append(rec)
        out.append((it, lines))
    return out


def beyond_line_support(items, fold_map, ordered_items) -> dict[str, int]:
    prepared = prepared_candidate_lines(items, ordered_items)
    counts = {str(f): 0 for f in range(N_FOLDS)}
    for it, lines in prepared:
        f = int(fold_map[it.item_id]); hist = []
        for line in lines:
            first_clean_seen = False
            for _raw, atoms, accepted in line:
                if atoms is None:
                    hist = []; first_clean_seen = False
                    continue
                had_prior = bool(hist)
                if accepted and not first_clean_seen and had_prior:
                    counts[str(f)] += 1
                first_clean_seen = True
                for sym in E145.token_symbols(atoms):
                    hist.append(sym); hist[:] = hist[-E145.FIXED_K:]
    return counts


def score_beyond_line(items, fold_map, ordered_items) -> dict:
    prepared = prepared_candidate_lines(items, ordered_items)

    def train_models(test_fold):
        line_model = E145.K2RunModel(); cont_model = E145.K2RunModel()
        for it, lines in prepared:
            if int(fold_map[it.item_id]) == test_fold:
                continue
            cont_hist = []
            for line in lines:
                line_hist = []
                for _raw, atoms, _accepted in line:
                    if atoms is None:
                        line_hist = []; cont_hist = []
                        continue
                    for sym in E145.token_symbols(atoms):
                        line_model.observe(line_hist, sym); line_hist.append(sym); line_hist[:] = line_hist[-E145.FIXED_K:]
                        cont_model.observe(cont_hist, sym); cont_hist.append(sym); cont_hist[:] = cont_hist[-E145.FIXED_K:]
        return line_model, cont_model

    outer = []
    for f in range(N_FOLDS):
        line_model, cont_model = train_models(f)
        ll_line, ll_cont = [], []
        line_start_scored = 0
        for it, lines in prepared:
            if int(fold_map[it.item_id]) != f:
                continue
            cont_hist = []
            for line in lines:
                line_hist = []
                first_clean_seen = False
                for _raw, atoms, accepted in line:
                    if atoms is None:
                        line_hist = []; cont_hist = []; first_clean_seen = False
                        continue
                    before_cont = list(cont_hist)
                    lp_line = k2_logp_stream(line_model, atoms, line_hist)
                    lp_cont = k2_logp_stream(cont_model, atoms, cont_hist)
                    if accepted and not first_clean_seen and before_cont:
                        ll_line.append(lp_line); ll_cont.append(lp_cont); line_start_scored += 1
                    first_clean_seen = True
        if not ll_line:
            raise RuntimeError(f"R5 beyond-line fold {f} has zero supported line starts")
        bits_line = float(-np.mean(ll_line) / LN2); bits_cont = float(-np.mean(ll_cont) / LN2)
        outer.append({"fold": f, "n_scored_line_starts": line_start_scored, "bits_LINE_RESET": bits_line, "bits_BEYOND_LINE_CONT": bits_cont, "G_beyond": float(bits_line - bits_cont)})
    gains = [x["G_beyond"] for x in outer]
    robust = bool(float(np.mean(gains)) > 0 and sum(x > 0 for x in gains) >= 4)
    return {"outer": outer, "mean_G_beyond": float(np.mean(gains)), "positive_folds": int(sum(x > 0 for x in gains)), "robust_positive": robust}

def score_r5_r6(items, fold_map, ordered_items):
    runs = candidate_runs(items, fold_map, {it.item_id: it.item_id for it in items})
    same = score_same_line_edge(runs)
    beyond = score_beyond_line(items, fold_map, ordered_items)
    mean_gain = float(same["gain"]["mean"])
    r5_pass = bool(same["gain"]["positive_folds"] >= 4 and ratio_band(mean_gain, tuple(R5_TARGET.values())) and not beyond["robust_positive"])
    r5 = {"pass": r5_pass, "same_line": same, "beyond_line": beyond, "target_bands": R5_TARGET}
    r6 = {"pass": r5_pass, "per_reading_tuning": False, "same_candidate_table_for_both_target_reading_comparisons": True, "reading_specific_repair": False}
    return r5, r6, runs


# ---- R7 A1 Currier outcome bias ---------------------------------------------
def edge_counts(runs, train_folds):
    out = defaultdict(Counter)
    for fold, _group, _loc, _ln, run in runs:
        if int(fold) not in train_folds:
            continue
        prev = None
        for ti, rec in enumerate(run):
            syms = E145.token_symbols(rec["atoms"])
            if ti > 0 and prev is not None:
                out[prev][syms[0]] += 1
            prev = syms[-2]
    return dict(out)


def pool_tables(a, b):
    out = {}
    for ctx in sorted(set(a) | set(b)):
        row = {}
        for y in sorted(set(a.get(ctx, {})) | set(b.get(ctx, {}))):
            v = Fraction(a.get(ctx, {}).get(y, 0), 2) + Fraction(b.get(ctx, {}).get(y, 0), 2)
            if v > 0:
                row[y] = v
        if row: out[ctx] = row
    return out


def score_currier_cell(regime, regime_runs, pool, regime_table, full_multiplier, sparse_by_k, test_fold):
    model = E145.CommonEdgeModel(regime_runs, set(range(N_FOLDS)) - {test_fold})
    l_pool=[]; l_reg=[]; l_full=[]; l_sparse={k:[] for k in S167.KS}
    body=0; supported=0
    for fold, _g, _loc, _ln, run in regime_runs:
        if int(fold) != test_fold: continue
        prev=None
        for ti, rec in enumerate(run):
            syms=E145.token_symbols(rec["atoms"])
            lp_pool=S155.matched_token_logp(model,pool,syms,ti==0,prev)
            lp_reg=S155.matched_token_logp(model,regime_table,syms,ti==0,prev)
            lp_full=S161.outcome_token_logp(model,pool,full_multiplier,syms,ti==0,prev)
            lp_sparse={k:S161.outcome_token_logp(model,pool,sparse_by_k[k],syms,ti==0,prev) for k in S167.KS}
            if rec["slotparser_accepted"]:
                l_pool.append(lp_pool); l_reg.append(lp_reg); l_full.append(lp_full)
                for k in S167.KS: l_sparse[k].append(lp_sparse[k])
                if ti>0:
                    body += 1; supported += int(prev in pool)
            prev=syms[-2]
    if not l_pool or body <= 0:
        raise RuntimeError(f"R7 {regime} fold {test_fold} has zero scoring support")
    n=len(l_pool)
    bpool=-sum(l_pool)/(n*LN2); breg=-sum(l_reg)/(n*LN2); bfull=-sum(l_full)/(n*LN2)
    out={"fold":test_fold,"regime":regime,"n_scored":n,"n_body":body,"matched_supported_body":supported,"G_Currier":float(bpool-breg),"G_interaction":float(bfull-breg),"G_outcome_full":float(bpool-bfull),"K":{}}
    for k in S167.KS:
        bs=-sum(l_sparse[k])/(n*LN2)
        out["K"][str(k)]={"G_sparse":float(bpool-bs),"G_missing":float(bs-bfull)}
    return out


def score_r7_a1(runs, leaf_currier: Mapping[int,str]):
    regime_runs={r:tuple(x for x in runs if leaf_currier.get(int(x[1]))==r) for r in ("A","B")}
    if any(not regime_runs[r] for r in regime_runs):
        raise RuntimeError("R7 A1 lacks Currier regime runs")
    outer={"A":[],"B":[]}
    for f in range(N_FOLDS):
        train=set(range(N_FOLDS))-{f}
        ca=edge_counts(regime_runs["A"],train); cb=edge_counts(regime_runs["B"],train)
        matched,_summary=G155.support_match(ca,cb)
        a,b=matched["A"],matched["B"]; pool,_pool_audit=G161.G158.pool_tables(a,b)
        agg_a=G161.aggregate_outcomes(a); agg_b=G161.aggregate_outcomes(b); agg_pool=G161.aggregate_outcomes(pool)
        total_a=sum(agg_a.values(),Fraction(0,1)); total_b=sum(agg_b.values(),Fraction(0,1))
        qa=G167.probability_vector(agg_a,total_a); qb=G167.probability_vector(agg_b,total_b)
        ranking,_j,_audit=G167.jeffreys_ranking(qa,qb)
        full={"A":G161.build_multiplier(agg_a,agg_pool),"B":G161.build_multiplier(agg_b,agg_pool)}
        for r, table in (("A",a),("B",b)):
            sparse={k:G167.sparse_multiplier(full[r],set(ranking[:k])) for k in S167.KS}
            outer[r].append(score_currier_cell(r,regime_runs[r],pool,table,full[r],sparse,f))
    regime_summary={}
    for r in ("A","B"):
        g=[x["G_Currier"] for x in outer[r]]; gi=[x["G_interaction"] for x in outer[r]]
        regime_summary[r]={"G_Currier":stability(g),"G_interaction":stability(gi),"within_both_target_bands":ratio_band(float(np.mean(g)),R7_TARGET[r])}
    k_summary={}; first=None
    for k in S167.KS:
        all_useful=True; any_missing=False; cells={}
        for r in ("A","B"):
            gs=[x["K"][str(k)]["G_sparse"] for x in outer[r]]; gm=[x["K"][str(k)]["G_missing"] for x in outer[r]]
            useful=bool(np.mean(gs)>0 and sum(x>0 for x in gs)>=4); missing=bool(np.mean(gm)>0 and sum(x>0 for x in gm)>=4)
            cells[r]={"useful":useful,"robust_full_over_sparse_residual":missing,"G_sparse":stability(gs),"G_missing":stability(gm)}
            all_useful &= useful; any_missing |= missing
        sufficient=bool(all_useful and not any_missing); k_summary[str(k)]={"suffices":sufficient,"cells":cells}
        if sufficient and first is None: first=k
    no_interaction=all(not regime_summary[r]["G_interaction"]["pass_positive_4_of_5"] for r in ("A","B"))
    pass_main=all(regime_summary[r]["G_Currier"]["positive_folds"]>=4 and regime_summary[r]["within_both_target_bands"] for r in ("A","B"))
    sparse_rule=(first==16 and all(not k_summary[str(k)]["suffices"] for k in (1,2,4,8)))
    return {"pass":bool(pass_main and no_interaction and sparse_rule),"outer":outer,"regimes":regime_summary,"K":k_summary,"smallest_sufficient_K":first,"requirements":{"no_robust_Currier_x_previous_terminal_interaction":no_interaction,"K16_and_no_K_le_8":sparse_rule},"target_bands":R7_TARGET}


# ---- R8 candidate-native corrected causal prefix ----------------------------
def clone_for_causal_order(items, ordered_items, group_fn):
    """Give B2-compatible Items explicit causal-group/reset and ordinal keys."""
    b=P68.b
    group_rank={}; next_group=0; within=defaultdict(int); out=[]; original={it.item_id:it for it in items}
    for it in ordered_items:
        g=group_fn(it)
        if g not in group_rank: group_rank[g]=next_group; next_group+=1
        within[g]+=1
        oid=it.item_id
        out.append(b.Item(item_id=f"g{group_rank[g]:04d}:p{within[g]:06d}|{oid}",document=f"g{group_rank[g]:04d}",lines=copy.deepcopy(it.lines),leaf=group_rank[g]))
    if len(out)!=len(original): raise RuntimeError("R8 causal clone item count changed")
    return out


def parse_candidate_items(items, parser):
    C=B2.I.C
    parsed={}
    for it in items:
        parsed[it.item_id]=[[C.token_units(parser,token_text(tok)) for tok in line] for line in it.lines]
    return parsed


def generic_fit(items, parsed, fold_map, excluded):
    tr=[it for it in items if int(fold_map[it.item_id]) not in set(excluded)]
    seqs=B2.I.training_sequences(tr,parsed)
    if not seqs: raise RuntimeError("R8 empty training sequence population")
    v2=B2.I.C.V2Model(seqs); index=B2.I.NeighborIndex(B2.I.training_vocab(tr,parsed))
    return tr,v2,index


def r8_features(items, parsed, fold_map, v2, index, parser, score_folds, forbidden_folds=()):
    score_folds = set(map(int, score_folds)); forbidden_folds = set(map(int, forbidden_folds))
    local=B2.P1.RecencyAccumulator(40,32.0); p_cache={}; p0=[]; qlocal=[]; avlocal=[]
    qline=[]; avline=[]; qprev=[]; avprev=[]
    current=None; prev_para=[]; para=[]; pos=0
    for it in items:
        f=int(fold_map[it.item_id])
        if it.leaf!=current:
            current=it.leaf; prev_para=[]; para=[]; pos=0; local.reset()
        elif f not in forbidden_folds:
            prev_para.extend(para); para=[]
        if f in forbidden_folds:
            prev_para=[]; para=[]; pos=0; local.reset()
            continue
        for li,line in enumerate(it.lines):
            line_sources=[]
            for ti,tok in enumerate(line):
                local.prune(pos); seq=parsed[it.item_id][li][ti]
                if seq is not None and f in score_folds:
                    p=B2.P1.P0.p0_surface(v2,parser,tok,p_cache); ql,av=local.q(tok)
                    sl=B2.source_stats(line_sources,tok,pos,"LINE",it.leaf,False)
                    sp=B2.source_stats(prev_para,tok,pos,"PREV_PARAS",it.leaf,False)
                    p0.append(float(p)); qlocal.append(float(ql)); avlocal.append(bool(av))
                    qline.append(float(sl["q_bag"])); avline.append(sl["n"]>0)
                    qprev.append(float(sp["q_bag"])); avprev.append(sp["n"]>0)
                dist=B2.P1.source_distribution(index,tok); local.add(pos,dist)
                if dist is not None:
                    rec=(int(pos),dist); line_sources.append(rec); para.append(rec)
                pos+=1
    if not p0:
        raise RuntimeError(f"R8 zero scored tokens for folds {sorted(score_folds)}")
    return {"p0":np.asarray(p0),"qlocal":np.asarray(qlocal),"avlocal":np.asarray(avlocal,dtype=bool),"qline":np.asarray(qline),"avline":np.asarray(avline,dtype=bool),"qprev":np.asarray(qprev),"avprev":np.asarray(avprev,dtype=bool)}


def select_r8_controls(items, parsed, fold_map, outer, parser):
    local_ll=np.zeros(len(B2.GRID)); line_ll=np.zeros(len(B2.GRID)); prev_ll=np.zeros(len(B2.GRID))
    inner_feats=[]
    for g in range(N_FOLDS):
        if g==outer: continue
        _tr,v2,index=generic_fit(items,parsed,fold_map,(outer,g))
        feat=r8_features(items,parsed,fold_map,v2,index,parser,{g},{outer}); inner_feats.append(feat)
        p0=feat["p0"][:,None]; q=feat["qlocal"][:,None]; av=feat["avlocal"][:,None]; grid=B2.GRID[None,:]
        probs=np.where(av,(1-grid)*p0+grid*q,p0); local_ll+=np.log(probs).sum(axis=0)
    li=B2.choose(B2.GRID,local_ll); local_pi=float(B2.GRID[li])
    for feat in inner_feats:
        pl=B2.mix(feat["p0"],feat["qlocal"],feat["avlocal"],local_pi)
        line_ll+=B2.scalar_curve(pl,feat["qline"],feat["avline"])
        prev_ll+=B2.scalar_curve(pl,feat["qprev"],feat["avprev"])
    return {"local_pi":local_pi,"line_alpha":float(B2.GRID[B2.choose(B2.GRID,line_ll)]),"prev_alpha":float(B2.GRID[B2.choose(B2.GRID,prev_ll)])}


def score_r8(items, fold_map):
    parser=B2.I.e.SlotParser(); B2.I.e.validate_parser(parser); parsed=parse_candidate_items(items,parser)
    outer=[]
    for f in range(N_FOLDS):
        sel=select_r8_controls(items,parsed,fold_map,f,parser)
        _tr,v2,index=generic_fit(items,parsed,fold_map,(f,))
        feat=r8_features(items,parsed,fold_map,v2,index,parser,{f},set())
        pl=B2.mix(feat["p0"],feat["qlocal"],feat["avlocal"],sel["local_pi"])
        p_line=B2.mix(pl,feat["qline"],feat["avline"],sel["line_alpha"]); p_prev=B2.mix(pl,feat["qprev"],feat["avprev"],sel["prev_alpha"])
        a0=B2.bits(pl); bl=B2.bits(p_line); bp=B2.bits(p_prev)
        outer.append({"fold":f,"n_scored":len(pl),"selected":sel,"G_same_line_inventory":float(a0-bl),"G_prev_paragraph_inventory":float(a0-bp)})
    gp=[x["G_prev_paragraph_inventory"] for x in outer]; gl=[x["G_same_line_inventory"] for x in outer]
    sp=stability(gp); sl=stability(gl); passed=bool(sp["positive_folds"]>=4 and R8_BAND[0]<=sp["mean"]<=R8_BAND[1] and not sl["pass_positive_4_of_5"])
    return {"pass":passed,"outer":outer,"previous_paragraph":sp,"same_line":sl,"target_band_bits_per_token":list(R8_BAND),"causal_order_preserved_across_fold_mask":True,"future_tokens_used":False}


# ---- score-free preflight -----------------------------------------------------
def preflight(zl_path: Path, it_path: Path, cremma_root: Path, naibbe_root: Path):
    pins={
        "stage0_plan":require_blob(STAGE0_PLAN_PATH,EXPECTED_BLOBS["stage0_plan"],"Stage0 plan"),
        "stage0_manifest":require_blob(STAGE0_MANIFEST_PATH,EXPECTED_BLOBS["stage0_manifest"],"Stage0 manifest"),
        "stage0_checker":require_blob(STAGE0_CHECKER_PATH,EXPECTED_BLOBS["stage0_checker"],"Stage0 checker"),
        "target_plan":require_blob(TARGET_PLAN_PATH,EXPECTED_BLOBS["target_plan"],"Issue172 target plan"),
        "preflight68":require_blob(JCT/"preflight68.py",EXPECTED_BLOBS["preflight68"],"Issue68 preflight"),
        "phase62b":require_blob(EXP/"phase62"/"phase62b_n0.py",EXPECTED_BLOBS["phase62b"],"Phase62B authority"),
        "slotparser":require_blob(EXP/"issue26-music"/"issue26e_core.py",EXPECTED_BLOBS["slotparser"],"SlotParser authority"),
        "phase62c":require_blob(EXP/"phase62"/"phase62c_c0_a1.py",EXPECTED_BLOBS["phase62c"],"Phase62C authority"),
        "phase62p":require_blob(EXP/"phase62"/"phase62p_h62p1.py",EXPECTED_BLOBS["phase62p"],"Phase62P authority"),
        "phase64b":require_blob(EXP/"phase64"/"phase64b_naibbe.py",EXPECTED_BLOBS["phase64b"],"Phase64B authority"),
        "issue81":require_blob(EXP/"cross-token-memory"/"issue81_minimal_memory.py",EXPECTED_BLOBS["issue81"],"Issue81 authority"),
        "r1":require_blob(P4A_DIR/"phase4a_boundary_first_reveal.py",EXPECTED_BLOBS["r1_phase4a_first_reveal"],"R1 authority"),
        "r5":require_blob(EDGE_DIR/"issue145_common_eva_first_reveal.py",EXPECTED_BLOBS["r5_issue145"],"R5 authority"),
        "r7_155":require_blob(CURRIER_DIR/"issue155_common_eva_currier_gate0.py",EXPECTED_BLOBS["r7_issue155_gate"],"R7 Issue155 gate"),
        "r7_155_scorer":require_blob(CURRIER_DIR/"issue155_common_eva_currier_first_reveal.py",EXPECTED_BLOBS["r7_issue155_scorer"],"R7 Issue155 scorer"),
        "r7_158_gate":require_blob(CURRIER_DIR/"issue158_currier_gate_decomposition_gate0.py",EXPECTED_BLOBS["r7_issue158_gate"],"R7 Issue158 gate"),
        "r7_161":require_blob(CURRIER_DIR/"issue161_outcome_factor_gate0.py",EXPECTED_BLOBS["r7_issue161_gate"],"R7 Issue161 gate"),
        "r7_161_scorer":require_blob(CURRIER_DIR/"issue161_outcome_factor_first_reveal.py",EXPECTED_BLOBS["r7_issue161_scorer"],"R7 Issue161 scorer"),
        "r7_167":require_blob(CURRIER_DIR/"issue167_sparse_currier_gate0.py",EXPECTED_BLOBS["r7_issue167_gate"],"R7 Issue167 gate"),
        "r7_167_scorer":require_blob(CURRIER_DIR/"issue167_sparse_currier_first_reveal.py",EXPECTED_BLOBS["r7_issue167_scorer"],"R7 Issue167 scorer"),
        "r8_phase2b":require_blob(P2B_DIR/"phase2b_boundary_localization.py",EXPECTED_BLOBS["r8_phase2b"],"R8 Phase2B authority"),
        "source_order":require_blob(PRED_DIR/"source_order_authority.py",EXPECTED_BLOBS["source_order"],"source order authority"),
    }
    manifest=json.loads(STAGE0_MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest_text=canonical_json(manifest)
    ancestry={
        "base_main": require_ancestor(EXPECTED_BASE_MAIN, "post-Stage0 main"),
        "target_plan_head": require_ancestor(EXPECTED_TARGET_PLAN_HEAD, "corrected target-plan head"),
        "runtime_head": git_head(ROOT),
    }
    if EXPECTED_STAGE0_GATE_SHA256 not in TARGET_PLAN_PATH.read_text(encoding="utf-8"):
        raise RuntimeError("target plan does not name accepted Stage0 Gate result")
    if EXPECTED_BASE_MAIN not in TARGET_PLAN_PATH.read_text(encoding="utf-8"):
        raise RuntimeError("target plan base-main authority changed")

    phase62c_first,phase62p,phase64=load_phase62_authorities()
    parser=P68.e.SlotParser(); P68.e.validate_parser(parser)
    a1=generate_a1(zl_path,parser,phase62c_first,phase62p)
    naibbe=generate_naibbe(cremma_root,naibbe_root,phase64)
    af=a1_fold_map(a1)

    SOURCE_ORDER.configure(zl_path); SOURCE_ORDER.verify(a1["items"])
    a1_order=SOURCE_ORDER.ordered(a1["items"])
    naibbe_order=naibbe["ordered_items"]

    support={}
    for name,items,fmap,order in (
        ("A1",a1["items"],af,a1_order),
        ("Naibbe_C1_E0",naibbe["items"],naibbe["fold_map"],naibbe_order),
    ):
        atoms=atomized_tokens_by_fold(items,fmap)
        r1_p1={str(f):sum(1 for line in atoms[f] for l,r in zip(line,line[1:]) if l is not None and r is not None and len(l)>=2 and len(r)>=2) for f in range(N_FOLDS)}
        r1_mid={str(f):sum(1 for line in atoms[f] for a in line if a is not None and len(a)>=4) for f in range(N_FOLDS)}
        r1_p2={str(f):sum(1 for line in atoms[f] for l,r in zip(line,line[1:]) if l is not None and r is not None and len(l)>=3 and len(r)>=3) for f in range(N_FOLDS)}
        runs=candidate_runs(items,fmap,{it.item_id:it.item_id for it in items})
        r5={str(f):sum(1 for fold,_g,_loc,_ln,run in runs if int(fold)==f for rec in run[1:] if rec["slotparser_accepted"]) for f in range(N_FOLDS)}
        beyond=beyond_line_support(items,fmap,order)
        if any(v<=0 for v in r1_p1.values()) or any(v<=0 for v in r1_mid.values()) or any(v<=0 for v in r1_p2.values()) or any(v<=0 for v in r5.values()) or any(v<=0 for v in beyond.values()):
            raise RuntimeError(f"{name} preflight support gate failed")
        support[name]={"R1_P1_boundary_events":r1_p1,"R1_MID_TOKEN_events":r1_mid,"R1_P2_events":r1_p2,"R5_same_line_accepted_body_events":r5,"R5_item_internal_beyond_line_events":beyond,"fold_item_sha256":{str(f):item_fold_hash([it.item_id for it in order if int(fmap[it.item_id])==f]) for f in range(N_FOLDS)}}

    def causal_audit(order,fmap,group_fn):
        ids=[it.item_id for it in order]
        if len(ids)!=len(set(ids)) or set(ids)!=set(fmap):
            raise RuntimeError("R8 causal order/fold-map identity mismatch")
        group_seq=[str(group_fn(it)) for it in order]
        seen=set(); last=None
        for g in group_seq:
            if g!=last and g in seen:
                raise RuntimeError("R8 causal group is non-contiguous/cyclic")
            seen.add(g); last=g
        counts={str(f):sum(int(fmap[x])==f for x in ids) for f in range(N_FOLDS)}
        if any(v<=0 for v in counts.values()):
            raise RuntimeError("R8 fold assignment has empty fold")
        return {"ordered_item_ids_sha256":item_fold_hash(ids),"n_items":len(ids),"n_causal_groups":len(seen),"fold_item_counts":counts,"acyclic":True,"future_tokens_used":False}
    r8_audit={
        "A1":causal_audit(a1_order,af,lambda it:int(it.leaf)),
        "Naibbe_C1_E0":causal_audit(naibbe_order,naibbe["fold_map"],lambda it:it.document),
    }

    synth={"R1":R1A.self_test(),"R5":E145.self_test(),"R7_155":G155.synthetic_test(),"R7_161":G161.synthetic_test(),"R7_167":S167.self_test()}
    if not all(x.get("ok") for x in synth.values()): raise RuntimeError("historical synthetic self-test failed")

    gate155=G155.run_gate(zl_path,it_path); leaf_currier=S155.leaf_currier_from_gate(gate155)
    r7_runs=candidate_runs(a1["items"],af,{it.item_id:int(it.leaf) for it in a1["items"]})
    regime_runs={r:tuple(x for x in r7_runs if leaf_currier.get(int(x[1]))==r) for r in ("A","B")}
    currier_support={r:{} for r in ("A","B")}
    for f in range(N_FOLDS):
        train=set(range(N_FOLDS))-{f}
        ca=edge_counts(regime_runs["A"],train); cb=edge_counts(regime_runs["B"],train)
        matched,_=G155.support_match(ca,cb); retained=set(matched["A"])
        for r in ("A","B"):
            body=0; matched_body=0
            for fold,_leaf,_loc,_ln,run in regime_runs[r]:
                if int(fold)!=f: continue
                prev=None
                for ti,rec in enumerate(run):
                    syms=E145.token_symbols(rec["atoms"])
                    if ti>0 and rec["slotparser_accepted"]:
                        body+=1; matched_body+=int(prev in retained)
                    prev=syms[-2]
            if body<=0 or matched_body<=0:
                raise RuntimeError(f"A1 R7 {r} fold {f} lacks score-free matched BODY support")
            currier_support[r][str(f)]={"accepted_body":body,"matched_context_body":matched_body}

    empirical_vocab_types=int(phase62c_first["inputs"]["A1_empirical_vocabulary_types"])
    r10={
        "A1":{
            "role":"SURFACE GENERATOR ONLY",
            "issue172_trainable_scalars":0,
            "trainable_scalars":0,
            "empirical_table_dimensions":{"historical_generator":"fold-specific entry/local-family tables; no Issue172 refit"},
            "state_count":{"historical_generator":"no new Issue172 latent state"},
            "transition_table_dimensions":{"historical_generator":"frozen Phase61/62 implementation"},
            "empirical_vocabulary_dependence":{"voynich_types":empirical_vocab_types,"training_side":True},
            "target_token_identity_access":False,
            "layout_access":{"heldout":True,"fields":["item/leaf identity","line count","token-count skeleton"]},
            "currier_access":"SCORING_ONLY_METADATA",
            "section_folio_scribe_access":False,
            "target_derived_lookup_tables":False,
            "external_corpus_plaintext_assumptions":False,
            "inverse_side_information":False,
            "candidate_specific_repairs":False,
            "per_reading_tuning":False,
            "heldout_item_fitting":False,
            "historical_generator_scalar_parameters_per_fold":["entry_strength","local_family_p"],
            "heldout_target_identity_or_statistic_used_for_fitting":False,
            "post_reveal_selection":False,
        },
        "Naibbe_C1_E0":{
            "role":"REVERSIBLE TRANSFORM / DECODER CANDIDATE",
            "issue172_trainable_scalars":0,
            "trainable_scalars":0,
            "empirical_table_dimensions":{"published_codebook_cells":468,"tables":6,"states":3},
            "state_count":3,
            "transition_table_dimensions":{"published_tables":6,"published_codebook_cells":468},
            "empirical_vocabulary_dependence":{"voynich_target_aware_public_codebook":True},
            "target_token_identity_access":False,
            "layout_access":False,
            "currier_access":False,
            "section_folio_scribe_access":False,
            "target_derived_lookup_tables":{"fixed_public_target_aware_codebook":True,"fixed_before_issue172":True},
            "external_corpus_plaintext_assumptions":"CREMMA medieval Latin four-manuscript panel",
            "inverse_side_information":"published decoder only; no new side information",
            "candidate_specific_repairs":False,
            "per_reading_tuning":False,
            "heldout_item_fitting":False,
            "heldout_target_identity_or_statistic_used_for_fitting":False,
            "post_reveal_selection":False,
        },
    }
    return {"gate_pass":True,"scientific_candidate_scores_computed":False,"authority_blobs":pins,"ancestry":ancestry,"stage0_manifest_sha256":hashlib.sha256(manifest_text.encode()).hexdigest(),"surface_support":support,"R8_causal_order_audit":r8_audit,"A1_currier_matched_body_support":currier_support,"Naibbe_R7_disposition":"FAIL_NO_CURRIER_COMPARABLE_CHANNEL","synthetic_self_tests":synth,"R10_predeclared":r10},a1,naibbe,af,a1_order,naibbe_order,leaf_currier,r10,phase62c_first,phase62p


# ---- joint first reveal -------------------------------------------------------
def candidate_class(r: dict, decoder: bool) -> str:
    if r["R10"]["pass"] is False:
        return "OVERFIT / EXCESS-TARGET-ACCESS"
    science=[r[f"R{i}"]["pass"] for i in range(1,9)]
    if all(science):
        if decoder and not r["R9"]["pass"]:
            return "JOINT-STRUCTURAL COMPETITIVE SURFACE/ENCODING MODEL — NOT DECODER"
        return "JOINT-STRUCTURAL COMPETITIVE"
    if any(science):
        return "PARTIAL STRUCTURAL MODEL"
    return "NOT COMPETITIVE"


def score_all(zl_path,it_path,cremma_root,naibbe_root):
    pf,a1,naibbe,af,a1_order,naibbe_order,leaf_currier,r10,phase62c_first,phase62p=preflight(zl_path,it_path,cremma_root,naibbe_root)

    a1_r1=score_r1(a1["items"],af); n_r1=score_r1(naibbe["items"],naibbe["fold_map"])
    a1_r3,a1_r4=score_r3_r4_a1(a1,phase62c_first,phase62p); n_r3,n_r4=score_r3_r4_naibbe(naibbe,a1)
    a1_r5,a1_r6,_a1_r5_runs=score_r5_r6(a1["items"],af,a1_order)
    n_r5,n_r6,_n_runs=score_r5_r6(naibbe["items"],naibbe["fold_map"],naibbe_order)
    a1_r7_runs=candidate_runs(a1["items"],af,{it.item_id:int(it.leaf) for it in a1["items"]})
    a1_r7=score_r7_a1(a1_r7_runs,leaf_currier)

    a1_clone=clone_for_causal_order(a1["items"],a1_order,lambda it:int(it.leaf))
    a1_clone_fold={it.item_id:int(af[it.item_id.split("|",1)[1]]) for it in a1_clone}
    n_clone=clone_for_causal_order(naibbe["items"],naibbe_order,lambda it:it.document)
    n_clone_fold={it.item_id:int(naibbe["fold_map"][it.item_id.split("|",1)[1]]) for it in n_clone}
    a1_r8=score_r8(a1_clone,a1_clone_fold); n_r8=score_r8(n_clone,n_clone_fold)

    r10_a={**r10["A1"],"pass":True}; r10_n={**r10["Naibbe_C1_E0"],"pass":True}
    out={
        "schema":"issue172-historical-anchor-first-reveal-v1","issue":172,"scored":True,"preflight":pf,
        "candidates":{
            "A1":{
                "role":"SURFACE GENERATOR ONLY","R1":a1_r1,"R2":HISTORICAL_R2["A1"],"R3":a1_r3,"R4":a1_r4,"R5":a1_r5,"R6":a1_r6,"R7":a1_r7,"R8":a1_r8,"R9":HISTORICAL_R9["A1"],"R10":r10_a,
            },
            "Naibbe_C1_E0":{
                "role":"REVERSIBLE TRANSFORM / DECODER CANDIDATE","R1":n_r1,"R2":HISTORICAL_R2["Naibbe_C1_E0"],"R3":n_r3,"R4":n_r4,"R5":n_r5,"R6":n_r6,"R7":{"pass":False,"disposition":"FAIL_NO_CURRIER_COMPARABLE_CHANNEL","numerical_target_score_computed":False},"R8":n_r8,"R9":HISTORICAL_R9["Naibbe_C1_E0"],"R10":r10_n,
            },
        },
        "controls":{
            "N0":{"promotion_eligible":False,"role":"CONTROL / NULL"},
            "C0-4":{"promotion_eligible":False,"role":"CONTROL / NULL"},
            "OBSERVABLE_CORE_REPLAY":{"promotion_eligible":False,"target_derived":True,"role":"SCORER-SENSITIVITY POSITIVE CONTROL","frozen_sensitivity_authority":{"R1_target_boundary_effect_positive":True,"R5_common_eva_target_gains":R5_TARGET,"R7_target_currier_gains":R7_TARGET,"R7_first_sufficient_K":16,"R8_previous_paragraph_gain":0.0414587,"R8_same_line_inventory_gain":0.0}},
        },
        "firewall":{"post_reveal_seed_view_representation_or_threshold_selection":False,"new_candidate_repair":False,"per_reading_candidate_tuning":False,"semantic_plaintext_language_cipher_or_historical_inference":False},
    }
    out["candidates"]["A1"]["classification"]=candidate_class(out["candidates"]["A1"],False)
    out["candidates"]["Naibbe_C1_E0"]["classification"]=candidate_class(out["candidates"]["Naibbe_C1_E0"],True)
    out["result_sha256_without_self_field"]=sha256_obj(out)
    return out


def self_test():
    r1=R1A.self_test(); r5=E145.self_test(); r7=S167.self_test()
    vals=stability([1,1,1,1,-1]);
    if not vals["pass_positive_4_of_5"]: raise AssertionError("4/5 stability rule failed")
    if not ratio_band(1.0,(0.75,1.25)): raise AssertionError("conjunctive ratio band failed")
    fake={"R10":{"pass":True},**{f"R{i}":{"pass":True} for i in range(1,9)},"R9":{"pass":False}}
    if "NOT DECODER" not in candidate_class(fake,True): raise AssertionError("decoder R9 classification failed")
    return {"ok":True,"target_sources_loaded":False,"real_issue172_candidate_scores_computed":False,"historical_synthetic":{"R1":r1,"R5":r5,"R7":r7},"joint_rules_tested":True}


def invalid_result(exc:Exception):
    return {"schema":"issue172-historical-anchor-first-reveal-v1","issue":172,"scored":False,"classification":"INVALID / NON-COMPARABLE","error":f"{type(exc).__name__}: {exc}","firewall":{"post_failure_target_driven_repair_allowed":False}}


def main(argv:Sequence[str]|None=None)->int:
    ap=argparse.ArgumentParser(); g=ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--self-test",action="store_true")
    g.add_argument("--run",nargs=5,metavar=("ZL3B","IT2A","CREMMA_ROOT","NAIBBE_ROOT","OUT_JSON"))
    ns=ap.parse_args(argv)
    if ns.self_test:
        print(canonical_json(self_test()),end=""); return 0
    zl,it,cr,nr,out=map(lambda x:Path(x).resolve(),ns.run)
    try: result=score_all(zl,it,cr,nr); rc=0
    except Exception as exc: result=invalid_result(exc); rc=1
    out.parent.mkdir(parents=True,exist_ok=True); out.write_text(canonical_json(result),encoding="utf-8")
    print(canonical_json(result),end=""); return rc


if __name__=="__main__":
    raise SystemExit(main())
