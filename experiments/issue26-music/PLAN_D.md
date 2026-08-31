# Issue #26 experiment D — adversarial audit of the public `daiin = octave` / f113r music claim

Status: **FROZEN BEFORE EXECUTABLE / SCIENTIFIC REVEAL**

Issue: #26

Base main: `96e6f4cf7b2a12f624ebf1e43ab674c58eb8c5bb`

## Purpose

Audit a specific public direct-musical interpretation rather than inventing a new Voynich-to-music mapping.

The public claim, as posted in March 2026, asserts all of the following:

1. `daiin` is an octave marker and `aiin` / `ain` is a tone or note;
2. on f67r2, `aiin` forms occupy positions 1–4, disappear at positions 5–6, then resume at position 7, interpreted as two tetrachords separated by a tone of disjunction;
3. an `ain` at approximately 12 o'clock lies opposite a `-daiin` at approximately 6 o'clock;
4. on f113r, the pitch mapping `che-=G, o-=D, qo-=F, sho-=A, cho-=E, ch-=C` produces the Mode-VIII `Veni Creator Spiritus` contour;
5. f113r paragraphs 6–8 form an antiphonal `A+B / A / B` structure, with paragraphs 7 and 8 repeating the respective halves of paragraph 6 word for word.

This experiment treats those statements as a fixed external hypothesis. It does not repair them by inventing additional prefix stripping, glyph equivalences, note mappings, paragraph choices, rotations or reversals after seeing the result.

Public claim source frozen for provenance:

- Voynich Ninja thread `daiin as Octave and Veni Creator Spiritus`, March 2026.
- The audit tests the literal claims visible in the public text, not later revisions of unrelated decoding systems.

## Frozen manuscript source

Voynich transcription:

- repository: `matthewdgreen/cipher_benchmark`
- commit: `315f0cad4de3d021bd4185765c037cf2a28d341c`
- file: `benchmark/unsolved/sources/voynich/transcriptions/ZL3b-n.txt`
- expected git blob: `2a4533ab9bdfa85db9bad602d590978953055df1`

## Frozen chant reference

`Veni Creator Spiritus`, Solesmes/Liber Hymnarius version as represented by GregoBase score id 14258, mode 8.

For the first stanza, the pitch groups are frozen separately in `VENI_CREATOR_STANZA1_PITCH_GROUPS.txt`. They were copied from the GABC source before writing the executable. Only pitch groups are retained, not the lyric text.

The pitch groups are flattened to a diatonic event sequence. Absolute transposition is discarded by comparing successive diatonic intervals.

## D1 — f67r2 twelve-sector factual audit

Use the twelve sector blocks beginning at the twelve `@Pb` paragraph starts on f67r2, in ZL3b transcription order. ZL3b explicitly describes the blocked text as starting at approximately 10:00.

Primary `AIIN` presence for a sector is true if any normalized token contains the contiguous substring `aiin`. This includes forms such as `daiin`, `saiin`, `alaiin`, `chedaiin`.

The externally claimed first-seven pattern is:

`[present, present, present, present, absent, absent, present]`

Report literal Hamming agreement for sectors 1–7. Do not rotate or reverse the primary sequence.

Sensitivity only: repeat with an `A-I-RUN-N` family defined by regex `a[i]+n`, so exact `ain`, `aiin`, `aiiin`, etc. are all included. This sensitivity cannot rescue a failed primary claim unless it independently satisfies the same first-seven pattern.

Frozen factual condition D1 passes only if the primary first-seven pattern is exact (7/7).

## D2 — f67r2 `ain` ↔ opposite `-daiin` audit

With sector 1 at ~10:00, sector 3 is ~12:00 and sector 9 is ~6:00.

Check the literal factual statement:

- sector 3 contains exact token `ain`;
- sector 9 contains a normalized token ending exactly in `daiin`.

Then measure whether the opposition is unusual rather than merely present:

- `root sectors` = sectors containing exact token `ain`;
- `octave sectors` = sectors containing any token ending `daiin`;
- observed score = number of root sectors whose diametrically opposite sector (+6 mod 12) is an octave sector;
- exact circular null = rotate the octave-sector occupancy pattern by every one of 12 offsets relative to the fixed root sectors;
- one-sided exact p = fraction of 12 rotations with score >= observed.

D2 support requires the literal pair to exist **and** exact p <= 0.05. Presence without rarity is not evidence for octave semantics.

## D3 — f113r `A+B / A / B` repetition claim

Paragraphs are the units started by `<%>` on f113r. Number them from 1.

Normalize visible tokens using the same conservative ASCII-letter extraction as experiment A.

The public word-for-word claim is tested literally:

- P7 must equal an initial contiguous token sequence of P6;
- P8 must equal the remaining terminal contiguous token sequence of P6;
- therefore `P7 + P8 == P6`.

Report token counts, equality flags, longest common contiguous token-run length, LCS length and token-set Jaccard for P6/P7 and P6/P8.

D3 passes only if the exact concatenation identity holds. Similar vocabulary does not count as word-for-word repetition.

## D4 — f113r `Veni Creator Spiritus` prefix-to-pitch mapping

Target text is fixed to f113r paragraphs 1–3, exactly as claimed.

Fixed literal prefix map:

- `che` -> G
- `o` -> D
- `qo` -> F
- `sho` -> A
- `cho` -> E
- `ch` -> C

Prefix matching is at the beginning of the normalized token only. Where prefixes overlap, longest-prefix match wins; lexical order breaks equal-length ties. No undocumented removal of leading `p/k/y/l/...` is allowed.

Convert note names to diatonic integers `C=0,D=1,E=2,F=3,G=4,A=5`. Take successive differences to form a transposition-invariant interval sequence.

Flatten the frozen GABC first-stanza pitch groups to ordered diatonic letters and likewise take successive differences.

Distance metric: deterministic dynamic time warping on the two interval sequences with point cost `abs(x-y)`, normalized by DTW path length. No local parameter is fitted.

Two exact multiplicity controls are frozen:

### D4a mapping search control

Keep the six prefix classes and the six pitch values fixed, but enumerate all `6! = 720` one-to-one assignments. Rank the published assignment by smallest DTW distance.

`p_map = (# assignments with distance <= published distance) / 720`.

### D4b paragraph-window control

Keep the published mapping fixed. Evaluate every contiguous three-paragraph window on f113r that yields at least 8 mapped pitch events. Rank P1–P3 by smallest DTW distance.

`p_window = (# eligible windows with distance <= P1–P3 distance) / (# eligible windows)`.

Report mapping coverage: mapped tokens / all tokens in P1–P3.

D4 support requires both `p_map <= 0.05` and `p_window <= 0.05`.

## Frozen overall interpretation

- `SUPPORTED`: D1, D2, D3 and D4 all pass.
- `PARTIAL`: at least two of D1–D4 pass, but not all.
- `NOT SUPPORTED`: fewer than two pass.

This classification applies only to this published package of claims. It does not falsify every possible musical encoding of Voynichese.

## Non-negotiable anti-overfitting rules

After reveal, do not:

- rotate/reverse f67r2 and call that the same claim;
- redefine `aiin form` based on which sectors fit;
- strip arbitrary leading glyphs before prefix matching;
- change the six pitch assignments;
- choose different f113r paragraphs;
- substitute a different melody/version because it scores better;
- relax `word for word` to vague vocabulary overlap;
- use a post-hoc positive sensitivity as if it were the frozen primary result.
