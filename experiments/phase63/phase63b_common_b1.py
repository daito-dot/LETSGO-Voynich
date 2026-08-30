#!/usr/bin/env python3
"""Phase63B parser B1: pre-science ZL Eva- apostrophe/zero compatibility.

Imports the frozen base parser and changes only the native-unit acceptance rule
recorded in PARSER_AMENDMENT_B1.md. parse_ivtff in the base module resolves the
patched global function at runtime.
"""
from __future__ import annotations

import re
from typing import List

import phase63b_common as base


HIGH_RE = base.HIGH_RE


def _native_units_b1(token: str, alphabet: str) -> base.b.Token:
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
        if alphabet == "Eva-":
            if "A" <= ch <= "Z" or "a" <= ch <= "z":
                out.append(ch.lower())
            elif ch in {"'", "0"}:
                out.append(ch)
            else:
                raise RuntimeError(f"unexpected Eva- glyph {ch!r} in token {token!r}")
        elif alphabet == "EvaT":
            if not ("A" <= ch <= "Z" or "a" <= ch <= "z"):
                raise RuntimeError(f"unexpected EvaT glyph {ch!r} in token {token!r}")
            out.append(ch.lower())
        elif alphabet == "v101":
            if ch.isspace() or ch in ".,<>[]{}/@:;":
                raise RuntimeError(f"unexpected surviving IVTFF structural char {ch!r} in v101 token {token!r}")
            out.append(ch)
        else:
            raise RuntimeError(f"unsupported alphabet {alphabet}")
        i += 1
    return tuple(out)


base._native_units = _native_units_b1

# Explicit re-exports used by Phase63B code.
b = base.b
EXPECTED = base.EXPECTED
NativeParagraph = base.NativeParagraph
verify_source = base.verify_source
parse_ivtff = base.parse_ivtff
items = base.items
leaf_subset = base.leaf_subset
token_strings = base.token_strings
to_phase61_paragraphs = base.to_phase61_paragraphs
