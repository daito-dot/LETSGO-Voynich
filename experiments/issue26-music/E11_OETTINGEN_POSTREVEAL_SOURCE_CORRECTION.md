# E11-O post-reveal historical-source correction

Status: **POST-REVEAL SOURCE CORRECTION; ORIGINAL RESULT PRESERVED**

The first-reveal E11-O report and artifact remain frozen for audit. A later direct re-check of the Herzog August Bibliothek transcript identified a factual error in the historical plaintext table used by the executable.

## Error

`REPORT_E11_OETTINGEN.md` and the first-reveal executable represented the row `sol`, column `re` cell as a duplicated plaintext `l` and described `Lalalala` as a historical filler.

That is incorrect as a plaintext-key interpretation.

The HAB transcript/editorial reduction gives the exact third-letter key as:

```text
        ut  fa  sol mi  re
ut      Q   R   S   T   U
sol     W   X   Y   Z   -
fa      A   B   C   D   E
mi      L   M   N   O   P
re      F   G   H   I   K
```

and explicitly explains that the 24-letter alphabet leaves a **Leerstelle** (blank cell) at `sol → re`. `Lalalala` is the angel-table placeholder occupying that source cell; it is not another plaintext `L`.

Primary source/editorial transcript:

- Herzog August Bibliothek Wolfenbüttel, Cod. Guelf. 56 Aug. 4°, *Steganographia comitis Friderici Öttingensis in Wallerstein*, especially the table and editorial explanation around fol. 100r / the worked `Hansen` example.
- Digital transcript: `https://diglib.hab.de/content.php?dir=edoc/ed000213&distype=optional&xml=briefe/240319.xml&xsl=tei-transcript.xsl`

The transcript states that the alphabet contains only 24 letters and that the interval `sol-re` therefore yields a `Leerstelle` after Z.

## Consequence

The original E11-O numerical result **cannot be described as an exact source-faithful replay of the Öttingen key**. Its frozen negative remains a valid result for the mistakenly completed 25-cell table that was actually executed, but it is not the canonical historical Öttingen table.

Do not silently replace the original artifact or report numbers.

A source-faithful sequential-dyad experiment using the genuine blank cell was independently preregistered and executed later (originally under an accidental E11 label, administratively carried forward as E13). It also produced a clear plaintext negative, while treating `sol→re` as illegal rather than as a deletion or character.

## Research interpretation

This correction strengthens the need to distinguish:

1. frozen computational provenance — what table an executable actually used; and
2. historical provenance — what the primary/transcribed source actually says.

E11-O's first-reveal classification remains preserved as historical audit evidence, but future comparisons must use the blank-cell table above.
