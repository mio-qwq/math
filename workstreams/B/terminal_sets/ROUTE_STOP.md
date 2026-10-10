# Terminal-set route pause, 2026-10-10 11:01UTC

Original Conjecture3.3/finalConjecture6 remains unresolved. This packet does not assert a new existence theorem or counterexample.

Three distinct mechanisms were tried:
1. Exact permitted-subset/endpoint-coverage search on220 connected nonbipartite bridgeless cubic graph presentations,20at each even order12through32, all diameter>=4. Every one produced a terminal-set witness, with at most163 search nodes; no hard or failed instance emerged. These are a bounded deterministic seeded sample, not all cubic graphs.
2. Unequal subdivisions of K4,K5,K6 with edge lengths1through4 distorted the metrics. Among79 retained nonbipartite diameter>=4 presentations all had witnesses; no graph-theoretic uniform rule was proved.
3. A proposed constructive potential based on inclusion-minimal geodesic convex hulls of maximal GP sets failed in the fifth12vertex sample. Raw obstruction is in hull_route_obstruction.json: a maximal nonterminal triple{2,5,11} with four-vertex star hull. This auxiliary classification was discovered using the same original-distance search and has NOT been independently certified; it is recorded only as a reason not to base a proof on that stronger assertion. The graph has a separate actual terminal-set witness, so it cannot refute the original conjecture.

A separate verifier rebuilds all299 positive witnesses using Floyd-Warshall and direct triple equalities, without discovery imports. Run `python workstreams/B/terminal_sets/verify_witnesses.py`; actual PASS output and one negative control (P3 endpoints are maximal GP but nonterminal) are recorded. These checks guard semantic mistakes;299 witnesses do not settle the conjecture.

Pause these three mechanisms rather than increase sample counts or report the already-known small-graph regimes as research gains. Resume only with a concrete general construction/exchange invariant, a structurally exceptional graph, or an exact unsuccessful full subset search. The reserved scope remains recorded but inactive. B is screening the separate lower-GP Cartesian-product conjecture from the same paper, for which small split factors give a new concrete diagnostic; that scope must be reserved before substantive search.
