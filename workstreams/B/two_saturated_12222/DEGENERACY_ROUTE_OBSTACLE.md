# A second exact route obstruction: 3-degeneracy is too strong

B, 2026-10-10. Original scope: arXiv2603.25113v1 Section5 Conjecture4, defined in SOURCE_GATE.md. Classification: auxiliary strengthening counterexample, not original counterexample. Pending independent review.

The cube obstruction does admit an independent set whose complementary original square is3-degenerate. Thus replacing the maximum-degree-four prerequisite by3-degeneracy was a genuinely different possible proof strategy. A bounded test stopped at its first obstruction: take the Petersen graph with outer5-cycle 0,...,4, inner star edges (i+5,(i+2 mod5)+5), and spokes (i,i+5). Subdivide matching (0,1),(2,3),(4,9),(5,7),(6,8) once, with new vertices10,...,14 respectively.

The resulting graph is simple, connected,2-saturated, subcubic, with15vertices and20edges. For EVERY independent set I, G²[V\I] contains a nonempty induced subgraph with minimum degree at least4, and so is not3-degenerate. This does not obstruct ordinary4-colorability. The original12222 palette has the explicit vertex-order coloring

    0,0,1,0,1,2,2,3,3,0,3,2,4,0,0.

Independent-definition checker verify_degeneracy_obstacle.py rebuilds the graph and all original BFS distances. It scans ALL32768 subsets, keeps exactly882 independent sets, and for each simultaneously peels vertices of residual square degree at most3. Every residual core is nonempty; its minimum degree is explicitly rechecked. Core orders8,...,15 have frequencies40,75,191,275,200,85,15,1. These sum to882. No discovery routine, MILP or coloring solver is imported.

Actual Python3.12.14 standard-library run:

    python workstreams/B/two_saturated_12222/verify_degeneracy_obstacle.py

PASS:32768 subsets,882 independent sets,225 full-distance entries, original coloring and two controls. The JSON's initial “original coloring undecided” scope line is historical; its later SAT witness and the checker settle that finite question.

There are40 independent sets whose residual4-core has maximum degree exactly4. This leaves open a different Brooks-on-the-core argument, but it is NOT proved for general graphs. Do not claim that original4-colorability follows from merely4-degeneracy. Stop further sampling of the rejected3-degeneracy criterion; finding more failures has little value. Source/log/JSON are preserved as discovery evidence, separate from this exact certificate.
