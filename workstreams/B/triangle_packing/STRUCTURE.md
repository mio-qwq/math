# Structural reduction, B working proof, 2026-10-10

For a finite simple subcubic graph with at most one degree-three neighbor
per degree-three vertex, and with every degree-three vertex in a triangle:

1. A triangle has at most two degree-three vertices. Three would each have
   two such neighbors.
2. Distinct intersecting triangles cannot share just one vertex (degree
   at least four). If they share an edge uv, u and v have degree three.
   Their two other neighbors x,y cannot have degree three, because then u
   would have more than one degree-three neighbor. Thus x,y have degree two,
   and the component is precisely the diamond K4 minus one edge. The edge
   xy cannot be present because it would make all four degrees three.
3. Outside these isolated diamonds, all triangles containing degree-three
   vertices are vertex-disjoint. Each triangle has zero, one or two external
   edges. Vertices outside these triangles have degree at most two.
   Contracting each such triangle therefore gives a connected multigraph
   of maximum degree two. Loops/parallel edges are allowed in this description.
   A component is consequently a path, a cycle, a singleton, or an isolated
   triangle/degree-at-most-two component. This gives triangle necklaces
   and chains with triangular or leaf ends, as well as plain paths/cycles.
4. A two-port triangle has two adjacent degree-three vertices. An external
   neighbor of either port must consequently have degree at most two.
   Thus a path joining such ports has length at least two. The only direct
   edge between two triangles possible in a connected component joins two
   one-port cap triangles. Leaf tails can have length one. These cases were
   NOT all covered by the first experiment.

This reduction explains why the initial necklace/chain search is relevant,
without asserting that finite tests settle the source problems.

First exact experiment: 2904 generated presentations, four requested palettes
per presentation, all SAT, zero UNSAT/UNKNOWN. These are presentations, not
2904 certified pairwise nonisomorphic graphs. The exploration suppresses
cyclic rotations and chain reversal but does not compute graph isomorphisms.
Gaps in {2,...,6}, between one and five gaps; triangle-ended chains and
necklaces only. All reported colorings were distance checked. The exploratory
solver is not an independent acceptance checker and no UNSAT certificate
was generated. Source and actual receipt: explore.py, experiment.json.

A useful failed restricted model: forcing all triangles to have port colors
(2,h), apex1 with h in {3,4,5}, and all connector interiors in {1,2,3},
cannot handle an odd necklace whose gaps all have length3. Such a connector
forces interior 1,3 and hence excludes h=3 on either end; the remaining
high colors4,5 must alternate around an odd cycle. This is an obstruction
to this restricted coloring ansatz, NOT a counterexample to any source
question. The graph is colorable with the triangle pattern (1,2,4),
connector interiors (1,3), repeated cyclically. Next: use distinct triangle
boundary states rather than repeat the failed fixed state.
