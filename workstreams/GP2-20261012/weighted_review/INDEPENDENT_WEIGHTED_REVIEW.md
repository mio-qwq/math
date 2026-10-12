# Independent exact review of the weighted Jiggs 57-word lift

Date: 2026-10-12. **Verdict: PASS for the exact algebra and counting claims
reviewed below, with the numerical-display correction recorded in revision 2.**

The reviewer did not participate in discovering the proposed weights or the
sum-of-squares identity. All algebra was reconstructed from the literal
57-word file, using a new Python standard-library checker. No discovery
program, graph-distance checker, floating-point optimizer, symbolic-algebra
package, or historical assertion of maximality was imported.

## 1. Exact inputs and acceptance boundary

| Input | SHA256 |
| --- | --- |
| `../literature_lifts/jiggs57_words.txt` | `26d405621e125016c26edf662bd1d18cb721bb6b09976c421fa5093e531a1f14` |
| `../literature_lifts/JIGGS57_WEIGHTED_LIFT_V2.md` | `6f1068bd29261ac4eea4cfc11b9392593900580498d087f3f7856cf04d334918` |

The final review binds revision 2, specifically its Sections 3–5 and the
exact lift counts in Section 2. The full literal dictionary is the classical
dictionary attributed in the candidate to B. H. Jiggs (1963), page 184. This
review checks the supplied words; it does not independently repeat the
visual transcription from the printed source or certify historical priority.

The strict-window property and the original directed Kautz GP bridge have a
separate construction review in
`../construction/JIGGS57_INDEPENDENT_REVIEW.md`. This algebra review does
not repeat its exhaustive eight-window checks or original-adjacency BFS.
The implication to a GP lower bound below uses that separate bridge.
The upper bound `182/729` and existence of the density limit are inherited
from the existing project proofs, not newly certified here.

### Numerical-display correction found during review

Revision 1, `JIGGS57_WEIGHTED_LIFT.md`, has SHA256
`069a2aad0a9bf45796ad97f549c0bfa282dce0d0a4a3b1114f74f47b5dfdde23`.
Its displayed root `0.18673085336460038...` is not the root of the stated
cubic to the displayed precision. The exact cubic, quartic, compression
identity and lower-bound formulas in that revision are correct. Revision 2
preserves those claims, fixes the decimal display, and adds the independently
verified reduced expression for the maximum. The rational intervals in
Section 4 below certify the corrected digits. Revision 1 remains preserved;
the source was not silently overwritten.

## 2. Primitive rotation orbits and the exact density

Let `D` be the supplied dictionary and let

\[
F(a,b,c,d)=\sum_{w\in D}\prod_{i=0}^3p_{w_i},
\qquad (p_A,p_B,p_C,p_D)=(a,b,c,d).
\]

Every nonprimitive length-four word has period dividing two and is of the
form `XYXY`. There are exactly 16 such words among the 256 words over four
letters. The remaining 240 words have four distinct cyclic rotations and
therefore form 60 primitive rotation orbits.

Independent enumeration of all 256 words confirms that every dictionary
word is primitive, its 57 canonical rotation representatives are distinct,
and the missing representatives are exactly

\[
\boxed{\mathrm{ADCB},\quad\mathrm{ADCD},\quad\mathrm{BCDC}.}
\]

Rotation preserves product weight. The sum of the weights of the 16
nonprimitive words is
`(a^2+b^2+c^2+d^2)^2`, while the sum over all words is
`(a+b+c+d)^4`. Consequently the following is a homogeneous polynomial
identity, without any normalization hypothesis:

\[
F=\frac{(a+b+c+d)^4-(a^2+b^2+c^2+d^2)^2}{4}
-abcd-acd^2-bc^2d.
\tag{1}
\]

On the simplex `a+b+c+d=1`, (1) is exactly the claimed expression with
constant numerator term 1. The checker constructs the 31 nonzero monomial
coefficients by summing the 57 literal products and compares every
coefficient with both the orbit construction and (1). All residual
coefficients vanish. The coefficient sum is 57.

## 3. Exact compression and its equality case

Set

\[
u=a+b,\quad v=c+d,\quad r=a-b,\quad s=c-d.
\]

Substituting
`a=(u+r)/2`, `b=(u-r)/2`, `c=(v+s)/2`, `d=(v-s)/2` into the literal-word
polynomial gives the following identity:

\[
\begin{aligned}
16\bigl(F(u/2,u/2,v/2,v/2)-F(a,b,c,d)\bigr)
={}&2(ur)^2+((u-v)s)^2+(v(r-s))^2\\
&+(r^2)^2+2(rs)^2+(rs+s^2)^2.
\end{aligned}
\tag{2}
\]

The checker compares the complete coefficient maps. In the variable order
`u,v,r,s`, the expanded right side has precisely ten nonzero terms:

\[
2u^2r^2+u^2s^2-2uvs^2+v^2r^2-2v^2rs+2v^2s^2
+r^4+3r^2s^2+2rs^3+s^4.
\]

In particular, the cross term is **`+2rs^3`**. Reversing that sign fails
the exact check. Identity (2) is valid even before imposing `u+v=1`.

Every multiplier of a square is positive. On the simplex the compressed
vector remains feasible, since `u,v>=0` and `u+v=1`. Its density cannot
decrease. Equality in (2) implies `r=0` from the term `r^4`, and then
`s=0` from `(rs+s^2)^2=s^4`. Thus every maximizer satisfies

\[
a=b=x,\qquad c=d=y,\qquad x+y=\tfrac12.
\]

This equality argument includes the boundary of the simplex.

## 4. Unique fixed-template optimum and rational certification

Substituting `(a,b,c,d)=(1/2-y,1/2-y,y,y)` in the literal polynomial gives

\[
f(y)=\frac3{16}+\frac y2-\frac94y^2+4y^3-3y^4,
\qquad 0\le y\le\tfrac12.
\]

Let

\[
P(y)=24y^3-24y^2+9y-1.
\]

Exact coefficient comparisons establish

\[
f'(y)=-\frac12P(y),\qquad
P'(y)=72(y-\tfrac13)^2+1>0.
\]

Also `P(0)=-1` and `P(1/2)=1/2`. By continuity and strict monotonicity,
`P` has a unique root `rho` in `(0,1/2)`, and `f` increases up to that root
and decreases after it. Together with (2), this proves the unique global
maximizer of this fixed four-variable polynomial is

\[
(a,b,c,d)=(\tfrac12-\rho,\tfrac12-\rho,\rho,\rho).
\]

There is a convenient exact reduction for its value. Direct coefficient
comparison gives

\[
f(y)-\left(\frac{11}{48}-\frac{y^2}{8}\right)
=\left(\frac1{24}-\frac y8\right)P(y).
\tag{3}
\]

Thus

\[
\boxed{\beta=\max_{a,b,c,d\ge0,\ a+b+c+d=1}F(a,b,c,d)
=f(\rho)=\frac{11}{48}-\frac{\rho^2}{8}.}
\]

The following strict bounds use finite decimals as **exact rationals**:

\[
\begin{aligned}
0.186730853364600134432293139877952573
&<\rho\\
&<0.186730853364600134432293139877952574,
\end{aligned}
\]

\[
\begin{aligned}
0.22480811521688269199843581722429
&<\beta\\
&<0.22480811521688269199843581722430.
\end{aligned}
\]

For the first interval, the checker evaluates `P` exactly at both rational
endpoints and obtains strictly negative and strictly positive values.
The already proved positivity of `P'` certifies uniqueness. For the second
interval, `11/48-y^2/8` is strictly decreasing for positive `y`, so its values
at the two root endpoints give an exact enclosing interval. Both displayed
beta endpoints are verified to lie strictly outside that enclosing interval.
No floating-point sign test or approximate root finder is used.

## 5. Exact integer lift and its asymptotic consequence

For block sizes `n_A,n_B,n_C,n_D`, fixing a template `w` gives exactly

\[
n_{w_0}\prod_{i=1}^3
\left(n_{w_i}-\mathbf1_{w_i=w_{i-1}}\right)
\tag{4}
\]

valid original words. If adjacent block names differ, the actual letters
already differ. If the names agree, precisely the immediately previous
letter is excluded. Nonadjacent repetitions remain allowed. Different
templates give disjoint sets of actual words, so (4) is summed over the
literal 57 ordered words.

Substitute `(n_A,n_B,n_C,n_D)=(5q,5q,3q,3q)`. The checker independently
multiplies all 57 four-factor products. Its coefficient vector in ascending
powers `q^0,...,q^4` is

\[
\boxed{(0,0,94,-2528,14733).}
\]

Hence the separately certified GP lift has size

\[
14733q^4-2528q^3+94q^2\qquad(q\ge1),
\]

on an alphabet of size `16q`. Its leading coefficient normalized by
`(16q)^4` is exactly

\[
\frac{14733}{65536}
=F(5/16,5/16,3/16,3/16)
=f(3/16)
=0.2248077392578125.
\]

The certified rational beta bounds also prove, without rounding,

\[
0<\beta-\frac{14733}{65536}<\frac1{2500000}=4\cdot10^{-7}.
\]

As a further exact count check, uniform block weights give the histogram
`{0:23,1:28,2:6}` for the number of equal adjacent block pairs, and therefore

\[
23q^4+28q^3(q-1)+6q^2(q-1)^2=57q^4-40q^3+6q^2.
\]

For every large integer `m`, choose integer block sizes with sum `m` whose
ratios tend to the optimal vector. For example, round down the first three
optimal block sizes and assign the remaining letters to the fourth block.
Each error is bounded independently of `m`. Formula (4) then has total size
`beta*m^4+O(m^3)`: its degree-four part is the literal product polynomial,
and every adjacency correction has lower degree. The separate GP bridge
therefore yields the asymptotic lower bound `lambda_4>=beta`. This step
works along all sufficiently large alphabet sizes, not only multiples of 16.

This proves the optimum of the **fixed 57-word template under four block
weights**. It does not optimize over other dictionaries, a variable number
of blocks, all strict codes, or all original GP sets. It does not prove any
new upper bound. In particular, combining this result with an independently
proved upper bound requires retaining the scope of that upper-bound proof.

## 6. Actual verification, negative controls, and replay

The supplied checker uses only Python standard-library modules, integer
arithmetic, and `fractions.Fraction`. Its sparse polynomial operations
recompute the claimed identities from the literal dictionary. The JSON
certificate stores the full primitive-orbit data, all density and
compression coefficients, the six square factors, both rational isolating
intervals, and each of the 57 exact integer lift polynomials.

The actual replay log is `weighted_check.log`. The command exits with code
0 and ends with `RESULT: PASS`:

```bash
python workstreams/GP2-20261012/weighted_review/verify_weighted_jiggs57.py --negative-controls
```

Default input paths are resolved relative to the checker, so the absolute
checker path can also be run from any working directory. The checker pins
both the exact dictionary bytes and revision 2 of the reviewed statement.

All nine deliberate corruptions were actually rejected:

1. Rotating the first word while retaining the certificate.
2. The same rotation while forging a replacement dictionary hash in the certificate.
3. Permuting block weights while preserving their multiset and sum.
4. Incrementing a density coefficient.
5. Changing the exact lift's `q^2` coefficient from 94 to 95.
6. Changing `(rs+s^2)^2` to `(rs-s^2)^2`.
7. Changing the critical cubic's linear coefficient from 9 to 8.
8. Placing a narrow root interval at the obsolete erroneous decimal.
9. Corrupting the constant in the reduced beta polynomial.

The first control is stronger than a product-density check alone: rotating
a word preserves its leading product monomial but can change its adjacent
repetition pattern and finite lift count. The immutable literal-word pin
therefore binds information the weighted density alone does not retain.

`weighted_provenance.json` records the actual replay command, exit code,
scope, input bindings and artifact hashes. `SHA256SUMS` supplies a directly
replayable digest list. This package is a written all-parameter algebra
proof plus exact computational certificates. It is not a Lean formalization,
an external human peer review, a historical-maximality certificate, or a
global solution of the original GP extremal problem.
