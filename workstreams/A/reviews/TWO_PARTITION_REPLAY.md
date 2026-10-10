# Two-partition theorem packets — exact independent replay, 2026-10-10

**Agent A, workstreams/A only.** This is a new original mathematical argument and algorithmic certificate **pending independent ROOT review**; not a Lean/kernel proof, peer review, journal acceptance, priority certificate, or correction to the frozen full Conjecture 10 proof.

## Two distinct claims

1. **Hall proof:** Given two partitions of the same finite nonempty set, all blocks size≥2, one can select exactly one element from every first-part block without fully containing any second-part block. For each first block preselect two candidates; define dangerous second blocks; use the precise double count \`2|J| <= |union_{j in J} S_j| <= 2|N(J)|\` and finite Hall matching. Choose the **other** candidate in each matched first block. See \`proof/HALL_TRANSVERSAL.md\`.
2. **Strong simultaneous bichromatic refinement:** One can instead 2-colour **all** elements so every block of BOTH partitions contains both colours. Proof: consider the *bipartite incidence multigraph* on first/second blocks with one **labelled edge per element**, so all vertex degrees≥2. In each component colour an EVEN (possibly parallel-edge 2-)cycle alternately; root a spanning forest at its vertices, precolour other nontree edges, then colour forest edges children-first opposite a precoloured incident edge. This is a deterministic O(|X|)-time construction. Choosing one 0-coloured element per first block then gives the earlier transversal. See \`proof/TWO_PARTITION_BICOLOURING.md\`.

**Exact mathematical provenance:** These are alternative proofs/strengthenings of the component-avoiding transversal lemma needed in the original complete Conjecture 10 theorem. The original written mathematical theorem was independently accepted by ROOT at \`7168f6df66ba5518cd3420c4668eab5352e4be8c\`; we neither rewrite that reviewed Git object nor infer ROOT acceptance of the new arguments. No historical firstness asserted; Hall's 1935 marriage theorem is imported with attribution.

## Exact source hashes

Review object (new files all present by worker commit \`d51cfdf5d4f5192c3deac14295fc1f5c30f81583\`):

| Code file under workstreams/A/code/ | Git blob SHA1 |
| --- | --- |
| \`hall_transversal.py\` | \`da7362d802464620d95336e573295c6338194df1\` |
| \`verify_hall_transversal.py\` | \`9e3930dcdc89770c156f367eb7fffc163090cdfc\` |
| \`linear_split.py\` | \`00eb07caf4059c3161289b38c8f8768b6ce7476a\` |
| \`verify_linear_split.py\` | \`3bb26e32e60345f6972c203a5a6c0a22275d87c3\` |

Every SHA was verified against the actual executed source via \`git hash-object\`, and the same exact blob SHA was read back from GitHub after publication.

## Freshly extracted execution

Portable user-file ZIP: \`/mnt/data/agent_A_partition_theorems.zip\`; 7,136 bytes; SHA256 \`68f5ec4006eee30f66ebf1f708d32b8b3bf4fec11ced98b43bba7059a9ffb231\`. Assembled in the worker container and then extracted into a NEW temporary directory, where all four \`git hash-object\` checks passed. Actual Python 3.13.5 (stdlib only, no network) run with exit code zero and empty stderr for:

    python3 verify_hall_transversal.py
    python3 verify_linear_split.py

Actual stdout:

    PASS all two-partition pairs n=2..8 and larger deterministic checks: 541389 pairs; dangerous cases 314852, multicomponent cases 121720; parallel/safe/invalid controls PASS
    PASS 541389 bipartite-multigraph partition pairs, both colours in EVERY block; safe transversal verified; parallel/loop-equivalent/negative cases PASS

Both verifiers enumerate every pair of set partitions with min block size two for n up to 8, plus larger fixed-seed pairs. They check literal original block membership and failure to saturate any second block. For n≤6, each has an independent exhaustive brute checker of the corresponding existence statement. The tests are not a substitute for the two exact all-n proofs.

## Lean interface and execution boundary

The pinned Mathlib commit \`d13f23b723b8a846827a245b89c10fc7d3f11612\` contains \`Finset.all_card_le_biUnion_card_iff_existsInjective'\` in \`Mathlib.Combinatorics.Hall.Finite\`, confirmed by reading exact Git blob \`9e013ce0f999e3135ec53e1abda4d178af3fa044\`. The standalone \`formal/HALL_LEAN_PLAN.md\` maps the double-counting proof to this lemma. The minimal \`formal/HallBridge.lean\` is **UNCOMPILED** and merely re-exposes an existing Mathlib Hall theorem; it does NOT formalize the full partition theorem. Current worker has no Lean/Lake/Elan toolchain. No remote paid compute was invoked.

## Review request

1. Independently prove the double-count Hall inequality and verify safe/dangerous partition cases, particularly the opposite-candidate selection and all cardinal hypotheses.
2. Separately reconstruct the bipartite incidence multigraph edge colouring with even 2-cycles for parallel edges, correct child-before-parent processing, and proof of worst-case linear time.
3. Verify that picking exactly one red element per first block preserves a blue witness in each second block, then instantiate second partition as Q-component vertex sets in original graph lemma.
4. Once accepted, formalize with pinned Mathlib Hall theorem and actual compiled graph semantics, recording diagnostic and \`#print axioms\` receipts.
5. Do not conflate this new result with the already accepted original frozen Conjecture 10, existing Python execution HOLD, historical novelty, journal submission or signed GitHub release.

All commits remain on \`partner/dist-A\`, no main merge, PR, author contact, project numbering or automation.
