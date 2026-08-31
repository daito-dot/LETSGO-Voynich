# Issue #26 direct-music research status

Updated after Issue26E6 first reveal.

| Track | Direct question | Result | Narrow interpretation |
|---|---|---|---|
| A | Do visible Voynich tokens reduced sequence-blind to 6/7 finite states reproduce medieval plainchant cadence/motif geometry? | **NOT SUPPORTED** | 0/5 folds closer to chant; Voynich much closer to structured medieval Latin under frozen screen. |
| B | Do surviving zodiac labels preferentially group Ptolemy *Harmonics* III.12 same-tonos zodiac pairs? | **NOT SUPPORTED** | target rank 75/105, exact p=.714 after production-order correction. |
| C | Can Ptolemy III.8–9 interval↔zodiac geometry itself identify musical encoding? | **NON-IDENTIFYING AS STATED** | ordinary zodiac geometry already contains opposition/trine/square angular relations; requires an extra independent observable. |
| D | Does the March-2026 public `daiin=octave` / f67r2 / f113r *Veni Creator* package survive literal and multiplicity-aware audit? | **NOT SUPPORTED** | 0/4 frozen components pass; one highlighted f67r2 opposition is factual but not statistically exceptional. |
| E | Does Zattera slot10 as a six-state channel plus sequence-blind 20-class remaining morphology predict the Guidonian 20×6 admissibility lattice? | **NARROW POSITIVE, LATER REFINED** | under full per-fold refitting Guidonian beat ordinary degree-matched nulls on ZL; this architecture-level effect later fails stronger E6 structured controls under the primary parser. |
| E2 | Does E survive higher null resolution, independent IT2a, and prospective fixed-map transfer? | **NUMERIC REPLICATION, LATER REFINED** | E2-A/B replay and architecture replication are real; E2-C fixed-map transfer is later shown by E5 not to be selection-adjusted evidence for Guidonian specificity. |
| E3 | Does the fixed-map result prefer the actual Guidonian higher-order row neighborhoods over strongly matched non-musical lattices? | **PAIR-GEOMETRY SUFFICIENT / GUIDONIAN NOT SPECIFIC** | non-Guidonian alternatives with the same labeled pair-intersection matrix equal/beat Guidonian under the fixed-map test. |
| E4 | Can a purely non-musical topology learned from Voynich morphology transfer to another transcription? | **NON-MUSICAL TOPOLOGY MATCHES/BEATS GUIDONIAN** | ZL-learned topology transfers to IT2a better than Guidonian, but E5 clarifies that Voynich→Voynich self-learning is not by itself the correct measure of external Guidonian surprise. Draft PR #34 remains unmerged. |
| E5 | After giving every external lattice the same ZL mapping/parser selection path that produced E2-C, is Guidonian fixed-map transfer still unusual? | **SELECTION FREEDOM EXPLAINS APPARENT SURPRISE** | 86/200 degree-matched alternatives transfer at least as well as Guidonian (`p≈.433`); joint stable-map+transfer event `p≈.154`. Draft PR #36 remains unmerged. |
| E6 | Under full per-fold 720-map refitting, does Guidonian beat pair-overlap-matched and exact-pair non-musical structures on both ZL and IT? | **PAIR GEOMETRY / GENERIC STRUCTURE SUFFICIENT UNDER FULL REFIT** | primary `min`: structured-null p=.376 (ZL), .525 (IT), so the E/E2 architecture effect is not Guidonian-specific. `max` sensitivity retains a narrow topology-class preference but is not primary. |

## Current interpretation

Issue26 does **not** support a broad claim that visible Voynich running text is music or a direct Guidonian encoding. A–D remain negative or non-identifying. E/E2 found a real structural regularity, but E3–E6 progressively identify why it is not currently diagnostic of music.

The strongest current statement is:

> Voynich token morphology contains a stable six-state dependency structure. The Guidonian gamut happens to instantiate a compatible six-state overlap topology, but the primary fully-refitted comparison does not distinguish the historical Guidonian structure from stronger non-musical overlap-matched alternatives.

This is a **six-state formal/dependency result**, not a musical decipherment.

## What E5 corrected

E2-C had looked unusually strong because a state→vox map discovered on ZL was frozen and transferred to IT2a, while random null lattices were forced to use the same numeric column mapping.

E5 gave each alternative its own analogous ZL discovery→freeze→IT path. Under that matched selection process:

- Guidonian IT fixed-map mean: `0.833714`;
- degree-matched alternative median: `0.830968`;
- 86/200 alternatives reached or exceeded Guidonian;
- `p_transfer≈0.433`;
- 30/200 simultaneously achieved mapping recurrence >=4/5 and IT accuracy >= Guidonian (`p_joint≈0.154`).

Therefore the E2-C ~10.5-point apparent advantage over its original fixed-map null median is not a valid selection-adjusted measure of Guidonian specificity.

## What E6 adds

E6 attacks the remaining architecture-level E/E2-A/B effect with stronger controls while restoring the original full fitting freedom for every candidate.

Primary `min`:

- ZL Guidonian `0.850966`, structured median `0.850249`, `p=.376`;
- IT Guidonian `0.851215`, structured median `0.851376`, `p=.525`.

Thus the primary architecture effect disappears once non-musical lattices preserve comparable six-state pair-overlap geometry.

Among the exhaustive exact-pair alternatives, one ties Guidonian exactly. A post-reveal combinatorial check shows that this alternative is just the Guidonian row-neighborhood multiset under column reversal `(0,1,2,3,4,5)→(5,4,3,2,1,0)`. Because E/E2/E6 freely permute all six state↔column mappings, those two are mathematically observationally equivalent under this model and cannot be distinguished.

The other two exact-pair alternatives are genuinely non-isomorphic and Guidonian beats them under full refit.

## Residual max-parser signal

The preregistered `max` sensitivity remains more interesting than the primary result:

- ZL Guidonian `0.843903` vs structured median `0.835988`, `p=.0297`;
- IT Guidonian `0.840472` vs structured median `0.831423`, `p=.0495`;
- Guidonian beats the two genuinely non-isomorphic exact-pair alternatives in both transcriptions.

This suggests a possible narrow preference for the **Guidonian unlabeled topology class** under the `max` parse convention.

However, `max` is a sensitivity analysis that became salient during the earlier music search. It cannot be promoted to primary after E6. Any follow-up must prospectively test this already-observed `max` pattern on an independently justified population or transcription/representation, with column-isomorphic topologies quotiented before reveal.

## Current falsification frontier

The direct-music slot-lattice path has reached a strong boundary for the primary analysis. The highest-information remaining questions are now:

1. **Prospective max test:** can the already-observed `max` topology-class preference replicate on an independent population without selecting `max` again?
2. **Slot10 exceptionalism:** is the six-state slot10 dependency unusually strong compared with other slots / matched categorical factors, accounting for the fact that slot10 was selected because its arity matched six Guidonian voces?
3. **k dependence:** does the signal persist when `k=20` is no longer privileged, or under a k-free information-theoretic dependency measure?
4. **Mechanism discrimination:** do natural-language morphology, cipher transforms, artificial slot grammars, lookup systems, or procedural text generators predict the observed six-state dependency better?

Do not proceed to melody extraction, pitch-order fitting, rhythm inference, or literal `ut/re/mi/fa/sol/la` naming from the current evidence.

Negative results and refinements must remain visible alongside the positive numerical replications. Do not summarize Issue26 as “Voynich is music” or “decoded.”
