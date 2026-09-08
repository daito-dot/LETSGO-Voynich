#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

SCHEMA = "issue194-ramanacoil-gate0-v1"
EXPLICIT_DELIMS = {
    "|", "||", "/", "//", "<SPACE>", "[SPACE]", "<WORD>", "[WORD]",
    "WORDSEP", "WordSeparator", "SPACE",
}
SPACE_PLAINTEXTS = {" ", "<SPACE>", "[SPACE]", "<WORD>", "[WORD]", "SPACE", "WordSeparator", "WORDSEP"}
KEY_RE = re.compile(r"^\[([^\]]*)\];\[([^\]]*)\]\s*$")
ALPHA_TOKEN_RE = re.compile(r"[^\W\d_]+", re.UNICODE)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def newline_audit(data: bytes) -> dict:
    crlf = data.count(b"\r\n")
    cr_total = data.count(b"\r")
    lf_total = data.count(b"\n")
    bare_cr = cr_total - crlf
    bare_lf = lf_total - crlf
    if crlf and not bare_cr and not bare_lf:
        convention = "CRLF"
    elif bare_lf and not crlf and not bare_cr:
        convention = "LF"
    elif bare_cr and not crlf and not bare_lf:
        convention = "CR"
    elif not (crlf or bare_cr or bare_lf):
        convention = "NONE"
    else:
        convention = "MIXED"
    return {"crlf": crlf, "bare_cr": bare_cr, "bare_lf": bare_lf, "convention": convention}


def decode_utf8(data: bytes) -> str:
    return data.decode("utf-8-sig")


def normalized_lines(text: str) -> list[str]:
    return text.replace("\r\n", "\n").replace("\r", "\n").split("\n")


def escaped_sample(lines: list[str]) -> dict:
    nonempty = [x for x in lines if x.strip()]
    def esc(s: str) -> str:
        return s.encode("unicode_escape").decode("ascii")[:240]
    return {"first": [esc(x) for x in nonempty[:3]], "last": [esc(x) for x in nonempty[-3:]]}


def load_pair(path_a: Path, path_b: Path) -> dict:
    out = {"path_a": str(path_a), "path_b": str(path_b), "exists_a": path_a.exists(), "exists_b": path_b.exists()}
    if not path_a.exists() or not path_b.exists():
        out.update({"stable": False, "reason": "missing_download"})
        return out
    a = path_a.read_bytes()
    b = path_b.read_bytes()
    out.update({
        "bytes": len(a),
        "bytes_repeat": len(b),
        "sha256": sha256_bytes(a),
        "sha256_repeat": sha256_bytes(b),
        "stable": bool(a == b and len(a) > 0),
        "newline": newline_audit(a),
        "line_count_bytes": a.count(b"\n") + (1 if a else 0),
    })
    if not a:
        out["reason"] = "empty_download"
    elif a != b:
        out["reason"] = "repeat_mismatch"
    else:
        out["reason"] = "byte_identical"
    try:
        text = decode_utf8(a)
        out["utf8"] = True
        out["sample"] = escaped_sample(normalized_lines(text))
    except UnicodeDecodeError as exc:
        out["utf8"] = False
        out["utf8_error"] = str(exc)
    return out


def parse_key(text: str) -> dict:
    mapping: dict[str, str] = {}
    conflicts: dict[str, list[str]] = {}
    metadata_cipher: set[str] = set()
    metadata_plain: set[str] = set()
    parsed_lines = 0
    unparsed_nonempty = 0
    for raw in normalized_lines(text):
        if not raw.strip():
            continue
        m = KEY_RE.match(raw.strip())
        if not m:
            unparsed_nonempty += 1
            continue
        parsed_lines += 1
        plain_raw = m.group(1)
        plain = " " if plain_raw and plain_raw.strip() == "" else plain_raw.strip()
        rhs = m.group(2).strip()
        alts = [x.strip() for x in rhs.split("|") if x.strip()]
        for cipher in alts:
            if cipher in mapping and mapping[cipher] != plain:
                vals = conflicts.setdefault(cipher, sorted({mapping[cipher], plain}))
                if plain not in vals:
                    vals.append(plain)
                    vals.sort()
            else:
                mapping[cipher] = plain
            if plain.startswith("DC") and cipher.isdigit():
                metadata_cipher.add(cipher)
                metadata_plain.add(plain)
    boundary_key_tokens = {
        c for c, p in mapping.items()
        if p in SPACE_PLAINTEXTS or "wordsep" in p.casefold() or "word_separator" in p.casefold() or "wordboundary" in p.casefold()
    }
    examples = [{"cipher": c, "plaintext": mapping[c]} for c in sorted(mapping)[:20]]
    return {
        "mapping": mapping,
        "conflicts": conflicts,
        "metadata_cipher": metadata_cipher,
        "metadata_plain": metadata_plain,
        "boundary_key_tokens": boundary_key_tokens,
        "parsed_key_lines": parsed_lines,
        "unparsed_nonempty_key_lines": unparsed_nonempty,
        "distinct_cipher_tokens": len(mapping),
        "examples": examples,
    }


def self_identifying_boundary(tok: str) -> bool:
    s = tok.casefold()
    return "wordsep" in s or "word_separator" in s or "wordboundary" in s


def audit_transcription(text: str, key: dict) -> dict:
    mapping = key["mapping"]
    metadata = key["metadata_cipher"]
    key_boundary = key["boundary_key_tokens"]
    token_counts = Counter()
    candidate_occ = 0
    covered_occ = 0
    atom_lines = []
    boundary_counts = Counter()
    boundary_lines = set()
    for line_idx, raw in enumerate(normalized_lines(text)):
        if not raw.strip():
            continue
        tokens = re.findall(r"\S+", raw)
        if not tokens:
            continue
        if "\t" in raw and re.search(r"\S\t+\S", raw):
            n = len(re.findall(r"(?<=\S)\t+(?=\S)", raw))
            if n:
                boundary_counts["tab"] += n
                boundary_lines.add(line_idx)
        n2 = len(re.findall(r"(?<=\S) {2,}(?=\S)", raw))
        if n2:
            boundary_counts["double_space"] += n2
            boundary_lines.add(line_idx)
        atoms_this_line = []
        for tok in tokens:
            if tok in metadata:
                continue
            if tok in EXPLICIT_DELIMS:
                boundary_counts["literal_delimiter_token"] += 1
                boundary_lines.add(line_idx)
                continue
            if self_identifying_boundary(tok):
                boundary_counts["self_identifying_boundary_token"] += 1
                boundary_lines.add(line_idx)
                continue
            if tok in key_boundary:
                boundary_counts["key_mapped_boundary_token"] += 1
                boundary_lines.add(line_idx)
                continue
            candidate_occ += 1
            token_counts[tok] += 1
            if tok in mapping:
                covered_occ += 1
            atoms_this_line.append(tok)
        if atoms_this_line:
            atom_lines.append((line_idx, raw, atoms_this_line))
    coverage = covered_occ / candidate_occ if candidate_occ else 0.0
    lines_ge5 = sum(len(x[2]) >= 5 for x in atom_lines)
    physical_support_ratio = lines_ge5 / len(atom_lines) if atom_lines else 0.0
    return {
        "candidate_atom_occurrences": candidate_occ,
        "distinct_candidate_atoms": len(token_counts),
        "key_covered_occurrences": covered_occ,
        "key_coverage_fraction": coverage,
        "atom_bearing_lines": len(atom_lines),
        "atom_lines_ge5": lines_ge5,
        "atom_lines_ge5_fraction": physical_support_ratio,
        "boundary_channel_counts": dict(sorted(boundary_counts.items())),
        "boundary_event_total": sum(boundary_counts.values()),
        "boundary_bearing_lines": len(boundary_lines),
        "top_tokens": [{"token": t, "count": n} for t, n in token_counts.most_common(30)],
        "_atom_lines": atom_lines,
    }


def is_decryption_marker(line: str, metadata_plain: set[str]) -> bool:
    s = line.strip()
    if not s:
        return True
    if s in metadata_plain or s.strip("[]") in metadata_plain:
        return True
    if re.fullmatch(r"\[?DC\d+[^\s]*\]?", s, flags=re.IGNORECASE):
        return True
    return False


def audit_decryption(text: str, metadata_plain: set[str]) -> dict:
    content = []
    lexical_lines = 0
    lexical_tokens_total = 0
    for idx, raw in enumerate(normalized_lines(text)):
        if is_decryption_marker(raw, metadata_plain) or not raw.strip():
            continue
        content.append((idx, raw))
        fields = [f for f in re.split(r"[ \t]+", raw.strip()) if f]
        alpha_fields = [f for f in fields if ALPHA_TOKEN_RE.search(f)]
        if len(alpha_fields) >= 2:
            lexical_lines += 1
            lexical_tokens_total += len(alpha_fields)
    return {
        "content_lines": len(content),
        "lexical_multitoken_lines": lexical_lines,
        "whitespace_separated_alpha_tokens_on_multitoken_lines": lexical_tokens_total,
        "_content_lines": content,
    }


def normalize_compare(s: str) -> str:
    s = unicodedata.normalize("NFC", s)
    s = s.strip(" \t")
    return re.sub(r"[ \t]+", " ", s)


def audit_alignment(trans: dict, dec: dict, key: dict) -> dict:
    mapping = key["mapping"]
    boundary_key = key["boundary_key_tokens"]
    tlines = []
    total_covered_atoms = 0
    for _idx, _raw, toks in trans["_atom_lines"]:
        parts = []
        covered_here = 0
        for tok in toks:
            if tok in mapping:
                parts.append(mapping[tok])
                if tok not in boundary_key:
                    covered_here += 1
            else:
                parts.append(f"<UNK:{tok}>")
        tlines.append((normalize_compare("".join(parts)), covered_here))
        total_covered_atoms += covered_here
    dlines = [normalize_compare(raw) for _idx, raw in dec["_content_lines"]]
    strict_match_atoms = 0
    strict_match_lines = 0
    strict_ci_match_atoms = 0
    strict_ci_match_lines = 0
    paired = min(len(tlines), len(dlines))
    for i in range(paired):
        tv, atoms = tlines[i]
        dv = dlines[i]
        if tv == dv:
            strict_match_lines += 1
            strict_match_atoms += atoms
        if tv.casefold() == dv.casefold():
            strict_ci_match_lines += 1
            strict_ci_match_atoms += atoms
    strict_cov = strict_match_atoms / total_covered_atoms if total_covered_atoms else 0.0
    strict_ci_cov = strict_ci_match_atoms / total_covered_atoms if total_covered_atoms else 0.0
    tstream = "\n".join(x[0] for x in tlines)
    dstream = "\n".join(dlines)
    stream_exact = bool(tstream == dstream and tstream)
    stream_ci_exact = bool(tstream.casefold() == dstream.casefold() and tstream)
    coverage = max(strict_cov, 1.0 if stream_exact else 0.0)
    return {
        "transcription_content_lines": len(tlines),
        "decryption_content_lines": len(dlines),
        "paired_lines": paired,
        "total_key_covered_atoms": total_covered_atoms,
        "strict_exact_matching_lines": strict_match_lines,
        "strict_exact_atom_coverage": strict_cov,
        "strict_casefold_matching_lines": strict_ci_match_lines,
        "strict_casefold_atom_coverage_diagnostic": strict_ci_cov,
        "sequential_stream_exact": stream_exact,
        "sequential_stream_casefold_exact_diagnostic": stream_ci_exact,
        "frozen_alignment_coverage": coverage,
        "key_conflict_count": len(key["conflicts"]),
    }


def run(paths: dict[str, tuple[Path, Path]]) -> dict:
    source = {name: load_pair(a, b) for name, (a, b) in paths.items()}
    stable = all(x.get("stable") for x in source.values())
    utf8 = all(x.get("utf8") for x in source.values()) if stable else False
    result = {
        "schema": SCHEMA,
        "issue": 194,
        "parent_issue": 172,
        "scientific_score_computed": False,
        "r5_score_computed": False,
        "voynich_data_accessed": False,
        "authority": source,
        "layers": {},
        "classification": None,
        "stage1_licensed": False,
    }
    if not stable:
        result["classification"] = "AUTHORITY_UNAVAILABLE_OR_UNSTABLE"
        return result
    if not utf8:
        result["classification"] = "NON_COMPOSABLE_OTHER"
        result["reason"] = "strict_utf8_decode_failure"
        return result
    texts = {name: decode_utf8(paths[name][0].read_bytes()) for name in paths}
    key = parse_key(texts["key"])
    trans = audit_transcription(texts["transcription"], key)
    dec = audit_decryption(texts["decryption"], key["metadata_plain"])
    align = audit_alignment(trans, dec, key)
    ciphertext_symbols = (
        trans["candidate_atom_occurrences"] >= 1000
        and trans["distinct_candidate_atoms"] >= 20
        and trans["key_coverage_fraction"] >= 0.95
    )
    physical_lines = (
        trans["atom_bearing_lines"] >= 100
        and trans["atom_lines_ge5_fraction"] >= 0.80
        and dec["content_lines"] >= 100
    )
    cipher_units = trans["boundary_event_total"] >= 100 and trans["boundary_bearing_lines"] >= 20
    plaintext_lexical = (
        dec["content_lines"] >= 100
        and dec["lexical_multitoken_lines"] >= 100
        and dec["whitespace_separated_alpha_tokens_on_multitoken_lines"] >= 500
    )
    alignment = align["frozen_alignment_coverage"] >= 0.95 and align["key_conflict_count"] == 0
    layers = {
        "CIPHERTEXT_SYMBOLS": ciphertext_symbols,
        "PHYSICAL_LINES": physical_lines,
        "CIPHER_UNIT_BOUNDARIES": cipher_units,
        "PLAINTEXT_LEXICAL_BOUNDARIES": plaintext_lexical,
        "CIPHER_PLAINTEXT_ALIGNMENT": alignment,
    }
    result["layers"] = layers
    result["key_audit"] = {
        "parsed_key_lines": key["parsed_key_lines"],
        "unparsed_nonempty_key_lines": key["unparsed_nonempty_key_lines"],
        "distinct_cipher_tokens": key["distinct_cipher_tokens"],
        "conflict_count": len(key["conflicts"]),
        "conflicts": key["conflicts"],
        "metadata_cipher_token_count": len(key["metadata_cipher"]),
        "metadata_plaintext_count": len(key["metadata_plain"]),
        "key_boundary_token_count": len(key["boundary_key_tokens"]),
        "key_boundary_tokens": sorted(key["boundary_key_tokens"]),
        "examples": key["examples"],
    }
    result["transcription_audit"] = {k: v for k, v in trans.items() if not k.startswith("_")}
    result["decryption_audit"] = {k: v for k, v in dec.items() if not k.startswith("_")}
    result["alignment_audit"] = align
    if all(layers.values()):
        classification = "COMPOSABLE_FOR_CLEAN_R5_ATTRIBUTION"
    elif ciphertext_symbols and physical_lines and plaintext_lexical and alignment and not cipher_units:
        classification = "PHYSICAL_LINES_AND_ALIGNMENT_PRESENT_BUT_NO_CIPHER_UNIT_BOUNDARIES"
    elif cipher_units and (not plaintext_lexical or not alignment):
        classification = "PLAINTEXT_OR_ALIGNMENT_NOT_PRESERVED"
    else:
        classification = "NON_COMPOSABLE_OTHER"
    result["classification"] = classification
    result["stage1_licensed"] = classification == "COMPOSABLE_FOR_CLEAN_R5_ATTRIBUTION"
    return result


def self_test() -> None:
    key_text = "[A];[Earth]\n[B];[Moon]\n[ ];[SEP]\n[DC1_RAM1];[1001]\n"
    k = parse_key(key_text)
    assert k["mapping"]["Earth"] == "A"
    assert "SEP" in k["boundary_key_tokens"]
    assert "1001" in k["metadata_cipher"]
    tr = audit_transcription("1001\nEarth Moon  Earth\nEarth\tMoon SEP Earth\n", k)
    assert tr["boundary_channel_counts"]["double_space"] == 1
    assert tr["boundary_channel_counts"]["tab"] == 1
    assert tr["boundary_channel_counts"]["key_mapped_boundary_token"] == 1
    dec = audit_decryption("DC1_RAM1\nAB A\nAB\n", k["metadata_plain"])
    assert dec["content_lines"] == 2
    assert dec["lexical_multitoken_lines"] == 1
    assert normalize_compare("  A\t B ") == "A B"
    print(json.dumps({"schema": SCHEMA, "self_test": "PASS"}, sort_keys=True))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--transcription-a")
    ap.add_argument("--transcription-b")
    ap.add_argument("--key-a")
    ap.add_argument("--key-b")
    ap.add_argument("--decryption-a")
    ap.add_argument("--decryption-b")
    ap.add_argument("--output")
    args = ap.parse_args()
    if args.self_test:
        self_test()
        return
    if not args.run:
        ap.error("choose --self-test or --run")
    required = [args.transcription_a, args.transcription_b, args.key_a, args.key_b, args.decryption_a, args.decryption_b, args.output]
    if any(x is None for x in required):
        ap.error("--run requires all input/output arguments")
    paths = {
        "transcription": (Path(args.transcription_a), Path(args.transcription_b)),
        "key": (Path(args.key_a), Path(args.key_b)),
        "decryption": (Path(args.decryption_a), Path(args.decryption_b)),
    }
    out = run(paths)
    Path(args.output).write_text(json.dumps(out, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "classification": out["classification"],
        "stage1_licensed": out["stage1_licensed"],
        "layers": out["layers"],
        "scientific_score_computed": out["scientific_score_computed"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
