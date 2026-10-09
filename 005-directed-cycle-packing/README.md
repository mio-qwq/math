# Directed cycle packing: a feedback-set obstruction

## Scope and prior work

The original Bermond–Thomassen conjecture says that every finite nonempty
loopless simple digraph with minimum out-degree at least `2k-1` contains
`k` vertex-disjoint directed cycles. Antiparallel arcs are allowed and
two-vertex directed cycles count. The first general unknown case is `k=4`.

The [August 2026 relaxation paper](https://arxiv.org/html/2608.12948v1)
explicitly describes every `k>=4` as unresolved. Its near-directed-cycle
theorem does not prove the original statement. A second
[August 2026 paper](https://arxiv.org/html/2608.20012v1) also records the
original conjecture as open and solves a different length-restricted
existence problem. These are positive recent status statements, not a
guarantee that no subsequent solution exists. The 1981 source is
[Bermond–Thomassen, Cycles in digraphs—a survey](https://doi.org/10.1002/jgt.3190050102);
its original full text was not obtained in this review.

The argument below is a short consequence of classical arc-domination
and minimal-counterexample tools. Those tools appear explicitly in
[Lichiardopol–Pór–Sereni](https://iti.mff.cuni.cz/series/2007/339.pdf),
Property (B) and Lemma 6(ii), and in
[Bucić](https://arxiv.org/pdf/1701.06364v2), Section 3.
The contraction is attributed by the former paper to Thomassen (1983).
Historical novelty of the feedback-set corollary has not been established;
neither it nor the Lean implementation is presented as a first solution
of an open special case.

## Kernel-checked structural statement

Let `D` be a finite nonempty oriented graph. Here oriented means that
`u -> v` forbids `v -> u`, including when `u=v`, so loops are excluded.
Assume every arc `u -> v` has a common predecessor `w` with
`w -> u` and `w -> v`. If every vertex has at least `r>0` distinct
out-neighbors, then every vertex set `S` whose deletion leaves an acyclic
graph satisfies

\[
|S|>r.
\]

The [Lean source](proof/FeedbackCoreObstruction.lean) uses the actual
adjacency relation and actual finite sets of distinct neighbors.
`AcyclicAfterDeletion` forbids a nonempty transitive-closure walk from
a surviving vertex to itself. It does not supply a rank function or
assume a sink; finite acyclicity yields the needed well-founded relations.
The endpoint is `feedback_set_card_gt_min_outdegree`.

Proof: suppose `|S|<=r`. If every vertex belongs to `S`, a vertex has
at most `|S|-1` out-neighbors, a contradiction. Otherwise take a sink
`x` in the finite acyclic graph `D-S`. Its out-neighbors lie in `S`.
Degree and cardinality force `N+(x)=S`. Orientation therefore forces
every predecessor of `x` to lie outside `S`. This predecessor set is
nonempty: dominate any outgoing arc of `x`. Every arc `y -> x` has
a common predecessor, so the induced graph on `N-(x)` has positive
minimum **in-degree**. A finite nonempty graph with this property has
a directed cycle, contradicting acyclicity of `D-S`.

Finiteness, nonemptiness, positive `r`, orientation and arc-domination
are all explicit hypotheses.
For example, an ordinary directed triangle has minimum out-degree one
and a one-vertex feedback set, but its arcs are not dominated.

## Written packing corollary

For a finite nonempty loopless simple digraph, allowing antiparallel
arcs, minimum out-degree at least seven and a feedback vertex set of
size at most seven imply four vertex-disjoint directed cycles.
**This corollary is proved below in writing, not by the Lean endpoint.**

Suppose the corollary fails and choose a counterexample with the fewest
vertices **within this restricted class**. A two-cycle can be removed:
all remaining vertices still have at least five out-neighbors, and the
known Lichiardopol–Pór–Sereni three-cycle theorem supplies three disjoint
cycles, contradicting the supposed absence of four. The counterexample
is therefore oriented.

If an arc `u -> v` has no common predecessor, delete all other outgoing
arcs of `u` and merge `u,v` into `z`. The new vertex inherits exactly
the outgoing neighbors of `v`; its incoming neighbors are the union
of those of `u,v`. Do not inherit all outgoing arcs of both endpoints.
No other vertex points to both endpoints, so it loses no distinct
out-neighbor. Orientation excludes `v -> u`, so `z` also keeps at
least seven out-neighbors. The contracted graph may contain a two-cycle;
the restricted class permits this.

A cycle avoiding `z` remains unchanged. A cycle containing `z` has
one segment `a -> z -> b`. Replace it by `a -> v -> b` if `a -> v`
was present, and otherwise by `a -> u -> v -> b`. All other vertices
of the cycle avoid `u,v`. At most one cycle in a disjoint packing uses
`z`, so this lifts every such packing without losing disjointness.
Consequently, the contracted graph still has no four-cycle packing.

The original feedback set `S` has an image of size at most seven.
If it meets either endpoint, its image contains `z`; deleting that
image leaves a subgraph of the original acyclic remainder. If it
meets neither endpoint, a cycle avoiding its image lifts to a cycle
avoiding `S`, since any inserted `u,v` also avoid `S`. Thus the image
is still a feedback set. The contracted graph belongs to the same
restricted class and has one fewer vertex, a contradiction.

Every arc of the minimal counterexample is therefore dominated.
The structural statement with `r=7` contradicts its feedback set.
This proves the written corollary. The only external packing input is
the already proved three-cycle theorem; the four-cycle target is not
assumed.

## Remaining boundary and reproduction

The general `k=4` conjecture and every possible counterexample with
feedback vertex number at least eight remain untouched. The Lean file
does not formalize the minimal-counterexample choice, contraction,
cycle-packing lift, three-cycle theorem or the written packing corollary.
It does not define the minimum feedback number as a separate function.
Its theorem quantifies over every actual acyclic deletion set instead.

The source was compiled with Lean `4.34.1` and pinned Mathlib
`d13f23b723b8a846827a245b89c10fc7d3f11612`, using the existing shared
Mathlib project. From the repository root:

```sh
cd 002-weighted-rectangular-pruning/proof/mathlib
lake env lean ../../../005-directed-cycle-packing/proof/FeedbackCoreObstruction.lean
```

The source prints its endpoint's axioms. The source-specific
[verification record](results/feedback-core-verification.json) separates
the author run, the independent rerun and mathematical scope review.
No original-conjecture counterexample, complete four-cycle proof or
historical priority is claimed.
