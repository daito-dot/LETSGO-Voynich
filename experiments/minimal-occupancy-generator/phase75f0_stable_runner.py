#!/usr/bin/env python3
"""Normalization-stable runner for the frozen Phase F0 diagnostic.

This wrapper leaves the frozen Phase-E M5 refit untouched and substitutes a
mathematically equivalent explicitly renormalized component evaluator only for
new F0 G2/G3 objective and held-out calculations.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.special import logsumexp

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import phase75e_generator_support as real_egen  # noqa: E402
import phase75f0_training_latent_diagnostic as f0  # noqa: E402


def stable_component_logprob_and_mu(theta: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    theta = np.asarray(theta, dtype=np.float64)
    if theta.shape != (real_egen.N_COMPONENT_FREE,) or np.any(~np.isfinite(theta)):
        raise RuntimeError("invalid F0 component theta")
    logp = np.full(4095, -np.inf, dtype=np.float64)
    mu = np.zeros((len(real_egen.DESCRIPTORS), real_egen.N_COMPONENT_FREE), dtype=np.float64)
    for d in real_egen.DESCRIPTORS:
        did = real_egen.DESC_TO_ID[d]
        idx = np.asarray(real_egen.cgen.bgen.DESC_TO_INDEX[d], dtype=np.int64)
        F = real_egen.FREE_FEATURES[idx]
        logits = F @ theta
        lz = float(logsumexp(logits))
        lp = logits - lz
        p = np.exp(lp)
        s = float(p.sum())
        if not math.isfinite(s) or s <= 0.0:
            raise RuntimeError(f"non-finite F0 component normalization descriptor {d}")
        p = p / s
        lp = lp - math.log(s)
        if np.any(~np.isfinite(lp)) or np.any(~np.isfinite(p)):
            raise RuntimeError(f"non-finite F0 component probabilities descriptor {d}")
        logp[idx] = lp
        mu[did] = p @ F
    if np.any(~np.isfinite(logp)) or np.any(~np.isfinite(mu)):
        raise RuntimeError("F0 component state coverage incomplete")
    return logp, mu


class F0EGenProxy:
    def __getattr__(self, name: str):
        if name == "component_logprob_and_mu":
            return stable_component_logprob_and_mu
        return getattr(real_egen, name)


# Important: real_egen.fit_m5 remains a function whose own module globals point
# to the untouched Phase-E evaluator. Only lookups through f0.egen use the
# stabilization above.
f0.egen = F0EGenProxy()


if __name__ == "__main__":
    raise SystemExit(f0.main(sys.argv))
