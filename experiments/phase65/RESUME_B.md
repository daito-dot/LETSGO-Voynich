# Phase 65B GitHub-only resume checkpoint

Status: **ACTIVE — Phase65B0 source freeze PASS; text-blind crop freeze is the next gate.**

Purpose: this file is an operational checkpoint so a fresh agent can resume the current Phase65B work from GitHub alone, without relying on chat history or local scratch files.

## Authority and branch

- repository: `daito-dot/LETSGO-Voynich`
- accepted base main before Phase65B implementation: `8feb1a6d5b4b01a9b8256b896d443ea13ec4fc20`
- active implementation branch: `phase65b-image-label-science`
- checkpoint parent head before this file: `905dfb1b6d86822d2d9af4a940c856b7b7ecdf47`
- normative experiment design: `experiments/phase65/PLAN_B.md`
- exact source freeze: `experiments/phase65/SOURCE_MANIFEST_B.json`
- B0 audit/provenance: `experiments/phase65/PREFLIGHT_B0.md`
- source-only executable: `experiments/phase65/phase65b_source_preflight.py`
- source-only workflow: `.github/workflows/phase65b-source-preflight.yml`

Before doing any work, re-fetch current `main`, this branch head, open PRs and Actions. Treat current GitHub as descriptive authority and `PLAN_B.md` as normative authority. Do not trust the SHAs in this checkpoint if GitHub has moved.

## Completed on Phase65B

### B0 source-only preflight — PASS

Exact successful execution:

- scientific/source-preflight head: `1e6aa9824084dadec2bd43b65da9f7f47d3e1cbb`
- Actions run: `33345560254`
- job: `99348878636`
- artifact: `9741863634`
- artifact ZIP SHA-256: `9104f0aec5829fff0c69e9bbd188d474353ce07d161feb1a5b05d80db058cd5a`
- generated source-manifest SHA-256: `71023a2c395ad95848697e866373541deb1beb02dfbfaaabcd21140293775a56`

Frozen source identities include:

- ZL3b SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`
- IT2a SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`
- DINOv2 ViT-S/14 weights SHA-256 `b938bf1bc15cd2ec0feacfe3a1bb553fe8ea9ca46a7e1d8d00217f29aef60cd9`
- Yale f100v image ID `1006249`, SHA-256 `72637b9770f40f7a8ff6b96a551e64775e88994ae69bafec0b43d48974364c33`
- Yale f102v2 image ID `1006252`, SHA-256 `8cdb1030d805b968932146124915cb0d86f7abf853167ffec028b59599820fad`

No DINO embedding, image↔text association, text distance, correlation or permutation statistic was computed during B0.

### Frozen transcription consequence

The 25 preregistered physical loci resolve to:

- f100v T.1–T.4 -> ZL3b f100v.1–4
- f100v M.1–M.5 -> ZL3b f100v.5–9
- f100v B.1–B.4 -> ZL3b f100v.10–13
- f102v2 L2.1–L2.7 -> ZL3b f102v2.10–16
- f102v2 L3.1–L3.5 -> ZL3b f102v2.25–29

The already-frozen confidence firewall excludes exactly:

- `L2.7 / f102v2.16`, reading `to[d:?]?`, because it contains both an alternative and `?`.

Pre-crop eligible population:

- f100v: 13/13
- f102v2: 11/12 = L2 6 + L3 5
- combined: 24/25

This exclusion happened before any Phase65B association result.

## Current exact frontier

**Do not run the scientific image↔label statistic yet.**

The next required operation is the text-blind crop freeze defined in `PLAN_B.md`:

1. Retrieve the exact Yale images whose hashes are frozen in `SOURCE_MANIFEST_B.json`.
2. Select one integer `(x, y, width, height)` rectangle for each still-eligible plant fragment using visible image/layout geometry only.
3. Each crop must contain exactly the intended plant fragment and no associated label glyphs.
4. Record page-edge/fold/other-plant quality flags and crop PNG SHA-256.
5. Apply only the preregistered image/layout-quality exclusion rule; never inspect label similarity to decide a crop/exclusion.
6. Freeze the result as `experiments/phase65/CROP_MANIFEST_B.json` before any association score.
7. Verify coverage firewall from `PLAN_B.md` before continuing.

Some contact-sheet/grid images were produced locally while beginning crop inspection, but they were not frozen in GitHub and are **non-authoritative disposable aids**. A restart does not need them: regenerate any visual aids deterministically from the frozen Yale source images. No crop rectangle had been accepted/frozen when this checkpoint was written.

## After crop freeze

Proceed in this order, without changing the frozen scientific design:

1. Build/run a **synthetic-only** implementation preflight proving parser, DINO forward path, preprocessing, normalized Levenshtein, Spearman aggregation and exact permutation machinery without computing P25 association outcomes.
2. Freeze deterministic implementation/dependency details.
3. Authorize the first scientific reveal on **f102v2 only**.
4. Archive raw primary result and exact provenance immediately.
5. From that point, do not change scientific code/parameters before replication.
6. Run unchanged-code **f100v replication regardless of the primary outcome**.

## Frozen primary rule reminder

Within physical rows only:

- visual distance: `1 - cosine(DINOv2 embedding_i, embedding_j)`;
- text distance: normalized unit-cost Levenshtein;
- row statistic: Spearman rho over unordered pairs;
- page statistic: pair-count-weighted row rho;
- null: exact within-row label reassignment;
- page pass: `T >= 0.20` AND exact one-sided `p <= 0.05`.

Use the effective retained row sizes after confidence/crop exclusions when enumerating the exact null. Do not preserve the originally quoted 604,800 count if an already-frozen input-quality exclusion changes a row size; the scientific null remains exhaustive permutation of the actually retained labels within each row.

## Claim boundary

Even a replicated positive establishes only local covariance between attached label form and an independently measured visual property of the attached drawing. It does not establish plant names, plaintext, language, a cipher key, N/C/G family truth, or decipherment.

A negative result rejects only this frozen morphology↔label-form relation at the tested representation/population. It does not establish semantic absence.

## Safe instruction for a new session

A new agent can be told only:

> `daito-dot/LETSGO-Voynich` をcurrent GitHubから再取得し、`phase65b-image-label-science` の `experiments/phase65/RESUME_B.md`、`PLAN_B.md`、`SOURCE_MANIFEST_B.json`、`PREFLIGHT_B0.md` を読んで、GitHubを唯一の作業コンテキストとしてPhase65Bを再開してください。過去チャットのSHAや進捗は信用せずcurrent stateを再確認してください。

That is sufficient to reconstruct the current scientific and operational state.