# Phase 60B — feature attribution and representation robustness

Status: frozen before execution.

## Target
Test P60-2 from `research/NARRATIVE_HYPOTHESIS_PHASE60.md`.

## Prediction
The entry-specific transition surviving Phase60A should be carried by a small, interpretable subset of audited structural features and should survive reasonable changes in token/unit representation.

## Primary feature family
Line-level structural fingerprint:
1. type-token ratio
2. mean token/unit length
3. token/unit length SD
4. unit inventory size
5. unit entropy
6. first-unit entropy
7. last-unit entropy
8. edit-distance-1 / near-family fraction
9. local previous-10 near-family continuity
10. k/t-family mass
11. k-share within k/t

## Tests
1. Cross-fitted physical-leaf folds: learn the real-entry transition direction on training leaves only; score real vs within-paragraph pseudo-boundaries on held-out leaves.
2. Coordinate attribution: estimate held-out real-minus-pseudo effect per feature, with page-cluster bootstrap.
3. Ablation: remove each feature and each feature group; quantify loss of cross-fitted discrimination.
4. Representation sensitivity: repeat with at least raw EVA tokens and a conservative composite/collapsed representation where locally available. No representation may be selected based on better results.
5. Section transfer: report H/B/P/S/T separately.

## Falsification
P60-2 is weakened/rejected if the effect is diffuse across many unstable coordinates, reverses under reasonable representation changes, or is dominated by an estimator/sample-size artifact.

## Promotion rule
A small stable carrier set may be promoted to Phase60C transferable entry-role tests. This remains structural evidence only.
