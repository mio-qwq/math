# Computer-assisted affirmative answer to Problem 1, second palette

Agent B, 2026-10-10. Complete mathematical reduction plus an exact finite
invariant certificate, self-checked by B; pending independent acceptance.
This is a positive answer, not a counterexample or a claim of Lean formalization.

## Target and structural reduction

El Zein and Mortada, arXiv:2603.25113v1 (26 March 2026), Section 5 Problem 1,
SECOND question asks whether every finite simple 1-saturated subcubic graph
with every degree-three vertex on a triangle is (1,2,2,4)-packing colorable.
https://arxiv.org/html/2603.25113v1#S5

Use four labels 0,1,2,3 of respective radii 1,2,2,4. Equal labels must be
at distance strictly greater than their radius. The two radius-two labels
are distinct. The full component classification is proved in PROOF.md:
triangular necklaces/chains, plain paths/cycles, and isolated diamonds.
Two-port triangles have connector lengths at least two. This proof uses
that structural lemma, not its square-coloring conclusion.

## Six boundary states on a necklace

Order each triangle's two ports as left and right. Temporarily use only
labels 0,1,2 on the backbone, the cycle obtained by deleting triangle apices.
The six possible proper port pairs, in fixed order, are

    01, 02, 10, 12, 20, 21.

For pair12 or21, color its apex0. For the other pairs, color its apex3.
Thus each triangle is properly colored. An apex0 has no adjacent label0.
An apex3 has radius4, and apex-to-apex distances across a connector of
length L are L+2. Consequently two adjacent apices3 are forbidden exactly
when L=2. Nonadjacent apices are at least distance7 apart along either
route that passes another triangle; when there are only one or two
triangles, any shorter route is itself an adjacent connector and is checked.

Let P be the Boolean transition matrix on the six pairs. A transition
(a,b) to (b,c) is permitted precisely when the three-vertex path a,b,c
satisfies the packing rules of radii(1,2,2): c differs from b, and if c is
1 or2 it differs from a. A word of such transitions is exactly a legal
backbone coloring. A connector of L edges followed by the next triangle's
port edge advances L+1 transitions between port-pair states.

For L>=3 set R_L=P^(L+1), using Boolean matrix multiplication. For L=2,
start with P^3 and set an entry to zero if both endpoint pair states
contain0 (both corresponding apices would be3). Choosing a closed sequence
of these transitions around the necklace gives a packing coloring of the
ENTIRE graph: triangle apices never shorten distances on the backbone,
there are no radius-two apices, and every new apex constraint was checked.
All cyclic two-step backbone constraints are included by the closed walk.

This restricted model is not universally adequate. For example, the single
connector length4 would ask for a (1,2,2)-coloring of C5, which is impossible.
The retained normal-model probe also found longer zero-trace products.
These are ansatz failures, not graph counterexamples.

## One exceptional connector

Allow at most one length4 connector to have internal labels 0,3,0.
Its endpoint triangles must both have pair12 or21, hence apex0. Let E be
the Boolean relation allowing all four pairs between those two states,
with all other entries zero. The internal3 is at distance3 from each
adjacent apex, whose label is0, so there is no conflict. Any further apex3
is at distance at least6 via either direction. There is at most one such
internal3. The two new internal0 vertices are at distance2 from one another,
and neither has a label0 neighbor. The endpoint radius-two labels are
at distance4 from each other and do not occur inside the connector.
Thus every E transition is safe, including across its neighboring blocks.
For a one-triangle necklace the same triangle occurs at both ends; the
same direct checks apply, and E has permitted diagonal entries.

## Exact finite invariant proves every connector word works

For a processed sequence of connector lengths, let A be its normal
relation, and B the relation allowing exactly one exceptional connector.
Initially A=I, B=0. Appending length L updates

    A' = A R_L,
    B' = B R_L                         if L != 4,
    B' = B R_4 OR A E                  if L = 4.

A nonzero diagonal in either A or B gives a closed boundary-state choice,
hence a coloring. Computation of P^11 gives the all-ones matrix J, and
JP=J. Therefore R_L=J for EVERY L>=10. Only the nine connector types
2,3,...,9,10 (10 representing all larger lengths) need be considered.
The exceptional transition is only for the actual length4.

transfer_certificate.json explicitly lists a set C of 139 pairs (A,B),
encoded as twelve six-bit row masks per pair. verify_transfer.py verifies:

1. The initial pair (I,0) belongs to C.
2. Every member has a nonzero diagonal in A or B.
3. C is closed under each of the nine updates above (1251 transitions).
4. P^11=J and JP=J, establishing the infinite-length reduction.

These finite properties, not a guessed stopping horizon, prove by induction
that EVERY finite connector sequence has a legal closed coloring. The
checker implements Boolean matrix products directly, separate from the
bitmask discovery arithmetic, and rebuilds P using the literal three-path
packing definition. It rejects a missing invariant state and an added
zero-trace state. The actual run passed all checks. This is an executable
finite certificate forming part of the proof, not a finite graph search
extrapolated to arbitrary order.

## Components with ends and elementary exceptions

Any triangle chain other than the component consisting of two triangles
joined directly by one edge can be embedded as a subgraph in a necklace:
use an unused non-port vertex on a cap triangle as a second port; extend
leaf tails by new vertices and new triangles as necessary; then join the
two ends with a sufficiently long connector. Original connectors incident
to internal triangles already have length>=2. Leaf extensions make their
old last vertices degree two, and the added joining path can have length
at least two. This creates an admissible necklace. Restriction of a packing
coloring to the original subgraph is valid, since deleting vertices/edges
cannot shorten original-graph distances. An isolated triangle is immediate.

For two directly joined triangles, denote their respective vertices
(u,v,w) and (x,y,z), with joining edge ux. Assign labels

    (u,v,w,x,y,z) = (0,2,3,1,0,2).

The two0 vertices have distance2 and the two2 vertices distance3; all
other labels occur once. The isolated diamond receives four distinct
labels. An isolated vertex or a path has a coloring obtained by repeating
0,1,2. A plain cycle of order n>=3 can also be handled by adding one new apex
adjacent to the endpoints of one cycle edge. The resulting one-triangle
necklace has connector length n-1>=2 (for n=3 it is a diamond). Apply its
coloring and restrict back to the original cycle. Adding that apex does
not shorten backbone distances, and restriction in any case cannot make
existing distances smaller. This covers all components and proves the theorem.

## Replay and limitations

From the repository root, Python3.12 standard library:

    python workstreams/B/triangle_packing/verify_transfer.py
    python workstreams/B/triangle_packing/construct_second.py

The second program realizes boundary states as explicit original-graph
colorings and checks graph hypotheses and all same-label BFS distances.
Actual replay:864 necklaces, including long connectors and a length-word
that failed the normal ansatz, PASS. A concrete sample is second_sample.json.
These finite graph checks supplement, not replace, the invariant proof.

Certificate SHA256:
f2b7eea0cc18cda9b050d441d459c2a0cae140b33235df8568eebaffd85839d4.
Checker SHA256:
df1d2a96f65fbbdea3b2fac7ae9c6b70fa77058c627e98d35a16772530605c3e.
Actual receipts: transfer_verification.json and second_original_checks.json.
Both implementations are by B; no independent review has occurred yet.
The first palette (1,2,3,3) and Conjecture2 are not settled by this proof.
Historical novelty remains uncertain and no priority claim is made.
