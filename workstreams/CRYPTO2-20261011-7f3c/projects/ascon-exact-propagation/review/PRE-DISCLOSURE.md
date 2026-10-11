# Independent pre-disclosure reconstruction: Ascon two-round path exactness

## Independence and scope

This note was completed before reading the discoverer's `discover.py`, rank or mismatch certificates, status file, or proposed proof. I used only the task's candidate statement, the original NIST standard, generic GF(2) linear algebra, and independently written code in this review directory. I did not inspect or reproduce the 2026/358 team's algorithm or source code. A filename search revealed that those files exist, but none of their contents was read.

**Pre-disclosure mathematical assessment:** the at-most-two-initial-columns exactness assertion is valid, supported by a complete finite verification of the required projection ranks and the conditional-uniformity proof below. I independently constructed two three-column paths: one has actual probability zero despite a positive DDT product, and another has actual probability twice that product. These are full 320-bit, two-S-layer paths, not reduced-width experiments.

Historical originality, multi-round attacks, and an attack on an instantiated keyed Ascon mode are outside this assessment.

## Original-standard reconstruction and conventions

Primary source: NIST SP 800-232, August 2025, Section 3, especially Section 3.2, equation (7), Table 6, and equations (8)–(12):

https://doi.org/10.6028/NIST.SP.800-232

https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-232.pdf

The source was opened directly through the web tool. The state has five 64-bit words. A round adds its constant to word/lane 2, applies 64 parallel 5-bit S-boxes, and then applies independent linear maps to the five words. I independently transcribed all five S-box coordinate polynomials and checked their outputs against all 32 entries of the standard's Table 6.

A column value is encoded as

\[
x=16x_0+8x_1+4x_2+2x_3+x_4.
\]

Thus lane 0 is the most significant bit of the 5-bit column value, matching Table 6. My column index j is the numerical word-bit position of 2^j, with j=0 the least significant bit. These conventions are stated to prevent an accidental lane-bit reversal when comparing certificates.

The word rotation pairs, in lane order 0 through 4, are

\[
(19,28),\ (61,39),\ (1,6),\ (10,17),\ (7,41).
\]

For pair (a_i,b_i), the output bit at position j is the XOR of source bits j, j+a_i, and j+b_i, modulo 64. A separate direct word-rotation implementation was checked against the row-incidence representation on all 320 word-bit basis vectors.

The specific two constants for the independent counterexamples are 0xf0 followed by 0xe1, added to lane 2 before each S layer. The standard lists these as the first two constants of its 12-round permutation. The at-most-two-columns proof below actually works for arbitrary fixed additive constants at those positions, and even for arbitrary fixed 320-bit additive masks there.

## Exact event being assessed

Let X be uniform on the entire 320-bit vector space. Let K_1,K_2 be fixed round-constant masks, and write S for the parallel substitution layer. Define

\[
U=X+K_1,\qquad Y=S(U),\qquad Z=L(Y)+K_2.
\]

All additions in state equations are XOR. For a fixed input difference A, the first event is

\[
E_1:\quad S(U+A)+S(U)=B.
\]

On E_1, the second S-layer input difference is exactly \(\alpha=L(B)\). The second event is

\[
E_2:\quad S(Z+\alpha)+S(Z)=C.
\]

The joint path probability is \(\Pr[E_1\land E_2]\). It is not the unconditional probability of a two-round input/output differential summed over possible intermediate B values. A final application of L after the second S layer would merely map the fixed difference C to LC and would not change this path probability.

For one S-box define

\[
D(a,b)=\#\{x\in\{0,1\}^5:S(x+a)+S(x)=b\}.
\]

The nominal local-DDT product is

\[
P_{\rm DDT}=\prod_{j=0}^{63}\frac{D(A_j,B_j)}{32}
              \prod_{j=0}^{63}\frac{D(\alpha_j,C_j)}{32}.
\]

## Why a projection-rank condition suffices

Let I be the set of nonzero columns of A. Because U is uniform and S is a permutation, Y is uniform across all 320 bits. The first event E_1 imposes separate constraints only on columns in I. For a feasible B, B is zero outside I. Conditional on E_1, all Y columns outside I remain jointly uniform, independent of the constrained columns Y_I. This uses permutation of the S-box, not any Markov assumption about successive rounds.

Let T be the set of nonzero columns of alpha. Fixing the constrained values Y_I leaves the second input coordinates Z_T as an affine function of the uniform free coordinates Y_(I-complement). If the linear map from those free coordinates to all 5|T| bits in Z_T has full row rank, then Z_T is uniform and independent of Y_I. Therefore it stays uniform after conditioning only on E_1. Its columns are independent, and

\[
\Pr[E_2\mid E_1]=\prod_j D(\alpha_j,C_j)/32.
\]

Independence of the first input columns gives \(\Pr[E_1]=\prod_j D(A_j,B_j)/32\), proving equality with the joint product.

The infeasible cases need no conditional argument. If a first local DDT entry is zero, E_1 is impossible and both sides are zero. If alpha_j=0 but C_j is nonzero, E_2 is impossible and both sides are zero. If I is empty, the only feasible path has A=B=alpha=C=0 and both sides are one.

## Complete independent rank check for one or two active columns

For every possible B supported on I, all potentially active second columns lie in the envelope

\[
T^*(I)=\bigcup_{i=0}^4\bigcup_{u\in I}\{u,u-a_i,u-b_i\}\pmod {64}.
\]

For each lane i, each row j in T^*(I) has source support

\[
\{j,j+a_i,j+b_i\}\setminus I.
\]

The full free projection is block diagonal by lane. I represented each lane's row as a 64-bit GF(2) incidence vector after deleting source positions I, and performed exact XOR Gaussian elimination. Checking the envelope is stronger than checking the actual support T, because any subset of independent rows is independent.

Cyclic translation simultaneously permutes source and target coordinates and preserves these ranks. Therefore every singleton support is represented by {0}, and every two-column support is represented by {0,h}, 1<=h<=63. This normalization remains legitimate with fixed unrotated round constants because constants only change affine offsets, not the rank condition or the resulting uniformity.

The independent results are:

* For I={0}, the envelope has 11 columns and each of the five lane matrices has rank 11.
* For every one of the 63 normalized pairs {0,h}, every lane matrix has rank exactly the envelope size. There are no deficient pair cases.

This exhausts all one-column and two-column placements on the full 64-column state. It covers all nonzero 5-bit differences at those columns and every feasible B without enumerating their values, because the rank argument deliberately uses the larger value-independent envelope.

The code is `independent_probe.py`; the complete rank results are `independent_projection_results.json`. The rank routine is short, standalone Python using integer XOR, with no dependency on the discoverer's code. This is a finite computer-assisted rank proof; I have not replaced it with an entirely symbolic classification of the 63 separations.

The S-box-specific fact used for the positive theorem is only that it is a permutation. The rank argument would apply to any 5-bit permutation substituted into the same 5-lane diffusion geometry. The counterexamples below do use the actual Ascon S-box.

## Independent three-column obstruction search

For orientation, I also checked all 1953 normalized triples {0,a,b}, 1<=a<b<=63. Exactly 30 have an envelope projection deficient by one bit; the other 1923 have no deficiency. This is a search over column geometry only, not an exhaustive search over differences or a full-state enumeration.

A rank failure alone is not a path-probability counterexample. To establish an actual mismatch, I independently constructed the following transitions for I={0,1,6}.

Set

\[
A_j=2,\quad B_j=25\qquad(j\in\{0,1,6\}),
\]

and set all other columns of A and B to zero. Decimal values here use the standard column encoding above.

The four local first-layer inputs realizing 2 to 25 are

\[
\{16,18,28,30\},
\]

and their S-box outputs are

\[
\{30,7,22,15\}.
\]

All four outputs have lane-2 bit equal to one. Thus, conditional on E_1,

\[
Y_{2,0}=Y_{2,1}=Y_{2,6}=1.
\]

Since lane 2 uses rotations 1 and 6 and bit zero of 0xe1 is one,

\[
Z_{2,0}=Y_{2,0}+Y_{2,1}+Y_{2,6}+1=0.
\]

The active columns and values of alpha=L(B) are

| Columns j | alpha_j |
| --- | --- |
| 0,1,6 | 25 |
| 3,4,9,25,26,31 | 8 |
| 23,24,29,57,58,63 | 1 |
| 36,37,42,45,46,51 | 16 |

There are 21 active second columns. The free projection to these exact active columns has lane ranks

\[
(21,21,20,21,21).
\]

In lane 2 the row for j=0 is zero after deleting the three constrained input columns. The other 20 rows are independent. All rows in the other four lanes are independent. Therefore, conditional on any allowed first-layer values, the 104 second-input bits other than Z_(2,0) are jointly uniform and independent; Z_(2,0) is the fixed zero identified above. Mixing over the allowed first-layer values preserves that same uniform hyperplane distribution.

## Two explicit exact path mismatches

For every j other than zero, choose

\[
C_j=S(0)+S(\alpha_j).
\]

This makes the local second DDT entry positive; inactive columns have C_j=0. Consider the following two choices at column zero:

1. **Zero-probability witness:** C_0=3. The local transition 25 to 3 has four inputs {5,13,20,28}, all with lane-2 bit one. But the actual second input has Z_(2,0)=0. Thus the actual joint path is impossible.
2. **Positive mismatch witness:** C_0=6. The local transition 25 to 6 has four inputs {2,10,19,27}, all with lane-2 bit zero. On the actual 16-element slice Z_(2,0)=0, its local probability is 4/16, twice its unconditional DDT probability 4/32. All other active second columns retain their uniform independent distributions.

For both witnesses the nominal DDT product is exactly 2^-66. The actual joint probabilities are respectively

\[
0\qquad\text{and}\qquad 2^{-65}.
\]

These exact fractions count the whole uniform 320-bit sample space. The first constant 0xf0 has been included in the model and is absorbed by the bijective translation X to U; no initial state restriction is silently introduced. The second constant 0xe1 is used explicitly in the fixed-bit calculation.

`independent_witness.py` checks the DDT solution sets, computes alpha, checks the relevant projection ranks and zero row, and computes both exact rational probabilities. Complete A,B,alpha,C arrays and local DDT counts are recorded in `independent_witness_results.json`. The computation uses the generic conditional-uniformity argument above, not a routine imported from any research implementation.

## Pre-disclosure conclusion and limitations

I find the proposed two-column bound mathematically sound: for every A supported on at most two 5-bit columns and every fixed B,C and fixed round constants, the actual two-S-layer joint path probability equals the product of local DDT probabilities. The proof consists of a general conditional-uniformity lemma plus an exhaustive, exact check of the finite column-placement rank condition.

Three initially active columns suffice for failure under the specified f0/e1 constants; the independent witnesses above establish both a zero-versus-positive mismatch and a positive factor-two mismatch. A deficient rank does not universally imply a mismatch; these witnesses explicitly verify the missing additional local constraints.

This does not state that arbitrary multi-round trail products are exact, that sums of paths equal an individual path probability, that a fixed-key/state-restricted experiment is uniform on 320 bits, or that these examples yield an attack on a standardized Ascon construction. Historical originality and external peer review are not certified. The discoverer's artifacts remain unread at sealing time.
