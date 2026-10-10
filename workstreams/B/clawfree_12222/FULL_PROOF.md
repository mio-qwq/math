# Full claw-free subcubic (1,2,2,2,2) coloring: a prior-theorem corollary

**Candidate theorem.** Every finite simple claw-free graph of maximum degree at most three admits a (1,2,2,2,2)-packing vertex coloring.

This is exactly Conjecture1 in Section6 of Mortada–El Zein–Al Hajjar, arXiv:2608.02566v1. The proof below is a corollary of Yang–Wu's PUBLISHED2022 edge-coloring theorem plus explicit elementary diamond reductions. It is not a new general edge-coloring theorem, not a counterexample, and not a historical-priority claim. Pending independent review. No Lean.

Use colors0,1,2,3,4. Equal color0 vertices must have distance greater than1, and equal positive-colored vertices distance greater than2, in the original graph. Disconnected components can be colored independently.

## 1. Imported theorem and exact semantics

Yang and Wu proved that every finite simple graph B with d_B(u)+d_B(v)<=5 for each edge uv admits a(1,2,2,2,2)-packing EDGE coloring. Their definition uses precisely the vertex distance between corresponding edges in the line graph L(B). Thus L(B) has the vertex packing coloring required here.

W. Yang and B. Wu, *On S-packing edge-colorings of graphs with small edge weight*, Applied Mathematics and Computation418(2022),126840, DOI10.1016/j.amc.2021.126840.
https://www.sciencedirect.com/science/article/pii/S0096300321009231
https://doi.org/10.1016/j.amc.2021.126840

The publisher-indexed primary abstract explicitly provides both the theorem and line-graph metric. Direct opening returned403; the full source proof was not reverified. The same relevant consequence is explicitly restated in the introduction of Liu–Yang–Zhang, arXiv:2603.14398v1, following Open Question1.1, with Yang–Wu as reference[22]. No result of that later paper is needed for the proof.
https://arxiv.org/html/2603.14398v1

## 2. Diamond-free base case: construct a SIMPLE root graph

Let G be connected, claw-free, subcubic, not K4, and contain no induced diamond K4 minus one edge. Every degree-three vertex belongs to a triangle: otherwise its neighbors would be an independent triple. Distinct triangles cannot share just one vertex, as that vertex would have degree at least four. If they share an edge, their four vertices induce either a diamond or K4; the latter would be the entire connected component. Both are excluded. Hence the triangles of G are vertex-disjoint.

Partition the edges of G into cliques: one three-vertex clique for every triangle, and one two-vertex clique for every edge not in a triangle. Each vertex of G belongs to at most two of these cliques. Indeed, a triangle vertex has at most one external edge, and a nontriangle vertex has degree at most two.

Construct B as follows. Make one root vertex for each clique. For each original vertex x in two cliques, create a root edge between those two clique vertices. If x belongs to just one clique, create an edge from its clique vertex to a fresh private leaf. If x is isolated, create a separate edge between two fresh leaves. Label that root edge by x.

This root graph is SIMPLE: two distinct cliques intersect in at most one vertex, so no two original vertices create parallel root edges; private leaves are distinct and no loop arises. Each clique vertex has degree equal to the clique size, either2 or3. No edge joins two degree-three clique vertices, since the triangles are disjoint. Thus every root edge has endpoint-degree sum at most5.

Two root edges intersect if and only if their original vertex labels lie in the same clique, which is equivalent to adjacency in G. Consequently the map x -> its labelled root edge is a graph isomorphism G ~= L(B). It preserves ALL graph distances, not just adjacency or bounded distances. Yang–Wu's theorem therefore colors G. This also handles paths, cycles, leaves and isolated vertices; no minimum-degree assumption is used. K4 itself is colored with four distinct colors.

In particular, all of our earlier triangle-expansion subcases follow from prior theory. They cannot be counted as new existence results. Their frozen constructions are retained only as alternate arguments and exact interfaces.

## 3. Extension operations, in the original metric

### Adding a leaf

Given a coloring and a vertex u of degree at most2 before attachment, add a leaf r. If u is positive, set r=0. If u=0, its at most two other neighbors forbid at most two positive colors for r, so choose another. Old-old distances do not change.

### Inserting a diamond into an edge

Replace edge uv by a diamond with tips a,b, centers p,q, and attachment edges ua,bv. Its internal edges are ap,aq,bp,bq,pq. If the old endpoint colors are A,B, they are distinct. Set a=B,b=A and choose distinct positive colors for p,q different from both A,B. At least two such colors are available.

This colors the diamond correctly. Tip a has exactly the same potential distance-one/two conflicts outside the gadget as the old v across edge uv, and similarly for b and old u. Centers p,q only see u,v outside the diamond within distance two and avoid their colors. Old-old distances cannot decrease. This is a safe extension for every old coloring, including a zero endpoint.

### Pendant diamond and pendant seven-vertex cap

Start with a leaf r joined to an old outside vertex z, already validly colored. Square-color permutations reduce (color(r),color(z)) to (0,1),(1,0),(1,2). New vertices in an attached cap are at distance at least three from every old vertex other than r,z. Thus the following literal rows suffice for all outside graph structures.

Pendant diamond P: vertices(r,s,p,q)=(0,1,2,3), edges02,03,12,13,23. Root r=0; append outside z=4 and edge04. Rows in vertex order0..4:

    (r,z)=(0,1): 0 1 2 3 1
    (r,z)=(1,0): 1 0 2 3 0
    (r,z)=(1,2): 1 0 3 4 2

Cap D: vertices0..6, root0; edges01,02,12,13,24,35,36,45,46,56. It is a triangle whose other two vertices connect to the two tips of a diamond. Append outside7 and edge07. Rows0..7:

    (r,z)=(0,1): 0 2 3 0 0 1 4 1
    (r,z)=(1,0): 1 0 2 3 0 1 4 0
    (r,z)=(1,2): 1 0 3 2 0 1 4 2

Direct BFS verifies these six rows. Delete z for isolated caps. The D rows coincide with the previously frozen cap certificate; no change to frozen proof bytes is required.

## 4. Induction removes every possible diamond

Proceed by induction on |V(G)|, treating connected components separately. The diamond-free case and K4 are done above. Choose an induced diamond with nonadjacent tips a,b and centers p,q. Each center already has its three neighbors inside the diamond. Each tip has at most one outside neighbor.

**No outside neighbors.** G is the isolated diamond. Give its four vertices distinct colors.

**Exactly one outside neighbor.** Say a is joined to u. Delete all four diamond vertices, color the smaller induced graph by induction, attach a leaf a at u, and use pendant cap P. This reconstructs G without changing any old color.

**Two outside neighbors, both equal to u.** If u had a third neighbor w, then a,b,w would be pairwise nonadjacent: a,b are nonadjacent tips and are already saturated. This would be a claw centered at u. Hence u has degree two and G is exactly the five-vertex diamond with a two-edge outside a-u-b path. Set a=b=0 and give p,q,u three distinct positive colors. This is valid.

**Two distinct outside neighbors u,v, with uv not an edge.** Form G'=G-{a,b,p,q}+uv. It is simple and subcubic. It is also claw-free. To verify the only possibly new claws, suppose u has degree three. Its two neighbors other than a in G must be adjacent, because neither can be adjacent to the saturated tip a. That same adjacent pair remains in G'; replacing a with v cannot create a claw at u. The same holds at v. Elsewhere adding an edge cannot create an induced claw, and deleting diamond vertices cannot create one. Color G' by induction and insert the diamond into uv using Section3.

**Two distinct outside neighbors u,v, with uv already an edge.** If u has degree three, write its third neighbor as w. Claw-freeness at u forces vw to be an edge, since the saturated tip a is adjacent to neither v nor w. Thus v also has degree three with this same third neighbor w. Conversely if v has degree three, the same reasoning applies. There are exactly two subcases:

- Both u and v have degree two. Connectedness makes G the six-vertex diamond with outside path a-u-v-b. Set a=b=0 and give p,q,u,v the four distinct positive colors.
- Both have degree three and share w, forming triangle uvw. The diamond plus this triangle is exactly cap D with root w. If w has degree two, it is an isolated cap, colored by a D row without its outside vertex. If w has degree three, let its remaining neighbor be z. Delete the whole seven-vertex cap, color the smaller induced graph by induction, add leaf w at z, and apply cap D.

These cases are exhaustive. Every induction call has fewer vertices and satisfies the original simple/claw-free/subcubic hypotheses. Every restoration has been justified in the original metric. Therefore every G has the asserted coloring. QED, subject to independent review of this candidate proof and the stated imported theorem.

## 5. Verification and status

verify_full.py checks local cap rows, original-distance diamond extensions and all reduction cases on its explicitly stated finite labeled graph range, and verifies the root graph construction by exact line-graph reconstruction. It does not claim to reprove or implement Yang–Wu's published theorem. Finite base-case colors are found independently by exact backtracking only to test reductions on those instances. No finite run proves the universal theorem; the mathematical proof is the induction plus imported theorem above.

Original target: https://arxiv.org/html/2608.02566v1#S6 . Source and duplicate-status searches refreshed2026-10-10 09:43–09:45UTC. No same-scope full-claw-free resolution located in those searches, but novelty remains unconfirmed and no world-first statement is made. The achievement claimed is a COMPLETE candidate corollary for the original printed statement, rather than independent rediscovery of the2022 theorem. No author contact, submission, independent acceptance or Lean compilation claimed.
