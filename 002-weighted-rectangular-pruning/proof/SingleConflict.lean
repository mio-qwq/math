import Std

/-!
# Arbitrary scaled costs in a single rectangular conflict

The augmented graph is the path `zl -- c -- r -- zr`.
Its original members have costs `x` and `y`; both copies of the corner
have cost `z`. The other cross-corner has cost `h`.

All parameters are arbitrary natural numbers, so nonnegative rational
costs are covered after multiplication by a common denominator.
This file proves the exact cover and pruning criteria, and the scaled
strictly-positive nonproduct counterexample. It does not formalize the
general rectangular rank/pruning theorem.

No `sorry`, added axiom, or `native_decide` is used. The only imports are
Lean's standard library; arithmetic goals are closed by kernel-checked
`omega` proofs.
-/

namespace RectangularPruning.SingleConflict

/-- The three graph edges must each meet the chosen cover. -/
def IsCover (r c zl zr : Bool) : Prop :=
  (r || c) = true ∧ (r || zr) = true ∧ (zl || c) = true

/-- Each Boolean indicates whether its named vertex is selected. -/
def coverCost (x y z : Nat) (r c zl zr : Bool) : Nat :=
  (if r then x else 0) + (if c then y else 0) +
  (if zl then z else 0) + (if zr then z else 0)

/-- An exact criterion for a cover below the cross-corner budget. -/
theorem cover_iff (x y h z : Nat) :
    (∃ r c zl zr : Bool,
      IsCover r c zl zr ∧ coverCost x y z r c zl zr ≤ h + z) ↔
    x ≤ h ∨ y ≤ h ∨ x + y ≤ h + z := by
  constructor
  · rintro ⟨r, c, zl, zr, hcover, hcost⟩
    cases r <;> cases c <;> cases zl <;> cases zr <;>
      simp [IsCover, coverCost] at hcover hcost <;> omega
  · intro hcriterion
    rcases hcriterion with hx | hy | hxy
    · refine ⟨true, false, true, false, ?_, ?_⟩
      · simp [IsCover]
      · simp [coverCost]
        omega
    · refine ⟨false, true, false, true, ?_, ?_⟩
      · simp [IsCover]
      · simp [coverCost]
        omega
    · refine ⟨true, true, false, false, ?_, ?_⟩
      · simp [IsCover]
      · simpa [coverCost] using hxy

/-- A Boolean records deletion of its original member. -/
def IsConflictFreePruning (deleteR deleteC : Bool) : Prop :=
  (deleteR || deleteC) = true

def deletionCost (x y : Nat) (deleteR deleteC : Bool) : Nat :=
  (if deleteR then x else 0) + (if deleteC then y else 0)

/-- The corner is uncovered precisely when both original members are deleted. -/
def uncoveredCost (z : Nat) (deleteR deleteC : Bool) : Nat :=
  if deleteR && deleteC then z else 0

/-- The exact pruning criterion agrees with the exact cover criterion. -/
theorem pruning_iff (x y h z : Nat) :
    (∃ deleteR deleteC : Bool,
      IsConflictFreePruning deleteR deleteC ∧
      deletionCost x y deleteR deleteC ≤ h + uncoveredCost z deleteR deleteC) ↔
    x ≤ h ∨ y ≤ h ∨ x + y ≤ h + z := by
  constructor
  · rintro ⟨deleteR, deleteC, hfree, hcost⟩
    cases deleteR <;> cases deleteC <;>
      simp [IsConflictFreePruning, deletionCost, uncoveredCost] at hfree hcost <;> omega
  · intro hcriterion
    rcases hcriterion with hx | hy | hxy
    · refine ⟨true, false, ?_, ?_⟩
      · simp [IsConflictFreePruning]
      · simpa [deletionCost, uncoveredCost] using hx
    · refine ⟨false, true, ?_, ?_⟩
      · simp [IsConflictFreePruning]
      · simpa [deletionCost, uncoveredCost] using hy
    · refine ⟨true, true, ?_, ?_⟩
      · simp [IsConflictFreePruning]
      · simpa [deletionCost, uncoveredCost] using hxy

/-- Cover feasibility and pruning feasibility coincide for every scaled budget. -/
theorem cover_iff_pruning (x y h z : Nat) :
    (∃ r c zl zr : Bool,
      IsCover r c zl zr ∧ coverCost x y z r c zl zr ≤ h + z) ↔
    (∃ deleteR deleteC : Bool,
      IsConflictFreePruning deleteR deleteC ∧
      deletionCost x y deleteR deleteC ≤ h + uncoveredCost z deleteR deleteC) :=
  (cover_iff x y h z).trans (pruning_iff x y h z).symm

/-- The nonproduct boundary costs, multiplied by 100, admit no affordable cover. -/
theorem nonproduct_no_cover :
    ¬ (∃ r c zl zr : Bool,
      IsCover r c zl zr ∧ coverCost 101 101 20 r c zl zr ≤ 20 + 20) := by
  rw [cover_iff]
  omega

/-- The same boundary costs admit no pruning satisfying the proposed budget. -/
theorem nonproduct_no_pruning :
    ¬ (∃ deleteR deleteC : Bool,
      IsConflictFreePruning deleteR deleteC ∧
      deletionCost 101 101 deleteR deleteC ≤ 20 + uncoveredCost 20 deleteR deleteC) := by
  rw [pruning_iff]
  omega

end RectangularPruning.SingleConflict

#print axioms RectangularPruning.SingleConflict.cover_iff
#print axioms RectangularPruning.SingleConflict.pruning_iff
#print axioms RectangularPruning.SingleConflict.cover_iff_pruning
#print axioms RectangularPruning.SingleConflict.nonproduct_no_cover
#print axioms RectangularPruning.SingleConflict.nonproduct_no_pruning
