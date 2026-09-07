# Issue #165 — section/domain source-attribution first reveal provenance

## Frozen entry authority

- Issue: #165
- score-free Gate0 PR: #166
- Gate0 merge: `389043ad2cc55eb15760ed3504fd03fc01253eb9`
- Gate0 result SHA-256: `3b6eededdfe197ed9152b9b0f756dffe34870eaf1a33b810d7e23f84d0d84f1a`
- original Gate0 script blob: `adaca5dc387d58542044089aac5faaedc8880ccf`
- Gate0 authority-fix wrapper blob: `8ad582bdea2351606e97e52c0ee733999c11820f`
- Gate0 provenance blob: `15627264ce598c315810458a64482e8f60d9afeb`
- frozen plan blob: `d334092e6c7cd38f76deb48250fa09d8f9468064`
- pure-I physical-leaf map SHA-256: `47ab536c6806eca5b037bc8cf81bae11069a153c92e4d17162c6381c92025eb1`
- Issue #161 scorer blob: `d24149977770118505f2147c5aa2bb727631906f`
- Issue #161 declared first-reveal result SHA-256: `11e179abcc53e5507d188b46f335c38198ee6a9d36f31fee406650610cafd031`

Gate0 licensed exactly one scientific section contrast: Currier B with pure `I=B` versus pure `I=S`. Currier A was `UNSCORABLE_BY_FROZEN_SUPPORT`. Scribe attribution was `SCRIBE_NOT_IDENTIFIABLE`.

## Pre-scorer clarification chronology

Before the scientific scorer existed, Issue #165 froze the remaining implementation details:

1. one section multiplier family shared across both transcription readings using `0.5*ZL3b + 0.5*IT2a` all-clean-BODY training counts;
2. section and Currier aggregate masses converted to smoothed outcome probabilities before their ratio was taken, so section sample size could not act as an outcome multiplier;
3. the section multiplier applied only on previous-terminal contexts retained by the frozen Issue #161 pooled edge table; unsupported exact contexts retained the Issue #161 empty-additive `1/32` distribution;
4. the same construction was used for the already-frozen one-leaf-left placebo labels.

No held-out target outcome was used in this clarification.

## Scorer chronology

- scientific scorer path: `experiments/predictive-information/source-attribution/issue165_section_domain_first_reveal.py`
- scorer-only commit: `a8267a38759ff1e897f4531159ccf813598a6b92`
- frozen scorer git blob: `10f5d54e14700e758054b216fd487c25d23dda84`
- workflow added only after scorer freeze
- first-reveal workflow head: `ec5450f779b4aca3dd6ff0de8dafba5961458889`
- workflow run: `34078834259`
- workflow conclusion: `success`
- artifact ID: `10003041494`
- artifact name: `issue165-section-domain-first-reveal-ec5450f779b4aca3dd6ff0de8dafba5961458889`
- artifact ZIP digest: `sha256:bab9f8d04396e7b5a17042c114b6739312832c25c4bf1bdbf5c880f2efbcfb63`
- result JSON SHA-256: `0b124ac9b3bbeb3a1a8165390e63176ff30594d46ae45e49be5536efa7e8805c`

The workflow reproduced the frozen Gate0 and authority pins, verified the exact ZL3b and IT2a sources, passed the target-free synthetic self-test, ran the scientific scorer once, asserted the frozen classification contract, and uploaded the result authority.

## Frozen classification

`NO ROBUST SECTION/DOMAIN OUTCOME INFORMATION`

Currier A was not scored because the score-free Gate0 found no eligible within-A section contrast. The only eligible section in A was `I=H`; sparse `I=T` and `I=C` leaves could not be promoted after target reveal.

### Currier B — ZL3b

`G_section = bits(EDGE_CURRIER) - bits(EDGE_SECTION)`

- folds: `[+0.008088080349596183, +0.0132260981209118, -0.014254522960696292, +0.018749144602006496, +0.01871423840195341]`
- mean: `+0.008904607702754318 bit/token`
- positive folds: `4/5`

`G_placebo = bits(EDGE_SECTION_SHUFFLED) - bits(EDGE_SECTION)`

- folds: `[-0.01099365267232777, -0.008006053143631675, -0.010408427153546285, +0.01866761213628898, -0.005337467206526725]`
- mean: `-0.0032155976079486946 bit/token`
- positive folds: `1/5`

The true section model therefore had positive raw incremental gain in 4/5 folds, but failed the preregistered placebo criterion.

### Currier B — IT2a

`G_section`:

- folds: `[+0.016492063818285274, +0.012320538319110952, -0.013843984227149164, +0.019356710478762196, +0.019582832212559964]`
- mean: `+0.010781632120313845 bit/token`
- positive folds: `4/5`

`G_placebo`:

- folds: `[-0.007899247434734136, -0.008284971974406474, -0.010561918388109603, +0.016848438510130848, -0.005430510291594359]`
- mean: `-0.003065641915742745 bit/token`
- positive folds: `1/5`

The independent IT2a reading shows the same pattern: positive raw section gain, but no superiority to the fixed placebo.

## Interpretation boundary

The result does **not** support promoting manuscript section/domain as an additional predictive responsibility beyond the compact Issue #161 observable edge model. The raw section effect is reproducible across readings, but the frozen placebo performs at least as well and therefore blocks attribution of that gain to the true section labels.

The accepted compact edge description remains:

> one shared common-EVA terminal→initial base table + a Currier-specific global next-initial outcome bias.

This result does not establish absence of all section structure. It establishes only that the preregistered section/domain outcome factor did not clear the held-out-plus-placebo gate on the identifiable Currier-B population. Currier A and scribe effects remain unidentifiable under the frozen support rules.

No claim about words, plaintext, semantics, language/cipher family, authorship, historical mechanism, artificiality/hoax, or decipherment is licensed by this result.
