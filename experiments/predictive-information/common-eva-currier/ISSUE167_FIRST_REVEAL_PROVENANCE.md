# Issue #167 — sparse Currier outcome first reveal provenance

Date: 2026-09-07
Status: **COMPLETE — FROZEN CLASSIFICATION**

## Frozen classification

> **`CURRIER OUTCOME BIAS SPARSE SUPPORT: K=16 SUFFICES`**

The preregistered hierarchy was `K={1,2,4,8,16}`. Every tested K produced a useful sparse gain in all four reading×Currier cells. K=1,2,4 retained a robust full-over-sparse residual in all four cells. K=8 removed that residual in both Currier-A cells but not in either Currier-B cell. K=16 was the first rung with no robust full-over-sparse residual in any cell.

No retention-percentage rescue threshold or post-reveal K/model change was used.

## Frozen chronology and authority

Issue #167 score-free Gate0:

- Gate0 PR: #169
- Gate0 merge: `bb56158e907d7253758cc5a0d8bc4dfa2606f1c7`
- plan blob: `d5b79c64ffc8297672f2de39f6478156ee3442b7`
- Gate0 script blob: `5b3aac1a03ef087340f6e0ffd241a4909476c815`
- Gate0 provenance blob: `f76feea360417e52261bf69dc1425cfceb58963c`
- Gate0 result SHA-256: `ff5dfe546333f6e454bb5a36907f88f30ade2ecb36354f20064879e16276484c`
- Gate0 run: `34079560066`

Scientific first reveal:

- scorer-only commit: `7c3d29e48ecb5026b11b065c7816ac4bb0d447a2`
- frozen scorer git blob: `5e67cecc312b431791c6623d1077ac46533fce0a`
- workflow added only after scorer freeze
- exact workflow head: `148faf934a917239d2059a8215de48a799b89b48`
- workflow run: `34079999067`
- workflow conclusion: `success`
- artifact ID: `10003436653`
- artifact name: `issue167-sparse-currier-first-reveal-148faf934a917239d2059a8215de48a799b89b48`
- artifact ZIP digest: `sha256:f7b698cc44c914e54baa83228823bbb67d6b1b72b759974177e3795baa91a41b`
- result JSON SHA-256: `a532136b821d3c42f7b340729961da438f1f7cbd9bf20afb73408261d8d7befd`

The workflow reproduced the merged Gate0, exact #161 scorer/provenance authority, exact sources, frozen training-only top-K selections, and foldwise #161 `G_outcome` values before accepting the scientific result. The workflow then recomputed the classification from the result JSON and passed the frozen contract.

## Cell results

All values below are mean held-out bits/token across the five fixed outer physical-leaf folds.

| reading / Currier | K | mean `G_sparse` | positive `G_sparse` folds | useful | mean `G_missing` | positive `G_missing` folds | robust missing residual |
|---|---:|---:|---:|---|---:|---:|---|
| ZL3b / A | 1 | +0.0146090081 | 4/5 | yes | +0.0537636463 | 4/5 | yes |
| ZL3b / A | 2 | +0.0348607643 | 5/5 | yes | +0.0335118900 | 4/5 | yes |
| ZL3b / A | 4 | +0.0620863508 | 5/5 | yes | +0.0062863035 | 4/5 | yes |
| ZL3b / A | 8 | +0.0647880477 | 4/5 | yes | +0.0035846066 | 3/5 | no |
| ZL3b / A | 16 | +0.0692249547 | 4/5 | yes | -0.0008523004 | 1/5 | no |
| ZL3b / B | 1 | +0.0177872148 | 4/5 | yes | +0.0761896236 | 5/5 | yes |
| ZL3b / B | 2 | +0.0327834896 | 5/5 | yes | +0.0611933487 | 5/5 | yes |
| ZL3b / B | 4 | +0.0485968262 | 5/5 | yes | +0.0453800122 | 5/5 | yes |
| ZL3b / B | 8 | +0.0788258820 | 5/5 | yes | +0.0151509564 | 4/5 | yes |
| ZL3b / B | 16 | +0.0930699022 | 5/5 | yes | +0.0009069362 | 3/5 | no |
| IT2a / A | 1 | +0.0171510148 | 4/5 | yes | +0.0572228545 | 4/5 | yes |
| IT2a / A | 2 | +0.0373357748 | 5/5 | yes | +0.0370380945 | 4/5 | yes |
| IT2a / A | 4 | +0.0646259716 | 5/5 | yes | +0.0097478977 | 4/5 | yes |
| IT2a / A | 8 | +0.0711824649 | 4/5 | yes | +0.0031914044 | 3/5 | no |
| IT2a / A | 16 | +0.0745157397 | 4/5 | yes | -0.0001418704 | 2/5 | no |
| IT2a / B | 1 | +0.0189547762 | 4/5 | yes | +0.0763999484 | 5/5 | yes |
| IT2a / B | 2 | +0.0352298739 | 5/5 | yes | +0.0601248508 | 5/5 | yes |
| IT2a / B | 4 | +0.0557600163 | 5/5 | yes | +0.0395947084 | 5/5 | yes |
| IT2a / B | 8 | +0.0816619815 | 5/5 | yes | +0.0136927432 | 4/5 | yes |
| IT2a / B | 16 | +0.0952106091 | 5/5 | yes | +0.0001441156 | 3/5 | no |

The reproduced full #161 outcome gains are:

- ZL3b / A: `+0.0683726543 bit/token`
- ZL3b / B: `+0.0939768384 bit/token`
- IT2a / A: `+0.0743738693 bit/token`
- IT2a / B: `+0.0953547247 bit/token`

Thus K=16 closely reaches the frozen full outcome factor in every cell, while K=8 remains detectably incomplete specifically for Currier B under the preregistered 4/5 criterion.

## Structural interpretation

Issue #167 rules out an extremely sparse explanation of the Currier next-initial bias under the frozen ranking family. The predictive Currier contrast is not carried by only one, two, or four exceptional next-initial outcomes. Eight outcomes capture enough for Currier A, but Currier B still retains a robust full-over-sparse residual in both independent transcription readings. Sixteen training-ranked outcomes are needed before the full 32-outcome factor no longer has a robust held-out advantage.

This is still a substantial compression relative to a fully free Currier×previous-terminal table: the accepted model remains one shared terminal→initial base table plus a context-invariant Currier outcome factor. Issue #167 only says that this global outcome factor has moderately broad, rather than ultra-sparse, support.

The frozen top outcomes are common-EVA transcription atoms. Their appearance in the ranking is not a semantic claim and does not identify words, plaintext, language/cipher family, authorship, historical mechanism/direction, artificiality/hoax, or decipherment.

## Consequence

The accepted compact edge description is now:

> **one shared common-EVA terminal→initial base table + a Currier-specific context-invariant next-initial bias whose training-ranked top 16 outcomes suffice prospectively.**

A later descriptive issue may characterize stability/sign/patterns within the frozen selected outcomes, but it must not rerank them from held-out target scores or attach semantics from the predictive result.

Refs #88 #158 #161 #164 #165 #167 #169 #170.
