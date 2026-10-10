# An exact global-order constructor for arbitrary properly edge-coloured simple graphs

**Original research statement:** Gorzkowska and Kwaśny, *Distinguishing adjacent vertices by ordering edges*, arXiv:2609.11832v1 (10 September 2026), https://arxiv.org/html/2609.11832v1 , Conjecture 10. **Attribution:** The component algorithm for unequal adjacent colour palettes is an implementation of the ORIGINAL AUTHORS' Theorem 5; it is **not** a newly discovered proof of that step. The uniform-palette regular algorithm uses A's complete constructive theorem reviewed at immutable commit \`7168f6df66ba5518cd3420c4668eab5352e4be8c\`. ROOT accepted its original written mathematics independently, but execution/Lean/priority are separate. This new note is a computational corollary and original-definition regression; not a peer-reviewed source or historical-firstness claim.

## Corollary: exact obstruction classification even for disconnected graphs

Let G be any finite simple graph and let w be a **fixed proper edge colouring** on E(G). There exists one global total order of E(G) whose induced incident-colour sequences distinguish the endpoints of **every** edge if and only if the graph has **no connected component** that is either:

1. exactly \(K_2\); or
2. an even cycle on which the given edge colouring uses exactly **two** colours.

Thus isolated vertices and disconnected graphs are allowed. A cycle coloured with three or more global colours is **not** an obstruction, including when the underlying cycle is even.

**Necessity.** An isolated K2 edge produces the same one-term list at both endpoints in every global edge order. In a properly two-coloured even cycle, consider its **earliest edge among edges of the cycle** in the proposed global order. Its two endpoints each have that edge first among their incident cycle edges, and their other incident edges both have the same second colour. Hence these adjacent endpoints receive the identical two-term sequence. Interleaving unrelated component edges does not affect either local sequence.

**Sufficiency.** For every nontrivial connected component not of these types: either its adjacent palettes differ, in which case the original authors' Theorem 5 supplies a constructive order; or every palette is identical. In the latter case connectivity implies regularity and exactly d global colours. For d≥3 the full uniform-palette construction in ALL_DEGREES_THEOREM.md supplies one order. For d=1 the component is K2, contrary to the assumption. For d=2 the connected component is an even cycle with exactly two colours, also excluded. Singleton components require no edges. Concatenate the resulting componentwise orders in any order. They form a **single** global order and preserve all local sequences. QED.

This is a direct disconnected corollary of the complete original connected conjecture, **not** a separate solution to an unrelated open problem.

## Faithful executable implementation of the two proof mechanisms

Run with standard-library Python 3.13+ from the root of the GitHub repository:

    python3 workstreams/A/code/construct_full_graph.py input.json

JSON input:

    {"n":4,"edges":[[0,1,0],[1,2,1],[2,3,0],[0,3,2]]}

Colours may be JSON integers or strings. Each undirected edge appears once, endpoints are 0..n−1, loops and parallel edges are forbidden. The input must be **properly edge-coloured**; the program checks this itself. On success, output includes the explicit full original-colour ordered edge list and the exact original-definition postcondition \`verified: true\`. If an exceptional component is present, it reports a structural obstruction. The graph is never recoloured. The regular case depends on the original frozen \`verify_all_regular.py\` in the same directory.

### Case I: unequal adjacent palettes (original authors' constructive Theorem 5)

Fix any vertex v and let A consist of all vertices whose incident-colour palette equals that of v. Let M be all edges between A and its complement: these edges are automatically safe, since their endpoint palettes differ. Delete M; each resulting component Q has at least one boundary edge in M (connectivity). Order M arbitrarily once and for all. For each Q, reserve every boundary edge after its earliest one as a fixed suffix, then process a spanning tree of Q leaves-first, greedily inserting still-unordered incident edges before the suffix. Every nonroot x has at least one unordered tree edge to its unprocessed parent. The parent edge has \(\deg_Q(x)\) distinct positions among the other Q edges incident with x, all producing distinct sequences by properness. At most \(\deg_Q(x)-1\) neighbours are already processed, so one position avoids all forbidden neighbour sequences. The root has \(\deg_Q(r)+1\) positions for its earliest boundary edge but only \(\deg_Q(r)\) internal neighbours. This is exactly the greedy invariant of the source Theorem 5.

The Q-local total orders agree on the relative order of their shared boundary M edges; combine them with the fixed M order into **one** global total order. In implementation, every internal Q edge is placed in the gap after its preceding M edge in the Q-local order, so all Q-local edge comparisons and every local vertex sequence are preserved. Since every M edge is safe, every edge of G is distinguished.

### Case II: all adjacent palettes equal

In a connected component all palettes then agree. The component is d-regular, using exactly d colours. For d≥3, canonically biject the **given** colour labels to 0,...,d−1, run the full regular constructor, and map the output colours back by the inverse bijection. This is merely renaming of labels to run the algorithm, not a change of the fixed edge colouring. It preserves equality and inequality of vertex sequences. For d<3 the only nontrivial cases are exactly the two obstructions.

## Actual independent testing and boundary

A local **prototype with the same two mathematical mechanisms**, using the explicit original-definition endpoint checker \`independent_validate\`, was run with Python 3.13.5 on 2026-10-10. Regression command: \`python3 verify_full_graph.py\`. It checked 25,204 graph/colouring inputs; **24,070** produced complete valid orders and **1,134** correctly reported exceptional components, plus five deliberately invalid input controls. It exhausts all simple graphs on up to five labelled vertices under two deterministic proper colourings each; six-vertex and larger portions are deterministic-seed bounded samplings. The 24,070 successful inputs are *tests*, not asserted pairwise nonisomorphic graphs. The exact prototype source was kept locally; the worker GitHub revision is a shorter refactoring of that successful implementation, so a **new ROOT replay against its own exact Git blob** is required for formal execution acceptance. Do not silently transfer a local prototype's stdout receipt to an unrun refactored source.

Files:
- \`workstreams/A/code/construct_full_graph.py\`: shipped generic constructor.
- \`workstreams/A/code/verify_full_graph.py\`: shipped original-definition graph/colouring regression, with negative tests.
- \`workstreams/A/code/verify_all_regular.py\`: frozen uniform-palette regular constructor; never patched as part of this extension.

**Result status:** the mathematics is a straightforward corollary of previously independently accepted written results and the cited source theorem, but the new unified software revision needs a fresh source-hash-bound execution receipt. Neither this corollary nor the code is a universal Lean proof, an independent ROOT software acceptance, or a historical novelty certificate.

## Deterministic complexity and next step

The uniform-palette regular algorithm has an \(O(n+m)\) implementation when colours are indexed 0..d−1, as explained in \`paper/ALGORITHM_AND_COMPLEXITY.md\`. The straightforward local list-insertion and filtering implementation of the distinct-palette case is polynomial time; conservatively it admits an \(O(n+m^3)\) bound on each finite input (without relying on undocumented Python optimizations). A more efficient source-Theorem-5 implementation may be pursued only after a verified baseline.

Highest-priority next stage: independent replay of the newly committed exact bytes; then formal Lean graph/partition semantics of the component-avoiding transversal and the global edge-list construction when a compiler is actually available. No new external conjecture is reserved by this direct extension. No merge, author contact, submission, scheduler or new project number is authorized or claimed.
