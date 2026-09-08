# Issue #196 — complete-preservation historical cipher corpus screening

Date: 2026-09-08  
Parent: #172  
Base main: `e293e50f15c68f1bebbca8474b0bf935533ddb70`  
Status: **SCORE-FREE SOURCE SCREENING — NO R5 EFFECT ACCESS**

## Objective

Select at most one historical ciphertext corpus for a new prospective R5 source-attribution Gate 0 using preservation architecture alone.

A candidate is not selected because it is a similar cipher family, because its surface looks Voynich-like, or because an R5 score is favorable. No R5 scorer is run in this issue.

## Fixed admission layers

A candidate must have positive external evidence for all five:

1. `CIPHERTEXT_SYMBOLS` — deterministic ciphertext atom identities;
2. `PHYSICAL_LINES` — original/source physical lineation preserved in the machine-readable representation;
3. `CIPHER_UNIT_BOUNDARIES` — independently observed grouping coarser than atom separation and suitable for terminal-unit -> initial-unit events;
4. `PLAINTEXT_LEXICAL_BOUNDARIES` — solved plaintext lexical boundaries;
5. `CIPHER_PLAINTEXT_ALIGNMENT` — deterministic key/scholarly alignment sufficient to distinguish plaintext transition, cipher transform, grouping, and physical lineation.

Failure of any one layer is sufficient to reject a transport for the Priority-3 purpose.

## Frozen screening panel

### A — HCPortal historical cryptographic postcards

Priority: **A**.

External motivation fixed before record inspection:

- Tobias Schroedel's HistoCrypt 2021 paper describes a scanned/evaluated private collection of more than 400 encrypted postcards.
- HCPortal's 2026 status paper reports a collection of 988 cryptographic postcards in its database.
- Antal et al., HistoCrypt 2026, explicitly use historical encrypted postcards, typically simple substitution ciphers, as a research dataset.
- The same 2026 paper identifies HCPortal record `pc_hcp_135` (`/dashboard/cryptograms/1454`) as a Pigpen example with six ciphertext lines plus one additional row.

Why high priority: simple substitution postcards can preserve visually meaningful word spacing and physical lines; if the portal also exposes a transcription and a solution/key, they may satisfy the five-layer requirement with substantially less transport ambiguity than symbol-only manuscript datasets.

Frozen source/API authority for score-free inspection:

- HCPortal: `https://hcportal.eu/`
- current SPA/API host inferred from the public historical frontend source: `https://api.hcportal.eu/`
- read endpoint in public frontend source: `GET api/cryptograms/{id}`
- list endpoint in public frontend source: `GET api/cryptograms?detailed=1&per_page=...`
- fixed first record for structural inspection: HistoCrypt-2026-cited record ID `1454`; this ID was fixed by the publication, not selected from API content.

The historical frontend source used only to freeze API semantics is `Blochin/HC-Portal` commit `c8e8641942dbd6c758ebe0bad3ced20c67bf393c`, where `src/utils/api.js` sets `https://api.hcportal.eu/` and `src/repository/CryptogramRepository.js` defines the read routes. Current API payloads remain authoritative for current availability.

### B — Mary Stuart / Castelnau lost letters

Priority: **B**.

External motivation fixed before data inspection:

- Lasry, Biermann, and Tomokiyo report more than 50 previously undeciphered letters, roughly 50,000 words / over 150,000 cipher symbols in public reporting, deciphered with a large nomenclator system.
- CrypToolProject/CTTS publicly records that CTTS was used in the 2022/2023 decipherment.

Required unresolved checks:

- reproducible public access to raw scholarly ciphertext transcription;
- preservation of source physical lineation;
- an independently documented cipher-unit/grouping channel distinct from symbol tokenization;
- machine-readable solved plaintext and deterministic alignment/key.

A paper or viewer alone is not enough for promotion if the complete paired data cannot be reproduced.

### C — ICDAR / DECRYPT handwritten cipher datasets

Priority: **C, expected low yield for this exact R5 question**.

The official ICDAR 2024 task description states that every cipher page was segmented into text lines and manually transcribed, but evaluation is at line level because cipher texts avoid grouping symbols into words. Therefore the competition transport itself does not license target-independent cipher-word/group boundaries.

Subclasses:

- Borg: `ALREADY_STOPPED_BY_PRIOR_GATE` (#182 transport confound).
- Copiale: `NO_INDEPENDENT_CIPHER_UNIT_BOUNDARY` from #181 Gate0.
- Ramanacoil current DECODE transport: `ALREADY_STOPPED_BY_PRIOR_GATE` (#194).
- BnF ICDAR representation: presumptive `NO_INDEPENDENT_CIPHER_UNIT_BOUNDARY` unless a separate independent solved source explicitly supplies grouping.
- Vatican/digit ICDAR representation: same rule; line transcription alone is insufficient.

No invented word segmentation is allowed.

### D — DECRYPT/HistoCrypt shared-task paired sets

Priority: **B/C exploratory**.

An independent 2026 source audit in `matthewdgreen/cipher_benchmark` notes that HistoCrypt 2020–2022 shared tasks distributed curated paired ciphertext transcriptions/plaintext solutions and may be the most benchmark-ready DECRYPT subsets. This issue may inspect them only for the five preservation layers. Paired text alone is insufficient if original physical lines or cipher-unit boundaries are missing.

### E — new independently solved sources

A source discovered during screening may enter only if external documentation already provides all five layers. It cannot enter because preliminary R5 behavior is favorable.

## Frozen screening classes

For each candidate or transport:

- `ADMIT_FOR_PROSPECTIVE_R5_GATE0`
- `NO_INDEPENDENT_CIPHER_UNIT_BOUNDARY`
- `PLAINTEXT_ALIGNMENT_INSUFFICIENT`
- `PHYSICAL_LINEATION_INSUFFICIENT`
- `SOURCE_NOT_REPRODUCIBLY_ACCESSIBLE`
- `ALREADY_STOPPED_BY_PRIOR_GATE`
- `NEEDS_SCORE_FREE_SOURCE_INSPECTION`

## Stage S0-A — HCPortal API structural inspection

The first executable inspection is fixed to record ID `1454` only.

It may retrieve and archive:

- HTTP status / content type / byte size / SHA-256;
- top-level JSON keys and recursively summarized field names/types;
- cryptogram name/category/date/language/availability if present;
- `cipher_key_id` presence;
- attachment/data-group descriptions, data item types/titles, links, image metadata, and text byte/line/whitespace statistics;
- any explicit field whose name itself indicates transcription, plaintext, solution, decryption, decipherment, key, cleartext, spacing, or lineation;
- whether attachment text is directly present or retrievable by a stable public URL.

It must **not** calculate transition statistics, symbol adjacency, terminal/initial distributions, or R5-like gains.

### S0-A decision

- If record 1454 exposes sufficient structured transcription/solution/key material to assess the five layers, freeze a population-level HCPortal query before inspecting additional records.
- If it is image/metadata only, classify record 1454 accordingly but do not infer that all 988 postcards are unavailable; proceed to a population metadata schema audit without record cherry-picking.
- If the public API is unavailable, classify HCPortal current transport `SOURCE_NOT_REPRODUCIBLY_ACCESSIBLE` for this lane and move to Priority B.

## Population selection firewall

If HCPortal advances beyond record 1454, the population filter must be frozen before listing matching record contents. Allowed filter concepts are only source metadata properties directly relevant to reproducibility/composability, such as:

- public availability;
- solved/solution attachment present;
- transcription/text attachment present;
- paired cipher key present;
- historical postcard collection/category.

No filter may use ciphertext statistics, line edge behavior, symbol frequency, apparent Voynich similarity, or desired R5 sign.

## Selection rule

At most one candidate proceeds to a new executable Gate 0. Choose the highest-priority source with positive evidence for all five layers and reproducible access. If none qualify, Priority 3 is recorded as blocked by source preservation; the five-layer standard is not weakened.

## Sources fixed for the screening record

- HCPortal: https://hcportal.eu/
- HCPortal HistoCrypt 2020 overview: https://hcportal.eu/pdf/ecp2020_171_003.pdf
- Tobias Schroedel, `Cryptographic postcards`, HistoCrypt 2021.
- Antal et al., `Solving Historical Ciphers with AI: Analysis of GPT's Capability in Processing and Deciphering Cryptographic Postcards`, HistoCrypt 2026.
- ICDAR 2024 Historical Ciphers official task page: https://rrc.cvc.uab.es/?ch=27&com=tasks
- Lasry, Biermann, Tomokiyo, `Deciphering Mary Stuart's Lost Letters from 1578–1584`, Cryptologia.
- CrypToolProject/CTTS public repository.
- `matthewdgreen/cipher_benchmark` pinned source-audit commit `729aad62d12483c549e64a2541d4f9255538c8cf`.
