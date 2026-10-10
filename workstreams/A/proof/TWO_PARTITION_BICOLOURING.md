# Every pair of large-block partitions admits a simultaneous non-monochromatic 2-colouring

**Research status (2026-10-10):** A constructive strengthening of the independently derived two-partition Hall lemma in \`HALL_TRANSVERSAL.md\`. It yields a deterministic **linear-time** transversal algorithm, and is an alternative proof of the key component-avoiding transversal used in the complete Gorzkowska–Kwaśny Conjecture 10 proof. This result is a mathematics/proof candidate pending independent ROOT review; historical novelty is NOT certified and no Lean compilation or journal acceptance is claimed.

## Main theorem — simultaneous two-colour splitting

Let X be a **nonempty finite set** with two set partitions
\[
 X=P_1\sqcup\cdots\sqcup P_k
   =S_1\sqcup\cdots\sqcup S_m.
\]
Assume every block in both partitions has at least two elements. Then there exists a colouring \(\chi:X\to\{0,1\}\) such that for **every** i and j,
\[
 \chi(P_i)=\{0,1\},\qquad \chi(S_j)=\{0,1\}.
\]
Such a colouring can be found in deterministic time **O(|X|)** with adjacency lists.

### Lemma — minimum-degree-two bipartite multigraph edge colouring

Let H be a finite **bipartite multigraph**, including permitted parallel edges, such that every vertex has degree at least two (degree counts edge labels with multiplicity). Then its edges may be coloured 0/1 so that every vertex has an incident edge of each colour.

**Constructive proof.** Work separately in every connected component of H. Since the component is finite with minimum degree at least two, it contains an undirected cycle; if it has two parallel edges, those may constitute a 2-cycle. Because H is bipartite, every such cycle has even length (including 2). Colour the edges of one chosen cycle alternately 0,1. Each vertex of that cycle now already has at least one incident edge of each colour.

Construct a spanning forest **rooted simultaneously at all cycle vertices**. Every vertex outside the cycle has a unique parent edge in this forest, and every other graph edge is either a cycle edge, another tree edge, or a non-tree edge. Precolour every non-tree non-cycle edge with 0. Then process all vertices **outside** the cycle in a child-before-parent order. At the moment vertex v is processed, all incident edges other than its parent edge are already coloured: tree edges to children were coloured earlier and non-tree edges were precoloured. Since degree(v)≥2, at least one such edge exists. Give the parent edge the opposite colour from any one of these already-coloured incident edges. Thus v has both colours; previously processed vertices remain valid, since no previously coloured edge is changed. Cycle vertices remain valid because their original two differently coloured cycle edges are never changed. Every edge is eventually coloured. QED.

### Deduction for two partitions

Create a bipartite multigraph H whose vertices are the first-part symbols \(p_i\) and second-part symbols \(s_j\). Every element x∈X gives one **labelled edge** between its unique containing blocks \(p_{i(x)},s_{j(x)}\). The resulting H is bipartite and each vertex has degree equal to the size of its corresponding partition block, hence ≥2. Parallel edges correspond to multiple original elements in the same intersection; they must NOT be collapsed.

Apply the preceding lemma to colour each edge 0/1 and transfer the edge colour back to its element x. Every partition block sees both colours by construction. This proves the theorem. QED.

### Immediate component-avoiding transversal corollary

Choose exactly one **0-coloured** element from each P block to obtain a transversal R. Since each S block contains at least one **1-coloured** element, \(S_j\nsubseteq R\) for every j. Taking S to be the connected-component partition of the remaining-colour graph Q of a d-regular properly coloured graph, with d≥3 ensuring Q has no isolated vertices, recovers the graph-specific root-selection lemma. The rest of the already accepted original Conjecture 10 proof, notably ordering roots and producing a SINGLE globally consistent edge order, is unchanged.

## Complexity and exact proof boundaries

The labelled incidence graph has \(k+m\le|X|\) vertices and exactly \(|X|\) edges, because all blocks have size≥2. Its connected components, depth-first even-cycle detection, multi-source breadth-first forest and child-before-parent edge-colouring all take time \(O(k+m+|X|)=O(|X|)\) and the same space. There is no bipartite matching computation and no reliance on the external Hall theorem. In contrast, the already established Hall argument uses a more direct cardinality inequality and the classical matching theorem, which can be easier to formalize with existing Mathlib.

This 2-colouring assertion is stronger than the previous component-avoiding transversal because it simultaneously splits **every block of both partitions**, not merely avoiding full S blocks after choosing exactly one P element. The assumptions are essential in general: singleton blocks cannot contain both colours. The empty-universe case is trivial if separately allowed but is intentionally excluded by the statement.

## Independent original-definition verification

Independent standard-library Python:
- \`workstreams/A/code/linear_split.py\`: labelled incidence multigraph with preserved parallel edges; DFS cycle extraction, 0/1 alternating cycle colouring, multi-source BFS forest, reverse-order parent-edge colouring, literal two-colour postcondition.
- \`workstreams/A/code/verify_linear_split.py\`: all partition pairs with block sizes≥2 on n=2,...,8 plus deterministic larger pairs; direct rebuilding of every P and S block's encountered colours; independent brute-force colouring-existence checks for n≤6; repeated intersection/parallel edges, safe blocks and four invalid-condition controls.

Actually executed with Python 3.13.5, standard library only:

    PASS 541389 bipartite-multigraph partition pairs, both colours in EVERY block; safe transversal verified; parallel/loop-equivalent/negative cases PASS

This finite result is regression evidence, **not** a proof for arbitrary |X|. The mathematical proof above is exact. No claim of completed Lean theorem, independent ROOT acceptance, external historical novelty, paper submission, author contact or merging has been made.
