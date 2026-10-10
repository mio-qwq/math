# A negative answer to August 2026 Problem 1

Status: exact original-question counterexample candidate; B's self-review only, independent acceptance and historical novelty pending. No Lean claim.

## Original question

Maidoun Mortada, Ayman El Zein and Sara Al Hajjar, *On (1,1,2,3)- and (1,1,3,3,3)-Packing Colorings of Claw-Free Subcubic Graphs*, arXiv:2608.02566v1 (3 August 2026), Section 6, Problem 1, asks whether every connected claw-free subcubic graph other than the twelve-vertex graph H admits a (1,1,3,3,4)-packing coloring. Equal-color vertices must have distance strictly greater than the indicated integer, measured in the full graph.

We give a 36-vertex negative answer, and an infinite family. This does not contradict the paper's proved (1,1,3,3,3) theorem.

## Explicit construction

For an odd integer k >= 3, let D_k have vertices a_i,b_i,p_i,q_i, with i modulo k. For each i add the five edges a_i b_i, a_i p_i, a_i q_i, b_i p_i, b_i q_i, and add q_i p_(i+1). Thus D_k is a cyclic chain of k diamonds, with the two nonadjacent diamond vertices joined to the preceding/following diamond. It is a connected simple cubic graph on 4k vertices.

Form G_k by replacing every vertex v of D_k with a triangle T_v, whose three vertices are the incidences (v,e) for the three core edges e incident to v. Join every pair in T_v. For each core edge e=uv add the joining edge (u,e)(v,e). Then G_k has 12k vertices and 18k edges. Our fixed certificate is k=3.

G_k is finite, simple, connected, cubic, and claw-free: every vertex has two mutually adjacent neighbors in its own triangle. It cannot equal the excluded graph H, since 12k >= 36 > 12.

## Necessary projection from ANY original coloring

Suppose G_k had the questioned coloring, with colors 1a,1b,3a,3b,4. Each triangle T_v contains a vertex of one of the last three colors, since a triangle cannot be colored with two independent classes. Choose one such representative x_v from each triangle. This is legitimate even if the triangle initially contains multiple high-colored vertices.

Label v by the color of x_v. Adjacent core vertices u,v receive different labels: every vertex of T_u is within distance at most three of every vertex of T_v (one internal edge at each end and the joining edge). Thus the chosen labels form a proper three-coloring f of D_k, using labels A=3a, B=3b, C=4.

Let I=f^{-1}(C). If x_v is the port (v,vw), then w must be an external private neighbor of v relative to I: N_D(w) intersect I = {v}. Indeed, if u != v in I were adjacent to w, then u and v are not adjacent (properness), and the path from x_v through T_w and the joining edge to T_u reaches EVERY vertex of T_u in at most four edges. In particular d_G(x_v,x_u) <= 4, contradicting their common color 4.

This is a necessary condition for every original coloring, not merely for a construction that assumes one high-colored vertex per triangle. No normalization of the remaining low-colored vertices is assumed.

## Diamond forcing contradicts the private-neighbor condition

In every proper three-coloring of a diamond a_i,b_i,p_i,q_i, the vertices a_i,b_i have distinct labels, and p_i,q_i must both have the third label; call it t_i. The joining edge q_i p_(i+1) forces t_i != t_(i+1).

If t_i=C, then both p_i and q_i belong to I. The neighbors a_i,b_i of p_i cannot be private, since each is adjacent to q_i as well. Its only remaining neighbor is q_(i-1). The joining edge forces t_(i-1) != C, so exactly one of a_(i-1),b_(i-1) has label C. That vertex is also adjacent to q_(i-1). Thus q_(i-1) is not private either. Hence p_i has NO private neighbor, a contradiction.

Therefore no t_i can be C. But then the cyclic sequence t_0,...,t_(k-1) is a proper two-coloring of an odd cycle, impossible. This proves that G_k is not (1,1,3,3,4)-packing colorable for every odd k >= 3.

## Scope and provenance

The 36-vertex witness alone suffices; no minimality or exact packing chromatic number is asserted. It arises from B's independently derived private-neighbor obstruction and the proper-three-color rigidity of diamonds, not from the source's different fifth-radius-five example. The triangle/core language and generic Hall framework are established tools in the source, not claimed as B inventions. The proof above does not invoke Hall, a solver, or a numerical assumption. A separate checker reconstructs original adjacency/BFS and enumerates all possible projected labelings and all radius-four representative choices.
