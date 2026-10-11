# Exact-version review receipt for PROOF-v2.md

**Mathematical verdict: PASS.** I read the actual complete `PROOF-v2.md`, checked its byte hash, and compared it with the preserved version 1. The changes agree with the independently verified conclusions in `ADDENDUM.md`. No mathematical gap was found in this exact version's theorem or added Proposition 5a.

## Exact artifacts bound by this receipt

Reviewed file:

`workstreams/CRYPTO2-20261011-7f3c/PROOF-v2.md`

Actual SHA256, matching the requested version:

`71d5a5dc6e757402db8b54a15507ffd6e4e8e87eec0f4f4fe438c21f6cf55d91`

Preserved version 1, used for the exact diff:

`PROOF.md` — `5526707c49ab8864f54a11c816f6bebd95bf981115577dc584ab25c221956fd4`

Prior addendum, whose mathematical conclusions are now bound to the actual version-2 text:

`review/ADDENDUM.md` — `152b50c252d9e412acfecb773b353df2028368bc75c68977a2eb5d1d65874816`

The prior `PRE-DISCLOSURE.md`, `REVIEW.md`, and `ADDENDUM.md` were not edited. No numerical tests were repeated for this receipt. No parent proof or Git ref was modified.

## Checked changes from version 1

The exact diff consists of the version/provenance preface, two corrected comments about MDS inheritance, and the added Section 5a. The main theorem, its constructive lemmas, and its case split remain unchanged.

1. The odd-circulant comment now distinguishes the general invertible theorem from the MDS specialization and correctly says that an MDS input has an MDS periodic quotient.
2. The comment after divisor lifting now correctly says that invertibility alone does not force the quotient to be MDS, but an MDS original matrix does. This wording is valid: for example, a periodic quotient of an identity circulant can be an identity matrix of order at least two, which is invertible but not MDS.
3. Section 5a states and proves the branch-number inequality and then obtains MDS inheritance. Both match the addendum.
4. The short original-scope proof uses an odd MDS quotient and repetition, with no non-MDS fallback. Its stricter bound d>=5 is correct for the specifically remaining residues n congruent to +/-2 modulo 12 with n>2; the smallest such n is 10. The general n=2 modulo 4 case earlier in the file correctly only requires d>=3.

## Section 5a assessment

With n=td, the repetition map J satisfies MJ=JB and multiplies Hamming weight by t. Hence, for every nonzero x,

\[
t\bigl(\operatorname{wt}(x)+\operatorname{wt}(Bx)\bigr)
=\operatorname{wt}(Jx)+\operatorname{wt}(MJx)
\ge\beta(M).
\]

Taking an integer ceiling and the minimum over x gives exactly

\[
\beta(B)\ge\left\lceil\beta(M)/t\right\rceil.
\]

For MDS M, \(\beta(M)=td+1\), so \(\beta(B)\ge d+1\). The universal upper bound from a coordinate vector gives equality. The standard equivalence between branch number d+1 and nonsingularity of every square minor then establishes that B is MDS. That equivalence was proved explicitly in my addendum and is valid over every field.

Thus the new proposition and its MDS corollary are correct. The factor t concerns integer weights and entails no division by a possibly zero field element. In fact this proposition does not require characteristic 2 or invertibility, although the surrounding related-differential theorem is stated over characteristic-2 fields and assumes invertibility.

For the remaining MDS orders, B is an odd MDS circulant. Applying the valid odd MDS base and repeating its witness establishes the claimed short proof. Both input nontriviality and the output relation survive repetition. Section 5a therefore resolves the precise issue recorded in the addendum rather than merely avoiding it.

## Accepted scope and limitations

This receipt accepts the exact mathematical statement:

> Over every field of characteristic 2, every invertible circulant matrix of order n>=3 has nonzero unequal input vectors u,v that are coordinatewise related, whose images Mu,Mv are also coordinatewise related.

Invertibility ensures nonzero unequal output vectors. The version retains the necessary exclusion of order 2 and does not extend the existence theorem to arbitrary singular matrices or other characteristics. No new missing assumption was found.

The source framing remains appropriate: Kumar–Yadav–Samanta, arXiv:2605.27535v1, Theorem 5 and the concluding remaining-case direction in Section VI. The source does not print a fully quantified numbered conjecture. The original nontriviality convention and attribution caveats documented in the earlier review continue to apply.

**Historical originality is not certified.** This is an exact-version mathematical review, not a completed literature novelty investigation. The parent reported additional potentially relevant 2025–2026 sources and a full-text access gap; I have not independently reviewed those new sources in this receipt. They therefore cannot be treated as either proving novelty or disproving it on the strength of this receipt. The existing proof text correctly leaves historical publication priority unresolved. The additional Whirlwind attribution remains outside this review's independently checked citation scope, as recorded previously, and is not used as an unproved mathematical premise.

This receipt also does not certify external peer-review acceptance, Lean formalization, a cipher attack, or attack complexity/security bounds. Its PASS applies to the written mathematics in the exact hashed version above.
