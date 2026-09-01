#!/usr/bin/env python3
"""Transport-only wrapper for Issue #72 V2 B1.

The scientific scorer remains `b1_r1_calibration72_v2.py` unchanged. This
wrapper replaces only the failed large-JSON repository transport authority with
the compact, artifact-derived Stage-B0 execution manifest documented in
`STAGE_B0_ARCHIVE_TRANSPORT_INCIDENT.md`.
"""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import b1_r1_calibration72_v2 as scorer  # noqa: E402

scorer.B0_PATH = HERE / "stage_b0_authority.json"
scorer.B0_SHA256 = "d38ab785b421bcd7eea0e48fb03d5c6f55d8f733dc662fc4793a1f7c0d161d28"

if __name__ == "__main__":
    raise SystemExit(scorer.main(sys.argv))
