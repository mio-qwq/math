# C — An explicit asymmetric unstable order-five cycle-bundle witness

**10 October 2026.** Independent exact witness supporting the **positive** theorem candidate for Mizzi arXiv:2603.27559v3 **second** clause and its multi-cycle strengthening. This is **not a counterexample, a minimum-order record, a new published result, or external peer review**. The finite example illustrates that the strengthened bundle genuinely occurs under all original asymmetric/unstable hypotheses, not only in a symmetric conditional toy family.

## Graph and exact claims

File `asymmetric_order5_bundle_raw.json` freezes a complete **20-vertex, 80-edge**, loopless undirected graph as a literal edge list, not code importing its discovery script. Its four displayed TF permutation cycles are:

\[
(0\ 1\ 2\ 3\ 4),\
(5\ 6\ 7\ 8\ 9),\
(10\ 11\ 12\ 13\ 14),\
(15\ 16\ 17\ 18\ 19).
\]

The TF pair is `(alpha,alpha^{-1})` of order `5`. For full reproducibility, the original edge generator used six sets of residues mod 5 for sums across orbit pairs:

\[
S_{01}=\{0,1\},\quad S_{02}=\{1,2,4\},\quad
S_{03}=\{2,4\},\quad S_{12}=\{1,3,4\},\quad
S_{13}=\{0,1,2,3\},\quad S_{23}=\{1,3\}.
\]

Every edge `(5i+x,5j+y)` with `i<j` is present iff `x+y mod 5 \in S_{ij}`; there are no edges inside one orbit. This formula describes the frozen graph, but **the checker reads and audits the raw edge list independently**.

The three **pairwise vertex-disjoint** simple cycles are given with explicit vertex labels:

- `C3 = [0,5,11]`
- `C6a = [1,9,12,4,6,10]`
- `C6b = [2,8,13,3,7,14]`

The three cycles use **all 15 vertices** of the first three 5-cycles of alpha, exactly as predicted by the new orbit-bundle theorem with `M=5, k=3`.

## Independent validator

Run from the repository root:

```bash
cd workstreams/C
python3 check_asymmetric_bundle20.py
python3 -m py_compile check_asymmetric_bundle20.py
sha256sum check_asymmetric_bundle20.py asymmetric_order5_bundle_raw.json
```

Actually executed, CPython **3.13.5** on Linux, standard library only:

```text
PASS: {"asymmetric": true, "colour_refinement_rounds": 3, "connected": true, "disjoint_cycle_lengths": [3, 6, 6], "distinct_vertex_colours": 20, "edges": 80, "n": 20, "nonbipartite": true, "unstable_TF": true}
negative_controls_rejected: 5
```

Raw checker semantics:

1. Decode the literal edge list as a **symmetric simple adjacency relation**, rejecting loops or repeated edges.
2. Check connectedness and non-bipartiteness from graph traversal.
3. Compute graph-isomorphism-invariant **degree, per-vertex triangle counts and repeated neighbour-colour multiset refinement**. After exactly **three refinement rounds**, all **20 vertices have different invariant colours**; thus any ordinary graph automorphism fixes **every** vertex, which certifies **asymmetry** without trusting a computational isomorphism package. Also check vertex determination (all open-neighbourhood bitvectors differ).
4. Check that alpha is a permutation consisting of exactly the four specified order-five cycles, and for **all 20² ordered vertex pairs**, verify `A[u][v] == A[alpha[u]][alpha^{-1}[v]]`. Thus the original graph is **unstable** under the precise source definition.
5. Verify every cycle edge, individual simplicity, pairwise vertex disjointness and coverage of the first 15 vertices. Reject **five** deliberately corrupted inputs: edge removal, broken alpha, overlapping cycle labels, loop and duplicate edge.

The finite exact result is independent of the **networkx** exploratory generator; that package was used only to discover a candidate, not to accept the raw witness.

**Published actual-source SHA-256**:

- `asymmetric_order5_bundle_raw.json`: `270861042814e3d94b7b98640b9ae59d5541d88e6c5d0eb2fbf5cf9d0be222e4`
- `check_asymmetric_bundle20.py`: `217b43fe53c701944bc849905625c086e7aefdd85c39ade4827754cab3d360e3`

Git blob identifiers: raw JSON `719b3af7268b97dbc27f22c116fc34a2921e520a`, checker `d9713cbd8a5cbf049d822ce16f2b0704cbec8ff4`.

## Meaning and limits

This exact example is more targeted than the separate `29`-vertex heterogeneous-orbit **conditional** sample: it satisfies the actual original **asymmetric unstable** hypotheses, and the extra doubled cycle is a genuinely stronger **verified instance**. Nonetheless, one finite graph cannot establish the universal statement; the complete written mathematical proof is separately frozen as `mizzi_v3_short_proof.md` and `mizzi_v3_asymmetric_full_proof.md`. The latter's historical priority and independent ROOT review are not yet established. The first clause of Mizzi v3 (two distinct TF-cousin graphs) remains **untouched** by this proof.

**Operational direction:** Use this input as an adversarial/positive regression test for any later Lean or independently implemented review; no new larger-order enumeration is warranted solely to repeat this bundle mechanism. Existing frozen proofs and other agents' files remain unchanged.
