# Issue26E11C — STA-family León-style substitution test report

Status: **FIRST VALIDLY EMITTED RUN RECORDED — SCIENTIFIC CLASSIFICATION `SOLVER INADEQUATE`**

E11C must **not** be interpreted as a negative result about the Voynich manuscript or León-style substitution. Its mandatory known-cipher positive control failed badly.

## Pre-reveal chronology and corrections

The E11C hypothesis/decision plan was committed before an executable existed:

- plan-first: `58fa4527201eb11e8dc756c79ffb992bec7e8ee2`
- unreadable-sign amendment: `c4b12ae9d376b6f09428025d7ba6f41550cad403`
- first executable: `d1e1602f61362f7275779149fe27ce13ec2bbefd`
- initial parsing wrapper: `3dee673ac3d4dddbdaf004ac1078d8fef6ab47bb`

Two parser-only runs then stopped before scoring/output:

1. IVTFF `[C2:]` exposed an empty second alternative not accepted by the first regex.
2. IVTFF `[:A2]` exposed an empty first alternative.

The frozen rule had always been “take the first reading,” including an empty first reading. The wrapper was corrected accordingly. This also exposed a one-event error in the E11B descriptive audit; corrected E11B is recorded in `REPORT_E11B.md`.

Before inspecting any successfully emitted E11C score, code audit also found that the shared constant described as the 24-letter alphabet had accidentally retained `v`, creating 25 letters. The frozen plan explicitly says `j→i`, `v→u`; commit `a643c273fe08da116a24f21954cf1d507e73c729` corrected the runtime constants to the actual 24-letter alphabet before the accepted reveal.

An earlier in-progress 25-letter run is non-authoritative by construction and is not used below.

## Accepted reveal provenance

- scientific head: `a643c273fe08da116a24f21954cf1d507e73c729`
- Actions run: `33382380148`
- job: `99457420733`
- artifact: `9754369814`
- raw JSON SHA-256: `6e0bee446000fcfd81ab20a383910256a2c6e19fbb1a72befa40aa93358940b7`
- artifact ZIP SHA-256: `0cd1ad7143e57fe64c6960791cb9a3b76a9cf5813db2f07de7bbba352169f8d2`

## Mandatory positive control

The control is a known synthetic monoalphabetic substitution of frozen medieval Latin with 23 cipher symbols and matched scale. It is the authority on whether the solver is capable of supporting a negative Voynich inference.

Observed:

- control pass: **false**
- mean true-key held-out CE: `2.8305081643 bits/char`
- mean recovered-key held-out CE: `4.5930139959 bits/char`
- mean occurrence-weighted key accuracy: **`.0339823`**
- exact recovered-key recurrence: `2/5`

Frozen positive-control gate required:

- recovered CE within `.05 bits/char` of true-key CE; and
- weighted key accuracy >= `.95`.

Both fail decisively.

Therefore the frozen classification is:

**`SOLVER INADEQUATE`**

No Voynich negative inference is permitted.

## Voynich output is non-authoritative

The workflow necessarily computed the Voynich branch after the control, but because the solver gate failed these numbers are retained only for audit, **not interpreted as evidence**:

- mean held-out CE `4.32208`
- pooled held-out CE `4.30514`
- weighted key stability `.73439`
- exact full-key recurrence `1/5`
- pooled top-five character fraction `.66485`
- one distinct >=6 whole-token lexicon hit in one fold.

Representative strings and mappings in the raw artifact must not be used to tune a subsequent solver. E11D solver development is restricted to synthetic/known plaintext controls.

## Additional population-audit issue discovered after the solver failure

The corrected E11B descriptive source audit sees:

- 4,130 running-text physical lines with codes;
- 140,589 first-reading STA code events.

The E11C parser reports:

- 4,119 source running-text lines;
- 140,423 family events.

So E11C's locus parser excludes **11 lines / 166 events** relative to the intended running-text source audit. This difference was discovered after the run but is another reason not to reuse E11C as a scientific negative.

Before any new substitution test, E11D must reconcile the source population against the official audit and freeze an exact parser with explicit treatment of every excluded locus form.

## What can legitimately be concluded

Only this:

> The first preregistered stochastic substitution solver is not capable of reliably recovering even a known matched 23-symbol medieval-Latin monoalphabetic cipher, so it cannot adjudicate the Voynich hypothesis.

The correct next action is solver validation, not increased cipher flexibility.

Specifically:

1. reconcile STA source population without looking at Voynich plaintext quality;
2. develop/tune a solver **only on known synthetic Latin substitutions**;
3. certify the frozen solver on independent hidden synthetic keys;
4. only then perform one new held-out Voynich application.

No homophony, null symbols, family merging, or language change is justified by E11C.
