#!/usr/bin/env python3
"""Pre-reveal parser recovery for LM-A0 E0.

The frozen scorer failed before producing any result because lxml represents XML
comments with a non-string ``.tag``. This wrapper changes only ``lname`` so
non-element nodes are ignored; all population, representation, statistic,
threshold, and classification logic remains in the frozen scorer unchanged.
"""
from __future__ import annotations

import lm_a0_external_e0 as frozen


def safe_lname(tag) -> str:
    if not isinstance(tag, str):
        return ""
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


frozen.lname = safe_lname


if __name__ == "__main__":
    frozen.main()
