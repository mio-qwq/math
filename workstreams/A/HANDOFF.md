# Agent A — handoff to ROOT (2026-10-10)

Read STATUS.md for the task acknowledgement, exact scope and old-archive recovery gap. This branch contains a **new unsigned transport reconstruction**, not the earlier signed frozen handoff. The user explicitly requested that available results be pushed first; the GitHub connector cannot transmit an old signed commit object and the original local archive is inaccessible in this session. Do not silently attribute this new commit to the old signed SHA.

## New self-contained result

Braun–Bruegge, *Facets of Symmetric Edge Polytopes for Graphs with Few Edges*, JIS 26 (2023), Article 23.7.2, Conjecture 31, PDF p.24. Full written argument: workstreams/A/braun-bruegge-f31/PROOF.md. Exact standard-library checker: workstreams/A/code/verify_braun_f31.py. The proof addresses the original scalar binomial-sum assertion only, not the broad geometric conjectures 13/32/33/36.

Reproduce from repository root:

    python3 workstreams/A/code/verify_braun_f31.py

Actually run with Python 3.13.5 in the recovered container:
    
    PASS original=720 brute=23 transfer=1029 maxima=720 Vandermonde=209 negative-tests=PASS

Two canonical Git blob SHAs verified by refetching the worker branch through GitHub:

    eef18bb24d0ab4d6d882039e74cc72ce85f67dc2  workstreams/A/braun-bruegge-f31/PROOF.md
    c3eaaa71c9e5b9e934cd1f85a85b814089ec3a20  workstreams/A/code/verify_braun_f31.py

ROOT acceptance checklist: (1) Read the exact published definition in Proposition 22 (p.12), and the two inequalities and parity cases in Conjecture 31 (p.24); (2) independently establish the Vandermonde row-product identity, sign change including endpoints |t|=q, and the arbitrary monotone B_r weighting; (3) check that both order-sensitive substitutions are legal, or follow from symmetric T; (4) verify the final parameter 1 and 2 endpoints; (5) run code against immutable blob SHAs, inspect the negative tests. The printed explanatory inequality in the source seems to omit the +2 offset; keep this erratum observation separate from the genuine statement.

The written proof and finite regression were freshly reconstructed and executed this session. **No ROOT review, Lean formalization or novelty certificate is claimed.** A previous session reported distinct frozen signed commits, but their exact source files and cryptographic signatures cannot be recovered from this runtime. Treat this packet as a new review object.

## Next research / independent handoff

No active high-cost new claim yet. Existing reservation covers Ficarra–Moradi Question 4.2; proposed alternative Braun–Bruegge scalar result is flagged for ROOT scope acceptance. Agent A should source-gate a new disjoint conjecture and publish a separate claim/STATUS update before expensive work. Do not create project numbers, alter shared docs, or re-run large negative enumerations solely to inflate progress.


## Two new theorem packets after the initial scalar proof

1. GENERALIZATION.md — strict transfer for any t>=3 same-parity rows, uniqueness of each fixed-parity extremizer. Exact checker command: python3 workstreams/A/code/verify_generalization.py. Git blobs 6ce46c7fe426a8c62b508cc17ca308ce4591e94b and 3dc16deef1bb333e61394035a7e743b0d1e7a1a8; actually passed 2924 transfers, 499 maxima and 51 independent binary-word cases.
2. CROSS_PARITY.md — even t=2h>=4 parity-class comparison; odd/even extremum ratio increases strictly in k and tends above one; t>=8 has a single crossover starting from even dominance at S=2t. Checker command: python3 workstreams/A/code/verify_cross_parity.py. Git blobs e6695ed03c2459f5a22106f43352c6c7900f4edb and d63eb3fd2b3b836c0983b389f794b9054a8066a5; actually passed 1798 monotone-ratio comparisons, plus exact t=8 boundary examples.

Both are derived from the *scalar original Proposition 22 definition*, not claims on arbitrary multigraph facets. In particular, multiple path lengths 1 violate simple-graph distinct-path conditions. ROOT must audit that semantic scope before declaring a combinatorial polytope theorem. These additions were constructed/tested in the resumed session, without external independent review. The previous-session signed archive is still unavailable; all GitHub API transport commits remain unsigned. No automatic scheduled task has been created.


## New distinct candidate handoff: Gorzkowska–Kwaśny Conjecture 10

Original: https://arxiv.org/html/2609.11832v1 (September 2026), Conjecture 10; read full HTML including induced-sequence definition and remaining degrees. This **proposed** additional reservation needs ROOT scope approval; it does not supersede the original A task card automatically.

Positive proof (not counterexample): workstreams/A/bipartite-sequential/PROOF.md. Any fixed proper colouring of finite simple bipartite G=(U,V,E) with all degrees in U >=3 is sequentially orderable. The original class-one regular d=3,4,5 *bipartite* cases follow, but nonbipartite cases are not addressed. Checker: python3 workstreams/A/code/verify_bipartite_block.py; PASS 71 graph/colouring cases, negative controls. Proof blob a09be92dfde981b681dc3b0995bb3d7beca473da; checker blob 2a5746af6700fa24a296ab7100e24d7b559194ea.

Polynomial construction (d+1 local permutations not d!): workstreams/A/bipartite-sequential/ALGORITHM.md; checker python3 workstreams/A/code/verify_bipartite_fast.py; PASS 255 graph/colouring cases, negative controls. Blobs 4eb9fb7884aef9c4d5eb9b527220104d252750b8 and 824d523454445d0aa5c70ab885ce01094748d1cc.

Acceptance chain for ROOT: independently read the paper's one-global-order definition; verify one edge per U block at any V (uses simplicity); verify V sequences independent of within-block permutation; verify d!>d and d+1 mutually different chosen candidates for d>=3; inspect fixed colouring and negative tests; distinguish this restricted affirmative theorem from the entire conjecture. Check for prior same-scope published results before claiming novelty. These are exact source snapshots from connected GitHub API, **unsigned** commits, no third-party review and no Lean. GitHub branch publication is not equivalent to a direct message to the ROOT agent.


## Final scope addendum for this research cycle

Bipartite subcase is completely classified by combining our worker theorem with **the author's existing** results: workstreams/A/bipartite-sequential/CLASSIFICATION.md (blob 0c279f93009dcad5ea538b93575ae61eeaac87c4). Exception exactly K2 and properly **two-coloured** even cycles; even cycles with >=3 colours are orderable by the original source Theorem 5.

Independent bounded script python3 workstreams/A/code/verify_classification.py (blob c26bf0c479d661fa423d66450500d945d0534154), actual C4/C6/C8 proper 3-colouring counts (18,66,258), only 6 failures each (the 2-colourings); K2/P4 controls pass. For originally unresolved nonbipartite cubic examples, python3 workstreams/A/code/verify_small_nonbipartite.py (blob f161bce7c5c2d205b2dbc6e09962f17d3fd2057b) covers all 6 legal 3-edge-colorings each for K4 and the triangular prism; all succeed. This limited negative search is not an upper bound or universal proof. Important true remaining unknown in this packet: 3-,4-,5-regular **nonbipartite** graphs under arbitrary fixed proper d-edge-colouring.

The previously published signed local archive is not available in this environment. This latest state is consistently **unsigned transport / pending ROOT independent review**. It is not a direct inter-agent message and does not assert receipt or acceptance. No scheduled tasks were created.


## Frozen high-priority cubic-class theorem packet, 2026-10-10

Review commit: 6bf3683b544e2e18694012cf05588245c36004d8.
Written proof: workstreams/A/bipartite-sequential/ALL_CUBIC_THEOREM.md (Git blob 8c54efb2d1b5930d951b5e7ee01e4b9f806aa302).
Executable original-definition check: workstreams/A/code/verify_cubic_factors.py (Git blob 94fba67e833b6a6488dd5159662d22f9962d83e0).

Run from the repository root with Python 3.13:

    python3 workstreams/A/code/verify_cubic_factors.py

Actually executed under Python 3.13.5:
PASS 13964 all-cubic coloured instances in ten cycle partitions; incomplete-edge-order negative test PASS. Actual executed script matches the remote Git blob hash.

ROOT independent review checklist: (1) read source arXiv:2609.11832v1, Conjecture 10, source Theorem 5 and degree-two exceptions. (2) Prove an independent-root transversal exists: choose two candidate vertices per colour-0/1 cycle, add one pair edge and any matching edges within the candidates; the union of two matchings is bipartite. (3) Check every root has colour-2 in middle and every nonroot has colour-2 first/last under the specified single total edge order. (4) Check all colour-2 matching edges and colour-0/1 cycle edges; no edge recolouring. (5) Verify fixed proper colourings using globally >3 colours reduce via original published unequal-palette theorem. (6) Run stdlib exact checker and omitted-edge negative test; regenerate small graphs independently. (7) Perform source/citation/priority gate independently. The next open regular degrees are 4 and 5, not 3.

STATUS: remote unsigned transport reconstruction with precisely frozen source blobs, NOT original missing signed archive, NOT independently accepted by ROOT, NOT Lean, NOT world priority. All writes confined to workstreams/A and no main changes.


## Frozen new high-priority d=4 theorem packet (2026-10-10)

Frozen source/checker commit SHA: 12b2c09814f65a4d0bfd0a658e9563ee699c735a.
Proof: workstreams/A/bipartite-sequential/DEGREE_FOUR_THEOREM.md (Git blob c4a9c457b70ce0d49e8ade0885d4476d052d6af7).
Exact stdlib checker: workstreams/A/code/verify_degree_four.py (Git blob 77f4e54c33efc67aa59fae82faaaefc0dc89792d).

    python3 workstreams/A/code/verify_degree_four.py

Actual Python 3.13.5 run after matching Git source blob hash: PASS 4-regular complete two-factor/matching enumeration {'(8,)': 446, '(4, 4)': 504} plus nonbipartite K4xK2, 5-regular K6, negative control. No third-party packages needed.

**ROOT audit request:** (1) Read original Gorzkowska–Kwaśny Conjecture 10, Theorem 5 and their d=3/4/5 remaining scope. (2) Independently verify cited Haxell theorem t>=2Delta (see Haxell–Wdowinski 2024 Theorem 1, https://doi.org/10.1002/jgt.23085). The complementary graph Q of colours 2,3 has max-degree exactly 2; all parts from colour0/1 cycles have >=4 vertices, so the theorem applies without extra assumptions. (3) Verify single global insertion order, including two extra-colour edges after one cycle edge, and root/nonroot distinction via adjacency of colour 0 and colour 1 in vertex sequences. (4) Verify each matching edge: nonroot earlier/later endpoints have its colour after/before 0 and 1; when root present the root/nonroot type is unequal. (5) Check consequence for arbitrary proper colourings with >4 global colours invokes **published** unequal-palette theorem. (6) Distinguish all d=4 from d=5 C4-free *partial* result, and make a fresh prior-art/source gate. (7) Run checker and omitted-edge negative test; frozen bytes must remain unchanged during review.

No independent ROOT review or full Lean formalization has occurred, the transport commits are unsigned, and novelty remains unverified. The same bounds show Conjecture 10 for connected maximum degree <=4 when combined with the earlier frozen cubic packet and source established low-degree results. Remaining high-level target is the five-regular class-one case in which every two-colour factor contains a 4-cycle. No main merge, external contact or scheduler.


## 2026-10-10 — HIGHEST PRIORITY: complete source Conjecture 10 candidate (original fixed-colouring quantifiers)

**Immutable review object:** commit 7168f6df66ba5518cd3420c4668eab5352e4be8c on partner/dist-A. Mathematical proof workstreams/A/bipartite-sequential/ALL_DEGREES_THEOREM.md, Git blob 84ab0860bb1fe9ca0812225bb01227f5b6d63d13 (SHA256 5690ae1bbb5d9c864119868cdf0b33059bea233caf1534229ef678c88425469d).

**Three original-definition checking programs:**
- code/verify_all_regular.py blob dfd147219f4fb016e945daabfffea9bbe419919d
- code/verify_d5_exhaustive.py blob 3106840ac93fbe3d5bbf2f35dcdbd7dd23134081
- code/verify_component_transversal.py blob 5dae7d46b8830c21fcc328b4b8dc73ebe9bb2de1

From the repository root, with Python 3.13.5 and NO external Python packages:

    python3 workstreams/A/code/verify_all_regular.py
    python3 workstreams/A/code/verify_d5_exhaustive.py
    python3 workstreams/A/code/verify_component_transversal.py

Actually executed, 2026-10-10T09:08:16Z. Outputs: PASS all-degree 4042 complete graph-colouring orders across 50 cases, plus missing-edge negative; PASS exhaustive d=5 partitions (8):2502, (4,4):3096; PASS all six-vertex Q graphs with no isolates:27449, with three partitions:82347, plus edgeless-Q negative. Exact executed local sources were compared by git hash-object to the above GitHub blob hashes, and all 4 remote files re-fetched.

**ROOT mathematical audit checklist, independently of our checker:**

1. Read original Gorzkowska–Kwaśny arXiv:2609.11832v1, Sections 1,3–5, Conjecture 10, source Theorem 5 and cycle exceptions. Verify the exact quantifiers: finite simple connected graph, every fixed proper edge colouring, a single global total edge order with unequal induced incident-colour sequences for each edge; no recolouring.
2. Lemma 1: For any Q without isolates and any partition into parts of size >=2, choose two candidates per part. Make an auxiliary multigraph T on Q-components, one edge per part joining its candidate components. A component of Q is safe if it contains a noncandidate or two candidates of one part; otherwise each of its >=2 vertices yields a distinct incident auxiliary edge, hence T-degree>=2. Orient T towards a safe node or a cycle in every T-component, forcing every dangerous vertex to have positive outdegree. Choose the candidate at each edge head; verify every original Q-component excludes at least one chosen root.
3. Lemma 2: The Q-induced graph on chosen roots has no component without a Q-boundary vertex, else it would be a fully selected Q-component. Root a forest of Q[R] towards such boundary vertices, list children before parent. Thus every chosen root has a leftover-colour edge to a nonroot or later root.
4. Theorem 3: In a properly d-coloured d-regular graph with exactly d global colours, 0/1 edges are alternating even cycles with length>=4, Q consists of the other d-2 matchings and has no isolates for d>=3. Apply the two lemmas, order whole cycles by roots and orient each cycle starting at its root with the 0-coloured outgoing edge. Insert every remaining-colour edge after the outgoing cycle edge of (i) the unique root endpoint; or (ii) earlier root if both endpoints are roots; or (iii) lexicographically earlier endpoint if neither is a root.
5. Check EVERY endpoint type: at a root, colour 0 and 1 are separated by at least one extra colour; at a nonroot, 0 and 1 are adjacent. Root-nonroot edges distinguished by this signature. Nonroot-nonroot cycle neighbours have opposite relative 0/1 orders. For Q root-root edges the edge's extra colour occurs between 0/1 at the earlier root, before both at the later; for Q nonroot-nonroot edges it occurs after both at the earlier, before both at the later. These cases exhaust every edge.
6. Finish full Conjecture 10: for connected nonregular graphs use authors' published Theorem 5; for regular graphs with different adjacent palettes use it again. If all adjacent palettes equal, connectedness makes one global d-colour palette and the new theorem applies when d>=3. Degree-1 only K2; degree-2 proper >=3 colours are handled by original cycle analysis, while the proper two-colour even cycles are stated exceptions.
7. Repeat exact tests, independently regenerate graphs or implement a separate proof checker. Search follow-up literature/author pages and check historical prior art without assuming originality. Do not claim acceptance from our self-check or search absence.

**Review limitations:** proof is complete in written mathematics but ROOT acceptance PENDING; no complete Lean proof, no outside referee, no priority certificate, no signed GitHub transport (the old signed local archive is not accessible here). This is a positive proof of the original conjecture, not a counterexample. The source hash was frozen before these coordination edits; do not overwrite it during review. No main merge, paper submission, contact with authors, arbitrary project number or scheduled automation.


## Execution-HOLD repair, mathematically accepted theorem (2026-10-10)

ROOT task card now confirms independent complete Conjecture10 written **mathematical PASS** on original frozen SHA 7168f6df66ba5518cd3420c4668eab5352e4be8c (original proof Git blob 84ab0860bb1fe9ca0812225bb01227f5b6d63d13), but explicitly placed the **executables on HOLD**. No complete Lean theorem exists.

A completed revised replay packet is now frozen at worker-branch commit **7529211218cabae349be690ca827c34db8bb20f3**. Detailed new immutable log: workstreams/A/reviews/EXECUTION_REPLAY_V2.md.

Updated files and exact Git blobs:
- bipartite-sequential/ALL_DEGREES_THEOREM.md: faa2daa78f76dbda0d0f7629bfe37abbbab8d4c4 — same mathematics; corrected unsupported "distinct" count to 4,042 generated test runs not deduplicated.
- code/verify_all_regular.py: dfd147219f4fb016e945daabfffea9bbe419919d — frozen unchanged.
- code/verify_d5_exhaustive.py: 20197f09c231e2b6641c29abe0ca7fa8ab2da02f — import changed to verify_all_regular.
- code/verify_component_transversal.py: 7b28fc7f3d878ef3ee427e08c3ecb061759c634d — import changed to verify_all_regular.
- code/construct_order_cli.py: b6e4fd5e41547519d2f93a13ed25b2c923402392 — independent original-definition witness output/self-test.

**ROOT reproduction from a fresh clone**:

    python3 workstreams/A/code/verify_all_regular.py
    python3 workstreams/A/code/verify_d5_exhaustive.py
    python3 workstreams/A/code/verify_component_transversal.py
    python3 workstreams/A/code/construct_order_cli.py --self-test
    python3 workstreams/A/code/construct_order_cli.py workstreams/A/paper/example_k4.json

All four test commands were actually run with Python 3.13.5 in a **fresh extraction** of the 90,601-byte corrected package; each returned 0, every expected Git blob matched, including intentional negative tests. Test counts 4,042 (not deduplicated), 2,502+3,096=5,598 and 82,347 graph/partition checks. The sample K4 produces a literal six-edge order certified by its independent semantic validator. Package SHA256: 8b5d6f3a67081fa4c2191ed86dabf6c553595209023f7b980e8d3cd34e59898c. Portable zip artifact exists in conversation at /mnt/data/agent_A_conjecture10_corrected_review.zip but was not falsely claimed uploaded as a signed GitHub release.

**Please remove execution HOLD only after the coordinator's own source/import/replay verification.** Do not conflate worker replay with external execution acceptance, or mathematical PASS with a Lean proof. Original mathematical freeze was not rewritten. Do not create 007/008, merge main, submit papers, contact original authors or claim original priority. The next work is minimal Lean proof of the auxiliary transversal and root-order lemmas plus precise semantics, conditional on available toolchain.


## Formalization preparation and document export

The separate worker-owned \`paper/FORMALIZATION_INTERFACES.md\` now specifies all six necessary Lean theorem interfaces, the exact fixed-colouring/global-order semantics, the auxiliary **labelled multigraph** requirements (including parallel-edge 2-cycles), and the no-sorry compilation/axiom audit protocol. This is **not** compiled Lean; local \`lean\`, \`lake\`, and \`elan\` executables are unavailable, and the current host cannot bootstrap GitHub dependencies.

The A working paper is \`paper/WORKING_MANUSCRIPT.md\`, source attribution and independent-PASS status explicit; the local PDF pre-review export is \`agent_A_conjecture10_review.pdf\`, four inspected A4 pages. All packet files are additionally available in the portable \`agent_A_conjecture10_corrected_review.zip\` linked by the user-facing artifact; SHA256 \`8b5d6f3a67081fa4c2191ed86dabf6c553595209023f7b980e8d3cd34e59898c\`. The ZIP was genuinely extracted to a separate temporary directory and all four standard-library programs returned zero. These container artifacts are not represented as signed GitHub releases.

This handoff must continue to distinguish **independent mathematical PASS on the original source** from **pending ROOT acceptance of the corrected execution packet**. The worker will not submit/merge or assert Lean/world-priority independently.


## New full-graph constructive corollary and exact 25,204-case replay

No change to original mathematical Conjecture 10 freeze \`7168f6df66ba5518cd3420c4668eab5352e4be8c\`; no change to repaired v2 core sources. The new executable supplements those frozen proofs by implementing the published unequal-palette Theorem 5 **as well as** the independently reviewed A uniform-palette regular theorem.

- \`workstreams/A/code/construct_full_graph.py\`, exact Git blob \`b0da98d468428cb81063e31b57f02f9f290d59ab\`
- \`workstreams/A/code/verify_full_graph.py\`, exact Git blob \`8c712181eda1a6641c3bf8efeab7a2dc5a99ef60\`
- Existing dependency \`workstreams/A/code/verify_all_regular.py\`, Git blob \`dfd147219f4fb016e945daabfffea9bbe419919d\`
- Proof + source attribution: \`workstreams/A/paper/FULL_GRAPH_ALGORITHM.md\`, blob \`e57cab14c4b1121b4bf3f7a3fe5813b960ae7a09\`.
- Source-bound replay: \`workstreams/A/reviews/FULL_GRAPH_EXECUTION_RECEIPT.md\`, blob \`7239a123d6f671826e85633100dc6b6a8d27747c\`.

**Run from cloned repo root:**

    python3 workstreams/A/code/verify_full_graph.py
    echo '{"n":4,"edges":[[0,1,0],[1,2,1],[2,3,0],[0,3,2]]}' | python3 workstreams/A/code/construct_full_graph.py

All three exact GitHub code blobs were reconstructed in a new temporary directory, confirmed by \`git hash-object\` and executed with Python 3.13.5, no external packages. Actual PASS 25,204 graph/colouring tests = 24,070 generated validated global orders + 1,134 correctly identified K2/bicoloured-even-cycle exceptional-component cases, and five malformed inputs rejected. Literal K4-like example returns four ordered edges, verified true; actual subprocesses exited 0. These test runs are not claimed all pairwise nonisomorphic; the mathematical classification is a direct corollary of the original connected full theorem and the cited Theorem 5.

Conversation artifact \`/mnt/data/agent_A_full_graph_replay.zip\` (8,588 bytes, SHA256 \`3a6a4bb64e86a13f81ca6d6d7ee2f34d95137daf640c168d659f637a1f82c284\`) holds exact code and manifest. The ZIP is not a signed GitHub Release. New software and classification still await independent ROOT source/replay review; do not conflate it with original complete mathematical PASS or the older separately pending v2 execution HOLD.

**Autonomous next phase:** preserve frozen objects; pursue the first genuinely executable Lean finite-graph/labelled-multigraph orientation lemma when a toolchain is present. Independently refresh original paper/version citations, then convert the already published Theorem 5 algorithm into a standalone, explicitly attributed manuscript appendix. No new open-problem reservation or project number needed for these direct proof/algorithm extensions. Do not merge, submit or contact authors without separate authorization.
