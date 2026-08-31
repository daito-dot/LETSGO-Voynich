# Issue #26 H4 — historical music-cipher candidate frontier

Status: **LIVING LITERATURE / EXPLORATION BOUNDARY**

## Purpose

E8-A/E8-A2 tested Nicholas Philip (1436) confirmatorily and found that its apparent four-state compatibility is explained by preserving the Latin vowel class rather than by Philip's specific consonant subdivision.

A methodological distinction is now explicit:

1. **confirmatory evidence for H4** still requires a prospectively frozen finite family or an independent manuscript-local selector; but
2. **exploratory practical decoder probes** may apply a well-attested historical mechanism directly to Voynich to see whether coherent plaintext emerges, provided each result is labelled exploratory, failed methods are retained, and no one-by-one success is promoted as family-level significance.

This distinction follows the later user-requested research direction: a single historical method may be a local optimum or the wrong mechanism, so practical exploration should traverse genuinely different cipher mechanisms rather than repeatedly retune one fit.

## Pre-/near-Voynich historical frontier

### Martinus Polonus — 1277 attribution

Klaus Schmeh's historical gallery identifies a musical cipher attributed to Martinus Polonus in 1277 and cites David A. King, *The Ciphers of the Monks* (2001), p. 114.

Current limitation:

- the attribution/image is public, but an exact independently auditable machine-readable key has not yet been recovered from Martinus/King;
- do not guess the key from a low-resolution figure or infer it from Voynich statistics.

Disposition: **high chronological priority, blocked on exact key recovery**.

### León / Visigothic musical cryptography — ca. 10th century tradition

Elsa De Luca's work documents neume/neume-like musical signs used as alphabetic cryptographic substitutes in the León Antiphoner / related Visigothic tradition. This is structurally different from pitch×duration grids: the relevant computational family is ordinary monoalphabetic substitution with music-shaped visible signs.

Disposition: **active E11 family**.

E11B introduced the externally maintained Voynich STA1 visual-family representation (23 families) to avoid inventing a glyph alphabet from the target. E11C's mandatory synthetic monoalphabetic positive control failed, including after restoring the frozen 24-letter Latin specification. Therefore E11C is **`SOLVER INADEQUATE`**, not a Voynich negative or positive. E11D now calibrates and locks a substitution solver using medieval-Latin synthetic controls only; Voynich is excluded from solver development.

### Nicholas Philip — 1436

Historical 5-pitch × 4-duration cipher with duration letter groups:

`aeiou | bcdfg | klmnp | qrstz`

Disposition:

- E8-A: stable near-hit but failed frozen significance gate;
- E8-A2: exhaustive vowel-fixed control shows Philip's exact consonant subdivision is ordinary (`p≈.486`);
- E9 practical full-cipher decode: no coherent plaintext, exact pitch key only 3/5 folds.

Classification remains **not supported**.

### Sloane MS 351 — 15th century / commonly late 15th century

Five pitches combined with note-form/stem/value variants; 24 note-system symbols plus an out-of-system `h` in the historical scheme.

Disposition: **exploratory E10 practical probe completed**.

- literal mappings: strongly non-Latin;
- fitted 28,800-key search: same full key 4/5 folds but output collapses to `concon...` because the optimizer maps dominant EMPTY×EMPTY to the multi-character `con` abbreviation;
- CE≈4.222 vs medieval-Latin self-baseline≈2.452;
- zero exact lexicon hits length >=6.

Frozen result: **`NO READABLE SLOANE PLAINTEXT`**.

A separate non-musical future question retains only the 4/5 slot3×slot5 structural recurrence; that backlog must not reuse Sloane letters, Latin likelihood, or music ordering.

## Later mechanisms retained only as structural decoder probes

These are too late to support historical availability to an early-15th-century Voynich author. They can nevertheless test whether a different *algorithm family* exposes plaintext.

### Öttingen-Wallerstein — ca. 1600

HAB transcript gives a source-auditable two-note Polybius-like table using `ut/re/mi/fa/sol`; first note selects row, second note column. The `sol→re` cell is a genuine historical **Leerstelle**, because the alphabet contains 24 letters.

Important source correction:

- an earlier token-internal E11-O executable mistakenly treated the `Lalalala` placeholder in that cell as duplicated plaintext `l`;
- its original numerical artifact remains frozen but is not source-faithful;
- the correction is documented rather than silently rewriting the result.

A later source-faithful sequential-dyad probe, administratively carried as E13, treats successive Voynich five-state events as the two notes and keeps `sol→re` illegal. It is clearly negative: CE=`4.58496`, shuffle `p≈.742`, top-five fraction≈`.986`, zero >=6 lexicon hits. Its nominal 5/5 key recurrence is a deterministic tie-break artifact caused by a q-heavy collapse.

### Porta — 1602

11 pitches × 2 note values, structurally distinct from 5×5 schemes. In E12 the historical `11` is explicitly hypothesis-side; Voynich remaining morphology is clustered to 11 only to instantiate the method.

Disposition: **clean exploratory negative with validated solver**.

- mandatory known-Porta positive control decoded at 100% accuracy;
- Voynich primary mean held CE≈`5.013` vs Latin≈`2.437`;
- duration orientation repeats 5/5 but output does not collapse severely;
- only one >=6 exact word (`missus`) in one fold, no coherent plaintext.

Frozen result: **`NO READABLE PORTA PLAINTEXT`**.

### Schwenter — 1622

HAB scholarly commentary explicitly notes another musical cipher in Daniel Schwenter, *Steganologia* (1622), pp. 303–304, involving the 24-letter alphabet and semitone/whole-tone relations. This is potentially useful because it appears interval-based rather than another fixed pitch×duration grid.

Disposition: **literature lead only**. Recover the exact page-303/304 rule/key before any execution. Do not infer the missing details from Voynich.

### Kircher — 1650

Secondary historical descriptions report a six-instrument × up-to-four-successive-notes scheme yielding 24 letter codes: one note on the first instrument=A, two=B, etc. This is a run-length/instrument family, structurally different from E8–E13.

Disposition: **literature lead only** until the exact 24-letter ordering and primary-source table are independently verified from *Musurgia universalis*. Do not guess period alphabet conventions.

## Current mechanism coverage

The exploratory branch has now crossed several non-equivalent mechanisms:

- Philip: `5 pitch × 4 duration`;
- Sloane: token-internal approximately `5 × 5` graphical product;
- Porta: `11 pitch × 2 duration`;
- Öttingen: source-faithful **successive two-note** code;
- León: ordinary monoalphabetic substitution using music/neume-like visible glyphs.

Thus the current exploration is no longer a repeated optimization of one 5×5 topology.

## Confirmatory boundary

No sequence of exploratory decoder failures or successes by itself supplies a family-level p-value for H4. A future confirmatory claim still requires one of:

1. **finite-family route:** freeze an independently justified candidate family and multiplicity rule before inspecting target scores; or
2. **independent-selector route:** a manuscript-local visual/textual anchor selects a specific historical construction before its text fit is inspected.

Exploratory output may motivate such a test, but cannot substitute for it.

## Sources currently anchoring the frontier

- David Løberg Code, “Can musical encryption be both? A survey of music-based ciphers,” *Cryptologia* 47(4), 2023, 318–364. DOI `10.1080/01611194.2021.2021565`.
- Elsa De Luca, “Musical Cryptography and the Early History of the León Antiphoner,” *Early Music History* 36 (2017).
- David A. King, *The Ciphers of the Monks* (2001).
- Herzog August Bibliothek digital transcript of Cod. Guelf. 56 Aug. 4° for the Öttingen table and comparative notes on Schwenter.
- Eric Sams, “Musical Cryptography,” *Cryptologia* / historical essay (1979).
- Klaus Schmeh, “Musical Ciphers,” historical gallery.
- Giambattista della Porta, *De furtivis literarum notis*, revised 1602 musical-cipher material.

## Research boundary

- Preserve every failed decoder and historical-source correction.
- Do not reinterpret a stable optimizer key as plaintext without absolute language/readability evidence.
- Do not use Voynich output to repair a historical key.
- Do not rerun León on Voynich until the Voynich-blind E11D solver validation passes.
- Do not merge these research branches to `main` without explicit user authorization.
