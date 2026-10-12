# A pair-color defect, and an obstruction to the proposed 2/9 upper route

This supplements `ENDPOINT_SUPPORT_AND_INDEPENDENT_CODES.md`. The quarter bound and a stronger strict gap were obtained after that note's final prospective paragraph; see `../quarter_bound/PROOF.md` and `../pair_color_bound/PROOF.md`. The prospective statement there that an upper bound of `1/4` still needed an inequality is therefore superseded. The endpoint lemmas and deletion obstruction themselves are unchanged.

The following arguments are for strict window codes on a finite alphabet with an arbitrary probability distribution. They give valid asymptotic Kautz bounds through the elementary repair theorem, not an exact value of the density. No Lean proof or historical-priority claim is made.

## 1. Four rotations and the pair-color defect

For a strict code `C`, the pair digraph `ab -> cd` when `abcd in C` has no three-edge walk. Let `ell : A^2 -> {0,1,2}` be its canonical increasing level function.

For any four-letter word `w`, at most one of its four cyclic rotation **positions** can be selected. If two rotation positions `i<j` were selected, the periodic eight-letter extension starting at position `i` would select positions `0,j-i,4`. This contradicts strictness even if the occurrences at `0,4` coincide as words. In particular words of period one or two cannot be selected.

If `w=abcd` satisfies

`ell(ab)=ell(cd)` and `ell(bc)=ell(da)`,

none of its rotations can be selected: each would require a strict increase between one of these equal pairs. For four independent letters with their common distribution, put

`p = Pr[abcd in C]`,

`E = Pr[ell(ab)=ell(cd) and ell(bc)=ell(da)]`.

Rotation preserves this product distribution, so averaging the pointwise inequality gives

`4p <= 1-E`.                                              (1)

Thus a universal positive lower bound for this particular directed pair-color pattern improves the quarter bound.

## 2. A rigorous general bound E >= 1/729

The argument below was obtained independently in the main pair-color note and via the equivalent common-profile formulation here.

For `i,j in {0,1,2}`, let

`K_ij(x,y) = 1{ell(xy)=i and ell(yx)=j}`,

and write `s_ij = E K_ij(x,y)`. These nine functions partition the full ordered-pair space, so `sum s_ij=1`.

If all four cross pairs `(a,b),(a,d),(c,b),(c,d)` have the same `K_ij` value one, then

`ell(ab)=ell(cd)=i`, `ell(bc)=ell(da)=j`.

For fixed four letters these monochromatic cross-pair events are disjoint for different `(i,j)`. Therefore

`E >= sum_(i,j) E[K_ij(a,b)K_ij(a,d)K_ij(c,b)K_ij(c,d)]`.

For any nonnegative kernel `K` of mean `s`, two applications of Cauchy–Schwarz prove that the displayed four-factor expectation is at least `s^4`: first condition on `a,c` and square the common-neighbor average over `b`; then average the squares of the column means. No graph symmetry or distinct-letter assumption is needed. Finally, convexity gives

`E >= sum s_ij^4 >= 9*(1/9)^4 = 1/729`.

Together with (1), this proves `p <= 182/729 < 1/4` for every weighted finite strict code. The main pair-color theorem supplies the original-Kautz statement using the repair bound. This is a structural positive gap, not a finite-integrality improvement. Its constant is coarse.

## 3. The attractive general estimate E >= 1/9 is false

The inequality `E>=1/9`, if valid for every three-color function `ell`, would turn (1) into `p<=2/9`. It cannot be used without further restrictions on `ell`: the following construction gives deterministic finite colorings with `E<1/9`.

We first give a rational probabilistic coloring on three equally weighted vertex types. Let `P` be a three-cycle permutation matrix, `J` the all-one matrix, `A=J/3`, and

`B=(I-P)/9`.

Define normalized color operators

`M_0=A/3+B`, `M_1=A/3-B`, `M_2=A/3`.

All entries are nonnegative and `sum M_i=A`. The actual conditional color-probability matrices are `K_i=3M_i`; their entries lie in `[0,1]` and sum to one at every ordered type pair. Up to a cyclic convention, their rows have the three patterns

`K_0 : (2/3,0,1/3)`,

`K_1 : (0,2/3,1/3)`,

`K_2 : (1/3,1/3,1/3)`.

Independently color each ordered edge according to the probability vector given by its endpoint types. When four actual vertices are distinct, the four ordered edges used by the defect event are distinct, so their colors are independent conditional on those types. Averaging over independent types gives

`E_* = sum_(i,j) tr(M_i M_j M_i M_j)`.

Here `A^2=A`, `AB=BA=0`, `tr A=1`, and the elementary identity

`tr B^4 = -1/729`

follows by expanding `(I-P)^4`, using `P^3=I`, `tr P=tr P^2=0`. Thus

`E_* = 1/9 + 4 tr B^4 = 77/729 < 1/9`.       (2)

Every number and matrix in this calculation is rational.

### Deterministic finite existence

Take `3q` vertices, with `q` of each type, and sample the ordered-edge colors independently using the displayed probabilities. Let `E_q` be the empirical defect probability for four independently sampled vertices, with replacement. Four vertices fail to be distinct with probability at most `6/(3q)=2/q`.

For comparison, imagine resampling each of the four involved edge colors separately even if an ordered edge is repeated. Its expected defect probability is exactly `E_*`, because the four independently sampled vertex types are uniformly distributed. On distinct vertices this agrees with the actual coloring experiment; on the remaining tuples the two probabilities differ by at most one. Consequently

`E E_q <= 77/729 + 2/q`.

For every integer `q>=365`, the right side is strictly smaller than `1/9`. Hence some deterministic coloring of a finite alphabet has `E_q<1/9`. This is a direct probabilistic-method existence proof, with no optimization or unverified numerical extrapolation. It is not a strict-code construction.

## 4. What the counterexample does and does not establish

Equation (2) disproves only a claim about **arbitrary** three-color functions on ordered pairs. A level coloring that comes from a large strict code may satisfy additional constraints. In particular, the strict-code support restrictions and the overlapping triple cut from the endpoint note have not been used in the general matrix counterexample.

The independently verified ternary strict construction now gives the lower density `2/9`; see `../review/TERNARY_STRICT_CONSTRUCTION_FROM_LITERATURE.md` and `../construction/lower18_certificate.json`. The present counterexample does not disprove `lambda_4=2/9`, nor provide any strict code above that value. It identifies exactly why the simple unrestricted three-color C4 estimate cannot prove that proposed value.

The next worthwhile upper route must exploit either the canonical nature of the pair levels or the additional prefix/suffix compatibility. Merely optimizing the unrestricted three-color C4 problem cannot establish `E>=1/9`.

## 5. Exact check

`verify_c4_color_counterexample.py` uses only rational arithmetic to verify the matrices, normalization, trace identities, the two evaluations of `E_*` (matrix multiplication and an independent four-type sum), and the explicit finite-existence threshold. Deliberately damaged normalization and sign/trace values must fail. This is a checker of the explicit algebra and finite probabilistic bound; the universal strict-code and Cauchy–Schwarz arguments are the written proofs above.
