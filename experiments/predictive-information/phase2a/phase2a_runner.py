#!/usr/bin/env python3
"""Interface-only runner for Issue #94 Phase 2A.

The frozen scientific implementation defined `mix_probs` locally but its first
workflow attempt called the same helper through the imported Phase-1 module.
That failed before any outer result was produced. This shim binds that exact
local helper to the expected compatibility name and delegates unchanged.
"""
from __future__ import annotations

import phase2a_order_vs_prefix as M

M.P1.mix_probs = M.mix_probs

if __name__ == "__main__":
    raise SystemExit(M.main())
