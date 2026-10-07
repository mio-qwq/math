# Lean: exact single-conflict cover and pruning criteria

`SingleConflict.lean` is a kernel-checked proof of the arbitrary-cost, single-conflict classification in `boundary.md`. It uses Lean 4.34.1 and the standard library (`import Std`), with no Mathlib dependency.

For **every** `x y h z : Nat`, it proves:

* a cover of the path `zl -- c -- r -- zr`, with original costs `x,y` and two corner costs `z`, has total cost at most `h + z` if and only if `x ≤ h ∨ y ≤ h ∨ x + y ≤ h + z`;
* a conflict-free pruning has deletion cost at most `h` plus the actual uncovered-corner cost if and only if the same condition holds;
* the cover and pruning feasibility conditions are equivalent;
* at the scaled boundary costs `x = y = 101`, `h = z = 20`, neither condition is feasible.

The Booleans in `IsCover` denote selection into the cover. The two Booleans in `IsConflictFreePruning` instead denote deletion of the original members. `uncoveredCost` charges `z` exactly when both originals are deleted. Nonnegative rational costs are included mathematically by scaling them to natural numbers with a common denominator; the Lean statements themselves quantify over natural costs.

The proof exhausts the 16 cover selections and four deletion selections, but its arithmetic parameters remain universally quantified. Each remaining arithmetic implication is proved by the kernel-checked `omega` tactic. This is a general classification, rather than only a check of the numerical example.

The source uses no `sorry`, added axiom, or `native_decide`. Its five `#print axioms` commands report only Lean's standard `propext` and `Quot.sound` axioms. Successful compilation and axiom reports are recorded in [compile-output.txt](compile-output.txt).

## Reproduce

The repository's `lean-toolchain` pins Lean 4.34.1. From the repository root on this Windows workspace:

```powershell
& 'C:\Users\Administrator\.elan\bin\lean.exe' '002-weighted-rectangular-pruning\proof\SingleConflict.lean'
```

With an equivalent Lean installation on other platforms, from the repository root:

```text
lean 002-weighted-rectangular-pruning/proof/SingleConflict.lean
```

**Scope:** this formalizes the one-conflict exact classification and the scaled nonproduct obstruction. It does not formalize the arbitrary rectangular rank argument, weighted cover theorem, or general pruning theorem in `paper.md`.
