# Exact connector reduction for the reserved Conjecture5 route

B, 2026-10-10. This concerns ONLY disjoint triangles replacing vertices of a loopless cubic multigraph H, with each core edge replaced by an internally disjoint port-to-port path of length L_e>=2. These graphs satisfy the original 2-saturation and triangle-local hypotheses of arXiv:2603.25113v1 Conjecture5. This is not a classification of all graphs in that conjecture, and does not prove the full conjecture.

## Exact four-square-color boundary model

Use four ordinary radius-two colors. Every triangle uses three distinct colors; write t_v for its unique missing color, and p_(v,e) for its port color on edge e. At the v-end, the first internal path vertex is within distance2 of all three triangle vertices and is therefore FORCED to color t_v.

A connector's color word must consequently start with(p_(v,e),t_v) and end with(t_w,p_(w,e)), with no repetition at distances1 or2 along it. Conversely, any triangle assignments and connector words satisfying these rules give a valid four-square-coloring of the WHOLE original graph. Indeed, a path of length at most2 lies within one triangle/connector neighborhood. Interiors on different connectors have distance at least3; all interior-to-triangle restrictions are precisely the forced missing color at distance1 and the port exclusion at distance2. Core parallel edges create no omitted two-step restrictions because they use distinct ports and L_e>=2.

Thus this is an exact boundary-constraint reduction, not just a sufficient template.

## Consequence A: all connectors of length2

The graph on old triangle vertices with its distance-at-most2 constraints is precisely the triangle expansion T(H), with unsubdivided port edges. T(H) is connected simple cubic, has at least6 vertices, and is not K4. By classical Brooks it is properly3-colorable. Give every new subdivision vertex the fourth color: any two such vertices have distance at least3. This proves four-square-colorability for every such H. Disconnected cores are handled componentwise.

## Consequence B: all connectors of length3

The four-word sequence on e=vw is

    p_(v,e), t_v, t_w, p_(w,e).

It works exactly when t_v!=t_w and each port avoids the opposite missing color. At a core vertex v its three port colors must be the three colors other than t_v, assigned bijectively; port e must also avoid t_w. Such an assignment exists if and only if the three incident neighbor labels are NOT all equal. For sufficiency, each of the three ports has a two-element list inside the three-color palette. Every one- or two-port collection satisfies Hall, and all three lists cover the palette unless their excluded neighbor color is identical. Necessity is immediate.

Therefore the original graph is four-square-colorable exactly when H admits a proper4-coloring whose incident neighbor labels are not monochromatic. Parallel incidences count with multiplicity here.

If connected H is not the two-vertex triple-edge multigraph, its underlying simple graph U has minimum degree at least2 and maximum degree at most3. U cannot be C5: positive integer edge multiplicities x_i on an odd cycle would require x_(i-1)+x_i=3 around the cycle, forcing x_i=3/2. The classical theorem of Lai, Montgomery and Poon gives a dynamic4-coloring of U, and hence the desired port assignment. This is an APPLICATION OF PRIOR THEORY, not a new dynamic-coloring theorem.

The excluded triple-edge core really fails four-square-colorability: both core vertices see just one neighbor label. Its12vertex original expansion was already exactly certified in verify_obstacle.py to need two occurrences of the fifth radius-three color, while satisfying the original(2,2,2,2,3) conjecture. It is not an original counterexample.

## Consequence C: all connectors have length at least7

The12 states are ordered unequal pairs of four colors. Transition(a,b)->(b,c) is allowed exactly when c differs from a,b. Starting from(0,1), the numbers of reachable states after0,1,...,6 transitions are1,2,4,7,10,11,12. A literal reachable-set certificate is emitted by check_short_connectors.py. Color permutation symmetry gives all initial states. Once all12 states are reached, they remain reached because each state has predecessors. Thus after ANY t>=6 transitions every ordered unequal endpoint pair is attainable.

A connector of edge-length L uses L-1 transitions between its prescribed first and last pairs. Therefore L>=7 imposes no restriction on triangle boundary choices. Color each triangle arbitrarily with three of four colors and extend every connector independently; the exact boundary reduction proves validity globally.

## Provenance, limits, and useful restart

Lai, Hong-Jian; Montgomery, Bruce; Poon, Hoifung, *Upper Bounds of Dynamic Chromatic Number*, Ars Combinatoria68 (2003),193–201. Publisher primary PDF/abstract retrieved2026-10-10:
https://combinatorialpress.com/article/ars/Volume%20068/volume-68-paper-20.pdf
Its subcubic dynamic4 bound except a C5 component is imported as a published theorem. A new proof of that theorem is not claimed. Supporting author-maintained reference:
https://www.dwest.web.illinois.edu/regs/dyncol.html

No expensive random search is justified by these uniform-length results. Any new obstruction in the present loopless three-port model must involve mixed short connector constraints, or length4,5,6 constraints not handled above. Loops, two-port direct links, diamonds and other admissible original graphs remain outside these corollaries. Do not infer that no counterexample exists in the original class. The next useful step would be an original-coloring argument that solves the mixed constraints, or a concrete incompatible gadget; simply increasing homogeneous random cores repeats settled cases.


## Actual exact replay, 09:01 UTC

`python workstreams/B/triangle_22223/check_short_connectors.py`: PASS. All literal four-color path words for connector lengths2..7 checked,108 local neighbor-label cases, two negative controls. `python workstreams/B/triangle_22223/check_short_connector_graphs.py`: PASS,24 constructed original graphs and45252 original BFS vertex pairs, including simple cores and parallel-edge even-cycle cores, lengths2,3,7,8. Python3.12.14 stdlib. These tests supplement the universal reduction and imported published theorem; they do not exhaust original Conjecture5.

For mixed lengths2 and3, each length2 edge forces equal missing labels and each length3 edge forces unequal labels. Hence a length3 edge whose endpoints lie in one length2-connected component obstructs four-square-colorability. This explains why the uniform corollaries do not extend automatically. It does not obstruct the original fifth-color palette: fifth-colored triangle vertices or connector vertices invalidate the four-color missing-label model and must be analyzed separately. Do not treat this auxiliary conflict as an original counterexample.
