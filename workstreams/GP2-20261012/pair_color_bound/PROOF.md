# A uniform gap below quarter density from three pair levels

GP2-20261012, 2026-10-12. Complete elementary written proof.
This note improves the quarter-density bound in `../quarter_bound/PROOF.md`.
It uses the elementary repair theorem to address the **original directed**
general-position problem on `Ka(m,4)`. The alphabet has `m` letters;
adjacent-letter inequalities, digons and every shortest-path quantifier are
unchanged. Historical priority has not been certified.

## 1. Statements

**Theorem 1.** For every finite alphabet `A`, every probability distribution
`mu` on `A`, and every strict window code `C subset A^4`,

    Pr[(U_0,U_1,U_2,U_3) in C] <= 182/729,

where the four letters are independent with distribution `mu`.

**Corollary 2.** For the original Kautz general-position problem,

    gp(Ka(m,4)) <= floor(182m^4/729) + 73m^3     (m>=3),

and

    2/9 <= lambda_4 <= 182/729 < 1/4.

The lower endpoint comes from the independently checked reversal of a
classical eighteen-word ternary code, as explained in
`../review/TERNARY_STRICT_CONSTRUCTION_FROM_LITERATURE.md` and its
independent construction review. The exact remaining density gap is
`20/729`. No exact finite optimum or exact limiting value is claimed.

The upper constant is deliberately an elementary consequence of the new
structural bridge; the nine-color inequality below is not asserted sharp.
Both this theorem and the quarter bound have `O(m^3)` finite corrections
after repair. The separate seven/nine-window moment bound remains useful
at finite alphabet sizes because its correction is only `O(m^2)`.

## 2. Three levels on ordered pairs

A strict window code permits at most two selected occurrences among the
five length-four windows in every eight-letter word. Repeated occurrences
of the same word count separately.

Form a digraph on `A^2` by putting the edge `ab -> cd` exactly when
`abcd in C`. It has no directed walk of three edges: a walk

    B_0 -> B_1 -> B_2 -> B_3

would give three selected windows at positions `0,2,4` in the eight-letter
concatenation `B_0 B_1 B_2 B_3`.

For each ordered pair `v`, let `ell(v)` be the greatest length of a
directed walk ending at `v`, allowing a walk of length zero. There are no
walks of length three or more, so

    ell: A^2 -> {0,1,2}.

Appending an edge to a longest incoming walk shows that every selected
word satisfies

    ell(ab) < ell(cd).                                      (1)

This is an exact consequence for all strict codes. It does not assume that
selected original vertices are independent. The same level argument was
developed in `../global_upper/ENDPOINT_SUPPORT_AND_INDEPENDENT_CODES.md`;
the proof is included here so that this bound does not depend on that note.

## 3. Empty rotation orbits

For independent letters `a,b,c,d`, let

    N = 1_C(abcd)+1_C(bcda)+1_C(cdab)+1_C(dabc).

Strictness gives `N<=1`: if two positions were selected, repeating the
four-letter word would give selected occurrences at `0,j,4` for some
`1<=j<=3`. This also excludes short-period words. Each cyclic rotation
has the same product distribution, so `E N = 4p`, where
`p=Pr[abcd in C]`.

Consider the event

    E = {ell(ab)=ell(cd) and ell(bc)=ell(da)}.

On `E`, condition (1) excludes both `abcd` and `cdab`, and also excludes
both `bcda` and `dabc`. Thus `N=0` on `E`. Pointwise,

    N <= 1-1_E,

and therefore

    4p <= 1-Pr(E).                                         (2)

The remaining question is a finite-color inequality for an arbitrary
three-valued relation on ordered pairs. No optimization over the code
appears in the proof below.

## 4. A reciprocal-pair coloring and two Cauchy inequalities

For `i,j in {0,1,2}`, define a zero-one kernel on two independent copies of
the alphabet by

    K_ij(x,y) = 1_{ell(xy)=i and ell(yx)=j}.

These nine kernels partition `A x A`. Write `d_ij=E K_ij(x,y)`; then
`sum_(i,j) d_ij=1`.

Let `R_ij` be the event that all four pairs

    (a,b), (a,d), (c,b), (c,d)

belong to `K_ij`. On this event `ell(ab)=ell(cd)=i`, whereas
`ell(bc)=ell(da)=j`. Consequently `R_ij subset E`.
The events `R_ij` are pairwise disjoint, since the single pair `(a,b)`
already determines `i,j`. Hence

    Pr(E) >= sum_(i,j) Pr(R_ij).                            (3)

For any nonnegative kernel `K` on two independent copies of `(A,mu)`, put

    T(K) = E[K(a,b)K(a,d)K(c,b)K(c,d)].

Two applications of Cauchy's inequality give

    T(K)
      = E_(a,c) [E_b K(a,b)K(c,b)]^2
      >= [E_b (E_a K(a,b))^2]^2
      >= [E_(a,b) K(a,b)]^4.                               (4)

All expectations are finite sums. No symmetry of `K` is required: the
two sides of this bipartite calculation are independent copies of the
same alphabet, and do not need disjoint underlying sets of symbols.

Apply (4) to every `K_ij`. Since `Pr(R_ij)=T(K_ij)`, equations (3) and
the convexity of the fourth power show

    Pr(E) >= sum_(i,j) d_ij^4
          >= 9 (1/9)^4
          = 1/729.                                        (5)

Combining (2) and (5) proves

    p <= (1-1/729)/4 = 182/729.

This establishes Theorem 1 for every alphabet size and every probability
distribution, including distributions with zero weights.

## 5. Bridge back to the original directed graph

The elementary repair theorem in
`../construction/STRICT_WINDOW_REPAIR.md` states that every original GP
set `S subset Ka(m,4)` contains a strict code `C` with
`|S minus C|<=73m^3`. Its full proof and independent original-adjacency
review are included in this package. The reviewed source SHA256 is
`56ed0af016042abcbca256b52f6fb7539edb908fe81d6ba585a21102f9c4c4f5`.

With the uniform distribution on the original alphabet, Theorem 1 gives
`|C|<=floor(182m^4/729)`. Adding back the deleted vertices proves the
finite upper bound in Corollary 2. Divide by `m^4` and take the limit;
existence is inherited and is also proved by subalphabet averaging in
`../quarter_bound/PROOF.md`, Section 4.

In particular the limiting density is separated from `1/4` by at least
`1/2916`. This is a fixed positive loss from incompatible pair levels,
not an integer-rounding effect that disappears in the limit.

## 6. Relation to ordinary comma-free codes

The upper proof in Sections 2–4 only needs two consequences of strictness:
the prohibition at positions `0,2,4`, and the rotation-orbit bound. Both
hold for an ordinary length-four comma-free code, because its two selected
end windows at positions zero and four forbid a selected interior window.
Thus Theorem 1 also bounds the density of any ordinary length-four
comma-free code.

This observation does not identify ordinary comma-free codes with strict
window codes. The strict model has extra prohibitions at spans two and
three; the explicit counterexample in
`../review/INDEPENDENT_QUARTER_REVIEW.md` separates the classes.

The primitive-orbit count and the eighteen-word ternary dictionary are
classical: S. W. Golomb, B. Gordon and L. R. Welch,
[*Comma-free codes*](https://doi.org/10.4153/CJM-1958-023-9),
Canadian Journal of Mathematics 10 (1958), 202–209.
The historical status of the particular reciprocal-pair inequality and
its application has not been certified. We describe the proof actually
established here and make no claim of priority for a coding-theoretic bound.

## 7. Verification boundary

The proof is a chain of finite combinatorial arguments and exact
inequalities. It does not rely on a floating-point LP, MILP, timeout, or
finite search asserting a universal optimum. A separate independent review
reconstructs the three-level argument, checks the direction of all four
pair conditions, and verifies both applications of Cauchy's inequality.
The original graph semantics enter only through the separately reviewed
repair theorem. No all-parameter Lean proof or successful Lean compilation
is claimed for this new result; internal AI-agent review is not external
human peer review.
