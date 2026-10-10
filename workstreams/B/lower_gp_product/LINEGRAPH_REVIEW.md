# B self-review: complete-line-graph product subclass

2026-10-10 11:32UTC. Independent review pending. LINEGRAPH_FAMILY_PROOF.md proves the original product inequality for L(K_n) square L(K_m), ALL n,m>=2. It is a full elementary proof for this family, not an arbitrary-factor proof or a new exact product formula. The factor lowerGP formula is known and credited.

The proof is driven by the hypothetical witness size k, not a fixed graph order. The previously frozen arbitrary truncation forces k>=4. Strict factor inequalities imply n,m>=2k-1. A distinct non-GP projection contains a P4 on four symbols and consequently uses<=2k-2symbols. If only one symbol remains unused, equality forces exactly a P4 plus k-3disjoint isolated edges; k>=4 ensures an isolated edge to exploit. Pair distances1require special attention and are explicitly covered by equality of the new distances, rather than incorrectly assuming all old product distances>=2. Repeated projections are handled first or leave>=3unusedsymbols in both factors.

The proposed constructor checks the STRICT factor-parameter conditions, not just n,m>=2k-1. This matters at even n=2k, where the numerical support bound holds but the factor lowerGP equals k and extension of an arbitrary GP projection need not be possible. A negative control deliberately supplies n=m=8,k=4 and is rejected.

Actually run:

    python workstreams/B/lower_gp_product/verify_linegraph_extension.py

Python3.12.14, standard library; no discovery imports. The checker builds intersection adjacency separately, runs BFS factor distances, and checks constructed extensions by the original product metric. Each exercised construction branch also receives a full original Cartesian-adjacency BFS from a returned point; it does not silently inherit the closed factor distance formula.10,000GP sets of sizes4,5,6 across(7,7),(7,9),(9,9),(11,13) factor-symbol pairs all extend.14,320factor BFS entries and55,560product BFS entries checked. All9branches occur, including1118one-unused-symbol cases and14both-unused cases. Three negative controls cover wrong intersection/disjointness convention, duplicate extension, and non-strict factor premises.

These finite tests validate code and semantic edge cases; the universal theorem follows from the complete arbitrary-n,m,k written proof. The symbolic source ROUTE file records the discovery mechanism; there was no external-team construction or new subagent. No Lean or independent reviewer is claimed.

Dependencies: prior Di Stefano et al. factor values; elementary distance and support counting; frozen ebaa4094 universal truncated theorem (also pending review). This family proof does NOT depend on the separate computer-assisted Kneser quotient. Preserve all frozen prior proof bytes. Stop this covered family; only an explicit new mathematical mechanism should reopen work on the remaining arbitrary-factor regime.
