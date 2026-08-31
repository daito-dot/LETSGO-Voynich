# Issue #26E11-O — Öttingen-Wallerstein 5×5 music-cipher probe report

Status: **FIRST REVEAL RECORDED**

Frozen plaintext classification: **`NO READABLE OETTINGEN PLAINTEXT`**

Preregistered 5×5 local-optimum flag: **`NO NUMERIC LOCAL-OPTIMUM FLAG`**

`E11-O` is used in this report to distinguish this parallel Öttingen branch from the separately created León substitution E11 branch. The preregistration itself remains historically frozen as `PLAN_E11.md`; no pre-reveal history is rewritten.

## Question

E10 found a 4/5 recurrent fitted key under the Sloane 351 5×5 cipher but no readable plaintext. E11-O asks whether an independently documented 5×5 musical Polybius cipher produces readable Latin under the same engine, and whether the Sloane stable-key/frequency-collapse pattern simply recurs for another 5×5 table.

The tested Öttingen-Wallerstein system is ca. 1600 and therefore later than the usual Voynich dating window. It is used only as an exploratory algorithm-family comparison, not as evidence for historical transmission to the Voynich author.

## Frozen historical table

From the HAB transcription of *Steganographia comitis*, the third letters of the angel names give the following 5×5 plaintext table in documented row/column solfège order:

```text
q r s t u
w x y z l
a b c d e
l m n o p
f g h i k
```

Rows: `ut, sol, fa, mi, re`.
Columns: `ut, fa, sol, mi, re`.

The duplicated `l` is historical: the `Lalalala` cell is the superfluous/filler cell discussed in the source tradition.

## Audit/provenance

- branch base: Issue26E8 head `343afac73da2e52b3a75f69e0a43257d54bdf952`
- plan-first: `13380346f55a0e9df82af243c9fa0c7d8a053c90`
- first executable: `aee157a150ee8112a269c8e95cdae5ed578bea9b`
- first-reveal scientific head: `40b08ce7e6f99ddb4de0d6ca9fd2a3a0ad272927`
- exact frozen E10 engine dependency: `39eebc9f3fc1085e506a0b55ed86e43c83dbc579`
- Actions run: `33381272618`
- job: `99453947431`
- artifact: `9753849723`
- raw JSON SHA-256: `df33837106c7468b200d5fd34ea90f3fd84a18726a7cbb899523e1829a235a3e`
- artifact ZIP SHA-256: `99fbb7b24ebb95b29faa49d9a789bcf548ca4993ad24ec214a1195f1993c2617`

The workflow verified that the plan predates the executable and checked the exact E10 engine SHA, ZL3b source/blob, and CREMMA commit before execution.

## Evaluation engine

E11-O reuses the exact E10 search/language engine; only the historical 5×5 plaintext table is replaced.

- same two natural five-state Zattera factors: slot3 and slot5;
- same two axis assignments;
- all `120 × 120` row/column permutations;
- **28,800 keys/fold**;
- selection on four-fifths of physical leaves only;
- untouched one-fifth held out;
- same external medieval-Latin 4-gram model;
- same Latin self-baseline: **`2.4515716158 bits/char`**.

Primary parser is `min`; relevant `max` results are numerically identical here.

## Track A — literal/canonical application

Four deterministic, unfitted conventions all fail plainly:

| row/style slot | column/pitch slot | column order | CE bits/char | top-five char fraction | distinct lexicon hits >=6 |
|---:|---:|---|---:|---:|---:|
| 3 | 5 | documented | 4.59335 | .96518 | 0 |
| 3 | 5 | reversed | 4.98523 | .96518 | 0 |
| 5 | 3 | documented | 4.60655 | .96514 | 0 |
| 5 | 3 | reversed | 4.89911 | .96514 | 0 |

Representative literal outputs:

```text
qqqqaaqarqsq
qqqaqqqaqaqq
aqqqqwwqqwqq

uuuueeuetusu
uuueuuueueuu
euuuulluuluu
```

They are far from the Latin baseline and collapse to a few characters.

## Track B — exhaustive training-only alignment

Primary `min`:

- pooled held-out CE: **`4.3870557918 bits/char`**;
- mean held-out fold CE: `4.3874928506`;
- exact full-key recurrence: **3/5**;
- recurrent key:
  - row/style slot3 permutation `[4,1,3,2,0]`;
  - column/pitch slot5 permutation `[3,1,4,2,0]`;
- pooled top-five-character fraction: **`95.5686%`**;
- distinct exact CREMMA lexicon hits length >=6: **0**.

Held-out fold CEs:

- fold0 `4.3463977632`
- fold1 `4.4472387685`
- fold2 `4.3007699456`
- fold3 `4.4262755561`
- fold4 `4.4167822198`

Representative untouched outputs:

```text
iiiiooiogiki
iiioiiioioii
iooooiiiiiio
iooziziiizozii
iiziozziizzii
oiiiiiiizizi
ziiizizzizii
ziiiiizizzzii
iozoiigziogi
zoioziiziozi
```

The output again becomes strongly low-diversity and non-lexical. Reported exact lexicon matches are only four-character artifacts such as `iiii`; there are no six-character-or-longer exact hits.

## Comparison with E10 Sloane

The comparison is informative but more nuanced than “the same optimum repeats.”

| diagnostic | E10 Sloane | E11-O Öttingen |
|---|---:|---:|
| fitted exact key recurrence | **4/5** | **3/5** |
| held-out CE | 4.22241 | 4.38706 |
| Latin self-baseline | 2.45157 | 2.45157 |
| top-five char fraction | 94.6915% | **95.5686%** |
| exact lexicon hits >=6 | 0 | 0 |
| characteristic collapse | `concon...` | `i/o/z...` |

Therefore the preregistered label `5X5 LOCAL-OPTIMUM PATTERN REPEATS` does **not** fire because Öttingen does not reach the required >=4/5 exact-key recurrence.

However, the broader optimizer pathology clearly persists: a different historical 5×5 table still produces an extremely concentrated held-out alphabet and no coherent Latin. The Sloane **exact key stability** is not a universal property of arbitrary 5×5 tables, while the **frequency-collapse/non-language optimum** is much less table-specific.

This makes the E10 residual worth keeping, but it should not be interpreted as generic 5×5 evidence or as Sloane plaintext evidence.

## Frozen result

Neither literal nor fitted application approaches readable medieval Latin.

**`NO READABLE OETTINGEN PLAINTEXT`**

The separate preregistered local-optimum diagnostic is:

**`NO NUMERIC LOCAL-OPTIMUM FLAG`**

because exact-key recurrence is 3/5 rather than >=4/5.

## Interpretation

E11-O gives a useful cross-probe distinction:

1. the E10 Sloane 4/5 exact key recurrence was **not automatically reproduced** by another 5×5 historical table;
2. nevertheless both 5×5 decoders exploit the severe imbalance of the Voynich slot3×slot5 population and produce highly concentrated, non-language-like output;
3. stable or semi-stable language-model optima therefore cannot be treated as decipherment evidence without explicit anti-collapse diagnostics and coherent held-out lexical/syntactic output.

The next music-cipher probe should move to a structurally different mechanism rather than continue optimizing 5×5 tables.

## Merge policy

Keep E11-O on `issue26-music-e11-oettingen-probe` as a parallel exploratory research branch. Do not merge to `main` without explicit user authorization.
