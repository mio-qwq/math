# Cross-review of the discovery endpoint manuscript

Date: 2026-10-11. Reviewed file: `../proofs/special_bit_signed_correlation.md`.

Reviewed SHA-256: `184c9f29b147e4035ac155a1e375accbc0fd58cb591fc222bdc84e3fe5281d73`.

Verdict: **no mathematical error found in the stated theorem or its proof**.

## Independence record

Before reading the discovery manuscript, this verifier independently wrote `independent_word_enumerator.cpp`, `independent_verify.py`, `INDEPENDENT_PROOF.md`, and `VERIFICATION_REPORT.md`. The original word enumerator produced 50 rotation-parameter groups and checked the endpoint closed form throughout its declared small-width domain. A separate integer threshold sum checked further endpoint parameter pairs. The full quarter-round RFC 8439 known-answer vector also passed.

The discovery agent subsequently authorized written-proof cross-review. Only the manuscript above was read for this review; discovery experimental implementation and its `tooling/` implementation were not read. The two ordinary proofs reach the same carry/threshold/Walsh description. This is independently reconstructed verification, not a claim that the mathematical methods are unrelated, and not human peer review.

## Critical points checked

1. **Definition and model.** The displayed `L` is exactly the result of replacing all three modular additions by XOR. The stated result conditions on no word and assumes uniform independent input words. The manuscript explicitly separates this distribution from a standard first-column round with a fixed constant.
2. **Carry identity.** Direct word substitution gives `alpha XOR R_(r+q)(alpha) XOR R_q(beta) XOR gamma`. At `i=r+q<n`, the rotated first carry refers to bit zero and vanishes. The hypotheses are sufficient for this reduction.
3. **Invertible variables.** The inverse map from `(s,b,u,t)` is correct. The transformed words really are independent uniform words, rather than being assumed independent after an irreversible substitution.
4. **Strict threshold and endpoint count.** `carry_h(x+y)=[y_low>sum_low]` uses a strict inequality. The middle-carry expectation `(2(U+1)-2^r)/2^r` correctly includes the equality case, including `U=0` and `U=2^r-1`.
5. **Rotation wrap and fresh bits.** The low `q` output bits use high input bits of `u` disjoint from its low `r` bits because `n-q>r`. Independence still holds if the corresponding bits of `b` overlap other retained bits. No unstated `n>=r+2q` condition is required.
6. **Unmasked moment.** The conditional first threshold factor is `2(S+1)/N-1`; the final-addition factor is `1-2S/N`. Their exact average is `-1/3+4/(3N^2)`.
7. **Masked moment.** The prefix sums use `S+1` on the subtraction side and `N-S` on the addition side. The latter equals the triangular prefix at `S` by symmetry and periodicity. For `ell<p`, `2^(ell+1)` divides `2^p`, so the half-period pairing is legitimate even at the endpoints. Its sum gives `M_(ell,p)=2^(ell+p)/N^2`.
8. **Geometric sum and sign.** The exponent is `3*ell`; summing yields `(2^(3r)-1)/7`. The stated rational formula follows. Since `r,q>=1`, `N>=4`, the unmasked moment is negative and every subtracted mixed moment is positive; strict negativity follows without numeric approximation.
9. **Complexity and interpretation.** No 32-bit exhaustive enumeration is represented as having been done. Correlation, absolute correlation, and half-sized probability bias are distinguished. The deliberately false carry-independence calculation is correctly identified as a negative control, not attributed to any paper.

## Numerical reconciliation

The discovery standard fraction agrees with the independently derived fraction

`-47180567524833621/1180591620717411303424`.

Independent direct counterexamples already establish that the endpoint closed form must not be extended without proof to `q=0`, `r+q=n`, or right-rotation conventions. The discovery theorem excludes those cases correctly. The general arbitrary-bit formula is reviewed and proved separately.

## Limits of this review

This review establishes consistency with an independently obtained proof and finite direct enumeration. It does not establish literature novelty, a best published attack improvement, machine-checked formal correctness, or the usefulness of this local statistic in a full-round attack. No correction to the reviewed mathematical statement is requested.
