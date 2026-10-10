# Conjecture 5 screening checkpoint — not a resolution

B's public reservation05beb022 precedes these computations. Original target remains open in this stream. All work is personal, with no new agents.

- Three-port triangle replacements: 175 presentations across dipole, K4, K3,3, triangular prism and Petersen cores, with uniform and mixed connector lengths, all (2,2,2,2,3)-colorable.
- Distinct boundary mechanism:54 diamond-cap chains and54 leaf-cap chains, all colorable.
- Stronger four radius-two-color route:56 sorted length triples for two triangles,43 colorable and13 noncolorable. All13 admit the original five-color sequence. These are stronger-route obstructions, NOT original conjecture counterexamples.
- A substantive restriction: for two triangles joined at corresponding ports by three length-three paths (12 vertices), every valid original coloring uses at least TWO vertices of the fifth color. Thus B's prior one-exception-per-component mechanism cannot extend to this 2-saturated class.

Exact independent implementation `verify_obstacle.py` builds that graph directly, computes original BFS distances, and exhaustively rejects four-colorings of G^2-v for each of its12 vertices. It constructs an original valid coloring with exactly two distance-three-independent fifth-colored vertices. Run `python workstreams/B/triangle_22223/verify_obstacle.py`; actual PASS recorded in verify_obstacle.log. This establishes the restricted-route obstruction, not a counterexample to Conjecture5. The discovery imports the earlier frozen generic coloring solver; the obstacle verifier does not.

No general theorem, exhaustive class coverage, minimality of graph order, Lean, independent peer acceptance or novelty is claimed. Simple presentations may be isomorphic. Search timeouts were supported but none arose in these runs. Do not repeatedly enlarge this same search: a useful next step needs a mechanism handling multiple separated exceptional vertices, or a new forcing gadget with attachable ports. Without that, this route is paused and B may select another exact unoccupied original target.

## Dense-interface route reopening, 2026-10-10 08:25–08:28 UTC

A previously uncovered admissible mechanism was checked: direct edges between TWO-port triangles preserve 2-saturation, unlike direct edges at three-port triangles. Definition-checked direct/mixed necklaces gave263SAT presentations; branching cores with dense direct two-port triangle chains gave200SAT presentations, noUNKNOWN. These are discovery CSP results, not independent proof of the original conjecture.

A separate small-gadget analysis enumerated all legal locations of the radius-three color and exact four-square-colorability of the complement, using ORIGINAL full-graph BFS. Two triangles joined by two paths of lengths2and3 form an attachable nine-vertex gadget that requires the fifth color, but EVERY individual vertex can carry that color in some valid coloring. In particular, a central choice lies at distance2 from BOTH free ports. Thus this gadget does not force its exceptional color near an attachment, and joining copies by admissible length>=2 paths cannot by itself force conflicts between those central choices. This defeats the intended local-density forcing mechanism; it is not an original counterexample or general existence theorem.

Sources/logs: probe_direct_necklaces.py/.log, probe_dense_interfaces.py/.log, probe_twoport_forcing.py/.log. All personally run with Python3.12.14 stdlib; no new agents. The original question remains unresolved. Pause further unchanged necklace/gadget repetition. Restart needs a gadget with genuinely restricted exceptional-color location or a global compatibility obstruction, rather than merely square chromatic number five.
