# Issue #84 Phase B — cipher-family map for the Voynich inter-token regime

Status: **COMPLETE — AUTHORITATIVE FIRST REVEAL ARCHIVED**

Date: 2026-09-06

Parent: Issue #84

Preregistered authority:

- `PLAN_B.md` — frozen at `b991b948f8bb4d5041ed2e6d348eef4d91feca84` before the Phase-B executable existed and before any candidate score was produced;
- `AMENDMENT_B0.md` — notation-only `S1 → SUB1` clarification;
- `AMENDMENT_B1.md` — prereveal correction of the published Naibbe table cardinality from an implementation-only 26-letter assumption to the pinned 23-effective-letter interface; no candidate score existed before this correction;
- score-free full-generation preflight run `34011756256`, head `dba354675defb5e2cd3f0fa99c8392d38fd992ea`;
- authoritative first-reveal run `34011823328`, scientific head `51891bd2a992dd90b9ad69d1f6a4f64c216fb3e8`;
- first-reveal artifact ID `9982705587`, ZIP SHA-256 `0264ccd299b6e95a1b9edf12c48ab8a7a026edebfa4b83834e14ce997b8e32a7`;
- full result JSON SHA-256 `de8ac6882f52000139e3989c1672b86d41946e238ad56ae8053516f754d7a431`;
- compact summary SHA-256 `e0b9b4d1d5e197b4fc0bd40682e758d9db2889d73764b2c4475b8a4f51a04fe4`.

The exact first-reveal result and provenance files are committed under `first-reveal-b/`.

---

## 1. Frozen question

> Which bounded reversible cipher-operation families, applied to the already frozen CREMMA medieval-Latin source panel, can move ordinary-language token sequences into the same inter-token regime as seven independent Voynich readings?

This was a mechanism-family screen. It was not a decipherment attempt and it did not permit target-driven parameter tuning, post-hoc candidate addition or post-hoc composition of partial mechanisms.

The three preregistered responsibilities were imported unchanged from Phase A:

1. adjacent-token corrected mutual information, `MI1`;
2. exact-repeat excess at distance `1–2`, `z1_2`;
3. exact-repeat excess at distance `21–40`, `z21_40`.

A candidate counted as a `VOYNICH INTER-TOKEN REGIME HIT` only if its frozen center lay inside the seven-reading Voynich interval for **all three** components. No weighted omnibus score could compensate for a failed responsibility.

Exact empirical target intervals from the frozen Phase-A JSON:

| responsibility | seven-reading Voynich interval |
|---|---:|
| `MI1` | `0.052873 … 0.110956` bits |
| `z1_2` | `+2.79637 … +8.45583` |
| `z21_40` | `−0.77007 … +3.43462` |

The Phase-A far bins were not reused as hard criteria because Phase A had already shown that they were confounded by document length.

---

## 2. Input and implementation controls

Plaintext authority was exactly the same four equal-weight CREMMA manuscripts used by Phase62/64, at `HTR-United/CREMMA-Medieval-LAT@292525969ad98380b398e6606a9c2a36d51913ae`.

The parsed Phase-B source contained:

- 241 source items;
- 18,178 tokens;
- 5,767 token types in the P0 Latin anchor;
- 278 source units.

The Phase-A Latin anchor replay passed before candidate scoring:

- `MI1 = 0.3989188020`;
- `z1_2 = −3.484170419`;
- `z21_40 = +19.64352602`.

Every in-house realization passed exact decoder closure **before** any candidate score was accepted. `SUB1` and `VERBOSE2` also preserved the frozen token-equality relation sample as required.

The published Naibbe challenger was replayed at `greshko/naibbe-cipher@f2675ec5dd275268bc64dd48ea64fc0e0e9827a2` with the same Phase64B projection, defaults and seeds. Its concrete published table contains the expected `6 × 3 × 23 = 414` reachable mapping cells.

---

## 3. Frozen candidate result

For stochastic in-house candidates and Naibbe, the center below is the preregistered componentwise median of five fixed realizations. Deterministic candidates have one realization.

| candidate | `MI1` | `z1_2` | `z21_40` | responsibilities passed | frozen classification |
|---|---:|---:|---:|---|---|
| `SUB1` monoalphabetic | 0.39936 | −3.364 | +15.167 | 0/3 | `NO INTER-TOKEN HIT` |
| `H2` homophonic ×2 | 0.14784 | −3.062 | +8.239 | 0/3 | `NO INTER-TOKEN HIT` |
| `H4` homophonic ×4 | **0.05919** | −2.044 | +5.906 | MI only | `PARTIAL INTER-TOKEN HIT (1/3)` |
| `H8` homophonic ×8 | 0.02028 | −1.336 | +5.311 | 0/3 | `NO INTER-TOKEN HIT` |
| `N256-1` deterministic nomenclator | 0.40079 | −4.409 | +16.622 | 0/3 | `NO INTER-TOKEN HIT` |
| `N256-4` 4-way nomenclator | **0.10804** | +0.358 | +14.737 | MI only | `PARTIAL INTER-TOKEN HIT (1/3)` |
| `NULL10` | 0.24622 | −2.612 | +14.186 | 0/3 | `NO INTER-TOKEN HIT` |
| `NULL20` | 0.16344 | −2.334 | +10.643 | 0/3 | `NO INTER-TOKEN HIT` |
| `NULL30` | 0.12318 | −3.321 | +8.600 | 0/3 | `NO INTER-TOKEN HIT` |
| `TRANS-LINE` | 0.02862 | **+7.389** | +22.311 | short-repeat only | `PARTIAL INTER-TOKEN HIT (1/3)` |
| `VERBOSE2` | 0.39980 | −3.525 | +18.647 | 0/3 | `NO INTER-TOKEN HIT` |
| published `NAIBBE` | 0.04452 | −5.031 | **+2.389** | mid-range only | `PARTIAL INTER-TOKEN HIT (1/3)` |

**Frozen across-candidate result:**

> `0` full hits; `0` target-independent in-house hits.

No tested operation family reproduces the complete three-component Voynich inter-token regime from this Latin prose source.

---

## 4. Replicate robustness

The partial classifications are not produced by one fortunate seed.

### H4

All five realizations place `MI1` inside the Voynich interval (`0.05899 … 0.06091`). All five retain the wrong immediate-repeat direction (`z1_2 = −2.58 … −1.29`) and all five retain too much 21–40 recurrence (`+4.82 … +6.42`).

### N256-4

All five realizations place `MI1` inside the target interval (`0.10571 … 0.10973`). None produces the required positive immediate-repeat excess (`z1_2 = −0.46 … +0.84`), and every realization retains a large mid-range excess (`+12.55 … +19.15`).

### TRANS-LINE

Four of five realizations place `z1_2` inside the Voynich interval; one overshoots at `+9.23`. Every realization drives `MI1` below the Voynich interval (`0.02547 … 0.03408`) and leaves extremely strong 21–40 recurrence (`+17.30 … +23.47`).

### Naibbe

Four of five primary respaced realizations place `z21_40` inside the Voynich interval; one is slightly high at `+4.12`. All five have `MI1` below the Voynich lower bound (`0.03756 … 0.05184`) and all five show a strong **deficit**, not excess, of immediate exact repetition (`z1_2 = −6.54 … −3.47`).

The non-promoting raw-token Naibbe sensitivity gives the same qualitative result: center `MI1 = 0.05088`, `z1_2 = −5.397`, `z21_40 = +2.185`; classification remains `PARTIAL INTER-TOKEN HIT (1/3)`.

Thus Naibbe respacing is not what causes its Phase-B failure.

---

## 5. What the family map says

### 5.1 Relabeling and within-token verbosity do not solve a token-relation problem

`SUB1` and `VERBOSE2` remain effectively Latin-like on the primary inter-token responsibilities. That is the expected invariance result: changing symbols or expanding each source unit inside a preserved token cannot erase the source token-relation geometry.

The deterministic one-code-per-word nomenclator is likewise ineffective because it preserves token identity relations.

### 5.2 Homophony can tune adjacent MI into the Voynich range, but it does not create the Voynich recurrence geometry

The homophonic series shows a clear attenuation of adjacent dependence:

- H2: `MI1 = 0.148`;
- H4: `0.059` — inside Voynich;
- H8: `0.020` — below Voynich.

But this is not sufficient. H4 still has negative immediate-repeat excess and retains excessive 21–40 recurrence. Increasing random homophony eventually destroys too much dependence without generating the positive immediate repetition that distinguishes Voynich from the Phase-A natural-language panel.

The same separation appears in `N256-4`: its adjacent MI enters the Voynich interval while its mid-range burstiness remains strongly language-like.

### 5.3 Null insertion attenuates dependence but preserves the wrong recurrence regime

Increasing null insertion from 10% to 30% progressively lowers `MI1` (`0.246 → 0.163 → 0.123`) and mid-range recurrence (`14.19 → 10.64 → 8.60`), but none of the frozen rates reaches the three-component target and all retain negative immediate-repeat excess.

This rejects the tested null-insertion representatives as standalone explanations; it does not reject every possible null system.

### 5.4 Line-local transposition can create immediate-repeat excess, but at the wrong cost

`TRANS-LINE` is the only tested target-independent candidate whose center reproduces the Voynich positive `z1_2` responsibility. It does so while driving adjacent MI **below** Voynich and preserving very strong 21–40 recurrence.

This matters because it demonstrates experimentally that the three target components are not redundant. One can manufacture the immediate-repeat signature without entering the full Voynich regime.

### 5.5 Published Naibbe suppresses ordinary mid-range recurrence but misses the local signature in the opposite direction

Naibbe is the only tested candidate whose center reproduces the Voynich 21–40 recurrence interval. Its adjacent MI is also numerically near, but below, the lower Voynich boundary. The decisive failure is immediate exact repetition: Naibbe produces a strong negative `z1_2`, whereas every Voynich reading has a positive value.

This sharpens the earlier Naibbe interpretation. Its published architecture can produce a low-dependence / low-mid-range surface and its target-aware codebook can reproduce R1, but the complete mechanism still does not reproduce the manuscript's local token-reuse regime.

Do **not** repair Naibbe from this result by adding a local repetition rule. Such a composition was not preregistered for Phase B.

---

## 6. Scientific conclusion

The strongest allowed Phase-B statement is:

> **On frozen CREMMA medieval-Latin prose, none of the preregistered common reversible operation representatives — monoalphabetic substitution, bounded homophony, bounded nomenclators, 10–30% null insertion, line-local transposition, minimal verbose recoding, or exact published Naibbe — reproduces the full transcription-robust Voynich inter-token regime. Different operations can reproduce individual components, but the Voynich conjunction remains unaccounted for.**

This is stronger than the Phase-A observation that ordinary language itself lies outside the regime. It shows that several common ways of encrypting or recoding such language do not automatically produce the missing conjunction.

It is not a proof that the manuscript is not encrypted language. Phase B tested frozen representatives, not the mathematical universe of ciphers. In particular, it has not yet tested whether a non-prose source genre already has different recurrence geometry before encryption.

---

## 7. Consequence for the hypothesis tree

The result changes the priority of the next test.

The observed responsibilities are separable:

- random homophony / homophonic nomenclators can supply Voynich-scale **adjacent dependence**;
- line-local reordering can supply **positive immediate exact repetition**;
- published Naibbe can supply **suppressed 21–40 recurrence**;
- no frozen single family supplies all three.

Because Phase B prohibited post-hoc composition, the correct next step is **not** to combine these partial mechanisms after seeing their scores.

The next high-information discriminator is Issue #84 **Phase C genre control**:

> Do enumerative, recipe, herbal, calendar, liturgical or account-like source texts already depart from ordinary prose in the specific `z1_2` / `z21_40` directions seen in Voynich?

If Phase C finds no such source regime, the evidence against ordinary meaningful-text-plus-common-transform explanations materially strengthens. If a source genre does enter or approach the regime, only then is a separately preregistered source×transform composition warranted.

In parallel, Issue #81's independently motivated soft near-family memory remains live as a **generative** explanation for local recurrence. It must continue under its own training-only selection rules and must not be retrofitted as a repair to Phase-B candidates.

---

## 8. Claim boundary

The Voynich Manuscript is not deciphered.

Phase B identifies which preregistered operation representatives can and cannot reproduce a narrow, transcription-robust token-relation regime. It does not identify plaintext, a historical cipher, a key, semantics, token boundaries as linguistic words, or authorship.
