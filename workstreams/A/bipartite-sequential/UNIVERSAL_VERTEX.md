# Vertex-rank ordering lemma for graphs with a universal vertex

**Source:** Gorzkowska–Kwaśny, *Distinguishing adjacent vertices by ordering edges*, arXiv:2609.11832v1, Conjecture 10, https://arxiv.org/html/2609.11832v1. The paper already covers nonregular and high-degree cases. This theorem explicitly produces **pairwise distinct sequences at every vertex**, not merely at neighbours. No historical novelty, Lean or external ROOT acceptance is claimed.

## Theorem

Let G be a finite simple graph of n>=3 vertices with a *universal vertex* r (adjacent to all other vertices). For every fixed proper edge colouring w, there exists an explicit global edge order making the n induced incident-colour sequences **pairwise distinct**.

**Proof.** Rank the vertices 0,...,n-1 with r at rank 0 and s at rank 1, then order edges by **sum of endpoint ranks**, breaking ties arbitrarily. Incident edges at a fixed vertex have unequal rank-sums, so their local order is exactly the order of their *opposite endpoints* by rank.

Every v!=r has first neighbour r, hence its first colour is w(rv). These are pairwise distinct as v varies over V\{r}, since the colouring is proper at r. The first colour at r is w(rs), so r can coincide only with s. If d(s)<n-1, their sequences have different lengths. If d(s)=n-1, then s is universal too; their second entries are respectively w(rt), w(st), where t has rank 2. Those differ by properness at t. Thus all vertex sequences are distinct. QED.

This is a deterministic O(|E|log|E|) construction, without recolouring. In particular K4 under any fixed proper three-edge-colouring and K6 under any proper five-edge-colouring satisfy the original Conjecture 10. These are among the nonbipartite regular cases not covered merely by differing endpoint palettes or the published d>=6 theorem.

## Cubic infinite-family consequence

Start with K4 and repeatedly replace vertices by properly three-coloured triangles, as in `TRIANGLE_EXPANSION.md`. The result is an infinite class of nonbipartite cubic graphs for which **every proper three-edge-colouring** is sequentially orderable. A proper colouring using >3 colours is already covered by the original authors' distinct-palette Theorem 5. Thus this graph class meets the original *every proper colouring* quantifier. Replacing one K4 vertex gives the triangular prism.

## Exact finite check and boundaries

`python3 workstreams/A/code/verify_universal_vertex.py` reconstructs all incident sequences from the actual global order for all labelled graphs through n=7 with one universal rank-0 vertex, using two valid proper colourings per graph, and rejects an incomplete-order negative control. Actual stdlib result: `PASS 67732 labelled universal-root graphs/proper-colouring samples through n=7, missing-edge negative control`. The infinite result relies on the preceding proof, not the finite sample. No assertion is made about arbitrary nonbipartite cubic graphs without a universal vertex or a reducible triangle.
