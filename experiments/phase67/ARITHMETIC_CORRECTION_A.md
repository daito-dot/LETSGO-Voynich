# Phase 67A exact-null arithmetic correction

Status: **POST-REVEAL CLERICAL CORRECTION; SCIENTIFIC RULE UNCHANGED**

The frozen `PLAN_A.md` wrote the correct factorial expression for the within-folio assignment space but evaluated it incorrectly:

`4! * 3! * 2! * 1! * 2! * 2!`

The plan text stated 2,304. The correct product is **1,152**.

The executable did not hard-code 2,304. It derived the exact assignment count from the frozen block manifest and asserted that the number of enumerated assignments matched the product of the folio factorials. Therefore the successful run enumerated **all 1,152 assignments exactly**, including identity, and the reported exact p-values are unaffected except that their correct denominator is 1,152.

This correction was written after the Phase67A result was opened. It changes no block, image annotation, text feature, statistic, permutation stratum, threshold, or classification.