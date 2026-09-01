#!/usr/bin/env python3
"""Issue #72 V2 Stage C1 paired common-support R1 target scorer.

Scientific authorities:
- STAGE_C_FIXED_PATH_RANDOMIZATION_PLAN.md
- STAGE_C_SCORING_AMENDMENT_C1.md
- STAGE_C_TARGET_IMPLEMENTATION.md

One invocation handles one frozen (axis, assignment) pair.  A verify-only mode
reconstructs exact C0 surfaces/support without loading target residual vectors.

Usage:
  python c1_r1_target72_v2.py NAIBBE_ROOT C0_DIR AXIS J OUTPUT_JSON [--verify-only]
"""
from __future__ import annotations

import gzip
import hashlib
import json
import math
import os
import subprocess
import sys
from pathlib import Path
from typing import Mapping, Sequence

import numpy as np

HERE = Path(__file__).resolve()
EXPERIMENTS = HERE.parents[1]
for rel in (
    "phase62",
    "phase64",
    "issue26-music",
    "occupancy-graph-stability",
    "occupancy-graph-residual",
    "occupancy-graph-independent-transcription",
    "joint-constraint-tournament",
):
    p = EXPERIMENTS / rel
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import phase58b_graph_stability as b58  # noqa: E402
import phase58c_residual_graph as c58  # noqa: E402
import phase58d_independent_residual as d58  # noqa: E402
import phase64b_naibbe as n64  # noqa: E402
import target68 as t68  # noqa: E402
import c0_support72_v2 as c0  # noqa: E402
import c0_support72_v2_recovery as c0r  # noqa: E402

AXES = ("EL", "ES", "ET", "EG")
N_ASSIGN = 31
N_REF = 1000
N_EDGES = 66
MANUSCRIPTS = ("BIS193", "CLM13027", "Mazarine915", "UBL758")
REPS = tuple(range(5))
EXPECTED_NAIBBE = "f2675ec5dd275268bc64dd48ea64fc0e0e9827a2"
EXPECTED_C0_GZ_SHA256 = "946d8f8fa61d996a548a344f7e303f804283230ce8bef0d51add473d811e4ed3"
EXPECTED_C0_GZ_BYTES = 12780097
EXPECTED_C0_RAW_SHA256 = "da00a66b77a90eb36a158a9942927a27743e64aba7fac69337ff3a67424d695a"
EXPECTED_C0_RAW_BYTES = 206486933
EXPECTED_C0_MANIFEST_SHA256 = "aba822be57bbac0c04a9fa785a0a835eafe192b406fead5cd7166051825f45ae"
EXPECTED_C0_STATUS = "STAGE C0 FIXED-PATH RANDOMIZATION SUPPORT FROZEN"
EXPECTED_B2_SHA256 = "2da5f0a4f8191820875ed264284f2d3b651489a7e8aeed3805cc2ed4d08c5147"
PAIRS = b58.PAIRS


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def git_head(root: Path) -> str:
    return subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()


def load_c0_authority(c0_dir: Path) -> tuple[dict, dict]:
    gz = c0_dir / "stage_c0_support.json.gz"
    manifest_path = c0_dir / "MANIFEST.json"
    if gz.stat().st_size != EXPECTED_C0_GZ_BYTES:
        raise RuntimeError("C0 gzip byte count mismatch")
    if sha256_file(gz) != EXPECTED_C0_GZ_SHA256:
        raise RuntimeError("C0 gzip SHA mismatch")
    if sha256_file(manifest_path) != EXPECTED_C0_MANIFEST_SHA256:
        raise RuntimeError("C0 manifest SHA mismatch")
    with gzip.open(gz, "rb") as f:
        raw = f.read()
    if len(raw) != EXPECTED_C0_RAW_BYTES or sha256_bytes(raw) != EXPECTED_C0_RAW_SHA256:
        raise RuntimeError("C0 reconstructed raw identity mismatch")
    obj = json.loads(raw)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if obj["status"] != EXPECTED_C0_STATUS:
        raise RuntimeError("C0 status mismatch")
    if obj["stage_b2_authority_sha256"] != EXPECTED_B2_SHA256:
        raise RuntimeError("C0 Stage B2 authority changed")
    if obj["population"]["process_reps"] != list(REPS):
        raise RuntimeError("C0 process population changed")
    if obj["population"]["axes"] != list(AXES) or obj["population"]["randomizations_per_axis"] != N_ASSIGN:
        raise RuntimeError("C0 randomization population changed")
    if any(bool(v) for v in obj["target_access"].values()):
        raise RuntimeError("C0 target firewall is not clean")
    if manifest["stage_c0_support_sha256"] != EXPECTED_C0_RAW_SHA256 or manifest["stage_c0_support_bytes"] != EXPECTED_C0_RAW_BYTES:
        raise RuntimeError("C0 manifest/raw mismatch")
    return obj, manifest


def load_traces(c0_dir: Path, c0obj: Mapping) -> dict:
    traces: dict[int, dict[str, dict]] = {}
    for rep in REPS:
        traces[rep] = {}
        for ms in MANUSCRIPTS:
            key = f"rep{rep}:{ms}"
            meta = c0obj["trace_manifest"][key]
            path = c0_dir / meta["file"]
            if path.stat().st_size != int(meta["gzip_size"]):
                raise RuntimeError(f"trace gzip size mismatch {key}")
            if sha256_file(path) != meta["gzip_sha256"]:
                raise RuntimeError(f"trace gzip SHA mismatch {key}")
            with gzip.open(path, "rt", encoding="utf-8") as f:
                row = json.load(f)
            if row["rep"] != rep or row["manuscript"] != ms or row["seed"] != meta["seed"]:
                raise RuntimeError(f"trace identity mismatch {key}")
            traces[rep][ms] = row
    return traces


def compare_support(got: Mapping, expected: Mapping, label: str) -> None:
    for k in ("visible_tokens", "accepted_tokens"):
        if int(got[k]) != int(expected[k]):
            raise RuntimeError(f"{label} support mismatch {k}: {got[k]} != {expected[k]}")
    if abs(float(got["coverage"]) - float(expected["coverage"])) > 1e-15:
        raise RuntimeError(f"{label} coverage mismatch")


def reconstruct_surfaces(naibbe_root: Path, c0obj: Mapping, traces: Mapping, axis: str, j: int):
    if git_head(naibbe_root) != EXPECTED_NAIBBE:
        raise RuntimeError("Naibbe commit mismatch")
    module = n64.load_naibbe(naibbe_root)
    original_map = dict(module.placeholder_to_glyph)
    random_map, _invariants = c0r.randomized_map_recovery(original_map, axis, j)

    baseline: dict[int, dict[str, Sequence]] = {}
    randomized: dict[int, dict[str, Sequence]] = {}
    baseline_rep_shas = {}
    for rep in REPS:
        baseline[rep] = {}
        randomized[rep] = {}
        for ms in MANUSCRIPTS:
            trace = traces[rep][ms]["trace"]
            bp, _br = c0.render_trace(trace, ms, original_map)
            rp, _rr = c0.render_trace(trace, ms, random_map)
            baseline[rep][ms] = bp
            randomized[rep][ms] = rp
        plain_pool = [it for ms in MANUSCRIPTS for it in baseline[rep][ms]]
        got = c0.surface_sha(plain_pool)
        expected = c0obj["baseline"]["per_rep"][f"rep{rep}"]["pooled_primary_surface_sha256"]
        if got != expected:
            raise RuntimeError(f"baseline rep{rep} surface SHA mismatch")
        baseline_rep_shas[f"rep{rep}"] = got

    rand_pool = c0.pooled(randomized)
    rand_sha = c0.surface_sha(rand_pool)
    c0row = c0obj["randomizations"][axis][f"r{j}"]
    if rand_sha != c0row["surface_sha256"]:
        raise RuntimeError("randomized pooled surface SHA mismatch")
    parser = c0.e.SlotParser()
    c0.e.validate_parser(parser)
    got_support = c0.parser_support(rand_pool, parser)
    compare_support(got_support, c0row["parser_support"], "randomized pooled")

    mask_rows = c0row["common_support"]["per_line_counts_and_mask"]
    mask_sha = sha256_bytes(c0.canonical_json_bytes(mask_rows))
    if mask_sha != c0row["common_support"]["mask_payload_sha256"]:
        raise RuntimeError("stored common-support mask payload SHA mismatch")

    return baseline, randomized, parser, baseline_rep_shas, rand_sha, c0row


def line_lookup(items_by_rep_ms: Mapping) -> dict:
    out = {}
    for rep in REPS:
        for ms in MANUSCRIPTS:
            for it in items_by_rep_ms[rep][ms]:
                for li, line in enumerate(it.lines):
                    key = (rep, ms, it.item_id, int(li))
                    if key in out:
                        raise RuntimeError(f"duplicate line key {key}")
                    out[key] = line
    return out


def occ(parser, units) -> np.ndarray:
    tok = "".join(units)
    picked = parser.pick(tok, "min")
    if picked is None:
        raise RuntimeError("C0 common-support position no longer parses")
    vals = picked[1]
    return np.fromiter((bool(vals[s]) for s in range(12)), dtype=np.uint8, count=12)


def make_dataset(lines: list[dict]) -> dict:
    if not lines:
        raise RuntimeError("empty common-support dataset")
    X = np.concatenate([x["occ"] for x in lines], axis=0)
    token_folds = np.concatenate([
        np.full(len(x["occ"]), int(x["fold"]), dtype=np.int8) for x in lines
    ])
    maxlen = max(len(x["occ"]) for x in lines)
    padded = np.zeros((len(lines), maxlen, 12), dtype=np.uint8)
    line_mask = np.zeros((len(lines), maxlen), dtype=bool)
    for i, row in enumerate(lines):
        z = row["occ"]
        padded[i, : len(z)] = z
        line_mask[i, : len(z)] = True
    if not np.array_equal(padded[line_mask], X):
        raise RuntimeError("common-support padded/flat order mismatch")
    return {
        "X": X,
        "token_folds": token_folds,
        "padded": padded,
        "line_mask": line_mask,
        "line_count": len(lines),
        "token_count": int(len(X)),
    }


def build_common_pair(baseline: Mapping, randomized: Mapping, parser, c0row: Mapping) -> tuple[dict, dict, dict]:
    blook = line_lookup(baseline)
    rlook = line_lookup(randomized)
    mask_rows = c0row["common_support"]["per_line_counts_and_mask"]
    if set(blook) != set(rlook):
        raise RuntimeError("baseline/randomized line key sets differ")
    if len(mask_rows) != len(blook):
        raise RuntimeError("C0 mask-line population does not match reconstructed lines")

    blines = []
    rlines = []
    seen = set()
    common_total = 0
    for row in mask_rows:
        key = (int(row["rep"]), row["manuscript"], row["item_id"], int(row["line_index"]))
        if key in seen:
            raise RuntimeError(f"duplicate C0 mask line {key}")
        seen.add(key)
        if key not in blook:
            raise RuntimeError(f"C0 mask line not reconstructed {key}")
        bline = blook[key]
        rline = rlook[key]
        if len(bline) != len(rline) or len(bline) != int(row["visible_positions"]):
            raise RuntimeError(f"visible line length mismatch {key}")
        mask = row["mask"]
        if len(mask) != len(bline) or mask.count("1") != int(row["common_support_count"]):
            raise RuntimeError(f"C0 mask content/count mismatch {key}")
        bo = []
        ro = []
        for ti, flag in enumerate(mask):
            if flag == "0":
                continue
            if flag != "1":
                raise RuntimeError("invalid common-support mask character")
            bo.append(occ(parser, bline[ti]))
            ro.append(occ(parser, rline[ti]))
        if bo:
            fold = MANUSCRIPTS.index(row["manuscript"])
            blines.append({"fold": fold, "rep": int(row["rep"]), "occ": np.stack(bo)})
            rlines.append({"fold": fold, "rep": int(row["rep"]), "occ": np.stack(ro)})
            common_total += len(bo)

    if seen != set(blook):
        raise RuntimeError("not every reconstructed line has a frozen C0 mask")
    expected_total = int(c0row["common_support"]["common_support_count"])
    if common_total != expected_total:
        raise RuntimeError(f"common-support total mismatch {common_total} != {expected_total}")

    bd = make_dataset(blines)
    rd = make_dataset(rlines)
    if bd["token_count"] != rd["token_count"] or not np.array_equal(bd["line_mask"], rd["line_mask"]):
        raise RuntimeError("paired common-support dataset geometry differs")

    expected_fold_counts = []
    by_ms = c0row["common_support"]["per_rep_manuscript"]
    for ms in MANUSCRIPTS:
        expected_fold_counts.append(sum(int(by_ms[f"rep{rep}:{ms}"]["common"]) for rep in REPS))
    got_folds = [int(np.sum(bd["token_folds"] == f)) for f in range(4)]
    if got_folds != expected_fold_counts:
        raise RuntimeError(f"four-manuscript fold counts mismatch {got_folds} != {expected_fold_counts}")
    if not np.array_equal(bd["token_folds"], rd["token_folds"]):
        raise RuntimeError("paired fold identity mismatch")

    support = {
        "common_support_count": expected_total,
        "common_support_fraction": float(c0row["common_support"]["common_support_fraction"]),
        "visible_positions": int(c0row["common_support"]["visible_positions"]),
        "baseline_parser_accepted_full": int(c0row["common_support"]["baseline_parser_accepted"]),
        "randomized_parser_accepted_full": int(c0row["common_support"]["randomized_parser_accepted"]),
        "randomized_full_coverage": float(c0row["parser_support"]["coverage"]),
        "mask_payload_sha256": c0row["common_support"]["mask_payload_sha256"],
        "common_line_count": int(bd["line_count"]),
        "four_manuscript_fold_counts": got_folds,
    }
    return bd, rd, support


def full_q(d: Mapping, X: np.ndarray) -> np.ndarray:
    q = t68.q_views_candidate(d, X, False)["full"]
    if q.shape != (N_EDGES,) or not np.all(np.isfinite(q)):
        raise RuntimeError("invalid full Q vector")
    return q


def build_reference(d: Mapping, namespace: str, label: str) -> np.ndarray:
    ref = np.empty((N_REF, N_EDGES), dtype=np.float64)
    for n in range(N_REF):
        Y = c58.shuffled_flat(d, namespace, n)
        ref[n] = full_q(d, Y)
        if (n + 1) % 100 == 0:
            print(f"{label} reference {n+1}/{N_REF}", file=sys.stderr, flush=True)
    return np.sort(ref, axis=0)


def residualize(q: np.ndarray, sref: np.ndarray) -> np.ndarray:
    z = c58.normal_score_array(q, sref)
    if z.shape != (N_EDGES,) or not np.all(np.isfinite(z)):
        raise RuntimeError("invalid residual-Z vector")
    return z


def target_metrics(z: np.ndarray, targets: Mapping[str, np.ndarray]) -> dict:
    out = {}
    for name, target in targets.items():
        rr = b58.corr(z, target)
        if rr is None or not math.isfinite(float(rr)):
            raise RuntimeError(f"undefined target correlation {name}")
        out[name] = {
            "pearson": float(rr),
            "sign_agreement": int(d58.sign_agreement(z, target)),
            "sign_denominator": N_EDGES,
        }
    return out


def verify_only(naibbe_root: Path, c0_dir: Path, axis: str, j: int, output: Path) -> int:
    c0obj, _manifest = load_c0_authority(c0_dir)
    traces = load_traces(c0_dir, c0obj)
    baseline, randomized, parser, base_shas, rand_sha, c0row = reconstruct_surfaces(
        naibbe_root, c0obj, traces, axis, j
    )
    bd, rd, support = build_common_pair(baseline, randomized, parser, c0row)
    # Deliberately stop before Q, residuals, target loading or target correlations.
    result = {
        "schema": "issue72-v2-stage-c1-target-blind-preflight-v1",
        "status": "C1 SUPPORT RECONSTRUCTION VERIFIED TARGET BLIND",
        "axis": axis,
        "randomization": j,
        "c0_raw_sha256": EXPECTED_C0_RAW_SHA256,
        "baseline_rep_surface_sha256": base_shas,
        "randomized_pooled_surface_sha256": rand_sha,
        "support": support,
        "paired_geometry": {
            "baseline_tokens": bd["token_count"],
            "randomized_tokens": rd["token_count"],
            "same_line_mask": bool(np.array_equal(bd["line_mask"], rd["line_mask"])),
            "same_fold_identity": bool(np.array_equal(bd["token_folds"], rd["token_folds"])),
        },
        "target_access": {
            "slot_pair_Q_computed": False,
            "residual_Z_computed": False,
            "target_vectors_loaded": False,
            "target_correlation_computed": False,
        },
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "axis": axis, "r": j, "support": support}, sort_keys=True))
    return 0


def score(naibbe_root: Path, c0_dir: Path, axis: str, j: int, output: Path) -> int:
    c0obj, _manifest = load_c0_authority(c0_dir)
    traces = load_traces(c0_dir, c0obj)
    baseline, randomized, parser, base_shas, rand_sha, c0row = reconstruct_surfaces(
        naibbe_root, c0obj, traces, axis, j
    )
    bd, rd, support = build_common_pair(baseline, randomized, parser, c0row)

    baseline_q = full_q(bd, bd["X"])
    randomized_q = full_q(rd, rd["X"])
    base_ns = f"issue72v2:C1:{axis}:r{j}:baseline-common:reference:v1"
    rand_ns = f"issue72v2:C1:{axis}:r{j}:randomized-common:reference:v1"
    base_ref = build_reference(bd, base_ns, f"{axis} r{j} baseline")
    rand_ref = build_reference(rd, rand_ns, f"{axis} r{j} randomized")
    baseline_z = residualize(baseline_q, base_ref)
    randomized_z = residualize(randomized_q, rand_ref)

    # Frozen targets are loaded only after C0 reconstruction and both candidate-owned
    # residual coordinates have been completed.
    targets, target_authority = t68.load_target_references()
    bt = target_metrics(baseline_z, targets)
    rt = target_metrics(randomized_z, targets)
    topology = {}
    for name in ("ZL3b", "IT2a"):
        topology[name] = {
            "baseline_pearson": bt[name]["pearson"],
            "randomized_pearson": rt[name]["pearson"],
            "DELTA_R_randomized_minus_baseline": float(rt[name]["pearson"] - bt[name]["pearson"]),
            "baseline_sign_agreement": bt[name]["sign_agreement"],
            "randomized_sign_agreement": rt[name]["sign_agreement"],
            "sign_denominator": N_EDGES,
        }

    result = {
        "schema": "issue72-v2-stage-c1-paired-r1-target-v1",
        "status": "STAGE C1 ASSIGNMENT TARGET SCORED",
        "target_reveal": True,
        "github_sha": os.environ.get("C1_TARGET_HEAD_SHA") or os.environ.get("GITHUB_SHA"),
        "axis": axis,
        "randomization": j,
        "scientific_role": "FIXED_PATH_ASSOCIATION_CAUSAL_LOCALIZATION_ON_FROZEN_COMMON_SUPPORT",
        "authority": {
            "Naibbe_commit": EXPECTED_NAIBBE,
            "C0_raw_sha256": EXPECTED_C0_RAW_SHA256,
            "C0_gzip_sha256": EXPECTED_C0_GZ_SHA256,
            "C0_manifest_sha256": EXPECTED_C0_MANIFEST_SHA256,
            "target_authority": target_authority,
        },
        "surface_identity": {
            "baseline_rep_surface_sha256": base_shas,
            "randomized_pooled_surface_sha256": rand_sha,
            "C0_expected_randomized_pooled_surface_sha256": c0row["surface_sha256"],
        },
        "support": support,
        "reference_null": {
            "n_reference_each_side": N_REF,
            "baseline_namespace": base_ns,
            "randomized_namespace": rand_ns,
            "null": "line-local slot-occupancy shuffle on the exact frozen common-support line fragments",
            "test_null_computed": False,
        },
        "pairs": [list(map(int, p)) for p in PAIRS],
        "baseline_common": {
            "q_full": baseline_q.tolist(),
            "z_full": baseline_z.tolist(),
            "residual_energy": float(c58.residual_energy(baseline_z)),
        },
        "randomized_common": {
            "q_full": randomized_q.tolist(),
            "z_full": randomized_z.tolist(),
            "residual_energy": float(c58.residual_energy(randomized_z)),
        },
        "topology": topology,
        "decision_policy": {
            "hard_intervention_threshold_applied": False,
            "readings_averaged": False,
            "coverage_gate_applied": False,
            "primary_estimand": "DELTA_R_randomized_minus_baseline on exact C0 common support",
            "negative_delta_meaning": "published assignment more Voynich-R1-like on paired support",
        },
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "axis": axis,
        "r": j,
        "support": support["common_support_fraction"],
        "delta": {name: topology[name]["DELTA_R_randomized_minus_baseline"] for name in topology},
    }, sort_keys=True))
    return 0


def self_test() -> int:
    if len(PAIRS) != 66 or N_REF != 1000 or N_ASSIGN != 31 or len(MANUSCRIPTS) != 4:
        raise RuntimeError("frozen C1 constants changed")
    X = np.zeros((16, 12), dtype=np.uint8)
    for i in range(16):
        X[i, i % 12] = 1
        X[i, (i + 3) % 12] = 1
    lines = [{"fold": i % 4, "rep": 0, "occ": X[i:i+1]} for i in range(16)]
    d = make_dataset(lines)
    q = full_q(d, d["X"])
    if q.shape != (66,):
        raise RuntimeError("C1 self-test Q shape failed")
    print(json.dumps({
        "C1_self_test": "ok",
        "n_edges": len(PAIRS),
        "n_reference": N_REF,
        "n_assign": N_ASSIGN,
        "fold_semantics": "4_MANUSCRIPTS_NOT_20_REP_X_MANUSCRIPT_PSEUDOFOLDS",
        "target_loaded": False,
    }, sort_keys=True))
    return 0


def main(argv: Sequence[str]) -> int:
    if len(argv) == 2 and argv[1] == "--self-test":
        return self_test()
    if len(argv) not in (6, 7):
        raise SystemExit(f"usage: {argv[0]} NAIBBE_ROOT C0_DIR AXIS J OUTPUT_JSON [--verify-only]")
    nai = Path(argv[1]).resolve()
    c0_dir = Path(argv[2]).resolve()
    axis = argv[3]
    j = int(argv[4])
    output = Path(argv[5]).resolve()
    if axis not in AXES or j not in range(N_ASSIGN):
        raise SystemExit("invalid AXIS/J")
    verify = len(argv) == 7 and argv[6] == "--verify-only"
    if len(argv) == 7 and not verify:
        raise SystemExit("only optional flag is --verify-only")
    return verify_only(nai, c0_dir, axis, j, output) if verify else score(nai, c0_dir, axis, j, output)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
