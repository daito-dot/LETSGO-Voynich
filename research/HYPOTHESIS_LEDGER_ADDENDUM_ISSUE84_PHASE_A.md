# Hypothesis ledger addendum — Issue #84 Phase A

Status: **COMPLETE / FROZEN**. Authority: `experiments/cross-linguistic-baselines/PLAN_A.md`, `REPORT_A.md`, `first-reveal/phase84a_results.json` (SHA-256 `86d18560b5999836b7c0d22fa9c3d8dbfd9f11ba246613fd0c2527d5ed5ffe1c`).

## H84-A-LANG — some natural language, written as prose, falls inside the Voynich regime of inter-token dependence and repeat clustering

**REFUTED for 101 languages (parallel Bible, first 32,570 NT tokens each).** Null-corrected adjacent-token mutual information: Voynich readings `0.053–0.111` bits; languages `0.173–1.584` (median `0.82`). No language meets the joint frozen criterion. Frozen class `NO NATURAL LANGUAGE IN VOYNICH REGIME`.

## H84-A-TX — the Voynich regime depends on the EVA/ZL transcription lineage

**REFUTED.** ZL3b, IT2a, VT0e, RF1b (EVA family), GC2a (v101), CD2a (Currier) and FG2a (FSG) all lie below every language on adjacent MI and have non-positive far-bin excess. Frozen class `VOYNICH REGIME TRANSCRIPTION-ROBUST`.

## Recorded limitations and descriptive findings

- The frozen far-bin (81–320 tokens) criterion was uninformative: 100/101 languages also show depletion there because chapters are ~660 tokens long; the classification rests on adjacent MI. The exploratory CREMMA "burstiness to 160 tokens" was a document-length effect.
- Descriptive (not classificatory): natural prose *avoids* immediate repetition (distance 1–2 excess negative in 96/101 languages, median z −18) while every Voynich reading shows *positive* excess (z +2.8…+8.5); mid-range (21–40) burstiness is present in 101/101 languages (median z +20) and absent in Voynich (−0.8…+3.4).
- Voynich vocabulary is **not** small: 6.6k–8.6k types at ~34k tokens vs language median 4.7k; held-out unseen-type rate 14–18% vs median 10%. The informal "small vocabulary" remark in earlier discussion is withdrawn.
- Character-level density (11.3–12.1 bits/token; 2.5–3.1 bits/unit) is low-middle within the language range, not extreme.

## Consequence

The OGH synthesis survives its first control-tested challenge and is restated: Voynich differs from natural prose in **how tokens relate to their neighbours** (near-zero adjacent dependence, immediate self-repetition where language suppresses it, no topical burstiness), not in per-token information content or vocabulary size. Phases B (cipher-family map) and C (genre controls) remain.
