# Issue #72 V2 — Stage D0 corrected-preflight B0 authority incident (2026-09-01)

Status: **SCIENTIFIC NO-OP / PRE-TARGET / PRE-PT-SURFACE**

## Incident

The corrected target-blind PT preflight at head

`e2eacdf000b08d3244ce1bb5219b493ceca6a2e6`

workflow run `33486920603` reached `d0_pt_support72_v2.py::load_b0_authority()` and failed while parsing the repository copy of `stage_b0_support.json`:

`json.decoder.JSONDecodeError` at byte/character offset `11176`.

Representative failed job: `99789054062` (`j=30`, `rep=4`).

The failure occurred before:

- unchanged baseline regeneration;
- PT plaintext permutation;
- PT ciphertext generation;
- pair-Q computation;
- residual-Z computation;
- ZL3b/IT2a target loading;
- any R1 topology score or rank.

Therefore no PT scientific result was revealed and no intervention outcome exists from this run.

## Root cause class

The repository copy of Stage B0 authority had been manually repaired after archival. Its whole-file SHA was changed from the earlier expected authority to `99dbf2143b2ad276e054b794980014d89ec79c83041d61d011319b1e87f0225d`, but the repaired file was not valid JSON.

A subsequent attempted repair workflow (`33487240118`, head `80f247e94a8fdcc0807c6d31a5ab32af7957f904`) successfully regenerated Stage B0 from the frozen generator and frozen external authorities, but its comparison step selected commit `083f5c161c45da09a41346dfe16094f79380a531` as the historical comparison file. That comparison copy was itself not valid JSON, so the workflow stopped before replacing repository authority.

This second failure also occurred entirely before PT generation or target access.

## Recovery authority

The recovery reference is not the damaged archive lineage. It is the Stage B0 file present at the **successful Stage B1 scientific head**:

`398d5a9d6c32052405e26533e45c7c2ed705e627`.

That exact B0 was consumed by the successful Stage B1 scorer, whose frozen implementation requires:

`SHA256(stage_b0_support.json) = 96b2865496306b48a4d843b590da32b06684520e4db6a21dd0ed0b859ca27d58`.

Recovery is authorized only if all of the following hold before replacement:

1. the B1-head file parses as JSON;
2. its SHA-256 is exactly `96b2865496306b48a4d843b590da32b06684520e4db6a21dd0ed0b859ca27d58`;
3. the frozen `b0_support72_v2.py` blob remains `ef3144591839395c18e1bdf308311bf99562bf9a`;
4. fresh target-blind regeneration from pinned CREMMA `292525969ad98380b398e6606a9c2a36d51913ae` and pinned Naibbe `f2675ec5dd275268bc64dd48ea64fc0e0e9827a2` is byte-for-byte identical to the B1-head B0 authority;
5. no target vector or R1 statistic is loaded during repair.

If any condition fails, recovery must stop rather than choose fields manually.

## Scientific design remains unchanged

This incident does **not** authorize changes to:

- Stage D PT scientific question;
- line-wise character-multiset-preserving permutation law;
- assignments `j=0..30`;
- RNG blocks `rep0..rep4`;
- cipher seeds;
- Naibbe codebook/defaults/output view;
- SlotParser policy;
- D1 R1 metric or target readings;
- B2 effect-size context;
- interpretation map.

The only permitted recovery is restoration of the exact valid Stage B0 authority bytes already used by successful Stage B1, followed by a fresh target-blind D0 preflight.
