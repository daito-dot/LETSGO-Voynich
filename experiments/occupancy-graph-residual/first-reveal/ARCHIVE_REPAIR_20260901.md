# Issue #64 first-reveal permanent-copy integrity repair

Status: **archive transport copy repaired; scientific first reveal unchanged**.

During Issue #58D preflight, reconstruction of the permanent base64/gzip copy failed CRC verification. The original GitHub Actions first-reveal artifact was still available and was used as the independent authority for repair.

Verified original authority:

- original Actions artifact ID: `9776775160`
- original artifact ZIP SHA-256: `ed3c28b214ed78b9c19a67182eac7e867e51bc3e13ef4ee6c778ef329f9a7650`
- exact raw JSON SHA-256: `fba60daea6e30682065900a4cf15d53d2a2f536d933b588fae447fb43bb4728d`
- deterministic gzip SHA-256: `666cfa3e211b097b30025a7947cf8bbb22e1bf24cae18a55d99017328b511d4f`

Rebuilding all eight intended 8,192-byte base64 chunks from the verified original showed that parts 00–05 and 07 already matched their expected Git blobs. Only part06 differed:

- corrupted stored part06 blob: `8fd93462e2a8a07f422e83eeec5aed850e9194a0`
- correct rebuilt part06 blob: `bb0487406575344bb300207c40967fbd3d6453e6`

This repair replaced only part06. Repository reconstruction was then verified end-to-end back to the frozen deterministic-gzip and raw-JSON hashes above.

Repair workflow run: `33449531393`.

The scientific result, first-reveal run, first-reveal raw bytes, frozen classification, and all numerical interpretations are unchanged. This is solely a repair of the later text-transport copy used for permanent repository storage.
