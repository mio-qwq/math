# Computer-assisted proof candidate for the original five-color conjecture

Agent B, 2026-10-10. Complete mathematical reduction and finite certificate.
B self-review passed; independent acceptance and historical novelty pending.

## Original conjecture and conclusion

Ayman El Zein and Maidoun Mortada, *Impact of local girth on the S-packing
coloring of k-saturated subcubic graphs*, arXiv:2603.25113v1 (26 March 2026),
Section 5 Conjecture 2: if a finite simple subcubic graph is 1-saturated
and its maximum local girth over degree-three vertices is3, its packing
chromatic number is at most5.
https://arxiv.org/html/2603.25113v1#S5

The graph hypotheses mean: maximum degree at most3; each degree-three
vertex has at most one degree-three neighbor; and each degree-three
vertex lies on a triangle. No connectivity or minimum degree is added.
We construct a (1,2,3,4,5)-packing coloring. Internally labels0,...,4 have
radii1,...,5, respectively. Equal label c vertices must be at distance
STRICTLY greater than c+1 in the FULL original graph.

This is an affirmative proof candidate for the ORIGINAL conjecture, not
an original-conjecture counterexample or just a bound on a restricted
search family. The restriction below is on our chosen coloring, not an
extra assumption on the input graph.

## Structural reduction and restricted color placement

The classification proved in PROOF.md applies: components are triangular
chains/necklaces, plain paths/cycles, isolated triangles or diamonds.
In a necklace every connector between triangle ports has length at least2.
We seek a coloring in which label4 (radius5) occurs only at triangle apices,
never on the backbone or connector vertices. Finding such a coloring is
sufficient for the unrestricted conjecture.

The five-vertex gadget (a,u,z,w,b) has edges au,uz,uw,zw,wb. Its apex is z;
a,b are the first connector neighbors of its ports. Enumerate all packing
colorings of this gadget, with labels0,...,3 on a,u,w,b and labels0,...,4
on z. There are90 states, in lexicographic order.

For connector length L define H_L as two triangles joined by that path,
with one pendant outside neighbor on each triangle's other port. Define
R_L(s,t)=1 if H_L has a packing coloring extending the two gadget states,
using label4 only on the two apices. For L=2, the two inside-neighbor slots
refer to the same vertex and their labels must agree. For L=2,3, all
vertices are fixed by the two states, so the matrices follow directly
from original-distance checks without a coloring solver.

## Why local compatibility controls every full-graph distance

For labels0,...,3 a violation has a path of length at most4. A shortest
path never traverses two sides of one triangle, because the third side
shortens it. If it traverses two distinct triangle edges, their connector
has length at least2 and the whole path, of length at least4, is contained
in H_L for those two triangles. Otherwise it lies in one connector and
an end triangle, or crosses a single triangle between its two incident
connectors. In the latter case a length-at-most4 path can extend at most
two edges on one side and one on the other; H_L on the longer side includes
that connector and the outside neighbor on the shorter side. It is
therefore checked in some H_L or its gadget.

The remaining label4 has radius5 and occurs ONLY on apices. Two apices
on adjacent triangles have a route of length L+2, covered by their H_L.
Any route between nonadjacent apices traverses at least two connectors
and an intermediate triangle edge, and has length at least2+2+1+2=7.
Thus no radius-five constraint is omitted. If two triangles are adjacent
on both sides of a short necklace, both connectors are checked.

A closed compatible state sequence and connector extensions consequently
give a full-graph packing coloring. Overlapping outside slots are glued
consistently. Short wraparound paths lift to the periodic chain of gadgets
and are covered by the same H_L argument. The only necklace with backbone
circumference less than4 is a single triangle with connector length2,
namely a diamond; handle it explicitly with four different labels.
The relation may impose additional harmless restrictions on self-copies
in a one-triangle short necklace; the verified diagonal witnesses for
length>=3 show these restrictions still allow a coloring.

## Rigorous treatment of arbitrarily long connectors

Let W consist of all legal FOUR-letter path colorings over labels0,...,3
of radii1,2,3,4. There are48 states. Let T shift a word and append a letter
exactly when the resulting FIVE-letter path is a packing coloring. Since
all these radii are at most4, walks in T describe precisely the legal
long path colorings.

For a gadget state s=(a,u,z,w,b), append two new vertices c,d in a path
b-c-d. Check every original packing constraint in this SEVEN-vertex graph,
with c,d restricted to labels0,...,3. Define F(s,(w,b,c,d))=1 exactly for
successful choices. This includes the distances from the outside vertex a
and the apex z to c,d. Further connector vertices are at distance at least5
from z, so cannot conflict with z if its radius is at most4; if z is label4,
they cannot conflict because label4 is prohibited on the connector.

Set B(q,t)=F(reverse(t),reverse(q)). For every L>=4 we then have

    R_L = F T^(L-3) B.                          (1)

The first four-letter state ends at connector position3, the last at
position L, so there are L-3 shifts. F and B check the two end neighborhoods;
T checks the path between them. For L=4,5 the constrained ends overlap,
which is allowed and enforced by the overlapping word states. The two
apices are at distance L+2>=6, so they have no untested mutual constraint.

The verifier computes M=T^13 and checks MT=M, or equivalently T^14=T^13.
Induction then gives T^n=M for every n>=13. Thus (1) proves R_L=FMB for
EVERY L>=16. Importantly M is NOT claimed to be the all-ones matrix;
some locally legal path states do not extend. Observing several equal
experimental relations would not prove stabilization; MT=M does.

## Finite certificate and induction over all necklaces

Use lengths2,...,16, with16 representing every larger length. The file
five_invariant.json encodes a set C of139 Boolean90-by-90 matrices. The
checker reconstructs the gadget/path states and all R_L from the preceding
definitions, then verifies:

1. Every two-connector product R_i R_j belongs to C (225 checks).
2. Every A in C remains in C after right multiplication by any R_i
   (2085 closure checks).
3. Every A in C has a nonzero diagonal.
4. Each individual R_i for i>=3 has a nonzero diagonal.
5. The exact stabilization identity MT=M used for all larger lengths.

By induction every connector word with at least two letters has its
product in C. Nonzero diagonal supplies a closed compatible boundary-state
sequence and connector witnesses. Item4 handles one-connector necklaces
of lengths>=3; the length2 diamond has four distinct colors. This proves
five-colorability for every necklace, with no bound on its number of
triangles or connector lengths.

The certificate is compactly encoded as base64 of zlib-compressed UTF-8
JSON, with a recorded SHA256 of the decoded JSON. Its decoded matrices
are explicit90-row lists of bitmasks. verify_five.py verifies the hash,
uses set-based Boolean relation composition instead of discovery bitmask
multiplication, and rejects both a missing matrix and a zero-trace matrix.
The encoding is ordinary reversible storage, not an oracle or assumption.

## All remaining components

The necklace-embedding argument in SECOND_PROOF.md covers chains with
triangle or leaf ends, except two cap triangles joined directly by one
edge. Adding sufficiently long connectors at unused cap vertices and
extending leaf tails produces an admissible necklace; restriction cannot
shorten original distances. For the direct-cap exception, triangles
(u,v,w),(x,y,z) joined by ux receive labels

    (u,v,w,x,y,z)=(0,1,3,2,0,1).

The repeated0 vertices are at distance2 and repeated1 vertices at distance3;
labels2,3 occur once. Hence this already uses only the first four packing
colors. An isolated triangle or diamond uses distinct labels. Plain cycles
embed into one-triangle necklaces by adding an apex on one edge; paths
embed into cycles, and isolated vertices are immediate. Color components
separately: there are no finite paths between them.

All original hypotheses and all components have been covered. Therefore
chi_rho(G)<=5, as conjectured. QED, subject to independent review of the
mathematical reductions and the accompanying exact finite certificate.

## Actual reproducibility, failure history and scope

Python3.12 standard library, repository root:

    python workstreams/B/triangle_packing/verify_five.py
    python workstreams/B/triangle_packing/construct_five.py
    python workstreams/B/triangle_packing/five_boundary_checks.py

Actual invariant result:139 matrices,90 boundary states,48 path states,
225 initial products,2085 closure transitions and both negative controls
PASS. The independently written graph checker verifies864 constructed
necklaces by full BFS, plus33 boundary fixtures including paths, cycles,
direct caps, leaf ends and disconnected graphs. Three damaged graph/color
certificates are rejected, including two nearby vertices of color5.

The initial attempt to reuse the four-label sample checker rejected label4
because that checker was intentionally restricted to four labels. A separate
full five-label original-graph checker was written and actually rerun; this
was a checker-interface limitation, not a graph counterexample. The early
idea that the path matrix becomes all-ones was also rejected; the actual
verified statement is T^14=T^13, as used above.

Certificate SHA256:
27882d4e867f155012ecb847483bf0d3ddde9129744397946970718a4fcf8ca6.
Checker SHA256:
68266f6722b2dd9eb5c6d3c0d0c6f36c1727632c0071e59f31bba487c106a333.
Receipts:five_verification.json, five_original_checks.json,
five_boundary_results.json. Concrete sample:five_sample.json.

B wrote both implementations personally. This is self-verification, not an
independent review or Lean compilation. Human responsibility review and
historical novelty remain pending. No exact packing chromatic numbers,
classification of optimal colorings, world-first claim or signed release
is asserted. The finite certificate proves the stated invariant; the
original-graph semantic bridge above must be reviewed separately.
