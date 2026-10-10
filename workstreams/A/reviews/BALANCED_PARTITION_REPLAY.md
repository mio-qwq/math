# Eulerian two-partition discrepancy — exact source-bound replay

**Date:** 2026-10-10. **Worker:** distributed researcher A. **Review status:** new auxiliary proof/algorithm pending independent ROOT mathematical acceptance; NO Lean compilation, historical priority, signed GitHub Release, external publication, or merger.

## Theorem being checked

For **any** two partitions P and S of a finite set X (including singleton blocks), there is a red/blue colouring with

    |#red(B)-#blue(B)| ≤ 1

for every part B in **both** partitions. The proof in workstreams/A/proof/BALANCED_TWO_PARTITIONS.md uses Eulerian balanced orientations of the bipartite incidence **multigraph** whose separately labelled edges are the original elements. This is an application of classical graph theory, not a claimed world-first theorem.

When all parts have size≥2, choosing one red element from each P part gives a transversal R with the stronger quantitative certificate

    |S_j \ R| ≥ floor(|S_j|/2)

for every S-block. This is a valid replacement for the root-avoidance lemma in A's already independently mathematically reviewed frozen Conjecture 10 proof. The other lemmas in that frozen proof are not silently modified.

## Immutable source objects and exact GitHub blob IDs

All these paths lie under workstreams/A/ on branch partner/dist-A:

- proof/BALANCED_TWO_PARTITIONS.md — published in c24af31eb76da0af2e61a67021377542bf00d4a1
- proof/BALANCED_SHARPNESS.md — published in f793608989c4bdc009e22ebe06117db4868da344
- code/balanced_partitions.py — Git blob 3cb72e2517c5004014063de166129a1d07151ee0, published in 4cb6bacefb505d62d9ec676e373f61354343b408
- code/verify_balanced_partitions.py — Git blob 0dcfe750e273ccf96447f988c6d0fdbd3eb9ee1d, published in 4ae0736d5ce39772caf398f5ed61484becfdda1f
- code/verify_balanced_sharpness.py — Git blob 13a57f50c3c72bc700b15f2edab6ef146cc7027a, published in c4f91669d5bb2793232822893c9562631024b97f

The three Python files above were reconstituted as the exact remote source bytes in the worker container; invoking git hash-object on each produced EXACTLY those Git blob identifiers. The mathematical files are readable in the branch; the portable archive includes an equivalent local proof text, but its separate Markdown SHA is not represented as matching the remote proof blob.

## Actual clean-extraction replay receipt

Portable conversation artifact: /mnt/data/agent_A_balanced_partitions_20261010.zip; size 10,358 bytes; SHA256 9bce2af9f7588e656ddf04d841f568f53f5cf092aae8f78bb26bcb2245456c35.

A fresh temporary directory was created, the ZIP was extracted into it, all three Python file SHA1s were verified via git hash-object, and **both** test scripts were run using standard-library Python 3.13.5. Both returned exit code 0 and empty stderr:

    python3 workstreams/A/code/verify_balanced_partitions.py
    python3 workstreams/A/code/verify_balanced_sharpness.py

Actual stdout:

    PASS exhaustive two-partition pairs: {0: 1, 1: 1, 2: 4, 3: 25, 4: 225, 5: 2704, 6: 41209} total 44169
    PASS extra seeded n=7..80: 2738 100000-singleton stress PASS
    PASS parallel-incidence, wrong-certificate, six malformed/singleton negative controls
    PASS every two of P,S,T simultaneously split, all three impossible (16 assignments)
    PASS singleton discrepancy-one lower bound

The 44,169 cases enumerate **all pairs of set partitions up to 6 labelled elements**, not distinct graph-isomorphism classes. For n≤4 an independent exhaustive red/blue search verifies existence. The 2,738 further tests sample n=7..80 using a fixed seed; the 100k test exercises memory and stack behaviour. These finite observations do not prove the theorem for arbitrary n; the general theorem follows deductively from Eulerian orientation.

## Essential conceptual boundaries

1. Parallel edges in the incidence multigraph are **not collapsed**; each x∈X has a unique labelled edge.
2. The dummy vertex receives one edge from each odd-degree original vertex; its degree is even by the handshaking lemma. Euler traversal then balances augmented indegree/outdegree exactly. Removing a dummy edge changes the imbalance by at most one.
3. At a P vertex red counts OUT-oriented original edges; at an S vertex red counts IN-oriented original edges. Both inherit absolute imbalance at most one, which is the exact original partition claim.
4. Singleton blocks cannot generally contain both colours, but they satisfy discrepancy one; the all-block-size≥2 hypothesis is used only to derive the root-transversal corollary.
5. Three arbitrary partitions do NOT satisfy this theorem in general. On X={0,1,2,3}, perfect-matching partitions P={{0,1},{2,3}}, S={{0,2},{1,3}}, T={{0,3},{1,2}} would require a proper two-colouring of K4; all 16 assignments fail. Each pair remains splittable.
6. "Deterministic linear-time" is a standard **indexed adjacency-list RAM-model** bound. The Python reference implementation uses hash tables for arbitrary element labels, for which constant-time hash operations are expected-case rather than worst-case over adversarial hashes.

**Remaining acceptance:** An uninvolved mathematical review is requested, followed by actual Lean compilation of the finite partition/graph semantics (when a compatible toolchain is available). Root's prior independent mathematical PASS of frozen complete Conjecture 10 at SHA 7168f6df66ba5518cd3420c4668eab5352e4be8c does not itself confer acceptance on this NEW auxiliary result. Root's older execution HOLD also remains separate. No background scheduler, main merge, author contact or manuscript submission occurred.
