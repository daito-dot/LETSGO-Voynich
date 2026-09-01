# Issue #72 V2 — Stage B0 repository authority corruption incident — 2026-09-01

Status: **EVIDENCE-TRANSPORT CORRUPTION / SCIENTIFIC SOURCE ARTIFACT RECOVERED / PRE-PT-TARGET**

## Summary

The repository copies of `stage_b0_support.json` were found to be malformed JSON during Stage D PT target-blind preflight. This is an evidence-transport/storage defect, not a Stage B0 scientific computation failure and not a PT result.

The original successful Stage B0 Actions artifact has been recovered and independently validated as intact.

## Original Stage B0 first target-blind authority

- workflow run: `33462658689`
- workflow conclusion: `success`
- scientific head: `135e8ac956541e2c2259431efee0fdb064b9c03e`
- artifact ID: `9783720673`
- artifact name: `issue72-v2-stageB0-support-135e8ac956541e2c2259431efee0fdb064b9c03e`
- artifact ZIP digest reported by GitHub: `sha256:0bdb5022c5c348b0898a8de253c2b644576c2654c19710059edabc79bb3b03b5`
- exact raw `stage_b0_support.json` SHA-256 from artifact: `96b2865496306b48a4d843b590da32b06684520e4db6a21dd0ed0b859ca27d58`
- exact `stdout.txt` SHA-256: `426b07f1fbae59f9fd110716b5763ff1f1f47e3a8da6dfb2ebfaa0623677c8fa`

The recovered artifact `stage_b0_support.json` parses successfully as JSON. Its `PROVENANCE.txt` states:

- `rep1_rep4_R1_scored=false`
- `issue72_intervention_R1_scored=false`

The original workflow itself enforced the complete rep0..rep4 population, all target-access flags false, exact historical rep0 pooled surface SHA, rep0 visible/accepted counts, and the historical seed law before artifact upload.

## Corrupted repository copies

### First archived repository copy

- add commit: `2329f8da5c55776cc1e0b63af2b691798b429134`
- blob: `30713b1dbe23f36545d22aa51e1c8925fc6e4a3d`
- malformed JSON at end (`JSONDecodeError`, char 23725 in audit workflow)

This copy also contains evidence of manual/transcription corruption in nested fields (for example `acccepted`). It is not authoritative over the original Actions artifact.

### Later attempted repository repair

- repair commit: `350463fcf696446a0bc995b000b03c4b7db44a1d`
- blob: `f6bc24fe6882e1071d9aaa04495168b15601dde3`
- whole-file SHA-256: `99dbf2143b2ad276e054b794980014d89ec79c83041d61d011319b1e87f0225d`
- malformed/truncated JSON at char 11176

This repair is superseded as evidence authority.

## Detection chronology

1. Initial Stage D0 run `33486372047` stopped before PT surface generation because D0 expected the original artifact SHA `96b286...` but repository bytes had changed.
2. Updating the expected SHA to the repository copy exposed that the current repository JSON itself was malformed.
3. Target-blind PT preflight run `33486920603` failed before Naibbe PT execution while parsing B0.
4. Target-blind B0 regeneration workflow run `33487240118` successfully regenerated a valid B0 JSON from the frozen generator, but its attempted comparison to the malformed historical repository copy failed while parsing that copy.
5. The original Stage B0 Actions run/artifact was then located and recovered intact.

No step above loaded a PT Voynich target or computed PT pair-Q, residual-Z, E/W, topology correlation, sign agreement, or PT R1 statistic.

## Recovery rule

The recovery authority order is:

1. original successful target-blind Stage B0 Actions artifact (`9783720673`);
2. exact frozen B0 generator + pinned CREMMA/Naibbe authorities as an independent deterministic reconstruction check;
3. repository transport copies only after exact equality with (1) is verified.

A recovery workflow must regenerate B0 from the frozen generator and require **byte-for-byte equality** with the recovered original artifact before replacing repository `stage_b0_support.json`.

No missing/truncated JSON bytes may be guessed or hand reconstructed.

## Scientific effect

**None.**

This incident changes no Stage D scientific question, PT permutation law, intervention population, RNG-block population, source panel, mechanism authority, parser policy, D1 measurement, or interpretation boundary.
