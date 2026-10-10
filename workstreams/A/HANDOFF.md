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
