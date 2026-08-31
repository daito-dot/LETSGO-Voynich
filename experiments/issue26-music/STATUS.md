# Issue #26 direct-music research status

Updated after Issue26E5 first reveal.

| Track | Direct question | Result | Narrow interpretation |
|---|---|---|---|
| A | Do visible Voynich tokens reduced sequence-blind to 6/7 finite states reproduce medieval plainchant cadence/motif geometry? | **NOT SUPPORTED** | 0/5 folds closer to chant; Voynich much closer to structured medieval Latin under frozen screen. |
| B | Do surviving zodiac labels preferentially group Ptolemy *Harmonics* III.12 same-tonos zodiac pairs? | **NOT SUPPORTED** | target rank 75/105, exact p=.714 after production-order correction. |
| C | Can Ptolemy III.8–9 interval↔zodiac geometry itself identify musical encoding? | **NON-IDENTIFYING AS STATED** | ordinary zodiac geometry already contains opposition/trine/square angular relations; requires an extra independent observable. |
| D | Does the March-2026 public `daiin=octave` / f67r2 / f113r *Veni Creator* package survive literal and multiplicity-aware audit? | **NOT SUPPORTED** | 0/4 frozen components pass; one highlighted f67r2 opposition is factual but not statistically exceptional. |
| E | Does Zattera slot10 as a six-state channel plus sequence-blind 20-class remaining morphology predict the Guidonian 20×6 admissibility lattice? | **NARROW POSITIVE, LATER REFINED** | Under equal per-fold 720-map fitting, Guidonian beats ordinary degree-matched nulls on ZL; this architecture-level result remains numerically real. |
| E2-A/B | Does the freely refitted E architecture survive higher null resolution and independent IT2a transcription? | **REPLICATED ARCHITECTURE-LEVEL SIGNAL** | Degree-matched-null advantage survives higher-resolution ZL and refitted IT2a. It does not by itself identify music. |
| E2-C | Does a ZL-posthoc recurring Guidonian six-state map prospectively transfer to IT2a? | **RAW TRANSFER REPLICATES, SELECTION SIGNIFICANCE LATER FAILS** | Guidonian fixed-map IT mean = 0.833714, but E5 shows the apparent ~10.5-point advantage is not unusual once each null gets its own analogous ZL selection. |
| E3 | Does the fixed-map result prefer the actual Guidonian higher-order row neighborhoods over strongly matched non-musical lattices? | **PAIR-GEOMETRY SUFFICIENT / GUIDONIAN NOT SPECIFIC** | two of three exhaustive non-Guidonian alternatives with the exact same labeled pair-intersection matrix equal/beat Guidonian. |
| E4 | Can a Voynich-trained non-musical topology transfer better than Guidonian across transcriptions? | **YES, BUT NOT A FAIR EXTERNAL-SURPRISE NULL BY ITSELF** | A self-trained Voynich model beats Guidonian, but learning Voynich from Voynich makes this comparison intrinsically favorable to the non-musical model. E5 supplies the fairer selection audit. |
| E5 | After charging the actual ZL parser/map selection path, is Guidonian's external fixed-map transfer still unusual? | **SELECTION FREEDOM EXPLAINS THE APPARENT SURPRISE** | 86/200 degree-matched nulls equal/beat Guidonian IT accuracy after their own ZL selection (`p_transfer=.433`); joint recurrence+transfer `p=.154`. |

## Current interpretation

Issue26 does **not** support a broad claim that visible Voynich running text behaves like ordinary monophonic music. A–D remain negative or non-identifying.

E/E2-A/B do retain a real structural observation:

> under sequence-blind `20 residual-morphology classes × 6 slot10 states`, the Guidonian topology performs somewhat better than ordinary degree-matched random lattices when every lattice is freely refitted on training data.

But E3 and E5 sharply limit the musical interpretation of that observation.

### What E3 established

The full Guidonian 20-locus×6-vox lattice is not identified. Once the entire labeled 6×6 pairwise column-intersection matrix is held equal to Guidonian, non-Guidonian higher-order row systems equal or outperform it.

Thus the positive architecture-level signal can be localized to lower-order six-state dependency geometry rather than the uniquely Guidonian higher-order lattice.

### What E5 corrected

E2-C's very large fixed-map advantage compared Guidonian's **ZL-selected** recurring map with random null lattices forced to use the same numeric state→column permutation.

E5 instead gives every candidate lattice its own analogous discovery path:

1. search all 720 state↔column mappings on ZL folds;
2. inspect both `min` and `max` parser policies;
3. choose the most recurrent ZL mapping using ZL only;
4. freeze it;
5. transfer it to IT2a.

Under this matched-selection process:

- Guidonian recurrence = **4/5**;
- Guidonian IT mean = **0.833714**;
- degree-matched null IT median = **0.830968**;
- **86/200** nulls equal/beat Guidonian IT accuracy;
- `p_transfer = 0.432836`;
- **30/200** simultaneously reach recurrence >=4/5 and IT accuracy >=Guidonian;
- `p_joint = 0.154229`;
- 91/200 nulls have recurrence 4/5 or 5/5 at all.

So the repeated six-state map and its prospective transfer are **not rare once the same post-reveal selection opportunity is charged to the null family**.

The stronger E3 structured family is even less favorable to Guidonian after matched selection: median IT transfer `0.839598` exceeds Guidonian, with 69/100 nulls equal/above.

All three exhaustive exact-pair alternatives match or exceed Guidonian under the recurrence+transfer criterion; one reaches 5/5 recurrence and IT mean `0.843521`.

## Strongest surviving statement

The strongest defensible statement is now:

> Voynich slot10 participates in a cross-transcription-stable six-state dependency structure. Its low-order pair geometry is compatible with geometry also present in the Guidonian six-vox system, but that compatibility is not specific to the Guidonian higher-order lattice and does not yield an unusually strong prospective transfer once the actual ZL selection process is applied equally to non-Guidonian alternatives.

This is a **formal six-state dependency signal**, not affirmative evidence of musical plaintext or a Guidonian encoding.

## Current falsification frontier

The remaining positive E/E2-A/B architecture-level effect should now be attacked directly:

> When every candidate lattice is allowed full 720-map refitting independently on every training fold, does Guidonian still outperform **pair-overlap-matched** and **exact-pair** non-Guidonian alternatives on held-out ZL and IT?

This is different from E3/E5 because it tests the original freely refitted architecture-level signal under stronger structured controls rather than the fixed-map transfer path.

If that effect also collapses, the music-specific structural branch is effectively exhausted. If it survives, the next task is to identify exactly what low-order property makes Guidonian-like lattices unusually compatible, without assigning literal pitch semantics.

Do **not** proceed to melody extraction, pitch-order fitting, duration inference, or literal `ut/re/mi/fa/sol/la` naming from the current evidence.

Negative results A–D and refinements E3/E5 must remain visible alongside E/E2. Do not summarize Issue26 as “Voynich is music” or “decoded.”

E4 remains on its separate unmerged branch/PR; E5 is also branch-only. **No experiment branch should be merged to `main` without explicit user authorization while parallel experiments are active.**
