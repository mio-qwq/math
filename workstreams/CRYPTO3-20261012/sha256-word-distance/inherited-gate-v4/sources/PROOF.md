# Certified bound for actual SHA-256 message expansion

Classification: universal word-distance lower bound with an exact finite
certificate. Sharpness only for a support relaxation. Originality and
importance unconfirmed; awaiting independent review. No attack claim.

Let E:(Z/2^32)^16 -> (Z/2^32)^64 be the actual FIPS 180-4 expansion:
W_t=sigma1(W_(t-2))+W_(t-7)+sigma0(W_(t-15))+W_(t-16) mod 2^32.

Claim: for every M!=M', at least 13 coordinates of E(M),E(M') differ.

## Reduction from exact words

Let a_t=1 exactly when W_t!=W'_t. Both small sigmas are F2-linear
and invertible. The certificate supplies 32 right-inverse columns for
each. The checker evaluates every column by the FIPS output-bit
equations, verifying the corresponding basis vector. Linearity proves
the inverse on all 2^32 vectors, hence injectivity.

For each t>=16 the number of active positions in
    {t,t-2,t-7,t-15,t-16}
cannot be one. A lone changed output contradicts identical inputs.
A lone changed input, after cancelling unchanged summands, contradicts
injectivity of its sigma (or the identity) and equality of the output.
This uses cancellation in Z/2^32, NOT XOR-linearized addition.
Some a_t with t<16 is nonzero since the input messages differ.
The resulting binary support condition is only necessary.

## Exact certificate proof

Before step t, state q has bit j equal to a_(t-16+j). A new bit b has
successor q'=floor(q/2)+2^15 b and cost b. The four source bits are
j=14,9,1,0. A transition is permitted precisely when their sum plus b
is not one.

The certificate has integer arrays V_t(q), 16<=t<=64, 0<=q<65536,
encoded as 49 rows of 65536 bytes. The checker verifies
    V_64(q)=0;
    V_t(q)<=b+V_(t+1)(q') for EVERY permitted transition;
    popcount(q)+V_16(q)>=13 for EVERY q!=0.
There are 5,308,416 transition inequalities. Summing along any valid
path telescopes to sum a_t>=popcount(q_16)+V_16(q_16)>=13.
Every actual message pair induces such a path, proving the claim.

Discovery computes backward minima. The checker instead verifies all
inequalities and never trusts that optimization. Raw potential SHA256:
1f04aa2b5ac13c5144e677cf75eb6d6af323d518abf96ec65a44a96fa07df23c.
There is no random-input or independent-carry assumption.

## Exact limitation of the relaxation

The support {2,9,10,16,23,24,30,37,38,44,51,52,58} has 13 active
positions and satisfies every binary constraint, checked separately.
Therefore 13 is the exact minimum in this relaxation. This method
alone cannot prove 14. No actual pair realizing that support is known
here, so we have NOT proved d64<=13.

## First lifting failure: all-zero base

Suppose one message is all zero and the other has the displayed support.
Write w for the nonzero expansion and v=w9!=0. Steps 16,23,24,31 force
    w16=w23=v, w24=sigma0(v), 0=w24+sigma0(w16).
Thus 2 sigma0(v)=0. Injectivity rules out sigma0(v)=0, leaving
sigma0(v)=0x80000000 and v=0x94857ee6 (the inverse column).
Steps 18,17,26 require
    w2=-sigma1(v), w10=-sigma0(w2), w10=-sigma1(0x80000000).
Exact evaluation gives
    sigma0(-sigma1(0x94857ee6)) = 0xabacb99f,
    sigma1(0x80000000)         = 0x00205000.
They differ, a contradiction. This written proof replaces reliance
on that restricted SMT unsat answer. The checker verifies the constants.
It excludes only this support with an all-zero base. For arbitrary
base words the cancelled equal summands need not be zero.

The unrestricted-base SMT query timed out after 20 seconds (unknown),
not a proof of impossibility. Neither this nor the restricted failure
improves the universal bound to 14.

## Research value

The theorem concerns the original full-width, full-length expansion,
but it is a coarse necessary constraint. It yields no probability or
hash collision-complexity bound. Truncated differentials, stopping-set
constraints and trellis optimization are established techniques.
The exact 13-word parameter was not located in the bounded search;
that does not establish novelty. A stronger global constraint with
cryptanalytic relevance is required before calling this substantial
SHA-256 research progress. Do not grow equivalent sample/certificate sets.
