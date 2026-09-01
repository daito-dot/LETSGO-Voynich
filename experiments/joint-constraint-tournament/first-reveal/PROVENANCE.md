# Issue #68 R1 first-reveal provenance

Status: **PERMANENT SCIENTIFIC FIRST-REVEAL RECORD WITH DETERMINISTIC TRANSPORT RECOVERY**

## Scientific first execution

The preregistered scientific first reveal remains the original PR-open execution:

- PR: `#71`
- workflow run: `33456282445`
- job: `99696811349`
- exact scientific head: `65e020cb2827a28670005da6d5d02bd6a6c1e51a`
- exact `target68.py` Git blob: `e94a24fbdfbb922099407313f23a1b87859130b6`
- first-reveal workflow Git blob: `ce57060cad2308e19ae580fa42f66fb6948e285d`
- design main: `b2298d7fe251070dacd21852ae3b5a1dac95fe65`

The real target step completed successfully after all `1,000` reference and `1,000` test nulls. The following JSON-validation step failed because stdout contained one legacy informational line before the final JSON, so the original runner-local result file was not uploaded.

The first execution remains the scientific first reveal; it is not relabeled or replaced by the recovery run.

## Deterministic transport reconstruction

Before recovery, `FIRST_REVEAL_TRANSPORT_FAILURE.md` froze the allowed recovery conditions and recorded that no target metric had been observed.

Recovery then re-executed the **exact original scientific head/code** under the exact first-run package versions and exact external authorities:

- recovery workflow run: `33456556334`
- recovery job: `99697644345`
- recovery workflow branch head: `e86abb0f78c629d758efd1cb023046e8b24a61e2`
- code actually checked out/executed: `65e020cb2827a28670005da6d5d02bd6a6c1e51a`
- exact scorer blob: `e94a24fbdfbb922099407313f23a1b87859130b6`
- `TARGET_HEAD_SHA`: `65e020cb2827a28670005da6d5d02bd6a6c1e51a`
- numpy `2.5.2`
- scipy `1.18.1`
- pandas `3.0.5`
- CREMMA `292525969ad98380b398e6606a9c2a36d51913ae`
- Naibbe `f2675ec5dd275268bc64dd48ea64fc0e0e9827a2`

The recovery saved all stdout before parsing. The exact legacy prefix was:

`Total ambiguity retries: 0`

followed by one newline. The final JSON suffix was isolated mechanically without scientific-content modification.

## Recovery artifact

- artifact ID: `9781669431`
- artifact ZIP SHA-256: `4586a90998a1b54a81c2b2c7ee0a2477c1eb56c79ba1b4cd001e94506cbaa7ad`
- recovered scientific JSON SHA-256: `5cef35e9df56149fb1db5edff8d52fad9291208476b0d4ac64bd9c8782faa471`
- complete recovery raw stdout SHA-256: `416e05a7603c681c517a7b736150c44e7f022188bb52fdc46487b76a34756a65`
- legacy prefix SHA-256: `da7a7c54d7ceb82c9022fa02014eb84139e4e2e5ced874feacde7b71807915a5`

Permanent files:

- `issue68_joint_tournament_results.json` — isolated exact scientific JSON produced by the frozen scorer;
- `recovery_raw_stdout.txt` — complete deterministic recovery stdout;
- `transport_legacy_prefix.txt` — exact non-JSON prefix responsible for the original transport failure.

## Scientific-authority rule

Cite the scientific event as run `33456282445` / job `99696811349` / head `65e020cb...`.

Cite the JSON bytes as a **deterministic transport reconstruction** from run `33456556334`, not as a second independent experiment or a replacement first reveal.

No candidate, threshold, seed, parser, output view, null namespace, target reading, package version, scorer code, or source corpus was changed between the scientific first execution and deterministic recovery.
