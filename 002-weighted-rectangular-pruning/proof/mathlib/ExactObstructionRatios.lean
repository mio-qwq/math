import SingleConflictReal
import Mathlib.Tactic.FieldSimp

/-!
# Exact critical coefficients for the two-product obstruction

For the two strictly positive coordinate systems
`(ε,1,1,ε)` and `(1,ε,ε,1)`, the summed pair costs are
`x = y = 1 + ε²`, `h = z = 2ε`.

This file proves the exact cover minimum and the necessary-and-sufficient
cover and pruning coefficient formulas for every real `ε > 0` and every
real coefficient `K`, including equality. No approximation, limiting
argument, or finite parameter range is used.

The general rectangular rank/pruning theorem is outside this file.
-/

namespace RectangularPruning.SingleConflictReal

def HasScaledCover (x y h z K : ℝ) : Prop :=
  ∃ r c zl zr : Bool,
    IsCover r c zl zr ∧ coverCost x y z r c zl zr ≤ K * (h + z)

def HasScaledPruning (x y h z K : ℝ) : Prop :=
  ∃ deleteR deleteC : Bool,
    IsConflictFreePruning deleteR deleteC ∧
      deletionCost x y deleteR deleteC ≤
        K * (h + uncoveredCost z deleteR deleteC)

/-- Closed form of the three canonical costs. This is the genuine cover
minimum when epsilon is nonnegative, as required by `cover_cost_iff`. -/
theorem epsilon_minimum_cover (ε : ℝ) :
    minimumCoverCost (1 + ε ^ 2) (1 + ε ^ 2) (2 * ε) = (1 + ε) ^ 2 := by
  have hcomparison : 1 + ε ^ 2 + 2 * ε ≤ (1 + ε ^ 2) + (1 + ε ^ 2) := by
    nlinarith [sq_nonneg (ε - 1)]
  simp only [minimumCoverCost, min_self]
  rw [min_eq_right hcomparison]
  ring

/-- A cover meets the scaled bound exactly at or above this critical coefficient. -/
theorem epsilon_scaled_cover_iff (ε K : ℝ) (hε : 0 < ε) :
    HasScaledCover (1 + ε ^ 2) (1 + ε ^ 2) (2 * ε) (2 * ε) K ↔
      (1 + ε) ^ 2 / (4 * ε) ≤ K := by
  have hz : 0 ≤ 2 * ε := by linarith
  have hden : 0 < 4 * ε := by linarith
  rw [HasScaledCover, cover_cost_iff _ _ _ _ hz, epsilon_minimum_cover]
  rw [div_le_iff₀ hden]
  constructor <;> intro hbound <;> nlinarith

/-- All three feasible prunings have the same exact critical coefficient. -/
theorem epsilon_scaled_pruning_iff (ε K : ℝ) (hε : 0 < ε) :
    HasScaledPruning (1 + ε ^ 2) (1 + ε ^ 2) (2 * ε) (2 * ε) K ↔
      (1 + ε ^ 2) / (2 * ε) ≤ K := by
  have hden : 0 < 2 * ε := by linarith
  rw [div_le_iff₀ hden]
  constructor
  · rintro ⟨deleteR, deleteC, hfree, hcost⟩
    cases deleteR <;> cases deleteC <;>
      simp [IsConflictFreePruning, deletionCost, uncoveredCost] at hfree hcost <;>
      nlinarith
  · intro hbound
    refine ⟨true, false, ?_, ?_⟩
    · simp [IsConflictFreePruning]
    · simpa [deletionCost, uncoveredCost] using hbound

/-- The two thresholds differ by a nonnegative square, with equality at ε = 1. -/
theorem epsilon_critical_coefficient_gap (ε : ℝ) (hε : 0 < ε) :
    (1 + ε ^ 2) / (2 * ε) - (1 + ε) ^ 2 / (4 * ε) =
      (1 - ε) ^ 2 / (4 * ε) := by
  have hne : ε ≠ 0 := ne_of_gt hε
  field_simp [hne]
  ring

theorem epsilon_cover_coefficient_le_pruning (ε : ℝ) (hε : 0 < ε) :
    (1 + ε) ^ 2 / (4 * ε) ≤ (1 + ε ^ 2) / (2 * ε) := by
  have hgap := epsilon_critical_coefficient_gap ε hε
  have hnonneg : 0 ≤ (1 - ε) ^ 2 / (4 * ε) :=
    div_nonneg (sq_nonneg (1 - ε)) (by linarith)
  linarith

/-- The formulas are attached to the actual summed product-cost construction. -/
theorem actual_epsilon_systems_exact_coefficients (ε K : ℝ) (hε : 0 < ε) :
    let w := addCosts (productCosts (epsilonSystem1 ε)) (productCosts (epsilonSystem2 ε))
    (HasScaledCover w.x w.y w.h w.z K ↔ (1 + ε) ^ 2 / (4 * ε) ≤ K) ∧
    (HasScaledPruning w.x w.y w.h w.z K ↔ (1 + ε ^ 2) / (2 * ε) ≤ K) := by
  dsimp only
  rw [epsilon_summed_costs]
  exact ⟨epsilon_scaled_cover_iff ε K hε, epsilon_scaled_pruning_iff ε K hε⟩

end RectangularPruning.SingleConflictReal

#print axioms RectangularPruning.SingleConflictReal.epsilon_minimum_cover
#print axioms RectangularPruning.SingleConflictReal.epsilon_scaled_cover_iff
#print axioms RectangularPruning.SingleConflictReal.epsilon_scaled_pruning_iff
#print axioms RectangularPruning.SingleConflictReal.epsilon_critical_coefficient_gap
#print axioms RectangularPruning.SingleConflictReal.epsilon_cover_coefficient_le_pruning
#print axioms RectangularPruning.SingleConflictReal.actual_epsilon_systems_exact_coefficients
