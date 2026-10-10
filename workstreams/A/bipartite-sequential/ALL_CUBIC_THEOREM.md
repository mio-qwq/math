# Sequential edge orderability for all cubic graphs

**Primary-source scope.** Aleksandra Gorzkowska and Jakub Kwaśny, *Distinguishing adjacent vertices by ordering edges*, arXiv:2609.11832v1, 10 September 2026, Conjecture 10, https://arxiv.org/html/2609.11832v1 . Checked 2026-10-10. Their paper proves the fixed-proper-colouring assertion for connected nonregular graphs, class-two graphs, and connected d-regular graphs for d>=6; it leaves the d=3,4,5 class-one cases open. This note gives a constructive **positive proof for the entire d=3 case**. With the source's already-proved Theorem 5, it also settles Conjecture 10 for connected subcubic graphs. It is not a counterexample, not the d=4 or d=5 proof, and has **not** yet been independently accepted by ROOT or checked with Lean. Bounded external literature search did not locate this proof; no novelty or priority is asserted.

## Exact original definitions

For a finite simple graph G, fix an **arbitrary proper** edge colouring w:E(G)->C. For one **global total order** ≺ of E(G), let f(v) be the sequence of colours of the edges incident with v, read in increasing ≺ order. Sequential orderability means that f(u) differs from f(v) **for every edge uv**. The edge colours are never changed during the construction.

## Theorem A (all fixed proper three-edge-colourings of cubic graphs)

For every finite simple cubic graph G (connected or disconnected) and every fixed proper edge colouring w:E(G)->{0,1,2}, there exists a total order ≺ on all of E(G) such that f(u) != f(v) for every uv in E(G). The order is constructible in polynomial time.

### Step 1: alternate even cycles and a perfect matching

Every vertex has exactly one incident edge of each colour. The union of colour-0 and colour-1 edges is therefore a disjoint union of **even cycles** C_1,...,C_k, each of length at least four because G is simple. The colour-2 edges form a perfect matching M (possibly joining vertices in different cycles).

### Step 2: choose a root on every cycle, no roots joined by M

We need a set R that chooses exactly one vertex from each C_i but whose vertices are pairwise nonadjacent in M.

Take **any two distinct vertices** a_i,b_i of each C_i. On the selected 2k vertices form an auxiliary graph with two types of edges: all candidate-pair edges a_i b_i, and those colour-2 matching edges of M whose endpoints are both selected. Each type of edges forms a matching. Every auxiliary cycle alternates between these two matchings and thus has **even length**. Hence the auxiliary graph is bipartite. Two-colour it; choose all auxiliary vertices of colour zero. The chosen set R contains **exactly one** endpoint of each candidate pair (and thus one root per C_i), and no edge of M has both endpoints in R. This is a constructive independent-transversal lemma, using only the elementary bipartiteness of the union of two matchings.

### Step 3: define one global edge order

Fix any ordering of the cycles. For each C_i rotate and orient its cyclic vertex list as (v_0,...,v_{m-1}) such that v_0 is the selected root of C_i and the outgoing edge e_0=v_0v_1 has colour 0. This orientation always exists: at v_0 the two cycle neighbours have colours 0 and 1. Label cyclic edges e_j=v_jv_{j+1} for j<m-1 and e_{m-1}=v_{m-1}v_0. Their colours alternate w(e_j)=j mod 2.

Initially order all cycle edges in consecutive blocks:

    e_0(C_1),...,e_{m_1-1}(C_1),e_0(C_2),...,e_{m_k-1}(C_k).

Insert each matching edge xy in the single slot **immediately after** the outgoing cycle edge e_j at one designated endpoint v_j, as follows:

- If either endpoint is a selected root, designate that root (the two endpoints cannot *both* be roots).
- Otherwise designate the endpoint that appears first in the lexicographic order (cycle block index, local vertex index).

Since M is a perfect matching, every vertex designates **at most one** matching edge, so no two insertions request the same slot. This makes a well-defined **single total order** of all E(G) without changing the fixed colouring.

### Step 4: inspect the exact induced sequences

For every root v_0, its matching edge appears after e_0 but before e_{m-1}. Consequently,

    f(v_0)=(0,2,1).

For a nonroot v_j, 1<=j<=m-1, its two cycle edges are e_{j-1}<e_j. The matching edge at v_j lies **either before both or after both**, never between: if designated at v_j it lies after e_j. If designated at another vertex in the same cycle, that vertex necessarily has smaller local index at most j-2, since M cannot duplicate either of the two cycle edges; its insertion precedes e_{j-1}. If designated in a different cycle, the whole foreign cycle block is earlier or later. Thus the nonroot's colour 2 is in **first or last** position, never middle.

Every matching edge is safe. If one endpoint is a root, it has colour 2 in the middle and the other endpoint has colour 2 first or last. Otherwise, the matching edge is inserted after the later cycle edge at its earlier endpoint, making colour 2 **last** there, but before the earlier cycle edge at its later endpoint, making colour 2 **first** there (within a cycle, the two endpoints cannot be adjacent, and their indices differ by at least two; in different cycles the block order makes this automatic).

Every cycle edge is safe. For e_0 and e_{m-1}, one endpoint is a root with colour 2 in the middle and the other is a nonroot with colour 2 first/last. On all remaining cycle edges e_j (1<=j<=m-2), the endpoint v_j sees colour 0 before 1 exactly when j is odd, whereas v_{j+1} sees the opposite order. Inserting colour 2 cannot change the relative order of 0 and 1, so their three-term sequences differ.

Every edge belongs either to M or to one of the cycles, so every edge is safe. This proves Theorem A. QED.

### Corollary B (the full cubic and subcubic cases of Conjecture 10)

Let G be a connected finite simple **cubic** graph and w **any** proper edge colouring, possibly using >3 globally distinct colours. If exactly three colours are used, relabel them and apply Theorem A. Otherwise, since each vertex has a three-element incident-colour palette, connectedness forces at least one edge between vertices with unequal palettes; the **already published Theorem 5 of Gorzkowska–Kwaśny** then gives a good order. Thus **every proper edge colouring of every connected cubic graph is sequentially orderable**.

Combining this new d=3 case with the original paper's results for nonregular graphs and degree-two graphs shows its Conjecture 10 for **all connected graphs of maximum degree at most three except the stated K2/even-cycle exceptions**. The d=4 and d=5 regular class-one cases remain unresolved by this proof.

## Reproduction and evidence boundaries

Command from the repository root:

    python3 workstreams/A/code/verify_cubic_factors.py

This standard-library script reconstructs every matchings-and-even-cycles instance in ten partitions, selects roots via the auxiliary two-colouring, constructs the actual ordered edge list, and independently recomputes every vertex's sequence and every edge inequality (without trusting the proof's first/middle/last analysis). Exhaustive run on Python 3.13.5 yielded:

    PASS all cubic 2-factor+matching instances: {'(4,)': 1, '(6,)': 4, '(8,)': 31, '(10,)': 293, '(12,)': 3326, '(4, 4)': 33, '(4, 6)': 292, '(4, 8)': 3327, '(6, 6)': 3328, '(4, 4, 4)': 3329}
    PASS incomplete-order negative test

These are **13,964** exact finite instances. Their success is a regression, not a finite-to-infinite inference; the mathematical proof covers all graph orders. The output is a newly reconstructed unsigned worker-branch result, pending an independently frozen source/hash, independent ROOT mathematical reconstruction and wider plagiarism/prior-art screening. It does not modify any public project root or other agent's files.
