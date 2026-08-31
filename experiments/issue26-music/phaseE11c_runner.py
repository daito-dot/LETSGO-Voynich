#!/usr/bin/env python3
"""Serialization/parser-name wrapper only; scientific logic lives in phaseE11c_sta_family_substitution.py."""
import re
import phaseE11c_sta_family_substitution as e11c

# The first executable named the regex capture `locus` while parse_sta reads `loc`.
# Correct the capture name before execution; no source population or scoring rule changes.
e11c.LOCUS_RE = re.compile(r"^<(?P<folio>f[^.>,]+)\.(?P<loc>[^,>]+),(?P<kind>[^>]+)>\s+(?P<body>.*)$")

if __name__ == "__main__":
    raise SystemExit(e11c.main())
