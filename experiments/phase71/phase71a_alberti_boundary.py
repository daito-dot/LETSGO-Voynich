#!/usr/bin/env python3
"""Phase71A source-grounded Alberti boundary-signal mechanism test.

Primary scientific question is frozen in PLAN_A.md. The executable can run a
strict construction-only preflight without calling any Phase62/64 scientific
metric, or perform the first authorized score after the preflight is sealed.

Usage:
  python experiments/phase71/phase71a_alberti_boundary.py \
      ZL3b-n.txt /path/to/CREMMA-Medieval-LAT --preflight-only

  python experiments/phase71/phase71a_alberti_boundary.py \
      ZL3b-n.txt /path/to/CREMMA-Medieval-LAT
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

HERE = Path(__file__).resolve().parent
PHASE64 = HERE.parent / "phase64"
if str(PHASE64) not in sys.path:
    sys.path.insert(0, str(PHASE64))

import phase64b_naibbe as core  # noqa: E402

b = core.b

STATIONARY = "ABCDEFGILMNOPQRSTVXZ1234"
PLAIN_CAPS = "ABCDEFGILMNOPQRSTVXZ"
PLAIN_LOWER = PLAIN_CAPS.lower()
MOVABLE = "gklnprtuz&xysomqihfdbace"
INDEX = "k"
PRIMARY_INTERVAL = 4
SENSITIVITY_INTERVAL = 3
REPS = 5
TIE_EPS = 1e-12


@dataclass
class ProjectedItem:
    item_id: str
    document: str
    lines: List[List[str]]


def stable_indicator(key: str, previous: Optional[str] = None) -> str:
    digest = hashlib.sha256(("phase71-alberti-indicator-v1|" + key).encode("utf-8")).digest()
    idx = int.from_bytes(digest[:8], "big") % len(PLAIN_CAPS)
    value = PLAIN_CAPS[idx]
    if previous is not None and value == previous:
        value = PLAIN_CAPS[(idx + 1) % len(PLAIN_CAPS)]
    return value


def alignment_map(indicator: str) -> Dict[str, str]:
    if indicator not in PLAIN_CAPS:
        raise ValueError(f"invalid indicator: {indicator}")
    outer_pos = STATIONARY.index(indicator)
    index_pos = MOVABLE.index(INDEX)
    shift = outer_pos - index_pos
    rotated = "".join(MOVABLE[(i - shift) % len(MOVABLE)] for i in range(len(MOVABLE)))
    if rotated[outer_pos] != INDEX:
        raise RuntimeError("alignment construction failed")
    return {
        ch.lower(): rotated[STATIONARY.index(ch)]
        for ch in PLAIN_CAPS
    }


def project_word(token: b.Token) -> Tuple[str, List[str]]:
    raw = "".join(token)
    norm = unicodedata.normalize("NFKD", raw).lower().replace("j", "i").replace("u", "v")
    out: List[str] = []
    dropped: List[str] = []
    for ch in norm:
        if unicodedata.combining(ch):
            continue
        if ch in PLAIN_LOWER:
            out.append(ch)
        elif ch.isalpha():
            dropped.append(ch)
    return "".join(out), dropped


def project_manuscript(items: Sequence[b.Item], manuscript: str) -> Tuple[List[ProjectedItem], dict]:
    projected: List[ProjectedItem] = []
    source_words = retained_words = retained_chars = dropped_chars = 0
    dropped_types = set()
    nonempty_items = 0
    source_units = 0

    for item in items:
        out_lines: List[List[str]] = []
        item_nonempty = False
        for line in item.lines:
            words: List[str] = []
            for tok in line:
                source_words += 1
                source_units += len(tok)
                word, dropped = project_word(tok)
                dropped_chars += len(dropped)
                dropped_types.update(dropped)
                if word:
                    words.append(word)
                    retained_words += 1
                    retained_chars += len(word)
                    item_nonempty = True
            out_lines.append(words)
        if item_nonempty:
            nonempty_items += 1
        projected.append(ProjectedItem(item.item_id, manuscript, out_lines))

    fingerprint = plaintext_fingerprint(projected)
    return projected, {
        "source_items": len(items),
        "nonempty_projected_items": nonempty_items,
        "source_words": source_words,
        "source_graphematic_units": source_units,
        "retained_words": retained_words,
        "retained_characters": retained_chars,
        "dropped_unsupported_characters": dropped_chars,
        "dropped_unsupported_character_types": sorted(dropped_types),
        "projected_plaintext_sha256": fingerprint,
    }


def plaintext_fingerprint(items: Sequence[ProjectedItem]) -> str:
    h = hashlib.sha256()
    for item in items:
        h.update(item.item_id.encode("utf-8"))
        h.update(b"\0")
        for line in item.lines:
            for word in line:
                h.update(word.encode("ascii"))
                h.update(b"\x1f")
            h.update(b"\x1e")
        h.update(b"\x1d")
    return h.hexdigest()


def ciphertext_fingerprint(items: Sequence[b.Item]) -> str:
    h = hashlib.sha256()
    for item in items:
        h.update(item.item_id.encode("utf-8"))
        h.update(b"\0")
        for line in item.lines:
            for tok in line:
                h.update("".join(tok).encode("utf-8"))
                h.update(b"\x1f")
            h.update(b"\x1e")
        h.update(b"\x1d")
    return h.hexdigest()


def encrypt_word(word: str, mapping: Dict[str, str]) -> str:
    try:
        return "".join(mapping[ch] for ch in word)
    except KeyError as exc:
        raise RuntimeError(f"unprojected plaintext character reached cipher: {exc}") from exc


def encode_projected(
    projected: Sequence[ProjectedItem],
    manuscript: str,
    realization: int,
    interval: int,
    arm: str,
) -> Tuple[List[b.Item], dict]:
    if arm not in {"CONT", "PARA"}:
        raise ValueError(arm)
    if interval not in {PRIMARY_INTERVAL, SENSITIVITY_INTERVAL}:
        raise ValueError(interval)

    out: List[b.Item] = []
    current_indicator: Optional[str] = None
    mapping: Optional[Dict[str, str]] = None
    word_count = 0
    continuous_block = 0
    total_tokens = 0
    total_data_units = 0
    initial_indicators = 0
    periodic_indicators = 0
    paragraph_resets = 0
    prefixed_signals = 0
    started = False

    for item in projected:
        item_words = sum(len(line) for line in item.lines)
        if arm == "PARA" and item_words:
            paragraph_resets += 1
            current_indicator = stable_indicator(
                f"{manuscript}|r{realization}|i{interval}|PARA|initial|{item.item_id}"
            )
            mapping = alignment_map(current_indicator)
            word_count = 0
            initial_indicators += 1
            pending_signal: Optional[str] = current_indicator
        elif arm == "CONT" and item_words and not started:
            current_indicator = stable_indicator(
                f"{manuscript}|r{realization}|i{interval}|CONT|initial"
            )
            mapping = alignment_map(current_indicator)
            word_count = 0
            initial_indicators += 1
            pending_signal = current_indicator
            started = True
        else:
            pending_signal = None

        out_lines: List[b.Line] = []
        local_block = 0
        for line in item.lines:
            oline: b.Line = []
            for word in line:
                if mapping is None or current_indicator is None:
                    raise RuntimeError("cipher mapping missing before retained plaintext word")

                if word_count >= interval:
                    if arm == "PARA":
                        local_block += 1
                        key = (
                            f"{manuscript}|r{realization}|i{interval}|PARA|periodic|"
                            f"{item.item_id}|{local_block}"
                        )
                    else:
                        continuous_block += 1
                        key = (
                            f"{manuscript}|r{realization}|i{interval}|CONT|periodic|"
                            f"{continuous_block}"
                        )
                    current_indicator = stable_indicator(key, previous=current_indicator)
                    mapping = alignment_map(current_indicator)
                    pending_signal = current_indicator
                    periodic_indicators += 1
                    word_count = 0

                cipher_word = encrypt_word(word, mapping)
                if not cipher_word:
                    raise RuntimeError("retained plaintext produced empty ciphertext word")
                token_text = (pending_signal or "") + cipher_word
                if pending_signal is not None:
                    prefixed_signals += 1
                    pending_signal = None
                if not any(ch in MOVABLE for ch in token_text):
                    raise RuntimeError("ciphertext token lacks encrypted data unit")
                oline.append(tuple(token_text))
                total_tokens += 1
                total_data_units += len(cipher_word)
                word_count += 1
            out_lines.append(oline)
        out.append(b.Item(item.item_id, manuscript, out_lines, None))

    return out, {
        "arm": arm,
        "interval_words": interval,
        "realization": realization,
        "plaintext_sha256": plaintext_fingerprint(projected),
        "ciphertext_sha256": ciphertext_fingerprint(out),
        "cipher_tokens": total_tokens,
        "encrypted_data_units": total_data_units,
        "initial_indicators": initial_indicators,
        "periodic_indicators": periodic_indicators,
        "prefixed_signals": prefixed_signals,
        "paragraph_resets": paragraph_resets,
    }


def validate_ring() -> dict:
    if len(STATIONARY) != 24 or len(MOVABLE) != 24:
        raise RuntimeError("Alberti ring length mismatch")
    if len(set(STATIONARY)) != 24 or len(set(MOVABLE)) != 24:
        raise RuntimeError("Alberti ring symbols must be unique")
    if MOVABLE.count(INDEX) != 1:
        raise RuntimeError("Alberti movable index must occur exactly once")
    if len(PLAIN_CAPS) != 20 or STATIONARY[:20] != PLAIN_CAPS:
        raise RuntimeError("Alberti plaintext alphabet mismatch")

    mapping_hashes = {}
    for cap in PLAIN_CAPS:
        mp = alignment_map(cap)
        if set(mp) != set(PLAIN_LOWER):
            raise RuntimeError(f"alignment {cap}: plaintext alphabet mismatch")
        if len(set(mp.values())) != 20:
            raise RuntimeError(f"alignment {cap}: plaintext mapping is not one-to-one")
        mapping_hashes[cap] = hashlib.sha256(
            json.dumps(mp, sort_keys=True).encode("utf-8")
        ).hexdigest()
    return {
        "stationary": STATIONARY,
        "movable": MOVABLE,
        "index": INDEX,
        "plaintext_letters": PLAIN_CAPS,
        "alignment_mapping_sha256": mapping_hashes,
    }


def load_projected_sources(cremma_root: Path) -> Tuple[Dict[str, List[ProjectedItem]], Dict[str, dict]]:
    raw_sources = {
        name: b.parse_latin_manuscript(cremma_root, name, rel)
        for name, rel in b.PRIMARY_MANUSCRIPTS.items()
    }
    projected: Dict[str, List[ProjectedItem]] = {}
    diagnostics: Dict[str, dict] = {}
    for name in b.PRIMARY_MANUSCRIPTS:
        projected[name], diagnostics[name] = project_manuscript(raw_sources[name], name)
    return projected, diagnostics


def construction_preflight(voynich_path: Path, cremma_root: Path) -> dict:
    zblob = b.git_blob_sha1(voynich_path.read_bytes())
    if zblob != b.EXPECTED_ZL3B_BLOB:
        raise RuntimeError(f"ZL3b authority mismatch: {zblob} != {b.EXPECTED_ZL3B_BLOB}")
    ccommit = b.verify_cremma_commit(cremma_root)
    ring = validate_ring()
    projected, projection_diag = load_projected_sources(cremma_root)

    paired = {}
    for manuscript, items in projected.items():
        para1, pd1 = encode_projected(items, manuscript, 0, PRIMARY_INTERVAL, "PARA")
        para2, pd2 = encode_projected(items, manuscript, 0, PRIMARY_INTERVAL, "PARA")
        cont1, cd1 = encode_projected(items, manuscript, 0, PRIMARY_INTERVAL, "CONT")
        cont2, cd2 = encode_projected(items, manuscript, 0, PRIMARY_INTERVAL, "CONT")

        if pd1["ciphertext_sha256"] != pd2["ciphertext_sha256"]:
            raise RuntimeError(f"{manuscript}: PARA is not deterministic")
        if cd1["ciphertext_sha256"] != cd2["ciphertext_sha256"]:
            raise RuntimeError(f"{manuscript}: CONT is not deterministic")
        if pd1["plaintext_sha256"] != cd1["plaintext_sha256"]:
            raise RuntimeError(f"{manuscript}: paired plaintext differs")
        if pd1["cipher_tokens"] != projection_diag[manuscript]["retained_words"]:
            raise RuntimeError(f"{manuscript}: PARA token count changed")
        if cd1["cipher_tokens"] != projection_diag[manuscript]["retained_words"]:
            raise RuntimeError(f"{manuscript}: CONT token count changed")
        expected_para_initial = projection_diag[manuscript]["nonempty_projected_items"]
        if pd1["initial_indicators"] != expected_para_initial:
            raise RuntimeError(f"{manuscript}: PARA initial indicator count mismatch")
        expected_cont_initial = int(projection_diag[manuscript]["retained_words"] > 0)
        if cd1["initial_indicators"] != expected_cont_initial:
            raise RuntimeError(f"{manuscript}: CONT initial indicator count mismatch")
        if cd1["paragraph_resets"] != 0:
            raise RuntimeError(f"{manuscript}: CONT unexpectedly resets at paragraphs")
        if pd1["paragraph_resets"] != expected_para_initial:
            raise RuntimeError(f"{manuscript}: PARA paragraph reset count mismatch")
        if pd1["prefixed_signals"] != pd1["initial_indicators"] + pd1["periodic_indicators"]:
            raise RuntimeError(f"{manuscript}: PARA signal prefix accounting mismatch")
        if cd1["prefixed_signals"] != cd1["initial_indicators"] + cd1["periodic_indicators"]:
            raise RuntimeError(f"{manuscript}: CONT signal prefix accounting mismatch")
        if any(not tok for it in para1 for line in it.lines for tok in line):
            raise RuntimeError(f"{manuscript}: empty PARA ciphertext token")
        if any(not tok for it in cont1 for line in it.lines for tok in line):
            raise RuntimeError(f"{manuscript}: empty CONT ciphertext token")

        paired[manuscript] = {
            "projection": projection_diag[manuscript],
            "PARA_rep0": pd1,
            "CONT_rep0": cd1,
        }

    return {
        "status": "PASS",
        "voynich_git_blob_sha1": zblob,
        "cremma_commit": ccommit,
        "ring": ring,
        "paired_construction": paired,
        "scientific_metrics_called": False,
    }


def load_science_context(voynich_path: Path) -> Tuple[List[dict], dict, dict]:
    phase62c_path = core.PHASE62 / "phase62c_c0_a1_results.json"
    phase62p_path = core.PHASE62 / "phase62p_h62p1_results.json"
    phase63a_path = core.PHASE63 / "phase63a_training_vocab_results.json"
    if core.sha256_file(phase62p_path) != core.PHASE62P_SHA256:
        raise RuntimeError("Phase62P authority digest mismatch")
    if core.sha256_file(phase63a_path) != core.PHASE63A_SHA256:
        raise RuntimeError("Phase63A authority digest mismatch")
    phase62c = json.loads(phase62c_path.read_text(encoding="utf-8"))
    phase62p = json.loads(phase62p_path.read_text(encoding="utf-8"))
    phase63a = json.loads(phase63a_path.read_text(encoding="utf-8"))
    if phase62p["across_fold"]["prospective_profile_leader"] != "A1":
        raise RuntimeError("Phase62P authority no longer records A1 as leader")
    contexts, _ = core.fold_contexts(voynich_path, phase62c, phase63a)
    return contexts, phase62p, phase63a


def run_arm(
    projected: Dict[str, List[ProjectedItem]],
    contexts: Sequence[dict],
    phase63a: dict,
    interval: int,
    arm: str,
) -> dict:
    per_manuscript = {}
    diagnostics = {}
    for manuscript in core.MANUSCRIPTS:
        reps = {}
        rdiag = {}
        for r in range(REPS):
            items, diag = encode_projected(projected[manuscript], manuscript, r, interval, arm)
            reps[f"rep{r}"] = core.output_metrics(
                items,
                f"Phase71A:{arm}:i{interval}:{manuscript}:rep{r}",
                contexts,
            )
            rdiag[f"rep{r}"] = diag
        per_manuscript[manuscript] = core.aggregate_realizations(
            reps,
            f"Phase71A:{arm}:i{interval}:{manuscript}",
        )
        diagnostics[manuscript] = rdiag

    aggregate = core.aggregate_manuscripts(
        per_manuscript,
        f"Phase71A:{arm}:i{interval}:equal-manuscript",
    )
    evaluation = core.evaluate_aggregate(
        aggregate,
        contexts,
        phase63a,
        f"Phase71A:{arm}:i{interval}",
    )
    return {
        "arm": arm,
        "interval_words": interval,
        "per_manuscript_aggregate": per_manuscript,
        "aggregate": aggregate,
        "evaluation": evaluation,
        "construction_diagnostics": diagnostics,
    }


def boundary_decision(cont: dict, para: dict) -> dict:
    rc = float(cont["evaluation"]["candidate_ratio_of_means_to_voynich"]["S1"])
    rp = float(para["evaluation"]["candidate_ratio_of_means_to_voynich"]["S1"])
    positive_folds = sum(
        row["candidate_exposed"]["S1"] > TIE_EPS
        for row in para["evaluation"]["folds"]
    )
    broad = 0.5 <= rp <= 2.0
    paired_closer = abs(rp - 1.0) + TIE_EPS < abs(rc - 1.0)
    higher = rp > rc + TIE_EPS
    if broad and positive_folds >= 4 and paired_closer and higher:
        classification = "P71-AB1 BOUNDARY-SIGNAL MECHANISM DEMONSTRATED"
    elif paired_closer and higher:
        classification = "P71-AB1 BOUNDARY-SIGNAL PARTIAL"
    else:
        classification = "P71-AB1 BOUNDARY-SIGNAL NOT SUPPORTED"
    return {
        "R_CONT": rc,
        "R_PARA": rp,
        "PARA_positive_S1_folds": positive_folds,
        "PARA_broad_gate_0.5_to_2.0": broad,
        "PARA_closer_to_target_than_CONT": paired_closer,
        "PARA_strictly_higher_than_CONT": higher,
        "classification": classification,
    }


def run_science(voynich_path: Path, cremma_root: Path) -> dict:
    preflight = construction_preflight(voynich_path, cremma_root)
    contexts, phase62p, phase63a = load_science_context(voynich_path)
    projected, projection_diag = load_projected_sources(cremma_root)

    primary_cont = run_arm(projected, contexts, phase63a, PRIMARY_INTERVAL, "CONT")
    primary_para = run_arm(projected, contexts, phase63a, PRIMARY_INTERVAL, "PARA")
    primary_decision = boundary_decision(primary_cont, primary_para)

    sensitivity_cont = run_arm(projected, contexts, phase63a, SENSITIVITY_INTERVAL, "CONT")
    sensitivity_para = run_arm(projected, contexts, phase63a, SENSITIVITY_INTERVAL, "PARA")
    sensitivity_decision = boundary_decision(sensitivity_cont, sensitivity_para)

    return {
        "phase": "71A",
        "hypothesis": "P71-AB1 historically grounded Alberti message-initial boundary signal/reset as paragraph-entry mechanism control",
        "inputs": {
            "voynich_git_blob_sha1": b.git_blob_sha1(voynich_path.read_bytes()),
            "cremma_commit": b.verify_cremma_commit(cremma_root),
            "manuscripts_equal_weight": list(core.MANUSCRIPTS),
            "stationary_ring": STATIONARY,
            "movable_ring": MOVABLE,
            "index": INDEX,
            "plaintext_projection_letters": PLAIN_LOWER,
            "realizations_per_manuscript_per_arm": REPS,
            "primary_interval_words": PRIMARY_INTERVAL,
            "sensitivity_interval_words": SENSITIVITY_INTERVAL,
            "phase62p_raw_sha256": core.PHASE62P_SHA256,
            "phase63a_raw_sha256": core.PHASE63A_SHA256,
            "source_note": "Alberti first method: capital alignment signals and disk change after three or four words; no optional nulls/numeric supercipher used",
        },
        "preflight": preflight,
        "projection_diagnostics": projection_diag,
        "primary_4word": {
            "CONT": primary_cont,
            "PARA": primary_para,
            "decision": primary_decision,
        },
        "sensitivity_3word_nonrescuing": {
            "CONT": sensitivity_cont,
            "PARA": sensitivity_para,
            "decision": sensitivity_decision,
            "can_rescue_primary": False,
        },
        "frozen_primary_classification": primary_decision["classification"],
        "claim_limit": "source-grounded mechanism sufficiency control only; no claim that Voynich paragraphs are messages, no Alberti identification, plaintext language, key, semantics, or decipherment",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("voynich")
    ap.add_argument("cremma")
    ap.add_argument("--preflight-only", action="store_true")
    args = ap.parse_args()

    vp = Path(args.voynich).resolve()
    cr = Path(args.cremma).resolve()
    if args.preflight_only:
        out = construction_preflight(vp, cr)
        print(json.dumps(out, ensure_ascii=False, indent=2))
        print("NO PHASE71 SCIENTIFIC SCORE COMPUTED")
        return 0

    out = run_science(vp, cr)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
