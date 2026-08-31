# Issue #26E5 — selection-adjusted external-structure surprise audit

Status: **SELECTION FREEDOM EXPLAINS THE APPARENT SURPRISE**

E5 was motivated by a methodological correction to the interpretation of E4 and E2-C. A topology learned directly from Voynich should be expected to transfer well to another transcription of the same manuscript, so the fact that the E4 non-musical self-trained model beat Guidonian does not by itself tell us how surprising the external historical Guidonian fit is.

E5 therefore re-ran the actual E→E2-C discovery path as a matched selection experiment: every comparator lattice was allowed to search the same ZL parser/mapping freedom, choose its own most stable six-state correspondence using ZL only, freeze that correspondence, and then transfer it prospectively to IT2a.

Under that corrected comparison, the large E2-C fixed-map advantage is **not unusual**.

## 1. The key result

Guidonian replayed exactly:

- ZL-selected parser policy: **max**
- cross-fold mapping recurrence: **4/5**
- selected mapping: `EMPTY,d,l,r,m,n → (ut,fa,sol,re,mi,la)` = `(0,3,4,1,2,5)`
- ZL fixed-map mean held-out accuracy: **0.8417411147**
- IT2a fixed-map mean held-out accuracy: **0.8337140490**

But after giving each of 200 degree-matched non-Guidonian lattices the same or greater ZL-only selection freedom:

- **86/200** nulls reached or exceeded Guidonian's IT accuracy;
- selection-adjusted transfer `p = 0.4328358209`;
- **30/200** simultaneously had recurrence `>=4/5` and IT accuracy `>= Guidonian`;
- joint `p = 0.1542288557`;
- lexicographic historical-path `p = 0.2935323383`.

Frozen classification:

**`SELECTION FREEDOM EXPLAINS THE APPARENT SURPRISE`**

The E2-C ~10.54-percentage-point advantage over its fixed-map degree-null median therefore should **not** be interpreted as a selection-adjusted measure of how unusual Guidonian is among external 20×6 structures.

## 2. Why this changes E2-C

E2-C froze the Guidonian state→vox mapping after it had been observed on ZL, then used that same numeric six-state→column permutation for every random null lattice on IT2a.

That was a valid prospective test of the specific Guidonian correspondence once selected, but it did **not** give a random alternative topology the analogous opportunity to discover *its own* stable correspondence on ZL before IT transfer.

E5 does exactly that.

For every candidate lattice independently:

1. run both `min` and `max` on ZL;
2. in each of five ZL folds freely search all `6! = 720` state↔column bijections, exactly as in E;
3. measure which fitted permutation recurs most often across folds;
4. if several recurring maps tie, choose the one with best ZL fixed-map held-out performance;
5. choose the parser policy with greatest mapping recurrence, then greatest ZL fixed-map held-out performance;
6. freeze that candidate's own selected parser+mapping;
7. transfer it to IT2a, allowing only the 20 cluster→row assignment to train on IT folds.

IT2a is never used to choose a candidate's parser or six-state mapping.

This is a direct simulation of the researcher-selection path that produced E2-C.

## 3. Degree-matched null family

200 shared non-Guidonian lattices preserved:

- 20 rows;
- Guidonian row degrees;
- six columns each of degree 7;
- 42 allowed cells.

Unlike E/E2 fold-specific null generation, each E5 lattice remains the **same object across all ZL and IT folds**, because cross-fold mapping recurrence is the quantity being audited.

### IT transfer distribution after ZL-only selection

| quantity | result |
|---|---:|
| Guidonian IT mean | **0.833714** |
| null median | **0.830968** |
| null q95 | **0.849580** |
| null maximum | **0.859062** |
| nulls `>= Guidonian` | **86 / 200** |
| `p_transfer` | **0.432836** |

So Guidonian is only modestly above the null median once the nulls receive the same discovery→freeze→transfer opportunity.

### Mapping recurrence distribution

| maximum recurrence among 5 ZL folds | null count |
|---:|---:|
| 1/5 | 2 |
| 2/5 | 36 |
| 3/5 | 71 |
| 4/5 | 55 |
| 5/5 | 36 |

Guidonian's originally striking **4/5** mapping recurrence is therefore not rare in this model family: **91/200 (45.5%)** degree-matched null lattices reach recurrence 4/5 or 5/5 after the same min/max + 720-map search.

This is the most direct answer to the concern that the repeated Guidonian mapping itself looked extraordinary.

### Joint historical path

A stricter event requires both:

- recurrence at least Guidonian's 4/5;
- IT fixed-map accuracy at least Guidonian's 0.833714.

**30/200** nulls satisfy both, giving:

`p_joint = 0.1542288557`.

Thus even the combined “stable on ZL, then transfers well to IT” path is not statistically unusual under this matched search process.

## 4. Stronger E3 structured-null family

E5 also re-used the frozen 100 E3 lattices that already match the Guidonian row/column capacity **and the histogram of pair-overlap strengths**.

After each structured null was allowed to select its own ZL-stable mapping:

| quantity | result |
|---|---:|
| Guidonian IT mean | **0.833714** |
| structured-null median | **0.839598** |
| structured-null q95 | **0.849770** |
| structured-null max | **0.853090** |
| nulls `>= Guidonian` | **69 / 100** |
| `p_transfer` | **0.693069** |
| joint exceedances | **26 / 100** |
| `p_joint` | **0.267327** |

Under this stronger structural family, the median comparator actually transfers **better** than Guidonian.

This also qualifies the earlier E3-B result. E3-B showed Guidonian strongly outperforming the structured catalog **when every lattice was forced to use the one Guidonian-selected fixed column mapping**. E5 shows that advantage largely disappears when each alternative is allowed its own ZL-selected correspondence.

## 5. Exact Guidonian-pair-geometry alternatives

E3 exhaustively found only three non-Guidonian alternatives sharing the entire labeled 6×6 Guidonian pair-intersection matrix.

E5 gives them the same selection procedure:

| candidate | ZL-selected policy | recurrence | IT mean |
|---|---|---:|---:|
| Guidonian | max | 4/5 | **0.833714** |
| exact alt 0 | max | 4/5 | **0.833714** |
| exact alt 1 | min | **5/5** | **0.843521** |
| exact alt 2 | max | 4/5 | **0.835484** |

All three exact-pair alternatives match or exceed Guidonian under the joint recurrence+transfer criterion. One has a perfect **5/5** recurring ZL map and beats Guidonian by about **0.98 percentage point** on IT.

This strengthens E3's conclusion: the observed success is not identifying the actual Guidonian higher-order lattice.

## 6. What remains real from E and E2

E5 does **not** erase all earlier positive numerical facts.

### E remains a real within-transcription result

In E, Guidonian and each degree-matched null were given equal per-fold freedom to optimize all 720 state mappings and the 20 row assignments on training data. Guidonian had a small but consistent held-out advantage on ZL:

- primary `min`: about +0.97 percentage point over paired-null median;
- sensitivity `max`: about +2.53 percentage points;
- both global Monte-Carlo comparisons were positive.

E5 does not invalidate that comparison.

### E2-B remains an architecture replication

The freely refitted architecture also replicated on IT2a against degree-matched nulls.

What E5 invalidates is the stronger reading of **E2-C's fixed-map effect** as evidence that the specific Guidonian correspondence transfers in a way random external structures generally cannot.

Once the actual ZL selection step is granted to the alternatives, many can do the same.

## 7. Revised evidence chain

The current sequence is best summarized as:

1. **E:** Guidonian topology is somewhat better than ordinary degree-matched random lattices under fully refitted held-out ZL comparison.
2. **E2-A/B:** this broad architecture-level effect is numerically stable and replicates on another transcription.
3. **E2-C:** a post-E recurring Guidonian map prospectively transfers to IT and appears extremely strong against nulls forced to use that same map.
4. **E3:** the full Guidonian lattice is not identified; non-Guidonian lattices with identical pair geometry equal/beat it.
5. **E4:** a Voynich-trained non-musical topology transfers even better, but this is not by itself a fair measure of external Guidonian surprise because it learns Voynich from Voynich.
6. **E5:** after giving random external lattices the same ZL mapping/parser selection opportunity that produced E2-C, the fixed-map transfer ceases to be unusual (`p_transfer≈0.433`; `p_joint≈0.154`).

The strongest surviving object is therefore a **generic six-state dependency / pair-geometry compatibility**, not a specifically Guidonian musical coding result.

## 8. Music-hypothesis interpretation

The user's methodological objection was correct: “Voynich trained on Voynich” is not the right comparator for deciding whether an external medieval-music structure is surprising.

E5 replaces that comparator with the appropriate matched-selection question.

The answer is still negative for music specificity, but for a different and stronger reason:

> Once ordinary non-Guidonian external lattices are allowed the same search→stability-selection→prospective-transfer pipeline, Guidonian's apparent fixed-map success is not exceptional.

This means the **83.4% number remains a real held-out score**, but it is not evidence that becomes surprising specifically because the external structure is Guidonian.

The genuinely interesting remaining fact is narrower:

> Voynich slot10 participates in a stable six-state dependency structure whose low-order geometry happens to be compatible with the Guidonian pair geometry, but many non-musical structures can reproduce the relevant predictive behavior once selection is matched.

## 9. What E5 does not test

E5 does not numerically charge the entire history of deciding to investigate music rather than other domains. It also does not test every possible external six-state formal system in history.

Conversely, slot10 and k=20 were not searched in E5: slot10 is the unique six-state slot in the frozen Zattera inventory, and `20` comes from the externally fixed twenty Guidonian gamut loci.

Therefore E5 is a **within-model selection audit**, not a universal Bayes factor for “music vs all alternatives.”

## 10. Next high-information test

If Issue26 continues, the remaining positive E/E2-A/B effect should be attacked directly with **fully refitted structured nulls** rather than fixed-map structured nulls:

> When every candidate is allowed full 720-map fitting independently on each training fold, does Guidonian still outperform pair-overlap-matched and exact-pair non-Guidonian lattices on held-out ZL and IT?

That would isolate whether *anything beyond generic six-state overlap geometry* remains in the original architecture-level E/E2-B result.

Do not proceed to melody extraction or literal pitch naming before that question is settled.

## 11. First-reveal provenance

- branch: `issue26-music-e5-selection-audit`
- scientific head: `47662450b5a8f7e7fc147b30803c6e787e2bccfd`
- plan-first commit: `9a1f7d60e2506a281331be15cc99bc068d1760de`
- first executable commit: `eac8c7504b2360e967eec66b5898586f434ab45c`
- Actions run: `33365306673`
- job: `99404619460`
- artifact: `9748101247`
- artifact ZIP SHA-256: `81e864fab0e83a3654f19f632c3d296c663fa60a7cc849afa072009e0fa64022`
- raw JSON SHA-256: `929d7f35b4b68999f18f6951b9912c50a69c6810aa95da1120a4f77fac9222fb`
- plan SHA-256: `53a6ac02d26b87bb24fc1d38527ccbc45b930d35e1d38ecd59cc26637fe028d1`
- script SHA-256: `b258b22d195f02f0614aa22ebf22a06ca5ca122772e3c43246562743a61d38af`
- core SHA-256: `3e37c0223497f7008cb9d78ceeab18b34518c0c0b70860528a2017502fc1392d`
- ZL blob SHA-1: `2a4533ab9bdfa85db9bad602d590978953055df1`
- IT2a SHA-256: `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`

The branch remains independent. **No merge to main is authorized by this result.**
