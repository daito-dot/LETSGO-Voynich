#!/usr/bin/env python3
"""Serialization-only wrapper for E8-A2.

The first E8-A2 Actions attempt completed the exhaustive calculation but failed
before emitting JSON because numpy scalar booleans are not handled by the
stdlib JSON encoder. This wrapper changes only JSON serialization: numpy scalar
objects are converted with .item(). It does not alter population, scoring,
selection, thresholds, or classification logic in phaseE8A2_vowel_fixed.py.
"""

import json
import sys

import numpy as np

import phaseE8A2_vowel_fixed as science


_original_dump = json.dump


def _numpy_default(obj):
    if isinstance(obj, np.generic):
        return obj.item()
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


def _dump_with_numpy(obj, fp, *args, **kwargs):
    kwargs.setdefault("default", _numpy_default)
    return _original_dump(obj, fp, *args, **kwargs)


json.dump = _dump_with_numpy

if __name__ == "__main__":
    raise SystemExit(science.main())
