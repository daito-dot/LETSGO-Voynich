# Phase 64A clean replay audit

Status: **scientific verdict replay-stable to machine precision**.

This audit does not create a new scientific result. The first reveal remains authoritative.

## First-reveal authority

- scientific head: `5e9121f7e05d8950f223298a44b816d6ee088e07`
- Actions run: `33335306504`
- job: `99321036069`
- artifact: `9738893689`
- artifact ZIP SHA-256: `058852cfc8bf5d718d200f05758d21452f45715d35a2b682f7422afc6261d8fc`
- raw JSON SHA-256: `43b59ad8539db4cf089e6265c38f81ec9afd2f864877b77373a12adbdccdce1b`

## Clean replay

- Actions run: `33335636754`
- job: `99321917194`
- replay artifact: `9739006133`
- replay artifact ZIP SHA-256: `4d9fdf888242665df5d4e457ae9a20252ca4dee956fb28e2e275e424977b334e`
- replay raw JSON SHA-256: `a5581e9210bbbc8718b493ebed11fcc8862743033d72f6dcec2f7c024d86d5a2`

The replay used the unchanged frozen Phase64A science entrypoint, exact ZL blob, exact IT2a SHA, exact prior-result authorities, exact seeds and `PYTHONHASHSEED=0`.

## Recursive comparison

First reveal versus replay:

- recursive value differences: **20**;
- non-numeric differences: **0**;
- maximum absolute numeric difference: **4.440892098500626e-16**;
- overall classification unchanged;
- ZL primary pass/fail unchanged;
- IT independent pass/fail unchanged;
- ZL/IT S1/S2/S3 frozen scalar-gate booleans unchanged.

The raw JSON byte SHA differs because of machine-level floating-point reduction order, but every difference is numeric and below `5e-16`.

Accepted replay statement:

> **Phase64A is semantically replay-stable to machine precision. The frozen `INCONSISTENT / PRIMARY FAILURE` classification and the isolated canonical ZL S3 failure are unchanged.**

This audit does not relax the failed ZL S3 threshold and does not increase the scientific claim beyond the first-reveal result.
