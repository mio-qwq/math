# Independent mathematical review of the exact theta maximizers

Review date: 2026-10-12.

## 1. Bound object and conclusion

The complete manuscript reviewed is `../MAXIMIZERS.md`, 14079 bytes,
SHA256 `c0c02847ae525260d65dd5b11c1ee940b4b63aec6e2167c39fa8a9c12fc12fab`.
The graph-label semantics and centered-binomial definitions were also checked
against Sections 1 and 2 of `../PROOF.md`, 15452 bytes, SHA256
`81f7c5f4326828b16a34204e1a84b3dec136ea1d61c30cfb60b17e6395616655`.
The present review does not automatically review all other claims in that
earlier manuscript.

**Conclusion:** the reviewed exact-maximizer theorem is mathematically
supported for every nonempty simple theta order n>=4. Both compression
inequalities, the strict balancing comparisons, the exclusion of both
same-parity classes, and the unique unordered length triple are valid.
All four exact values and all four ratios in Section 8 are correct. No
mathematical revision of the bound manuscript was required by this review.

The source's Conjecture 33 asks for the listed maximizers for n>=10.
The extension to n>=4 and uniqueness follow from the strict inequalities;
they are not assumptions imported from that conjecture. The source is
Braun--Bruegge, *Facets of Symmetric Edge Polytopes for Graphs with Few
Edges*, JIS 26 (2023), Article 23.7.2, printed p. 24:
<https://cs.uwaterloo.ca/journals/JIS/VOL26/Braun/braun6.pdf>.

This is an independently reconstructed AI mathematical review, not human
peer review or a Lean certificate. Finite execution and literature scope
are recorded separately below. The conclusion is bound to the bytes above.

## 2. Reconstruction from the graph and facet definitions

For three paths with positive lengths a,b,c and common distinct endpoints,
the condition that at most one length equals 1 is precisely what prevents
duplicating a simple edge. With disjoint internal vertices, the graph then
has a+b+c edges and a+b+c-1 vertices. Its internal vertices all have degree
two. The smallest possible length sum is 5, so n>=4.

For completeness, the usual facet-label criterion can itself be checked
through polarity. The signed edge vectors of a connected graph span the
(n-1)-dimensional space of vectors whose coordinate sum is zero. In the
dual quotient, fix one vertex label to zero. The polar inequalities are
|f(u)-f(v)|<=1 for every edge. A feasible point is a polar vertex exactly
when its active edge forms have rank n-1, which is equivalent to their
graph being connected and spanning. An active spanning tree makes all
labels integers, since its differences are ±1. Thus facets correspond
exactly to the normalized integer labels satisfying the edge inequalities
and active-edge connectedness. Opposite labels give different facets.
This is the prior characterization stated as Theorem 5 in the source.

Orient the three paths in the same endpoint direction. A path with two
zero increments leaves a nonempty internal segment disconnected from both
endpoints in the active graph. Hence each path has at most one zero
increment. At least one path has none, because otherwise the two common
endpoints are disconnected. Conversely these two conditions make every
internal segment attach to endpoints connected by an intact path, and
therefore suffice for active-edge connectedness.

Let B_m(t)=binom(m,(m+t)/2) when its lower index is an integer in [0,m],
and zero otherwise, including B_0(t)=1[t=0]. This counts the ±1 words of
length m with endpoint sum t. For common-parity lengths, parity and the
preceding zero restrictions force all paths to have no zero, giving

\[
N(a,b,c)=T(a,b,c)=\sum_t B_a(t)B_b(t)B_c(t).
\]

For mixed parity, let x,y have the same parity and z have the opposite
parity. For one parity of t only z has a zero; for the other parity just
x and y have a zero. Choosing the zero positions gives exactly

\[
N(x,y,z)=zT(x,y,z-1)+xyT(x-1,y-1,z).
\tag{R1}
\]

There are no further allowed patterns. Deleting a zero is a count of sign
words, not a declaration of a graph path of length zero. In particular,
when x=1 the row B_0 imposes t=0, and when z=1 the same convention gives
the original single-edge boundary term. Equation (R1) agrees with the
original Corollary 25(ii)--(iv), with the required length coefficients.

## 3. Scalar ingredients and the two boundary formulas

Vandermonde, with reflection of the second lower index, gives

\[
\sum_t B_p(t)B_q(t)=B_{p+q}(0)
\]

for same-parity nonnegative p,q. Consequently
T(a,b,c)<=max B_a times B_{b+c}(0) when the three rows have common parity.
The zero-row boundary cases satisfy the same identity.

For b_j=binom(2j,j), the exact ratio rho_j=4-2/(j+1) is positive and
strictly increasing. Hence

\[
\frac{b_u b_v}{b_{u+v}}\le\frac{u+1}{2u+1}
\quad(u\ge0,\ v\ge1),
\qquad
b_r b_s\le2b_{r+s-1}\quad(r,s\ge1).
\tag{R2}
\]

For the first statement the quotient's next-v ratio is
rho_v/rho_{u+v}<=1; evaluate at v=1. For the second, fix s and increase r;
the next-r ratio is rho_r/rho_{r+s-1}<=1, and the starting value at r=1
is 2. The manuscript uses this valid two-variable inequality, not an
incorrect global monotonicity claim along a fixed-sum interval.

The ratio in the first statement is constant when u=0. In particular,
the later E/D estimate has equality for y=1 at any z, not only at z=2.
The proof does not require strictness there; its separate scalar
comparison supplies strictness when z>2.

Direct substitution in (R1) verifies the short-path identities

\[
N(p,q,1)=\frac{pq+2}{2}B_p(0)B_q(0)
\quad(p,q\ge2\text{ even}),
\tag{R3}
\]

\[
N(x,y,2)=\frac{xy+5}{4}B_{x+1}(0)B_{y+1}(0)
\quad(x,y\ge1\text{ odd, at most one equal to }1).
\tag{R4}
\]

For (R3), the B_0 term contributes B_p(0)B_q(0), and the two t=±1
terms contribute pq B_p(0)B_q(0)/2. For (R4), put
A_x=B_{x-1}(0), r_x=(x-1)/(x+1), and similarly for y. The two summands
in (R1) are

\[
4B_x(1)B_y(1),\qquad 2xyA_xA_y(1+r_xr_y).
\]

Their sum is 4xy(xy+5)A_xA_y/((x+1)(y+1)), while
B_{x+1}(0)=4xA_x/(x+1). This proves (R4), including x=1 or y=1.
These are specializations of prior facet-count formulas, not additional
new counting theorems asserted by the review.

## 4. Compression and all strictness conditions

### Even n

For even x,y>=2 and odd z>=1, the peak values of B_x and B_{x-1} are
B_x(0) and B_x(0)/2. Put D=B_{y+z-1}(0)>0. Applying the same
Vandermonde convolution to both terms of (R1) gives

\[
N(x,y,z)\le B_x(0)D\left(z+\frac{xy}{2}\right).
\]

The target N(x,y+z-1,1), calculated by (R3), is larger than the
displayed bound by

\[
B_x(0)D\,\frac{(z-1)(x-2)}2.
\]

The new second length is a positive even integer, so simplicity and the
total length are preserved. If x>2 and z>1, the displayed difference is
positive. If x=2 and z>1, then z>=3; at t=2,
B_y(2)B_{z-1}(2)>0 whereas B_2(2)=1<B_2(0)=2. The first summand of
(R1) therefore had a strict peak inequality already. This verifies
strict compression for every z>1, including x=y=2. At z=1 the target
is the original graph.

### Odd n

Here x,y are odd and z>=2 is even. Since x=y=1 is excluded by
simplicity, the two odd paths can be named so that x>=3. Put

\[
A=B_{x-1}(0),\quad D=B_{y+z-1}(0),\quad
E=B_{y-1}(0)B_z(0),\quad r=\frac{x-1}{x+1}.
\]

For every even t, B_{x-1}(t)<=rA+(1-r)A 1[t=0]. This bound is exact
at zero and at the nearest nonzero positions ±2. For odd t, the peak
of B_x is 2xA/(x+1). These give, jointly rather than term by term with
unrelated envelopes,

\[
N(x,y,z)\le\frac{xA}{x+1}
 \left((2z+y(x-1))D+2yE\right).
\]

Use (R2) with u=(y-1)/2 and v=z/2. It gives E/D<=(y+1)/(2y), also
when y=1. Consequently

\[
N(x,y,z)\le\frac{xAD}{x+1}(xy+2z+1).
\]

With y'=y+z-2, (R4) gives N(x,y',2)=xAD(xy'+5)/(x+1). The scalar
difference is exactly (x-2)(z-2). Positivity of x-2, A and D proves
strict compression whenever z>2. The new y' is positive and odd;
x>=3 ensures at most one length 1 remains. At z=2 the comparison is
the identity. This closes the possible small-path loophole in the odd
case without any unproved strictness assertion about E/D.

## 5. Strict balancing and uniqueness

For even u>=v+4 and v>=2, write

\[
d=u-v-2>0,\quad P=uv,\quad S=u+v,\quad
U=u(v+1),\quad V=(u-1)(v+2)=U+d.
\]

Under (u,v)->(u-2,v+2), the product P increases by 2d while the
central-binomial product is multiplied by U/V. Both denominators are
positive. The differences after cross multiplication are

\[
U(P+2d+2)-V(P+2)=d(uv+2u-2)>0
\]

for (R3), and

\[
U(P+2d-S+6)-V(P-S+6)=d(uv+3u+v-6)>0
\]

for (R4), where x=u-1 and y=v-1. The latter transfer gives positive
odd lengths at least 3, so even a starting length y=1 causes no domain
problem. Repeated transfers leave a pair differing by zero or two,
uniquely as an unordered even pair. A gap of two would merely exchange
the pair, not produce a second unordered maximizer.

The strict compressions first force z=1 at even n, or z=2 at odd n.
The strict pair transfers then force exactly the four triples in the
theorem. To conclude over all triples, the same-parity exclusion below
is essential; it is present in the manuscript.

## 6. Same-parity exclusion and small orders

For all-even lengths with sum 2k, k>=3, the row-peak bound and (R2)
give

\[
N(a,b,c)\le b_{a/2}b_{(b+c)/2}\le2b_{k-1}.
\]

The legal mixed triple (1,2k-3,2) has (k+1)b_{k-1} facets by (R4),
strictly more; its second odd length is at least 3.

For all-odd lengths, put c=2u+1 and a+b=2v, so u>=0, v>=1 and
u+v=k. Then

\[
N(a,b,c)\le\frac{2u+1}{u+1}b_u b_v\le b_k.
\]

The legal mixed triple (2,2k-2,1) has k b_k facets by (R3), strictly
more for k>=2. At n=4 no all-odd simple theta exists, which does not
affect the argument. At n=5 the all-even graph does exist and is
strictly excluded. Thus there is no unhandled small-order parity class.

These exclusions plus strict compression and balancing establish
uniqueness among all admissible unordered triples. The degree-three
vertices are exactly the common endpoints, so a graph isomorphism also
preserves the multiset of lengths of the maximal intervening paths.
There is consequently no hidden distinction between unordered length
uniqueness and ordinary isomorphism of simple theta maximizers.

## 7. Independent algebra check of Section 8

The four H values follow by substituting the four balanced pairs into
(R3)--(R4). For even k, with C=binom(k,k/2), the original M values reduce
to M(2k-1)=k(k+1)C^2/4 and M(2k)=k(k+1)C^2/2. For odd k, with
C=binom(k-1,(k-1)/2), they are k^2 C^2 and 2k^2 C^2.
Division gives precisely the manuscript's numerators:

| Order | k parity | Numerator of H/M with denominator k(k+1) | Denominator minus numerator |
| --- | --- | --- | --- |
| 2k-1 | even | k^2-2k+6 | 3k-6 |
| 2k-1 | odd | k^2-2k+5 | 3k-5 |
| 2k | even | k^2+2 | k-2 |
| 2k | odd | k^2+1 | k-1 |

The last column is positive in every n>=5 domain: the even-k cases
have k>=4 and the odd-k cases have k>=3. At n=4 the even-order,
even-k formula gives H(4)=12. This is a statement about the actual
graph Theta(2,2,1), without assigning a graph meaning to C1.
Each ratio tends to one along its specified subsequence, as claimed.

The even-order formulas agree with the corrected original Proposition 30
ratios in `../literature/PROPOSITION30_CORRECTION.md`. The exact theta
maximization itself is a further claim; it does not follow merely from
that proposition's bound on two selected graphs.

## 8. Finite execution and limited overlap check

`check_small_maximizers.py` independently constructs each simple theta
for 4<=n<=8 and enumerates all increments in {-1,0,1} along a fixed
spanning tree. It tests the remaining edge inequalities and active-edge
connectedness directly. It does not call T or import a discovery
program. Binomial expressions enter only after the direct count, for
comparison with the stated H values.

The actual Python 3.12.14 run on 2026-10-12 at 09:11 UTC exited with
status 0 and checked 16 unordered triples. The unique maximizer counts
at n=4,5,6,7,8 were respectively 12,24,60,126,324. The saved output
also witnesses the x=2 strict-compression case, the y=1 strict-compression
case, both boundary balancing cases, and both same-parity exclusions.
Disconnected active-edge assignments are explicitly rejected, and the
duplicate-length-one construction is a failing-domain control. These
are finite regressions; none is an assumption in the universal argument.
`run_evidence.json` and `small_maximizers.json` preserve the real run and
hashes.

The earlier source gate remains `../literature/SOURCE_GATE.md`. An
additional targeted search pass on 2026-10-12 used the queries
`"Braun" "Bruegge" "Conjecture 33" theta facets`,
`"symmetric edge polytopes" "theta" "path" "maximized"`,
`"symmetric edge polytopes" "Vandermonde" facets compression`,
`"Facets of symmetric edge polytopes for graphs with few edges" "Conjecture 33"`,
and `"theta" "symmetric edge polytopes" compression balancing`.
The returned material did not identify an equivalent compression and
balancing proof. Relevant returned sources remained the original article,
the previously inspected IPAM 2025 slides, and adjacent symmetric-edge
polytope literature. This modest additional search does not establish
historical priority or certify that every public later result has been
excluded. In particular, the previously recorded publisher full-text
access limitation for the Mori--Mori--Ohsugi journal article remains.

No Lean compilation was run for this review, and no full Lean theorem
is asserted.
