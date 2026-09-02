# OGH-C stage C1 provenance

- PLAN_C first-add: `f81b67b5ae942b6ee3fcda30cbb62a78bba33439`
- executable first-add: `636bac227b2b8b6cd39c1d5c7ddd5cf32d4d9375`
- stage C0 commit / pre-reveal head: `3e19c7ee76d1377b4a48cc9ab276e891b1fff61b` (selected content grammar V2; no cross-token statistic computed at C0)
- execution: Claude Code remote container, Linux 6.18.44-fc-v22 x86_64; Python 3.11.15; numpy 2.4.6; finished 2026-09-02 01:48:26 UTC
- population: V0, V2, V+ × realizations 0–2 = 9 synthetic manuscripts (735 items each, all five held-out folds), seeds `OGH-C:{model}:fold{f}:rep{r}`
- frozen scorers: `phase64b_naibbe.output_metrics / aggregate_realizations / evaluate_aggregate` with `fold_contexts` from `phase62c_c0_a1_results.json` and `phase63a_training_vocab_results.json`
- source: ZL3b-n.txt Git blob `2a4533ab9bdfa85db9bad602d590978953055df1`
- decision: `MEMORYLESS TOKEN GRAMMAR PARTIAL` (see REPORT_C §2.2 for the H62 normalization caveat)
