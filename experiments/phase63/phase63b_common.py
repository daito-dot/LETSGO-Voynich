#!/usr/bin/env python3
"""Frozen Phase63B IVTFF/native-unit parser shared by preflight and science.

No scientific metric is computed in this module.
"""
from __future__ import annotations

import hashlib
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

PHASE62 = Path(__file__).resolve().parents[1] / "phase62"
if str(PHASE62) not in sys.path:
    sys.path.insert(0, str(PHASE62))
import phase62b_n0 as b  # noqa: E402


LOCUS_RE = re.compile(r"^<([^>.]+)\.(\d+),([^>;]+)(?:;[^>]+)?>\s*(.*)$")
LEAF_RE = re.compile(r"^f(\d+)", re.I)
HIGH_RE = re.compile(r"@\d{3};")
BRACKET_RE = re.compile(r"\[[^\]]*\]")
INLINE_RE = re.compile(r"<[^>]*>")
BOUND = "\ue000"
UNCERTAIN = "\ue001"

EXPECTED = {
    "ZL3b": {
        "sha256": "bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc",
        "git_blob_sha1": "2a4533ab9bdfa85db9bad602d590978953055df1",
        "alphabet": "Eva-",
    },
    "GC2a": {
        "sha256": "b09570cb6c993bc2d87134d115e60a978650a8a6495483ddbb1f6005a586096f",
        "git_blob_sha1": "8417a644fbd9c11cdaf85224f29cafee9ba1bdb0",
        "alphabet": "v101",
    },
    "IT2a": {
        "sha256": "7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5",
        "git_blob_sha1": "4d6d3f2537b1f507a257529b49c94af7d6e03446",
        "alphabet": "EvaT",
    },
}


@dataclass
class NativeParagraph:
    item_id: str
    page: str
    leaf: Optional[int]
    start_locus: str
    lines: List[b.Line]
    excluded_uncertain_tokens: int = 0

    def as_item(self) -> b.Item:
        return b.Item(self.item_id, self.page, self.lines, self.leaf)


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify_source(path: Path, label: str) -> Dict[str, str]:
    if label not in EXPECTED:
        raise RuntimeError(f"unknown source label: {label}")
    data = path.read_bytes()
    actual = {"sha256": sha256(data), "git_blob_sha1": git_blob_sha1(data)}
    expected = EXPECTED[label]
    for key in ("sha256", "git_blob_sha1"):
        if actual[key] != expected[key]:
            raise RuntimeError(f"{label} {key} mismatch: {actual[key]} != {expected[key]}")
    header = data.decode("utf-8-sig", errors="strict").splitlines()[0].strip()
    if not header.startswith(f"#=IVTFF {expected['alphabet']} "):
        raise RuntimeError(f"{label} unexpected IVTFF header: {header!r}")
    return {**actual, "header": header}


def physical_leaf(page: str) -> Optional[int]:
    m = LEAF_RE.match(page)
    return int(m.group(1)) if m else None


def generic_is_p(code: str) -> bool:
    return len(code) >= 2 and code[1] == "P"


def _replace_uncertain_brackets(text: str) -> str:
    # Require balanced, non-nested current IVTFF bracket syntax rather than
    # silently accepting malformed input.
    if text.count("[") != text.count("]"):
        raise RuntimeError(f"unbalanced uncertainty brackets in {text!r}")
    while "[" in text:
        new, n = BRACKET_RE.subn(UNCERTAIN, text)
        if n == 0:
            raise RuntimeError(f"cannot parse uncertainty bracket in {text!r}")
        text = new
    return text


def _native_units(token: str, alphabet: str) -> b.Token:
    out: List[str] = []
    i = 0
    while i < len(token):
        if token[i] == "@":
            m = HIGH_RE.match(token, i)
            if not m:
                raise RuntimeError(f"malformed high-ASCII glyph in token {token!r}")
            out.append(m.group(0))
            i = m.end()
            continue
        ch = token[i]
        if alphabet in ("Eva-", "EvaT"):
            if not ("A" <= ch <= "Z" or "a" <= ch <= "z"):
                raise RuntimeError(f"unexpected non-EVA glyph {ch!r} in token {token!r}")
            out.append(ch.lower())
        elif alphabet == "v101":
            if ch.isspace() or ch in ".,<>[]{}/@:;":
                raise RuntimeError(f"unexpected surviving IVTFF structural char {ch!r} in v101 token {token!r}")
            out.append(ch)
        else:
            raise RuntimeError(f"unsupported alphabet {alphabet}")
        i += 1
    return tuple(out)


def tokenize_body(body: str, alphabet: str, view: str) -> Tuple[bool, bool, b.Line, int]:
    if view not in ("W1", "W2"):
        raise RuntimeError(f"unknown word-space view: {view}")
    starts = body.count("<%>")
    ends = body.count("<$>")
    if starts > 1:
        raise RuntimeError(f"multiple paragraph starts on one line: {body!r}")
    if ends > 1:
        raise RuntimeError(f"multiple paragraph ends on one line: {body!r}")
    start = starts == 1
    end = ends == 1

    text = body.replace("<%>", "").replace("<$>", "")
    text = text.replace("<->", f" {BOUND} ").replace("<~>", f" {BOUND} ")
    text = INLINE_RE.sub("", text)
    text = _replace_uncertain_brackets(text)
    if text.count("{") != text.count("}"):
        raise RuntimeError(f"unbalanced ligature braces in {body!r}")
    text = text.replace("{", "").replace("}", "")

    if view == "W2":
        text = text.replace(",", "")
        raw_tokens = [x for x in re.split(rf"[\.\s{BOUND}]+", text) if x]
    else:
        raw_tokens = [x for x in re.split(rf"[\.,\s{BOUND}]+", text) if x]

    tokens: b.Line = []
    excluded = 0
    for raw in raw_tokens:
        if UNCERTAIN in raw or "?" in raw:
            excluded += 1
            continue
        units = _native_units(raw, alphabet)
        if units:
            tokens.append(units)
    return start, end, tokens, excluded


def parse_ivtff(path: Path, label: str, view: str) -> Tuple[List[NativeParagraph], dict]:
    source_id = verify_source(path, label)
    alphabet = EXPECTED[label]["alphabet"]
    out: List[NativeParagraph] = []
    current: Optional[NativeParagraph] = None
    current_page: Optional[str] = None
    pid_by_page: Dict[str, int] = {}
    starts_consumed = 0
    p_loci = 0
    ignored_p_lines_outside_paragraph = 0
    total_excluded = 0

    def close() -> None:
        nonlocal current
        if current is not None:
            out.append(current)
            current = None

    for rawline in path.read_text(encoding="utf-8-sig", errors="strict").splitlines():
        m = LOCUS_RE.match(rawline)
        if not m:
            continue
        page, num, code, body = m.groups()
        if not generic_is_p(code):
            continue
        p_loci += 1
        locus = f"{page}.{int(num)}"
        if current_page is not None and page != current_page:
            close()
        current_page = page

        start, end, tokens, excluded = tokenize_body(body, alphabet, view)
        total_excluded += excluded
        if start:
            close()
            pid_by_page[page] = pid_by_page.get(page, 0) + 1
            current = NativeParagraph(
                item_id=f"{page}:p{pid_by_page[page]}",
                page=page,
                leaf=physical_leaf(page),
                start_locus=locus,
                lines=[],
                excluded_uncertain_tokens=0,
            )
            starts_consumed += 1
        if current is not None:
            current.excluded_uncertain_tokens += excluded
            if tokens:
                current.lines.append(tokens)
            if end:
                close()
        elif tokens:
            ignored_p_lines_outside_paragraph += 1
    close()

    return out, {
        "source_identity": source_id,
        "view": view,
        "P_loci_seen": p_loci,
        "paragraph_starts_consumed": starts_consumed,
        "ignored_nonempty_P_lines_outside_paragraph": ignored_p_lines_outside_paragraph,
        "excluded_uncertain_or_unreadable_tokens": total_excluded,
    }


def items(paragraphs: Sequence[NativeParagraph]) -> List[b.Item]:
    return [p.as_item() for p in paragraphs]


def leaf_subset(paragraphs: Sequence[NativeParagraph], leaves: Iterable[int], include: bool) -> List[NativeParagraph]:
    s = set(leaves)
    return [p for p in paragraphs if p.leaf is not None and ((p.leaf in s) == include)]


def token_strings(paragraphs: Sequence[NativeParagraph]) -> List[str]:
    return ["".join(tok) for p in paragraphs for line in p.lines for tok in line]


def to_phase61_paragraphs(paragraphs: Sequence[NativeParagraph], p61_module) -> List[object]:
    # Only intended for Eva/EvaT. High-ASCII units need a fixed one-symbol
    # surrogate because the historical A1 implementation treats Python string
    # characters as glyph units.
    high_codes = sorted({u for p in paragraphs for line in p.lines for tok in line for u in tok if HIGH_RE.fullmatch(u)})
    if len(high_codes) > 0xF8FF - 0xE100 + 1:
        raise RuntimeError("too many high-ASCII units for frozen surrogate range")
    surrogate = {code: chr(0xE100 + i) for i, code in enumerate(high_codes)}

    def encode(tok: b.Token) -> str:
        chars: List[str] = []
        for u in tok:
            if HIGH_RE.fullmatch(u):
                chars.append(surrogate[u])
            elif len(u) == 1:
                chars.append(u)
            else:
                raise RuntimeError(f"cannot serialize multi-char native unit {u!r}")
        return "".join(chars)

    out = []
    pid_by_page: Dict[str, int] = {}
    for p in paragraphs:
        if p.leaf is None:
            continue
        pid_by_page[p.page] = pid_by_page.get(p.page, 0) + 1
        out.append(
            p61_module.Paragraph(
                page=p.page,
                pid=pid_by_page[p.page],
                leaf=p.leaf,
                section="?",
                lines=[[encode(tok) for tok in line] for line in p.lines],
            )
        )
    return out
