# Independent acceptance review: reciprocal trace upper bound

Date of actual review and execution: 2026-10-12 UTC.

**Verdict: PASS for the all-parameter written mathematical proof and its
stated strict-code/Kautz consequences.** No mathematical correction was
needed. The finite checker is supporting semantic and algebraic evidence;
it is not a replacement for the universal arguments reviewed below. This
is an independent agent review, not external human peer review, a complete
Lean formalization, or a historical originality certificate.

The accepted candidate is `../RECIPROCAL_TRACE_BOUND.md`, SHA256
`7095f6e72557ca0f7635206048277c914cc3d6afdbaa2f608ad3cf7c555ab1ab`.
The candidate labels itself 2026-10-13; the execution timestamp here is the
actual UTC date rather than an inferred date from that label.

## 1. Inputs, independence, and acceptance boundary

Before reviewing, this reviewer read `AGENTS.md`, the continuity files, the
live primary status, and the actual source proof. The live Git state was
inspected and `git fetch origin` completed. All writes are confined to this
new `trace_review/` directory; no Git commit or publication is made here.

The reviewer independently reconstructed the event truth table, trace-word
expansions, finite weighted tensor counts, weighted Gram inner products,
quartic tangent identity, and binary strict-window semantics. The new
standard-library checker imports no candidate checker, discovery program,
optimization package, matrix library, or prior computational result.

The scope accepted is:

* Every finite nonempty alphabet, every probability distribution on it,
  including zero weights, and every arbitrary level function
  `ell:A^2->{0,1,2}` satisfy the displayed lower bound for `E_ell`.
* Every strict four-window code satisfies the resulting product-density
  upper bound, with repeated occurrences counted separately.
* The finite original directed Kautz consequence holds for alphabet size
  `m>=3`, using the independently inspected written `73m^3` repair theorem.
* The upper endpoint for `lambda_4` follows by division by `m^4` and the
  inherited density-limit theorem. The lower endpoint `beta` is inherited
  from the bound revision and its separate weighted/construction reviews.

The acceptance does not assert that the new constant is optimal, that the
relaxed relation problem is identical to strict-code optimization, or that
the exact general-position number or exact `lambda_4` is known. The
candidate's historical literature statements are not independently checked
by this mathematical acceptance review.

## 2. Event reconstruction, including repeated letters

For an off-diagonal class `i<j`, list the four row-to-column pairs in order

`(a,b), (a,d), (c,b), (c,d)`.

Each pair is either in `K=K_ij` or in `K^t=K_ji`. Let its bit be one for
`K` and zero for `K^t`. The equality `ell(ab)=ell(cd)` equates bits one and
four. The equality `ell(bc)=ell(da)` equates the reversed labels on pairs
three and two and hence equates bits three and two. Of the sixteen formal
direction patterns, the eligible ones are exactly:

| Pattern | Cross-pair kernels | Weighted probability |
| --- | --- | --- |
| `1111` | `K,K,K,K` | `T(K)` |
| `0000` | `K^t,K^t,K^t,K^t` | `T(K)` |
| `1001` | `K,K^t,K^t,K` | `L(K)` |
| `0110` | `K^t,K,K,K^t` | `L(K)` |

For `1001`, the four `K` factors are precisely
`K(a,b)K(b,c)K(c,d)K(d,a)`. Thus the coefficient is `2(T+L)`, not `T+L`,
`2T`, or `4T`. Transposition leaves both four-letter product-weight counts
unchanged, by relabeling the four summed indices.

The kernels `K` and `K^t` have disjoint support for `i!=j`. Repeated letters
can identify some of the cross pairs and make a formal direction pattern
impossible, but never cause two distinct eligible events to overlap. In
particular `K(x,x)=0` for off-diagonal classes. The tuple sums do not discard
any repeated-letter tuple or collapse its multiplicity.

For the diagonal class, all four cross pairs in `K_ii` imply the two desired
equalities and contribute `T(K_ii)`. Across different unordered reciprocal
classes, the pair `(a,b)` already separates the events. All counted events
are disjoint subsets of `E_ell`; other mixed-class tuples can belong to
`E_ell` and are deliberately omitted. This establishes universally

`E_ell >= sum_i T(K_ii) + sum_(i<j) 2(T(K_ij)+L(K_ij))`.

The three diagonal masses and three unordered off-diagonal masses partition
`A^2`; they are nonnegative and sum to one under arbitrary probability
weights. No symmetry of `ell` is assumed.

## 3. Dimension-independent trace and Gram verification

Let `M` be any entrywise nonnegative real square matrix and use the
candidate's `T,L,Y,X`. The weighted application is a special case; no
indicator or disjoint-support assumption is needed for this matrix lemma.

`Y=||M^2||_F^2`, while `T=||MM^t||_F^2=||M^tM||_F^2`. Cyclic trace gives

`<MM^t,M^tM>_F = tr(MM^tM^tM) = tr(M^2(M^t)^2) = Y`.

Frobenius Cauchy therefore gives `Y<=T`. This is not a commutation claim
about `MM^t` and `M^tM`.

For `B=M^2+(M^t)^2`, `D=MM^t+M^tM`, both matrices are symmetric. Expanding
and applying cyclic trace and transposition yields exactly

`<B,D>_F=4X`, `||B||_F^2=2(Y+L)`, `||D||_F^2=2(T+Y)`.

Consequently `16X^2<=4(Y+L)(T+Y)`, giving the required factor `1/4`:

`X^2 <= (Y+L)(T+Y)/4 <= T(T+L)/2 <= (T+L)^2/2`.

Nonnegativity of the matrix entries ensures `L,X>=0`, so taking the
nonnegative square root gives `X<=(T+L)/sqrt(2)`. No division by `T`, `L`,
`Y` or `T+L` occurs. The zero matrix is included.

The sixteen words in `tr((M+M^t)^4)` have trace classes with multiplicities
`2L,8X,4Y,2T`. The checker compares formal words modulo cyclic rotation
and transposition, rather than substituting a fixed matrix to justify
this dimension-independent identity. Thus

`tr(R^4)=2L+8X+4Y+2T`

`<=2L+6T+4sqrt(2)(T+L)<= (6+4sqrt(2))(T+L)`.

Inverting this positive constant gives

`2(T+L)>=(3-2sqrt(2))tr(R^4)`.

Entrywise nonnegativity is material. For example
`M=[[1,1],[-1,1]]` has `tr(M^4)=-8`; hence a proof relying on `L>=0`
cannot simply be extended to arbitrary real matrices.

## 4. Correct weighted transpose and C4 lower bound

Use `M_xy=sqrt(mu(x))K(x,y)sqrt(mu(y))`. Four factors cancel each square
root in pairs, giving the exact product-weight tuple sums, even when some
weights vanish. Its ordinary transpose represents the reversed kernel
`K^t`. For an off-diagonal reciprocal class, `R=M+M^t` represents the
symmetric union `S=K+K^t`, with no double counting of edges. Because `R`
is symmetric, `tr(R^4)=T(S)`.

The independent checker avoids square roots by using rational operators
`G=K diag(mu)` and `H=K^t diag(mu)`. It reconstructs weighted tensor sums
separately and checks every trace binding. The ordinary matrix transpose
of `G` is generally not `H`. A dedicated unequal-weight negative control
detects this exact implementation mistake. The rational implementation
also checks Gram products with the weighted kernel inner product
`sum_(x,y) mu(x)mu(y)U(x,y)V(x,y)`.
If an implementation instead places weights on the left and writes
`G=diag(mu)K`, the correct reversed-kernel representation is
`H=diag(mu)K^t`, again not the ordinary transpose `G^t`. Both rational
conventions have the same closed trace sums as the genuinely symmetric
square-root representation used in the written proof.

For any kernel of mean `r`, with its finite sums weighted by a probability
distribution, let `Q(a,c)=sum_b mu(b)S(a,b)S(c,b)`. Two Cauchy applications
give

`T(S)=E_(a,c)Q(a,c)^2 >= (E_(a,c)Q(a,c))^2`

`= [E_b(E_a S(a,b))^2]^2 >= (E_(a,b)S(a,b))^4=r^4`.

The expectations here are genuine finite probability averages. Zero
weights create no normalization problem. Together with the event count,
this proves the all-parameter six-mass inequality

`E_ell >= sum_i r_ii^4 + kappa sum_(i<j) r_ij^4`,

where `kappa=3-2sqrt(2)>0`.

## 5. Optimization and exact rational certificate

For positive coefficients `c_s`, set
`Z=sum_s c_s^(-1/3)` and `q_s=c_s^(-1/3)/Z`. Jensen for the fourth power
under the positive probability weights `q_s` gives

`1=(sum_s r_s)^4 <= sum_s q_s(r_s/q_s)^4 = Z^3 sum_s c_s r_s^4`.

With three coefficients one and three coefficients `kappa`, this is
exactly

`delta=1/[27(1+(3+2sqrt(2))^(1/3))^3]`.

This is an optimum of the auxiliary six-mass simplex functional. It is
not a claim that actual reciprocal kernels achieve those masses and all
the preceding equalities simultaneously.

The rational calculation is independently verified without decimal
rounding. Namely

`(177/250)^2-1/2=79/62500>0`,

`2/(6+8*177/250)=125/729`,

`(1031/729)^2-2=79/531441>0`.

The last equality implies `kappa>=125/729`. For coefficients
`c=(1,1,1,125/729,125/729,125/729)` and tangent point
`t=(5/42,5/42,5/42,3/14,3/14,3/14)`,

`sum t_s=1`, and every `c_s t_s^3=125/74088`.

The coefficient identity

`x^4-t^4-4t^3(x-t)=(x-t)^2(x^2+2xt+3t^2)`

is checked independently. Multiplying by `c_s`, summing, and using
`sum r_s=sum t_s` cancels the tangent terms. All remainders are
nonnegative, so the minimum is at least `125/74088`, with equality at
the displayed `t`. Monotonicity in each coefficient then gives
`delta>=125/74088`. The strict comparisons with `1/729` and the former
upper endpoint are exact rational comparisons, not floating-point tests.

## 6. Strict-window and original Kautz bridge

Given a strict code, the selected graph on ordered pairs has no walk of
three edges. Concatenating a three-edge walk would select occurrences at
starts `0,2,4` in an eight-letter word; repeated vertices and repeated
four-letter words still count. Thus maximum incoming walk length is
defined, belongs to `{0,1,2}`, and increases strictly along every selected
edge. This constructs a level function to which the arbitrary-level
theorem applies; no assumption that an optimal code is independent is
needed.

For any four-letter word, count its four rotation positions with
multiplicity. If at least two are selected, the periodic eight-letter word
has selected starts `0,j,4` after a cyclic shift, contradicting strictness.
This also rules out a selected word of period one or two: equal rotations
are separate positions. On `E_ell`, all four corresponding pair-level
comparisons are equalities, so all four positions are unselected. The
pointwise rotation inequality is therefore

`sum_(j=0..3) 1_C(rot_j(abcd)) <= 1-1_(E_ell)`.

Product weight is unchanged by rotation, for every probability vector.
Expectation proves `4p<=1-E_ell` and hence

`p <= (1-delta)/4 <= 73963/296352 < 182/729`.

The inspected inherited repair proof deletes repeated-letter words and
words in small original prefix/suffix fibers. Its loss is bounded by
`[3+2(7+13+15)]m^3=73m^3`. For each possible gap pair
`(1,1),(1,2),(1,3),(2,2)`, choosing the larger free side first requires
bad-extension coefficients respectively `(4,5),(9,6),(15,7),(9,13)`;
all are covered by the specified thresholds. Surviving endpoints have
strictly larger original fibers, so they can be replaced by injective
extensions around the retained middle word. The resulting three distinct
selected vertices lie on an actual shortest directed path, because all
letters in the extended word are distinct. This contradicts original GP.
It does not assume arbitrary original walks are geodesic.

Applying the strict bound with uniform weights to the repaired set gives
the integer bound

`gp(Ka(m,4)) <= floor(73963 m^4/296352)+73m^3`, `m>=3`.

The same argument permits the sharper real coefficient inside the floor.
Dividing by `m^4` makes the repair term vanish. The inspected density-limit
proof establishes existence using isometric subalphabet restrictions and
monotonicity of the four-distinct-letter extremal function normalized by
`(m)_4`. Thus the upper bound for `lambda_4` is valid. Appending the
previously reviewed weighted Jiggs endpoint gives the inherited lower
endpoint `beta<=lambda_4`; this review does not redetermine the fixed
57-word optimum or retranscribe the historical dictionary.

## 7. Actual execution and negative controls

Run from repository root:

```sh
python3 workstreams/GP2-20261012/stage3/trace_review/check_trace_independent.py
```

The final execution completed with exit code zero in 3.607201 seconds,
using Python 3.12.14. `run.log` stores actual stdout; `run_metadata.json`
records actual UTC timestamps, executable, command, return code, source
hashes, and log hash.

The checker covers:

* The exact sixteen-direction truth table and all four disjoint counts.
* All 81 binary level arrays under four rational weight vectors, including
  nonuniform weights and a zero weight; 93 further deterministic tests
  on alphabets of sizes one, three and four. Total: 417 level/weight cases.
* 2,654 exact matrix checks, including non-indicator rational kernels,
  weighted Gram bindings, direct tensor/trace comparisons, zero matrix,
  and directed-cycle witnesses.
* Formal degree-four trace-word coefficient identities and exact quartic
  tangent coefficient comparison. The finite-sum Cauchy square identity
  is also coefficient-checked for dimensions one through five; its
  arbitrary-dimension sum-of-squares argument is the written proof.
* Exhaustive examination of all 65,536 binary four-letter code subsets.
  Exactly 83 pass the strict occurrence constraint, represented by 455
  forbidden masks reconstructed from all binary eight-letter words. All
  83 are then checked against all eight-letter occurrence lists, canonical
  levels and the pointwise four-rotation inequality. Three weight vectors
  give 249 additional weighted rotation-bridge checks.
* The symbolic repair thresholds and total `73` loss coefficient.

Eight negative controls are actually exercised and rejected: damaged `8X`
trace coefficient; a larger `126/74088` mass lower bound; an arithmetic
upgrade of the derived matrix coefficient to `1/4`; ordinary transpose of
the rational weighted operator; omission of directed-cycle patterns;
replacing the matrix coefficient by `1` on an actual witness; replacing
occurrence counting by distinct-word counting; and decreasing repair
threshold `T_3` to `14`. The `1/4` arithmetic control checks the stated
derivation, not a claim that every conceivable stronger matrix lemma with
coefficient `1/4` is false.

The hash bindings are listed in `run_metadata.json` and `SHA256SUMS.json`.
No finite alphabet sample, numerical optimizer, or successful process exit
is used to establish universal scope. That scope follows from Sections
2–6 of this review and the accepted written candidate.
