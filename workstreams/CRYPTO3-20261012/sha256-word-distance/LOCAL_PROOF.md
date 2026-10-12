# A sharp local cancellation restriction for the SHA-256 small sigma1

**Candidate for project integration.** Complete written reduction with a
small exact finite certificate; independent review is recorded separately
in `local-review/`. No Lean compilation or global distance improvement is
claimed. Historical originality is unconfirmed.

## 1. Exact object and statements

Let R=Z/(2^32), using unsigned representatives and bit 0 as the least
significant bit. Use the actual small sigma from FIPS 180-4, Sections 4.1.2
and 6.2.2:

    g(x) = ROTR17(x) XOR ROTR19(x) XOR SHR10(x),
    h(x) = x + g(x)  in R.

The word operations and modular addition are those of the
[original NIST standard](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf).
The following are statements about all 32-bit words, without assumptions
on the base word.

**Theorem 1.** If h(x)=h(y) and x is congruent to y modulo 2^13, then x=y.
Equivalently, every nonzero D=y-x satisfying g(y)-g(x)=-D has

    v2(D) <= 12.

Here v2 is defined only for a nonzero residue: it is the position of its
least significant nonzero bit. The threshold is sharp for this local
problem: the pair

    x = 0x5d130376,  y = 0xa6d97376

has h(x)=h(y) and y-x=0x49c67000, whose valuation is exactly 12.
This is one local word pair, not two 16-word inputs to the message schedule.

**Theorem 2.** If y-x is either +2^k or -2^k in R, for any 0<=k<32,
then h(x) is different from h(y).

**Schedule corollary.** For the frozen support patterns numbered
0,1,2,4,8,9, the shared nonzero word difference identified in Section 5
has valuation at most 12 and is not a signed power of two. The corollary
restricts six possible equality supports; it excludes none of them in
its entirety. The known global lower bound remains 13. Neither an actual
distance-13 message pair nor a proof of distance at least 14 is supplied.

## 2. Exact XOR masks and the six-dimensional kernel

Suppose h(x)=h(y), and put

    alpha = x XOR y,   beta = g(x) XOR g(y) = g(alpha).

The last equality follows from XOR-linearity of the rotations and shift.
If x=y modulo 2^13, then alpha has its low 13 bits zero. The equality
g(y)-g(x)=-(y-x) also makes the low 13 bits of beta zero. Thus alpha lies
in the following binary linear subspace K:

    K = {a in F2^32 : a[0..12]=0, g(a)[0..12]=0}.

The 26 homogeneous bit equations have rank 26. One basis of their kernel is

    d5402000  aa804000  55008000
    aa010000  eeaa0000  dd540000

(hexadecimal words). The certificate checks each word's membership,
their independence, and rank 26 of the original 26-by-32 matrix. These
checks prove K is exactly their span; checking membership alone would not
prove completeness. Therefore a nonzero alpha must be one of exactly
63 nonempty XOR sums of these six basis words.

`local_certificate.json` supplies every selection in the order 1 through
63, its actual alpha, its actual beta=g(alpha), and an impossible carry
position. This certificate is small and independent of the older
5,308,416-inequality potential certificate.

## 3. A signed carry obstruction for every nonzero mask

For any two words with XOR difference alpha,

    y-x = sum_i alpha_i (1-2*x_i) 2^i  modulo 2^32.

Apply this also to g(x),g(y), with XOR mask beta. If h(x)=h(y), the sum of
these two signed sums is zero modulo 2^32. We relax the signs of every
changed input/output bit to independent choices. This discards the
constraint that g(x) is computed from x, so impossibility in the relaxed
system is sufficient to prove the original impossibility.

Starting at bit 13 with C_13={0}, let

    T_i = {0}                 if alpha_i+beta_i=0,
          {-1,+1}             if alpha_i+beta_i=1,
          {-2,0,+2}           if alpha_i+beta_i=2,

    C_(i+1) = {(c+t)/2 : c in C_i, t in T_i, c+t is even}.

This follows by equating bit i to zero and carrying the resulting signed
integer into bit i+1. Every real solution must give a member of each
reachable set. We do not require the carry out of bit 31 to vanish;
arbitrary final carries are valid because equality is modulo 2^32.

For each of the 63 nonzero masks in K, a reachable set becomes empty
before the end. The counts by the first bit at which processing becomes
impossible are:

| Bit | 13 | 14 | 16 | 17 | 18 | 19 | 21 | 22 | 23 | 24 | 25 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Masks | 32 | 8 | 4 | 3 | 3 | 2 | 2 | 2 | 1 | 3 | 3 |

The checker regenerates the complete kernel span and all the reachable
sets from the original bit equations. It checks the first-empty-bit data,
rather than trusting a printed UNSAT answer or a solver's internal proof.
All nonzero alpha are excluded, giving x=y and proving Theorem 1.

The exact local sharpness pair above is checked by independently
recomputing g from its 32 output-bit equations and then modularly adding.
In particular, the theorem cannot be strengthened to common low 12 bits.

## 4. Signed powers of two

By exchanging x and y, it suffices to assume y=x+2^k. Addition changes
exactly a consecutive run of bits beginning at k; the run ends at the
first zero bit encountered or at bit 31 on wraparound. Thus

    alpha = 2^(a+1)-2^k,   k<=a<=31.

If h(x)=h(y), then g(y)=g(x)-2^k. Subtraction has the same consecutive-run
property, so beta must have the same form with an endpoint b>=k.

There are 528 possible input runs over all k. Applying the original g
and checking every legal output endpoint leaves exactly one match:

    k=0, a=31, b=21,
    alpha=0xffffffff, beta=0x003fffff.

The only +1 input pairs with XOR mask 0xffffffff are
(0x7fffffff,0x80000000) and (0xffffffff,0). Direct evaluation gives their
g differences, respectively,

    0x0000a001,  0xffc00001.

Neither equals -1 modulo 2^32. This eliminates the last possibility and
proves Theorem 2, including negative increments and wraparound.

## 5. Bridges to the actual message schedule

For any actual pair of expansions define

    d_i = W'_i-W_i,
    F_i = sigma0(W'_i)-sigma0(W_i),
    G_i = g(W'_i)-g(W_i).

Subtracting the two original modular recurrences gives, for every
16<=t<64,

    d_t = G_(t-2) + d_(t-7) + F_(t-15) + d_(t-16).

Whenever an index is outside the exact support, all three corresponding
differences vanish. In each row below, substitution into the recurrence
at t=u+7,u+14,u+16 gives exactly

    d_(u+7)=d_u,
    d_(u+14)=d_(u+7),
    0=G_(u+14)+d_u.

| Frozen support index | u | Three recurrence indices | Word pair giving h collision |
|---|---|---|---|
| 0 | 30 | 37,44,46 | 44 |
| 1 | 31 | 38,45,47 | 45 |
| 2 | 32 | 39,46,48 | 46 |
| 4 | 33 | 40,47,49 | 47 |
| 8 | 29 | 36,43,45 | 43 |
| 9 | 29 | 36,43,45 | 43 |

Every u,u+7,u+14 in the table is active, so their common D is nonzero.
The last equation is G_(u+14)=-d_(u+14), precisely the premise of
Theorems 1 and 2. All 18 reduced equations are checked from the original
lag list. In particular, the different initial boundaries of supports 8
and 9 are retained; no invalid shift below t=16 is used.

The support bytes are copied without change as `supports-v2.json` from
commit `80b71cb3b6a67c8f8aae80d9cd8b6ed87d74bd51`, path
`workstreams/CRYPTO2-20261011-7f3c/projects/sha256-schedule-distance/v2/supports.json`.
Their SHA256 is
`02a12d8caa3ee3b78ec140f20fc0ad253835a6d32273247d20d22e0d8818edaf`.
`source-provenance.json` binds the source and copy.

The conditional bridges do not need a new enumeration proving the
completeness of the old 15-support classification. Any use of that full
classification retains its original potential and equality-traversal
dependencies, whose exact review scope is stated in `../review/review.md`.

## 6. Verification and limitations

From this directory, run:

```sh
python -B check_local.py --negative
```

The checker uses only the Python standard library. It checks the complete
kernel, 63 carry contradictions, 528 input intervals, both wrap boundaries,
the sharpness word pair, all 18 recurrence identities, and 11 damaged or
false controls. Actual execution, source hashes and exit codes are in
`LOCAL_RUNS.json`. Discovery used small restricted SMT queries to locate
the low-bit threshold; neither theorem relies on their UNSAT outputs.

Generic signed-bit and carry constraints are established cryptanalytic
tools, as discussed in the
[programmatic SAT paper](https://arxiv.org/html/2406.20072v1) and the
primary-source comparisons in `../sources/SOURCE_GATE.md`. The specific
local threshold and its schedule application have not received a complete
historical novelty clearance. This note does not claim a new generic
method, an attack exponent, SHA-256 collisions, or a proof-assistant theorem.
