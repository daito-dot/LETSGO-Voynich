# Issue #196 HCPortal S0-C — solved-postcard detail outcome

Date: 2026-09-08  
Issue: #196  
PR: #197

## Frozen classification

**`HCPORTAL_POSTCARDS_NO_MACHINE_READABLE_CIPHERTEXT`**

No HCPortal postcard advances to a prospective R5 Gate 0.

## Authority

- exact tested head: `07ec6f53a6f0b273c1e1f599872aaac03414c167`
- Actions run: `34177349671`
- job: `101909297592`
- conclusion: `success`
- artifact: `issue196-hcportal-s0c`
- artifact ID: `10037705639`
- artifact ZIP SHA-256: `63fe22da51c5a79994e0f4a7f784c1c2dc5fe4e0dc0412c9900f9b34ae18fd5b`
- raw `issue196_hcportal_s0c_results.json` SHA-256: `02a950419f72767de6901abea44e220a2435516431ebf736ef6dfbc0c8f69114`

## Complete frozen S0-C population

The four records selected prospectively from S0-B metadata were all inspected by their public detail endpoints and double-fetched reproducibly:

- `1324 / pc_hcp_5`
- `1473 / pc_hcp_154`
- `1510 / pc_hcp_191`
- `1789 / pc_hcp_470`

All four have the same five-layer pattern:

| layer | all four |
|---|---|
| `CIPHERTEXT_SYMBOLS` | false |
| `PHYSICAL_LINES` | false |
| `CIPHER_UNIT_BOUNDARIES` | false |
| `PLAINTEXT_LEXICAL_BOUNDARIES` | true |
| `CIPHER_PLAINTEXT_ALIGNMENT` | false |

For each record:

- `solution.name = Solved`;
- `cipher_key_id = null`;
- exactly one explicit plaintext-role machine-readable source was present (`Solution`);
- zero explicit machine-readable ciphertext/transcription sources were present;
- no deterministic key/alignment field was present;
- cryptogram source is supplied as images, whose pixels were deliberately not accessed by S0-C.

## Interpretation

HCPortal's postcard collection is valuable for historical cipher research and provides solved plaintext for a small subset, but the current reproducible API transport does not preserve the full machine-readable chain required by this Priority-3 question. Producing that chain would require OCR/manual transcription and alignment from postcard images, which is explicitly outside the frozen admission rule.

This is a source-preservation result, not a statement about whether the original postcards visually preserve word spacing or physical lineation.

## Consequence

Stop the HCPortal postcard lane and move to the preregistered Priority-B Mary Stuart / Castelnau source-access screen. Do not repair HCPortal by manual image transcription for this program.
