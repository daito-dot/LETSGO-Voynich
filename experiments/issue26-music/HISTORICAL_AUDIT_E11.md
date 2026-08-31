# Issue #26E11 historical audit — León / Visigothic musical cryptography

Status: **SOURCE AUDIT BEFORE EXPERIMENT DESIGN**

## Why this audit exists

E9 and E10 tested two later, relatively regular music-cipher tables as practical decoders. The next useful historical comparison should not be invented from Voynich state counts. It should come from a genuinely attested pre-Voynich music-as-cipher mechanism.

The León / Visigothic tradition is substantially earlier and better suited to that purpose, but it is also structurally different from the Philip and Sloane systems.

## Source anchors

Primary modern scholarship:

1. Elsa De Luca, “Musical Cryptography and the Early History of the ‘León Antiphoner’,” *Early Music History* 36 (2017), DOI `10.1017/S0261127917000018`.
2. Elsa De Luca & John Haines, “Medieval Musical Notes as Cryptography,” in *A Material History of Medieval and Early Modern Ciphers* (Routledge, 2017/2018), DOI `10.4324/9781315267449-2`.
3. Elsa De Luca, “Musical cryptography: an elitist code for Visigothic scribes,” author presentation/booklet, Universidade NOVA de Lisboa.

The De Luca/Haines survey catalogs a substantial body of León-area charters and a small number of liturgical codices containing musical cryptography. In liturgical manuscripts the practice is concentrated around León c. 902–920; charter use continues later. The León Antiphoner cryptography itself is used in De Luca's dating/history argument and is not a hypothetical reconstruction.

## Mechanism actually supported by the historical evidence

The surviving system is **not** a fixed pitch/rhythm table analogous to Philip or Sloane.

The attested mechanism is closer to a substitution alphabet whose ciphertext signs are drawn or adapted from musical-neume paleography:

- ordinary alphabet letters are replaced by neume-shaped or neume-like signs;
- some signs are genuine musical/neumatic shapes;
- others are distorted representations of alphabetic letters made to look like musical notation;
- a broad/common cryptographic alphabet can be recognized across sources, but scribal implementation is not rigid;
- the same plaintext letter can have more than one cipher sign, including within one inscription;
- signs can be rotated/transversely written;
- genuine ordinary letters can occasionally appear within cryptographic text.

Thus the historically justified computational abstraction is **symbol substitution / occasional homophony with musical-looking glyphs**, not a sequence of musical pitches or a low-dimensional 5×4/5×5 product.

## Concrete León MS 22 alphabet evidence

De Luca/Haines Table 1.2 catalogs the cryptographic alphabet used in León, Archivo de la Catedral, MS 22. The text layer of the published table identifies categories including direct medieval-music-note ciphers and distorted-note ciphers. The graphic shapes themselves are essential and are not safely recoverable from plain-text extraction alone.

The associated fol. 90r inscription has a known Latin reading beginning with the book identifying itself as belonging to Saints Cosmas and Damian in the territory of León. This confirms that at least one historical use is a true symbol-for-Latin-text cipher.

The important methodological point for E11 is therefore available even without pretending to possess a machine-readable shape table: **the carrier mechanism is substitution of visible symbols for Latin letters**.

## Why E11 will not invent a León→Voynich shape key

A direct glyph-shape mapping would require the actual paleographic sign images and an independently frozen image-similarity rule. The sources also show real scribal variation and homophony. Creating a hand-picked mapping from Voynich glyphs to León glyphs now would introduce too much post-hoc freedom.

E11 therefore does **not** claim that a Voynich glyph visually equals a specific León cipher sign.

Instead it tests a mechanism-level consequence that is invariant to the decorative shape of the signs:

> If Voynich running text were produced by the same basic kind of cipher — one visible neume-like symbol standing for one plaintext letter under a manuscript-wide substitution key — then a single symbol→Latin-letter key fitted on some leaves should decode untouched leaves into ordinary medieval-Latin character statistics and should remain stable across physical-leaf folds.

This is exactly the property a substitution cipher preserves and does not require choosing a visual correspondence after seeing plaintext quality.

## Martinus Polonus 1277 audit

A secondary web/gallery source attributes a 1277 musical cipher to Martinus Polonus and points to David A. King, *The Ciphers of the Monks* (2001), p. 114.

During this audit the exact 1277 cipher key could **not** be independently reconstructed from a scholarly/public machine-readable source. Searches recover the attribution and King's bibliographic pointer, but not a sufficiently auditable symbol→letter table.

Therefore E11 does **not** execute a Martinus decoder and does not infer a key from screenshots or secondary descriptions. If the exact table is later recovered from a reliable facsimile/source, it can become a separate frozen practical-decode probe.

## Implication for the research tree

León changes the useful music-cipher question.

The next experiment should not ask whether another arbitrary 20/25-cell product fits Voynich. It should ask whether the **historically real pre-Voynich mechanism of musical-looking monoalphabetic substitution** can actually recover stable held-out Latin from the visible Voynich sign stream.

That is the target of `PLAN_E11.md`.
