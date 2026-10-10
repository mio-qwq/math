# Diameter-two truncation-at-five review packet

B,2026-10-10 11:49UTC. Baseline3b473b165596630c5cfd9b43d3996b03e3792332. Complete computer-assisted universal PARTIAL theorem for original product Conjecture3/preprint2.10. Independent review pending; no Lean/firstness claim.

The reduction is in DIAMETER_TWO_FIVE_PROOF.md. Scope: all finite connected factors of diameter<=2, arbitrary orders; lower bound min(5,gp^-G,gp^-H). Distinct from complete line/Kneser subclasses, and not a resolution for both factor parameters>5 or larger diameter.

Actual Python3.12.14 stdlib commands:
- python workstreams/B/lower_gp_product/probe_four_signatures.py
- python workstreams/B/lower_gp_product/verify_four_signatures.py

Both PASS the finite nonexistence test. Discovery uses127partition/graph models and recursive minimal transversals; separate verifier directly enumerates729pseudomatrix candidates, all profile subsets,1629minimal hitting sets,3956GP product models and522residual obstruction checks. No discovery imports. Actual35838original-adjacency BFS entries validate metric/profile meanings;3negative controls reject invalid triangle, collinear GP and duplicate extension. Certificate stream SHA256b02156e35e07a714fd7be38b168c1108a51784c867755c5322a222f040a18710. All logs included.

Proof SHA256594c61aae6ab0262a100780d76e73d01e3847857407a59e34cb5670519a879a9
Verifier SHA2566801217b06acd6d31d565f3fa89e368f50c616ae0eef1c5ffe136d24a1e9823d
Discovery SHA256cec07266af63f90edac5e34865a5c199c4d1b91d04205f0d8adcd2d3d12fe296

Audit the necessity of every maximal-landmark-GP demand, all repeated-coordinate cases, positivity for a new product vertex, and why selecting a minimal subset of actual A-profiles is exhaustive. Unordered model pairs are legitimate only because the factors are interchangeable and both use the same complete127-model list. Realizability of arbitrary profile systems is NOT assumed. The auxiliary BFS realization graphs are not claimed to have large lowerGP.

Discovery found no feasible local system; no failed candidate was suppressed. An initially trivial arithmetic negative control was replaced before freeze by an explicit corrupted three-point metric checked by the same metric predicate. The certificate output did not change. The finite verifier is part of the mathematical proof; calling it independent-definition does not mean an independent person reviewed it.

Next: freeze and clean-archive replay. A larger-diameter or arbitrary-metric extension requires genuinely new profile coverage; do not claim it from the diameter-two certificate or repeat the closed computation merely to add counts.
