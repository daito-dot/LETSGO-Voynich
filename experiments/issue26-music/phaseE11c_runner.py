#!/usr/bin/env python3
"""Pre-reveal compatibility fixes only; scientific logic lives in phaseE11c_sta_family_substitution.py."""
import re
import phaseE11c_sta_family_substitution as e11c

# The first executable named the regex capture `locus` while parse_sta reads `loc`.
e11c.LOCUS_RE = re.compile(r"^<(?P<folio>f[^.>,]+)\.(?P<loc>[^,>]+),(?P<kind>[^>]+)>\s+(?P<body>.*)$")

# IVTFF alternatives may have either side empty. Frozen rule: always first reading.
e11c.ALT_RE = re.compile(r"\[([^\]:]*):[^\]]*\]")

# PLAN_E11 / PLAN_E11C freeze j->i and v->u, hence a 24-letter Latin alphabet.
# The shared first executable accidentally retained `v`, creating 25 letters. Correct
# the constants before any scientific score is computed. Numba kernels compile lazily
# after this patch and therefore receive the frozen A=24 value.
correct_alphabet = tuple("abcdefghiklmnopqrstuwxyz")
assert len(correct_alphabet) == 24 and "j" not in correct_alphabet and "v" not in correct_alphabet
base = e11c.base
base.ALPHABET = correct_alphabet
base.A = len(correct_alphabet)
base.AI = {c: i for i, c in enumerate(correct_alphabet)}

if __name__ == "__main__":
    raise SystemExit(e11c.main())
