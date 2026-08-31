# Issue #26E6 — fully refitted structured-null architecture audit

Status: **PAIR GEOMETRY / GENERIC STRUCTURE SUFFICIENT UNDER FULL REFIT**

E6 tested the last strong architecture-level music-specific reading that survived E5: although the E2-C fixed-map surprise disappeared after selection correction, the original E/E2-B architecture had still shown Guidonian outperforming ordinary degree-matched nulls when every lattice was freely refitted on each training fold.

E6 replaced those weak nulls with the stronger E3 families and gave **every candidate exactly the same full fitting freedom**: all `6! = 720` state↔column bijections plus optimal 20-cluster↔20-row assignment, independently on every fold.

The primary `min` result does **not** identify Guidonian. Pair-overlap-matched non-musical structures explain the architecture-level advantage.

## 1. Frozen classification

Primary (`min`):

**`PAIR GEOMETRY / GENERIC STRUCTURE SUFFICIENT UNDER FULL REFIT`**

Predeclared `max` sensitivity receives the same formal classification because one exact-pair alternative is observationally tied under the free-column model. However, the `max` numerical pattern is substantially more favorable to the Guidonian **unlabeled topology class** and is discussed separately below.

## 2. Replay firewall

All four previously revealed Guidonian architecture means replayed exactly within `1e-12`:

| transcription | parser | Guidonian mean |
|---|---|---:|
| ZL | min | `0.8509664380470466` |
| ZL | max | `0.8439032769036159` |
| IT2a | min | `0.8512154779726009` |
| IT2a | max | `0.8404723923113318` |

Thus E6 is a stronger-null extension of the existing E/E2 architecture, not a changed implementation.

## 3. Primary min result — structured nulls

The 100 E3 structured nulls preserve the Guidonian row/column capacity **and the entire histogram of six-state pair-overlap strengths**, while changing which pairs receive which overlaps.

### ZL

- Guidonian: **`0.8509664380`**
- structured-null median: `0.8502488698`
- q95: `0.8537158856`
- maximum: `0.8567932089`
- empirical p: **`0.3762376238`**
- structured-family gate: **FAIL**

Guidonian is only about **+0.072 percentage point** above the structured median and is exceeded by many candidates.

### IT2a

- Guidonian: **`0.8512154780`**
- structured-null median: **`0.8513763912`**
- q95: `0.8553918255`
- maximum: `0.8575620073`
- empirical p: **`0.5247524752`**
- structured-family gate: **FAIL**

The structured-null median is slightly **higher** than Guidonian.

Therefore the original primary E/E2-B advantage against ordinary degree-preserving random lattices does not survive when the null family is strengthened to preserve comparable pair-overlap geometry.

## 4. Primary min result — exact pair-matrix alternatives

E3 exhaustively enumerated all four row-neighborhood multisets having the complete labeled Guidonian 6×6 pair-intersection matrix: Guidonian plus three non-Guidonian alternatives.

Under full per-fold 720-map fitting:

### ZL min

| candidate | mean accuracy | Guidonian − candidate |
|---|---:|---:|
| Guidonian | `0.8509664380` | — |
| exact alt 0 | `0.8509664380` | `0.0000000000` |
| exact alt 1 | `0.8507988113` | `+0.0001676267` |
| exact alt 2 | `0.8507164799` | `+0.0002499582` |

### IT2a min

| candidate | mean accuracy | Guidonian − candidate |
|---|---:|---:|
| Guidonian | `0.8512154780` | — |
| exact alt 0 | `0.8512154780` | `0.0000000000` |
| exact alt 1 | `0.8495840611` | `+0.0016314169` |
| exact alt 2 | `0.8495980073` | `+0.0016174707` |

The frozen exact-pair requirement was strict superiority over all three. The exact tie therefore fails the gate on both transcriptions.

## 5. Post-reveal structural diagnostic — why exact alt 0 ties exactly

After the E6 reveal, a direct combinatorial isomorphism check was performed on the already frozen E3 catalog. This diagnostic is **not part of the E6 gate**.

Exact alternative 0 becomes the Guidonian row-neighborhood multiset under the single column permutation:

`(0,1,2,3,4,5) → (5,4,3,2,1,0)`

That is, reverse all six columns.

The E/E2/E6 architecture freely searches every `6!` state↔column bijection on every training fold. Under that model, Guidonian and exact alt 0 are therefore not merely empirically similar: they are **observationally equivalent hypothesis classes**. Any dataset scored by this architecture must give them the same optimum and held-out score after fitting.

This reveals an important identifiability limit:

> A test that freely permutes all six voice labels can never identify the **labeled** Guidonian lattice against a column-isomorphic alternative.

Accordingly, the exact-alt-0 tie should not be interpreted as evidence for a genuinely different unlabeled topology. The genuinely non-isomorphic exact alternatives are alt 1 and alt 2, which Guidonian does beat under E6.

However, this does not rescue the primary min result because the 100 broader structured nulls already eliminate Guidonian specificity (`p=.376` on ZL; `p=.525` on IT).

## 6. Max-parser sensitivity — a narrower residual signal

The predeclared `max` sensitivity is substantially different numerically.

### ZL max

- Guidonian: **`0.8439032769`**
- structured-null median: `0.8359882311`
- q95: `0.8421984280`
- maximum: `0.8448184029`
- empirical p: **`0.0297029703`**
- structured-family gate: **PASS**

Genuinely non-isomorphic exact alternatives:

- alt 1: `0.8409381498` — Guidonian higher by `0.0029651271`
- alt 2: `0.8429531360` — Guidonian higher by `0.0009501409`

### IT2a max

- Guidonian: **`0.8404723923`**
- structured-null median: `0.8314230878`
- q95: `0.8387763965`
- maximum: `0.8426944706`
- empirical p: **`0.0495049505`**
- structured-family gate: **PASS**

Genuinely non-isomorphic exact alternatives:

- alt 1: `0.8351254415` — Guidonian higher by `0.0053469509`
- alt 2: `0.8394941802` — Guidonian higher by `0.0009782121`

Thus, if the irrelevant column-isomorphic duplicate is quotiented out, the `max` parser shows a **replicated narrow preference for the Guidonian unlabeled topology class** over both the 100 pair-histogram-matched structures and the two genuinely non-isomorphic exact-pair alternatives.

This is scientifically interesting, but it is a **sensitivity result**, not the frozen primary result. It cannot retroactively turn E6 positive.

## 7. What hypothesis is now rejected?

E6 rejects the strong claim:

> “The architecture-level E/E2 result identifies the historical Guidonian 20×6 lattice rather than a generic six-state overlap/dependency geometry.”

The primary min parser gives no such specificity once the comparison family preserves relevant overlap structure.

The broader direct-music claim remains unsupported.

## 8. What remains unresolved?

A narrower question remains because the `max` parser replicated a stronger topology-class preference on both transcription lineages:

> Is the `max` result a real property of an independently justified parse convention, or did `max` become scientifically salient because it looked stronger during the earlier music search?

That is now the appropriate next falsification target.

A clean next experiment must not simply declare `max` primary after seeing E6. It needs an **independent reason or independent population** to test the already observed `max` prediction prospectively, with the topology quotient defined before reveal.

Until such a test exists, the defensible conclusion remains:

> The robust finding is a six-state Voynich dependency geometry. Guidonian provides one historically interesting realization of a closely matching topology, but the primary analysis does not identify it as music-specific.

## 9. First-reveal provenance

- branch: `issue26-music-e6-refit-structured-null`
- scientific head: `36dac1a040f6a081f0980689c722d230ec80abfa`
- plan-first commit: `f241f83a67e4fcd92107b505290ca2c1bb366037`
- exact replay-constant amendment: `ebe21e30ebbbb76e40155598026e97b10b64535f`
- first executable: `5c0f6fdcfef090570873cd813ea900bf0c7b186e`
- Actions run: `33367604252`
- job: `99411404858`
- artifact: `9748860247`
- artifact ZIP SHA-256: `711cdbb80af0fd2108e61b164687e35f2665927abdf7b7159d3a487a2e901850`
- raw JSON SHA-256: `d0767fcafdf1faf77772f442a309fbb255a8b1778df83a46ac38f8ab8551dce8`
- plan SHA-256: `6623c87641620f7cf4dafbb55e276c98ef62c8c515eb7fd61e5385840ce83737`
- script SHA-256: `064cc9c023d40e7ee4936f170df7fdbc15ce1447c8beb65e1bfeae4d41248c19`
- core SHA-256: `3e37c0223497f7008cb9d78ceeab18b34518c0c0b70860528a2017502fc1392d`

The branch remains independent. **No merge to main is authorized by this result.**
