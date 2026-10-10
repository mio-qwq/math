# A short proof of Conjecture 10 using de Werra's equitable edge colouring

**Agent A, working revision — 10 October 2026.** This is an alternative
presentation of the full original Conjecture 10 written proof, which ROOT has
mathematically reviewed under immutable commit `7168f6df66ba5518cd3420c4668eab5352e4be8c`.
It is NOT itself independently reviewed, Lean-compiled, peer reviewed,
published, or a claim of historical firstness. The full original mathematical
freeze and its source files remain unchanged.

## Problem and proper attribution

Gorzkowska and Kwaśny, *Distinguishing adjacent vertices by ordering edges*,
arXiv:2609.11832v1 (10 September 2026), Conjecture 10: Given ANY fixed proper
edge colouring `w` of a connected finite simple graph G other than K2 or an
even cycle, find ONE total order `prec` of ALL edges such that the lists of
colours of incident edges, read in that order, differ at the endpoints of
EVERY edge. Colours must not be changed.

Their published Theorem 5 **already proves** this for connected graphs with
adjacent vertices having different incident-colour palettes, including all
nonregular graphs and class-two graphs. We reuse that theorem explicitly.

The selection lemma below is **NOT a new A theorem**: it is a direct
application of de Werra's equitable 2-edge-colouring of bipartite multigraphs,
known since the 1970s. See D. de Werra, *An extension of bipartite multigraphs*,
Discrete Math. 14 (1976), 133–138, DOI
10.1016/0012-365X(76)90056-X; also A. Frank,
*Connections in Combinatorial Optimization*, Theorem 2.4.22. The latter's
"strongly equitable" version also controls total colour class sizes, though
we only need local equitability here.

## Root selection from a classical theorem

Assume G is d-regular (d>=3) and the fixed proper colouring uses **exactly d
colours**, now bijectively relabelled 0,...,d−1. Each colour is a perfect
matching, so the edges of colours 0 and 1 form vertex-disjoint even cycles
`C_1,...,C_k`, each of length at least four because G is simple. Write Q for
the graph formed by the other d−2 colour classes. Since Q is (d−2)-regular,
**each Q component has at least two vertices**.

Make the bipartite incidence *multigraph* H with one left vertex for each C_i,
one right vertex for each Q-component S_j, and one **separately labelled
edge for each vertex x of G**, joining the left C_i containing x to the
right S_j containing x. Preserve all parallel incidence edges.

Apply de Werra's equitable two-edge-colouring of H: paint each labelled edge
red or blue so that, at every H vertex, the numbers of incident red and blue
edges differ by at most one. Since each C_i has at least four vertices, and
each S_j has at least two, **both red and blue occur at every such vertex**.
For each C_i choose exactly one vertex r_i whose labelled incidence edge is
red. Let R={r_1,...,r_k}. Every S_j contains a vertex with a blue incidence
edge, which is necessarily outside R. Therefore R meets each C_i exactly
once and contains no Q-component in its entirety.

## Put the selected roots in a suitable order

Every component K of the induced graph Q[R] has at least one vertex adjacent
in Q to a vertex of V(G)\R: otherwise K itself is a whole Q-component
contained in R, which was ruled out above. Choose one boundary root b in
K, root a spanning tree of K at b and list its vertices **child before
parent**. Concatenate these lists over all components of Q[R]. It follows
that every root r has an incident Q-edge to a nonroot or to a root LATER
in the resulting root ordering.

## Construct ONE total order of all original edges

Order the even cycles in the same order as their chosen roots. For each
cycle C, rotate/orient its vertex sequence `v_0,...,v_(m-1)` so that the
root is v_0 and its outgoing cycle edge e_0=v_0v_1 has colour 0.
List its cyclic edges `e_0,e_1,...,e_(m-1)` in that order; their colours
alternate 0,1,...,0,1. Concatenate these complete cycle blocks.

For every Q-edge xy, select precisely one endpoint as its owner:

- if one endpoint is a root, choose the root;
- if both are roots, choose the earlier root;
- otherwise choose the earlier endpoint in lexicographic (cycle block,
  vertex index within its cycle) order.

Insert each Q-edge **immediately after the outgoing cycle edge** of its
owner, and sort any multiple edges in the same slot by their original
(distinct) colours. All edges have a unique insertion slot, yielding one
global total order `prec` of precisely E(G). The original colouring `w`
remains fixed.

## Verify every possible adjacent pair

- **Root/nonroot:** at a root, colours 0 and 1 have at least one Q-colour
  between them, because its special ordering ensures at least one Q-edge
  is assigned there; at every nonroot these two colours are consecutive.
  Hence every edge between a root and a nonroot is distinguished.
- **Nonroot/nonroot cycle edge:** neighbouring nonroots on an alternating
  0/1 cycle see 0 and 1 in *opposite relative order*. Q-edge insertions
  never interpose between the two cycle edges at a nonroot, so their lists
  remain distinct.
- **Root/root Q-edge:** the Q-edge belongs to the earlier root, whose
  occurrence of its colour is between 0 and 1. At the later root the same
  Q-edge occurs before both 0 and 1. Their sequences are distinct.
- **Nonroot/nonroot Q-edge:** it belongs to the lexicographically earlier
  endpoint and its colour appears AFTER both 0 and 1 there and BEFORE both
  at the later endpoint. Within a single cycle, the endpoints cannot be
  consecutive because G is simple and their connecting 0/1 edge already
  exists. Again their sequences are distinct.

These cases cover ALL original edges, so the global order works for every
proper d-edge-colouring of every d-regular simple G for d>=3 (even when G
itself is disconnected).

## Finish the original connected conjecture

For connected nonregular graphs, or for any fixed proper colouring with one
edge joining different vertex-colour palettes, invoke the original authors'
Theorem 5. Otherwise connectedness forces all palettes equal: G is regular,
and if d>=3 the constructive argument above applies. Degree one gives K2;
degree two gives a cycle, where the proper alternating two-colour even-cycle
obstruction is precisely the original excluded case and colourings with
at least three colours have different adjacent palettes. K1 is vacuous.
Hence the original Conjecture 10 holds, subject to the already accepted
mathematical review of the complete A proof. QED.

## Provenance and independent checking

The original full proof frozen at
`workstreams/A/bipartite-sequential/ALL_DEGREES_THEOREM.md`
(commit `7168f6df66ba5518cd3420c4668eab5352e4be8c`) was independently
written-PASS reviewed by ROOT. This SHORT derivation is a different
presentation and is **not** independently accepted merely by association.
No original auxiliary theorem is claimed in the root-selection paragraph:
that is de Werra. The nontrivial algorithmic step connecting root order,
edge ownership and all endpoint cases remains explicitly proved above.

A separate strict finite certificate checker in
`workstreams/A/code/check_euler_order_certificate_strict.py` reconstructs
all these steps from the original graph; its checks are useful regression,
not a proof of the infinite statement or a Lean kernel certificate.
The source paper's historical status and later citations require a new
independent literature review before any external priority claim.
