# B self-review: two-parameter Kneser product subclass

2026-10-10 11:25UTC. Independent review pending. This computer-assisted proof establishes the ORIGINAL conjectured inequality for K(n,2) square K(m,2), all n,m>=5. It does not resolve the conjecture for arbitrary factors.

Main file: KNESER_FAMILY_PROOF.md. The decisive universal step is bounded-support compression: k product vertices involve at most2k symbols per coordinate, and every at-least-five-symbol Kneser alphabet restriction is isometric. Hence exact four-point extension at alphabet10 and five-point extension at alphabet12 transfer to every larger alphabet, even when the two orders differ. The previously frozen arbitrary-graph truncated-at4 theorem handles smaller witness sizes and all factors with lowerGP<=4.

Independent-definition self-check command:

    python workstreams/B/lower_gp_product/verify_kneser_products.py
    python workstreams/B/lower_gp_product/verify_kneser_factor.py

Python3.12.14 standard library; no discovery imports. Separate endpoint-set-partition generation covers all ordered projection lists, including repetitions. Factor distances come from original disjointness adjacency and BFS. The checker asserts closure under all simultaneous index permutations before reducing the first projection; the second remains unrestricted. Actual distance-vector representatives, not numerical optimization, provide extensions. Multiplicity is irrelevant only because distance-zero coordinates uniquely identify selected vertices; the manuscript explains this.

Actual PASS: k4 has1657 endpoint partitions,321 normalized presentations,122 metric types,19 first-projection orbits,2318 type pairs,677 GP configurations extended. k5 has43833 endpoint partitions,4900presentations,1718types,63orbits,108234pairs,25892 GP configurations extended. Product-root BFS entries2025+4356; two negative controls per k. The separate Petersen boundary has no maximal GP sets of sizes1,2,3 and exactly5of size4, with one rejected false GP control. Source hashes and deterministic witness digests are recorded with the frozen packet.

Control correction: the first Petersen negative-test fixture used indices(0,1,7), which actually form a GP triple, so its deliberately-negative assertion failed. It was replaced BEFORE freezing by(0,1,9), the explicit shortest path01–34–02, and the complete boundary check was rerun successfully. No theorem statement or positive computational result was changed to hide this test-fixture mistake.

Prior results retained as prior: factor lowerGP values from Di Stefano et al. Theorem5.1; matching terminal sets and the terminal-layer upper bound from the original product theory. Consequently the exact product value is5or6 when10<=min(n,m)<=13. For n,m>=14 the lower bound6 is proved but the exact value is not. The failed universal six-point upper template (720correlations, always48uncovered representative points) is preserved, with no nonexistence inference beyond that template.

Review obligations: every original quantifier; the factor formula attribution; completeness of restricted-growth endpoint partitions; all index permutations and equality-vector compression; omission of distinct GP projections using the ACTUAL factor lower bound; outside-point test; isometric compression back to arbitrary n,m; and the link to the separately frozen truncated theorem. This is a complete computer-assisted written proof of a subclass, not a finite graph sample and not Lean. No independent reviewer, historical priority, new root number or submission is claimed.

Stop the closed four/five-point Kneser search: its whole stated regime is covered. Resume the general product problem only with a genuinely different factor class or a new four-point structural argument. Do not simply increase Kneser n,m or repeat the same quotient to add counts.
