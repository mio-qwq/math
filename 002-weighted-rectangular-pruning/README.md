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

The [block and four-path expansion theorem](binary-one-side-costs.md)
now allows the other relation to be any finite relation: it suffices
that each nonisolated component of one relation is a complete
bipartite block or a complete four-path expansion. In particular,
one relation with at most two coordinates on each side suffices,
without any size bound on the other. A coupled high-row deletion and
an effective-cost residual block prove the bound directly for all
nonnegative costs. Complete-rectangle aggregation lifts it to expanded
paths, and disjoint components and zero padding cover arbitrary partial
families. This is a written structural theorem with a finite rational
construction; it does not supply a general optimum or a Lean proof.

The [nested-component theorem](nested-relation-costs.md) removes the
two-layer restriction. Every nonisolated component of either relation
may have arbitrarily many totally nested neighborhood levels, while
the other relation remains arbitrary. A suffix induction pools the
last-corner profit into higher original costs and the last-C charge
into residual H budgets, preserving every local inequality. Its
actual survivor lift includes zero pooled costs and partial families.
The sharp constant-one result has a complete written proof and a
finite rational construction. The case of two relations with
incomparable neighborhoods, the full Lean proof and historical
novelty remain open.

The [right-leaf preservation theorem](right-leaf-extension-costs.md)
also treats some incomparable neighborhoods. Removing all right
degree-one coordinates need only leave nested components; arbitrary
right leaves can be restored, and complete expansions of these
relations are included. The residual problem has partial R families,
reduced H costs and exactly matching coverage on its actual surviving
corners. An oriented five-vertex path with two left and three right
coordinates therefore works against every arbitrary other relation.
More generally, at most two distinct left neighborhoods per component
suffice by splitting right coordinates into the three possible
group-neighbor types. In particular \(|P|\le2\), with I unbounded,
or \(|S|\le2\), with J unbounded, suffices; the other relation is arbitrary.
The theorem includes all zero costs and partial families. It does
not settle two transposed five-vertex paths, all forests or the
unrestricted problem, and is not a Lean proof.

The subsequent [forest theorem](forest-pendant-star-costs.md) closes
the path-orientation and forest gaps of that earlier note. Either
relation can now be any finite bipartite forest, or its complete
expansion, with the other arbitrary. A pendant-star lemma pools
new auxiliary-left costs and H budgets into a partial old-pivot
problem, proves every residual local inequality directly at zeros,
and preserves actual shared-corner coverage. Rooting each tree on
its left side constructs it through finitely many such extensions.
All partial families and path orientations are included; the sharp
constant-one bound has a finite rational construction. This remains
a written theorem without a new Lean or executable-checker result.
Unrestricted cyclic relations, equality cases and global novelty
remain separate research questions.

The [chordal-bipartite theorem](chordal-bipartite-costs.md) now treats
cycles as well: either relation may have no induced cycle of length
at least six, while the other remains arbitrary. A new right
coordinate may attach to several old left coordinates whose old
neighborhoods are nested; other old neighborhoods need no ordering.
Suffix virtual costs and budgets preserve every local inequality,
and a prefix normalization gives an actual survivor lift even
at zero costs. A primary beta-acyclic hypergraph elimination proof
supplies the classical ordering, through an explicit incidence
translation that handles duplicate and isolated neighborhoods.
Four-cycles, partial inputs, complete expansions and the sharp
constant one are included. This is a complete written construction,
with no new Lean compilation or executable-checker claim.
The [question register](../RESEARCH_QUESTIONS.md) records the
unrestricted-relation and first induced-cycle problems separately
from the literature comparison.

The [cyclic six-cycle theorem](cyclic-six-costs.md) now handles a
specified case outside that structural class: both relations are
induced six-cycles and independent nonnegative costs are invariant
under simultaneous cyclic translation. Twelve local inequalities
imply an aggregate product bound and three actual covers give the
sharp coefficient one. An exact nine-expression formula determines
the weighted augmented optimum in this class, without requiring
the local inequalities. A positive infinite family lies outside
common coordinate-product domination, for which an exact criterion
is proved. Invariant partial families are included in the bound;
general asymmetric costs and arbitrary partial patterns remain
unresolved. The [Lean construction](proof/mathlib/README.md) now proves
the full-input invariant cover and actual pruning bounds, including
zeros and the sharp cover coefficient. Its actual graph is linked to
all twelve local orbit constraints. The exact optimum, partial inputs
and domination criterion remain written results.

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
