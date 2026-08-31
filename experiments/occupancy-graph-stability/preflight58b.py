#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parents[1] / "issue26-music"))

import issue26e_core as e
import phase58b_graph_stability as g


def main(path: str) -> None:
    parser = e.SlotParser()
    validation = e.validate_parser(parser)
    dmin = g.build_dataset(path, parser, "min")
    smin = g.validate_support(dmin)
    dmax = g.build_dataset(path, parser, "max")
    smax = g.validate_support(dmax)
    if smin != smax:
        raise RuntimeError("min/max support mismatch")
    print(json.dumps({
        "scope": "preflight_only_no_pair_graph_scoring",
        "source_blob": dmin["source_blob"],
        "visible_tokens": dmin["visible"],
        "parsed_tokens": dmin["parsed"],
        "group_support": smin,
        "parser_validation": validation,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: preflight58b.py ZL3b-n.txt")
    main(sys.argv[1])
