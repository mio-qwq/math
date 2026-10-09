import Mathlib.Data.Fin.VecNotation
import Mathlib.Data.Fintype.Basic
import Mathlib.Basic.Real.Basic
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-!
Exact algebraic certificate for one seven-cluster substitution profile.
The graph-to-profile reduction and the T9-free classification are written
mathematics, not declarations in this file. No conjecture is resolved here.
-/

namespace ShortCycleSubstitution

noncomputable section

def ratio : ℝ := 260889 / 805108

def mass (w : Fin 7 → ℝ) : ℝ :=
  w 0 + w 1 + w 2 + w 3 + w 4 + w 5 + w 6

def rows (w : Fin 7 → ℝ) : Fin 7 → ℝ :=
  ![(5 / 16) * w 0 + w 1 + w 2,
    (1 / 4) * w 1 + w 2 + w 3,
    (1 / 4) * w 2 + w 3 + w 4,
    (5 / 16) * w 3 + w 4 + w 5,
    (1 / 4) * w 4 + w 5 + w 6,
    (1 / 4) * w 5 + w 6 + w 0,
    (1 / 4) * w 6 + w 0 + w 1]

/-- All seven row lower bounds imply the exact sharp upper bound.
The statement holds for arbitrary real weights; no positivity oracle is used. -/
theorem row_bound (w : Fin 7 → ℝ) (d : ℝ)
    (h : ∀ i, d ≤ rows w i) : d ≤ ratio * mass w := by
  have h0 := h (0 : Fin 7)
  have h1 := h (1 : Fin 7)
  have h2 := h (2 : Fin 7)
  have h3 := h (3 : Fin 7)
  have h4 := h (4 : Fin 7)
  have h5 := h (5 : Fin 7)
  have h6 := h (6 : Fin 7)
  change d ≤ (5 / 16) * w 0 + w 1 + w 2 at h0
  change d ≤ (1 / 4) * w 1 + w 2 + w 3 at h1
  change d ≤ (1 / 4) * w 2 + w 3 + w 4 at h2
  change d ≤ (5 / 16) * w 3 + w 4 + w 5 at h3
  change d ≤ (1 / 4) * w 4 + w 5 + w 6 at h4
  change d ≤ (1 / 4) * w 5 + w 6 + w 0 at h5
  change d ≤ (1 / 4) * w 6 + w 0 + w 1 at h6
  dsimp [ratio, mass]
  linarith only [h0, h1, h2, h3, h4, h5, h6]

def witness : Fin 7 → ℝ :=
  ![27892 / 201277, 29749 / 201277, 26757 / 201277,
    31028 / 201277, 27505 / 201277, 28021 / 201277, 30325 / 201277]

/-- The bound is attained by strictly positive rational cluster proportions. -/
theorem witness_exact : mass witness = 1 ∧
    (∀ i, 0 < witness i) ∧ (∀ i, rows witness i = ratio) := by
  constructor
  · norm_num [mass, witness]
  constructor
  · intro i
    fin_cases i <;> norm_num [witness]
  · intro i
    fin_cases i <;> norm_num [rows, witness, ratio]

/-- The exact bound is strictly below both reference thresholds when mass is positive. -/
theorem strict_thresholds (w : Fin 7 → ℝ) (d : ℝ)
    (h : ∀ i, d ≤ rows w i) (hw : 0 < mass w) :
    d < (21 / 64) * mass w ∧ d < (1 / 3) * mass w := by
  have hb := row_bound w d h
  constructor
  · exact lt_of_le_of_lt hb
      (mul_lt_mul_of_pos_right (by norm_num [ratio]) hw)
  · exact lt_of_le_of_lt hb
      (mul_lt_mul_of_pos_right (by norm_num [ratio]) hw)

end

end ShortCycleSubstitution

#print axioms ShortCycleSubstitution.row_bound
#print axioms ShortCycleSubstitution.witness_exact
#print axioms ShortCycleSubstitution.strict_thresholds
