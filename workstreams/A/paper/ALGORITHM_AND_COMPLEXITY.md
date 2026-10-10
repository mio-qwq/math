# Constructive edge-order algorithm: interface, certificates, and complexity

**Status:** Further engineering and algorithm analysis for the frozen complete Conjecture 10 *proof candidate* (arXiv:2609.11832v1), not an independently accepted mathematical result. Frozen proof SHA: \`7168f6df66ba5518cd3420c4668eab5352e4be8c\`. Original theorem and proof are in \`../bipartite-sequential/ALL_DEGREES_THEOREM.md\`.

## Runnable output and independent semantic check

From the repository root:

\`\`\`bash
python3 workstreams/A/code/construct_order_cli.py --self-test
python3 workstreams/A/code/construct_order_cli.py workstreams/A/paper/example_k4.json
\`\`\`

The script takes JSON \`{"n":n,"d":d,"edges":[[u,v,c],...]}\`, with vertices \(0,\dots,n-1\), integer colours \(0,\dots,d-1\), each incident vertex having **exactly one edge of each colour**, and \(d\ge3\). A connected input is *not* required. Output is JSON with \`order\`, a list of every original edge exactly once, \`verified: true\`, and the number of alternating 0/1 cycles. It refuses missing/duplicate edges, loops, improper colouring and degree violations. **No recolouring occurs.**

Actual Python 3.13.5 independent end-to-end replay:

- CLI \`--self-test\`: PASS five complete graphs K4 through K12, independently checked induced sequences, deliberate missing-order-edge and 15 invalid-input controls.
- A separate implementation of the same mathematical theorem in \`/mnt/data/agent_A_paper/construct_global_order.py\` was constructed from the proof, **without importing the frozen discovery algorithm**. It rebuilt all 5,598 properly five-coloured 8-vertex instances with two-colour factors of types (8) and (4,4) and the independent original-definition verifier accepted all 5,598. This external working-container script is **not** part of the immutable Git branch: its test is a new independent code implementation, not an independent mathematical referee. The user can request the separately generated working artifact.
- The published CLI source Git blob is \`b6e4fd5e41547519d2f93a13ed25b2c923402392\`. Its hash was verified against the exact Python file that passed the CLI self-test; the original \`verify_all_regular.py\` it imports remains frozen at blob \`dfd147219f4fb016e945daabfffea9bbe419919d\`.

The output verifier checks **literal order completeness** and **full vertex incident-colour sequences**, not the internal signature conditions used to design the order.

## Deterministic algorithm (uniform-palette case)

1. Read each fixed colour class. Trace the alternating 0/1 cycles \(C_i\), each of even length \(\ge4\). Let Q consist of edges with remaining colours.
2. In each \(C_i\) mark two distinct candidate vertices. Find the connected components of Q. Create the labelled auxiliary **multigraph** T on Q-components with one edge per cycle connecting the Q-components of its two candidates. Loops and parallel edges must be preserved.
3. Mark a Q-component safe if it contains a noncandidate or both candidates of some cycle. Every other component is dangerous; it has T-degree at least two and no loop. In each T-component orient towards a safe vertex when one exists, or towards a directed cycle when none exists. Orient unused edges arbitrarily. Choose the candidate at the head of each labelled T-edge.
4. The selected roots form a transversal R not containing an entire Q-component. In each Q[R] connected component find a root with a Q-neighbour outside R and list the others by descending distance in a spanning tree from that boundary root. Each root owns an edge to a nonroot or a later root.
5. In that root order, make the list of 0/1-cycle edges, rotating each cycle so the chosen root is first and its outgoing cycle edge has colour 0.
6. Give each Q-edge to its root endpoint if exactly one exists, or to its earlier root if both exist, or otherwise to the earlier endpoint in (cycle rank, local vertex position). Insert it immediately after the designated endpoint's outgoing cycle edge. If several edges have the same designated endpoint, output them by fixed colour index.
7. Reconstruct the full induced vertex sequences and check inequality for every original edge before returning the order certificate.

The mathematical proof is in the frozen source. The new instructions are an **implementable presentation**, not a replacement lemma or a claim that the code itself proves the infinite result.

## Complexity

Let \(n=|V|\), \(m=|E|=nd/2\), and assume input colours are already integers \(0,\ldots,d-1\) with constant-time comparison/indexing. Tracing cycles, Q-components, auxiliary multigraph orientation (including 2-cycles of parallel edges), selected-root spanning forests, ownership and final output all take \(O(n+m)\) time and \(O(n+m)\) space. Rather than comparison-sort assigned edges at a vertex, place them into a colour-indexed array. Since the input proper colouring uses each colour once per vertex, this array has at most \(d\) slots per vertex. Its total size is \(nd=2m\), allowing **worst-case deterministic \(O(n+m)\) time and space** for the uniform-palette construction. This is an algorithmic strengthening of the frozen paper's conservative *polynomial time* bound.

If colour labels are arbitrary comparison keys rather than \([d]\), their canonical renaming can be performed by a comparison sort in \(O(m\log m)\), giving a deterministic \(O(m\log m)\) implementation without a unit-cost indexed-colour assumption. The current CLI prioritizes human inspection and uses Python dictionaries/sorts, so this is a **mathematical implementation bound**, not a measured worst-case runtime of the current Python script.

For general connected graphs with differing adjacent palettes, the existence proof invokes the *original authors' Theorem 5*. This note does not claim that the present CLI processes those graphs or that the composed full-conjecture algorithm has been separately implemented. Complexity and certificates above are for the full uniform-palette regular theorem only.

## Independent review

The crucial mathematical obligations remain the auxiliary multigraph's sinkless orientation (including parallel 2-cycles), Q[R] component boundary, actual one global insertion order and complete colour-sequence distinction. The current package remains **pending** independent ROOT source acceptance, Lean compilation, and broad historical originality verification.
