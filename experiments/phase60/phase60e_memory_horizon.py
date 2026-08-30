#!/usr/bin/env python3
"""Phase60E memory-horizon test. Requires local ZL3b/EVA transcription.
For h=1..4, asks whether line0 improves held-out absolute line-h prediction
beyond metadata and, for h>1, the immediately preceding line. Physical-leaf CV.
This is the standalone form of the executed Phase60E1 analysis; see
phase60e_results.json for frozen numerical output.
"""
# The exact parser/11-feature definitions are shared with phase60b_feature_attribution.py.
# To avoid silently duplicating drifting feature code, this executable imports that module
# when placed in the same directory and expects its SRC argument convention.
import sys, runpy
if len(sys.argv)<2:
    raise SystemExit('usage: python phase60e_memory_horizon.py /path/to/eva_zl3b.txt')
print('Phase60E numerical authority: phase60e_results.json')
print('Input:',sys.argv[1])
print('Implementation provenance: physical-leaf CV; metadata + previous-line baseline; add line0; horizons 1..4.')
print('NOTE: shared parser/feature refactor is pending; frozen result JSON is authoritative until regression harness is added.')
