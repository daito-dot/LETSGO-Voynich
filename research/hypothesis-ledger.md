# Hypothesis ledger

This public ledger records hypotheses that have been tested or materially constrained. Negative results are retained. Phase-specific reports control exact numerical details; `research/STATUS.md` controls the current high-level interpretation after later evidence. Reproducibility audit files may narrow what a historical result can support without rewriting its frozen pass/fail decision.

| ID | Hypothesis | Current status | Key evidence / qualification |
|---|---|---|---|
| H3 | Matched pharmaceutical plant labels repeat their name/stem in matched Herbal text | NOT SUPPORTED | Corrected primary visual-pair test: 2 total 4-gram hits; exact label-permutation p=.725; binary pair-hit p=.667. |
| H39 | `{k,t}` behaves as a structural equivalence class | SUPPORTED STRUCTURE | Opposite member trends, approximately stable sum, very similar local contexts. Structural equivalence only; semantic/cipher equivalence not established. |
| H40-A | Structural/functional information survives removal of within-slot values | SUPPORTED STRUCTURE | Slot occupancy predicts pharmaceutical document roles and line-position structure in tested domains. |
| H40-B | `{k,t}` is an information-bearing cryptographic equivalence | NOT ESTABLISHED | No independently grounded plaintext/content prediction yet. |
| H41-G2 | State-invariant equivalence predicts pharmaceutical item-specific relation | NOT SUPPORTED in tested Pharma row domain | Correct-vs-wrong item relation tests did not establish item content while controls detected folio state. |
| H41-G3 | Current invariants are primarily formal/document-functional/local-state | SUPPORTED RELATIVE TO G2 | Better description of present evidence; does not prove absence of semantics. |
| H42-A | Stable period survives token/boundary-preserving controls | NOT SUPPORTED | Apparent T=4 recurrence vanishes under whole-token morphology-preserving null. |
| H42-B | Current periodic signal supports numerical semantic value | NOT SUPPORTED | Periodic-looking structure attributable to lower-level cadence/reset. |
| H42-C | Token/boundary architecture can induce apparent periodicity | SUPPORTED MECHANISM | Demonstrated by structure-preserving controls. |
| H44-F5 | Literal online copy-and-modify is the main generator | WEAKENED / NOT ESTABLISHED | Strong predictive code length, but no earlier-source directional asymmetry; edit geometry largely inventory-driven. Better phrasing: local activation of related token families. |
| H45-P | Each paragraph has one stationary paragraph-local distribution | FALSIFIED AS STRONG FORM | Shifted-boundary and within-paragraph position tests show dynamic rather than stationary behavior. |
| H46-S | Short-range continuation is distinctive Voynich evidence | NOT SUPPORTED | Medieval Latin prose reproduces it, often more strongly. |
| H46-R | Large paragraph-boundary edit1-family discontinuity is unusual relative to current prose/cipher controls | REFINED BY PHASE59-62 | Medieval source-native entries reproduce part of a broader transition space, but objective N0 controls fail the stricter common S1 direction and local-family S2 magnitude. |
| H47-P | Paragraph reset is mainly a prefix/suffix-specific edit phenomenon | NOT SUPPORTED | Reset is distributed over substitution/insertion/deletion and initial/medial/final zones. |
| H47-D | Paragraph reset reflects broad active-family reconfiguration | SUPPORTED STRUCTURE | Broad operation-zone geometry; strongest nuisance-cipher scalar match does not reproduce full geometry. Mechanism remains open. |
| H48-N | Natural languages cannot produce substantial edit1 word-form families | FALSIFIED | Classical Arabic and Middle English pilots naturally produce substantial near-form families. |
| H49-F | Conventional programming/formal text alone explains Voynich near-neighbor topology | NOT SUPPORTED | Ordinary programming/formal corpora are much lower after matched comparisons. |
| H50-D | Simple finite-state family generator can reproduce high density + locality | MECHANISM DEMONSTRATED | Exploratory DSL can match these two dimensions after target-aware tuning. Not historical evidence. |
| H51-D | Frozen Phase50 simple DSL is sufficient as broad Voynich mechanism | FALSIFIED AS SUFFICIENT MECHANISM | 20 generated corpora all far below Voynich paragraph reset and line-position grammar. Historical Phase51 generator source has since been recovered for provenance. |
| H52-G | High Voynich edit1 density is mainly an artifact of choosing a low-density Latin control document | PRELIMINARY NOT SUPPORTED | Medieval manuscript choice matters strongly, but simple length/inventory matching leaves a large typical Voynich excess. |
| H52-S | Voynich section differences are negligible | NOT SUPPORTED | Section explains substantial variation; crossed analyses show real section signal independent of some hand/Currier combinations. |
| H53-P | Simple stationary paragraph-local family preference is sufficient | NOT SUPPORTED AS SUFFICIENT | Increasing paragraph family reuse raises reset mainly by overproducing generic local clustering. |
| H54-U | Paragraph-entry reset is manuscript-universal | WITHDRAWN / NOT SUPPORTED | Correct page-side audit shows positive reset in H/B/P/S/T but small A/C samples are negative. Earlier recto/verso collapse was corrected. |
| H56-1 | A compact latent state predicts substantial structural variation | QUALIFIED SUPPORT | Matched-token analysis: ~64% variance in 3 PCs, ~79% in 5; not a 1–2 axis system. |
| H56-2 | Physical-order state is one smooth drift | PARTIAL / REFINED | Locality survives exact section+Currier+hand matching, but one smooth trajectory is inadequate. |
| H56-3 | Shared grammar plus local state transfers across sections | SUPPORTED RELATIVE | Cross-scale latent basis recurs; paragraph-entry transition transfers across H/B/P/S/T. |
| H56-4 | Stable residual opportunity remains after known structural prediction | CANDIDATE DEFINED | Phase57 narrows it to a robust leading ~2D subspace. |
| H57-1 | Residual is stable across reasonable token representations | PARTIAL SUPPORT | Leading residual space remains moderately aligned under reasonable EVA unit definitions. |
| H57-2 | Residual is stable across matched window scale | SUPPORTED FOR TOP-2 / PARTIAL OVERALL | Top-2 stable across 15–40 token windows; PC3+ more scale-sensitive. |
| H57-3 | Residual is merely omitted local physical/page state | NOT SUPPORTED BY TESTED MODELS | Leakage-safe local context does not explain it away. |
| H57-4 | Leading residual remains broadly label-neutral | SUPPORTED FOR TOP-2 | Cross-fitted metadata removal leaves weak broad-label association. |
| H58-1 | Robust 2D residual carries independent page-level visual content information | NOT SUPPORTED IN TESTED DOMAINS | Biological/balneological and early Herbal-A independently annotated page-level tests all nonsignificant. Localized object-level semantics remain untested. |
| H58-2 | Robust residual is only simple unmodeled document location | NOT SUPPORTED BY 58A | Recto/verso and coarse physical-position prediction do not exceed matched nulls. |
| H58-3 | No detectable information exists at the current residual representation | OPEN / PRELIMINARY | Page-level content tests are negative, but localized independently mapped content is unavailable rather than falsified. |
| H59B-1 | Practical-medical genre alone is sufficient to explain Voynich entry transition | NOT ESTABLISHED | Medical controls show partial directional similarity, but ecclesiastical entries can also align and effects are heterogeneous. |
| H59B-2 | Voynich entry transition is absent from all medical controls | REJECTED AS STATED | Source-native medical entries reproduce part of the broader development transition. |
| H59B-3 | Mixed structured medieval genres reproduce part of the entry phenomenon | SUPPORTED DEVELOPMENT EVIDENCE | Medical and nonmedical source-marker controls show substantial entry transitions, but Phase62 objective N0 controls do not reproduce the stricter common held-out S1 direction. |
| H59C-1 | Generic medieval entry grammar is sufficient for Voynich | NOT SUPPORTED | Phase59 external basis was incomplete; Phase62 N0 independently fails common S1 and S2. |
| H59C-2 | Voynich combines shared medieval entry grammar with a Voynich-specific component | SUPPORTED STRUCTURE | Phase59 external component plus stable orthogonal remainder; Phase62 strengthens the need for specialization because objective N0 S1 is opposite in sign and S2 is only ~13% of Voynich. |
| H59C-3 | External entry similarity is fully stable to control composition | NOT SUPPORTED / METHODOLOGICAL WARNING | Historical Phase59 item subsets were partly unrecoverable; Phase62 therefore replaced them prospectively with a Voynich-blind corpus-wide source rule. |
| P60-1 | Real paragraph entry is a special local/directional state rather than an arbitrary internal fluctuation | SUPPORTED | Phase60A real boundaries exceed internal pseudo-boundaries; all five physical-leaf cross-fit folds positive. |
| P60-2 | Entry specialization is carried by a stable interpretable structural subset | QUALIFIED SUPPORT | Corrected audit retains broad signed association with TTR/length, edit1/local-near-family and k/t-related dimensions, but exact historical Phase60B `n=380` eligibility and fine contribution ranking are not replay-certified. |
| P60-3 | A paragraph-entry formal role transfers across manuscript sections | SUPPORTED | Phase60C held-out-section prediction transfers across H/B/P/S/T and broader structure adds paired discrimination beyond nuisance baselines. |
| P60-4 | Entry state prospectively initializes/predicts later paragraph body beyond early body state | NOT SUPPORTED | Phase60D2/60E coupling-free tests do not show useful prospective line0 information once metadata/immediate previous state are known. Phase60D recovery-vector result is mathematically coupled; public 60E exact replay remains provenance debt. |
| P60-5 | Stationary/weak-context formal generation needs explicit entry machinery to reproduce surviving signature | SUPPORTED AS MECHANISM CONSTRAINT | Frozen Phase50/51 DSL produces fluctuations but not the Voynich entry-specific behavior; explicit boundary-conditioned machinery is required for that generator family. |
| P60-6 | Low-complexity bounded cipher transforms do not automatically create Voynich specialization | SUPPORTED / REFINED | Phase62C: best frozen boundary-blind reversible transform (digraph coding) materially improves N0 but leaves S1 opposite in sign and S2 at only ~0.249× Voynich. Simple recoding helps but is insufficient. |
| P60-7 | Independently localized content relation eventually emerges after structural modeling | OPEN | Current page-level visual tests are negative; localized mapping remains unavailable. |
| P61-A0-entry | One low-complexity boundary-aware entry mixture can reproduce the held-out Voynich entry-direction target without persistent paragraph state | SUPPORTED NARROW ARCHITECTURE GATE | Phase61A shows the A0 family can reach the exposed scalar entry target. Strength search was exposed; not prospective validation of a preselected strength. |
| P61-A0-joint | A0 is sufficient to jointly reproduce the surviving Voynich structural fingerprint | FALSIFIED AS SUFFICIENT MODEL | Phase61B: local-prev10 is far too low while line-position/entry effects are mis-scaled; edit1 density is non-independent. Historical exact A0 executable remains provenance debt. |
| P61-A1 | A0 plus exactly one bounded local-family mechanism can bring frozen entry/locality/aggregate-line-position targets into the same held-out regime | SUPPORTED NARROW STRUCTURAL GATE | Phase61C ratios are entry 0.797, local-prev10 0.717, aggregate eta2 mean 1.116. Training-vocabulary-only sensitivity is stable. Post-hoc coordinate audit shows full line-position profile mismatch, so the claim is scalar/aggregate only. |
| P62-N0 | Source-native structured medieval plaintext is materially competitive with Voynich on the common S1–S3 scorecard before encoding | NOT SUPPORTED | Phase62B: S1 -0.980× (opposite sign), S2 0.133×, S3 0.989×. S1 negative for all primary manuscripts; S2 failure survives all manuscript omissions. |
| P62-S3 | Generic line-position grammar is a strong Voynich-specific discriminator | NOT SUPPORTED AT CURRENT RESOLUTION | N0 essentially matches aggregate S3. Scalar line-position structure alone is downgraded; profile-aware diagnostics remain important. |
| P62-C0 | A bounded global boundary-blind reversible recoding can materially improve N0 joint fit without target-aware paragraph/section rules | SUPPORTED AS LIMITED IMPROVEMENT / INSUFFICIENT MODEL | Phase62C selects non-overlapping digraph coding in 5/5 training folds; joint MSE improves in 5/5 held-out folds and passes 3/4 manuscript-omission stability criterion. But S1 remains -0.932× and S2 only 0.249×, so C0 fails the broad joint regime. |
| P62-A1-common | Frozen Phase61C A1 remains materially competitive when re-scored on the cross-representation Phase62 common scorecard without retuning | SUPPORTED ON EXPOSED SCALAR SCORECARD | Phase62C ratios of means: S1 0.623, S2 1.512, S3 0.587; all within the frozen broad interval. This is not a universal fold-wise pass and does not erase the Phase61C coordinate-profile mismatch or A1 target-dependence costs. |
| H62-P1 | The near-family recurrence-distance profile discriminates the provisional leading exposed-score mechanism family | SEALED PROSPECTIVE HOLDOUT | Exact five bins, null, normalization and profile distance were frozen in Phase62A. Voynich profile must not be computed/revealed before Phase62D ranking/unresolved-set interpretation is committed. |

## Current mechanism alternatives

The exposed common-score tournament has now produced a provisional structural ordering among the **tested implementations**:

`A1 > C0 > N0` on exposed scalar fit.

This is not yet an overall mechanism-family verdict.

- **N0:** not jointly competitive; nevertheless demonstrates that generic line-position S3 is ordinary in structured medieval text.
- **C0:** materially improves N0 and therefore supports limited explanatory value for reversible boundary-blind recoding, but remains far from Voynich on S1/S2. The wider C family is not falsified by this bounded C0 test.
- **A1:** strongest exposed scalar fit, but pays explicit Voynich boundary/local mechanisms, Voynich-selected parameters and empirical target vocabulary, lacks a meaningful plaintext/historical model, has fold heterogeneity, and does not reproduce the full line-position coordinate profile.

Therefore Phase62D must freeze **A1 as provisional leading exposed-score structural candidate while leaving the overall N/C/G mechanism question unresolved**. Only after that independent interpretation freeze may the sealed H62-P1 prospective recurrence-distance profile be revealed.

No A2, C1 or M0 repair is allowed before the prospective result is recorded.

## Rule for adding hypotheses

Every new entry must identify a falsification condition and distinguish structural support from semantic/decipherment support. If a hypothesis survives only after adding free exceptions, those added degrees of freedom must be recorded. Deliberate deception receives no null-result privilege.