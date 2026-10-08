# 002: Product-weighted rectangular pruning

For two arbitrary finite relations, this note proves a product-weighted bound for a vertex cover of the associated conflict/coverage graph. It yields a conflict-free pruning whose deletion cost is charged to cross-corners and points still uncovered. Nonnegative real weights are allowed; rational inputs have a deterministic exact algorithm. The universal coefficient one is sharp.

Read [paper.md](paper.md) for the complete proof, definitions, zero-weight cases, sharpness examples, and provenance. The rank method comes from the [upstream pruning argument](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/A-proof-of-Seymours-second-neighborhood-conjecture-September-23-2026/build/source/02-pruning.tex), independently proved in this note. The product-weighted lifting and exact certificate workflow are the extensions documented here. Literature priority has not been established.

The proof does not assume the upstream second-neighborhood theorem. [Lean proofs](proof/README.md) certify the complete single-conflict criteria, including a [Mathlib real-cost version and unbounded obstruction](proof/mathlib/README.md); the general rectangular theorem remains unformalized.

The [compatible pair-cost construction](compatible-pair-costs.md) proves
a separate general theorem for arbitrary nonnegative pair costs when
either relation is a disjoint union of complete bipartite blocks. Each
conflict need only satisfy the local inequality xy <= hz. A finite
threshold algorithm supplies the cover and pruning bounds, including
zero costs. A tight example has no common dominating product system.
This extension has a complete written proof and an independent exact
certificate checker; it is not Lean-formalized, and sufficiency of the
local condition for arbitrary pairs of relations remains open.

[Two reflexive cost families](reflexive-cost-families.md) now supply
constructions when both relations may be nonblock: arbitrary reflexive
relations on a common complete grid with proportional original tables,
and a nonproportional exchange family on two four-vertex paths. Three
explicit covers suffice for the first family; a weighted local witness
proves that deleting all originals suffices for the second. These written
proofs include zero costs and the actual uncovered sets. They do not
by themselves settle arbitrary independent original costs.

The [binary-coordinate local-cost theorem](double-path-independent-costs.md)
now treats arbitrary independent nonnegative original and corner costs
on two four-vertex paths, assuming only the nine local inequalities.
An exact three-branch formula gives the augmented optimum through at
most fifteen actual deletions. Two coupled scalar deficits prove the
middle parameter region; four finite threshold choices prove the outer
regions. Zero costs are included. Padding partial original families
with zero costs and using the existing block theorem extends this to
every pair of relations when each coordinate set has size at most two.
The coefficient one is sharp. This is a complete written theorem,
not a Lean proof; the arbitrary-relation problem on larger coordinate
sets remains open.

[boundary.md](boundary.md) proves that the product assumption cannot be convexified: a sum of two strictly positive product systems already violates both conclusions on one conflict, and no uniform finite coefficient can repair either extension. The obstruction has exact cover and pruning ratios, and its rational family has a complete written proof. The separate exact checker enumerates all covers and feasible prunings of the displayed numerical instance and checks a matching flow certificate. The finite stress results actually run for the main theorem are recorded in [validation.json](validation.json).

## Reproduce

Python 3.10 or later; standard library only. From this directory:

```text
python code/solve.py examples/sharp.json examples/sharp.certificate.json
python code/check_certificate.py examples/sharp.certificate.json
python code/solve.py examples/rational.json examples/rational.certificate.json
python code/check_certificate.py examples/rational.certificate.json
python code/solve.py examples/zero.json examples/zero.certificate.json
python code/check_certificate.py examples/zero.certificate.json
python code/stress.py
python code/check_nonproduct.py examples/nonproduct.json
python -B code/check_compatible_pair_costs.py examples/compatible-pair-costs.json
python -B code/check_compatible_rectangular.py
python -B code/check_reflexive_cost_families.py examples/reflexive-cost-families.json
python -B code/check_reflexive_independent.py
```

The checker independently rebuilds all conflicts, cross-corners, and network arcs. It verifies exact capacity/conservation constraints, equality of flow value and cover cost, the cover bound, and the pruning bound. A supplied flow and equal-cost cover certify the minimum cover, with no need to trust the search program. These finite checks support reproducibility; the mathematical theorem is proved in `paper.md`.

## Input

Coordinates are integers starting at zero, with sizes specified separately for `P`, `I`, `S`, `J`. Arrays `E`, `F`, `R`, `C` contain relation/family pairs in the order defined in the paper. The four weight arrays `a`, `b`, `c`, `d` contain nonnegative rational strings, such as `"3/7"` or `"0"`. Duplicate pairs are rejected. Example and certificate files are JSON.
