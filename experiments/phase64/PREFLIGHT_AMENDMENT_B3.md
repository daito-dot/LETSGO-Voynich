# Phase 64B preflight amendment B3 — published Naibbe alphabet compatibility

Status: **recorded before any Phase64B scientific score or classification is revealed**.

## Trigger

The first authorized science attempt, Actions run `33337753319` / job `99327642094` at frozen head `c7e7732b3ab5f8d28864ef9fcd4c71d0f0d69255`, passed all exact source identity checks and then stopped during plaintext preparation with:

`RuntimeError: Naibbe clean_line emitted unsupported normalized letters: ['ꝯ']`

The failure occurred inside `encrypt_manuscript()` before `output_metrics()` was called for the candidate. The verdict-summary and artifact-upload steps were skipped. Therefore no Phase64B S1/S2/S3, H62, permutation-control, codebook-specificity or classification value was revealed by this run.

## External-code behavior

Pinned `naibbe_v2.py` defines `clean_line()` using Unicode `str.isalpha()` after its explicit normalization replacements. Consequently a medieval Unicode alphabetic character such as `ꝯ` survives `clean_line()` even though the published Naibbe codebook contains only the 23 effective Latin letters remaining after `j/k/w` normalization.

This is an interface-domain mismatch between the frozen CREMMA source-native transcription and the exact published Naibbe codebook. It is not a model-score failure.

## Frozen compatibility rule

After calling the published `clean_line()` unchanged, the Phase64B adapter will apply exactly one deterministic alphabet-domain projection:

`cleaned = ''.join(ch for ch in published_cleaned if ch in EFFECTIVE_LETTERS)`

where `EFFECTIVE_LETTERS` is the already frozen 23-letter Naibbe reachable alphabet (`a-z` excluding `j`, `k`, `w`).

Rules:

1. unsupported surviving Unicode alphabetic characters are **dropped**;
2. no new transliteration, abbreviation expansion or historical reading is invented;
3. the published replacements and `j/k/w` normalization remain authoritative because they occur inside `clean_line()` first;
4. supported characters are left unchanged and in original order;
5. the projection is independent of Voynich folds, targets and scores;
6. dropped-character counts are recorded as descriptive retention diagnostics only.

This implements the already frozen `PLAN_B.md` intent that unsupported medieval graphemes are dropped rather than expanded.

## Scientific-firewall chronology

- `33337753319` is retained as a failed execution attempt, not a scientific result;
- no Phase64B score/classification was emitted or uploaded from it;
- PR-synchronize science triggering is temporarily disabled while this compatibility rule is frozen and non-scientifically preflighted;
- a B4 preflight may use the exact external Naibbe source and synthetic/toy strings, but must not check out/read ZL3b or CREMMA scientific sources;
- only after B4 passes may the pull-request synchronize science trigger be restored and a new first successful reveal be authorized.

No Naibbe parameter, codebook mapping, stochastic seed, scoring metric, aggregation rule, threshold, control or frozen classification is changed by B3.
