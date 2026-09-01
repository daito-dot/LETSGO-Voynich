# Issue #68 — target/preflight implementation notes

Status: **FROZEN BEFORE PREFLIGHT EXECUTABLE AND BEFORE ANY NEW REAL-CANDIDATE R1 GRAPH**

Authority: `experiments/joint-constraint-tournament/PLAN_A.md` on main commit `b2298d7fe251070dacd21852ae3b5a1dac95fe65`.

This note resolves mechanical implementation details only. It does not change any R1/R2/R3/R4/R5 threshold, candidate family, target reading, null size, or classification gate.

## 1. Naibbe primary realization for R4

`PLAN_A.md` explicitly fixes Naibbe R1 to historical **realization 0** for each of the four frozen CREMMA manuscripts, but R4 names only the published primary 3%-space-removal view without restating the realization index.

To prevent seed selection from decoder outcome, R4 primary uses the **same historical realization 0** per manuscript:

`seed = 6480000 + 100 * manuscript_index + 0`

with manuscript order inherited unchanged from `phase62b_n0.PRIMARY_MANUSCRIPTS` / Phase64B:

1. BIS193 → `6480000`
2. CLM13027 → `6480100`
3. Mazarine915 → `6480200`
4. UBL758 → `6480300`

The remaining historical realizations 1–4 may be reported only as non-promoting decoder sensitivities. They cannot rescue a realization-0 R4 failure.

## 2. A1 primary realization

A1 R1 primary remains the first member (`rep=0`) of the exact historical deterministic Phase62 seed family:

`6190000 + fold*100000 + int(entry_strength*10)*1000 + int(local_family_p*100)*10 + rep`

Thus primary seeds are prospectively fixed to:

- fold 0 → `6195200`
- fold 1 → `6295200`
- fold 2 → `6395300`
- fold 3 → `6495300`
- fold 4 → `6595200`

No realization may be substituted after parser coverage or R1 scoring.

## 3. Direct parser coverage

Coverage is computed without any pairwise association statistic:

- visible candidate token = every non-empty emitted surface token in the frozen primary realization;
- accepted token = `issue26e_core.SlotParser.pick(token, "min")` returns a parse without rewriting the token;
- no case-specific remapping, transliteration, token split/merge, or selected subset is allowed;
- overall candidate coverage is `accepted / visible` across the complete frozen primary candidate corpus;
- fold/manuscript support is reported separately.

Coverage `< 0.60` is the already preregistered R1 representation failure.

## 4. Naibbe normalized decoder target

For each source line, the primary R4 truth string is produced with the exact preexisting Phase64B interface:

1. `naibbe_v2.clean_line(source_line)`;
2. `phase64b_naibbe.project_effective_plaintext(...)`.

This is compared after removing only the public decoder's display syntax (spaces used to mark decoded compound pieces and `*` best-split marker). No original source word boundaries, punctuation, or pre-normalization `W/J/K` distinction is supplied or scored as recoverable.

## 5. Published decoder ambiguity semantics

R4 calls the pinned public `decrypt_naibbe_token(..., basic=True, compound=True)` token by token.

Its returned notation is interpreted mechanically as an expression language:

- `(...)` = grouping;
- `|` = alternative;
- adjacent letters / displayed compound-space = concatenation in the normalized letter stream;
- `*` = display marker only;
- `[?]` = unresolved and therefore no fully resolved candidate for that token.

Primary unique closure for a line requires every ciphertext token to resolve to exactly one normalized candidate string and their concatenation to equal the frozen truth string. Multiple distinct candidates, `[?]`, or a unique wrong result fail that line.

Truth-contained-among-alternatives is computed and reported separately but cannot promote R4.

## 6. Preflight target firewall

Preflight may construct the frozen candidate outputs because representation coverage and source-side R4 are explicitly allowed by `PLAN_A.md`.

Preflight MUST NOT call, directly or indirectly on a real candidate corpus:

- pair-code / pair-count functions;
- real 66-edge Q computation;
- candidate reference/test residual Z transformation;
- residual energy;
- residual reliability;
- correlation/sign agreement against ZL3b/IT2a;
- candidate R1 p-values;
- joint/global tournament classification.

R1 mathematical code may be self-tested only on synthetic arrays until the explicit first-reveal event.
