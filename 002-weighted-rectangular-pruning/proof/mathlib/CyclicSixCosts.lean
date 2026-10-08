import Mathlib.Basic.Real.Basic
import Mathlib.Data.Fin.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-!
# Independent local costs on two cyclic six-cycles

The four tables are simultaneous-translation orbit costs. `Local` is the
twelve representative inequalities of the thirty-six actual conflicts.
The aggregate theorem allows independent nonnegative real tables, including
all zero boundaries. It does not assume coordinate-product factorization.
The actual graph constructions are provided separately in `CyclicSixGraph`.
-/

namespace RectangularPruning.CyclicSixCosts

def total (f : Fin 3 → ℝ) : ℝ := f 0 + f 1 + f 2

def Local (X Y H Z : Fin 3 → ℝ) : Prop :=
  ∀ d, X d * Y d ≤ H d * Z d ∧
    X (d + 1) * Y (d - 1) ≤ H d * Z d ∧
    X (d + 1) * Y d ≤ H d * Z (d + 1) ∧
    X d * Y (d - 1) ≤ H d * Z (d - 1)

/-- A zero-safe version of the two-term geometric-mean estimate. -/
theorem twice_min_le_add (a c u v : ℝ)
    (ha : 0 ≤ a) (hc : 0 ≤ c) (hu : 0 ≤ u) (hv : 0 ≤ v)
    (hproduct : a * c = u * v) : 2 * min a c ≤ u + v := by
  have hm : 0 ≤ min a c := le_min ha hc
  have hmul : min a c * min a c ≤ a * c :=
    mul_le_mul (min_le_left a c) (min_le_right a c) hm ha
  by_contra h
  have hd : 0 < 2 * min a c - (u + v) := by linarith
  have hs : 0 < 2 * min a c + (u + v) := by linarith
  have hp := mul_pos hd hs
  nlinarith [sq_nonneg (u - v)]

/-- A common upper bound exceeds the sum minus the minimum. -/
theorem add_sub_min_le (a c t : ℝ) (ha : a ≤ t) (hc : c ≤ t) :
    a + c - min a c ≤ t := by
  rcases le_total a c with h | h
  · rw [min_eq_left h]
    linarith
  · rw [min_eq_right h]
    linarith

/-- The twelve genuine orbit constraints imply the aggregate product bound. -/
theorem local_aggregate (X Y H Z : Fin 3 → ℝ)
    (hX : ∀ d, 0 ≤ X d) (hY : ∀ d, 0 ≤ Y d)
    (hlocal : Local X Y H Z) : total X * total Y ≤ total H * total Z := by
  have h0 := hlocal 0
  have h1 := hlocal 1
  have h2 := hlocal 2
  norm_num at h0 h1 h2
  obtain ⟨ha0, hc0, hb0, hb2'⟩ := h0
  obtain ⟨ha1, hc1, hb1, hb0'⟩ := h1
  obtain ⟨ha2, hc2, hb2, hb1'⟩ := h2
  have hd0 := add_sub_min_le _ _ _ ha0 hc0
  have hd1 := add_sub_min_le _ _ _ ha1 hc1
  have hd2 := add_sub_min_le _ _ _ ha2 hc2
  have hm0 := twice_min_le_add
    (X 0 * Y 0) (X 1 * Y 2) (X 1 * Y 0) (X 0 * Y 2)
    (mul_nonneg (hX 0) (hY 0)) (mul_nonneg (hX 1) (hY 2))
    (mul_nonneg (hX 1) (hY 0)) (mul_nonneg (hX 0) (hY 2)) (by ring)
  have hm1 := twice_min_le_add
    (X 1 * Y 1) (X 2 * Y 0) (X 2 * Y 1) (X 1 * Y 0)
    (mul_nonneg (hX 1) (hY 1)) (mul_nonneg (hX 2) (hY 0))
    (mul_nonneg (hX 2) (hY 1)) (mul_nonneg (hX 1) (hY 0)) (by ring)
  have hm2 := twice_min_le_add
    (X 2 * Y 2) (X 0 * Y 1) (X 0 * Y 2) (X 2 * Y 1)
    (mul_nonneg (hX 2) (hY 2)) (mul_nonneg (hX 0) (hY 1))
    (mul_nonneg (hX 0) (hY 2)) (mul_nonneg (hX 2) (hY 1)) (by ring)
  dsimp only [total]
  nlinarith only [hd0, hd1, hd2, hm0, hm1, hm2,
    hb0, hb0', hb1, hb1', hb2, hb2']

/-- Scalar three-cover selection, directly including all zero boundaries. -/
theorem scalar_cover_alternative (x y h z : ℝ) (hh : 0 ≤ h)
    (hproduct : x * y ≤ h * z) : x ≤ h ∨ y ≤ h ∨ x + y ≤ h + z := by
  by_cases hx : x ≤ h
  · exact Or.inl hx
  by_cases hy : y ≤ h
  · exact Or.inr (Or.inl hy)
  right; right
  by_contra hbad
  have hx' : 0 < x - h := by linarith
  have hy' : 0 < y - h := by linarith
  have hp := mul_pos hx' hy'
  have ht : 0 ≤ h * (x + y - h - z) := mul_nonneg hh (by linarith)
  nlinarith

/-- At least one of the three actual all-side constructions meets its budget. -/
theorem local_cover_alternative (X Y H Z : Fin 3 → ℝ)
    (hX : ∀ d, 0 ≤ X d) (hY : ∀ d, 0 ≤ Y d)
    (hH : ∀ d, 0 ≤ H d) (hlocal : Local X Y H Z) :
    total X ≤ total H ∨ total Y ≤ total H ∨
      total X + total Y ≤ total H + total Z := by
  apply scalar_cover_alternative
  · exact add_nonneg (add_nonneg (hH 0) (hH 1)) (hH 2)
  · exact local_aggregate X Y H Z hX hY hlocal

end RectangularPruning.CyclicSixCosts

#print axioms RectangularPruning.CyclicSixCosts.twice_min_le_add
#print axioms RectangularPruning.CyclicSixCosts.add_sub_min_le
#print axioms RectangularPruning.CyclicSixCosts.local_aggregate
#print axioms RectangularPruning.CyclicSixCosts.scalar_cover_alternative
#print axioms RectangularPruning.CyclicSixCosts.local_cover_alternative
