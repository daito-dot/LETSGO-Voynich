# OGH-B first-reveal provenance

Status: **scientific first reveal complete — local execution**

## Chronology (git)

- PLAN_B first-add: `82245a49e7af7b3031a137c1679c03c998cddda2`
- executable first-add: `ef31e2e8c603ab31ad84ba39ecf82e9e3e3f1cef`
- pre-selection clarification: `27c4bbd218daea54cfd07c81348513810e82e3fb`
- stage-B0 selection commit and exact pre-reveal head: `2ea0a68482378c94218d9328192c23bdb25fe33a`
- selected model: G7A (second-order successor grammar), by the frozen PLAN_B §3 rule ("single eligible candidate"); G7B not scored.

## Execution

- host: Claude Code remote container, Linux 6.18.44-fc-v22 x86_64; Python 3.11.15; numpy 2.4.6, scipy 1.17.1
- population: 2 skeletons × G7A × 3 realizations = 6 corpora, 0 drops, 0 rerolls; four parallel processes
- finished: 2026-09-02 01:21:07 UTC
- seed namespaces `OGH-B:{source}:G7A:fold{f}:rep{r}`; nulls `OGH-B:{source}:G7A:rep{r}:{reference,test}-null`, 1,000 + 1,000
- sources: ZL3b-n.txt blob `2a4533ab9bdfa85db9bad602d590978953055df1`; IT2a-n.txt SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`
- anchors: OGH-A aggregate SHA-256 `6cabec85dcb4e49ca412df3468b544d7e427dacfb398379cb48248df7fa7a788` (G4/G5/G6 medians, not rescored)

## Frozen decision

`SUCCESSOR GRAMMAR NEAR-SUFFICIENT` (PLAN_B §5): Issue #68 gate passes in 6/6; gap to G6 median T is `−0.0165` (ZL3b arm, outside δ=0.0098) and `−0.0079` (IT2a arm, inside δ).

## Hashes

See `SHA256SUMS.txt`.
