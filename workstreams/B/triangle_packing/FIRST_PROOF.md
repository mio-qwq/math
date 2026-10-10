# Computer-assisted affirmative answer to Problem 1, first palette

B, 2026-10-10. Mathematical reduction plus finite exact certificate.
Self-verified, pending independent acceptance and novelty review.

## Target

Ayman El Zein and Maidoun Mortada, arXiv:2603.25113v1 (26 March 2026),
Section 5 Problem 1, FIRST question: every finite simple 1-saturated
subcubic graph with each degree-three vertex on a triangle admits a
(1,2,3,3)-packing coloring.
https://arxiv.org/html/2603.25113v1#S5

Labels 0,1,2,3 have respective radii1,2,3,3; equal labels must be at
STRICTLY greater distance than their radius. The two3 labels are distinct.
This is an affirmative proof of the original question, not a counterexample.

Use the structural classification proved in PROOF.md. We first color every
triangle necklace, whose connector lengths are integers at least two.
The elementary components and ends are handled at the end.

## Boundary gadget and compatibility relations

A gadget has five vertices (a,u,z,w,b) and edges au,uz,uw,zw,wb. Thus
u,z,w form a triangle; a,b are the first vertices on its left and right
connectors. Its state is the ordered five-tuple of labels. Retain exactly
the tuples that satisfy all original packing-distance conditions in this
gadget. Exhaustive definition-level enumeration gives 42 states, ordered
lexicographically; no quotient by a claimed symmetry is used.

For a connector of L edges between two triangles, form H_L: the two
triangles, that entire connector, and one pendant neighbor on the OTHER
port of each triangle. The five vertices of each end gadget are present;
when L=2 their connector-neighbor slots refer to the same vertex.
Define R_L(s,t)=1 exactly when H_L admits a packing coloring extending
both states. Shared slots must receive the same label. R_2 and R_3 have
no unfixed vertices once the end states are given, so their entries are
checked directly from the original graph-distance matrices.

A cyclic compatible sequence of states, with an H_L extension on each
connector, gives a coloring of the entire necklace. The states agree on
all shared vertices. Every possible violation has a path of length at
most three between equal-colored vertices. Such a path either lies in
one connector with its end triangles, or crosses one triangle between
its two first connector neighbors. The former lies in some H_L and the
latter in its five-vertex gadget. It cannot traverse two triangle edges
and the connecting path, which would need at least four edges. Thus all
forbidden pairs have been tested locally.

This local argument also covers wraparound: the backbone circumference
is at least four except for the one-triangle length2 necklace. Short
paths lift to the periodic sequence of gadgets without additional
identifications; triangle-internal shortcuts are included in H_L. The
one-triangle length2 graph is a diamond and is handled separately. For
a two-triangle necklace the two outside slots may denote the same vertex
when the other connector has length2; the second relation enforces their
agreement, and any short path using that side is checked there.

## All connector lengths reduce to finitely many relations

Let W be all legal three-letter path colorings over the four labels;
there are 27. Let T be the Boolean matrix that shifts a triple and appends
one label exactly when the resulting FOUR-letter path is packing colored.
Because the largest radius is three, walks in T describe exactly all
legal path colorings, with no omitted long-range condition.

For a gadget state s=(a,u,z,w,b), add a new vertex c adjacent to b.
Check all packing constraints in this SIX-vertex graph. Let F(s,(w,b,c))
be1 exactly for successful choices. These checks incorporate the apex z,
which can be at distance3 from c, as well as every other boundary vertex.
Beyond c the apex is at distance at least4 and has no further effect.
Let B(q,t)=F(reverse(t),reverse(q)), where reversing the five-tuple keeps
its central apex in the central position. For every L>=4,

    R_L = F T^(L-2) B.                         (1)

Indeed the starting triple ends at connector position2, the final triple
at position L, and there are L-2 shifts between them. F and B check the
extra end-apex constraints; T checks the connecting path. This argument
also permits the two constrained ends to overlap when L=4.

The verifier builds these graphs and matrices from their definitions.
It computes T^10=J, the all-ones 27-by-27 matrix, and JT=J. Hence (1)
proves R_L=FJB for EVERY L>=12. Only lengths2,...,12 need be considered,
where12 represents all larger lengths. This is a proved stabilization,
not the observation that a few consecutive experimental matrices agree.

## Finite invariant and induction over arbitrary necklaces

first_invariant.json lists 71 Boolean 42-by-42 matrices C. Each matrix is
encoded by its42 row masks. The checker verifies exactly:

1. Every product R_i R_j, for i,j in {2,...,12}, belongs to C (121 checks).
2. For every A in C and every such R_i, the product A R_i belongs to C
   (781 checks).
3. Every matrix in C has a nonzero diagonal.
4. Every individual R_i for i>=3 has a nonzero diagonal.

By induction every word of at least two connectors has its product in C,
so has a nonzero diagonal. Each one-connector necklace of length>=3 is
covered by item4 and stabilization. A nonzero diagonal gives a closed
sequence of states and actual connector extensions. The sole omitted
one-connector length2 necklace is the diamond, colorable with four distinct
labels. Therefore all triangle necklaces have the requested coloring.

verify_first.py uses sets and direct Boolean relation composition,
separate from discovery bitmask arithmetic. It regenerates the42 gadget
states,27 path states, the short relations, F,T,B, stabilization and all
invariant checks. It also compares the regenerated relations with the
original finite bridge experiment. Missing-invariant and zero-trace
corruptions are rejected. These exact finite calculations are part of a
computer-assisted proof; a bounded search over graphs is not substituted
for induction.

## Other components and original hypotheses

As explained in SECOND_PROOF.md, all triangle chains except the two
cap triangles joined by a single edge embed into a necklace: add long
connectors at unused cap vertices, and extend leaf tails if needed.
Restriction is safe because deleting edges or vertices cannot reduce
distances. For the direct-cap component (u,v,w) and (x,y,z), joined by ux,
assign labels (u,v,w,x,y,z)=(0,1,3,2,0,1). The repeated0 pair is at distance2,
the repeated1 pair at distance3, and the two radius-three labels occur
once. An isolated triangle or diamond uses distinct labels. A plain
cycle embeds into a one-triangle necklace by adding an apex on one edge;
a plain path embeds into a cycle (or can be colored directly). Isolated
vertices are immediate. Apply these colorings to each connected component;
there are no finite intercomponent paths.

All graph hypotheses, not just a minimum-degree-two subclass, are thus
covered. This completes the affirmative answer to the FIRST question.
Together with SECOND_PROOF.md and PROOF.md, all three palettes in Problem1
have separate proof candidates. Conjecture2 is not implied or settled here.

## Actual replay and limitations

Python3.12 standard library, from repository root:

    python workstreams/B/triangle_packing/verify_first.py
    python workstreams/B/triangle_packing/construct_first.py

Actual invariant result: PASS,71 matrices,121 initial products,781 closure
transitions,2 corruptions rejected. Certificate SHA256:
f95da4fd6af446c63c426955f34c4f4fcbf96c2f270c7024aa101fa07b7b3f35.
Checker SHA256:
d82d03ca9d8647b3df1e201be74b3611f3ed058b2534fd9d0d794284777b716c.
Actual original-graph replay:864 necklaces, including connector length23
and a long mixed necklace, colored and checked by BFS, PASS. Receipts:
first_verification.json, first_original_checks.json; sample:first_sample.json.

All research and both code paths are B's own work. No separate agent's
acceptance, Lean compilation, human review or historical firstness is
claimed. The full original-definition semantic reduction above must be
reviewed along with the finite certificate; checking only matrix closure
would not verify that reduction.
