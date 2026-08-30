# Hypothesis ledger

This public ledger records hypotheses that have been tested or materially constrained. Negative results are retained. Phase-specific reports control exact numerical details; `research/STATUS.md` controls the current high-level interpretation after later evidence.

| ID | Hypothesis | Current status | Key evidence / qualification |
|---|---|---|---|
| H3 | Matched pharmaceutical plant labels repeat their name/stem in matched Herbal text | NOT SUPPORTED | Corrected primary visual-pair test: 2 total 4-gram hits; exact label-permutation p=.725; binary pair-hit p=.667. |
| H39 | `{k,t}` behaves as a structural equivalence class | SUPPORTED STRUCTURE | Opposite member trends, approximately stable sum, very similar local contexts. Structural equivalence only; semantic/cipher equivalence not established. |
| H40-A | Structural/functional information survives removal of within-slot values | SUPPORTED STRUCTURE | Slot occupancy predicts pharmaceutical document roles and line-position structure in tested domains. |
| H40-B | `{k,t}` is an information-bearing cryptographic equivalence | NOT ESTABLISHED | No independently grounded plaintext/content prediction yet. |
| H41-G2 | State-invariant equivalence predicts pharmaceutical item-specific relation | NOT SUPPORTED in tested Pharma row domain | Correct-vs-wrong item relation tests did not establish item content while controls detected folio state. |
| H41-G3 | Current invariants are primarily formal/document-functional/local-state | SUPPORTED RELATIVE TO G2 in tested domain | Better description of present evidence; does not prove absence of semantics. |
| H42-A | Stable period survives token/boundary-preserving controls | NOT SUPPORTED | Apparent T=4 recurrence vanishes under whole-token morphology-preserving null. |
| H42-B | Current periodic signal supports numerical semantic value | NOT SUPPORTED | Periodic-looking structure attributable to lower-level cadence/reset. |
| H42-C | Token/boundary architecture can induce apparent periodicity | SUPPORTED MECHANISM | Demonstrated by structure-preserving controls. |
| H44-F5 | Literal online copy-and-modify is the main generator | WEAKENED / NOT ESTABLISHED | Strong predictive code length, but no earlier-source directional asymmetry; edit geometry largely inventory-driven. Better phrasing: local activation of related token families. |
| H45-P | Each paragraph has one stationary paragraph-local distribution | FALSIFIED AS STRONG FORM | Shifted-boundary and within-paragraph position tests show dynamic rather than stationary behavior. |
| H46-S | Short-range continuation is distinctive Voynich evidence | NOT SUPPORTED | Medieval Latin prose reproduces it, often more strongly. |
| H46-R | Large paragraph-boundary edit1-family discontinuity is unusual relative to current prose/cipher controls | OPEN / DISCRIMINATING TARGET | Dante raw/F1/F2 remain well below Voynich; aggressive nuisance cipher transforms move toward it but pilot controls are limited. |
| H47-P | Paragraph reset is mainly a prefix/suffix-specific edit phenomenon | NOT SUPPORTED | Reset is distributed over substitution/insertion/deletion and initial/medial/final zones. |
| H47-D | Paragraph reset reflects broad active-family reconfiguration | SUPPORTED STRUCTURE | Broad operation-zone geometry; strongest nuisance-cipher scalar match does not reproduce full geometry. Mechanism remains open. |
| H48-N | Natural languages cannot produce substantial edit1 word-form families | FALSIFIED | Classical Arabic and Middle English pilots naturally produce substantial near-form families. |
| H49-F | Conventional programming/formal text alone explains Voynich near-neighbor topology | NOT SUPPORTED | Ordinary programming/formal corpora are much lower after matched comparisons. |
| H50-D | Simple finite-state family generator can reproduce high density + locality | MECHANISM DEMONSTRATED | Exploratory DSL can match these two dimensions after target-aware tuning. Not historical evidence. |
| H51-D | Frozen Phase50 simple DSL is sufficient as broad Voynich mechanism | FALSIFIED AS SUFFICIENT MECHANISM | 20 generated corpora all far below Voynich paragraph reset and line-position grammar. |
| H52-G | High Voynich edit1 density is mainly an artifact of choosing a low-density Latin control document | PRELIMINARY NOT SUPPORTED | Medieval manuscript choice matters strongly, but simple length/inventory matching leaves a large typical Voynich excess. |
| H52-S | Voynich section differences are negligible | NOT SUPPORTED | Section explains substantial variation; later crossed analyses show real section signal independent of some hand/Currier combinations. |
| H53-P | Simple stationary paragraph-local family preference is sufficient | NOT SUPPORTED AS SUFFICIENT | Increasing paragraph family reuse raises reset mainly by overproducing generic local clustering. |
| H54-U | Paragraph-entry reset is manuscript-universal | WITHDRAWN / NOT SUPPORTED | Correct page-side audit shows positive reset in H/B/P/S/T but small A/C samples are negative. Earlier recto/verso collapse was corrected. |
| H56-1 | A compact latent state predicts substantial structural variation | QUALIFIED SUPPORT | Matched-token analysis: ~64% variance in 3 PCs, ~79% in 5; leading directions recur across page/paragraph scales. Not a 1–2 axis system. |
| H56-2 | Physical-order state is one smooth drift | PARTIAL / REFINED | Locality survives exact section+Currier+hand matching, but one smooth trajectory and simple changepoints are inadequate. Broad blocks + local similarity fit better descriptively. |
| H56-3 | Shared grammar plus local state transfers across sections | SUPPORTED RELATIVE | Cross-scale latent basis recurs; paragraph-entry transition learned from other sections transfers positively to held-out H/B/P/S/T. |
| H56-4 | Stable residual opportunity remains after known structural prediction | OPEN / CANDIDATE DEFINED | Reliable paragraph-specific residual remains after cross-fitted metadata/page-state prediction; Phase57 narrows it to a robust leading ~2D subspace. |
| H57-1 | Residual is stable across reasonable token representations | PARTIAL SUPPORT | Leading residual space remains moderately aligned under raw EVA and conservative/Phase56 composite units, but nontrivial rotation remains. |
| H57-2 | Residual is stable across matched window scale | SUPPORTED FOR TOP-2 / PARTIAL OVERALL | On a fixed eligible paragraph set, top-2 subspace remains close across 15–40 token windows; PC3+ is substantially more scale-sensitive. |
| H57-3 | Residual is merely omitted local physical/page state | NOT SUPPORTED BY TESTED MODELS | Adding leakage-safe same-page/opposite-side/adjacent-leaf context does not explain away the residual; model sensitivity remains documented. |
| H57-4 | Leading residual remains broadly label-neutral | SUPPORTED FOR TOP-2 | Explicit cross-fitted metadata removal leaves PC1/PC2 section/Currier/hand eta² around .01–.03; leaf-bootstrap top-2 subspace is stable. |
| H58-1 | Robust 2D residual carries independent content information | PROSPECTIVE / UNTESTED | Frozen before content inspection in Phase58. Requires independently defined content and matched permutation/null controls. |
| H58-2 | Robust residual is only unmodeled document structure | PROSPECTIVE / UNTESTED | Phase58A nuisance transfer is the first control. Strong nuisance prediction is a warning, not semantic evidence. |
| H58-3 | No detectable information exists at the current residual representation | PROSPECTIVE / UNTESTED | Supported only if both nuisance and independently grounded content relations fail under the frozen design. |

## Important open mechanism alternatives

Current evidence remains compatible with meaningful text, systematic cipher, bounded adversarial/deceptive cipher, hierarchical formal generation, or mixed mechanisms. The shared paragraph transition and robust residual constrain all of these but do not select one.

## Rule for adding hypotheses

Every new entry must identify a falsification condition and distinguish structural support from semantic/decipherment support. If a hypothesis survives only after adding free exceptions, those added degrees of freedom must be recorded. Deliberate deception receives no null-result privilege.
