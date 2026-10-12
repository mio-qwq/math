# Review of the weighted central-coefficient theta bound

## Scope and finding

The weighted central-coefficient argument is valid for every simple theta
graph whose three path lengths have mixed parity. It proves the strict
bound N(CB) < M(n) whenever n >= 5. The only simple theta on four vertices
is CB(1,2,2), with N=12=M(4). No full-parameter conclusion in this report
is inferred from finite enumeration.

This is an automated mathematical review and an independent implementation
of the graph definition; it is not human peer review. The current report
checks the explicit argument below. A subsequent audit of a particular
manuscript must additionally bind that manuscript's file hash.

Primary source:
[Braun--Bruegge, JIS 26 (2023), Article 23.7.2](https://cs.uwaterloo.ca/journals/JIS/VOL26/Braun/braun6.pdf).
Downloaded PDF SHA256:
`52e4b28b4e4106af07768940e60bb06fdd76f638b288e0139ec7bc5c05dd397a`.
The source's Theorem 5, Definition 12, Definition 20, Corollary 25, and
Theorem 27 were inspected. Definitions and the length-one clauses were
also checked on rendered PDF pages.

## 1. Graph domain and normalization

Write CB(x,y,z) for three internally disjoint paths between distinct
endpoints u and v. For a simple theta, x,y,z are positive integers and at
most one is 1. Then

    |V| = x+y+z-1 = n,       |E| = x+y+z = n+1.

Theorem 5 identifies facets with integer vertex labels f, modulo adding
one common constant, satisfying |f(a)-f(b)| <= 1 on each edge and having
a connected spanning subgraph of edges where equality holds. Set f(u)=0.
Opposite labelings are retained: opposite facets must both be counted.

Two paths of length 1 would name the same simple edge twice. The source's
Corollary 25(v), although useful for a formal repeated-path expression,
cannot be used to produce a simple theta with the asserted n+1 edges.

## 2. Independent derivation of the uniform mixed formula

Orient all three paths from u to v and record their edge increments in
{-1,0,1}. Call a zero increment an unsaturated edge. A saturated spanning
subgraph is connected if and only if both of the following hold:

1. Each path has at most one unsaturated edge.
2. At least one path has none.

Necessity of the first condition follows because two deleted edges on a
path isolate the intervening nonempty segment of internal vertices. The
second follows because a u-v path in a theta must be one of its three
original paths. For sufficiency, a path with no deleted edges connects u
and v. Every other path has at most one deletion, so each of its remaining
segments reaches u or v. Every vertex therefore lies in that connected
component. This includes a length-one path with its sole edge deleted.

Assume x and y have the same parity and z has the opposite parity. All
three oriented path sums equal t=f(v). A path with length l and h zero
increments has sum of parity l-h. Since h is either 0 or 1, there are
exactly two possible patterns:

| Path lengths | Zero counts | Choices of zero positions |
| --- | --- | --- |
| x,y,z | 0,0,1 | z |
| x,y,z | 1,1,0 | xy |

For a nonnegative integer m define

    B_m(t) = binom(m,(m+t)/2),

with value zero for wrong parity or an index outside [0,m]. In particular
B_0(t) is 1 at t=0 and zero otherwise. Define

    T(a,b,c) = sum over integer t of B_a(t) B_b(t) B_c(t).

The preceding classification gives exactly

    N(CB(x,y,z)) = z T(x,y,z-1) + xy T(x-1,y-1,z).       (1)

Each sign sequence with the specified common sum gives a unique normalized
vertex labeling, and the labeling recovers its edge increments, so this
count has no multiplicity. Formula (1) holds directly when one original
path has length 1. A remaining path length of 0 means the common endpoint
displacement is zero; this is precisely the B_0 convention. Thus the
formula agrees with Corollary 25(iii) and (iv), without introducing a
zero-length graph or a cycle of length 1.

## 3. Convolution and central coefficients

For a,b of the same parity,

    sum_t B_a(t) B_b(t) = binom(a+b,(a+b)/2).             (2)

To see this, replace t by 2j-a and use binomial symmetry on the second
factor; Vandermonde then applies with target (a+b)/2. This also covers
a=0 or b=0. There is no extra factor of 2: the sum includes precisely the
parity class on which both rows are nonzero.

For even m, the maximum coefficient in B_m is B_m(0). For odd m the two
equal maxima are B_m(1)=B_m(-1). The following ratios are exact:

    max B_x / B_(x-1)(0) = 2x/(x+1)                (x odd),
    max B_x / B_(x-2)(0) = 4(x-1)/x                (x even),
    max B_(x-1) / B_(x-2)(0) = 2(x-1)/x            (x even).

For both T terms in (1), after bounding the row involving x, the two
unbounded row lengths sum to the same even integer y+z-1:

    y+(z-1) = (y-1)+z.

This common convolution is the key compatibility check. Bounding the
two T terms separately by unrelated extremizers would not establish it.

## 4. Odd n

Here x,y are odd and z is even. Simplicity permits us to choose x>=3;
y>=1 and z>=2. Set

    A=B_(x-1)(0),       D=B_(y+z-1)(0).

Equations (1) and (2) give

    N <= [2xz/(x+1) + xy] AD
      = x[y+2z/(x+1)] AD
      < x(y+z) AD.                                    (3)

The strict inequality uses z>0 and x>1. Both x and y+z are odd and at
least 3, so the final expression is exactly

    N(C_x wedge C_(y+z)).

This wedge is a legitimate simple graph on n vertices and n+1 edges.
The source's Theorem 14 bounds its facet count by M(n). Thus N<M(n).

## 5. Even n, with one even path at least 4

Now x,y are even and z is odd. Choose x>=4, with y>=2 and z>=1. Set

    A=B_(x-2)(0),       D=B_(y+z-1)(0).

The same convolution yields

    N <= [4z(x-1)/x + 2y(x-1)] AD
      = 2(x-1)[y+2z/x] AD
      < 2(x-1)(y+z) AD.                               (4)

Both x-1 and y+z are odd and at least 3. Consequently the last expression
is exactly twice the facet count of the valid wedge
C_(x-1) wedge C_(y+z), whose order is n-1 and size is n. Theorem 14 and
the defining even-order relation M(n)=2M(n-1) imply N<M(n). In particular,
z=1 causes no loss of strictness.

## 6. Even n, both even paths equal 2

The remaining graph is CB(2,2,z), where z=2c+1 is odd. Put
A=binom(2c,c). The supported values in the T terms are t=0,+2,-2 and
t=+1,-1, respectively. Hence

    T(2,2,2c) = [4+2c/(c+1)] A,
    T(1,1,2c+1) = 2(2c+1) A/(c+1),

and

    N(CB(2,2,z)) = 6z(c+2) A/(c+1).                   (5)

For c>=1 this is strictly below 12zA, which is
2N(C_3 wedge C_z). The wedge has order n-1 because n=z+3, and both
cycles have length at least 3. The same comparison proves N<M(n).

For c=0 the graph is CB(1,2,2), the four-vertex diamond. Formula (5)
gives 12, also verified directly by normalized integer labels. The
numerical expression for M(4) is 12. The formal notation C_1 in
Definition 12's n=3 branch is not interpreted as a simple graph.

## 7. Consequence for the full bicyclic extremum

This mixed-parity argument combines with the published Theorems 14, 18,
and 27 as follows. Remove leaves from a connected simple graph with
n vertices and n+1 edges. Each removal multiplies its facet count by 2
when reversed. The resulting connected 2-core still has edge excess 1.
The degree excess sum over (degree-2) is 2. If its cycles are edge-disjoint,
Theorem 14 applies. Otherwise it is a theta: suppression of degree-two
vertices gives two degree-three vertices joined by three paths. A lone
degree-four vertex instead gives two edge-disjoint cycles; the alternate
two-degree-three configuration likewise has edge-disjoint cycles joined
by a path.

Same-parity theta cores satisfy Theorem 27, and mixed cores satisfy the
preceding argument. Theorem 18 iterates 2M(r)<=M(r+1) to restore the leaves.
The upper bound N(G)<=M(n) follows throughout the nonempty simple domain.
For n>=5 the graphs in Definition 12 are valid simple bicyclic graphs
attaining M(n). At n=4 the only five-edge simple graph is the diamond,
which attains M(4)=12. At n=3 no simple graph has n+1 edges, so a maximum
over that empty class is not asserted.

This establishes the mathematical implication to Conjecture 13 on its
nonempty simple-graph domain, conditional only on the cited published
same-parity and edge-disjoint results. It does not prove the stronger
four-family maximizer assertion of Conjecture 33 or classify every graph
attaining the full bicyclic bound.

## 8. Independent actual-graph verification

Run from the repository root:

```bash
python workstreams/STRUCT2-20261012/theta/independent/check_actual_facets.py
```

For each actual graph, the checker chooses a spanning tree, assigns its
edge increments independently from {-1,0,1}, and fixes vertex 0 to label
0. This parametrizes every normalized labeling satisfying the tree-edge
Lipschitz conditions, exactly once. All graph edges and the full saturated
subgraph are then checked. The counting method therefore implements
Theorem 5 independently of the formula being compared.

The recorded execution covers 19 theta graphs on 4 through 10 vertices,
including both mixed cases, every simple length-one clause, and four
same-parity controls. All exact counts match the separately transcribed
Corollary 25. Three cases were recomputed using genuinely different
spanning-tree edge sets; the SHA256 of the complete sorted normalized
facet-label sets agrees. Controls reject duplicate length-one paths,
nonpositive lengths, constant labels with disconnected saturated edges,
and an edge-label jump of 2. Counts for one tree and cycles of lengths
3, 4, and 5 provide additional normalization checks.

`actual_facet_checks.json` contains the actual graphs, counts, spanning
trees, label-set hashes, source hash, and checker hash.
`actual_facet_checks.log` is captured output from the recorded execution.
These finite checks support the definition/formula correspondence; the
full-parameter conclusion rests on Sections 2 through 7 above.
