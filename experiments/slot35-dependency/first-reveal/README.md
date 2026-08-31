# Issue #55 first-reveal archive

The original GitHub Actions artifacts for Issue #55A/#55B have 90-day retention. This directory stores deterministic `gzip -n` archives of the exact raw JSON bytes recovered from those first-reveal artifacts so the primary results remain reconstructible after Actions artifact expiry.

## #55A

- Actions run: `33393775999`
- artifact ID: `9758673652`
- artifact ZIP SHA-256: `b05e1237e5bcab5c25906a7c039f680b49b56cd2b7b2bc467538019f1f42aa6f`
- exact raw JSON SHA-256 after decompression: `a9a09260f136f2fbdee42186e7992c91a21ce2eba568aca38f57459ab8462e8c`
- archived gzip SHA-256: `4457ec1fbad97926ccd51d90c61249d596ddc5911f063d69336559e8b4741dc2`
- file: `issue55a_results.json.gz`

## #55B

- Actions run: `33394659964`
- artifact ID: `9758969505`
- artifact ZIP SHA-256: `0411671f38515dcd1be0c434bb2e3068ae1c4db53a0c941cb212e95702b63ba6`
- exact raw JSON SHA-256 after decompression: `46dbd7a40b8585f97063ba60b38f0e98f4801ff6e8e7d9c882de13b6762d77d0`
- archived gzip SHA-256: `039e5c4a17bb5e82b9c7b2acccc8834c5200eec89b501c105bec89d44c45c1ef`
- file: `issue55b_results.json.gz`

## Verification

Example:

```bash
gzip -dc experiments/slot35-dependency/first-reveal/issue55a_results.json.gz | sha256sum
gzip -dc experiments/slot35-dependency/first-reveal/issue55b_results.json.gz | sha256sum
```

The resulting hashes must match the exact raw JSON SHA-256 values above. The compact `RESULT_A_RECORD.json` and `RESULT_B_RECORD.json` files are navigation/provenance summaries; these gzip files preserve the exact first-reveal JSON bytes.
