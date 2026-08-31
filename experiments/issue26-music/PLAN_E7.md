# Issue #26E7 — prospective Guidonian dynamic prediction test

Status: **FROZEN BEFORE E7 EXECUTABLE / SEQUENCE REVEAL**

Issue: #26

Base main: `21ca553d0dc7f5e203465d08ae606b4c43305817`

## Why E7 exists

E/E2 found a sequence-blind static compatibility between the Voynich Zattera slot10 six-state factor and the historical Guidonian 20×6 admissibility lattice. E3–E6 showed that this static compatibility is not sufficient to identify music: structurally matched non-musical lattices can reproduce much of it.

A stronger test should therefore **not manufacture more six-state null lattices**. Instead it should ask the historical Guidonian hypothesis to predict a property of Voynich that was not used to obtain the static fit.

E7 freezes the E/E2 static mapping procedure and then reveals **token order for the first time**. The new prediction is derived from historical hexachord theory, not from Voynich sequence statistics.

## Historical prediction frozen before sequence scoring

The existing 42 allowed cells of `issue26e_core.GUIDO` decompose exactly into seven overlapping six-note hexachords. In row/vox coordinates the seven starts are:

`[0, 3, 6, 7, 10, 13, 14]`

and every hexachord contains, in order,

`ut re mi fa sol la`.

This yields exactly `7 × 6 = 42` unique `(row, vox)` cells, i.e. the full existing Guidonian lattice and no added cells.

For pitch identity, freeze the seven hexachord start semitones relative to low Gamma/G as:

`[0, 5, 10, 12, 17, 22, 24]`

with voice offsets:

`ut,re,mi,fa,sol,la = [0,2,4,5,7,9]`.

This is important because the existing 20-row static lattice collapses the two B signs into one row at two octave positions. Historical theory explicitly distinguishes `b-fa` and square-B/`mi` as different signs/sounds and therefore **not a mutation locus**. E7 accordingly uses cell-level semitone pitch identity, not row equality, for mutation.

Historical source basis:

- 13th-century theory text in the Thesaurus Musicarum Latinarum: `Mutatio ... sub eodem signo et in eodem sono`; mutation requires at least two voces at that place, and explicitly excludes `b fa` / square-B `mi` because they are different signs and sounds: https://chmtl.indiana.edu/tml/13th/ARITRA_TEXT.html
- Historical hexachord/gamut exposition showing seven hexachords and the overlapping `ut re mi fa sol la` structure: https://en.wikisource.org/wiki/A_Dictionary_of_Music_and_Musicians/Hexachord

The primary dynamic consequence is therefore:

> If successive Voynich tokens are genuinely instantiating the fitted Guidonian cells, a change from one inferred hexachord to another should preferentially occur at a boundary where one endpoint pitch is shared by both hexachords, so that a historically legal same-pitch mutation is available.

This consequence was not used by E/E2/E3/E4/E5/E6.

## Frozen data and static representation

Primary transcription: frozen ZL3b, Git blob SHA-1 `2a4533ab9bdfa85db9bad602d590978953055df1`.

Transcription robustness sensitivity: IT2a SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`. IT2a is the same manuscript/content, so it is **not an independent content replication**.

Use the existing `issue26e_core.py` unchanged:

- Zattera 12-slot parser;
- slot10 states `EMPTY,d,l,r,m,n`;
- residual one-hot morphology from slots `0..9,11`;
- deterministic sequence-blind k=20 clustering on unique training token types;
- five frozen physical-leaf folds;
- `fit_mapping`: all `6! = 720` state↔vox permutations plus optimal cluster↔row assignment on training occurrences only.

Primary parser: `min`.

Predeclared sensitivity: `max`. A positive `max` result cannot rescue a failed primary `min` result; this avoids retroactively promoting the parser that looked strongest in E6.

## Static-to-dynamic firewall

For every fold and parser:

1. fit k=20 and the complete Guidonian static mapping on training leaves only;
2. training uses token identity/morphology and occurrence counts, but **never adjacency, token order, line transitions, hexachord-run statistics, or mutation statistics**;
3. freeze `state_to_vox` and `cluster_to_row`;
4. only then map tokens in held-out leaves into `(row, vox)` cells and inspect their original within-line order.

A held-out token is **dynamically admitted** only when its fitted `(row, vox)` is an allowed Guidonian cell. Every admitted cell belongs to exactly one of the seven frozen hexachords and has one frozen absolute semitone pitch.

Do not bridge over an unparsed or statically disallowed token. Dynamic sequences are maximal contiguous runs of admitted tokens within one original transcription line. Only runs of length >=2 contribute adjacent transitions.

No transition crosses a line or paragraph boundary.

## Frozen dynamic metrics

For adjacent admitted cells `a,b` with inferred hexachords `H_a,H_b` and pitches `p_a,p_b`:

### D1 — overall Guidonian dynamic compatibility

A transition is compatible if either:

1. `H_a == H_b` (remain in the same hexachord), or
2. `H_a != H_b` and at least one endpoint pitch is present in both hexachords:
   - `p_a ∈ pitches(H_a) ∩ pitches(H_b)`, or
   - `p_b ∈ pitches(H_a) ∩ pitches(H_b)`.

Condition 2 means that a same-pitch mutation can occur on one of the two boundary notes.

Report compatible transitions / all admitted adjacent transitions.

### D2 — mutation-specific legality

Condition only on observed adjacent transitions with `H_a != H_b`.

Report the fraction for which condition 2 above holds.

This is the more music-specific metric. Merely having local category persistence can improve D1 but cannot by itself satisfy D2.

### Diagnostics, not gates

Also report:

- same-hexachord transition fraction;
- number/rate of hexachord switches;
- counts of invalid switches between non-overlapping hexachords;
- counts where row equality would falsely suggest mutation but cell-level pitch identity correctly rejects `b-fa` versus square-B/`mi`;
- transition and switch sample sizes per fold.

## Order-destruction null

The null does **not** create alternative six-state systems.

For each held-out fold it keeps the exact fitted Guidonian cells, exact admitted-token inventory, exact run lengths, and exact static E/E2 mapping, but independently randomizes the order of cells **within each admitted run**.

Thus the null asks only:

> Does the real Voynich order arrange the already-fitted Guidonian cells more coherently than the same cells in an order that carries no sequential information?

Use `N_SHUFFLES = 5000`, deterministic SHA-256-derived seeds fixed by dataset/parser/fold/replicate.

For D1 use a one-sided upper-tail empirical p-value:

`p_D1 = (1 + #{null >= observed - EPS}) / 5001`.

For D2 use the same upper-tail formula, aggregating valid-switch counts over all held-out folds per replicate before taking the ratio. Replicates with zero switches are impossible to score and must be reported; if any occur, exclude them only from D2 denominator and report how many.

For each metric report null median, q95, observed-minus-median, global p, and fold-level effect directions.

## Replay firewall

Before interpreting E7, the sequence-blind Guidonian held-out accuracy must replay the already revealed architecture-level means within `1e-12`:

- ZL min `0.8509664380470466`
- ZL max `0.8439032769036159`
- IT min `0.8512154779726009`
- IT max `0.8404723923113318`

If replay fails, E7 is invalid and no dynamic result is interpreted.

## Frozen primary classification

Primary classification uses **ZL/min only** for hypothesis status; folds are aggregated after each fold-specific mapping is frozen.

### `GUIDONIAN STATIC FIT PREDICTS NEW DYNAMICS`

Only if all hold:

1. replay firewall passes;
2. at least 500 admitted adjacent transitions and at least 100 observed hexachord switches exist in aggregate;
3. D1 observed > null median and `p_D1 <= 0.05`;
4. D2 observed > null median and `p_D2 <= 0.05`;
5. D1 effect is positive in at least 4/5 folds;
6. D2 effect is positive in at least 3/5 folds having >=10 observed switches.

### `SEQUENCE CLUSTERING ONLY / NO MUTATION-SPECIFIC SUPPORT`

If D1 passes its global/fold gates but D2 fails.

This outcome would show that the fitted categories cluster locally in text but would **not** support Guidonian mutation dynamics.

### `MUTATION-LOCAL SIGNAL ONLY`

If D2 passes but D1 fails. This is interesting but insufficient for the full dynamic claim.

### `STATIC COMPATIBILITY DOES NOT PREDICT GUIDONIAN DYNAMICS`

If neither D1 nor D2 passes, or if sample-size gates fail despite a valid replay.

## Interpretation boundary

A positive E7 would be materially stronger than another static 20×6 fit because the mapping is learned sequence-blind and then predicts an unused historical constraint on held-out token order.

It would still **not** decode the manuscript or establish that tokens literally denote pitches/voces. A positive result would require follow-up against real musical and non-musical sequential controls.

A negative E7 would substantially weaken the historical Guidonian interpretation: the static resemblance would not predict the dynamic behavior that the musical system itself requires.

## Chronology and branch policy

This plan must be committed before `phaseE7_guidonian_sequence.py` exists and before any E7 sequence score is computed.

Work remains on `issue26-music-e7-guidonian-sequence` / draft PR. Do not merge to `main` without explicit user authorization.
