# Universal connected model, strong deck and original fold

`ModelStructure.lean` extends the all-odd original source/model isomorphism.
It imports only the already supplied Std-based modules and requires no
Mathlib or graph catalogue. All-odd statements use n mod 2 = 1, including
the coordinate-valid n=1 instance; this does not remove its group exception.

## Proved objects and statements

- `modelGraph` is an actual symmetric loopless bipartite graph with the
  proved coordinate adjacency. `actualCoverGraph` is an actual bipartite
  graph with the original CDC adjacency and original Boolean layer colour.
- `originalStrongDeck` and `originalLayerDeck` are actual `Switch` objects:
  involutive, adjacency-preserving, part-reversing and nowhere adjacent to
  their images. Original base looplessness is proved from the literal
  defining edge types and cyclic successor rather than assumed.
- `ring_walk_to_root` constructs graph walks by induction on the ring
  index. Every A, Y and Z vertex is connected to that ring by actual source
  edges. `model_connected` proves walk-connectedness at every odd n.
- `transport_walk` maps actual graph walks along an actual adjacency
  isomorphism. `actualCDC_connected` therefore proves connectedness of the
  original canonical double cover itself for every odd n.
- `originalFoldRecoversCG` is an actual graph isomorphism from the original
  CG adjacency to the fold of the original layer deck. Both inverse laws
  and every adjacency are verified, with no original-base identification
  hypothesis.
- `model_folds_isomorphic_iff_conjugate` instantiates the complete classical
  correspondence on this connected original-defined model. Its conjugators
  are arbitrary actual model adjacency automorphisms. It does not assume
  that all automorphisms belong to a previously named finite group.

## Verification

```
python verify_odd_cover.py --include-structure --lean /path/to/lean-4.34.1-linux/bin/lean --build-dir /tmp/struct2-olean --output-dir /tmp/struct2-structure-receipt
```

The driver rebuilds StrongFold, OddCoordinates, OddCoverIso and
ModelStructure sequentially. The dependency chain has 50 printed axiom
audits (13 in the new module) and uses only the standard propext,
Classical.choice and Quot.sound axioms. No sorry, custom axioms or
native_decide occur. The actual receipt is under
`../../verification/20261013-cg-structure/`.

The parameter proof is constructive at the graph-walk level; finite BFS
experiments are not premises. The independently implemented named-edge
cross-check of the original coordinate bridge has its separate receipt.

## What remains

The universal six-cycle type invariant at n>=3 is now proved in the
separate `SixCycleInvariant.lean` module; see `SIX_CYCLE_SCOPE.md` for its
actual source-transfer and verification scope. The full automorphism upper
bound is now proved in `RingAction.lean` and `CycleRigidity.lean`; see
`UPPER_BOUND_SCOPE.md`. The matching actual family and exact original finite
bijection are now proved in `CycleActions.lean` and `ModelActions.lean`; see
`EXACT_AUTOMORPHISM_SCOPE.md`. Abstract group laws,
exhaustive strong-guide/conjugacy classification and exactly-two
TF-cousin Lean conclusion remain unformalized. The full all-odd written
theorem and its older independent review retain their separate scopes.
This new formal layer does not imply that those remaining statements
have already passed Lean or human peer review.
