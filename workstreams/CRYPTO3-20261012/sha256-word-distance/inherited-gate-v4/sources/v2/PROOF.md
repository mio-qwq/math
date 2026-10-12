# Equality supports and a universal impossible sigma chain

CRYPTO2-20261011-7f3c, 2026-10-12 UTC. Written proof and exact finite
dependencies; **awaiting independent review**. No SHA Lean formalization.
This is a continuation of the frozen v1 word-distance result, not a claim
of a SHA-256 collision, preimage attack, or improved security exponent.

## Object and claims

All words lie in R = Z/(2^32), represented by unsigned 32-bit integers;
bit 0 is the least significant bit. Put H=2^31. The actual small sigmas are

    f(x) = ROTR_7(x) XOR ROTR_18(x) XOR SHR_3(x),
    g(x) = ROTR_17(x) XOR ROTR_19(x) XOR SHR_10(x).

For each of two arbitrary 16-word message blocks, expand to W_0,...,W_63 by

    W_t = g(W_(t-2)) + W_(t-7) + f(W_(t-15)) + W_(t-16), 16 <= t < 64.

Write delta_i=W'_i-W_i, F_i=f(W'_i)-f(W_i), G_i=g(W'_i)-g(W_i).
The support is S={i:delta_i != 0}. There is no zero-base, padding, IV,
independence or random-input assumption. Both sigmas are bijective, as
proved by complete inverse bases in v1. Therefore delta_i, F_i and G_i
are simultaneously zero or simultaneously nonzero.

**Claim 1 (complete equality classification in the relaxation).** Exactly
15 supports of size 13 meet the v1 necessary condition

    |S intersect {t,t-2,t-7,t-15,t-16}| != 1, 16 <= t < 64.

They are listed, in zero-based indexed order, in supports.json. This is a
finite certificate result conditional on the already checked v1 potential.

**Claim 2 (actual universal exclusions).** Supports 3 and 14 in that file
cannot occur for any two actual expanded message blocks. Thus every actual
pair at distance 13, if any exists, must have one of the other 13 supports.
This DOES NOT prove distance >=14 or existence at distance 13.

## Completeness of Claim 1

Let V_t(q) be the frozen v1 nonnegative potential, where q encodes the
16 most recent activity bits before index t. The v1 checker establishes
V_64=0, popcount(q)+V_16(q)>=13 for every q!=0, and

    V_t(q) <= b + V_(t+1)(q')

for every transition satisfying the no-singleton condition. Along any
path of total weight 13, the initial inequality and EVERY transition
inequality must be equality: summing their nonnegative integer slacks
gives total weight minus 13, namely zero. Hence all such paths start in
the enumerated equality states and traverse only equality transitions.

enumerate_supports.py performs a depth-first traversal. The separate
checker rebuilds the states from full 64-bit path masks and traverses
breadth-first, checking both next bits at every step. It finds 15 initial
states, 735 total nodes including terminal nodes, and 15 terminal supports.
It checks equality with the complete supplied list, rather than just
testing that listed supports are allowed. Terminal paths have weight 13.
The v1 table is pinned by its decompressed SHA256; no optimality assertion
about unvisited states is needed beyond its verified inequalities.

## An elementary carry lemma

If a'-a is congruent to +2^13 or -2^13 modulo 2^24, put alpha=a' XOR a.
Then alpha_0,...,alpha_12=0, and

    alpha_19=1 implies alpha_18=1.                         (1)

Indeed, the lower 13 bits agree, and if q=floor(a/2^13) modulo 128,
q'=floor(a'/2^13) modulo 128, then q'=q+1 or q-1 modulo 128. If bit 6
changes on increment/decrement, all six lower bits change, in particular
bit 5. This includes wraparound between 127 and 0. The checker exhausts
all 128*2 possibilities; the argument explains the reduction from 32-bit
words to these cases.

Since f is XOR-linear, f(a') XOR f(a)=f(alpha). Its lowest two bits are

    f(alpha)_0 = alpha_7 XOR alpha_18 XOR alpha_3 = alpha_18,
    f(alpha)_1 = alpha_8 XOR alpha_19 XOR alpha_4 = alpha_19.

By (1), these two bits cannot be binary 10. For any two words z,z',

    z'-z = 2 (mod 4)  iff  (z' XOR z) = 2 (mod 4).         (2)

This follows directly by writing their two low bits, or by observing that
the least differing bit has the same position in the modular and XOR
differences. Consequently

    f(a')-f(a) != 2 (mod 4).                              (3)

## Universal impossible chain

There do not exist six words x,x',a,a',b,b' satisfying all of

    x'-x = H,
    a'-a = epsilon * (f(x')-f(x)), epsilon in {+1,-1},
    b'-b = f(a')-f(a),
    g(b')-g(b) = H.                                      (4)

Proof. A modular difference H equals the XOR difference H, so

    f(x') XOR f(x) = f(H) = 0x11002000
                              = 2^13 + 2^24 + 2^28.

The modular difference of two words with this XOR mask is a signed sum
of these three powers. Negating it merely negates the signs. Thus
a'-a is +2^13 or -2^13 modulo 2^24. By (3), b'-b cannot equal 2 modulo 4.

On the other hand g(b')-g(b)=H implies g(b') XOR g(b)=H. XOR-linearity
and bijectivity give

    b' XOR b = g^(-1)(H) = 0xc6eeaad6 = 2 (mod 4).

The constant is checked by applying g; uniqueness follows from the full
32-column right inverse. Equation (2) now gives b'-b=2 modulo 4,
a contradiction. This proves (4) for arbitrary words, with no SMT premise.

## Applying the chain to the actual schedule

Every actual pair satisfies the modular identity

    delta_t = G_(t-2) + delta_(t-7) + F_(t-15) + delta_(t-16).   (5)

For support 3, substituting its zero coordinates into (5) gives exactly

| Index t | Reduced identity |
|---|---|
| 34 | delta_34 = delta_27 |
| 43 | delta_43 = delta_27 |
| 50 | 0 = delta_43 + delta_34 |
| 49 | 0 = delta_42 + F_34 |
| 57 | delta_57 = F_42 |
| 59 | 0 = G_57 + delta_43 |

Since 27 is active, the first three identities give 2*delta_27=0 and
delta_27!=0 in R, hence delta_27=H. (The only residues annihilated by 2
are 0 and H.) Therefore delta_34=delta_43=H. The last three identities
give delta_42=-F_34, delta_57=F_42, G_57=-H=H. These are (4) with the
word pairs at indices 34,42,57 and epsilon=-1: impossible.

For support 14 use indices u=25,x=32,a=40,r=41,b=55. The corresponding
six recurrence indices are 32,41,48,47,55,57. Their reduced identities
are the identical six equations with every displayed index above shifted
by -2. The extra active index 62 does not enter these six equations.
The checker derives all twelve identities directly from the lag set and
the supplied supports. This proves Claim 2.

## Scope

The proof excludes two support patterns even in the relaxation where each
active word pair is independent but all difference equations (5) hold.
It is stronger than the v1 all-zero-base contradiction. It does not exclude
the other 13 patterns, provide an attainable minimum, constrain a complete
compression differential probability, or imply any collision advantage.

The enumeration/checker and written proof are by the same researcher.
They are not an independent-agent review or Lean verification. Generic
carry constraints and impossible-differential reasoning are established
prior art. Novelty, if any, concerns this specific complete equality list
and its universal exclusions; historical originality is unconfirmed.

## An exact boundary: the unforced tail is feasible

One must not drop the forced-H assumption and reuse the contradiction.
In fact, the five tail equations, using independent pairs at x,a,r,b,

    delta_r=-delta_x, F_r=F_x, delta_a=-F_x,
    delta_b=F_a, G_b=delta_x,

have an explicit solution with all four deltas nonzero and delta_x!=H.
TAIL.json supplies all eight unsigned words. The separately implemented
checker verifies them directly from the bit equations, without a solver.
These five equations correspond to t=49,50,57,58,59 with x=34,a=42,r=43,
b=57, or their valid shifts. They occur in several remaining supports.

This is a counterexample only to an overstrong extension of our own tail
lemma. It is not a full word-support witness: neither the earlier
difference equations nor the actual base-schedule equations are imposed.
Consequently the remaining work must use additional equations, not hope
for a contradiction in these five alone.
