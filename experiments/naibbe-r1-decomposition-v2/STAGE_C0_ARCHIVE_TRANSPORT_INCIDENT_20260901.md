# Issue #72 V2 Stage C0 — archive transport incident (2026-09-01)

Status: **SCIENTIFIC C0 COMPLETE / ARTIFACT AUTHORITATIVE / REPOSITORY TRANSPORT REPAIR ONLY**

Successful scientific C0 evidence was produced and validated in:

- workflow run: `33468199347`
- job: `99732343946`
- exact scientific head: `d21ce72c756ab9ed09ee58302366b2df9ea692c2`
- Actions artifact ID: `9785652875`
- artifact ZIP SHA-256: `c642519356f477441dcbb7d910988966a0c1c2b661e03be5cee078564e1426da`
- raw `stage_c0_support.json` SHA-256: `da00a66b77a90eb36a158a9942927a27743e64aba7fac69337ff3a67424d695a`
- raw bytes: `206486933`
- `MANIFEST.json` SHA-256: `aba822be57bbac0c04a9fa785a0a835eafe192b406fead5cd7166051825f45ae`

The run successfully completed:

1. exact source and prior-authority verification;
2. target-blind generation of all 4 axes × 31 fixed-path randomizations;
3. exact rep0..rep4 trace replay validation;
4. all intervention invariants;
5. common-support and parser-support freeze;
6. target firewall validation;
7. exact SHA manifest creation;
8. Actions artifact upload.

Only the final repository push failed. The local commit attempted to add the raw JSON directly, but GitHub rejected it because `stage_c0_support.json` is 196.92 MiB and exceeds GitHub's 100 MiB single-file limit (`GH001`).

This is an archive transport failure only. It occurred after scientific validation and artifact upload and cannot license any change to the Stage C population, randomization law, support definition, or scientific result.

## Authorized transport repair

Do **not** rerun C0.

Use the exact successful Actions artifact above as source authority. The transport-repair workflow must:

1. download that exact artifact;
2. verify the raw C0 SHA-256 and `MANIFEST.json` SHA-256 above;
3. verify the 20 trace gzip files against the successful run's `SHA256SUMS.txt`;
4. create deterministic `gzip -n -9` bytes from the exact raw `stage_c0_support.json`;
5. record both raw and gzip hashes and byte counts;
6. commit the gzip-compressed C0 support file, exact manifest, exact trace gzip files, exact successful-run SHA list/provenance, and a reconstruction README;
7. verify reconstruction by `gzip -dc` and raw SHA before commit.

No scientific executable is run during this repair.

Locally reproduced deterministic compression from the downloaded artifact before workflow creation:

- raw SHA-256: `da00a66b77a90eb36a158a9942927a27743e64aba7fac69337ff3a67424d695a`
- deterministic gzip SHA-256: `946d8f8fa61d996a548a344f7e303f804283230ce8bef0d51add473d811e4ed3`
- gzip bytes: `12780097`

The transport workflow must reproduce these exact values.

## Scientific firewall remains unchanged

The successful C0 provenance records:

- `counterfactual_R1_target_scored=false`
- `PT_generated_or_scored=false`
- `FI_generated_or_scored=false`

No Stage C R1 target scorer may be added until the exact C0 authority is permanently reconstructible from the repository.
