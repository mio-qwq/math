# Exact failure of a restricted fifth-color placement rule

This is an auxiliary-route obstruction, NOT an original counterexample.

Take core K4 on0,1,2,3, with core edges in order01,02,03,12,13,23. Replace vertices with triangles and give the six port connectors lengths2,2,2,2,2,3. The original graph has19vertices. Suppose the radius-three fifth color D is allowed ONLY on the five length2 connector interiors, while all triangle and length3-interior vertices must use the four radius-two colors.

Any two D-connector edges sharing a core vertex have their interiors at original distance3. Thus the D-edges must form a matching M in K4-23. Every other length2 connector forces equal missing triangle colors at its ends. But K4-23 remains connected after deleting any matching: every nontrivial bipartition has a crossing vertex incident with at least two cut edges. For singleton cuts this follows from minimum degree2; the three two-versus-two cuts have respectively four,three,three crossing edges and none is a matching. The missing colors at2 and3 must therefore be equal. The undeleted length3 connector requires them unequal, contradiction.

The original five-color palette nevertheless succeeds. With the discovery program's vertex numbering, an explicit coloring is

    [0,1,2, 1,0,2, 0,1,2, 0,1,2, 3,3,3,3,3,3,4].

The sole D is the second interior of the length3 connector. This precisely shows why confinement to length2 connectors is unjustified; it does not oppose Conjecture5. probe_mixed_matching.py/log record the first two K4 patterns: all-length2 SAT, then this restriction UNSAT in2297 search nodes and the original palette SAT. No timeout occurred, and no larger window was pursued.

Resume only with a placement argument that genuinely permits D on length3 connectors and/or triangles. Orienting D placements along monochromatic length3 edges appears useful but is not proved to solve the port-list constraints. Do not claim an orientation/list-coloring theorem without handling those constraints.
