"""Phase 51 frozen DSL falsification.

Historical source file: phase51_frozen_dsl_falsification.py.
The frozen specification and authoritative headline results are recorded in
README.md and phase51_frozen_dsl_falsification_results.json.

This public entrypoint intentionally records the frozen parameters independently
of later model development. The full historical implementation is being
normalized so input paths are explicit rather than depending on the original
workspace filename.
"""

FROZEN = {
    "nroots": 64,
    "block": 4,
    "state_use": 0.30,
    "prefix_p": 0.22,
    "suffix_p": 0.32,
    "variants_per_root": 2,
    "alphabet": "abcdefghiklmnoprstuy",
}

if __name__ == "__main__":
    print("Frozen Phase 51 parameters:", FROZEN)
    print("See README.md and result JSON for the completed 20-corpus falsification run.")
