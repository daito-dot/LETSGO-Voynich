# Issue #68 pretarget state

Status: **R1 FIRST REVEAL NOT YET RUN**

The target-free preflight has frozen the first tournament's candidate state:

| candidate | R1 representation | R2 | R3 | R4 |
|---|---|---|---|---|
| A1/A1-R1 | **FAIL** — coverage 0.388394 < 0.60 | PASS | PASS | not a decoder |
| Naibbe C1-E0 | **AUTHORIZED** — coverage 0.886370 | FAIL | FAIL | **FAIL** — 1167/1778 unique exact |

Consequences fixed before R1 reveal:

1. **A1 must not receive a real R1 pair/residual calculation in this tournament.** Its preregistered representation gate already failed.
2. **Naibbe remains the only representation-compatible R1 candidate and must still receive the planned complete-66 R1 reveal.** Its already-known R2/R3/R4 failures do not justify stopping early.
3. Because A1 cannot pass R1 and Naibbe already fails R2, R3 and R4, neither candidate can reach a joint-competitive class under the frozen rules. Nevertheless Naibbe R1 remains scientifically useful: it directly tests whether this published reversible-cipher family reproduces the independently replicated token-construction core.
4. No target gate may be changed because the global tournament outcome is already constrained by preflight failures.
