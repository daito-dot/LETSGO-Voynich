# Issue #72 V2 Stage C0 permanent archive

This directory is the size-safe repository archive of the scientifically successful target-blind C0 artifact from Actions run `33468199347`, job `99732343946`, scientific head `d21ce72c756ab9ed09ee58302366b2df9ea692c2`.

The raw scientific file was not altered semantically. It is stored as deterministic gzip because the exact raw JSON is 206,486,933 bytes and GitHub rejects single files above 100 MiB.

## Exact identities

- Actions artifact: `9785652875`
- artifact ZIP SHA-256: `c642519356f477441dcbb7d910988966a0c1c2b661e03be5cee078564e1426da`
- raw `stage_c0_support.json` bytes: `206486933`
- raw SHA-256: `da00a66b77a90eb36a158a9942927a27743e64aba7fac69337ff3a67424d695a`
- deterministic `gzip -n -9` bytes: `12780097`
- gzip SHA-256: `946d8f8fa61d996a548a344f7e303f804283230ce8bef0d51add473d811e4ed3`
- `MANIFEST.json` SHA-256: `aba822be57bbac0c04a9fa785a0a835eafe192b406fead5cd7166051825f45ae`

## Reconstruction

`gzip -dc stage_c0_support.json.gz > stage_c0_support.json`

Then require:

`sha256sum stage_c0_support.json`

to equal:

`da00a66b77a90eb36a158a9942927a27743e64aba7fac69337ff3a67424d695a`.

`SCIENTIFIC_SHA256SUMS.txt` and `SCIENTIFIC_PROVENANCE.txt` are copied byte-for-byte from the successful scientific artifact. The SHA list contains the original runner prefix `/tmp/issue72-c0/`; relocate that prefix to the reconstruction directory when verifying archived files.

## Scientific status

C0 is target-blind. Its provenance freezes `counterfactual_R1_target_scored=false`, `PT_generated_or_scored=false`, and `FI_generated_or_scored=false`.
