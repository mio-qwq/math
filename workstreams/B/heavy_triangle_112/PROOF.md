# Positive proof candidate for original Conjecture 6

## Original statement and scope

El Zein–Mortada, arXiv:2603.25113v1, Section5 Conjecture6: every (3,0)-saturated subcubic graph G with g3(G)=3 admits a (1,1,2)-packing coloring. All graphs are finite, simple and undirected. A degree-three vertex is heavy when all three neighbors have degree three; (3,0)-saturation says that heavy vertices form an independent set. The local-girth condition means every degree-three vertex belongs to a triangle. This is an affirmative candidate, not a counterexample. Historical novelty and independent review are pending.

It suffices to construct a set C with pairwise distances at least three such that G-C is bipartite. Its two bipartition classes receive the two radius-one colors; C receives the radius-two color.

## 1. Structural reduction

Peel degree-zero and degree-one vertices repeatedly, remembering their deletion order. Such vertices can later be added back in reverse order using one of the two radius-one colors different from their unique already-colored neighbor. Adding a leaf cannot shorten distances between old vertices. The hypotheses are preserved while peeling: degrees and heavy sets can only decrease, and a surviving degree-three vertex cannot lose a triangle vertex to leaf peeling. Thus it suffices to treat the minimum-degree-two remainder, and its connected components separately. A component with no degree-three vertices is a cycle and admits the required coloring (alternate the two radius-one colors on an even cycle; use one radius-two vertex on an odd cycle).

In a subcubic graph two triangles that intersect must share an edge, unless they coincide: intersecting in just one vertex requires degree at least four. Two triangles sharing an edge induce either K4 or a diamond K4-e. A K4 component is excluded because its adjacent vertices are all heavy. In a diamond the two shared-edge vertices already have degree three. If both nonadjacent outer vertices also had degree three, both shared-edge vertices would be adjacent heavy vertices, impossible. Hence at most one outer diamond vertex has an external neighbor. No additional triangle can intersect such a diamond: shared-edge vertices have no free degree, and an outer vertex has at most one outside neighbor.

Consequently the triangle-containing vertices partition into disjoint blocks: ordinary triangles and isolated or one-port diamonds. A port is a block vertex with an external edge. Every other vertex has degree two and lies on a path connecting block ports. Contract each block to a vertex and each maximal inter-block path to an edge, remembering its length L. This gives a finite multigraph H of maximum degree three; loops and parallel edges are allowed, with loops contributing two incidences. Diamond vertices have degree at most one. Let D be the set of core edges of length one. A degree-three core vertex is an ordinary triangle with three ports. A port on an edge in D is heavy (both triangle neighbors and its outside neighbor have degree three). Therefore at most one of its three ports can meet D, since any two ports in that triangle are adjacent. Thus every degree-three core vertex has at least two incidences outside D. A loop in D is impossible in the original simple graph, as triangle ports are already adjacent.

## 2. Selection lemma

Let H be a finite multigraph of maximum degree three, and D a set of non-loop edges such that every degree-three vertex has at most one D incidence. There is a selection of oriented edges outside D such that:

1. each degree-three vertex selects exactly one incident edge as its outgoing edge;
2. each lower-degree vertex selects zero or one outgoing edge;
3. no edge is selected by both of its endpoints;
4. every cycle in the graph of unselected edges uses only D edges.

Moreover degree-one vertices need never select an outgoing edge. For a loop, selection uses one specified incidence at its vertex, not both.

First match each degree-three vertex to a distinct incident edge outside D. Hall's condition holds: for a set X of degree-three vertices there are at least 2|X| incidences with edges outside D, while each such edge contributes at most two incidences, including loops. Thus there are at least |X| distinct incident edges. Select the matched edge from its matched vertex. All lower-degree vertices initially select nothing. The unselected graph R has maximum degree two.

If R has a cycle K containing an edge e=uw outside D, modify the selection at u as follows. If u selects no edge, simply let u select e. Since u lies on K and has no selection, u has degree two; it is not a degree-one vertex. This breaks K and cannot create an unselected cycle.

Otherwise u selects an edge f=uv. The two incidences of K and f exhaust its degree three, so f is the only selected edge incident to u. Its other endpoint v is outside K. Indeed, a degree-two vertex of K cannot have a selected incident edge, while at a degree-three vertex of K its unique selected incident edge would have to be its own outgoing edge. Were v on K, both ends would therefore select f, contrary to condition3. Change u's selection from f to e. The edge e was unselected, so no double selection is introduced.

Before the change, v has at most one unselected incidence: if it has an outgoing edge, that edge is different from the incoming f, while if it has none then its degree is at most two. Hence v lies in a path component of R, not in a cycle. Removing e breaks K into a path, and returning f connects that path to v's different path component. No new cycle is created. This reasoning also applies when K is a loop or a two-edge parallel cycle. Each modification decreases the number of cycles not wholly in D. Finiteness proves the lemma.

## 3. Select the radius-two vertices

Apply the lemma to the core. In each triangle with a selected outgoing edge, put the port of that selected incidence in C. In every triangle with no selection, put any non-port vertex in C; one exists because all degree-three core vertices have a selection. In each diamond put one of its two shared-edge vertices in C. Diamonds have core degree at most one and never acquired a selection in the lemma. Thus every block contains exactly one C vertex, and no degree-two connector vertex is in C.

C is a 2-packing. Within a block there is only one selected vertex. Across a connector of length L>=3, all distances are already at least three. For L=2 a conflict could occur only if both endpoint ports were selected, forbidden because an edge is selected from at most one end. For L=1 neither port is selected, since D edges cannot be outgoing selections. Each C vertex in an endpoint block is then at distance at least one from its port, so the total distance is at least three. A path traversing two different connectors must also traverse between two distinct ports of an intermediate block, adding at least one internal edge; its length is at least three. This exhausts all possible paths of length at most two. Loops do not introduce a second C vertex in their block or a shorter connection to a different block.

## 4. The remaining graph is bipartite

Deleting C from a triangle leaves an edge. Deleting the chosen shared vertex from a diamond leaves a three-vertex path with at most one external port. Each connector corresponding to a selected core edge loses one endpoint and therefore becomes a dangling path, not part of any cycle. All cycles that remain must correspond to cycles of the unselected core R. By the lemma, these use only D edges.

A D-only core cycle cannot pass through a degree-three core vertex, since such a vertex has at most one D incidence. Its vertices therefore all have degree two, are triangles (diamonds have degree at most one), and have no outgoing selection because both incidences are unselected. Their non-port vertices were put in C. Each passage through a triangle now uses its one remaining edge, while each D connector contributes one more edge. A k-edge D core cycle therefore lifts to an even cycle of length 2k. This includes parallel cycles; D loops were already excluded. Hence every cycle of G-C is even, and G-C is bipartite.

Assign its two bipartition classes the two radius-one colors and C the radius-two color. Restore peeled leaves and isolated vertices as above. This proves the full original statement.

## Review obligations

Key points are the diamond classification, Hall incidence count including loops, cycle-elimination exchange without a new cycle, and the original-distance packing check. The proof does not rely on source Lemma2, on a numerical search horizon, or on the earlier restricted matched-family proof. No Lean or independent peer review is asserted. A direct constructive checker and deliberately corrupted cases accompany this candidate; their recorded executions are regression evidence, not a substitute for the all-parameter argument above.
