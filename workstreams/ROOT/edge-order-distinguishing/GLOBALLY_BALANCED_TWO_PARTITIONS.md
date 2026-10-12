# Simultaneous two-partition balancing with an exact global half-size target

This is a classical corollary of de Werra's strongly equitable edge-colouring theorem for bipartite multigraphs. A self-contained constructive Eulerian proof is supplied below. It was independently reconstructed in an AI mathematical review on 12 October 2026; it is not claimed as a new mathematical theorem and has no complete Lean formalization.

## Prior art (this is NOT a discovery of a new theorem)

For any bipartite multigraph, D. de Werra's strongly equitable k-edge
colouring theorem gives colour classes that differ in size by at most one
("equalized") and whose incident counts at every vertex differ by at most
one ("equitable"). Applying it with k=2 to the bipartite incidence
multigraph of two set partitions gives the result below immediately.
Our odd-vertex pairing proof matches the standard Euler-orientation method.
For provenance see D. de Werra, *An extension of bipartite multigraphs*,
Discrete Mathematics 14 (1976), 133–138, DOI:
10.1016/0012-365X(76)90056-X; and A. Frank,
*Connections in Combinatorial Optimization*, Theorem 2.4.22
(de Werra's strongly equitable edge-colouring theorem, including the
within-side pairing proof). This corollary is classical; no claim of original priority is made.

## Theorem

Let a finite set X have **two arbitrary set partitions** P and S (singleton
blocks are allowed; X may be empty). There is a red/blue colouring c of X such
that every block B of P or S satisfies

    | #red(B) - #blue(B) | <= 1,

and **globally** exactly floor(|X|/2) elements are red and ceil(|X|/2) blue.
A deterministic indexed-adjacency algorithm takes O(|X|) time and space.

This strictly refines the previous simultaneous discrepancy-one statement,
which controlled each partition block but had no specified total red count.

## Proof: pair odd-degree vertices on the SAME side

Construct the bipartite incidence **multigraph** H: one vertex for every P
block, one for every S block, and a separately labelled edge e_x between the
blocks containing each x in X. Parallel edges are NOT collapsed. Every
vertex degree equals its block cardinality.

Let L be the left P vertices and R the right S vertices. There are
`n=|X|` original edges, so the number of odd-degree vertices in L has parity
n, and so does the number in R (the sum of degrees on either side is n).

Add auxiliary edges to make the graph Eulerian as follows:

1. Pair as many odd-degree vertices **within L** as possible and join each
   pair by one labelled dummy edge. Do the same within R.
2. If n is odd, precisely one odd vertex remains unmatched on each side;
   join this left-right pair with one final dummy edge. If n is even,
   none remain unmatched.

Every augmented vertex now has even degree, so orient every connected
component by following an Euler circuit, obtaining an orientation with equal
in- and outdegree at each augmented vertex. Delete the auxiliary edges.
Each original vertex had either zero or one dummy incident edge, so its
original in-/outdegree imbalance is at most one.

Colour each ORIGINAL incidence edge red when oriented L -> R, and blue when
oriented R -> L. At an L vertex its red count equals its original outdegree;
at an R vertex its red count equals its original indegree. Hence in every
P and S block the red-blue count difference has absolute value <=1.

It remains to control the **global** red count. Since each original red edge
contributes +1 to the sum of original outminus-in imbalances over L, and each
blue edge contributes -1, we have

    #red(X) - #blue(X) = sum_{v in L} (out_orig(v)-in_orig(v)).

Every dummy edge joining TWO L vertices has opposite contributions at its
endpoints when deleted, so its contribution to this sum is zero. Dummy edges
joining two R vertices do not affect the sum at all. If n is even there is no
cross-side dummy, so the sum is zero. If n is odd, exactly one cross-side
dummy affects the sum, by +1 or -1. Thus `|#red(X)-#blue(X)| <= 1`.
If needed, exchange the names red and blue globally, which preserves every
per-block inequality and makes `#red(X)=floor(n/2)`.

This proves the theorem. QED.

## Component-avoiding graph corollary

If each P and S block has at least two elements, then each block contains
both colours. Selecting exactly one red from each P block leaves a blue
unselected element in every S block; in fact at least
`floor(|S_j|/2)` blue witnesses remain. Take S as the connected-component
vertex sets of the leftover graph Q in the original edge-ordering proof.

This corollary supplies the root selection used in `DE_WERRA_SHORT_PROOF.md`; the root-ordering and single-global-edge-order arguments are separate steps.

## Executable scope and complexity

`code/global_balanced_partitions.py` implements the paired odd-vertex augmentation and Euler-tour orientation. Its literal validator checks every original block and the exact global floor-half red count. The 12 October 2026 independent review executed five boundary examples, including the empty set, a singleton, singleton blocks, an odd underlying size and parallel incidence edges. Historical worker counts of 44,169 small partition pairs, 2,738 larger examples and a 100,000-element stress test have not been independently rerun here.

The indexed-adjacency algorithm takes O(|X|) time and space under constant-time label access; the Python dictionary implementation has an expected-time bound for arbitrary hash keys. The finite examples supplement the all-finite-set proof above. Exact provenance and verification scope are recorded in `provenance.json` and `VERIFICATION.json`.
