# The valuation-17 boundary: bounded true-word sharpness search

Recorded before computation. All support12-v4 and support12-extension-v5
author files remain frozen. The new width lemma below is a candidate
mathematical reduction, not an inherited independently accepted theorem.

## Exact target

For actual 32-bit pairs X,Y,R, with sigma0=ROTR7 xor ROTR18 xor SHR3
and sigma1=ROTR17 xor ROTR19 xor SHR10, require all equations modulo
N=2^32:

    d(X)=d(Y)=D!=0, d(R)=-D,
    F(X)=F(Y)=F(R),
    G(Y)-G(X)=2D, G(Y)-G(R)=D.

Find and directly check a six-word witness with v2(D)=17. Such a witness
would show that the already proved <=17 ceiling is sharp for this local
core. It would not be an actual 13-word supported expanded-message pair
or two base blocks. Conversely, a complete finite exclusion would need
an exact certificate and independent review; SMT UNSAT alone is not a
proof.

## Candidate complete representative reduction

Let v2(D)=17 and M=2^31. Each actual pair agrees in its low 17 input
bits. The sigma1 output bits 22..29 agree. Output bit30 depends only on
input bits15 and17, so its XOR change is exactly 1, because adding the
odd high quotient changes bit17. Its ordinary additive contribution is
+/-2^30, whose two signs are equal modulo M. Bit31 contributes a multiple
of M and vanishes modulo M. Thus, for each of X,Y,R,

    G_i = 2^30 + q_i (mod M), |q_i|<2^22,

where q_i is the ordinary difference between the low22 sigma1 images.
The same bit17 change holds for -D since the negative quotient is odd.
The common quarter-word cancels in the two gaps. Put A=q_Y-q_R and
B=q_Y-q_X; then A=D mod M, B=2D mod M, |A|,|B|<2^23. Since
|B-2A|<3*2^23<M and it is a multiple of M, B=2A and |A|<2^22.
A is a nonzero odd multiple of 2^17, so A=+/-q*2^17 for odd
q=1,3,...,31. Consequently

    D = +/-q*2^17 + h*2^31 (mod N), h=0 or1.

Simultaneously reversing all three pairs negates every d,F,G and
converts a negative representative to a positive one with the same h
(because -2^31=2^31 mod N). The complete positive list therefore has
exactly 32 representatives. This reduction only screens D. Every
subsequent query still enforces the original full 32-bit equations
modulo N, including the top bit; it never replaces them by mod M.

## Initial budget and stop rules

Query the 32 representatives in ascending odd q, h=0 then1, with at
most 2,000 ms per query, stopping at the first SAT six-word assignment.
Check a SAT object with a separately written standard-library checker
that evaluates the original bit definitions and all equations modulo N.
Freeze a genuine local sharpness object if found and stop this stratum.

Every unknown keeps its exact timeout, reason and parameter record.
No unknown timeout is extended. UNSAT is discovery only unless followed
by a complete independently checked finite proof. If all queries suggest
exclusion, decide the next certificate mechanism from that new finite
problem rather than rerunning the same SMT query.

No zero-base block is imposed. No independent assignment to F,G of one
pair is permitted. No message-pair claim may omit genuine base completion.

## Discovery outcome and new certification budget

All 32 original fixed-D queries returned UNSAT within their original
2,000 ms limit, with no unknown or SAT result. Those answers remain
discovery observations. The next mechanism explicitly reuses the frozen
v4 finite proof kernel to rebuild each new representative separately,
including its full sigma0 equations and mod-2^32 high bits. Every case
has a 55-second process budget and saves its complete compressed proof
certificate before the next distinct representative. A timeout would
leave that representative uncertified and is not extended. This is an
exact finite certificate construction, not another SMT query. Stored
XOR contradiction rows and complete mask grids must pass a full replay
before any <=16 ceiling is claimed.
