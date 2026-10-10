# Mixed direct and longer connectors: precise remaining obstruction

Agent B, 2026-10-10. Positive subcase, pending independent review. This file supplements frozen cubic result b49a74f9ed65133a8c0e12ee998c44c5401e73d8; its bytes are unchanged. No claim that the original full subcubic conjecture has been solved.

## Universal local extension for lengths at least four

Let uv be an edge between two vertex-disjoint triangles in a subcubic graph. Every valid (1,2,2,2,2)-coloring extends, without recoloring old vertices, when uv is replaced by an internally disjoint path of ANY length L>=4.

The closed boundary consists of u and its two triangle neighbors, and v and its two triangle neighbors. Write them in order (u,a,b,v,c,d). The two triangles plus uv form the minimal boundary graph. Every actual coloring restricts to a valid coloring of this minimal graph, because deleting other edges cannot decrease distances. Exhausting its 5^6 assignments gives exactly 1008 valid assignments, or 42 orbits under permutation of colors 1,2,3,4 while fixing 0.

subdivision_certificate.json supplies, for every one of these 42 canonical boundaries, a path word at each length 4,5,6 that preserves the endpoints and is valid on the expanded boundary graph. These 126 literal rows are a finite proof certificate, checked without a discovery search by verify_subdivision_certificate.py. The checker enumerates the entire definition-level boundary space, verifies orbit coverage, and recomputes all graph distances for the supplied words. It also rejects a deliberately corrupted coloring. No numerical solver is involved.

For all larger lengths, use the following exact recurrence. If a valid word ends t,q, replace that final pair by t,q,r,t,q, where r is a positive color different from both t and q. There are at least two choices. Adjacent colors remain different. Every positive color repeated in this suffix is repeated at distance 3 or more; every distance-2 comparison across the retained prefix is the same as before or involves r versus t. The last internal color t and endpoint q are unchanged. The old prefix occurrences moved farther from the outside v-neighborhood cannot create new conflicts; the new second-from-last internal vertex has color r!=q. This proves every L>=4 from the three base lengths modulo 3.

The only old vertices within distance 2 of a new internal vertex are u,a,b,v,c,d: u and v have no fourth neighbor, and reaching any other old vertex costs at least three edges. An outside shortcut between new internal vertices through the two distinct endpoints costs at least three edges, so cannot create a forbidden pair. Old-old distances cannot decrease under subdivision. Thus these finite boundary checks and the recurrence prove the universal statement in the full graph, including extra edges among boundary vertices and arbitrary external graph structure.

## Why length two or three cannot be handled by that fixed-color rule

Exact probe_subdivision.py reports 288 of the 1008 boundaries fail for L=2, and 48 fail for L=3. For example (0,1,2,3,0,4) fails for L=2; (1,2,3,4,2,3) fails for L=3. These are failures to extend a PARTICULAR coloring, not noncolorable original graphs. No original counterexample is inferred.

## Global corollary with direct edges allowed

Take any finite loopless subcubic multigraph H; replace every vertex by a triangle, and each core edge by a port-to-port connector, all using distinct ports. If every connector has length 1 or at least 3, the graph is (1,2,2,2,2)-colorable.

To see this, subdivide in H every core edge whose required connector length is 3 once. Call the resulting loopless subcubic multigraph H'. The universal T3(H') theorem in Section 2 of CUBIC_PROOF.md applies, including parallel edges and unused ports. At each new degree-two core vertex, deleting the unused third triangle vertex leaves a length-3 connector. Deleting vertices cannot decrease graph distances, so this preserves packing validity.

Before those deletions, replace every remaining port edge whose target length is >=4 by the path-extension theorem just proved. Such edges join two vertex-disjoint original triangles and their ports are disjoint, so the theorem can be applied successively. Keep target-length-1 edges unchanged. Finally delete all unused third vertices introduced for target length 3. The resulting graph is exactly the prescribed one. This is an all-size constructive proof using the frozen triangle-expansion theorem, not an inference from a finite graph sample.

## Scope after combining the two new subcases

SUBDIVIDED_PROOF.md covers arbitrary connector lengths >=2, including loops and parallel core edges. The present corollary covers loopless cores with lengths 1 or >=3. Their union therefore leaves the mixed situation where both length-1 and length-2 connectors occur as a genuine unresolved family, as well as general attachments not yet reduced to this model. The two theorems cannot be combined to remove that restriction without a new argument.

No stronger (2,2,2,2,3) statement is claimed. Literature gate remains SOURCE_GATE.md. No new agent, independent acceptance, Lean or historical novelty is asserted. Actual Python 3.12.14 stdlib checks: 1008 boundaries; 42 orbits; 126 base words; 5712 expanded-boundary distance pairs; 504 generic suffix transitions; one negative control, all PASS.
