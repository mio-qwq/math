# Blind reconstruction of support-12 sigma0 anti-cycle constraints

This independent derivation and its complete binary table were frozen
**before opening any file in the author's `support12-structure-v7/`**.
Its scope is necessary constraints on actual local word pairs, not complete
support attainability or an improved global message-schedule distance.

## Derivation directly from all original lagged rows

Read only the pinned fifteen-support JSON, hash
`02a12d8caa3ee3b78ec140f20fc0ad253835a6d32273247d20d22e0d8818edaf`.
Its support 12 is
`{10,11,13,15,18,20,26,28,29,34,42,43,57}`.
The reviewer reconstructs all 48 integer rows

```
E_t=d_t-G_(t-2)-d_(t-7)-F_(t-15)-d_(t-16), 16<=t<64,
```

with inactive indices contributing zero. In the word ring R=Z/(2^32),
actual schedule pairs satisfy all E_t=0, with d,F,G at each coordinate
coming from its same two real words. Two exact original-row combinations
give

```
-E33 = d26+F18,
-E41-E34 = F26+d18.
```

Let X be the actual ordered pair at coordinate 18, P the actual ordered
pair at 26, D=d18, and A=F18. Then

```
(d(X),F(X))=(D,A),
(d(P),F(P))=(-A,-D).
```

D is nonzero since 18 is active. A is nonzero since d26=-A and 26 is
active. This is a universal necessary consequence of the original rows;
it does not assign independent derivative values in place of actual pairs.

## Complete valuation-signature reconstruction

For nonzero residues D,A, let k=v2(D) and l=v2(A), both in {0,...,31}.
For two words z,z', the least position in which they differ is both
the valuation of z'-z modulo 2^32 and the least set bit of z xor z'.
The original sigma0 map is binary linear. Hence any actual X requires
a nonzero input XOR mask B with

```
ctz(B)=k, ctz(f(B))=l,
f=ROTR7 xor ROTR18 xor SHR3.
```

The opposite-difference pair P requires the transposed signature (l,k),
since negation preserves the valuation of a nonzero residue. This is a
condition on valuations only; it forgets the actual magnitudes of D,A
and does not suffice to build an additive anti-cycle.

For each output position j the reviewer constructs f's original row
from input positions `(j+7) mod 32`, `(j+18) mod 32`, and `j+3` when
`j+3<32`. These 32 binary rows are checked against direct rotations and
shifts on every basis vector. For every one of the 32*32 signatures,
the exact affine binary equations are

```
B_i=0 for i<k; B_k=1;
(f(B))_i=0 for i<l; (f(B))_l=1.
```

The independent checker provides a verified satisfying 32-bit mask for
each of the 417 feasible systems. For each of the 607 infeasible systems,
it provides an explicit XOR combination of the original constraint rows
whose left side is zero and whose right side is one. Thus every negative
entry is backed by a finite original-row proof of 0=1. No solver status,
message search or enumeration of 2^32 input words is used.

A different test independently checks all 1,024 results. Let H consist
of the homogeneous low input and low output zero rows. The two required
forms, B_k and (f(B))_l, must both restrict nontrivially to ker(H). This
condition is also sufficient over F2: two nonzero forms have joint image
either the diagonal span of (1,1) or the full two-dimensional space, and
both contain (1,1). Each form is nonzero on ker(H) exactly when adjoining
it increases row rank. All 1,024 homogeneous-form tests agree with the
affine witnesses and contradiction certificates.

Intersecting the exact forward signature table with its transpose leaves
309 compatible ordered valuation pairs. Direct verification of **every**
remaining entry gives the necessary constraints

```
k+l <= 30,
k <= 23 and l <= 23,
if l >= 18, then k=l-18 <=5.
```

The high-l entries are exactly
`(0,18),(1,19),(2,20),(3,21),(4,22),(5,23)`.
By symmetry the corresponding high-k restriction also holds. The sum
bound and individual maxima are reached in this signature relaxation;
no sharpness for coupled additive pairs or whole schedules is asserted.

The rule for high l also has a direct bit proof. An input mask with least
set bit l>=18 has no bits below l. Its ROTR18 contribution first appears
at l-18, while ROTR7 and SHR3 first appear later. Thus its output valuation
is exactly l-18. Applying this to P gives k=l-18. The maximum 23 is
certified by the complete two-direction table.

## Independent orientation check for the three-pair image condition

The same reconstruction also checks seven further original-row identities:

```
E34 = d34-d18,
-E49-E42+E33 = F34-F18,
-E20-E27+E18 = G18+d13+d18,
-E36-E29+E27-E18 = G34+d13-d18,
-E50-E34 = d43+d18,
-E58-E42+E33 = F43-F18,
-E45-E29 = G43+d13.
```

Consequently with T=-d13, the actual pairs at coordinates 18,34,43 have
the interfaces

```
(d,F,G)18 = (D,A,T-D),
(d,F,G)34 = (D,A,T+D),
(d,F,G)43 = (-D,A,T).
```

T is nonzero in an exact support-12 pair because coordinate 13 is active.
Define the forward joint derivative image at D by

```
I_D = { (f(z+D)-f(z), g(z+D)-g(z)) : z in R }.
```

The two first pairs already point forward by D. Reversing the ordered
third pair changes its input difference to D and changes **both** sigma
differences to their negatives. The necessary image membership statement
is therefore

```
(A,T-D) in I_D,
(A,T+D) in I_D,
(-A,-T) in I_D.
```

For fixed D,A,T these memberships are exactly equivalent to the existence
of **these three independent actual pairs with the displayed interfaces**:
choose a realizing first word for each image member, and reverse the
third resulting forward pair. This local equivalence does not establish
the anti-cycle pair at coordinate 26, the other original interfaces,
common base-message solvability, or full support feasibility. In
particular `(-A,+T)` would be an incorrect reversal of the third pair.

## Reproduction and frozen independent scope

```
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-structure-review-v7/check_signatures_independent.py
```

The command is read only, rebuilding and checking the full table against
the frozen `SIGNATURES.json`. `--save` was used for the initial independent
construction and writes only the two independent JSON files here.
Six damaged controls are rejected: wrong sigma row, zero feasible mask,
invalid infeasibility combination, falsely feasible anti-cycle entry,
altered forward entry, and an incorrect original-row anti-cycle sign.
`INDEPENDENT_RUN.json` records the actual outputs and source hash.

This blind packet proves the exact binary-signature table and the
resulting necessary bounds, together with the correct orientation of the
local three-pair image criterion. Author-v7 comparison has not been used
as a premise. There is no actual message witness, support exclusion,
global distance-14 proof, Lean formalization, human peer review or
historical novelty conclusion.
