# Original product-conjecture counterexample review packet

B,2026-10-10 12:08UTC. Baseline8b42054aaee7e1aef22e1e50190f750786cd154d. Role independent discovery. Complete elementary proof and actual separate-definition checker PASS; independent reviewer pending. This is an ORIGINAL conjecture counterexample, not a partial bound, route obstacle or strengthened variant.

Original hypothesis map:
- Finite simple undirected factors: explicit clique unions,11and29vertices,30and140edges; no loops/multiple edges.
- Connected/nontrivial: each has a universal hub, diameter2.
- Product: actual Cartesian adjacency,319vertices/2410edges, not strong/direct/lexicographic product.
- Parameter: minimum size of an INCLUSION-MAXIMAL shortest-path GP set, not ordinary maximumGP or lower terminal number.
- Strict violation: both factor lowerGP>=6; explicit product GP5set maximal, hence product lowerGP<=5<6<=min(factors).

Complete proof COUNTEREXAMPLE_PROOF.md is elementary and standalone. It does NOT require the earlier universal-five metric-cone theorem to be accepted. FactorGhas exact lowerGP6. Huses true-twin saturation and six classified maximal landmarkGP sets; no exact Hvalue claimed. Product GP follows from off-diagonal distances2/3; product maximality has a short three-case argument. Stop size minimization and generalization until this packet is handed off.

Actual commands/environment:
- python workstreams/B/lower_gp_product/probe_block_wheel_counterexample.py
- python workstreams/B/lower_gp_product/verify_block_wheel_counterexample.py
Python3.12.14, standard library, PASS. Discovery constructs explicit adjacency and uses line-mask unions. The separate verifier imports no discovery code/data, reconstructs factors as twoK6/fourK9clique unions, constructs original product adjacency, computes ALL102723BFS entries across both factors/product, checks10selected triples and314outside product vertices, and gives an explicit valid extension to every GP factor subset of size<=5.

Factor scans: G1023subsets, GP counts11/55/140/230/262; H146595subsets, GP counts29/406/3192/17170/67764. All extend. Four true-twin classes and all six maximal five-landmarkGP subsets also checked. Three corrupted claims rejected: nonGP selection, falsely maximal four-point subset, and factorG falsely claimed lowerGP>=7 (explicit maximal6set rejects it).

Product-cover digest e97456a82e0234218b533cfd5608b7fb8977247dbebcb9c802d6bad13f3d1a7c
Factor-extension digest 421b4418abdf6b10136e23bb1fc905a84d40580c44762f154d8c955f868fe0bd
Proof SHA2564410d3d65163adc2a56385c17eedfab58d6fbc4a865d61f6d8f78094f5ba50b8
Verifier SHA256a7f99f7eea0d832e3dbdc84071b412b522e0865babe44b6f47801fc82fe67bef
Explicit discovery object SHA256b6a59acf6e3a26a5c871faf6c32854553d205616b9196d212071d3a2465b6f1c

Review priorities: original conjecture3/preprint2.10; maximal versus maximum; true versus false twins; landmark-only GP-set extension; full product maximality including selected-coordinate clones; factor connectivity and actual Cartesian distances. The fixed counterexample is sufficient; no optimum or minimality computation is needed.

Earlier stopped routes remain recorded. The five-point local relaxation was FEASIBLE, not itself a graph counterexample; realization plus independent-definition checking is the new step. Universal-five8b42054 remains a separate partial theorem. If accepted too, it makes this fixed product's lowerGP exactly5 and its universal cutoff sharp; the counterexample itself is independent of that implication.

Source/duplicate repeat gate is COUNTEREXAMPLE_SOURCE_GATE.md. No matching prior result located, historical novelty uncertain. No Lean claim or external independent acceptance. A clean-archive replay and immutable own-branch SHA complete handoff; ROOT alone controls integration/signing/review. No new subagents or peer messages.
