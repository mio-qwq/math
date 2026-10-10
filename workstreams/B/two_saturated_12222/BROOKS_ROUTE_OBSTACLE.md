# Exact obstruction to the maximum-degree-four route

Agent B; 2026-10-10. Classification: auxiliary proof-route obstruction, **not** a counterexample to the original conjecture. Pending independent review.

## Original scope

Mortada et al., arXiv:2603.25113v1, Section 5 Conjecture 4 asks for a (1,2,2,2,2)-packing coloring of every finite simple 2-saturated subcubic graph. Here each degree-three vertex has at most two degree-three neighbors. See SOURCE_GATE.md for the original and the earlier Mortada–Togni 2024 Open problem 2.

If I is the weak-color independent set, the remaining four colors must properly color **G²[V\I]**, with square distances taken in the original G. A tempting sufficient route first asks for maximum degree at most four, then handles the Brooks exceptions. Even the maximum-degree prerequisite can fail.

## Exact object and statement

Take the cube on vertices 0,...,7 with edges whose endpoint bit strings differ in one bit. Subdivide the matching (0,1),(2,3),(4,6),(5,7) once, using new vertices 8,9,10,11 respectively. The complete edge list is in brooks_route_probe.json. The graph has 12 vertices and 16 edges. Each original vertex has two degree-three neighbors and one degree-two neighbor; thus it is 2-saturated and subcubic. It is connected and simple.

For this graph,

    min over independent I of Delta(G²[V\I]) = 5.

Nevertheless, its original conjectured coloring exists: colors on vertices 0,...,11 are

    0,0,1,2,2,1,0,3,3,0,4,0.

Color 0 has separation greater than one; every other color has separation greater than two.

## Complete finite certificate

verify_brooks_obstacle.py rebuilds adjacency from the full edge list, checks the original graph hypotheses, and computes all distances by independent breadth-first searches. It imports no discovery or optimization code. It visits all 4096 subsets, rejecting precisely those containing an original edge. For each of the remaining 226 independent sets, it computes the maximum induced-square degree. The exact histogram is:

    degree 5: 27; degree 6: 96; degree 7: 82; degree 8: 21.

This exhaustive enumeration is a finite proof certificate for this particular obstruction, not a universal theorem. The checker also verifies the displayed original coloring and rejects a deliberately damaged coloring. An edgeless control rejects extending the obstruction to every graph. The discovery JSON retains a stale preliminary scope string saying the original coloring was not decided; its later original_status=SAT and explicit witness supersede that preliminary string.

Actual execution, Python 3.12.14, standard library only:

    python workstreams/B/two_saturated_12222/verify_brooks_obstacle.py

Result: PASS; all 4096 subsets, 226 independent sets, 144 distance entries, two controls. See verify_brooks_obstacle.log. File hashes are recorded in workstreams/B/SHA256SUMS.

The discovery MILP's infeasibility status is not used as evidence by this certificate. This result blocks only the uniform maximum-degree-four strategy. It does not block four-colorability at larger degree, a degeneracy strategy, recoloring, or the original conjecture. Do not count it as another original-problem refutation.
