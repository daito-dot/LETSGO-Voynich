# E10 residual exploration direction — non-musical 5×5 dependency audit

Status: **BACKLOG / DO NOT EXECUTE WHILE MUSIC-CIPHER EXPLORATION IS ACTIVE**

E10's fitted Sloane 351 probe is a plaintext negative: `NO READABLE SLOANE PLAINTEXT`.

One numerical residual is nevertheless worth retaining separately from the music-cipher interpretation:

- the exhaustive training-only search over the two natural five-state Zattera factors selected the same full slot3×slot5 axis/permutation key in 4/5 physical-leaf folds;
- held-out plaintext remained strongly non-language-like (`4.2224 bits/char` vs medieval-Latin self-baseline `2.4516`), with 94.69% of output characters in the top five and zero exact lexicon hits of length >=6;
- the recurrent key maps the dominant EMPTY×EMPTY cell to Sloane's multi-character `con` abbreviation, so the immediate explanation is optimizer frequency collapse rather than decryption.

## Future question

After the music-cipher branch has been explored independently, test whether the 4/5 stability reflects a manuscript-native relation between slot3 and slot5 rather than anything musical:

> Does a hypothesis-neutral 5×5 representation of slot3×slot5 show cross-leaf stability / predictive dependence beyond frequency-preserving non-musical controls?

The future audit should not use the Sloane plaintext table, Latin likelihood, `con`, or any music-derived ordering. It should compare direct slot3↔slot5 dependence, conditional distributions, held-out prediction, and appropriate frequency-preserving controls.

## Boundary

This residual observation is **not evidence for Sloane 351, music, plaintext, or a 25-symbol cipher**. It is retained only so that the potentially interesting 4/5 cross-fold structural recurrence is not lost when the failed music-cipher decoding branch is closed.
