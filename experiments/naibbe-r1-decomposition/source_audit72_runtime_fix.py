#!/usr/bin/env python3
"""Mechanical Stage-A launcher correcting one Phase64 diagnostics key name.

This file exists because the first target-blind source-audit run used the
nonexistent diagnostics key ``primary_tokens`` while the frozen Phase64B
wrapper emits ``primary_cipher_tokens``. No intervention definition, support
gate, source identity, seed, surface construction, or R1 quantity is changed.
"""
from __future__ import annotations

import sys
from pathlib import Path

import source_audit72 as s


def fixed_generate_with_map(module, sources, glyph_map, parser, label):
    by_m = {}
    diags = {}
    for mi, manuscript in enumerate(s.MANUSCRIPTS):
        primary, _raw, diag = s.n64.encrypt_manuscript(
            module, sources[manuscript], manuscript, glyph_map, s.PRIMARY_SEEDS[mi]
        )
        by_m[manuscript] = primary
        diags[manuscript] = diag
    pp = s.pooled(by_m)
    return {
        "label": label,
        "surface_sha256": s.surface_sha(pp),
        "support": s.parser_support(pp, parser),
        "generation_completed": True,
        "ambiguity_retries_by_manuscript": {
            m: int(diags[m]["ambiguity_retries"]) for m in s.MANUSCRIPTS
        },
        "primary_tokens_by_manuscript": {
            m: int(diags[m]["primary_cipher_tokens"]) for m in s.MANUSCRIPTS
        },
        "map_sha256": s.map_sha(glyph_map),
    }, by_m


s.generate_with_map = fixed_generate_with_map

if len(sys.argv) != 3:
    raise SystemExit(f"usage: {sys.argv[0]} CREMMA_ROOT NAIBBE_ROOT")

s.main(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve())
