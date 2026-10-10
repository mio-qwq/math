# An exact general-position formula for consecutive-generator circulant digraphs

Researcher B — proof candidate, 10 October 2026 UTC.
Classification: **proof of an original conjecture, not a counterexample**.
Historical novelty remains subject to literature review. This is not a submission or a priority claim.

## 1. Original question and definitions

Ullas Chandran S.V., Gabriele Di Stefano, Grahame Erskine, Haritha S,
Elias John Thomas, and James Tuite, *The general position number of digraphs*,
arXiv:2604.15909v1 (17 April 2026), Section 3.1, make an unnumbered
optimality conjecture immediately after Theorem 3.3.

Primary source: https://arxiv.org/html/2604.15909v1#S3.SS1
Version record: https://arxiv.org/abs/2604.15909

For integers 1 <= d < n, let D(n,d) have vertices 0,...,n-1 and arcs
x -> x+j modulo n for every 1 <= j <= d. A set S is in general position
if no shortest directed path between two of its distinct vertices contains
a third vertex of S. Distances are directed; the two directions are checked
separately. These digraphs are strongly connected because generator 1 is present.

The source constructs consecutive vertices and an arithmetic progression,
and conjectures that the larger construction is optimal (reporting tests
for n <= 50 and d <= 15). The result below establishes the matching upper
bound, with small/residue boundary cases included.

## 2. The formula

Write n = q*d + r uniquely with 2 <= r <= d+1 and integer q >= 0.
Then

- if r = d+1, gp(D(n,d)) = d+1;
- if 2 <= r <= d, gp(D(n,d)) = max(r, floor(d/r)+1).

The second expression equals max(r, ceil((d+1)/r)).
For d=1 only the first case occurs and gp(D(n,1))=2.
When q=0, the constraints d<n force n=d+1, so the first case includes
the complete digraph.

We give a self-contained proof. No numerical search or finite upper
cutoff is an assumption.

## 3. Directed distance and equality test

For distinct vertices u,v, put t=(v-u) mod n in {1,...,n-1}. Then

    dist(u,v) = ceil(t/d).

Indeed, a directed walk of length L has an integer sum of increments
between L and L*d, congruent to t modulo n. That positive sum is at
least t, so L >= ceil(t/d). Conversely, use floor(t/d) increments d and,
if necessary, one increment t mod d. This gives the asserted length.

For distinct vertices u,v,w, a shortest u,w path through v exists exactly
when dist(u,w)=dist(u,v)+dist(v,w). The forward implication is immediate.
For the reverse, concatenate shortest paths: its length equals dist(u,w),
so it cannot contain a repeated vertex (which would allow shortening).

For positive integers A,B, write their ordinary residues modulo d as
alpha,beta in {0,...,d-1}. Then

    ceil(A/d)+ceil(B/d) > ceil((A+B)/d)

holds exactly when alpha>0, beta>0 and alpha+beta<=d.
This follows by expanding A and B into quotient plus remainder. Otherwise
the two sides are equal. We will use this only for positive gaps with
A+B<n, so A+B is the actual forward displacement, not an extra turn.

## 4. Residue-order restriction

Translate any general-position set S to contain 0, and sort it as

    0=x_0 < x_1 < ... < x_(k-1) < n.

For i>=1 write x_i = b_i*d + t_i with 1<=t_i<=d;
thus t_i=d represents residue zero and b_i=floor((x_i-1)/d).
Set t_0=b_0=0.

For 0<i<j, the triple (0,x_i,x_j) must not be geodesic through x_i.
If t_i>=t_j, direct ceiling expansion gives

    ceil(x_i/d)+ceil((x_j-x_i)/d) = ceil(x_j/d),

which contradicts general position. Consequently

    0=t_0 < t_1 < ... < t_(k-1) <= d.

In particular k<=d+1 for every n,d. This proof also covers k<=2,
when the ordering condition is vacuous.

For additional clarity, compression x_i -> t_i preserves general
position: for any distinct i,j,

    dist_D(x_i,x_j) = dist_D(t_i,t_j) + b_j-b_i.

For i<j this follows from strict residue order. For i>j include n in
both forward displacements. The vertex-dependent terms cancel in every
three-vertex additivity test. This compression observation is useful but
is not needed as an extra assumption in the bound below.

## 5. The stronger bound when 2<=r<=d

Suppose first k>=3. For each anchored triple 0<x_i<x_j, its three positive
cyclic gaps are

    A=x_i, B=x_j-x_i, C=n-x_j.

None of the three clockwise two-gap paths may be geodesic. Applying the
ceiling test to (A,B), (B,C), (C,A), each individual ordinary gap residue
must be positive and each pair of these residues must have sum at most d.

Let t=t_i and s=t_j, so 0<t<s<=d. Their first two gap residues are
exactly t and s-t. We divide according to s relative to r.

- If s<r, no additional bound is needed.
- If s=r, the residue of C is zero (also when r=s=d).
  This is impossible for a general-position triple.
- If s>r, necessarily r<d, and C has ordinary residue c=d+r-s,
  which is in {1,...,d-1}. The two pair-sum inequalities give

      t+c<=d       => s-t>=r,
      (s-t)+c<=d   => t>=r.

Let M=t_(k-1). If M<r, all k distinct compressed vertices lie in
{0,...,r-1}, so k<=r. If M=r, an anchored triple with an interior
vertex is impossible; therefore this case cannot occur for k>=3.
If M>r, the triple involving t_1 and M gives t_1>=r. For every j>=2,
t_j>r, so the triple involving t_(j-1),t_j gives

    t_j-t_(j-1) >= r.

Thus M >= (k-1)*r. Since M<=d,

    k <= floor(d/r)+1.

If k<=2, the same stated bound holds because r>=2. This proves

    gp(D(n,d)) <= max(r, floor(d/r)+1).

## 6. Attaining the bounds

For 2<=r<=d, the set {0,...,r-1} has size r. Every increasing triple
has forward adjacent gaps u,v with u+v<r; the third cyclic gap has
ordinary residue r-u-v (when r=d this is still positive). All three
residues are positive and any pair sum is <=d, so none of the three
clockwise orders is geodesic.

The arithmetic-progression set {0,r,2r,...,floor(d/r)*r} has size
floor(d/r)+1. For each increasing triple its adjacent gaps u,v are
at least r and its span s=u+v<=d. If a triple exists then r<d and
s>=2r, so the third cyclic-gap residue is c=d+r-s>0. Hence

    u+v<=d, u+c=d+r-v<=d, v+c=d+r-u<=d.

Again no clockwise order is geodesic.

The other three possible orders of a triple cannot be geodesic in
either construction: their two forward displacements add to n plus
the direct forward displacement. Since n>d, the sum of their two
ceilings is strictly greater than the ceiling for that direct displacement.
This also explains why checking the three cyclic orders suffices.

If a displayed set has at most two vertices, the general-position
condition is automatic. The two constructions therefore prove the
matching lower bound without omitted small cases.

Finally take r=d+1, so n=q*d+d+1, and use S={0,...,d}.
For an increasing triple, both forward distances are 1 and each reverse
distance is q+1. None of the six additivity equalities is possible:
the relevant comparisons are 1 versus 2, q+1 versus q+2,
and 1 versus 2(q+1). Thus S is in general position. The residue-order
bound k<=d+1 proves equality. For d=1 there are no triples in this set,
and the same upper bound proves gp=2.

This proves the formula for all 1<=d<n. QED.

## 7. Scope and verification status

This is a full written proof of the source's circulant optimality conjecture,
not a result about all directed graphs, other circulant generator sets,
Kautz digraphs, or packing coloring. Computational tests are consistency
checks only. No Lean compilation or formalization is claimed. Independent
review and executable checks are recorded separately, tied to a frozen
source hash. Human responsibility review and historical originality remain
unconfirmed. No author has been contacted and no paper submitted.
