# Phase 70A — frozen A1 surface over reversible meaningful plaintext

Status: **CLOSED — P70-SC1 PARTIAL COMPATIBILITY**

## Question

Can the already-frozen A1 formal machinery operate as a surface layer over exactly recoverable meaningful plaintext and still reproduce the held-out Voynich structural regime?

This was deliberately a **compatibility construction**, not a new historical cipher proposal. It reused without retuning:

- the same four CREMMA medieval Latin manuscripts;
- the exact published Naibbe v2 reversible homophone catalog;
- the exact Phase61C fold-specific `entry_strength` and `local_family_p` values;
- the exact A1 entry shape definition;
- the exact previous-10 edit1 local-family rule;
- the existing S1/S2/S3 and H62-P1 scorecard.

`SC0` is the paired reversible homophonic control without A1 surface selection. `SC1` adds the frozen A1 entry and local selectors. Plaintext segmentation and respacing randomness are paired so that the causal contrast is the surface selector itself.

## Reversibility

Both arms remained exactly reversible over the entire frozen experiment:

- plaintext units: **864,323** across 5 folds × 4 manuscripts × 5 realisations;
- SC0 raw decode accuracy: **1.000**;
- SC1 raw decode accuracy: **1.000**.

For SC1 body units:

- an edit1-local candidate existed for **56.07%**;
- the frozen local Bernoulli selector activated on **23.99%**;
- an activation coincided with a usable local candidate on **13.50%** of body units;
- every such activated opportunity emitted from the intended local subset.

The local mechanism was therefore active while preserving exact plaintext recovery.

## Paired control — SC0

Without the A1 selectors, the meaningful-text homophonic construction remains far from the Voynich entry/locality effects:

| metric | SC0 / Voynich |
|---|---:|
| S1 paragraph-entry projection | **0.012×** |
| S2 previous-10 near-family excess | **-0.025×** |
| S3 aggregate line-position eta2 | **0.640×** |

H62-P1:

- mean `D_profile`: **1.343**
- median `D_profile`: **1.350**
- mean `|ΔC_short|`: **0.816**

The full SC0 gate fails.

## Frozen A1 surface — SC1

Adding the frozen A1 selectors changes the result substantially:

| metric | SC1 / Voynich | frozen [0.5, 2.0] gate |
|---|---:|---|
| S1 paragraph-entry projection | **0.151×** | **FAIL** |
| S2 previous-10 near-family excess | **1.426×** | PASS |
| S3 aggregate line-position eta2 | **0.598×** | PASS |

H62-P1:

- mean `D_profile`: **0.760**
- median `D_profile`: **0.844**
- mean `|ΔC_short|`: **0.224**

Against both frozen N0 and C0 baselines, SC1 wins **5/5 folds on both H62 diagnostics**. All H62 viability conditions pass.

So the full primary failure is narrow but real:

> **S2 passes, S3 passes, the complete H62-vs-N0/C0 gate passes, but S1 paragraph entry remains only about 15% of the Voynich target.**

The broad semantic-compatibility gate therefore fails.

## Paired causal result

The preregistered SC1-vs-SC0 causal comparison passes every required direction:

1. S1 absolute ratio error to the Voynich target is lower;
2. S2 absolute ratio error is lower;
3. mean H62 `D_profile` is lower;
4. mean H62 `|ΔC_short|` error is lower.

Thus the borrowed A1 surface selectors are not inert decorations. They causally move an exactly reversible meaningful-text encoding toward the Voynich structural regime.

The movement is especially large for locality:

- H62 mean `D_profile`: **1.343 → 0.760**;
- H62 mean `|ΔC_short|`: **0.816 → 0.224**;
- S2: **-0.025× → 1.426×**.

The entry selector also moves S1 in the correct direction, but only from **0.012× → 0.151×**, far short of the frozen lower gate.

## Comparison with frozen A1-R1

A1-R1 remains the best complete formal reference, but the separation is now informative.

| H62 metric | A1-R1 | SC1 meaningful-text composite |
|---|---:|---:|
| mean `D_profile` | 0.767 | **0.760** |
| median `D_profile` | **0.809** | 0.844 |
| mean `|ΔC_short|` | **0.118** | 0.224 |

SC1 beats A1-R1 on `D_profile` in **3/5 folds** and has a slightly lower mean profile distance. It loses on C-short concentration magnitude, winning only **2/5** folds there.

This is enough to reject a simple inference that the strong H62 recurrence geometry itself requires semantic-free generation. A fully reversible meaningful plaintext can carry essentially the same five-bin recurrence-profile shape under the frozen local selector.

But Phase70 does **not** establish full equivalence to A1. The paragraph-entry effect remains the decisive missing component.

## Raw-token sensitivity

The no-respacing/raw-token view gives the same qualitative verdict:

- S1 **0.157×** — fail;
- S2 **1.546×** — pass;
- S3 **0.593×** — pass;
- H62 mean `D_profile` **0.772**;
- H62 mean `|ΔC_short|` **0.231**;
- H62 viability vs N0/C0: pass.

Therefore the primary failure is not created by the 3% ciphertext-space removal layer.

## Decision

Frozen classification:

> **P70-SC1 PARTIAL COMPATIBILITY**

The strongest supported interpretation is now more specific than after Phase69:

> **Meaningful, exactly recoverable plaintext is strongly compatible with the tested Voynich short-range recurrence and aggregate line-position regime when the frozen A1 local surface selector is applied. The same construction does not reproduce the Voynich paragraph-entry state strongly enough.**

This separates two formal phenomena that had previously travelled together inside A1:

- **local near-family recurrence** can be imposed as a reversible surface-selection effect over meaningful plaintext;
- **paragraph-entry specialization** is not recovered by simply porting the frozen A1 entry shape weighting into the same homophonic codebook.

That is a useful mechanistic split. It weakens any argument from locality alone to semantic absence, while making paragraph entry a sharper discriminator among future models.

## Blinded routing constraint

`POST_RESULT_ROUTE_A.md` was committed while the first Phase70 scientific run was still in progress and before any Phase70 result was inspected.

The applicable frozen route is **Route P**. Therefore:

- no Phase70 parameter is changed;
- no local-probability, history-length, edit-rule, entry-strength, codebook, plaintext-panel or respacing search is allowed to repair the failed S1 gate;
- no `SC2` is created as a post-hoc rescue;
- the successful paired directions and the failed entry gate are both retained.

The next research step should be an **orthogonal, externally grounded discriminator**, preferably content-linked or source-grounded, rather than another optimization of the Phase70 construction.

## Claim boundary

This result does **not** show that:

- the Voynich plaintext is Latin;
- Naibbe is the historical cipher;
- A1 is the historical production algorithm;
- edit1-aware homophone choice was historically used;
- the manuscript is deciphered.

It is an existence/compatibility result using deliberately borrowed A1 training-side information. Its scientific value is the demonstrated coexistence of exact semantic recoverability with much of the strongest formal structure, and the isolated failure of the entry component.

## Provenance

- scientific head: `22c8969a88dd0e18d3c889cebc148fe6aecbadc5`
- GitHub Actions run: `33385619434`
- job: `99467454328`
- artifact: `phase70a-first-reveal`, ID `9756239580`
- artifact ZIP SHA-256: `dbbb5e1f027b492375d590390c23546a9ae272482b6a32c9ad4ff3da547e63da`
- raw result SHA-256: `03ede283ec8ad6ea0c1002b582dc98db346ec6b996ff3fdd081659c3c2695fd3`
- frozen plan SHA-256: `001ee763ecf759caf45e4bf04f64a1dc176ab39299909c46b999eb588b08496c`
- frozen decision SHA-256: `60d6f742324b3e8ba54444b3e42bd04b416052f8f114bf568808e291d1ab0a81`
- scientific executable SHA-256: `56720de2b3306fd1e7208401048ec5d82554ad9e2ad06efc947ebba5ac7b5955`
