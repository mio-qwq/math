# All three-column supports: exactness classification and a sharp error bound

Definitions and conventions are those of PROOF.md. This is a complete
written theorem for the restricted full-width model, with a finite exact
rank certificate. The frozen-source review and current replay are recorded
in ../VERIFICATION.json. No Lean proof, attack, or historical-priority
claim is made.

## Theorem 2

For the actual 64-bit Ascon rotation pairs (a_l,b_l), let E be the following
ten translation orbits of three-element column sets in Z/64Z:

    I = {s, s+k*a_l, s+k*b_l},  l=0,...,4, k in {1,2}, s in Z/64Z.

These are 640 distinct supports out of C(64,3)=41664. Fix arbitrary constants
c0,c1 and differences A,B,C, with A supported on exactly three columns I.

1. Let E1 be only the five k=1 orbits, comprising 320 supports. If I is
   outside E1, the actual joint two-round trail probability P equals the
   local-DDT product M, for every choice of A,B,C,c0,c1.
2. For every I, including E, 0 <= P <= 2M. The upper bound and zero lower
   bound are attained by the certificates in PROOF.md with M>0.
3. For I in E and M>0, P has the explicit formula below, requiring only
   local 32-point S-box sums, with no enumeration of 320-bit states.

The ten-orbit family E classifies failure of the sufficient free-value
projection condition; only the five-orbit subfamily E1 admits actual
product errors. Formula witnesses for all five lanes prove this last
assertion, and translate to each member of E1. It does not say every trail
on E1 fails. The formula decides each trail's error. Two is the largest
universal input-column threshold, while 41344 of 41664 three-column
supports also have universally exact products.

## 1. Exact finite linear-algebra certificate

For J=I+T with T as in PROOF.md, restrict Y -> (LY)_J to columns outside I.
Translation reduces all supports to {0,i,j}, 1<=i<j<=63: 1953 cases.
`triple-rank-certificate.json` lists all five ranks for every case.
`check_triples.py` independently reconstructs free-input column images,
checks all 9765 ranks, and regenerates the exception family above.

For 1923 normalized cases all five blocks are onto. The remaining 30
cases are exactly the three possible zero-anchored translates of each
of the ten representative triples. Each has exactly one rank deficiency,
in the corresponding lane l; its other four blocks are onto. No triple
has a nontrivial translation stabilizer since its size 3 is coprime to 64.
Thus each orbit has 64 members and the ten disjoint orbits contain 640
supports. The other 41024 supports satisfy the product equality.

There is a simple explicit missing parity in every exceptional case.
Let t be a binary mask on lane l of the second-round input, supported on

    K={s}                 if k=1;
    K={s,s+a_l,s+b_l}     if k=2.

Then K is contained in J and

    <t,LY> = sum_{i in I} Y_(l,i).

For k=1 this is one row of L. For k=2 it follows by squaring
(1+z^a+z^b) in characteristic two: the cross terms vanish. Consequently
t annihilates the free-input image. The rank certificate proves that
this is its only independent missing parity; the image is exactly the
hyperplane <t,w>=0, not merely a subset of it.

## 2. Exact error formula

Assume M>0. Set alpha=LB and define the nonempty local sets

    F_i = {S(x): S(x)+S(x+A_i)=B_i},  i in I;
    G_j = {z: S(z)+S(z+alpha_j)=C_j}, j in J.

When alpha_j=C_j=0, G_j is the full set of 32 column values. Define

    beta_F = product_{i in I} [ sum_{y in F_i} (-1)^(y_l) / |F_i| ];
    beta_G = product_{j in K} [ sum_{z in G_j} (-1)^(z_l) / |G_j| ];
    eta = (-1)^(sum_{j in K} (c1)_(l,j)).

Then the exact full-width trail probability is

    P = M * (1 + eta * beta_F * beta_G).                       (1)

Proof: condition on the first event. The Y_I are independent uniform
elements of their F_i. For any fixed Y_I, the free columns make (LY)_J
uniform on the affine hyperplane whose parity is sum_{i in I}Y_(l,i).
After averaging over Y_I and translating by c1, the mass function of
Z=(LY+c1)_J at z is exactly

    2^(-5|J|) * [1 + eta * beta_F * (-1)^(<t,z>)].

Sum this density over the rectangle product_{j in J}G_j. The uniform
term gives the second DDT product. The character term factors into the
coordinate averages beta_G. Multiplying by the first-event probability
gives (1). Since both beta factors lie in [-1,1], 0<=P<=2M.
If M=0, a locally impossible transition makes P=0 directly; no division
by an empty fiber is performed. This proves all three statements.

For a standard round constant only lane 2 contributes to eta; the general
statement allows arbitrary fixed 320-bit constants. c0 disappears because
X+c0 is still uniform. Translation reductions used for ranks do not assume
that a fixed round constant is rotation invariant: the actual constant's
positions remain in eta.

## 3. Why all five doubled-support families still have exact products

Each F_i is invariant under y -> y+B_i, because swapping the paired S-box
inputs swaps their outputs. Thus a nonzero lane-l bias in F_i implies
(B_i)_l=0. If beta_F=0 the correction already vanishes. Otherwise every
active B column has lane l equal to zero.

For k=2, use the following positions j in K. The table lists all possible
lane/source contributions to alpha_j= (LB)_j, relative to shift s=0;
all positions are modulo 64 and the same table translates for any s.

| l | I | j | (lane, source position) influencing alpha_j |
|---|---|---|---|
| 0 | {0,38,56} | 19 | (0,38) |
| 1 | {0,58,14} | 61 | (1,58), (3,14) |
| 2 | {0,2,12} | 1 | (2,2) |
| 3 | {0,20,34} | 17 | (3,34) |
| 4 | {0,14,18} | 41 | (4,18) |

For l=0,2,3,4, alpha_j=0. Since M>0, C_j=0 and G_j is all 32 inputs,
so its lane-l bias is zero. For l=1, alpha_j is either 0 or the single
lane-3 bit, encoded as 8. In the latter case the standard S-box satisfies

    D_8 S(z) = D_8 S(z xor 6) for every z in F2^5.

This is checked over all 32 inputs by the independent table checker;
it also follows since the affine derivative's columns for bits 1 and 2
are both 2. Translation by 6 flips lane 1 and pairs every solution in G_j,
so this fiber also has zero lane-1 bias. Hence beta_G=0 in every doubled
support case and P=M. This is a necessary refinement beyond rank alone.

For each of the five k=1 lane families, the formula certificate supplies
two examples with beta_F*beta_G nonzero. They prove failure for some
differences at every translate of that support: translating the differences
preserves the two bias magnitudes, while a fixed round constant changes
only eta's sign. This works for every c0,c1. Consequently E1 is exactly
the set of three-column supports which do not have universally exact
trail products. No endpoint-differential failure is inferred from this.

## 4. Verification and relevance

The rank checker uses physical bit images and low-pivot column elimination;
the discovery certificate uses equation rows and high-pivot elimination.
Additional formula examples cover all ten exceptional families; their
exact probabilities are first obtained by eliminating free variables in
the full derivative system, then checked via (1) using NIST's lookup table.
These bounded examples are sanity checks for the formula and existence
certificates in its five exceptional lane families, not the proof of the
quantified formula. Damaged ranks, family labels, missing cases and false exact
probabilities are rejected.

Summing the inequality over B gives a factor-two upper bound on each
two-round endpoint differential for every three-column A, relative to
the DDT-product composition. Equality holds outside the 320 support
exceptions. For signed DL sums a relative factor-two bound does NOT follow,
because cancellation matters; (1) gives the correct per-trail correction.
It does not establish all-round approximation error or full AEAD security.

The general character-density identity is elementary and existing diffusion
independence theory is explicitly prior art. The concrete contribution
under investigation is the complete standard-width support classification,
the sharp universal factor, and the checkable local error formula for this
restricted Ascon problem. Historical originality remains unconfirmed.
