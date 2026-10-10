# A seven-vertex counterexample to original Conjecture 3

## Statement and status

Ayman El Zein and Maidoun Mortada, *Impact of local girth on the S-packing coloring of k-saturated subcubic graphs*, arXiv:2603.25113v1 (26 March 2026), Section 5, Conjecture 3, asserts that every 2-saturated subcubic graph is (1,1,2)-packing colorable. The following graph refutes the assertion as printed. It does not refute the paper's separate theorem with local girth of every degree-three vertex equal to three. Historical novelty and independent acceptance remain pending.

## Exact construction

Start with K4 on a,b,c,z and subdivide each of za,zb,zc once, using new vertices x_a,x_b,x_c. The edge set is

    ab,bc,ca, ax_a,bx_b,cx_c, zx_a,zx_b,zx_c.

This is a connected, finite, simple undirected graph with seven vertices and nine edges. The degrees of a,b,c,z are three; the degrees of x_a,x_b,x_c are two. Each triangle vertex has exactly two degree-three neighbors, while z has none. Thus it is 2-saturated, with maximum degree three and minimum degree two. It even is planar and has no bridges; neither extra property is needed.

The machine certificate uses a=0,b=1,c=3,z=2,x_a=6,x_b=4,x_c=5. Its edge list is explicit and the verifier does not import the discovery program.

## Complete elementary contradiction

Assume a packing coloring with distinct colors A,B,C, with respective required pairwise distances greater than 1,1,2. The triangle abc cannot be colored using A and B alone. Therefore some triangle vertex, say a after permuting a,b,c, receives C.

Every other vertex is at distance at most two from a: b,c,x_a are adjacent to a; z is reached via x_a; x_b via b; x_c via c. Consequently no other vertex can receive C. But G-a contains the odd cycle

    b,c,x_c,z,x_b,b

of length five. All its vertices would have to use only A and B, each of which is an independent color class. Alternating two colors around an odd cycle is impossible. This contradiction proves that no (1,1,2)-packing coloring exists. No numerical search or computational assumption is needed for this proof.

For clarity, the local girths of a,b,c are three, while the local girth of z is five: any cycle through z follows two subdivided spokes and a path in the triangle. Thus the maximum local girth among degree-three vertices is five, not three. Original Conjecture 3 has no local-girth hypothesis; the construction satisfies all its printed assumptions.

## Verification and limitations

Python 3.12.14, standard library only:

    python workstreams/B/two_saturated_112/verify_candidate.py

Actually run 2026-10-10. Independent implementation reconstructs adjacency, verifies simplicity/degrees/saturation, runs integer BFS from every vertex, and tests every one of 3^7=2187 color assignments directly against the original distance definition. Zero valid assignments. It also checks all three explicit odd cycles used in the proof. The graph's diameter is two. Negative controls reject an added edge causing degree four and an edge-deleted graph for which the false no-coloring claim fails.

The initial discovery procedure used exact odd-cycle-transversal branching on partially subdivided cubic graphs. One thousand cycle-plus-matching cores with a perfect matching subdivided once were colorable (this restricted family is not claimed exhaustive). The first broader edge-cover batch found this graph and stopped. The parity batch was not run. No minimality, classification, optimum, Lean formalization, independent peer review, or historical firstness is claimed. All proof steps above were checked by B personally, without spawning new agents.
