# Issue #72 V2 Stage B1 — provenance

Scientific/calibration workflow:

- run: `33463625070`
- exact scientific head: `398d5a9d6c32052405e26533e45c7c2ed705e627`
- rep0 exact-gate job: `99718846598`
- aggregate job: `99719495544`

Gate condition:

- exact successful B0 artifact from run `33462658689` downloaded at runtime;
- full B0 JSON SHA-256 verified: `96b2865496306b48a4d843b590da32b06684520e4db6a21dd0ed0b859ca27d58`;
- runtime compact B0 authority mechanically re-derived and SHA-256 verified: `d38ab785b421bcd7eea0e48fb03d5c6f55d8f733dc662fc4793a1f7c0d161d28`;
- rep0 exact Issue #68 R1 coordinates reproduced before rep1–rep4 were authorized.

Final aggregate artifact:

- artifact ID: `9784131519`
- artifact name: `issue72-v2-stageB1-recovery2-calibration-398d5a9d6c32052405e26533e45c7c2ed705e627`
- artifact ZIP SHA-256: `143731f7e430f3cea5c878890852ae24de4917ea9fa73eb3166330c1ff541fd5`
- artifact size: `23,253` bytes
- aggregate `stage_b1_calibration.json` SHA-256: `b37d285b25d17623fa19910ff3f8f4586846bb8f19825c3dbdd6e8b19bb2e31d`
- aggregate JSON bytes: `44,780`
- aggregate stdout SHA-256: `ae635b84a52d9ab16d50fb3175fde312558284c47f515e89e4e3a8915da67967`

Per-rep exact JSON SHA-256:

- rep0: `43531593d1cee752df26ae650000b5fdbcf1244021d8e75afb8eda06d3d7855e`
- rep1: `11477eb78175a541796f64ec635e7dc4741396bb01e5f1c74224a21315599045`
- rep2: `7e1951a9000dc13f52eb22f7f05e7c5872c0891f3c2fafeb21e3b04b759f5a90`
- rep3: `c514e7ba1ab28acdee2ad0819165ec30b3d36fb80d4bff4dba693e025142711d`
- rep4: `e793519fe147865af57d793169e0236932ac7fa659ee9d6e05cc8063ecba2048`

Per-rep Actions artifact ZIP digests:

- rep0 artifact `9784112606`: `083e55d956ed2fa9014aff58382a7b8229d1c39900279f67073aed4d3f4c6670`
- rep1 artifact `9784117674`: `272e8472a3c1c0908bb869b444d57ac84bade09d1e2ac89fd0d0299f23b7ddf0`
- rep2 artifact `9784121547`: `a072a9503da11de8aea8688b683b66b9abb928f99d3da9a659f982a6839f36d2`
- rep3 artifact `9784117311`: `871fa0dc128175d0609ab6f255f0e4a73c99926cd30d0672b2e6c33f0c086e02`
- rep4 artifact `9784122089`: `f8d1064a9924a0803688781ac92e468da1b28997695dbdd7f97b9d1ba195ae4d`

Scientific firewall frozen in final artifact:

- `test_nulls_computed=false`
- `B1_p_values_computed=false`
- `issue72_intervention_R1_computed=false`
- `hard_intervention_threshold_derived=false`

B1 is therefore an unchanged-mechanism positive-control calibration, not an intervention reveal.

## Pre-science transport failures retained

The following runs failed before any B1 R1 calculation and remain part of provenance:

- `33463146153` / `99717392292` — repository B0 JSON hash mismatch;
- `33463363673` / `99718069215` — repeated repository transport mismatch;
- `33463531798` / `99718572908` — original B0 artifact/full hash and runtime compact hash passed, but repository compact-copy byte equality failed.

The final successful run removed repository file copies from the scientific authority chain and derived B0 execution authority directly from the exact successful B0 Actions artifact.
