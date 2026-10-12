# Universal folding semantics: actual compiled scope

`StrongFold.lean` imports Std only and uses Lean 4.34.1. It supplies the
classical folding/conjugacy correspondence as an actual graph theorem,
rather than assuming that a finite list of permutations is complete.

`BipGraph` contains a symmetric loopless adjacency relation and a Boolean
bipartition. `Switch` requires an involutive adjacency automorphism that
reverses that bipartition and never takes a vertex to a neighbour.
The actual folded vertices are the false-colour representatives of its
two-element orbits. Their adjacency is `adj u (switch v)`.

The file proves this relation symmetric and loopless; constructs mutually
inverse maps from the original graph to the actual canonical double cover
of that folded graph; and proves that they preserve every original
adjacency and intertwine the switch with the canonical deck map.

An isomorphism between two folded graphs is lifted to an actual original
graph automorphism conjugating the switches. Conversely, an adjacency
automorphism conjugating the switches restricts to an isomorphism of the
folds when it preserves colours. For a nonempty connected graph,
`automorphism_colour_uniform` derives the preservation/reversal dichotomy
from graph walks. A reversing conjugator is composed with the target
switch. The final compiled theorem is

```
Struct2.StrongFold.folds_isomorphic_iff_conjugate
```

Its parameters are an arbitrary vertex type, an actual bipartite graph,
two actual switches, one root vertex, and actual walk-connectedness.
Its equivalence ranges over all original-graph adjacency automorphisms,
not only those preserving the given bipartition.

The construction and correspondence are prior graph theory, credited to
Pacco--Scapellato and the framework discussed in Mizzi. The contribution
here is an explicit reusable Lean proof. It does not claim newness of the
classical result.

## Remaining CG-specific bridge

The all-odd source/model isomorphism is now formalized in
`OddCoordinates.lean` and `OddCoverIso.lean`; see `ODD_COVER_SCOPE.md`.
The later `SixCycleInvariant.lean` now proves the universal six-cycle type
invariant and arbitrary-automorphism type preservation; see
`SIX_CYCLE_SCOPE.md`. The remaining universal classification requires proofs of:

1. the full `D_(6n) x C2` automorphism upper bound;
2. the complete strong-guide and conjugacy classification in that group;
3. the other two fold classes and exhaustive ordinary-base classification.

The generic fold semantics removes an actual gap between a group
classification and ordinary base isomorphism classes, but none of those
remaining classification claims is supplied as a formal theorem by this file.
The original `Cg3.lean` stays frozen with its finite scope and receipt.
The later `ModelStructure.lean` proves actual connectedness, strong decks
and recovery of the original graph from its deck fold universally.

Reproduce on an ordinary host:

```
python verify_strong_fold.py --lean /path/to/lean-4.34.1-linux/bin/lean --output-dir /tmp/strong-fold-check
```

On the documented application-path compatibility host, add the same
`--adapter /path/to/runtime_path.so` used by the original finite driver.
The actual new execution and 11 axiom audits are recorded in
`../../verification/20261012-continuation/strong_fold_verification.json`.
No sorry, custom axioms or native_decide occur. The observed axiom union
is `propext` only. No independent human or AI written review of this new
file has been represented as complete.
