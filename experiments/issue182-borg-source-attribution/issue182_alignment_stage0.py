#!/usr/bin/env python3
"""Issue #182 Stage-0 score-free Borg plaintext/group alignment audit.

No edge likelihood or R5 gain is computed here. Scientific contract:
  research/ISSUE182_BORG_SOURCE_ATTRIBUTION_STAGE0_PLAN_20260907.md
"""
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

BRACKET_RE = re.compile(r"\[.*?\]")
Reward = tuple[int, int, int]  # matched chars, matched cipher groups, matched plaintext tokens
ZERO: Reward = (0, 0, 0)


def add_reward(a: Reward, b: Reward) -> Reward:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def normalize_plain_tokens(text: str) -> list[str]:
    text = unicodedata.normalize("NFC", text).casefold().replace("[", "").replace("]", "")
    chars = []
    for ch in text:
        cat = unicodedata.category(ch)
        if cat.startswith("L") or cat.startswith("M"):
            chars.append(ch)
        else:
            chars.append(" ")
    return [x for x in "".join(chars).split() if x]


@dataclass
class Group:
    flat_index: int
    line_index: int
    within_line_index: int
    diplomatic: str
    canonical_atoms: tuple[str, ...]
    keyed: bool
    decrypted: str | None


def parse_canonical(path: Path) -> list[list[tuple[str, ...]]]:
    lines = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        units = []
        for chunk in raw.split("|"):
            chunk = chunk.strip()
            if not chunk:
                raise RuntimeError(f"{path.name}: empty canonical group")
            units.append(tuple(chunk.split()))
        lines.append(units)
    return lines


def parse_diplomatic(
    path: Path,
    symbol_map: dict[str, str],
    cipher_key: dict[str, str],
) -> list[list[Group]]:
    lines: list[list[Group]] = []
    flat = 0
    for raw in path.read_text(encoding="utf-8").splitlines():
        s = raw.strip()
        if not s or s.startswith("<CLEARTEXT"):
            continue
        clean = BRACKET_RE.sub("", s)
        words = clean.split()
        if not words:
            continue
        line = []
        for wi, word in enumerate(words):
            missing_map = [ch for ch in word if ch not in symbol_map]
            if missing_map:
                raise RuntimeError(f"{path.name}: symbol-map miss in {word!r}: {missing_map!r}")
            atoms = tuple(symbol_map[ch] for ch in word)
            keyed = all(ch in cipher_key for ch in word)
            decrypted = "".join(cipher_key[ch] for ch in word).casefold() if keyed else None
            line.append(Group(flat, len(lines), wi, word, atoms, keyed, decrypted))
            flat += 1
        lines.append(line)
    return lines


def flatten(lines: list[list[Group]]) -> list[Group]:
    return [g for line in lines for g in line]


def verify_canonical(diplomatic: list[list[Group]], canonical: list[list[tuple[str, ...]]], page_id: str) -> None:
    d = [[g.canonical_atoms for g in line] for line in diplomatic]
    if d != canonical:
        # Find first structural mismatch for auditability, then stop.
        if len(d) != len(canonical):
            raise RuntimeError(f"{page_id}: diplomatic/canonical line-count mismatch {len(d)} != {len(canonical)}")
        for li, (dl, cl) in enumerate(zip(d, canonical)):
            if dl != cl:
                raise RuntimeError(f"{page_id}: diplomatic/canonical mismatch at canonical line {li}: {dl!r} != {cl!r}")
        raise RuntimeError(f"{page_id}: diplomatic/canonical mismatch")


def match_transitions(groups: list[Group], tokens: list[str], i: int, j: int) -> list[tuple[int, int, Reward]]:
    """Return exact-run matches from state (i,j) as (next_i,next_j,reward)."""
    if i >= len(groups) or j >= len(tokens) or not groups[i].keyed:
        return []
    target = tokens[j]
    acc = ""
    out = []
    for k in range(i, len(groups)):
        g = groups[k]
        if not g.keyed:
            break
        assert g.decrypted is not None
        acc += g.decrypted
        if len(acc) > len(target):
            break
        if acc == target:
            out.append((k + 1, j + 1, (len(target), k - i + 1, 1)))
            # All keyed groups are non-empty, so any further extension exceeds.
            break
        if not target.startswith(acc):
            break
    return out


def best_forward(groups: list[Group], tokens: list[str]) -> list[list[Reward | None]]:
    n, m = len(groups), len(tokens)
    dp: list[list[Reward | None]] = [[None] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = ZERO
    for i in range(n + 1):
        for j in range(m + 1):
            cur = dp[i][j]
            if cur is None:
                continue
            if i < n:
                if dp[i + 1][j] is None or cur > dp[i + 1][j]:
                    dp[i + 1][j] = cur
            if j < m:
                if dp[i][j + 1] is None or cur > dp[i][j + 1]:
                    dp[i][j + 1] = cur
            for ni, nj, rw in match_transitions(groups, tokens, i, j):
                val = add_reward(cur, rw)
                if dp[ni][nj] is None or val > dp[ni][nj]:
                    dp[ni][nj] = val
    return dp


def best_backward(groups: list[Group], tokens: list[str]) -> list[list[Reward | None]]:
    n, m = len(groups), len(tokens)
    dp: list[list[Reward | None]] = [[None] * (m + 1) for _ in range(n + 1)]
    dp[n][m] = ZERO
    for i in range(n, -1, -1):
        for j in range(m, -1, -1):
            if i == n and j == m:
                continue
            choices: list[Reward] = []
            if i < n and dp[i + 1][j] is not None:
                choices.append(dp[i + 1][j])
            if j < m and dp[i][j + 1] is not None:
                choices.append(dp[i][j + 1])
            for ni, nj, rw in match_transitions(groups, tokens, i, j):
                if dp[ni][nj] is not None:
                    choices.append(add_reward(rw, dp[ni][nj]))
            if choices:
                dp[i][j] = max(choices)
    return dp


def on_optimal_path(fwd: Reward | None, rw: Reward, bwd: Reward | None, global_best: Reward) -> bool:
    return fwd is not None and bwd is not None and add_reward(add_reward(fwd, rw), bwd) == global_best


def align_all_optimal(groups: list[Group], tokens: list[str]) -> dict:
    n, m = len(groups), len(tokens)
    fwd = best_forward(groups, tokens)
    bwd = best_backward(groups, tokens)
    global_best = fwd[n][m]
    if global_best is None or bwd[0][0] != global_best:
        raise RuntimeError("alignment DP inconsistency")

    possible_tokens: list[set[int]] = [set() for _ in groups]
    possibly_skipped = [False] * n
    optimal_match_transition_count = 0

    for i in range(n + 1):
        for j in range(m + 1):
            if fwd[i][j] is None:
                continue
            if i < n and on_optimal_path(fwd[i][j], ZERO, bwd[i + 1][j], global_best):
                possibly_skipped[i] = True
            # Plain skips do not affect per-group assignment directly.
            for ni, nj, rw in match_transitions(groups, tokens, i, j):
                if on_optimal_path(fwd[i][j], rw, bwd[ni][nj], global_best):
                    optimal_match_transition_count += 1
                    for gi in range(i, ni):
                        possible_tokens[gi].add(j)

    stable: list[int | None] = []
    for i in range(n):
        if len(possible_tokens[i]) == 1 and not possibly_skipped[i]:
            stable.append(next(iter(possible_tokens[i])))
        else:
            stable.append(None)

    return {
        "global_best": global_best,
        "stable_assignment": stable,
        "possibly_skipped": possibly_skipped,
        "possible_token_cardinality": [len(x) for x in possible_tokens],
        "optimal_match_transition_count": optimal_match_transition_count,
    }


def immediate_boundaries(lines: list[list[Group]]) -> list[tuple[int, int, str]]:
    out = []
    for line in lines:
        for a, b in zip(line, line[1:]):
            out.append((a.flat_index, b.flat_index, "SAME_PHYSICAL_LINE"))
    for a, b in zip(lines, lines[1:]):
        out.append((a[-1].flat_index, b[0].flat_index, "CROSS_PHYSICAL_LINE"))
    return out


def boundary_class(a: int | None, b: int | None) -> str:
    if a is None or b is None:
        return "UNALIGNED_OR_AMBIGUOUS"
    if a == b:
        return "WITHIN_WORD_SPLIT"
    if b == a + 1:
        return "LEXICAL_BOUNDARY"
    return "UNALIGNED_OR_AMBIGUOUS"


def audit_page(
    page_id: str,
    dip_path: Path,
    can_path: Path,
    plain_path: Path,
    symbol_map: dict[str, str],
    cipher_key: dict[str, str],
) -> dict:
    dlines = parse_diplomatic(dip_path, symbol_map, cipher_key)
    clines = parse_canonical(can_path)
    verify_canonical(dlines, clines, page_id)
    groups = flatten(dlines)
    tokens = normalize_plain_tokens(plain_path.read_text(encoding="utf-8"))
    ali = align_all_optimal(groups, tokens)
    stable = ali["stable_assignment"]

    bc = Counter()
    for i, j, phys in immediate_boundaries(dlines):
        bc[(phys, boundary_class(stable[i], stable[j]))] += 1

    stable_groups = sum(x is not None for x in stable)
    keyed_groups = sum(g.keyed for g in groups)
    stable_token_ids = {x for x in stable if x is not None}
    ambiguous_or_unassigned = len(groups) - stable_groups
    return {
        "page_id": page_id,
        "physical_line_count": len(dlines),
        "cipher_group_count": len(groups),
        "keyed_group_count": keyed_groups,
        "unkeyed_group_count": len(groups) - keyed_groups,
        "plaintext_token_count": len(tokens),
        "global_matched_characters": ali["global_best"][0],
        "global_matched_cipher_groups": ali["global_best"][1],
        "global_matched_plaintext_tokens": ali["global_best"][2],
        "plaintext_character_count": sum(len(x) for x in tokens),
        "stable_aligned_group_count": stable_groups,
        "ambiguous_or_unassigned_group_count": ambiguous_or_unassigned,
        "stable_plaintext_token_ids_touched": len(stable_token_ids),
        "groups_possibly_skipped_on_optimal_path": sum(ali["possibly_skipped"]),
        "groups_with_multiple_possible_token_indices": sum(x > 1 for x in ali["possible_token_cardinality"]),
        "optimal_match_transition_count": ali["optimal_match_transition_count"],
        "boundary_counts": {f"{p}|{b}": n for (p, b), n in sorted(bc.items())},
    }


def page_ids_from_canonical(trans_dir: Path) -> list[str]:
    ids = []
    for p in sorted(trans_dir.glob("borg_*.canonical.txt")):
        if parse_canonical(p):
            ids.append(p.name.removesuffix(".canonical.txt"))
    return ids


def audit(root: Path) -> dict:
    trans_dir = root / "benchmark/sources/borg/transcriptions"
    plain_dir = root / "benchmark/sources/borg/plaintext"
    meta_path = root / "benchmark/sources/borg/metadata/borg_symbol_map.json"
    meta = json.load(open(meta_path, encoding="utf-8"))
    symbol_map = meta["mapping"]
    cipher_key = meta["cipher_key"]
    if len(set(cipher_key.values())) != len(cipher_key):
        raise RuntimeError("published cipher_key is not one-to-one on values")

    ids = page_ids_from_canonical(trans_dir)
    if len(ids) != 397:
        raise RuntimeError(f"expected Issue #181 non-empty page population 397, got {len(ids)}")

    key_atoms = sorted(symbol_map[ch] for ch in cipher_key)
    pages = []
    totals = Counter()
    boundary_totals = Counter()
    missing = []
    for pid in ids:
        dip = trans_dir / f"{pid}.diplomatic.txt"
        can = trans_dir / f"{pid}.canonical.txt"
        plain = plain_dir / f"{pid}.txt"
        if not dip.exists() or not can.exists() or not plain.exists():
            missing.append(pid)
            continue
        r = audit_page(pid, dip, can, plain, symbol_map, cipher_key)
        pages.append(r)
        for k in (
            "physical_line_count", "cipher_group_count", "keyed_group_count", "unkeyed_group_count",
            "plaintext_token_count", "global_matched_characters", "global_matched_cipher_groups",
            "global_matched_plaintext_tokens", "plaintext_character_count", "stable_aligned_group_count",
            "ambiguous_or_unassigned_group_count", "groups_possibly_skipped_on_optimal_path",
            "groups_with_multiple_possible_token_indices",
        ):
            totals[k] += r[k]
        for k, v in r["boundary_counts"].items():
            boundary_totals[k] += v

    same_lex = boundary_totals["SAME_PHYSICAL_LINE|LEXICAL_BOUNDARY"]
    cross_lex = boundary_totals["CROSS_PHYSICAL_LINE|LEXICAL_BOUNDARY"]
    valid = not missing and len(pages) == 397 and same_lex >= 100 and cross_lex >= 100
    return {
        "experiment": "Issue #182 Borg source attribution Stage0 alignment audit",
        "edge_gain_computed": False,
        "page_population_expected": 397,
        "page_population_observed": len(pages),
        "missing_page_count": len(missing),
        "missing_pages": missing,
        "published_symbol_map_size": len(symbol_map),
        "published_cipher_key_size": len(cipher_key),
        "key_values_unique": len(set(cipher_key.values())) == len(cipher_key),
        "key_covered_canonical_atom_inventory": key_atoms,
        "key_covered_canonical_atom_count": len(key_atoms),
        "totals": dict(totals),
        "boundary_totals": dict(sorted(boundary_totals.items())),
        "support_gate": {
            "same_physical_line_lexical_boundary_min_100": same_lex >= 100,
            "cross_physical_line_lexical_boundary_min_100": cross_lex >= 100,
        },
        "classification": "ALIGNMENT_STAGE0_VALID" if valid else "ALIGNMENT_STAGE0_INVALID_OR_INSUFFICIENT",
        "pages": pages,
    }


def synthetic_preflight() -> None:
    # Exact run across a physical line: 'ef' + 'gh' must align to plaintext
    # token 'efgh'. A repeated plaintext token separately tests ambiguity.
    symbol_map = {ch: f"S{i+1:03d}" for i, ch in enumerate("abcdefghij")}
    key = {ch: ch.upper() for ch in "abcdefghij"}
    base = Path("/tmp/issue182_align_synth")
    base.mkdir(parents=True, exist_ok=True)

    dip = base / "x.diplomatic.txt"
    can = base / "x.canonical.txt"
    plain = base / "x.txt"
    dip.write_text("ab cd ef\ngh ij\n", encoding="utf-8")
    dlines = parse_diplomatic(dip, symbol_map, key)
    can.write_text(
        " | ".join(" ".join(g.canonical_atoms) for g in dlines[0]) + "\n" +
        " | ".join(" ".join(g.canonical_atoms) for g in dlines[1]) + "\n",
        encoding="utf-8",
    )
    plain.write_text("ab cd efgh ij", encoding="utf-8")
    r = audit_page("x", dip, can, plain, symbol_map, key)
    assert r["boundary_counts"]["CROSS_PHYSICAL_LINE|WITHIN_WORD_SPLIT"] == 1
    assert r["stable_aligned_group_count"] == 5

    # One group and two identical tokens: either token can be chosen in an
    # equally optimal path, so the group must not receive a stable assignment.
    groups = [Group(0, 0, 0, "ab", ("S001", "S002"), True, "ab")]
    amb = align_all_optimal(groups, ["ab", "ab"])
    assert amb["stable_assignment"] == [None]
    assert amb["possible_token_cardinality"][0] == 2
    print("SYNTHETIC_ALIGNMENT_PREFLIGHT_OK")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--synthetic-preflight", action="store_true")
    args = ap.parse_args()
    if args.synthetic_preflight:
        synthetic_preflight()
        return
    if args.root is None:
        ap.error("root is required unless --synthetic-preflight")
    result = audit(args.root)
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        args.out.write_text(text, encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()
