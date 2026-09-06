#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit("usage: apply_amendment_a.py STAGE1.json FINAL.json")
    stage1_path = Path(sys.argv[1])
    final_path = Path(sys.argv[2])
    stage1 = json.loads(stage1_path.read_text(encoding="utf-8"))
    final = json.loads(final_path.read_text(encoding="utf-8"))

    x1 = final["models"].get("X1")
    if x1 is not None and x1["classification"] != "RECOVERS":
        if x1["issue81_gates"]["X2_responsibility_pass"]:
            x1["classification"] = "PARTIAL"

    if not final["X4_license"]["licensed"]:
        summary = final["heldout_cross_entropy"]["summary"]
        if "X4" in summary:
            summary["X4_non_authoritative_unlicensed"] = summary.pop("X4")
        for row in final["heldout_cross_entropy"]["folds"]:
            if "X4" in row:
                row["X4_non_authoritative_unlicensed"] = row.pop("X4")

    final["amendment_A"] = {
        "path": "experiments/cross-token-memory/AMENDMENT_A.md",
        "sha256": hashlib.sha256((Path(__file__).with_name("AMENDMENT_A.md")).read_bytes()).hexdigest(),
        "X1_S2_H62_responsibility_classification_applied": True,
        "unlicensed_X4_cross_entropy_not_authoritative": not final["X4_license"]["licensed"],
    }
    final_path.write_text(json.dumps(final, sort_keys=True, indent=1, default=float) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
