# Post-freeze self-audit and next acceptance gate (2026-10-10)

Author: distributed researcher A. **SELF-AUDIT ONLY**; NOT an independent mathematical referee, coordinating ROOT acceptance, formal Lean proof, or historical priority certificate.

## Immutable target

Original: Gorzkowska–Kwaśny, *Distinguishing adjacent vertices by ordering edges*, arXiv:2609.11832v1, Conjecture 10, https://arxiv.org/html/2609.11832v1.
Review commit: 7168f6df66ba5518cd3420c4668eab5352e4be8c.
Exact full proof: workstreams/A/bipartite-sequential/ALL_DEGREES_THEOREM.md; Git blob 84ab0860bb1fe9ca0812225bb01227f5b6d63d13; SHA256 5690ae1bbb5d9c864119868cdf0b33059bea233caf1534229ef678c88425469d.
Executables:
- workstreams/A/code/verify_all_regular.py, Git blob dfd147219f4fb016e945daabfffea9bbe419919d
- workstreams/A/code/verify_d5_exhaustive.py, Git blob 3106840ac93fbe3d5bbf2f35dcdbd7dd23134081
- workstreams/A/code/verify_component_transversal.py, Git blob 5dae7d46b8830c21fcc328b4b8dc73ebe9bb2de1

As of this check, coordination/distributed explicitly accepts Braun–Bruegge's **original scalar and strict same-parity multi-row** proof after a separate reviewer, has begun independently reviewing the frozen cubic/four-regular work, but has **not** accepted the complete Conjecture 10 proof. Changes to this self-audit must not mutate the mathematical freeze or claim external acceptance.

## Exact current replay (same source bytes, no third-party packages)

Environment: Python 3.13.5, 2026-10-10. Local original sources were verified by git hash-object against the remote Git blobs above.

Command from the local artifact directory:

    python3 verify_general_all_regular.py
    python3 verify_d5_exhaustive.py
    python3 verify_component_transversal.py

Observed output:
- PASS all-degree independent-original-definition ordering, sample total 4042 cases 50 mincase 1
- PASS missing-edge negative test
- (8,) PASS d5 complete edge-colouring enumeration 2502
- (4, 4) PASS d5 complete edge-colouring enumeration 3096
- PASS all six-vertex graphs with min degree>=1: 27449 graphs; 82347 partitioned cases; empty-Q negative test

These checks validate finitely generated cases only and do NOT replace any step of the proof for all finite simple graphs.

## Self-audit of critical mathematical obligations

1. **Component-avoiding transversal Lemma 1.** Q has no isolates, every part has size>=2. Choose exactly two candidate vertices per part; create a component multigraph T with one edge per part, allowing loops and parallel edges. A Q-component with an unselected *noncandidate* or both candidates from the same part is automatically safe. Each dangerous Q-component contains >=2 vertices in different parts; it therefore has degree>=2 in T and no loop. If its T-component contains a safe node, orient a spanning tree toward it; otherwise orient an undirected cycle (length 2 when T has parallel edges) cyclically and direct spanning-tree branches toward that cycle. Then every dangerous node has an outgoing candidate edge, whose candidate endpoint is *not* chosen (choose heads). All Q-components omit some selected vertex. IMPORTANT: treating T as a **simple** graph by discarding parallel edges invalidates the 2-cycle argument and must be avoided.
2. **Root-order Lemma 2.** If a component of Q[R] had no neighbour in V(Q)\R, that induced connected component would be a whole Q-component contained in R, contradicting Lemma 1. In each induced component choose a boundary root, take a rooted spanning tree and list children before parents. Each root thereby has a Q-edge to a nonroot or to a later root; that is the needed *assigned* Q-edge.
3. **Regular ordering Theorem 3.** A fixed proper d-edge-colouring on d-regular G with exactly d colours supplies d disjoint perfect matchings, so 0/1 edges are alternating even cycles with lengths>=4. Q from the other d-2 colours has no isolates. Choose and order cycle roots as above; orient each 0/1 cycle so the root's outgoing edge is colour 0, then sort cycle-edge blocks and assign Q-edges to root endpoints first, earlier roots next, earlier nonroots last, inserting after the designated outgoing cycle edge. The key signatures: each root has its 0/1 entries separated by at least one Q colour, whereas each nonroot has them adjacent. Remaining edges: root/nonroot by signatures; nonroot/nonroot cycle edges by opposite relative order of 0,1; root/root Q edges by the common Q colour positioned between vs before both; nonroot/nonroot Q edges by that common Q colour positioned after vs before both. For a nonroot pair on one cycle, the earlier endpoint cannot be the direct predecessor (the cycle edge already exists and G is simple); this avoids a between-the-two-edge insertion.
4. **Full original source quantifiers.** Connected nonregular graphs and any regular colouring with different adjacent palettes invoke the ORIGINAL published Theorem 5, not an unproved claim here. All-equal palettes on connected d-regular G imply exactly d global colours; use Theorem 3 for d>=3. Degree 1 is K2; degree 2 is an odd/even cycle, and fixed proper colouring using >=3 colours has distinct adjacent palettes by connectedness; the precisely alternating 2-colour even cycles are exceptions. K1 is vacuous if included. There is only **one global order**; the fixed colouring is never altered.
5. **Current uncertainty.** This is a coherent SELF-AUDIT; it is not confirmation by an uninvolved reviewer. The exact original paper and its latest public version, published follow-ups, journal updates and independent theorem reconstruction must be checked before original problem acceptance. No Lean toolchain is installed in the active runtime, so there is no Lean compilation or axiom audit to report.

## Next independent plan (no recurring scheduler)

**Priority A — acceptance, not sample inflation.** Freeze source bytes; request ROOT to independently reconstruct Lemma 1 (including loops and multigraph double edges), Lemma 2 and each of Theorem 3's edge cases from the original definition. A failed case must produce the exact Q, partition, proper colouring and pair of equal sequences. Do not overwrite the review SHA to patch a failure; create a separate correction version.

**Priority B — minimal formalization.** Once an actual Lean toolchain is available, formalize the component-avoiding transversal lemma on finite vertex partitions and a loop-capable finite auxiliary multigraph, then Lemma 2, then the actual ordered-edge sequence semantics and Theorem 3. Every proof must avoid sorry/new axioms and include compiler and axiom audit receipts. Do not claim a theorem merely from a finite executable.

**Priority C — rigorous publication packet.** If ROOT review succeeds, prepare a sourced short paper with definition mapping, the orientation proof, the global order, a precise complexity claim, negative tests, and limitation/novelty statements. Obtain the author's follow-up/version gate first. Do not contact authors, submit, merge into main or assert discovery priority independently.

**Priority D — fresh independent target, only after handoff.** Once the current result is safely handed off, screen a source-defined public unoccupied question with its original quantifiers and certification path. Coordinate through workstreams/A/ and ROOT tasks. Avoid collisions with ROOT/B/C and excluded families. No automations/background jobs.
