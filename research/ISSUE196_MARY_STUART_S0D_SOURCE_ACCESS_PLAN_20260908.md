# Issue #196 — Mary Stuart / Castelnau S0-D public source-access screen

Date: 2026-09-08  
Status: **FROZEN BEFORE AUTOMATED SOURCE-LOCATOR EXECUTION — SCORE-FREE**

## Trigger

The HCPortal postcard lane stopped at S0-C because solved records expose plaintext solutions and images but no machine-readable ciphertext transcription or deterministic key/alignment in the reproducible API transport.

The preregistered Priority-B source is the Mary Stuart / Castelnau corpus deciphered by George Lasry, Norbert Biermann, and Satoshi Tomokiyo.

## Prior external facts fixed before locator execution

The open-access Cryptologia article, DOI `10.1080/01611194.2022.2160677`, establishes that:

- more than fifty previously unidentified BnF cipher letters were deciphered;
- the working corpus contains more than `150,000` ciphertext symbols;
- the team manually transcribed the graphical ciphertexts with the CrypTool transcription GUI;
- `219` distinct graphical symbol types were identified;
- a Mary–Castelnau cipher table was reconstructed;
- the paper provides deciphered plaintext for the corpus at varying levels of detail and reproduces some letters in full;
- seven newly deciphered letters have independently surviving plaintext copies in British archives;
- the paper explicitly says the plaintext shown for F38 is **reformatted with spaces and punctuation**, so paper plaintext formatting is not treated as source-preserved ciphertext grouping/alignment.

The current public CrypToolProject/CTTS `main` authority is frozen to commit:

`d8b7d77b4e12e7a22d3980f8b5fb4e44c773287b`

The repository README states that CTTS was used to decipher the Mary Stuart letters, but a pre-locator tree-name check found no path containing `Mary`, `Castelnau`, or `F38`. S0-D verifies this from the pinned tree in Actions rather than treating chat history as authority.

## Question

Is the **machine-readable scholarly transcription/key/alignment dataset actually reproducibly retrievable today** from a public source linked to the paper/project, without manually transcribing manuscript images or reconstructing the authors' working database?

This stage does not yet test line/group semantics. A positive source locator merely licenses a subsequent structural Gate 0.

## Frozen public source channels

S0-D may inspect only these externally motivated channels:

1. DOI / publisher metadata for `10.1080/01611194.2022.2160677`;
2. the public full-article page and its explicit hyperlinks, if automated access is allowed by the publisher;
3. Crossref metadata for the DOI;
4. current pinned `CrypToolProject/CTTS` repository tree and README;
5. GitHub public-code search restricted to `CrypToolProject` and `GeorgeLasry` for the exact source identifiers below;
6. Zenodo public API exact-title/DOI search;
7. public links explicitly discovered from channels 1–6 whose host is one of: `github.com`, `raw.githubusercontent.com`, `zenodo.org`, `figshare.com`, `osf.io`, `cryptiana.web.fc2.com`, `cryptiana.blogspot.com`, `de-crypt.org`, `decryptproject.eu`, `de-crypt.org`, `gallica.bnf.fr`, `bnf.fr`, `tandfonline.com`.

No general web crawling after reveal and no private/authenticated author storage is allowed as a rescue.

## Frozen exact search identifiers

Case-insensitive source-name/path/title queries are fixed to:

- `Mary Stuart`
- `Castelnau`
- `Mary-Castelnau`
- `F38`
- `fr. 2988`
- `2988 f.38`
- `20506`
- DOI `10.1080/01611194.2022.2160677`
- exact article title `Deciphering Mary Stuart’s lost letters from 1578-1584` plus ASCII apostrophe/hyphen normalization.

A generic occurrence of the word `mary` inside source code does not count; the hit must be source-role relevant by path/title/context.

## What counts as a positive machine-readable source candidate

A located artifact/link must be explicitly identified by surrounding source metadata, filename/path, title, or host record as at least one of:

- ciphertext transcription;
- CTTS project/transcription export;
- decryption key / nomenclator mapping;
- aligned cipher/plaintext data;
- corpus data/archive containing the Mary–Castelnau letters.

A paper PDF/HTML, manuscript image/IIIF record, figure image, news article, generic CTTS software binary/source code, or plaintext-only historical edition does **not** count.

The locator may archive candidate URL host/path, link text, filename, repository path, API record title/ID, byte size/content type if fetched, and SHA-256 of candidate machine-readable files. It must not compute ciphertext statistics.

## CTTS repository audit

Checkout exactly `CrypToolProject/CTTS@d8b7d77b4e12e7a22d3980f8b5fb4e44c773287b`.

Archive:

- commit identity;
- all path names matching the frozen source identifiers;
- text-file content hits for `Mary Stuart`, `Castelnau`, `Mary-Castelnau`, `F38`, `2988`, or `20506`, with file path and a bounded 240-character context only;
- classify README/article-reference hits separately from data-bearing hits.

Files under documentation screenshots/images cannot count as machine-readable corpus data.

## Publisher/Crossref link audit

For the DOI article:

- retrieve Crossref JSON twice and require stable DOI/title identity;
- attempt publisher HTML twice with a browser-like user agent; publisher blocking is reported, not treated as corpus-data absence by itself;
- extract explicit `href` values whose link text/URL contains `supp`, `data`, `dataset`, `transcript`, `download`, `github`, `zenodo`, `figshare`, `osf`, `decrypt`, `cryptiana`, or a frozen source identifier;
- do not follow manuscript-image or generic article-format links as data candidates.

## Zenodo audit

Use the public Zenodo records API with the exact DOI/title/Mary-Castelnau queries. Report every returned record title/DOI/ID symmetrically. A record only counts if its metadata explicitly identifies the corpus/transcription/key/alignment role.

## Frozen S0-D classifications

- `PUBLIC_MACHINE_READABLE_MARY_CASTELNAU_SOURCE_LOCATED` — at least one reproducible public artifact is explicitly source-role relevant and contains machine-readable ciphertext/transcription/key/alignment data.
- `SOURCE_NOT_REPRODUCIBLY_ACCESSIBLE` — all frozen channels execute sufficiently to establish that only article/manuscript-image/software references are public and no machine-readable scholarly corpus artifact is located.
- `SOURCE_ACCESS_SCREEN_INDETERMINATE` — critical channels fail in a way that prevents the negative classification (for example Crossref plus CTTS plus both GitHub/Zenodo discovery channels unavailable).
- `INVALID` — locator implementation/source-identity failure.

A positive result licenses a new five-layer structural Gate 0 before any R5 score. A negative result stops Mary–Castelnau for the main Priority-3 lane and moves to the already-preregistered DECRYPT/HistoCrypt paired shared-task source screen.

## Firewall

No manuscript OCR. No manual transcription. No ciphertext adjacency/frequency analysis. No R5. No Voynich access. No author contact/private share as a post-reveal rescue. No weakening of the five-layer requirement.
