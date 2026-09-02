#!/usr/bin/env python3
"""Run every frozen OGH-A (source, model, rep) scoring job in parallel and aggregate.

usage: python3 run_all.py ZL3b-n.txt IT2a-n.txt OUT_DIR [N_PROCS]

Jobs are independent processes so each candidate corpus owns its nulls and no
state leaks between candidates. Existing result files are not recomputed.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCES = ("ZL3b", "IT2a")
MODELS = ("G0", "G1", "G2", "G3", "G4", "G5", "G6")
REPS = (0, 1, 2)


def run(job, zl, it, out_dir):
    source, model, rep = job
    out = out_dir / f"{source}_{model}_rep{rep}.json"
    if out.exists():
        return job, "cached", 0.0
    t0 = time.time()
    cmd = [sys.executable, str(HERE / "ogh_a.py"), "--score", source, model, str(rep), str(zl)]
    if source == "IT2a":
        cmd.append(str(it))
    cmd.append(str(out))
    log = out_dir / "logs" / f"{source}_{model}_rep{rep}.log"
    log.parent.mkdir(exist_ok=True)
    with log.open("w") as fh:
        rc = subprocess.call(cmd, stdout=fh, stderr=subprocess.STDOUT, env={**os.environ, "OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1"})
    return job, ("ok" if rc == 0 else f"rc={rc}"), time.time() - t0


def main(argv):
    zl, it, out_dir = Path(argv[1]).resolve(), Path(argv[2]).resolve(), Path(argv[3]).resolve()
    n = int(argv[4]) if len(argv) > 4 else max(1, (os.cpu_count() or 2) - 0)
    out_dir.mkdir(parents=True, exist_ok=True)
    # rep0 (primary) first, then sensitivities
    jobs = [(s, m, r) for r in REPS for s in SOURCES for m in MODELS]
    with ThreadPoolExecutor(max_workers=n) as ex:
        for job, status, secs in ex.map(lambda j: run(j, zl, it, out_dir), jobs):
            print(f"{job} {status} {secs:.0f}s", flush=True)
    agg = out_dir / "ogh_a_aggregate.json"
    subprocess.check_call([sys.executable, str(HERE / "ogh_a.py"), "--aggregate", str(out_dir), str(agg)])
    print(json.dumps({"aggregate": str(agg)}))


if __name__ == "__main__":
    main(sys.argv)
