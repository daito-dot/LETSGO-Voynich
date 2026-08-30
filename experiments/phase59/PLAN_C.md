# Phase 59C plan — subtract the generic medieval entry component

Status: frozen before execution.

## Motivation

Phase59B changes the interpretation of the paragraph-entry phenomenon. Voynich differs strongly from Dante continuous prose, but explicit medieval manuscript item/section entries can move in a partially similar multivariate direction. The effect is neither uniquely medical nor universal across medieval genres.

The next question is therefore not whether Voynich has an entry transition, but which part of that transition remains after accounting for a generic medieval entry component.

## Data firewall

The comparison basis is learned only from external Latin source-marker controls. Voynich may be projected onto that basis only after it is fixed. No Latin entry may be selected because it resembles the Voynich vector.

Primary external classes currently available:
- medical/practical: H318, CLM13027;
- ecclesiastical: UBL758;
- scholastic: BIS193.

Dante remains a non-entry continuous-prose negative control.

## Primary analyses

1. Standardize each corpus in its own generic 11-feature measurement scale.
2. Estimate the external Latin entry-transition centroid and low-rank entry subspace from manuscript-level/source-entry deltas.
3. Decompose the frozen Voynich transition into:
   - component parallel to the Latin entry basis;
   - orthogonal residual component.
4. Test whether the orthogonal Voynich component remains consistent across major Voynich sections H/B/P/S/T using leave-one-section-out transfer and page bootstrap.
5. Repeat while leaving each Latin manuscript/control class out when estimating the external entry basis.

## Frozen hypotheses

### H59C-1 — generic entry explanation is sufficient
Most of the Voynich transition lies in the external medieval-entry subspace and the orthogonal component is weak or unstable across Voynich sections.

### H59C-2 — shared entry grammar plus Voynich-specific component
A substantial parallel component exists, but a stable orthogonal component also transfers across Voynich sections.

### H59C-3 — apparent Latin similarity is unstable
The external entry direction changes strongly under leave-one-manuscript/control-out analysis and cannot define a reliable generic entry basis.

## Falsification / interpretation rule

A stable orthogonal component supports a Voynich-specific structural specialization, not semantics or cipher. Failure of the orthogonal component supports a simpler medieval document-entry explanation. Instability of the external basis means Phase59B must remain descriptive and no subtraction claim is permitted.
