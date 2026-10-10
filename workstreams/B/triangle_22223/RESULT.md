# Conjecture 5 screening checkpoint — not a resolution

B's public reservation05beb022 precedes these computations. Original target remains open in this stream. All work is personal, with no new agents.

- Three-port triangle replacements: 175 presentations across dipole, K4, K3,3, triangular prism and Petersen cores, with uniform and mixed connector lengths, all (2,2,2,2,3)-colorable.
- Distinct boundary mechanism:54 diamond-cap chains and54 leaf-cap chains, all colorable.
- Stronger four radius-two-color route:56 sorted length triples for two triangles,43 colorable and13 noncolorable. All13 admit the original five-color sequence. These are stronger-route obstructions, NOT original conjecture counterexamples.
- A substantive restriction: for two triangles joined at corresponding ports by three length-three paths (12 vertices), every valid original coloring uses at least TWO vertices of the fifth color. Thus B's prior one-exception-per-component mechanism cannot extend to this 2-saturated class.

Exact independent implementation `verify_obstacle.py` builds that graph directly, computes original BFS distances, and exhaustively rejects four-colorings of G^2-v for each of its12 vertices. It constructs an original valid coloring with exactly two distance-three-independent fifth-colored vertices. Run `python workstreams/B/triangle_22223/verify_obstacle.py`; actual PASS recorded in verify_obstacle.log. This establishes the restricted-route obstruction, not a counterexample to Conjecture5. The discovery imports the earlier frozen generic coloring solver; the obstacle verifier does not.

No general theorem, exhaustive class coverage, minimality of graph order, Lean, independent peer acceptance or novelty is claimed. Simple presentations may be isomorphic. Search timeouts were supported but none arose in these runs. Do not repeatedly enlarge this same search: a useful next step needs a mechanism handling multiple separated exceptional vertices, or a new forcing gadget with attachable ports. Without that, this route is paused and B may select another exact unoccupied original target.
