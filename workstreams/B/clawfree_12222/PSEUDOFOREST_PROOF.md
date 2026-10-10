# Mixed short connectors when the direct-edge core is a pseudoforest

Agent B, 2026-10-10. A new affirmative subcase of arXiv:2608.02566v1 Section6 Conjecture1; pending independent review. No full-conjecture, counterexample, novelty or Lean claim.

## Precise theorem

Let H be a finite LOOPLESS subcubic multigraph. Replace each vertex by a triangle with distinct ports for its incidences; unused ports are retained. Replace each core edge by a connector of length 1 or 2. Let D be the spanning submultigraph consisting of the length-1 edges. If every connected component of D has at most one cycle (counting parallel-edge two-cycles), the resulting graph G admits a (1,2,2,2,2)-packing coloring.

Unlike the previous fully-subdivided theorem, this allows genuinely mixed direct and length-2 connectors, including arbitrarily large branching direct-edge trees and unicyclic components. No bound on core order is imposed.

## The weak color class

Orient every tree component of D toward a chosen root. Orient the unique cycle of each unicyclic component cyclically and orient its attached trees toward it. Thus every direct edge has exactly one tail, and each core vertex has outdegree at most one. This also works for a two-cycle of parallel edges, with opposite directions on its two distinct edges.

Let W consist of every length-2 connector's internal vertex and, for each oriented direct edge, its tail's port. Each triangle contains at most one selected port. On a direct edge exactly one endpoint is selected; selected ports cannot meet along another external edge because each port has only one external incidence. Length-2 internal vertices are adjacent only to their own ports, neither of which is selected (selected ports belong to direct edges). Therefore W is independent and may receive color 0.

## Four-color the exact remaining distance-two conflict graph

All vertices outside W are triangle vertices. Let F have these vertices, with an edge precisely when their distance IN G is at most two. We show maximum degree(F)<=4 and no component of F is K5. Brooks' classical theorem then gives a proper four-coloring of F, which is exactly the required assignment of colors 1,2,3,4.

Consider a triangle containing a selected outgoing port. It has two remaining vertices. Each remaining vertex x sees:

1. its one remaining triangle partner;
2. the positive port at the far end of the outgoing direct edge, at distance two through the selected port;
3. if x is an incoming direct-edge port, the two remaining vertices in its tail triangle, both at distance two through the selected opposite endpoint; or, if x is a length-2 port, just its opposite endpoint at distance two; or no such vertex if the port is unused.

There are no further positive vertices within distance two: the other triangle ports lead either to selected vertices or to their own distance-two endpoints, which are at least three steps from x. Hence an incoming direct-edge port has degree at most 1+1+2=4; a nondirect or unused port has degree at most 3.

A triangle with no selected outgoing port occurs at a root of a tree component of D (including an isolated vertex). It has three remaining vertices. An incoming direct-edge port sees its two triangle partners and the two positive vertices of the tail triangle, giving degree at most four. A nondirect or unused port sees its two partners and at most one opposite length-2 endpoint, giving degree at most three. This accounts for all possibilities, including identifications that only lower the count.

The positive vertices belonging to each D-component induce a connected subgraph of F: each triangle retains two or three vertices forming a clique, and each direct edge connects the head port to both remaining vertices of the tail triangle in F. A finite pseudoforest has average degree at most two, so each D-component contains a vertex of D-degree at most two. Its triangle has a nondirect or unused port, necessarily positive, whose degree in F is at most three by the previous paragraph. Adding distance-two edges from length-2 connectors does not change this bound. Therefore every component of F contains a vertex of degree at most three and cannot be K5.

Brooks applies componentwise: maximum degree four gives at most four colors unless K5; components of smaller maximum degree also require at most four colors, including odd cycles and K4. This proves the theorem. Brooks and functional orientation of pseudoforests are imported elementary/classical tools, not new claims.

## Optional long-connector extension

The same construction works if every nondirect connector has length 2 or at least 4. Define W initially using only length-2 interiors and outgoing direct ports, and construct F on positive triangle vertices. Long connectors create no distance-two conflicts between triangles, so the preceding bounds still hold. Their endpoints p,q are positive.

For each L>=4 insert a path with first and last internal colors 0. Bases are:

- L=4: p,0,r,0,q, with positive r distinct from p,q;
- L=5: p,0,r,s,0,q, with positive r!=p, s!=q and r!=s;
- L=6: p,0,r,0,s,0,q, with positive r!=p, s!=q and r!=s.

There are always choices among four positive colors. Extend by three using the suffix recurrence in MIXED_PATHS_PROOF.md, preserving final internal color 0. First/last internal zeros are not adjacent to any old zero: their endpoint ports are positive and selected ports in the same triangle are at distance two. Internal positive colors only see the actual endpoint at distance two, already enforced. Cross-connector internal distances are at least three. Thus the argument remains valid for all such mixed unbounded lengths. Length-3 connectors are not asserted covered by this optional extension.

## Remaining scope and evidence

In the all-short loopless model, only direct-edge components with at least two independent cycles remain outside this new theorem. This is a structural reduction of the still-open model, not a solution of those remaining components. General claw-free attachments still need their own justified reduction. Earlier cubic and connector frozen proof bytes remain unchanged.

verify_pseudoforest.py independently reconstructs the original graphs and their all-pairs distances, forms F by those distances (not the degree-count formula), checks W independence, the maximum-degree and non-K5 conditions, finds an exact proper four-coloring and validates the final original-graph packing. It exhausts the stated finite core edge-type families and includes a damaged-color negative test. Unbounded validity rests on the proof above, not the sample count. Python standard library only; no independent review or Lean claimed.
