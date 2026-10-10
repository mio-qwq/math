# Universal-five frozen-review packet

B,2026-10-10 11:58UTC. Baseline020539c3e7169bf1a78e7b4b6006ff3793992ec5. Result: for ALL nonempty finite simple undirected graphs G,H, gp^-(G square H)>=min(5,gp^-G,gp^-H). This resolves original Conjecture3/preprint2.10 whenever either factor parameter<=5; arbitrary orders/diameters/disconnected graphs included. It is a PARTIAL theorem, not the full original conjecture or a counterexample. Pending independent review.

The complete proof is UNIVERSAL_FIVE_PROOF.md. Unlike the immediately earlier diameter-two result, it uses a complete arbitrary-metric cone and does not rely on bounded-distance samples. The main checker also covers set sizes1,2,3 directly, so the proof has no dependency on B's earlier truncation-at4.

Actual commands, Python3.12.14 stdlib:
- python workstreams/B/lower_gp_product/verify_metric_rays.py
- python workstreams/B/lower_gp_product/verify_universal_five.py

All PASS. Exact double-description from10orthant rays and30triangle inequalities yields25extreme rays, at most64intermediate rays. Exact zero-pattern closure has9484faces. For k=1/2/3/4, landmark models1/2/8/106; outside profiles1/5/87/9101; GP product cases1/2/14/2381; actual search states including the negative-control case2/3/15/2508. Every necessary local system is infeasible. Each run also checks33unweighted graph realizations/6022BFS entries and3negative controls. The repeated33fixtures are the SAME semantic fixtures, not132distinct independent tests.

Certificate SHA256 by size:
1 96d806e0b6ceca36c5346273481079e390daa188fc97e4302f39b1dc0436133a
2 7772dbba1a8d4438b644d7b4fda05182389467038969c7629d5e9c239067d4e2
3 fa1fe74b732b9e524e0e13468067b8cb6651a50921f49632f025f4b5533c14ec
4 711f13a8995d9667bb276999ca636891a8ee82553193bbe068df0dc55ce1099f

Proof SHA256f9742af7532e5f2155048bc89e516747c659f42bd17b4bbf3133caffb1db4406
Metric-ray verifier SHA25659299a4e518d539dc9a527832eddfe8842f62c171cce1df0b46bf1634db9321c
Profile verifier SHA25669999ef184ce26c91ab5c2e53fb94a647e7d8b1f71a24b60d6596b41ad2e27b1
Harness SHA256f354221432d3b0309b7b9b2345c1a5456221528dc028b2d29e5338d66e256fce

Independent-definition verification means no discovery imports/data; it is still B's self-check. Discovery uses the PRIOR25ray cut/K2,3description, positive-support closure and first-side recursion; checking derives rays from inequalities and uses zero intersections/actual integer representatives/second-side iteration. Neither route uses floating-point optimization. No Lean or author contact. Generic polyhedral theory and original lowerGP problem are cited accurately.

Review priorities: exact double-description adjacency with redundant constraints; completeness of all zero patterns for real distances; duplicate labels in sizes<4; profile grouping as an OVERAPPROXIMATION; mandatory known profiles and positive new-product distance; all maximal-landmark demands; exhaustive second-demand branching; disconnected sum inequality. Known-profile compatibility checks both equality bits and shared zero labels. Outside profiles never have a zero landmark distance.

There were no unresolved candidate failures or omitted feasible local cases. All first-stage arbitrary-four local systems were infeasible. The k1–3 extension checks were added to remove reliance on the earlier theorem, not to patch a failure. Three-factor products and all sizes>=5 are unproved here. New progress requires a genuinely complete larger-metric mechanism or a new original counterexample; no more sampling of the now-proved sizes. Historical priority remains uncertain after bounded exact-query and source checks.
