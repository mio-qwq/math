# Independent interfaces for the S0 active-pair relaxation

This derivation was completed before reading the author construction. All
arithmetic is in R = Z/(2^32). A word pair X = (x,x') has
d(X) = x'-x, F(X) = f(x')-f(x), G(X) = g(x')-g(x), where f and g
are the FIPS 180-4 small sigma0 and sigma1. Every active pair must be
unequal; inactive pairs contribute zero to all three differences.

The active coordinates are Q_j at 2+14j, j=0..4; P_j at 9+14j,
j=0..3; and R_j at 10+14j, j=0..3. Use dQ_j, FQ_j, GQ_j and the
analogous notation for the other two families.

## 1. All 48 original equations

For every t=16,...,63, the original equation is

    d_t - G_(t-2) - d_(t-7) - F_(t-15) - d_(t-16) = 0.

Filtering its five actual indices by the support gives exactly the
following 24 nontrivial equations; the other 24 are 0=0.

| t | Equation |
|---|---|
| 16 | dQ1 = dP0 |
| 17 | dR0 + FQ0 = 0 |
| 18 | GQ1 + dQ0 = 0 |
| 23 | dP1 = dQ1 |
| 24 | dR1 = FP0 |
| 25 | GP1 + FR0 + dP0 = 0 |
| 26 | GR1 + dR0 = 0 |
| 30 | dQ2 = dP1 |
| 31 | dR1 + FQ1 = 0 |
| 32 | GQ2 + dQ1 = 0 |
| 37 | dP2 = dQ2 |
| 38 | dR2 = FP1 |
| 39 | GP2 + FR1 + dP1 = 0 |
| 40 | GR2 + dR1 = 0 |
| 44 | dQ3 = dP2 |
| 45 | dR2 + FQ2 = 0 |
| 46 | GQ3 + dQ2 = 0 |
| 51 | dP3 = dQ3 |
| 52 | dR3 = FP2 |
| 53 | GP3 + FR2 + dP2 = 0 |
| 54 | GR3 + dR2 = 0 |
| 58 | dQ4 = dP3 |
| 59 | dR3 + FQ3 = 0 |
| 60 | GQ4 + dQ3 = 0 |

The checker stores all 48 unfiltered five-term rows as well as their
filtered rows, then checks them against these independent family
formulas. In particular, the range ends at 63 and no recurrence at
t=64 or above is imposed.

## 2. Exact module equivalence and boundaries

For 13 actual unequal pairs, all 48 equations hold if and only if there
is D != 0 such that all of the following hold:

1. dP_j = D for j=0..3, and dQ_j = D for j=1..4.
2. GQ1 = -dQ0, and GQ_j = -D for j=2,3,4.
3. dR_j = -FQ_j for j=0..3.
4. GR_(j+1) = -dR_j for j=0..2.
5. FP_j = dR_(j+1) for j=0..2.
6. GP_(j+1) = -D-FR_j for j=0..2.

Proof: the seven equations at t=16,23,30,37,44,51,58 are a connected
path through P0,Q1,P1,Q2,P2,Q3,P3,Q4. They are equivalent to condition
1, with D=dP0. D is nonzero because P0 is an active unequal pair.
The remaining 17 nontrivial rows are exactly conditions 2--6 after
substitution of this common D. Every transformation is substitution
or multiplication by -1, valid in R; there is no division by a
nonunit. Reading these steps backwards proves sufficiency.

The leftmost pair Q0 is not on the common-D path. In particular,
setting dQ0=D without a separate justification would change the
model. The left boundary consists of the actual equations dQ1=dP0,
dR0=-FQ0 and GQ1=-dQ0. On the right, Q4 must have dQ4=D and GQ4=-D;
no FQ4 condition occurs. There is no FP3 or FR3 condition.

If Q4 is omitted from a proposed reduced module, it must be shown to
exist. Here that existence is automatic once the retained Q2 (or Q3)
is an actual pair with d=D and G=-D: assign Q4 the identical ordered
pair. Reusing a value at a different coordinate is permitted in the
independent-pair model. This observation would not justify a similar
assignment in a true base schedule. Merely specifying a nonzero
abstract D, without an actual Q2/Q3 witness, would not establish Q4
existence: one would need an x with g(x+D)-g(x)=-D.

All nonzero conditions concern actual pairs, not independent symbols
d,F,G. In particular the module is not an unrestricted linear
feasibility theorem for 39 unrelated residues.

## 3. Exact parametrizations of the R chain

Both small sigmas are linear permutations of the 32-dimensional
binary vector space. For the invertibility used here, the checker
constructs each bit matrix from FIPS source positions, performs
Gaussian elimination, and supplies 32 inverse-image basis words for
each map. All 64 basis-image equations are checked. Linearity then
proves the inverse on every word; no word-space enumeration is used.

Given an unequal R0 and arbitrary image parameters z1,z2,z3 in R,
recursively let r_j=d(R_j) and define

    R_(j+1) = (g^(-1)(z_(j+1)), g^(-1)(z_(j+1)-r_j)), j=0,1,2.

This satisfies GR_(j+1)=-r_j exactly. Since r_j != 0, the two sigma
images differ, so the next pair remains unequal. It describes every
solution of the R chain: recover z_(j+1)=g(first word of R_(j+1)).
The parameterization is therefore bijective for a fixed R0. A free
first-word parameter gives the equivalent expression
(x, g^(-1)(g(x)-r_j)). A carry or wrap in z-r_j is allowed.

An equivalent backward construction starts with any unequal R3 and
chooses arbitrary first words a2,a1,a0. Recursively define

    R_j = (a_j, a_j-G(R_(j+1))), j=2,1,0.

Injectivity of g makes G of an unequal pair nonzero, so each R_j is
unequal. The same recovery of first words proves completeness.

These parameterizations solve only the three R-chain equations.
They do not discharge the four FQ/dR interfaces or the P equations.
In particular the individual nonzero r_j need not equal one another
or equal the common P/Q difference D.

## 4. A necessary interface and a fixed-XOR exclusion

Subtract the t=45 and t=54 equations to obtain

    G52 = GR3 = FQ2 = F30.

More generally GR_(j+1)=FQ_j for j=0..2. This constraint is present
even when all R-chain pairs individually satisfy their own equations.

Suppose Q2 has XOR mask K=0x889b945b and R3 has XOR mask
L=0x4314a785. FIPS bit reconstruction gives

    f(K) = 0x4314a785,
    g(L) = 0xc722ccc1.

Linearity over XOR implies that the output XOR masks for the two
differences FQ2 and GR3 have low three bits 5 and 1, respectively.
For any z,z' with z XOR z' = m, the additive difference modulo 8
belongs to {((b XOR (m mod 8))-b) mod 8 : b=0,...,7}.
For m mod 8 = 5 that set is {3,5}: the weight-4 contribution is
always 4 modulo 8, and the weight-1 contribution is +/-1. For
m mod 8 = 1 the set is {1,7}. These sets are disjoint. Consequently
the necessary equality G52=F30 is impossible for those two fixed
masks, for arbitrary bases and arbitrary higher carries.

This exclusion concerns only that fixed-mask choice. It needs no
enumeration of the author's purported 32 or 4 fibers and supplies no
claim about their cardinalities. No active-pair solution, base lift,
full schedule or improved global distance bound follows.
