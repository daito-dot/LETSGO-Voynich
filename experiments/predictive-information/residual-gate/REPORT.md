# Issue #118 — flexible sequence residual beyond corrected B3

Date: 2026-09-06
Status: **COMPLETE PRIMARY FIRST REVEAL — LOCALIZATION REQUIRED**
Parent: Issue #88

## Question

After the corrected B3 non-latent predictive core is fixed, does a flexible byte-sequence expert contribute reproducible information specifically because it carries context across visible-space production boundaries, rather than merely because it supplies a different token-emission model?

## Design

The same frozen byte n-gram family is introduced in two matched forms:

- `RESET`: byte history resets before every visible token;
- `CONTINUOUS`: byte history carries across visible-space tokens and resets only at a physical-leaf boundary.

Each is independently mixed with the same corrected B3 token probability:

`p_mix = (1-w) p_B3 + w p_byte`.

Byte `(k, alpha)` and mixture `w` are selected only by inner held-out literal-token likelihood. The untouched outer physical-leaf fold is scored once. The primary residual is:

`G_context = bits(MIX_RESET) - bits(MIX_CONT)`.

The frozen pass rule is mean `G_context > 0` and positive in at least 4/5 outer folds.

## Authority

- scientific head: `8311c429e33b292e91582a349934705383335c68`
- workflow run: `34026324504`
- artifact: `9987190901`
- artifact digest: `sha256:45620aeff80ded52aeffd5395ebf1042674761929631ddfe902f95fcad0e957f`
- result JSON SHA-256: `0aa224f64f4495dfba3b6433730f42fa553d998ac8d72ee682a8313f4664ce59`.

The embedded corrected-core authority reproduced exactly on the first-reveal runner: raw and normalized SHA-256 both equal the merged authority `0d7f311dac17f5736f8191b8ea38cf5f2eac9b7391150a986204772da181ae27`.

## Result

Frozen classification:

> **`ROBUST FLEXIBLE SEQUENCE RESIDUAL EXISTS — LOCALIZATION REQUIRED`**

### Primary residual

`G_context` fold values, bit/token:

| Fold | `G_context` |
|---:|---:|
| 0 | +0.0349457 |
| 1 | +0.0232139 |
| 2 | +0.0093004 |
| 3 | +0.0108658 |
| 4 | +0.0109406 |

- mean: **+0.0178533 bit/token**
- positive folds: **5/5**
- frozen pass: **PASS**.

Thus, after allowing RESET and CONTINUOUS byte experts to complement B3 separately, carrying byte context across visible-space boundaries still supplies a small but reproducible held-out advantage.

### Any flexible complement beyond B3

`G_any = bits(B3) - bits(MIX_CONT)`:

- mean: **+0.0306054 bit/token**
- positive folds: **5/5**.

Mean code lengths:

- B3: `9.51726884 bits/token`
- MIX_RESET: `9.50451671`
- MIX_CONT: `9.48666342`.

The matched RESET complement therefore accounts for about `0.01275 bit/token` of the total continuous-expert improvement on average, while the cross-boundary component measured by the frozen contrast contributes `0.01785 bit/token`.

## Selected mixture strengths

| Fold | RESET `(k,alpha,w)` | CONT `(k,alpha,w)` |
|---:|---|---|
| 0 | `(3,.01,.02)` | `(2,.01,.08)` |
| 1 | `(3,.01,.01)` | `(2,.01,.08)` |
| 2 | `(2,.01,.04)` | `(2,.01,.09)` |
| 3 | `(2,.01,.04)` | `(2,.01,.08)` |
| 4 | `(2,.01,.04)` | `(2,.01,.09)` |

All Issue-#118 byte selections coincide with the frozen Phase-1 byte selections. CONT consistently receives a larger inner-selected mixture weight than RESET.

The raw byte experts themselves are substantially worse than B3 in absolute code length; the result therefore does not arise because a byte model simply replaces the token grammar. Their value is as a low-weight complementary expert.

## Scale of the result

The residual is statistically/reproducibly positive under the frozen fold rule, but information-light in absolute terms:

- B3 is about `9.52 bit/token`;
- cross-boundary residual is about `0.0179 bit/token`, roughly `0.19%` of that code length;
- it is also much smaller than the previously established LOCAL and longer-history gains.

Therefore the result should not be narrated as evidence for a large hidden information channel. It establishes only that the tested non-latent B3 summaries have not exhausted all cross-boundary surface predictability.

## Scientific interpretation

The supported statement is:

> A small, stable component of literal surface prediction remains after corrected B3 and after matching out byte-level token-emission complement; this component depends on carrying short byte context across visible-space production boundaries.

This is compatible with several mechanisms, including incomplete observable-history specification, Currier/regime-dependent parameters, boundary-adjacent morphotactics, or a small unobserved state. The current test does not distinguish them.

## Program consequence

Issue #88's latent-state licensing rule is **not yet fully satisfied**. This first residual gate licenses the next localization step, not direct semantic/latent interpretation.

Freeze localization controls against, at minimum:

1. Currier A/B or other already-authorized observable regime dependence;
2. already-defined paragraph-entry/body and line-position states;
3. support/emission artifacts under the matched expert design;
4. where possible, independent representation/transcription behavior.

Only a residual that survives those observable/support controls should motivate a prospectively frozen latent-state challenger.

## Firewall

This result does not establish:

- natural-language syntax or wordhood;
- semantics or plaintext;
- a cipher family or key;
- authorship or historical method;
- artificial/hoax generation;
- a latent state, let alone a semantic latent state;
- an entropy bound.
