# Issue #72 V2 — Stage B0 archive transport incident

Status: **TRANSPORT / REPOSITORY-ARCHIVE INCIDENT ONLY — NO B1 R1 TARGET VALUE REVEALED**

## Authoritative B0 science execution

The Stage B0 target-blind execution itself completed successfully:

- workflow run `33462658689`;
- job `99715920669`;
- artifact ID `9783720673`;
- artifact ZIP SHA-256 `0bdb5022c5c348b0898a8de253c2b644576c2654c19710059edabc79bb3b03b5`;
- exact full `stage_b0_support.json` SHA-256 `96b2865496306b48a4d843b590da32b06684520e4db6a21dd0ed0b859ca27d58`;
- B0 scientific firewall: all new R1/target/intervention access flags false.

The artifact is the authority for the full B0 output.

## Incident

Two subsequent attempts to copy the 24,094-byte JSON into the repository through a manual text/base64 transport path did **not** preserve the exact artifact bytes.

The B1 workflow correctly detected this before any R1 calculation because it required the exact B0 SHA-256.

Failed B1 runs:

1. run `33463146153`, job `99717392292`;
2. run `33463363673`, job `99718069215`.

Both stopped in `Verify B1 chronology and exact B0 archive` at the SHA-256 check.

In both runs:

- external source checkout did not occur;
- rep0 R1 exact replay did not occur;
- rep1–rep4 scoring jobs were skipped;
- aggregate was skipped;
- no new Q, residual Z, E, W, topology/sign, or R1 value was revealed.

Therefore this is not a first-reveal or scientific-score incident.

## Repair principle

Do not continue trying to duplicate the full large JSON through a lossy manual transport path.

B1 needs only the prospectively frozen surface identities, seeds, and parser-support counts. Those fields are therefore extracted mechanically from the exact Actions artifact into a compact authority manifest:

`stage_b0_authority.json`

The compact manifest contains:

- exact source run / artifact / full-JSON hashes;
- all five pooled primary surface SHA-256 values;
- all twenty manuscript×rep primary surface SHA-256 values;
- exact historical seeds;
- exact visible/accepted counts and coverage;
- B0 target-firewall flags.

It contains no new scientific score and no information unavailable in the exact B0 artifact.

The full B0 artifact remains the provenance authority. The compact file is an execution authority for B1 surface identity only.

## Scientific rule unchanged

No threshold, null, target, candidate, seed, representation, statistic, or causal interpretation is changed by this repair.

The B1 scientific firewall remains:

1. exact compact-authority hash;
2. exact rep0 Issue #68 R1 replay;
3. only then rep1–rep4 unchanged-mechanism positive-control calibration.
