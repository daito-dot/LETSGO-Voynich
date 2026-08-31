#!/usr/bin/env python3
"""Parsing-only wrapper; scientific logic lives in phaseE11c_sta_family_substitution.py."""
import re
import phaseE11c_sta_family_substitution as e11c

# The first executable named the regex capture `locus` while parse_sta reads `loc`.
# Correct the capture name before execution; no source population or scoring rule changes.
e11c.LOCUS_RE = re.compile(r"^<(?P<folio>f[^.>,]+)\.(?P<loc>[^,>]+),(?P<kind>[^>]+)>\s+(?P<body>.*)$")

# IVTFF may encode an empty second alternative, e.g. [C2:]. The frozen E11C
# rule is to take the first reading, so allow zero characters after the colon.
e11c.ALT_RE = re.compile(r"\[([^\]:]+):[^\]]*\]")

if __name__ == "__main__":
    raise SystemExit(e11c.main())
