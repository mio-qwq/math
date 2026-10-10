# A counterexample to permutation-digraph general-position optimality

Author of this research packet: distributed Agent B. Date: 2026-10-10 UTC.
Classification: counterexample to the original conjecture; pending independent review.

## Source and exact target

Ullas Chandran S.V, Gabriele Di Stefano, Grahame Erskine, Haritha S,
Elias John Thomas and James Tuite, *The general position number of digraphs*,
arXiv:2604.15909v1 (17 April 2026), Section 3.3, unnumbered conjecture
immediately after Theorem 3.6:

For integers k >= 3 and d >= 2k, the proposed equality is

    gp(Pe(d,k)) = 2 (d+k-2)_(k-1).

Here (x)_r = x(x-1)...(x-r+1). The theorem itself supplies a lower bound;
this packet contradicts its conjectured optimality, not that lower bound.
Primary source: https://arxiv.org/html/2604.15909v1#S3.SS3

Let A have d+k symbols. Vertices of Pe(d,k) are injective words of length k.
An arc drops the first letter and appends a letter absent from the ENTIRE
old word. Distances below are directed shortest-path lengths in the full
graph. A set is in general position if no directed geodesic contains three
of its distinct vertices (Definition 2.1 of the source).

## Construction and proof for the full stated parameter range

Put N=d+k. Partition A into T and C, with |T|=3 and |C|=N-3.
Take S to consist of all words (x_1,...,x_(k-1),t), where the x_i are
pairwise distinct members of C and t belongs to T. Then

    |S| = 3 (N-3)_(k-1).

All these words are valid vertices, because C and T are disjoint.
For any two distinct u,v in S we prove

    k <= dist(u,v) <= 2k-1.                         (1)

For the lower bound, after ell shifts with 1 <= ell < k, the last letter
of u remains at position k-ell. This position is one of the first k-1
positions of v, which only contain letters of C. The retained letter
belongs to T. Consequently no such walk ends at v. A walk of length zero
also cannot join distinct u,v.

For the upper bound, let U be the union of the letters of u and v.
Since |U| <= 2k and N=d+k >= 3k, A minus U has at least k letters.
Choose distinct buffer letters b_1,...,b_(k-1) in A minus U. Starting
at u, append these buffers in order and then append all k letters of v.
Each buffer is absent from the current word: it occurs neither in u nor
among the earlier buffers. After all buffers the current word is
(u_k,b_1,...,b_(k-1)). The next letter v_1 belongs to C whereas u_k
belongs to T, and no buffer is a letter of v. Hence this append is legal.
After that step u_k has disappeared. Every subsequent append is legal
because the letters of v are distinct and no buffer belongs to v.
This is a directed walk of length (k-1)+k=2k-1 ending at v. Removing
any repeated-vertex portions yields a directed path no longer than the
walk, proving the upper bound without invoking a diameter theorem.

For distinct u,v,w in S, (1) gives

    dist(u,v) + dist(v,w) >= 2k > dist(u,w).

Thus v cannot occur on a shortest directed u,w-path. This applies to
all orders of the triple, so S is in general position.

Finally the positive falling factorials cancel to give

    [3(N-3)_(k-1)] / [2(N-2)_(k-1)]
       = 3(d-1) / [2(d+k-2)] > 1,

because 3(d-1)-2(d+k-2)=d-2k+1 >= 1. Therefore

    gp(Pe(d,k)) >= 3(d+k-3)_(k-1) > 2(d+k-2)_(k-1)

for EVERY integer k >= 3 and d >= 2k. In particular, the original
optimality conjecture fails throughout its stated domain. QED.

Credit: the source's Theorem 3.6 uses two terminal symbols with a disjoint
prefix alphabet. The construction here changes that credited baseline
to three terminal symbols and supplies the explicit buffer-walk argument.
No claim is made to have invented the source's underlying construction.

## Explicit finite counterexample and hypothesis checklist

Set d=6, k=3, A={0,...,8}, C={0,...,5}, T={6,7,8}, and

    S = {(a,b,c): a,b in C, a != b, c in T}.

- Parameter hypotheses: 3 >= 3 and 6 >= 2*3.
- Ambient graph: precisely the original Pe(6,3), with 9*8*7=504 vertices
  and 504*6=3024 arcs; no modified edge convention or induced subgraph.
- Vertex hypotheses: all selected words have three distinct alphabet letters.
- Cardinality: 6*5*3=90 distinct selected words.
- General position: all ordered selected distances lie between 3 and 5,
  so two distances sum to at least 6 and cannot equal a third distance.
- Violation: source's proposed value is 2*(7)_2=2*7*6=84 < 90.

The explicit list is certificate.json. No claim that the exact maximum
is 90, or that this graph is a smallest counterexample, is required.

## Exact executable verification, limitations and review status

Run from the repository root with Python 3.12 (standard library only):

    python workstreams/B/permutation_gp/construct.py
    python workstreams/B/permutation_gp/verify.py
    python workstreams/B/permutation_gp/negative_tests.py

verify.py does not import the constructor or use (1). It rebuilds every
vertex and tests every ordered pair against the original arc definition,
then runs integer BFS from all 90 selected vertices. It checks every one
of the 704880 ordered triples of distinct selected vertices for shortest-
path distance equality. Actual results: PASS; 8010 ordered pairs, with
2880 distances 3, 3780 distances 4, and 1350 distances 5. Five corrupted
certificates are rejected, including one with an actual geodesic triple.
See verification.json and negative_tests.json for actual run receipts.

Both implementations and this proof were written and self-checked by B.
Separate code is not a separate reviewer. Independent review, historical
novelty and human responsibility review remain pending. No Lean compilation
or formalization is claimed. The executable deliberately covers the fixed
finite certificate; the all-parameter result is the written proof above.
