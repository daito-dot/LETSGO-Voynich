# OGH-A first-reveal provenance

Status: **scientific first reveal complete — local execution, Actions replay workflow provided**

## Chronology (git)

- plan first-add: `588892940554570feb6d6300acaae34969e9d5fb`
- executable first-add: `643955a5d06f20de98ff64ace30d79c113dc104b`
- admissible set / preflight freeze: `1d1f6db4c2a43ad5c05d209237b66be12ebc2211`
- exact pre-reveal head from which every scoring job ran: `1d1f6db4c2a43ad5c05d209237b66be12ebc2211`

## Execution

- host: Claude Code remote container, Linux 6.18.44-fc-v22 x86_64
- interpreter: Python 3.11.15; numpy 2.4.6, scipy 1.17.1
- driver: `run_all.py` with 4 worker processes; each job is an independent process
- population: 2 skeletons × 7 models × 3 replicates = 42 scored corpora, 0 drops, 0 rerolls
- started: 2026-09-01 ≈20:26 UTC (first four jobs); finished: 2026-09-01 20:55:17 UTC

Sources (third-party, not redistributed; fetched with `data/fetch_transcriptions.py`):

- ZL3b-n.txt Git blob `2a4533ab9bdfa85db9bad602d590978953055df1`
- IT2a-n.txt SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`

Frozen references verified at every job: #58C raw `fba60daea6e30682065900a4cf15d53d2a2f536d933b588fae447fb43bb4728d`, #58D raw `f26db8123f8f2b7a4148495fdeebe81c8c042a23606eb7c22e1c0687faaf86a6`.

## Replay

`.github/workflows/ogh-a-replay.yml` re-runs any single frozen job on GitHub Actions and asserts byte-identical generated corpus and residual vector against `results/`. Generation and nulls are seeded through `stable_seed` namespaces, so any machine with the pinned dependency majors should reproduce every number exactly.

## Hashes

See `SHA256SUMS.txt`.
