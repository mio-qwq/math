# B reservation: terminal-set existence

2026-10-10 10:54UTC. Original Eartha Kruft Welton, Sharif Khudairi, James Tuite, Lower General Position in Cartesian Products, arXiv2404.19451v1 (30April2024), **Conjecture3.3**. Final Communications in Combinatorics and Optimization10(1)(2025),110–125, DOI10.22049/cco.2024.29171.1879, **Conjecture6, printedpage118**. Both original preprint and final publisher-format PDF read; the renumbering matters.

Primary sources:
- https://arxiv.org/html/2404.19451v1
- https://oro.open.ac.uk/98050/9/98050final.pdf
- https://profiles.open.ac.uk/j-tuite (author publication list, read earlier this session)
- https://arxiv.org/html/2501.19385v5 (2026surveyConjecture5.13)

Claim: EVERY finite simple undirected graph has a terminal set. A terminal set S is a general-position set (no three selected vertices on a common shortest path) such that EVERY u outside S is the ENDPOINT of a shortest path containing two vertices of S. Endpoint coverage makes S automatically inclusion-maximal; an arbitrary maximal GP-set is not necessarily terminal. In a connected graph the endpoint condition is equivalent to d(u,a)+d(a,b)=d(u,b) for some distinct a,b in S, or the reversed a,b. Disconnected graphs can be handled componentwise, so a connected graph with no terminal set suffices to refute the original claim.

Prior coverage: every graph on at most11vertices was already tested; diameter<=3, cographs and chordal graphs have published existence proofs. Bipartite graphs and graphs with a bridge have a terminal edge, by the distance parity/bridge observation already used in the source. Cycles and wheels also have stated constructions. Do not rebrand these families or finite samples as new results. An isometric-minimal counterexample has no simplicial vertices, clique cutset, or twins, by the source's Lemma3 (preprintLemma3.4).

Multi-round exactidentifier, exactclaim, author/title, counterexample/proof/2026 searches on10October2026 found no same-scope later resolution or erratum. The2026primary survey continues to pose the conjecture. This is a bounded status gate, not historical-firstness certification; generic terminal sets in cuts/optimization are unrelated, and MathDB summaries are not used as original definitions.

Ownership refresh10:53UTC: coord abd8e856, A97b21cf, C-audit12b3a9a; no terminal-set/2404.19451 reservation in visible coordination/status. ROOT's directed orientation-spectrum problem, A's sequential edge order and C's TF questions have different quantifiers. Reserve only Conjecture3.3/final6 here, not the separate Cartesian-product lower-bound conjecture.

Initial independent mechanism: exact original-distance search on connected nonbipartite cubic graphs of order>=12 and diameter>=4, rather than repeating the source's already-covered small graphs. Use BFS, encode all forbidden geodesic triples and endpoint coverage, and enumerate all permitted subsets with a disclosed node cap. A completed exhaustive failure to find a terminal set would be a candidate; a timeout is not. An independent checker must rebuild distances and exhaust all sets or verify a complete rejection certificate. Positive witnesses are discovery evidence only, unless they lead to a complete new family proof. Stop after the diagnostic unless a candidate, structural constraint or constructive invariant justifies the next mechanism. No new subagents, no other branch changes.
