# The cubic subcase of the claw-free(1,2,2,2,2) conjecture

**Candidate theorem.** Every finite simple claw-free CUBIC graph admits a(1,2,2,2,2)-packing vertex coloring. Disconnected graphs are colored componentwise.

This is an affirmative subcase of Mortada–El Zein–Al Hajjar, arXiv:2608.02566v1 Section6 Conjecture1, not the full subcubic conjecture and not a counterexample. Colors are0,1,2,3,4; color0 has required separation>1, and each other color has separation>2 in the ORIGINAL graph. Pending independent review and novelty assessment. No Lean.

The proof imports Maydanskiy's classical incidence5 theorem for finite simple subcubic graphs. Triangle/diamond structural decompositions are standard (Oum2011 and, including bridges, Gutierrez–Ugarte2610.09565v1 Proposition3). Neither theorem nor those decomposition ideas are new claims here. The proposed contribution is their precise extension to this mixed-radius palette through the following interfaces.

## 1. Safe interfaces

A leaf can always be added without changing the old coloring. If its neighbor is not0, use0. Otherwise at most two additional old vertices are at distance2 from the leaf, forbidding at most two of the four radius-two colors; choose another.

### Diamond insertion into an edge

Replace an edge uv by u-x, v-y and the diamond on x,y,p,q with edges xp,xq,yp,yq,pq. Let old colors of u,v be a,b, necessarily distinct. Set x=b,y=a and choose p,q to have distinct radius-two colors different from a,b. At least two such colors exist. This is valid within the gadget. Outside it, x imitates the former v at u and y imitates the former u at v; p,q see only u or v within two edges outside the diamond and avoid both their colors. No distance between old vertices decreases. The color0 cases are covered because its only restriction is adjacency. Hence arbitrary strings of diamonds can be inserted safely. This is the standard edge-extension idea adapted to the stated palette, not a new graph construction.

### Two triangles joined by two edges: edge insertion

Let Q have triangles(a,x,y) and(b,z,w), with xz and yw. Its two free ports are a,b. Replace an old edge uv by u-a and b-v, keeping Q internally. Set a=old(v), b=old(u). The two old endpoint colors are different.

If both a,b have radius-two colors, set x=w=0 and give y,z the two other radius-two colors. If a=0 and b is a radius-two color, set z=0 and assign x,y,w the three radius-two colors different from b. If b=0 use the symmetric assignment obtained by exchanging(a,x,y) and(b,z,w). All required original-distance inequalities hold. Only a and its triangle neighbors are within two steps of u, and symmetrically at v; the chosen colors ensure the old boundary constraints. No old-old distance decreases.

### Three pendant caps

Each cap has one attachment vertex r. Start with a leaf r attached to an old outside vertex q, and add the rest of the cap. It suffices to extend for the three boundary types

    (color(r),color(q))=(0,1),(1,0),(1,2),

because the four radius-two colors may be permuted. Any NEW cap vertex is at distance at least3 from every old vertex other than r,q; old r already satisfies constraints with all old vertices. Thus the following literal finite table is a complete boundary extension certificate.

D: vertices0..6, root0; edges01,02,12,13,24,35,36,45,46,56. This is one triangle with a one-diamond loop attached at its other two vertices.

B: vertices0..5, root2; triangles012 and345, plus03 and14. This is the two-triangle parallel pair with one free port attached and the other unused.

T: vertices0..8, root8; triangles012,345,678, plus03,14,26,57. This is the three-triangle cap formed when both outside neighbors of a parallel pair are the same core vertex.

Append outside q as the last vertex and add rq. The color rows, including q, are:

    D (0,1): 0 2 3 0 0 1 4 1
    D (1,0): 1 0 2 3 0 1 4 0
    D (1,2): 1 0 3 2 0 1 4 2
    B (0,1): 2 3 0 0 1 4 1
    B (1,0): 0 2 1 3 0 1 0
    B (1,2): 0 3 1 2 0 1 2
    T (0,1): 1 3 0 2 4 0 2 3 0 1
    T (1,0): 1 3 0 2 4 0 2 3 1 0
    T (1,2): 3 0 2 0 1 2 0 3 1 2

Direct original-graph BFS checks every row. Removing q yields a coloring for an isolated cap. Discovery produced this table independently of the prior papers' examples; only the standard graph operations are shared background.

## 2. Triangle expansions of every loopless subcubic multigraph

For a loopless multigraph H of maximum degree at most3, let T3(H) replace EVERY vertex with a triangle, using one distinct port for each incident edge and leaving any unused ports of degree2. We prove T3(H) is colorable by induction on |V(H)|, componentwise.

If H is simple, use the published incidence5 theorem. Incidences(v,e) correspond to used triangle ports, and adjacent incidences are exactly used-port pairs whose distance in T3(H) is at most2. Thus the five incidence colors give a square coloring of all used ports. At a core vertex of degree2, its one unused port sees at most four different colors on used ports within distance2, so choose the fifth. At degree1, the two unused ports must avoid only the used port and its external partner, leaving at least three colors for two distinct choices. At degree0 color the isolated triangle with three colors. Unused ports at different triangles have distance at least3, so these choices are independent. Finally designate any one of these five square colors as color0, weakening its constraint.

If H has three parallel edges, their endpoints form an entire component. Its expansion is the triangular prism: label corresponding triangles(a,x,y),(b,z,w) and include ab,xz,yw. Color x=w=0 and give a,b,y,z the four distinct radius-two colors. This is valid, since x,w are nonadjacent and no other color repeats.

Otherwise choose a double edge uv. Each of u,v has at most one other edge.

- Neither has another edge: the component is Q, already colored by any cap B row with q removed.
- Exactly one has another edge to a vertex s: delete u,v from H. Color the smaller T3(H). At its newly unused s-port attach a leaf, then extend cap B. This exactly restores T3(H).
- Both have other neighbors s,t with s!=t: delete u,v and add an edge st, retaining any existing parallel edges. This is a smaller loopless subcubic multigraph. Color its expansion and replace the newly added port edge by the Q edge-insertion interface from Section1.
- Both have the same other neighbor s: u,v,s form cap T, and s has at most one remaining external edge. Delete all three core vertices; if there is an external edge, restore the cap by adding a leaf to the corresponding free port and applying T. Otherwise this component is the isolated cap T.

All operations decrease core order; every case preserves the actual port incidence structure and the original palette. This closes the induction, including parallel-edge and bridge cases.

## 3. From claw-free cubic graphs to the proved expansions

Let G be connected, simple, claw-free and cubic. Every vertex lies in a triangle, since its three neighbors cannot be independent. If overlapping triangles form K4, connectedness gives G=K4. Otherwise their union is an induced diamond; degree3 ensures distinct diamond blocks are vertex-disjoint. Vertices in no diamond belong to one unique triangle, and those triangle blocks are disjoint. This gives the familiar partition into triangle and diamond blocks.

Contract each block. Triangle blocks have three external incidences; diamond blocks have two. If all blocks are diamonds, connectedness makes a ring of diamonds. Such a ring is obtainable from K4 by repeated diamond insertions into an edge (the one-block case is K4); Section1 applies.

Otherwise suppress the degree-two diamond chains between triangles. This gives a cubic multigraph of triangle blocks. Nonloop chains may have length zero; loops necessarily contain at least one diamond because a new edge between ports of the same triangle would duplicate its existing edge. First set aside all nonloop diamond chains and retain only one diamond on each loop; restoring them later uses safe edge insertions.

A loop core vertex has at most one other external edge and hence forms a pendant D cap. Remove this whole triangle/loop cap from the core. After all such removals, the remaining object is T3(H) for a LOOPLESS SUBCUBIC multigraph H, possibly disconnected, with unused ports where caps were removed. Color it by Section2; restore removed caps in reverse order by the leaf and D interfaces. If removal consumes an entire component, start with its isolated-cap coloring. Finally restore every set-aside diamond by the edge insertion rule.

This proves the candidate theorem for every claw-free cubic G. K4 itself uses four distinct colors, so its case is immediate.

## 4. Sources, exact scope, and unresolved cases

M. Maydanskiy, *The incidence coloring conjecture for graphs of maximum degree3*, Discrete Mathematics292(1–3)(2005),131–141, DOI10.1016/j.disc.2005.02.003. The finite simple subcubic incidence5 theorem is an imported published result, not a lemma numerically assumed or a new claim.
https://www.sciencedirect.com/science/article/pii/S0012365X0500052X
Author-maintained summary and definitions:
https://www.labri.fr/perso/sopena/pmwiki/index.php?n=TheIncidenceColoringPage.TheIncidenceColoringPage

Standard decomposition background, including bridges:
https://arxiv.org/html/2610.09565v1 (Proposition3).
That paper's square6 theorem is not the same as this mixed-palette claim. The edge-extension/decomposition tools are credited; the claimed subcase must still be checked for earlier literature.

Degree-two vertices OUTSIDE triangles in a general claw-free subcubic graph are not covered by Section3. Such vertices cannot simply be completed to degree3 while preserving claw-freeness. Subdivision of an edge also need not extend every fixed coloring without recoloring. No universal full-subcubic conclusion is drawn. The original Conjecture1 remains unresolved by this packet. Review should focus on cap boundary completeness, all four double-edge cases, the unused-port incidence extension, and the loop-restoration order.
