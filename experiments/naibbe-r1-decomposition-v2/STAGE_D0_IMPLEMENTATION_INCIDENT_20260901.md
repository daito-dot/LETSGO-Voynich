# Issue #72 V2 — Stage D0 implementation incident — 2026-09-01

Status: **SCIENTIFIC NO-OP / PRE-TARGET / PRE-PT-SURFACE**

Initial Stage D0 workflow run:

- run: `33486372047`
- scientific/support head: `5a00d9287a7fdbd1743f22b932fd5d97901f6e36`
- representative failed job: `99787331482` (`support (0,0)`)
- failed step: `Generate exact target-blind PT surface`

## Exact failure

The D0 implementation carried forward the Stage B1-era expected whole-file SHA-256 for `stage_b0_support.json`:

`96b2865496306b48a4d843b590da32b06684520e4db6a21dd0ed0b859ca27d58`

Current GitHub authority has SHA-256:

`99dbf2143b2ad276e054b794980014d89ec79c83041d61d011319b1e87f0225d`

The current file is the later repository repair from commit:

`350463fcf696446a0bc995b000b03c4b7db44a1d` — `Issue72 V2: repair exact Stage B0 artifact bytes`.

The workflow stopped in `load_b0_authority()` on this byte-identity assertion.

## Firewall status

The failure occurred before:

- loading the Naibbe Python module for execution;
- reconstructing a paired baseline;
- generating any PT surface;
- loading any ZL3b/IT2a target;
- computing pair-Q, residual-Z, E/W, target topology, sign agreement, or any R1 statistic.

Therefore this run reveals no PT scientific outcome and creates no target leakage.

## Authorized recovery

Recovery is limited to updating the expected whole-file B0 byte authority to the current repaired repository bytes.

The following are **not changed**:

- Stage D scientific question;
- PT hash-order randomization law;
- 31 assignments;
- rep0..rep4 block population;
- seed rule;
- source panel;
- effective-letter projection;
- published Naibbe codebook/defaults/output view;
- parser policy;
- no-reroll/no-drop rule;
- D1 estimand or target firewall.

D0 will still independently regenerate each unchanged paired baseline and require exact Stage B0 primary/raw surface identities, token support, and ambiguity-retry counts. The byte-SHA repair therefore does not substitute for scientific baseline replay.
