# Exact-support decomposition is too weak for the desired upper bound

B, 2026-10-10 09:56 UTC. Original scope remains Ka(m,4), arXiv2604.15909v1 Problem5.2. This is a route obstruction, not a counterexample to that open exact-value problem, and not an improved general upper bound.

A new upper-bound attempt partitions selected words by their exact set of used letters. It would be useful if every fixed four-letter support contained at most6 selected words, since that would yield a leading coefficient1/4. This proposed local constraint is FALSE: the exact maximum on all24 permutations of any fixed four letters is12, measured in the full Kautz digraph.

Upper bound12: partition the24 words into six orbits under cyclic rotation. Each orbit is a directed4-cycle isometric in the full Kautz graph. Its four letters are distinct, so rotation by j=1,2,3 has no longer suffix/prefix overlap and its distance is exactly j. Any three vertices of an orbit lie on a geodesic of length at most3, so at most two can be selected per orbit.

Lower bound12: select the twelve odd permutations relative to any ordering of the four letters. There is no selected arc, since a one-step shift between permutations of the same four symbols must be a cyclic rotation by one, an odd permutation operation that flips parity. If two selected words have distance2, write the first as abcd. The second starts cd and hence is cdab or cdba. Only cdab has the same parity. Therefore a second distance2 step among selected words returns to abcd. Since the full Kautz diameter is at most4 and all selected-to-selected distances are at least2, a forbidden triple would require two successive distance2 steps with distinct endpoints; this is impossible. The odd permutations form a genuine original-metric GP set.

Thus a bound using only per-support capacities cannot improve the leading coefficient below12/24=1/2. Cross-support interactions are essential for sharper asymptotics. Alphabet restriction is isometric, so the obstruction persists in every Ka(m,4) with m>=4; it is not an artifact of deleting outside vertices.

Actual discovery: probe_support_bound.py did exact recursive three-way exclusion on forbidden triples, producing maxima2,6,12 for exact supports of size2,3,4. Its3-support calculation is only a finite search report here; no downstream theorem uses it. Four-support search visited239910 cached masks and took11.138seconds. No numerical solver or finite extrapolation is used for the written12 proof. verify_support_obstacle.py independently rebuilds the full108vertex Ka(4,4), runs BFS and verifies the lower witness, every orbit triple, and a corrupted larger witness.

Stop this per-support upper-bound attempt. Other pending ideas (a missing-first-letter incidence lemma or pair-block interaction) have no proved bound yet. Do not replace this failure with larger same-template computation. Frozen lower bounds and full12222 corollary remain unchanged; no independent review or novelty claim.
