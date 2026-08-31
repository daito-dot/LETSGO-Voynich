# Issue #58A exact first-reveal archive

This directory preserves the exact raw JSON bytes produced by the audited first reveal, compressed deterministically with `gzip -n -9`.

- GitHub Actions run: `33399104345`
- job: `99510744309`
- PR: `#60`
- audited branch head: `d0588651870f7cb818b74e2d9402bec3c103f412`
- plan commit: `84243646f5276ed1959f41f2e4c179c7357ead87`
- executable commit: `37968752114524de1ac4aa0c21489d55cbaa5239`
- source Git blob: `2a4533ab9bdfa85db9bad602d590978953055df1`
- artifact ID: `9760539131`
- artifact name: `issue58a-occupancy-graph-66674e1a69b013cb398f0d2b3a69b991100d4739`
- artifact ZIP digest reported by GitHub: `sha256:4dafa489e591a92c0f94a8c9416186fe5f25512d0b1d41a99e52c203b31b8eb6`
- raw JSON SHA-256: `ae0db7dc72cb890a325ef5313a3375a43efde7c27c9bd5b3fcb0632fb808e152`
- archived gzip SHA-256: `14964650cc8efee3fb851e0ea31e60a52007e3968b3ba92446aa51ad15f88803`

To verify the raw result later:

`gzip -dc issue58a_results.json.gz | sha256sum`

Expected raw SHA-256: `ae0db7dc72cb890a325ef5313a3375a43efde7c27c9bd5b3fcb0632fb808e152`.
