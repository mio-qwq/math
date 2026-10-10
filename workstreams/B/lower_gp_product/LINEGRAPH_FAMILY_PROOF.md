# The lower-GP product conjecture for line graphs of complete graphs

Agent B,2026-10-10. **Complete elementary all-parameter subclass proof; independent review pending.** No arbitrary-factor solution, exact product-value, Lean or historical-priority claim.

## Theorem and prior input

For every n,m>=2, writing T_n=L(K_n),

    gp^-(T_n □ T_m) >= min{gp^-(T_n),gp^-(T_m)}.

This proves the original Kruft Welton–Khudairi–Tuite product inequality for this family. It is different from the previously frozen two-subset Kneser family: T_n vertices are two-element symbol sets but adjacency is INTERSECTION, not disjointness.

The factor formula is known: gp^-(T_n)=n/2 for even n, and(n+3)/2 for odd n. See Di Stefano et al., *Lower General Position Sets in Graphs*, arXiv2306.09965v1 Theorem5.2, [primary paper](https://users.fmf.uni-lj.si/klavzar/preprints/2306.09965.pdf). The original product statement is arXiv2404.19451v1 Conjecture2.10/final2025Conjecture3. The arbitrary-graph truncation at4 used below is B's frozen ebaa409418b53983ef1bd52abe34703c5dca6618, proofSHA256cbc5d97fb06da0317e36973ea6e9ef4ec6e70f89cb8799c1f6d4701c014b5075.

In T_n, distinct symbol pairs have distance1 if they intersect and2 if they are disjoint: in the latter case a pair formed by one symbol from each gives a two-edge path. Thus diameter is at most2, and product diameter is at most4.

## 1. Set up a hypothetical counterexample

Suppose S={(a_i,b_i):1<=i<=k} is an inclusion-maximal GP-set of T_n □ T_m with

    k < gp^-(T_n), gp^-(T_m).

The frozen truncated theorem implies k>=4. The known factor formulas imply

    n,m >= 2k-1.

Indeed for even n the strict inequality implies n>=2k+2; for odd n it implies n>=2k-1. We construct an extension of S, contradicting maximality. Repeated first or second coordinates are allowed throughout.

We use two metric principles already proved in the truncated-bound manuscript. A GP-set smaller than its factor's lowerGP-number can be extended by a new factor vertex. A product triangle equality holds exactly when both coordinate triangle equalities hold with the same designated middle.

## 2. Easily extendable GP projections

If either projection consists of k DISTINCT GP points, extend it in that factor and use any value in the other coordinate. Strict coordinate triangle inequalities protect all new product triples.

If a projection consists of k-1 distinct GP points, it has exactly one repeated fiber, of size two. Extend that projection in its factor. In the other factor extend the pair corresponding to the repeated fiber; it is a pair of distinct vertices because S has distinct product points. Any old pair in different fibers is protected by the first-coordinate extension; the unique old pair in the repeated fiber is protected by the second-coordinate extension. This again extends S.

These arguments work with factors exchanged and require only the strict factor-parameter assumptions above.

## 3. A distinct non-GP projection uses fewer symbols

Suppose a projection consists of k DISTINCT points but is not GP; interchange factors if necessary and call these a_1,...,a_k in T_n. View them as k distinct edges on n symbols.

A non-GP triple in T_n has distances1,1,2. Its three underlying edges therefore form a three-edge path P4 on four symbols: the outer edges are disjoint and the middle edge meets both. Consequently all k selected edges together use at most

    4+2(k-3)=2k-2

symbols. Let U be the unused symbols; n>=2k-1 implies U is nonempty.

### 3a. At least two unused symbols

Take a new edge u joining two unused symbols. It has distance2 from every a_i. Choose any vertex v of T_m that is outside the second-coordinate projection; one exists since |V(T_m)|=C(m,2)>k for m>=2k-1,k>=4.

The new product distances t_i=d((u,v),(a_i,b_i)) all lie in{3,4}. An old product pair has distance at most4, so the new point cannot be its middle. Also |t_i-t_j|<=1. The only possible endpoint obstruction would therefore be an old pair at distance1 with |t_i-t_j|=1. Because all a_i are distinct, distance1 forces a_i,a_j adjacent and b_i=b_j. But then t_i=t_j, a contradiction. Hence (u,v) extends S.

### 3b. Exactly one unused symbol

Here n=2k-1 and the support has exactly2k-2 symbols, since n>=2k-1 and support<=2k-2. Equality in the support bound forces the selected edge graph to be one P4 together with k-3 mutually disjoint isolated edges. Every edge outside the P4 must introduce two new symbols, distinct from all previously used symbols. Since k>=4, at least one isolated edge a_i exists.

Let u join the unused symbol to one endpoint of a_i. Then

    d(u,a_i)=1;  d(u,a_j)=2 for j!=i.

Choose a vertex v of T_m that is disjoint from b_i and not in the second-coordinate projection. There are C(m-2,2)>=C(2k-3,2)>k possible pairs disjoint from b_i, while at most k pairs are forbidden by the projection, so such v exists. Thus d(v,b_i)=2, and every d(v,b_j) is1or2. All new product distances again lie in{3,4}.

As in3a, only an old product pair at distance1 could create a new collinear triple. Such a pair must have equal b-coordinates and adjacent distinct a-coordinates. Neither a-coordinate can be the isolated edge a_i. Their distances from u are therefore both2, and their new product distances are equal. This rules out the final possible obstruction, so (u,v) extends S.

This handles EVERY distinct non-GP projection in either coordinate, including cases where the other projection repeats.

## 4. Both remaining projections have many unused symbols

If neither coordinate admits an earlier extension, each projection has either

- at most k-2 distinct underlying edges; or
- exactly k-1 distinct underlying edges that are not GP.

The first alternative uses at most2k-4 symbols. In the second, the P4 argument from Section3 gives support at most2(k-1)-2=2k-4. Hence each factor has at least three unused symbols, since n,m>=2k-1.

Choose an unused-symbol edge u in the first factor and an unused-symbol edge v in the second. The new point (u,v) has distance4from every element of S. For any old pair, its distance is positive and at most4, while the new distance sum is8and difference is0. No triangle equality is possible, so this point extends S as well.

All projection cases are exhausted, contradicting the supposed maximality of S. This proves the theorem. The n=2or other small-parameter cases already follow from the truncated theorem (and T_2 is a singleton). QED.

## Verification, limitations and next regime

`extend_linegraph.py` implements the proof's extension, including the one-unused-symbol critical case. `verify_linegraph_extension.py` checks it using separately constructed intersection adjacency and original BFS distances, with explicit critical/fiber cases and deterministic GP test instances. The mathematical proof above, rather than a bounded numerical sample, covers arbitrary n,m,k.

The factor values and the graph distance formula are prior general theory. No exact value of gp^-(T_n □ T_m) is derived here, and the original conjecture for arbitrary factors is still open in this work. Checks, actual logs, source hashes, and negative controls are supplied with the frozen packet. No external acceptance or Lean compilation is claimed.
