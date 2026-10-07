import SingleConflictReal
import Mathlib.Algebra.Order.Archimedean.Real.Basic

/-!
The unbounded obstruction with an actual rational coordinate witness.
For every real finite coefficient K >= 0, the Archimedean property supplies
a positive integer n > K and the rational epsilon = 1/(4*n).
The proof checks every cover and every conflict-free pruning directly.
-/

namespace RectangularPruning.SingleConflictReal

/-- All coordinates of the two systems are the rational numbers q and one. -/
theorem no_uniform_constant_rational_systems (K : ℝ) (hK : 0 ≤ K) :
    ∃ q : ℚ, 0 < q ∧
      let u := epsilonSystem1 (q : ℝ)
      let v := epsilonSystem2 (q : ℝ)
      let w := addCosts (productCosts u) (productCosts v)
      PositiveCoordinates u ∧ PositiveCoordinates v ∧
      (∀ r c zl zr : Bool, IsCover r c zl zr →
        K * (w.h + w.z) < coverCost w.x w.y w.z r c zl zr) ∧
      (∀ deleteR deleteC : Bool, IsConflictFreePruning deleteR deleteC →
        K * (w.h + uncoveredCost w.z deleteR deleteC) <
          deletionCost w.x w.y deleteR deleteC) := by
  obtain ⟨n, hn⟩ := exists_nat_gt K
  have hnpos : 0 < (n : ℝ) := lt_of_le_of_lt hK hn
  let q : ℚ := (4 * (n : ℚ))⁻¹
  let ε : ℝ := q
  have hcast : ε = (4 * (n : ℝ))⁻¹ := by simp [ε, q]
  have hd : 0 < 4 * (n : ℝ) := by linarith
  have hε : 0 < ε := by rw [hcast]; exact inv_pos.mpr hd
  have hqreal : (0 : ℝ) < (q : ℝ) := hε
  have hq : 0 < q := by exact_mod_cast hqreal
  have hid : (4 * (n : ℝ)) * ε = 1 := by
    rw [hcast]
    exact mul_inv_cancel₀ (ne_of_gt hd)
  have hcoverBudget : K * (2 * ε + 2 * ε) < 1 := by
    nlinarith [mul_pos (sub_pos.mpr hn) hε]
  have hpruneBudget : K * (2 * ε) < 1 := by nlinarith
  obtain ⟨hfirst, hsecond⟩ := epsilon_systems_positive ε hε
  refine ⟨q, hq, ?_⟩
  dsimp only
  rw [epsilon_summed_costs]
  refine ⟨hfirst, hsecond, ?_, ?_⟩
  · intro r c zl zr hcover
    cases r <;> cases c <;> cases zl <;> cases zr <;>
      simp [IsCover, coverCost] at hcover ⊢ <;> nlinarith [sq_nonneg ε]
  · intro deleteR deleteC hfree
    cases deleteR <;> cases deleteC <;>
      simp [IsConflictFreePruning, deletionCost, uncoveredCost] at hfree ⊢ <;>
      nlinarith [sq_nonneg ε]

#print axioms no_uniform_constant_rational_systems

end RectangularPruning.SingleConflictReal
