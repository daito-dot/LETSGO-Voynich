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
| H46-R | Large paragraph-boundary edit1-family discontinuity is unusual relative to current prose/cipher controls | REFINED BY PHASE59-63 | Medieval source-native entries reproduce part of a broader transition space, but objective N0 controls fail stricter common S1/S2 while independent GC/IT transcriptions preserve Voynich entry/recurrence effects. |
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
| P60-1 | Real paragraph entry is a special local/directional state rather than an arbitrary internal fluctuation | SUPPORTED + INDEPENDENT TRANSCRIPTION REPLICATION | Phase60A real boundaries exceed internal pseudo-boundaries; all five physical-leaf cross-fit folds positive. Phase63B independently reproduces positive entry projection in 5/5 GC v101 folds and 5/5 IT EvaT folds. |
| P60-2 | Entry specialization is carried by a stable interpretable structural subset | QUALIFIED SUPPORT | Corrected audit retains broad signed association with TTR/length, edit1/local-near-family and k/t-related dimensions, but exact historical Phase60B `n=380` eligibility and fine contribution ranking are not replay-certified. |
| P60-3 | A paragraph-entry formal role transfers across manuscript sections | SUPPORTED | Phase60C held-out-section prediction transfers across H/B/P/S/T and broader structure adds paired discrimination beyond nuisance baselines. |
| P60-4 | Entry state prospectively initializes/predicts later paragraph body beyond early body state | NOT SUPPORTED | Phase60D2/60E coupling-free tests do not show useful prospective line0 information once metadata/immediate previous state are known. Phase60D recovery-vector result is mathematically coupled; public 60E exact replay remains provenance debt. |
| P60-5 | Stationary/weak-context formal generation needs explicit entry machinery to reproduce surviving signature | SUPPORTED AS MECHANISM CONSTRAINT | Frozen Phase50/51 DSL produces fluctuations but not the Voynich entry-specific behavior; explicit boundary-conditioned machinery is required for that generator family. |
| P60-6 | Low-complexity bounded cipher transforms do not automatically create Voynich specialization | SUPPORTED / REFINED | Phase62C: best frozen boundary-blind reversible transform (digraph coding) materially improves N0 but leaves S1 opposite in sign and S2 at only ~0.249× Voynich. H62-P1 and Phase63B IT transfer keep fixed C0 much farther than A1-R1 on recurrence geometry. |
| P60-7 | Independently localized content relation eventually emerges after structural modeling | OPEN | Current page-level visual tests are negative; localized mapping remains unavailable. |
| P61-A0-entry | One low-complexity boundary-aware entry mixture can reproduce the held-out Voynich entry-direction target without persistent paragraph state | SUPPORTED NARROW ARCHITECTURE GATE | Phase61A shows the A0 family can reach the exposed scalar entry target. Strength search was exposed; not prospective validation of a preselected strength. |
| P61-A0-joint | A0 is sufficient to jointly reproduce the surviving Voynich structural fingerprint | FALSIFIED AS SUFFICIENT MODEL | Phase61B: local-prev10 is far too low while line-position/entry effects are mis-scaled; edit1 density is non-independent. Historical exact A0 executable remains provenance debt. |
| P61-A1 | A0 plus exactly one bounded local-family mechanism can bring frozen entry/locality/aggregate-line-position targets into the same held-out regime | SUPPORTED NARROW STRUCTURAL GATE | Phase61C ratios are entry 0.797, local-prev10 0.717, aggregate eta2 mean 1.116. Training-vocabulary-only sensitivity is stable. Post-hoc coordinate audit shows full line-position profile mismatch, so the claim is scalar/aggregate only. |
| P62-N0 | Source-native structured medieval plaintext is materially competitive with Voynich on the common S1–S3 scorecard before encoding | NOT SUPPORTED | Phase62B: S1 -0.980× (opposite sign), S2 0.133×, S3 0.989×. S1 negative for all primary manuscripts; S2 failure survives all manuscript omissions. |
| P62-S3 | Generic line-position grammar is a strong Voynich-specific discriminator | NOT SUPPORTED AT CURRENT RESOLUTION | N0 essentially matches aggregate S3. Scalar line-position structure alone is downgraded; profile-aware diagnostics remain important. |
| P62-C0 | A bounded global boundary-blind reversible recoding can materially improve N0 joint fit without target-aware paragraph/section rules | SUPPORTED AS LIMITED IMPROVEMENT / INSUFFICIENT MODEL | Phase62C selects non-overlapping digraph coding in 5/5 training folds; joint MSE improves in 5/5 held-out folds and passes 3/4 manuscript-omission stability criterion. But S1 remains -0.932× and S2 only 0.249×. On sealed H62-P1 and Phase63B IT transfer, fixed C0 remains much farther than A1-R1. |
| P62-A1-common | Frozen Phase61C A1 remains materially competitive when re-scored on the cross-representation Phase62 common scorecard without retuning | SUPPORTED ON EXPOSED SCALAR SCORECARD | Phase62C ratios of means: S1 0.623, S2 1.512, S3 0.587; all within the frozen broad interval. This is not a universal fold-wise pass and does not erase the Phase61C coordinate-profile mismatch or A1 target-dependence costs. |
| H62-P1 | The frozen near-family recurrence-distance profile discriminates among N0/C0/A1 on unseen geometry | **SUPPORTED PROSPECTIVELY FOR A1 + TRANSCRIPTION ROBUST** | Frozen before tournament outcomes. Original A1 mean D 0.763 vs N0 1.530 / C0 1.859 and mean |ΔC_short| 0.116 vs 0.638 / 1.308, with 5/5 wins. Phase63B independently reproduces positive short-range concentration in 5/5 GC and 5/5 IT folds; IT A1-R1 retains mean D 0.830 and mean |ΔC_short| 0.0718. |
| P63-A1-R1 | A1's exposed and H62-P1 advantages survive when output vocabulary is restricted to token types observed on training leaves only, with no retuning | **SUPPORTED ROBUSTNESS** | Phase63A removes ~49% of held-out distinct types from generation candidates (mean held-out occurrence coverage ~0.802). A1-R1 still has S1/S2/S3 ratios 0.654/1.511/0.583 and H62-P1 mean D 0.767 / mean |ΔC_short| 0.118, beating N0 and C0 5/5 folds on both H62-P1 metrics. All frozen R1/R2/R3 conditions pass; degradation vs full-vocabulary A1 is negligible. |
| P63-TX | Strongest Phase60–63 entry/locality/A1 results survive independently maintained Voynich transcription/segmentation lineages | **SUPPORTED — STRONG PHASE63B REPLICATION** | GC v101: entry and `C_short` positive in 5/5 W1 folds with W2 sign stability. IT EvaT: same observational effects positive 5/5; frozen ZL-selected A1-R1 transfers without retuning with exposed ratios 0.737/1.586/0.647 and H62 mean D 0.830 / mean |ΔC_short| 0.0718, beating N0 on D 4/5 and C-short 5/5 and C0 5/5 on both. This reduces ZL/EVA representation dependence but does not establish historical identity or semantic emptiness. |
| P64-A1-R2 | A1's structural advantage survives removal of the empirical training token inventory as the output vocabulary | **MIXED / STRICT AUTONOMY NOT SUPPORTED** | Phase64A: ZL S1/S2 pass (`0.847×/0.920×`) but S3 fails the frozen lower bound at `0.468×`; IT passes all three (`1.136×/0.976×/0.586×`). Despite synthetic vocab train overlap only ~20–23%, held-out overlap ~12–13% and roughly halved edit1 connectivity, H62 remains essentially unchanged: ZL D `0.762`, C-short error `0.120`, 5/5 wins vs N0/C0 on both; IT D `0.832`, C-short `0.0749` and full arm pass. Full autonomy is not established, but empirical inventory membership is strongly weakened as the explanation for the prospective H62 success. |
| P64-C1 | A materially stronger but bounded meaningful-text + encoding model can rival A1 under explicit complexity cost | **PARTIAL SUPPORT FOR C STRUCTURAL POWER / NOT AN A1 RIVAL** | Exact published Naibbe v2 strongly improves over C0 on H62 (5/5 wins on both diagnostics) and improves N0 on D_profile, but primary S1/S2 are opposite-sign/near-zero, C-short is worse than N0, and it fails every frozen A1-rival condition except one fold-level D win. Frozen classification `C1-E0 PARTIAL`. This strengthens A1 relative to this serious C1 while explicitly leaving the broader C family open. |

## Current mechanism alternatives

The tested A1 mechanism now has five increasingly independent evidence layers:

### Exposed scalar scorecard

`A1 > C0 > N0` among tested implementations.

### Sealed prospective H62-P1

`A1` is the unique leader under every frozen original criterion, with 5/5 wins on both primary diagnostics.

### Held-out-vocabulary restriction

`A1-R1` retains essentially the same exposed and H62-P1 performance even though nearly half of held-out distinct token types are unavailable to generation.

### Independent-transcription replication

- GC2a/v101 reproduces entry specialization and positive short-range recurrence concentration in 5/5 folds without conversion to EVA.
- IT2a/EvaT reproduces the same observational effects and supports full frozen A1-R1 transfer.
- IT A1-R1 / IT exposed ratios are `0.737 / 1.586 / 0.647`.
- IT H62 mean D is `0.830` versus N0 `1.477` / C0 `1.797`; mean `|ΔC_short|` is `0.0718` versus `0.622 / 1.292`.

### Inventory-autonomy stress test

- A1-R2/MG0 removes the explicit empirical training-token membership list as output vocabulary.
- ZL strict source-arm gate fails only because S3 is `0.468×`; S1/S2 pass and H62 beats N0/C0 5/5 on both diagnostics.
- IT passes the entire frozen source-arm gate.
- H62 is nearly unchanged from A1-R1 despite low synthetic-vocabulary overlap and roughly half the empirical edit1 connectivity.

Current interpretation:

- **N0:** not jointly competitive and not competitive on unseen near-family recurrence geometry; nevertheless shows generic aggregate line-position S3 is ordinary in structured medieval text.
- **C0:** materially improves N0 on exposed structure, so simple reversible recoding has limited explanatory value, but remains far from Voynich on S1/S2 and performs poorly on H62-P1. The wider C family is not falsified by this bounded C0 test.
- **A1/A1-R1:** **leading tested structural mechanism with prospective support, training-only-vocabulary robustness and independent-reading transfer**. The evidence is now difficult to dismiss as a ZL3b/EVA-specific artifact. However A1 still uses empirical training-side morphology/vocabulary, Voynich-derived architecture, frozen Voynich-selected parameters, explicit paragraph boundaries/10-token memory and held-out layout. It has known fold/full-profile mismatch and is not a decipherment or historical model.

Phase64B has now supplied one serious independently published C1. It demonstrates that a developed meaningful-text cipher can move substantially closer than C0 on H62, but it still does not generate the entry/local-recurrence signature or rival A1. The next high-information challenge is therefore an **independently grounded localized content-anchor audit (Phase65A)** rather than A2/S3 repair or open-ended cipher fishing. If no defensible anchor exists, the content lane remains externally blocked and only a separately motivated residual C hypothesis with a distinct frozen prediction is admissible.

## Rule for adding hypotheses

Every new entry must identify a falsification condition and distinguish structural support from semantic/decipherment support. If a hypothesis survives only after adding free exceptions, those added degrees of freedom must be recorded. Deliberate deception receives no null-result privilege.
