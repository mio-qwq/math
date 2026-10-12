# Exact active-pair modules for SHA-256 support 0

**Research candidate, pending a separate review.** The first result is an
exact construction criterion for all 48 difference recurrences on the
frozen support 0. The second result is a short obstruction to one
specified construction family. No complete 13-pair assignment, actual
message pair, improvement of the global lower bound 13, or Lean theorem
is claimed.

## 1. Definitions and the complete interface equations

All additions and subtractions below are in `R = Z/(2^32)`. For an actual
ordered word pair `X=(x,x')`, define

    d(X) = x'-x,
    F(X) = f(x')-f(x),
    G(X) = g(x')-g(x),

where

    f(x) = ROTR7(x) xor ROTR18(x) xor SHR3(x),
    g(x) = ROTR17(x) xor ROTR19(x) xor SHR10(x).

These are the SHA-256 small sigmas, with bit 0 least significant. Every
occurrence of F and G on a particular pair refers to these same two
words. There are no independent assignments to its two sigma differences.

Let the independently chosen active pairs be

    Q_j at index 2+14j,   0 <= j <= 4,
    P_j at index 9+14j,   0 <= j <= 3,
    R_j at index 10+14j,  0 <= j <= 3.

They occupy exactly

    S0 = {2,9,10,16,23,24,30,37,38,44,51,52,58}.

At all other indices the three differences are zero. Subtracting the
original recurrence at each `16 <= t < 64` gives

    d_t - G_(t-2) - d_(t-7) - F_(t-15) - d_(t-16) = 0.       (1)

Exactly 24 of these 48 equations have nonzero symbolic terms. All of
them are equivalent to the following list; there is no boundary shift
or equation omission:

| Conditions | Original recurrence indices |
|---|---|
| `d(P_0)=d(Q_1)=d(P_1)=d(Q_2)=d(P_2)=d(Q_3)=d(P_3)=d(Q_4)=D` | 16, 23, 30, 37, 44, 51, 58 |
| `d(R_0)=-F(Q_0)` | 17 |
| `G(Q_1)=-d(Q_0)` | 18 |
| `d(R_(j+1))=F(P_j)`, `j=0,1,2` | 24, 38, 52 |
| `d(R_(j+1))=-F(Q_(j+1))`, `j=0,1,2` | 31, 45, 59 |
| `G(Q_2)=G(Q_3)=G(Q_4)=-D` | 32, 46, 60 |
| `G(P_(j+1))=-D-F(R_j)`, `j=0,1,2` | 25, 39, 53 |
| `G(R_(j+1))=-d(R_j)`, `j=0,1,2` | 26, 40, 54 |

In the first row D is `d(P_0)`. Its seven equalities form a path on eight
coordinates, so replacing these eight d symbols by D is reversible.
After that replacement each other displayed condition is one original
equation, up to sign. This proves equivalence over R without division.
The remaining 24 original equations reduce identically to zero.

The initial pair Q_0 is not required to have difference D. The initial
pair Q_1 is not required to satisfy `G(Q_1)=-D`. The last pairs P_3,
R_3 and Q_4 have no sigma0 requirement from (1). In particular, this is
not a periodic identification of actual pairs or of all their interfaces.

## 2. A constructive decomposition with an exact left boundary

Write `r_j=d(R_j)` and `u_j=F(R_j)`. The three G relations along R can
be solved constructively, before considering P or Q.

**Reversed-image chain lemma.** Choose any unequal terminal pair
`R_3=(a,b)` and any three words `c_2,c_1,c_0`. Recursively, if
`R_(j+1)=(v,w)`, set

    R_j = (g(w)+c_j, g(v)+c_j),   j=2,1,0.                 (2)

Then `G(R_(j+1))=-d(R_j)` for all three j. Conversely, every ordered
chain satisfying these three equations has a unique representation
(2), with

    c_j = first(R_j)-g(second(R_(j+1))).

Indeed, the required equation says that R_j and the reversed g images
of R_(j+1) have the same modular difference. Ordered pairs with the same
difference differ by a unique common modular translation. The map g is
bijective: the checker constructs its original 32 binary output rows
and verifies rank 32. Thus (2) preserves inequality at every step.

This parameterizes the entire R chain by five words: the two terminal
words and three translations. No R pair is identified with another.

**Exact module criterion.** After constructing an R chain by (2), a full
assignment of unequal actual pairs on S0 satisfying all 48 equations
(1) exists with this R chain if and only if some nonzero D and the
following actual-pair modules exist:

| Module | Exact requirements on its pairs |
|---|---|
| Left boundary `(Q_0,Q_1,P_0)` | `d(Q_1)=d(P_0)=D`; `F(Q_0)=-r_0`; `F(Q_1)=-r_1`; `F(P_0)=r_1`; `G(Q_1)=-d(Q_0)`; `d(Q_0)!=0` |
| First middle module `(Q_2,P_1)` | both differences D; `F(Q_2)=-r_2`; `G(Q_2)=-D`; `F(P_1)=r_2`; `G(P_1)=-D-u_0` |
| Second middle module `(Q_3,P_2)` | both differences D; `F(Q_3)=-r_3`; `G(Q_3)=-D`; `F(P_2)=r_3`; `G(P_2)=-D-u_1` |
| Right boundary `P_3` | `d(P_3)=D`; `G(P_3)=-D-u_2` |

Choose Q_4 independently with `d(Q_4)=D` and `G(Q_4)=-D`. Such a pair
already exists if the first middle module exists: Q_2 supplies an
available choice. This observation establishes existence of a right
completion; it does not impose Q_4=Q_2 on every solution. Its F value is
unconstrained.

For necessity, extract the R chain and D from a full solution and use
the table in Section 1. For sufficiency, combine the four modules, the
R chain, and the stated Q_4. They supply every row of that table, hence
all 48 original equations. All P and Q_1,...,Q_4 pairs are unequal
because D is nonzero. Q_0 is explicitly unequal, and all R pairs are
unequal by the chain lemma. Thus the support is exactly S0.

The module choices are conditionally independent once the actual R
chain and D are fixed. Their nonemptiness remains a substantive
condition. The criterion does not say that arbitrary R chains or D
admit the modules. In particular the left boundary retains the
nontrivial two-pair relation between Q_0 and Q_1.

## 3. Exact fixed-XOR fibres of actual pairs

The one construction test used the following elementary complete
description of a fixed-XOR fibre. This description also gives a finite,
checkable way to test a module when its input XOR masks are specified.

Let a pair be `(x,x xor alpha)` and let `L` be any fixed binary linear
word map, including the identity, f or g. Put `beta=L(alpha)`. Since
`L(x xor alpha)=L(x) xor beta`, its modular output difference is

    B = beta - 2 * sum_(0<=i<31, beta_i=1) L(x)_i 2^i
        modulo 2^32.                                      (3)

The sign of bit 31 is immaterial modulo `2^32`. Given beta and a target
B, form the unsigned word `delta=(beta-B) mod 2^32`. There is a solution
of (3) if and only if all of the following hold:

1. delta is even.
2. `c=delta/2` has no set bit outside `beta & 0x7fffffff`.
3. For every i<31 with beta_i=1, the linear output bit `L(x)_i` equals
   c_i.

To prove completeness, the weighted sum in (3), with its top input bit
omitted, lies in `[0,2^31)`. Thus dividing the congruence by 2 yields a
unique integer c in that interval. No further carry choice is hidden.
The remaining conditions are exactly linear equations over F2.

Combining these equations for `L=id,f,g` gives the complete actual-pair
fibre for any prescribed subset of `(d,F,G)`. Every nonempty fibre is an
affine binary space. This does not assume that the signs of the two
sigma differences are independent: both sets of rows act on the same
32 bits of x.

For a known seed `(x,y)` and common XOR translation z, preserving its
specified L difference is equivalently

    L(z) & L(x xor y) & 0x7fffffff = 0.                    (4)

The probe uses (3), while the first diagnostic calculation independently
uses the homogeneous form (4). The verifier reconstructs the word maps
from their output-bit formulas and checks the stored affine spaces.

## 4. One finite family, and a strict mod-8 obstruction

The coupled seed supplied by the parent researcher and rechecked here
is

    q  = 00305680, q' = 88abc2db,
    p  = 96e4e732, p' = 1f60538d.

Its actual interfaces are

    d(q)=d(p)=D=887b6c5b,
    F(q)=410c6383,   G(q)=778493a5=-D,
    F(p)=bef39c7d=-F(q),   G(p)=345653b1.

It is four words satisfying a local coupled condition, not a complete
difference assignment or actual schedule pair.

The single tested construction family lets every Q position choose an
independent pair with fixed input XOR mask
`alpha_Q=889b945b` and `(d,G)=(D,-D)`. Every P position independently
uses `alpha_P=8984b4bf` and d=D. Every R position independently uses
`alpha_R=f(alpha_Q)=4314a785`. The last choice comes from the masks of
reversed f images of Q pairs, but R words range over their entire
fixed-mask fibres; no equality to a Q image or to another R pair is
imposed.

Exact linear algebra found:

| Fibre | Dimension | Actual pairs | Distinct remaining sigma differences |
|---|---:|---:|---:|
| q mask, preserving `(d,G)` | 5 | 32 | 16 values of F |
| q seed, preserving `(d,F,G)` | 1 | 2 | 1 |
| p mask, with d=D and F opposite one of those 16 Q values | 2 for the only nonempty target | 4 | 4 values of G |

The only compatible P target is the original `A=bef39c7d`. At the
terminal R_3 interface the finite test found no pair. This failure has
a shorter proof that removes D, the P mask, and all affine enumeration:

**Mask obstruction.** Every assignment on S0 satisfying (1) has

    G(R_3)=F(Q_2), i.e. G_52=F_30.                        (5)

This follows directly from t=45, which gives
`d_38=-F_30`, and t=54, which gives `G_52=-d_38`.
If Q_2 has input XOR mask `889b945b` and R_3 has input XOR mask
`4314a785`, their output XOR masks are respectively

    f(889b945b) = 4314a785 = 5 modulo 8,
    g(4314a785) = c722ccc1 = 1 modulo 8.

Two words with XOR mask 5 modulo 8 have modular difference
`+/-1 +/-4`, hence either 3 or 5 modulo 8. Two words with XOR mask 1
modulo 8 have modular difference `+/-1`, hence either 1 or 7 modulo 8.
These sets are disjoint, contradicting (5). Higher bits and carries
cannot change a difference modulo 8.

Consequently the tested three-mask construction family is impossible.
More generally, a necessary condition on arbitrary support-0 pairs is
that the pair of low-three-bit masks

    ( f(W_30 xor W'_30) mod 8,
      g(W_52 xor W'_52) mod 8 )

cannot be `(5,1)` or `(1,5)`. This is a necessary interface condition,
not an exclusion of support 0. Other masks, word differences, and
construction mechanisms remain open. This bounded mechanism stops at
the proven obstruction; no timeout is extended and no seed sweep is
performed.

## 5. Relation to actual schedules and verification scope

A full actual-pair assignment from Section 2 would solve the 48 exact
difference equations. Its 13 first components would still have to lie
on one genuine base expansion. The separately reviewed `base-lift/`
reduction expresses that interpolation by 13 inactive parameters and
ten remaining original base equations. Nothing here proves that such
a base lift exists, or even constructs a full active-pair assignment.

`verify.py` checks the 48 original symbolic equations, the reversible
common-D reduction, the original bit rows, the affine-fibre certificates,
all 32 Q and four surviving P pairs, the local seed, the two boundary
equations used in (5), and the exact mod-8 residue sets. Deliberately
damaged masks, constants, bases and equations are rejected. This is a
separate implementation by the discoverer, not an independent-agent or
external human review. Run receipts and hashes are recorded alongside
the source. No SAT/SMT result is used and no proof assistant is invoked.

The schedule definition is inherited from FIPS 180-4 and the frozen
CRYPTO2 support data. The general signed-bit and binary-linear-fibre
methods are elementary and are not claimed as new. The earlier
literature/source gate remains applicable; this note makes no historical
priority claim or cryptanalytic attack claim.
