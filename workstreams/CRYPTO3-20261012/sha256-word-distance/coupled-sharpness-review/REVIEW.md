# Independent review: the local valuation bound 11 is sharp

**Verdict: PASS for the explicit four-word object and its local sharpness conclusion.** This is an independent AI technical check, not external human peer review or a formal Lean proof.

## Object and direct reconstruction

All words lie in R = Z/(2^32), bit 0 is least significant, and f = sigma0, g = sigma1 are exactly the small sigmas in FIPS 180-4 section 4.1.2, equations (4.6) and (4.7). The independent checker constructs every output bit from the three specified input positions. It uses no author code, solver, table, or claimed sigma output to compute its values.

| Word | Input | f(input) | g(input) |
|---|---|---|---|
| p | 0019f0ed | a6384dfa | c66b2673 |
| p' | 973448ed | dbf38441 | ad4eb46e |
| q | dff7f75f | 5996e6f8 | 0573e9f8 |
| q' | 77124f5f | 23dbb0b1 | 6e5991f8 |

Every entry is hexadecimal. Direct subtraction modulo 2^32 gives

    dP = dQ = D = 0x971a5800,
    Gq = 0x68e5a800 = -D,
    Fp = 0x35bb3647,
    Fq = 0xca44c9b9 = -Fp.

The nonzero residue satisfies D = 2^11 * 1237835, with odd quotient, so v2(D) = 11. In canonical integer representatives both Gq + D and Fp + Fq equal 2^32; their vanishing is correctly interpreted modulo 2^32.

The three equation pairs can also be checked directly:

| Modular expression | Common value |
|---|---|
| q + g(q) = q' + g(q') | e56be157 |
| p' + q = p + q' | 772c404c |
| f(p') + f(q') = f(p) + f(q) | ffcf34f2 |

In the middle row, p' + q overflows while p + q' does not; the checker deliberately reduces both sides modulo 2^32. Thus no accidental equality over unbounded integers or no-overflow restriction is used.

## Independence and finite verification

The supplied input words and claimed valuation were known. `RECONSTRUCTION.md`, `check.py`, and `INDEPENDENT_RUN.json` were completed and hashed in `PRECOMPARISON_FREEZE.json` before the author sharpness proof or witness was read. All three frozen hashes were checked again during comparison. This independence claim concerns the computation and order of review, not an independently discovered witness.

The standard-library checker ran under Python 3.12.14 and exited 0. Eight damaged controls were rejected: bit 0 of each of the four words; rotation 7 changed to 6 in f; rotation 19 changed to 18 in g; one damaged claimed D bit; and an incorrect claimed valuation 10. The wrong-constant controls fail the actual local equations rather than a hard-coded rejection of the parameter itself. The author proof and all 17 numerical witness fields agree with the independent result. The author seven-file manifest was checked for integrity. The discovery solver and the author checker were not executed or audited as part of this receipt.

Read-only reproduction from the repository root:

```sh
python workstreams/CRYPTO3-20261012/sha256-word-distance/coupled-sharpness-review/check.py
```

Use the explicit `--record PATH` option only to create a new run record.

## Consequence and exact limits

Together with the separately accepted local upper-bound proof, this object proves that the maximum possible v2(D) under precisely these three four-word conditions is 11. The upper-bound review receipt is pinned in `REVIEW_RECEIPT.json`; its main review directory was left unchanged.

A universal improvement below 11 cannot follow from these conditions alone. Any stronger bound for one of the seven support applications must use additional original schedule constraints. This object assigns no values to the remaining active coordinates, proves no base interpolation, and satisfies no asserted full set of 48 schedule-difference recurrences. It gives no pair of 16-word messages, no actual schedule-distance equality case, and no improvement to the known global word-distance lower bound 13. No historical priority claim is made.

Definition source: [NIST FIPS 180-4](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf), section 4.1.2.
