# Real costs and the unbounded two-product obstruction

`SingleConflictReal.lean` proves the complete single-conflict criterion over arbitrary **real** costs, including zero and irrational costs. Cover statements require only a nonnegative corner cost; the pruning equivalence is valid without sign assumptions.

The exact threshold is `min x (min y (x + y - z))`. The file proves both feasibility equivalences, equality of cover and pruning criteria, the exact attained cover minimum, and the concrete `101/100,101/100,1/5,1/5` counterexample as the sum of two explicitly positive product systems.

It further proves **for every real `K ≥ 0`** the existence of two strictly positive coordinate-weight systems whose summed pair costs fail both the cover bound with coefficient K and the pruning bound with coefficient K. The final theorem `no_uniform_constant_positive_systems` includes the actual coordinate systems and summed-cost construction, and quantifies over every cover and every conflict-free pruning. It uses a positive real witness `ε = (4 * (K + 1))⁻¹`; the written proof in `../../boundary.md` additionally chooses rational coordinate weights using an integer larger than K.

The source compiled successfully with Lean 4.34.1 and pinned Mathlib, and every printed axiom audit lists only `propext`, `Classical.choice` and `Quot.sound`. No `sorry`, added axioms or `native_decide` are used. This is a full formal proof of the single-conflict classifications and unbounded obstruction, rather than a numerical test. The general rectangular rank/pruning theorem remains outside this file.

## Replay

From this directory:

```sh
lake exe cache get Mathlib/Basic/Real/Basic.lean Mathlib/Tactic/Linarith.lean Mathlib/Tactic/NormNum.lean Mathlib/Tactic/Ring.lean
lake env lean SingleConflictReal.lean
```

The project pins Mathlib and transitive dependencies in `lake-manifest.json` and pins Lean in `lean-toolchain`. The independent Std natural-cost proof remains at `../SingleConflict.lean`. Provenance of the rectangular argument and the separate weighted extension is identified in `../../paper.md`.
