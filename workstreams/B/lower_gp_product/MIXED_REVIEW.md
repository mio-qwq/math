# Mixed-family verification — B, 2026-10-10 11:42 UTC

Classification: complete elementary subclass proof of original Conjecture 3 (preprint 2.10), not an original counterexample or the arbitrary-factor theorem. Independent human/agent review pending; no Lean claim.

Baseline: 95acdcd925c881809b7dee6c62ab7abf8ac18628. The exact mixed-family theorem and dependencies are in MIXED_FAMILY_PROOF.md. Prior factor formulas are credited. The proof covers every parameter n>=2,m>=5 and every hypothetical small maximal set, including repeated projections and the critical odd alphabet. The finite regressions are semantic checks, not a substitute for the proof.

Actual command: python workstreams/B/lower_gp_product/verify_mixed_extension.py
Environment: Python 3.12.14, standard library. Result PASS, 10000 GP sets extended, 31923 factor BFS entries, 46224 product BFS entries, 4 negative controls. Modes: constant_three 4968; critical_one_unused 623; distinct_gp 3706; one_repeated_gp 703. Exact run output: verify_mixed_extension.log. Constructor and verification use different distance implementations: the latter rebuilds original intersection/disjointness adjacency and BFS, and checks product BFS for each exercised branch.

SHA256 proof c1501ce17b0fc94d1d7fd9ea6fab48814117332dbd894eac87a3b02400ea8a68
SHA256 constructor 72f221b327df779a7728ba40ad6586ce435cacab8b79f9467f32bac5b075fe2d
SHA256 checker dc49de3a4745b035e226bcb00dccd1fb364fb2634100c1dc89726024d5444d1a

Review focus: Kneser distance to an unused pair is ONE, whereas line-graph distance is TWO. At the critical boundary choose the second edge INTERSECTING the selected edge, reversing the disjoint choice of the pure line-graph construction. Check that distance-one old pairs cannot involve the isolated first edge. No unsuccessful mixed search or hidden change to frozen proofs. Arbitrary factors and additional exact mixed product values remain uncovered. Historical novelty remains uncertain after bounded searches.

Next: freeze and replay a clean archive. Do not enlarge sampling within this already proved subclass. A further advance requires a new mechanism outside these two pair-graph families or a sharper arbitrary-factor theorem.
