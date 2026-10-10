# Affirmative answer to Problem 1, third palette

B, 2026-10-10. Complete written argument; B self-review only; independent
acceptance and historical novelty pending. This is NOT a counterexample.

## Original question

Ayman El Zein and Maidoun Mortada, *Impact of local girth on the S-packing
coloring of k-saturated subcubic graphs*, arXiv:2603.25113v1, 26 March 2026,
Section 5, Problem 1, third question, asks for a (2,2,2,2,4)-packing coloring
of every 1-saturated subcubic graph with maximum local girth at its
three-valent vertices equal to three.
https://arxiv.org/html/2603.25113v1#S5

A graph here is finite, simple and undirected. Subcubic means maximum degree
at most three. 1-saturated means each degree-three vertex has at most one
neighbor of degree three. The local-girth hypothesis means each degree-three
vertex lies on a triangle. Repeated 2's label four DIFFERENT color classes,
each with pairwise distances greater than two in the full original graph.
The fifth color requires distances greater than four.

## Stronger theorem sufficient for the original question

Let G satisfy the preceding structural hypotheses (also allow components
without degree-three vertices). Each connected component can be colored
with four distance-two packing colors and at most ONE exceptional vertex.
Consequently G admits a (2,2,2,2,r)-packing coloring for every positive
integer r. In particular r=4 answers the third question affirmatively.
The first two palettes in Problem 1 and Conjecture 2 are not resolved here.

Write H=G^2 for the graph joining distinct vertices at original G-distance
at most two. We show that, for each component, either H is 3-degenerate,
or H with one vertex deleted is 3-degenerate. An elimination order with
at most three remaining neighbors permits a four-coloring in reverse
order: at most three colors are forbidden. Give the deleted vertex the
fifth color. Across different components there is no finite path, so
reusing that fifth color in other components causes no distance violation.

IMPORTANT: H-v always means first form G^2, THEN delete v. It is not
(G-v)^2. The proof below explicitly retains all square edges through v.

## Structural classification

A triangle contains at most two degree-three vertices, because otherwise
each would have two degree-three neighbors. Two intersecting triangles
cannot share just one vertex, since that vertex would have degree at least
four. If they share an edge uw with other vertices z,t, then u,w have degree
three. Since u,w are adjacent, z,t must have degree two; otherwise u would
have a second degree-three neighbor. The component is the diamond K4-e.
The edge zt is excluded by 1-saturation. Its square is K4, already four-colorable.

Excluding these isolated diamonds, all triangles involving degree-three
vertices are disjoint. Every other vertex has degree at most two. Each
triangle has at most two external edges; its external-edge endpoints are
its ports. Contract the triangles. The resulting connected multigraph
has maximum degree two, so each component has a path or cycle arrangement.
Thus the possibilities are a plain path/cycle, a triangle, a chain of
triangles with leaf or triangle ends, or a necklace of triangles. In a
two-port triangle its ports are adjacent degree-three vertices, so each
external neighbor has degree at most two. Every connector incident to
such a triangle therefore has at least two edges before another triangle.
A direct edge between two one-port triangles and direct leaf tails are
allowed and will be handled below. No minimum-degree assumption is added.

## Elimination for components with ends

Consider a chain from one end to the other, forming square neighborhoods
in the original graph throughout.

At a leaf end, the leaf has at most three square neighbors: its neighbor
and that neighbor's other neighbors. Remove it. Continuing along an
ordinary path, a frontier vertex whose predecessor is already removed
has at most three remaining square neighbors: its successor and at most
two other neighbors of that successor. Vertices behind the frontier that
could occur at distance two have already been removed.

On reaching a triangle, name its incoming port u, outgoing port w (if
present), and non-port z. Let b be w's external neighbor, if present.
With the incoming connector already removed, the remaining square neighbors
of u are contained in {w,z,b}. Remove u; those of z are then contained in
{w,b}. Remove z; those of w consist of b and at most two other neighbors
of b. Remove w and continue along the outgoing connector. These upper
bounds remain valid if the outgoing connector ends immediately in another
cap triangle or a leaf.

If the chain begins in a cap triangle, first remove a non-port vertex z.
Its square neighbors are the other non-port vertex, the port, and the
port's external neighbor, at most three. Remove the other non-port vertex,
then the port, and proceed. A single triangle and a plain path are included.
Every removal therefore has at most three remaining square neighbors.
The square of any component with ends is 3-degenerate.

## Elimination for necklaces

Let a triangle have incoming port u, outgoing port w, and non-port z.
Let v be u's external neighbor and b be w's external neighbor. Both v,b
have degree two. Delete v from H, reserving it as the unique fifth-colored
vertex. Write t for v's other original neighbor and b' for b's other
original neighbor. Some named vertices can coincide in the shortest cases;
this only decreases the sizes of the following sets.

- z has square neighbors contained in {u,w,v,b}. With v deleted, at most
  three remain. Remove z.
- u has square neighbors contained in {w,z,v,t,b}. With v,z deleted, its
  remaining neighbors lie in {w,t,b}, at most three. Remove u. The square
  edge u-t THROUGH THE DELETED V is included in this count.
- w has square neighbors contained in {u,z,b,b',v}. With u,z,v removed,
  at most b,b' remain. Remove w.

Now proceed away from the removed triangle along the necklace, using the
same frontier/triangle removals as for chains. The only square connection
through deleted v was u-t; its endpoint u has already been removed. Any
other square edges entering the initial removed triangle end at removed
vertices. Thus at every subsequent step the remaining square neighbors
are contained in exactly the same forward sets as in the chain argument.
Continue until the opposite side of the cut is reached and all vertices
are removed. This proves H-v is 3-degenerate. Short necklaces with one or
two triangles cause identifications in the lists, not additional neighbors.
The isolated diamond was already treated.

For a plain cycle choose any v. In H-v remove the other vertices in cyclic
order starting next to v. The first vertex has at most three remaining
square neighbors (including the edge through v to the other end); later
vertices have at most three as well. For cycles of order three or four,
H is a clique of size at most four and needs no exception. C5-v is K4.
This proves the claimed degeneracy for every component and completes the
coloring proof. QED.

## Verification and exact scope

The argument proves existence for arbitrary size; finite computations do
not replace it. Run, with Python 3.12 standard library:

    python workstreams/B/triangle_packing/degeneracy_check.py

The checker reconstructs graph hypotheses, all original graph distances,
each proposed elimination step in G^2-v, and every same-color distance.
The discovery packing solver is not reused. Its finite fixtures comprise
2904 triangle-chain/necklace presentations with 1..5 gaps, each 2..6,
with reversal/rotation suppression but no graph-isomorphism deduplication.
The report includes three rejected corrupted certificates. The fifth color
is checked at most once per connected component; the numerical distance
check uses r=100, while uniqueness proves every r. A sample certificate is
in degeneracy_certificate.json. Both implementations are B-authored;
this is self-verification, not an independent agent's review or Lean proof.

Additional actual boundary replay:

    python workstreams/B/triangle_packing/boundary_checks.py

This checks 26 fixtures including isolated vertices, paths and cycles of
orders up to 11, directly joined cap triangles, short leaf tails, a cut
necklace and disconnected components containing two C5's. See
boundary_results.json. Path fixtures are copied before closing the cycles.
