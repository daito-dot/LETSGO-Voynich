# Issue #26E12 pre-executable amendment — plaintext word diagnostic

Status: **FROZEN BEFORE E12 EXECUTABLE / REVEAL**

Parent plan: `PLAN_E12.md` first committed at `8cf6532b0e6ab9799e64b55f4706905780515961`.

## Correction

The parent plan mistakenly requested “decoded whole-token CREMMA lexicon hits.” Under the E12 representation, however, **one parsed Voynich token is one Porta musical cipher event and therefore decodes to one plaintext character**. A Voynich token cannot simultaneously be a multi-character decoded plaintext word.

This is a representation-level logical error caught before any E12 executable or E12 score existed.

## Frozen replacement

Voynich token boundaries are treated as inter-symbol spacing only and are **not** asserted to be plaintext word boundaries.

For held-out readability diagnostics:

- decode each uninterrupted physical-line run to a plaintext character string;
- do not cross physical line boundaries or unparseable-token breaks;
- enumerate every contiguous substring of decoded length 4 through 15;
- record substrings that are exact normalized words in the frozen supported CREMMA lexicon;
- deduplicate the primary long-word diagnostic by `(word, fold)` for cross-fold support;
- report occurrences/context separately;
- the primary lead gate becomes: **at least 10 distinct exact CREMMA words of length >=6, with qualifying words occurring across at least 3 held-out folds**.

No manual respacing, dictionary-guided segmentation, skipped characters, anagramming, or spelling edits are allowed.

All other E12 plan elements, including the historical Porta table, slot11 binary factor, k=11 hypothesis-side clustering, key optimizer, positive control, CE gate, top-five-character gate, and duration-orientation recurrence gate, remain unchanged.
