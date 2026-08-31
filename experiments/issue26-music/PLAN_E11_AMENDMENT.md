# Issue26E11 pre-executable amendment — symmetric line handling

Status: **FROZEN BEFORE E11 EXECUTABLE / SCIENTIFIC REVEAL**

This amendment supersedes only the Latin-run boundary sentence in `PLAN_E11.md`.

## Problem found during implementation audit

`PLAN_E11.md` freezes Voynich primary character-LM scoring as ignoring token boundaries inside a physical line. The draft Latin wording said nonletters break LM runs, which would make spaces break Latin runs while Voynich spaces are ignored.

That is an asymmetric comparison and is corrected before any E11 executable exists or any E11 score/plaintext is computed.

## Authoritative rule

For the **character 4-gram model and Latin self-baseline**:

- work one physical Latin transcription line at a time;
- normalize alphabetic characters to lowercase ASCII with `j→i`, `v→u`;
- ignore/delete spaces, punctuation, digits, markup, and other nonalphabetic characters **within that physical line**;
- concatenate the remaining normalized letters;
- only the physical-line boundary breaks the 4-gram run.

Voynich likewise concatenates its frozen visible grapheme tokens within each physical transcription line for primary character-LM scoring; the physical-line boundary breaks the run.

Thus primary LM comparison is line-to-line and does not depend on treating Voynich spaces as true words.

For **lexicon/readability diagnostics only**, original token/word boundaries remain available on both sides. No key fitting uses lexicon boundaries.

## Positive-control clarification

The matched Latin positive control starts from these physical-line letter runs. Letters outside the frozen top-`M` plaintext set break a positive-control run as already specified in `PLAN_E11.md`; ordinary spaces/punctuation within the source line do not create additional breaks before that filtering.

No other E11 population, tokenizer, optimizer, threshold, control, or interpretation rule changes.
