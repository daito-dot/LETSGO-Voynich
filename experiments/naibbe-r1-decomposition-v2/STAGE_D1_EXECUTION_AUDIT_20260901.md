# Issue #72 V2 — Stage D1 execution audit (2026-09-01)

## Scope

This note records execution/transport chronology around the Stage D1 PT first reveal. It does not alter any scientific intervention, scorer, target, null, baseline, assignment, or aggregation rule.

## Canonical scientific execution

The canonical first target reveal is uniquely:

- scientific head: `02d757e36d85cdfc9231be0b8753904b3ceb543c`
- workflow: `.github/workflows/issue72-v2-stage-d1-pt-rebind-first-reveal.yml`
- workflow run: `33494367825`
- conclusion: `success`
- population: `155/155`
- drops: `0`
- rerolls: `0`
- complete artifact ID: `9795439622`
- artifact ZIP SHA-256: `f06f6190f802411494bbae77611c803e363013a366196993913a91394c5d6852`
- aggregate SHA-256: `402941d895c020e7f93c8ccab9585d684117227836fa69d7465376a609d24de2`

The canonical run followed successful target-blind rebind preflight run `33494182268` at head `0bc909526d5c41f0e31ab5d9f062f92f18b06ff3`.

The permanent repository copy was independently verified and frozen by workflow run `33495408033`, producing commit `0853092d1a6e5bd1dc7f922295a5cc06055fb516`.

## Duplicate first-reveal workflow incident

After the canonical run had already launched, an additional workflow file with overlapping intent was added:

`.github/workflows/issue72-v2-stage-d1-pt-first-reveal-rebind.yml`

Its run was `33494555298`.

The duplicate run failed at its authorization stage. Its scoring and aggregation jobs were skipped. It therefore produced no additional PT target-scored population and is not a scientific authority.

The duplicate workflow was removed in commit:

`30b9981bd712704fac829e0adcc421f50c779478`

The permanent `stage-d1-pt/ARTIFACT_AUTHORITY.txt` also records this exclusion.

## Duplicate evidence-freeze workflow

A second post-reveal evidence-freeze workflow was subsequently added at commit:

`90b972fb6c675470fd992ec0c3fc268a8876cdb6`

This occurred after the exact authority had already been copied into `stage-d1-pt/` by permanent-freeze commit `0853092d1a6e5bd1dc7f922295a5cc06055fb516`.

Its own guard requires `stage-d1-pt/` not to exist before copying, so it cannot supersede the already-frozen authority. It is transport-only and is not part of the scientific execution chain.

## Authority rule

For all subsequent interpretation and downstream work, the only Stage D1 scientific result authority is:

`experiments/naibbe-r1-decomposition-v2/stage-d1-pt/`

as frozen from canonical run `33494367825` with aggregate SHA-256:

`402941d895c020e7f93c8ccab9585d684117227836fa69d7465376a609d24de2`.

No later workflow run may replace, average with, select over, or tune this result.
