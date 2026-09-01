# Issue #72 V2 — Stage B0 transport addendum

Status: **FROZEN BEFORE ANY B1 R1 SCORE**

A third transport-recovery attempt, workflow run `33463531798` / job `99718572908`, established two important facts before stopping:

1. the original Stage B0 Actions artifact downloaded successfully with artifact digest
   `0bdb5022c5c348b0898a8de253c2b644576c2654c19710059edabc79bb3b03b5`;
2. its full `stage_b0_support.json` passed the frozen SHA-256
   `96b2865496306b48a4d843b590da32b06684520e4db6a21dd0ed0b859ca27d58`.

The workflow then mechanically re-derived the intended compact authority and its frozen hash assertion passed:

`d38ab785b421bcd7eea0e48fb03d5c6f55d8f733dc662fc4793a1f7c0d161d28`

The failure occurred only at comparison with a repository-stored copy of the compact file. External scientific sources were not checked out and rep0 R1 was not computed. All later jobs were skipped.

## Final transport rule

The repository copy is no longer part of the B1 scientific authority chain.

For every authorized B1 execution:

1. download the exact successful B0 artifact from run `33462658689`;
2. verify the artifact/file hashes above;
3. mechanically derive the compact execution authority from that exact full B0 JSON;
4. verify compact SHA-256 `d38ab785b421bcd7eea0e48fb03d5c6f55d8f733dc662fc4793a1f7c0d161d28`;
5. supply that runtime-derived compact file to the unchanged B1 scientific scorer;
6. only then perform the rep0 exact Issue #68 R1 replay gate.

This removes manual file transport from the scientific authority chain entirely.

The compact authority contains only source surface identities, historical seeds, parser-support counts and the already-frozen B0 target-firewall flags. It contains no R1 target value.

## Scientific conditions unchanged

No change is made to:

- the five positive-control surfaces;
- their historical seeds;
- the 12-slot parser;
- the 66-edge statistic;
- the 1,000-reference-null calibration;
- primary/secondary reference namespaces;
- the rep0 exact replay values;
- the no-p-value rule;
- the no-intervention-R1 rule;
- the interpretation of B1 as T2 effect-scale calibration rather than a hard threshold.

Runs `33463146153`, `33463363673`, and `33463531798` are all pre-science transport failures and must remain in provenance.
