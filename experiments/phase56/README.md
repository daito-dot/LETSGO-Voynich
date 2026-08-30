# Phase 56 — latent multiscale state map

The execution plan was frozen in `PLAN.md` before implementation.

## Phase 56A — canonical substrate: COMPLETE

`phase56_build_state_matrix.py` parses the actual ZL3b page-header metadata and preserves physical leaf and page-side separately.

Audited substrate: 226 page headers, 4,087 included P-coded prose lines, **206 page-sides**, **99 physical leaves**, **736 paragraphs**. The 197 page-sides overlapping Phase55 were regression-checked on the shared fingerprint definitions; maximum absolute difference was **0.0**.

## Phase 56B — drift versus regimes: COMPLETE AS DEVELOPMENT DIAGNOSTIC

Physical locality survives exact matching on section + Currier + hand, but neither one globally smooth trajectory nor a small set of sharp changepoints adequately describes it. The best current description is broad state/block differences plus local physical similarity.

## Phase 56C — latent dimensionality: COMPLETE AS DEVELOPMENT DIAGNOSTIC

A critical sample-size audit withdrew the original unmatched-PC1 section interpretation: full-page PC1 correlated **r=-0.886** with page token count.

After matched-token reconstruction, the leading direction is instead a near-family activation / local-continuity axis. Matched page fingerprints require several dimensions rather than one or two: first 3 PCs explain **63.7%**, first 5 **78.7%**, first 7 **90.0%**. Similar leading directions recur at paragraph scale. Linear PCA beats RBF kernel PCA in grouped held-out reconstruction, so no nonlinear-manifold advantage is currently established.

## Phase 56D — paragraph transition transfer: COMPLETE AS DEVELOPMENT EVIDENCE

The paragraph-entry transient is multivariate and transfers across sections.

Using a 5D matched paragraph-trained basis, line states were centered within page-side. For each paragraph with both entry and third line available, the line0 -> line2 delta was measured. A transition direction was learned from all but one major section and tested on the held-out section.

Held-out results:

| section | paragraphs | cosine to trained direction | mean projection | page-bootstrap 95% |
|---|---:|---:|---:|---:|
| H | 176 | .862 | 1.569 | [1.106, 2.022] |
| B | 74 | .738 | .635 | [.119, 1.085] |
| P | 41 | .876 | 2.073 | [1.305, 2.740] |
| S | 199 | .899 | 1.391 | [1.072, 1.716] |
| T | 27 | .966 | 2.102 | [1.331, 2.845] |

All held-out sections project positively onto a transition learned without them. Biological is weaker but remains positive.

Therefore the Phase54 paragraph-entry effect is no longer just a single continuity statistic. It is a transferable multivariate state transition within this manuscript.

This remains internal/development evidence, not external replication.

## Phase 56D — structural residualization

A first leakage-safe paragraph residual target was constructed.

Substrate:

- 635 paragraphs with >=20 body tokens
- fingerprint = mean of 10 random contiguous 20-token windows
- split-half reliability across independent window draws: median **r=.964**, range about .944-.983
- 5-fold CV grouped by physical leaf

Predictors were intentionally conservative:

1. section + Currier + hand + paragraph ordinal;
2. the same metadata plus a leave-one-paragraph-out mean fingerprint from other paragraphs on the same page-side.

Mean standardized held-out MSE:

- metadata model: **.919**
- metadata + page context: **.885**

Thus page-local context adds real predictive information, but most stable paragraph variation remains unexplained.

Feature-level cross-fitted R2 with page context ranges from essentially zero for unit inventory to about:

- mean token length **.369**
- final entropy **.220**
- `k/t` mass **.187**
- within-`{k,t}` balance **.140**

The residual's largest PCA axis has almost no remaining broad-label association:

- section eta2 **.0052**
- Currier eta2 **.0016**
- hand eta2 **.0020**

A modest page-local residual similarity remains, so this is not yet a final nuisance-free residual.

## Phase 56 decision

The manuscript-internal mapping has now answered the main questions posed in the frozen plan well enough to define the next research object:

1. **structural scales:** broad document constraints, page-local family activation, paragraph-entry transition, line/token morphology;
2. **physical order:** real locality, but not one simple smooth drift or a few sharp changepoints;
3. **latent dimensionality:** moderately low-dimensional, roughly several axes rather than one/two or eleven independent dimensions;
4. **metadata:** important but heavily confounded, and no longer dominant after matched-token correction;
5. **residual target:** reliable paragraph-specific structural variation remains after conservative cross-fitted metadata + page-context prediction.

### Hypothesis status

- H56-1 compact latent state: **QUALIFIED SUPPORT**
- H56-2 smooth physical drift: **PARTIAL / REFINED** — locality yes, globally smooth drift no
- H56-3 shared grammar plus local state: **SUPPORTED RELATIVE TO SEPARATE-GRAMMAR DESCRIPTION**, especially by cross-scale basis recurrence and cross-section paragraph-transition transfer
- H56-4 stable residual opportunity: **OPEN, candidate residual now defined**

## Immediate next frontier

Do **not** interpret the residual semantically yet.

First perform a residual robustness gate:

- alternative token-unit/collapse definitions;
- matched-window length sensitivity;
- richer but leakage-safe local structural predictors;
- transcription/source sensitivity where feasible;
- verify that residual axes and paragraph-level relationships reproduce under these perturbations.

Only residual structure that survives that gate should be exposed to illustration/content/cipher tests. This prevents a new round of semantic fishing on estimator artifacts.

Detailed numeric results: `phase56b_results.json`, `phase56c_results.json`, `phase56d_results.json`.
