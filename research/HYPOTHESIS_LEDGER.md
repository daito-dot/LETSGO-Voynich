# Hypothesis ledger

Last consolidated: 2026-09-06

This ledger records tested hypotheses and keeps failed hypotheses visible. `SUPPORTED` means supported under the stated frozen test, not historically or semantically identified.

## A. Earlier image / label / astronomy hypotheses

| Phase | Hypothesis / question | Status | Key evidence |
|---|---|---|---|
| 1 | f103v star entries have a special start form | SUPPORTED STRUCTURE | star/paragraph starts strongly enriched for `p` and gallows-class initials; image subtypes did not classify starts |
| 1-2 | one visible token = one 12-slot unit | NOT SUPPORTED as universal | useful coverage, but pharmaceutical labels can require multiple concatenated slot-units |
| 2 | `Lc` and `Lf` labels are structurally different | SUPPORTED STRUCTURE | leave-one-folio-out role classification ~0.65–0.69 balanced accuracy; permutation significant |
| 2 | same-row `Lc`/`Lf` labels encode paired content | NOT SUPPORTED | correct-row similarity did not beat within-folio shuffles |
| 2 | label ↔ own body row is semantic | NOT SUPPORTED | within-folio correct-row tests null; strong same-folio vs cross-folio effect instead |
| 2 | visible Pharma tokens can concatenate legal units | CANDIDATE STRUCTURE | <=3-part coverage ~89% Lc / ~97% Lf vs shuffled ~61–64%; segmentation not unique |
| 3 | matched Pharma plant labels repeat their name/stem in matched Herbal text | NOT SUPPORTED | corrected 5-pair exact test: 3/5 partial hits; permutation p=0.308 |
| 4 | residualized visual plant pair signal survives Currier/hand/position controls | NOT SUPPORTED | weak surface effects disappear under stricter controls |
| 5 | visually similar plant/root attributes yield similar labels | NOT SUPPORTED | combined similarity correlation ~-0.052; exact p~0.58 |
| 6 | duplicate Pharma labels are strongly local row/folio IDs | NOT SUPPORTED | localization did not significantly exceed random placement |
| 7 | `mousetail` root attribute has a shared short Voynich marker | NOT SUPPORTED | maxT-corrected fragment search null |
| 8 | zodiac labels show a simple two-part surface sigla structure | NOT SUPPORTED at raw surface | corrected 1–3 glyph search ~p 0.10–0.17 |
| 9 | Liber Hermetis XXV rising figures map to zodiac labels | NOT SUPPORTED | interval-preserving null removes initial similarity |
| 10/14 | zodiac labels contain a sign-independent 1–30 degree code | NOT SUPPORTED | leave-one-sign-out exact-position accuracy ~3.7% vs 3.33%; p~0.61 |
| 10-13 | zodiac morphology changes with physical production order | SUPPORTED STRUCTURE | page-distance similarity, `ee` trend r~+0.923, PCA chronology r~0.870; corrected p<0.01 |
| 15 | f69v first units directly encode Arabic 28 lunar-mansion article/Sa'd classes | NOT SUPPORTED | best circular/direction/category optimization p~0.34 |
| 16 | f69v uses `o = al-` plus root-initial encoding | NOT SUPPORTED | optimized permutation p~0.458 |
| 17 | specific same-context unit substitutions explain zodiac drift | CANDIDATE LOCAL | `iin` directionality survives one held-out context split; sparse |
| 18 | `al -> ee` is a universal Voynich substitution | NOT SUPPORTED globally | zodiac-local signal; pharmaceutical labels do not reproduce it |
| 20 | f68r3 star sectors share label morphology by sector | NOT SUPPORTED | exact 10-label permutations near null |
| 21 | f68r1 adjacent star labels are extremely similar | ARTIFACT | strong only in old S-number order; disappears in current ZL3b locus order |
| 22 | f68r2 adjacent labels alternate terminal class | CANDIDATE ORDER EFFECT | 21/23 changes in transcription/Petersen order; geometry unverified |
| 24/27 | `ot` is star-specific and supports `ot = Arabic al-` | NOT SUPPORTED | f68 prefix rates similar to zodiac label register |
| 26 | f68r2 terminal choice deliberately disambiguates similar stems | NOT SUPPORTED as main model | all-item maxT not significant |
| 28 | f68r2 terminal choice follows general Voynich morphology | SUPPORTED STRUCTURE | external-only terminal model predicts choices, p<5e-6 |
| 28b | residual f68r2 terminal alternation remains after fixing terminal counts | CANDIDATE ORDER EFFECT | pooled MCMC p~0.0138; order not verified geometry |
| 29 | f67r2 moon dark/light controls nearby label morphology | ARTIFACT / NOT SUPPORTED | corrected maxT ~0.54–0.66 |
| 29 | f67r2 color sequence encodes month lengths | NOT SUPPORTED | rotation/reversal-aware p~0.70 |
| 30 | f67r2 outer/sector/moon 12-layer strings share sector-specific lexical code | NOT SUPPORTED | 100k permutations: maxT p 0.24–0.53 |
| 30+ | image-grounded astronomical visual attributes carry residual text signal | OPEN | requires coordinate-verified object mapping |

## B. Token-construction / predictive-information program

| Program question | Status | Key evidence / consequence |
|---|---|---|
| Residual token-internal topology requires a rich latent construction state | NOT SUPPORTED / CURRENTLY UNNECESSARY | second-order occupied-slot successor grammar reaches within ~1–2% of empirical-inventory ceiling across ZL3b/IT2a; 298 conditional probabilities suffice |
| Token-internal grammar alone explains cross-token structure | REJECTED | complete memoryless V2 generator leaves major cross-token structure; held-out context models improve prediction |
| Cross-token structure is only a conspicuous but negligible local repeat effect | REJECTED | corrected Phase 1 B3 gains ~0.19164 bit/token over V2; longer history and observable state add reproducible gain after LOCAL40 |
| Apparent long history primarily requires literal long ordered memory | REJECTED as primary explanation | corrected Phase 2A/B: dominant increment is causal-prefix / previous-paragraph inventory; actual-order residual is much smaller but nonzero |
| Slow predictive information is only the immediately previous paragraph | REJECTED | Phase 2C OLDER inventory +0.0367964 bit/token vs PREV1 +0.0070407; both 5/5 |
| Slow predictive information is confined to the same page side/panel | REJECTED | Phase 2C same-side and cross-side prior histories both predict; cross-side survives conditional test |
| LOCAL40 mechanism is Currier-specific | REJECTED | Phase 3A LOCAL40 transports bidirectionally A↔B with nearly unchanged scalar strength |
| PREV_PARAS uses one universal scalar strength across Currier A/B | REJECTED | exact scalar transfer A→B only; B target prefers roughly twice A strength |
| Broad illustration/domain composition explains Currier PREV-strength asymmetry | REJECTED as sufficient explanation | matched pure-Herbal Phase 3C retains approximately twofold A/B alpha difference and A→B-only PREV scalar transport |
| Writing hand explains Currier PREV-strength asymmetry | UNRESOLVED / NOT IDENTIFIABLE WITH CURRENT METADATA | `$H` and Currier are inadequately crossed; no clean causal test licensed |
| Visible spaces are arbitrary transcription cuts with no production-boundary status | REJECTED under tested representations | ZL3b P1/P2 strongly support reset and exact cut; IT2a independently replicates all signs 5/5 |
| Visible certain spaces are reproducible construction/production boundaries | SUPPORTED ACROSS ZL3b/IT2a | ZL3b D_RESET +8.8119; IT2a +8.0926; exact cut beats ±1-atom shifts in 5/5 folds for both readings |
| Visible construction unit is therefore a natural-language word | NOT ESTABLISHED | production-boundary evidence does not distinguish word, cipher group, formal notation unit, procedural emission unit, etc. |
| Ordinary natural-language controls occupy the same inter-unit relation regime | REJECTED for frozen 101-language panel | Voynich has much lower adjacent corrected MI, strong immediate repeat excess and weak midrange recurrence relative to controls |
| Frozen common reversible-operation representatives reproduce the full Voynich regime | REJECTED for tested representatives | 0 full hits in Phase 84B; different transforms recover different partial components only |
| Frozen historical formulaic genres reproduce the full Voynich regime | REJECTED for tested 10-source panel | 0 full/partial hits; all miss in the same direction on MI/immediate/midrange recurrence |
| A flexible sequence challenger adds any complement beyond corrected B3 | SUPPORTED | Issue #118 `G_any = +0.0306054 bit/token`, positive 5/5; MIX_CONT beats B3 in every outer fold |
| Cross-boundary context adds information beyond a matched byte-level token-emission complement | SUPPORTED — SMALL ROBUST RESIDUAL | Issue #118 `G_context = +0.0178533 bit/token`, positive 5/5; RESET/CONT use the same frozen byte family and independently selected mixture weights |
| Corrected B3 has exhausted all reproducible cross-boundary surface predictability | REJECTED | matched RESET/CONT residual remains positive in all five outer folds |
| The surviving residual is large enough to imply a rich hidden information channel | NOT SUPPORTED | residual is only ~0.018 bit/token, ~0.19% of B3 code length; no large latent information rate follows |
| Rich latent-state modeling is currently licensed for direct interpretation | NOT YET — LOCALIZATION REQUIRED | Issue #118 passes the residual-capacity gate but Issue #88 still requires localization against observable regime/state/support effects before a latent challenger receives interpretation |
| Currier/observable-state/support effects explain the new Issue #118 residual | OPEN — NEXT GATE | freeze localization before any latent-state model; residual sign cannot be used to choose strata or architecture |

## Current working hypothesis

The most economical live structural hypothesis is:

> Each visible certain-space unit is a bounded construction episode produced by a compact internal grammar. Nearby units are weakly coupled by an edit-near recurrence/cache process, while slower paragraph/prefix inventory modulates which families are active. Some mechanism strength varies by observable manuscript regime. A further very small cross-boundary surface-context residual survives the strongest current non-latent summary, but its source has not yet been localized.

This is a working model to falsify, not a decipherment claim.
