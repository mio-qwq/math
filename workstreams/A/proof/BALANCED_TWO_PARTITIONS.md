# Simultaneously balancing two partitions by an Eulerian orientation

**Agent A · 10 October 2026 · mathematical and proof-engineering note — independent ROOT review pending.**

This strengthens the Hall-transversal and bichromatic splitting arguments used in the Gorzkowska–Kwaśny Conjecture 10 project. The Eulerian orientation construction is classical and **not claimed as historically novel**. It does not modify the original independently written-PASS freeze at 7168f6df66ba5518cd3420c4668eab5352e4be8c. No Lean compilation or axiom audit is claimed.

## Theorem: simultaneous discrepancy at most one

Let X be any finite set, possibly empty, with two partitions P={P_i} and S={S_j} into nonempty, pairwise disjoint blocks. There exists a map c:X→{red,blue} such that every block B in either partition satisfies

    | |B ∩ red| − |B ∩ blue| | ≤ 1.

An actual deterministic O(|X|)-time and O(|X|)-space construction exists. No minimum block-size assumption is needed. Singletons optimally have discrepancy one.

### Lemma: balanced orientation of an undirected multigraph

Every finite loopless undirected multigraph admits an orientation with |outdeg(v)−indeg(v)|≤1 at each vertex, counting all parallel edges as separately labelled edges.

**Proof.** Add one artificial vertex * and connect it by a separate artificial edge to every original odd-degree vertex. The number of odd-degree vertices is even by the handshaking lemma, so all augmented degrees, including deg(*), are even. Orient each Eulerian connected component along an Euler circuit. Every augmented vertex has equal in-/outdegree. Delete artificial edges. Original even-degree vertices remain balanced; original odd-degree vertices lost just one edge and have discrepancy exactly one. Isolated vertices are already balanced. QED.

### Proof of the partition theorem

Build a bipartite **multigraph** H with one left vertex p_i for each P-block and one right vertex s_j for each S-block. Every x∈X is a distinct **labelled edge** joining the uniquely containing p_i and s_j; retain parallel edges when an intersection has multiple elements.

Take a balanced orientation of H. Colour x red if its incidence edge goes P→S, otherwise blue. At each P-block vertex the red incident edges are precisely its outedges; at each S-block vertex the red incident edges are its inedges. Hence the count difference between red and blue is |outdeg−indeg|≤1 at *every* vertex, and incident edges correspond bijectively to the original elements of that block. QED.

## Quantitative strengthening of the component-avoiding transversal

If all P- and S-blocks have size≥2, then each block has at least one red and blue element. Select **exactly one red element** from each P-block to form R. Every S-block has at least floor(|S_j|/2) blue elements, none selected. Therefore

    |S_j \ R| ≥ floor(|S_j|/2) ≥ 1.

Taking S to consist of the connected-component vertex sets of the remaining-colour graph Q (which has no isolates in the d≥3 uniform-palette case) supplies the needed root transversal for the original full graph theorem. Its separate root ordering and single-global-edge-order proof remain unchanged.

The constructive method uses adjacency lists. The augmented graph has O(|X|) vertices and edges because every partition block is nonempty. Euler traversal via Hierholzer and orientation take O(|X|) time and space. It does not require Hall matching and is conceptually independent of the earlier alternating-cycle/forest 2-colouring proof.

## Exact executable evidence

Source files:
- workstreams/A/code/balanced_partitions.py — labelled incidence graph, dummy edges, Eulerian orientation, and literal independent per-block discrepancy checker
- workstreams/A/code/verify_balanced_partitions.py — all partition pairs for n=0…6, independent brute existence for n≤4, seeded larger cases and negative controls

Actual Python 3.13.5, standard library only:

    PASS exhaustive two-partition pairs: {0: 1, 1: 1, 2: 4, 3: 25, 4: 225, 5: 2704, 6: 41209} total 44169
    PASS extra seeded n=7..80: 2738 100000-singleton stress PASS
    PASS parallel-incidence, wrong-certificate, six malformed/singleton negative controls

These are **test runs**, not pairwise nonisomorphic structures or a substitute for the exact argument. The simultaneous discrepancy theorem is an application of classical Eulerian graph orientation, not a historical originality claim. This packet still needs an uninvolved mathematical review and a real Lean compiler/axiom audit before making any formalization claim. No project number, merge, submission, author contact or automation is authorized or claimed.
