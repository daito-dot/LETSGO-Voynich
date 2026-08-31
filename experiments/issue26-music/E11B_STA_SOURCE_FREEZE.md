# Issue26E11B — STA-family source freeze (non-scientific preflight)

Status: **SOURCE/PRESENTATION AUDIT ONLY — NO PLAINTEXT SCORING**

The first strict E11 run stopped as preregistered because a hand-built EVA-ish tokenizer exposed 31 symbol classes, more than the 24-letter Latin plaintext alphabet. That stop is not a negative result.

Official Voynich transliteration documentation independently identifies the same underlying problem: ZL3b uses Extended EVA, including rare single characters and ligatures, and the newer STA system was created specifically to place visually similar variants into published `character families` so that transliterations can be compared at a more stable level.

E11B will therefore audit the **official ZL3b-in-STA file**, not prune symbols by frequency.

Source fixed before audit execution:

- official page: `https://www.voynich.nu/extra/sta.html`
- official ZL STA level-0 link: `https://www.voynich.nu/data/sta/ZL3b.txt` (the site may redirect to the `mail.voynich.nu` host)
- expected header: `#=IVTFF STA1 2.0 M 5`

For this source-freeze audit only:

1. download the official STA file;
2. print SHA-256 and byte count;
3. parse only paragraph-running-text loci (`kind` containing `P`), matching the Issue26 running-text scope;
4. resolve bracketed alternatives by taking the first listed alternative, consistent with the existing benchmark convention;
5. remove IVTFF markup/interruption markers without joining text across a physical-line boundary;
6. parse every STA character as exactly two ASCII characters: one uppercase family letter plus one member character;
7. count full STA codes and **family letters** separately;
8. print the set/count/frequencies of family letters and the fraction of symbol events covered by each;
9. do not fit a plaintext key, train a language model, decode text, or compute a scientific score.

Decision after the source audit:

- if the official STA family alphabet in running text has `M_family <= 24`, a separately preregistered E11C may test strict family→Latin monoalphabetic substitution using those externally defined families;
- if `M_family > 24`, strict injection remains structurally inapplicable and no post-hoc family deletion is allowed;
- any future many-to-one/homophonic model must be separately justified from the historical León evidence and separately preregistered.

This source audit is descriptive infrastructure, not a hypothesis test.
