# Issue #75 Phase F0 — execution attempt 1 numerical abort

Date: 2026-09-02  
Status: **FAILED BEFORE F0 AUTHORITY / NO SCIENTIFIC RESULT**

Workflow run:

- run `33543350071`
- execution head `6f83ff3074b0898392824a607d9ca55371163f91`
- job `99974768532`
- conclusion `failure`

The chronology, Phase-E license, frozen source blob, dependency installation, and Python compilation all passed.

The diagnostic process then aborted during G2 optimization before producing `/tmp/f0/phase75f0_training_latent_diagnostic.json` as an accepted authority, before validation, before artifact upload, and before repository evidence commit.

GitHub reports **zero workflow artifacts** for this run. `experiments/minimal-occupancy-generator/stage-f0/` was not created.

## Mechanical failure

The exception was:

`RuntimeError: component normalization failed descriptor (2, 2, 3)`

raised by the inherited Phase-E helper `component_logprob_and_mu` while L-BFGS-B was evaluating an intermediate G2 parameter vector.

That helper computes class-conditional probabilities by log-sum-exp, then additionally aborts if the floating-point sum of the exponentiated probabilities differs from 1 by more than `1e-12`.

The richer G2 search visited an intermediate parameter vector for which this numerical audit was exceeded. This is an optimizer-path numerical issue; it is not a held-out support result and does not change the mathematical model.

## Scientific firewall

Because the executable aborted before completing all five folds and before the validation/authority stages:

- no F0 classification is accepted;
- no G2/G3 support flag is accepted;
- no held-out fold gain is accepted or used for model choice;
- no topology reference was loaded;
- no target-based repair is licensed.

The only permitted repair is a mathematically equivalent floating-point normalization stabilization, frozen before the next complete execution. All candidate families, parameter counts, deterministic starts, physical folds, support threshold, and architecture-selection rules remain unchanged.
