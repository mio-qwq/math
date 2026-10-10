# Distributed researcher B: handoff stage

- ID: B. Role: independent discovery, with separate internal mathematical review.
- Branch: partner/dist-B. Exclusive path: workstreams/B/.
- Baseline main SHA: 42a30d62d084a9dbe64c92666addd6cf28986b16.
- Coordination: coord/distributed returned 404 and no task card was accessible. Initial remote checks exposed only main. Unknown files preserved; no global management files repaired.
- Primary outcome: complete written proof of the original consecutive-generator circulant general-position conjecture after Theorem 3.3, arXiv:2604.15909v1. This is NOT a counterexample.
- Scope: all integers 1<=d<n; exact formula and all boundary cases in circulant/PROOF.md.
- Frozen corrected local source: 10c34c12b8ded555a953f75546f965cdf5a94151; proof SHA256 8003f03393834d7ee763b6e182a05de06fcc85ff208f50caaae1c2d9a528e30b.
- Actual evidence: written integer proof; direct BFS checks of 6,884,676 anchored triples across 3,346 graphs; independent internal audit and checker receipts under audit/. Read audit verdict rather than treating a requested review as completed.
- Literature: original coauthors' August 2026 survey still describes the bound as conjectured optimal. Bounded search found no prior resolution. Historical novelty unestablished.
- Earlier route: local-girth packing coloring paused after 95,165 checked SAT instances; no counterexample, no general theorem. See search/RESULT.md for exact coverage and restart conditions.
- Rejected candidate: nonsingular graph-energy bound already publicly reported proved in arXiv:2608.22139v1.
- Publication history: first claim 000f05222cc65398f21c7bbca3673db43e292d6d; route-change claim 6e5f9b5776ea0fa66fb9e23c45abe762950ce0c2. Shell push lacked credentials, connector publication succeeded. No other distributed member was directly notified.
- Remaining: main-Agent independent acceptance, human responsibility review, final prior-art review, optional Lean formalization. No submission, author contact, merge, new numbered project, or priority announcement performed.
- Next: use HANDOFF.md to reproduce and accept or identify a concrete gap. Do not repeat brute-force searches superseded by the general proof.

## Continued work and task-card receipt, 2026-10-10 05:16 UTC

- Read BRIEF and B card at coord/distributed cdbc7b6883cea32e21505ccf1b1d9ec72e8f924f. ROOT's recorded receipt of628cb35 is observed; acceptance remains pending. No direct peer communication is inferred.
- Circulant proof unchanged, including its exact frozen content hash.
- New mechanism on the already-reserved packing question: complete short-cycle structural reduction plus four universal path/cycle tiles handles arbitrary odd/even connector lengths and triangle/square/leaf caps. This is an affirmative original-conjecture proof candidate, NOT a counterexample.
- Frozen packing source: local29d3e9b472c1b05d6cc9d8268af36053cb5508c4, proofSHA2562ac000076874fefed2bd3cf15e983fcbae6b8f1672952229c79957665e5dbb94.
- B directly checked the universal argument, added a separate original-definition graph/coloring checker, ran seven positive boundary examples and five rejected negative controls. See packing_extension/B_SELF_REVIEW.md. No repeated95165-case search.
- Earlier helper review was stopped before its final report; partial computed evidence is retained under packing_review/. Do not mark it completed independent acceptance. Subsequent core reasoning is done directly by this B instance, per the user's B-only request.
- SOURCE_GATE.md records both actual targets, known even-connector overlap and literature limits.
- Pending: main-Agent independent review, human responsibility review and historical novelty. No Lean or signed commit claim. Current GitHub API publication is unsigned; controlled signed release remains unmet.
- Next: deliver the second frozen candidate for acceptance, retain earlier versions, then choose a genuinely distinct question only after a new source gate and public reservation.

## New exact reservation, 2026-10-10 05:21 UTC

- B reserves the permutation-digraph optimality conjecture immediately after Theorem 3.6 of Chandran et al., arXiv:2604.15909v1, Section 3.3: for k >= 3 and d >= 2k, gp(Pe(d,k)) is conjectured equal to 2(d+k-2)_(k-1).
- This is distinct from the completed circulant conjecture in Section 3.1 and from A/C/ROOT's visible reservations. The current BRIEF was checked again; no conflicting reservation was visible. A new numbered root project is not allocated.
- Source definitions: vertices are length-k words of distinct letters over an alphabet of d+k symbols; each arc drops the first letter and appends a symbol absent from the entire old word. General position uses directed geodesics.
- Low-cost derivation suggests a possible three-terminal-symbol improvement over the source's credited two-symbol construction. First exact target is d=6,k=3: a 90-word set against the conjectured value84. This is a candidate, not yet a completed verification or priority claim.
- Primary version and August2026 survey still state the conjectured optimality. Exact-ID/formula/permutation follow-up searches found no resolution; bounded status remains nonexhaustive. Source gate will be recorded in permutation_gp/.
- Next: reconstruct all504 graph vertices and actual arcs, run integer BFS and all selected ordered-triple checks, add corrupted-certificate controls, then freeze any valid counterexample promptly. B performs this derivation and verification directly, without new research agents.


## Original-conjecture counterexample verified, 2026-10-10 05:27 UTC

- Active target: permutation-digraph optimality after Theorem 3.6, arXiv:2604.15909v1.
- Public pre-computation claim: 5ca33dee312f98dc5d03d8c8b728aa675ecd2329.
- Result: Pe(6,3) contains the explicit general-position 90-set in permutation_gp/certificate.json, exceeding the proposed value84. This IS a counterexample to the original conjecture.
- Actual original-definition checker:504 vertices,3024 arcs,8010 ordered selected pairs,704880 ordered distinct triples, PASS. All five negative controls rejected.
- Complete written proof also gives a strict improvement for every integer k>=3,d>=2k. No exact maximum or minimality is claimed.
- Frozen local proof/certificate/checker: c13da4c8f3b42f11ad45269dd3100338e116378e. Proof SHA256:6d4d128f753600bbb43783ca9c7ecf42b2c1e64eb301099fe78d291aa635d8d1.
- Role: B personally derived, implemented and self-checked this result. No new research agents. Separate checker implementation is not independent peer review.
- Post-discovery primary-source and formula-specific duplicate searches found no prior same-scope resolution; this does not establish historical novelty. See permutation_gp/SOURCE_GATE.md.
- Blockers: independent acceptance, historical novelty and human review pending; no Lean or signed release. Existing two proof packets remain unchanged.
- Next: freeze/publish this packet, enable review using HANDOFF.md; do not wait for optimum/minimality or restart superseded searches. No remote acceptance or direct notification inferred.
