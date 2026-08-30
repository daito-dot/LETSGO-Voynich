# Reproducibility note
# Exact executable used for Phase60B is maintained with the experiment result.
# Input: local ZL3b/EVA transcription documented in data/README.md.
# The analysis preserves full page-side IDs, P-coded prose, paragraph-start markers,
# and uses physical-leaf cross-fitting. It computes 11 line structural features,
# compares real line0->line2 transitions against internal pseudo i->i+2 transitions,
# and repeats across raw EVA, conservative composites, and Phase56 composites.
#
# See phase60b_results.json for frozen numerical output and PLAN_B.md for the
# pre-registered design. The local executable artifact is phase60b_feature_attribution.py.
#
# IMPORTANT: This repository does not redistribute the third-party transcription.
# Reproduction requires the transcription described in data/README.md.
