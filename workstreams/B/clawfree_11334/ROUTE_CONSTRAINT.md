# A precise obstruction to simply strengthening the source's matching step

This is a restricted-route characterization, NOT a counterexample to original Problem1.

Let H be a loopless cubic multigraph, T(H) its triangle truncation with unsubdivided joining edges, and I an independent set of core vertices. A 4-packing choosing exactly one vertex in each triangle indexed by I exists if and only if every v in I has a neighbor w with N_H(w) intersect I = {v}. Here neighbors are distinct vertices, even if edges are parallel.

Proof. A candidate vertex in the triangle of v is the port for an edge vw. If w is also adjacent to u in I minus {v}, then this port has distance at most four from EVERY vertex of the triangle of u: one joining edge, one edge inside w's triangle, another joining edge, and at most one edge inside u's triangle. It cannot be selected. Thus a chosen port must point to a private neighbor.

Conversely choose a port toward a private neighbor for each v in I. Any possible path of length at most four between different chosen vertices would need to cross a common intermediate core neighbor w: core vertices in I are not adjacent, and a path crossing three joining edges needs at least two intervening triangle edges, hence length at least five. At a common intermediate neighbor, neither selected port points toward w, since w has at least two neighbors in I. The route therefore needs one extra triangle edge at each endpoint, for total length five. No short conflict is possible.

For example, in H=K3,3 take I to be a full bipartition class. No vertex in I has a private neighbor, so no such 4-packing transversal exists. The original five-color conjecture can still hold: the choice of a fixed independent core class is an extra restriction, not a source hypothesis. Therefore one cannot replace every 3-packing transversal in the August paper's framework by a 4-packing without a new core-class selection or recoloring argument.

Initial original-palette discovery tested114 direct truncation presentations,120 mixed subdivision presentations and20 independently specified edge-sum presentations; all254 were SAT. Six samples were excluded as the named graph H. Counts are presentations, not nonisomorphic classes. No timeouts occurred. The derived private-neighbor restriction gives a concrete reason to stop unchanged enumeration and seek a different matching/odd-cycle interaction mechanism. Original Problem1 remains unresolved in this stream.
