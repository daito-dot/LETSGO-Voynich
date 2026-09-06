#!/usr/bin/env python3
"""Interface-only runner for prereveal-amended Issue #94 Phase 2A.

The frozen base scorer defines `mix_probs` locally but references that identical
helper through its imported Phase-1 namespace. The first workflow attempt
failed on that missing attribute before producing an outer result. Bind the
identical helper to the compatibility name, then delegate to the amended model.
"""
from __future__ import annotations

import phase2a_amended as A

A.P1.mix_probs = A.B.mix_probs

if __name__ == "__main__":
    raise SystemExit(A.main())
