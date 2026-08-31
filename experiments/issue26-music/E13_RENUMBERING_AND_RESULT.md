# Issue #26E13 — administrative renumbering and frozen result record

Status: **POST-REVEAL ADMINISTRATIVE RENUMBER ONLY**

This experiment was preregistered, implemented, and first revealed under the accidental label `E11` on branch `issue26-music-e11-oettingen-dyad-probe`. After reveal, current GitHub inspection showed that the Issue #26 research program already had independent E11 branches (León substitution and an Öttingen token-internal probe) and an E12 Porta branch.

To avoid overwriting or relabeling those independent research lines, the exact revealed dyadic experiment is carried forward administratively as **E13** on branch `issue26-music-e13-oettingen-dyad-probe`.

No hypothesis, population, parser, key space, metric, threshold, code, result, or interpretation was changed by this renumbering. The original branch and original `PLAN_E11.md` / executable remain intact as the audit trail. There is deliberately **no retroactive `PLAN_E13.md`** pretending that E13 was the prereveal label.

## Original chronology

- original preregistration commit: `dd1b8895bfd626375e9ba577a7bce061e0bafd9f`
- original first executable: `a3e6ec81bd2aac03d19d27a968d02b351bfc062a`
- first reveal head: `78e58b48e916b90d52ef87574c1c92202e639444`
- Actions run: `33381601877`
- job: `99454983600`
- artifact: `9753979048`
- raw JSON SHA-256: `09eea98aeb3ad4845f4930e10cb2c230cf5a9b4c8590c87fc960161b40368053`
- artifact ZIP SHA-256: `5ba6a0012bce1cc42cc7782b94671ccc62af101b902f078661a1406a1e51a15a`

## Historical mechanism

Öttingen-Wallerstein's ca.1600 steganographic table uses two successive notes from five solmisation tones to encode one plaintext letter. The HAB transcript fixes first-note rows and second-note columns and has one genuine unused pair (`sol → re`). E13 therefore differs structurally from the token-internal 5×5 Sloane/Öttingen probes: a single Voynich five-state slot supplies one note per token and successive token states are paired into plaintext letters.

## Frozen first-reveal result

Classification: **`NO OETTINGEN PLAINTEXT SIGNAL`**.

Primary `min`, phase 0:

- pooled held-out 4-gram CE: `4.584962500721222 bits/char`;
- medieval-Latin self-baseline: approximately `2.45 bits/char`;
- held-stream shuffle lower-tail p: `.7422577423`;
- illegal historical dyad rate: `0`;
- pooled top-five-character fraction: `.9858545`;
- decoded characters: `10,392`;
- exact CREMMA lexicon hits length >=6: `0`;
- nominal full-key recurrence: `5/5`, slot5 identity mapping.

### Post-reveal tie audit

The nominal `5/5` recurrence is **not evidence of a stable decipherment key**. Multiple candidate keys attained the same training objective: zero illegal dyads and 4-gram CE at the uniform/unseen floor `log2(24) ≈ 4.5849625`. The deterministic lexicographic tie-break therefore repeatedly selected the identity permutation.

The mechanism of collapse is transparent:

- slot5 is overwhelmingly `EMPTY`;
- identity maps `EMPTY → ut`;
- the historical table maps `ut,ut → Q`;
- pooled plaintext is therefore dominated by `q` (about 90%), with `qqqq` frequent and absent from the external Latin comparator.

Phase-1 and parser sensitivities do not rescue the result; they remain non-language-like and fail the frozen readability/order criteria.

## Interpretation

E13 is useful as a structurally different negative control: changing from token-internal two-factor tables to a genuine sequential two-note musical cipher does **not** reveal Latin-like order. The apparent 5/5 key recurrence is a deterministic tie artifact and must not be promoted as a residual music signal.

This branch remains research-only and must not be merged to `main` without explicit user authorization.
