import Mathlib.Basic.Complex.Basic
import Mathlib.LinearAlgebra.Matrix.Circulant
import Mathlib.LinearAlgebra.Matrix.ConjTranspose
import Mathlib.Data.Fintype.BigOperators
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp

/-!
Actual balanced first and cubic characters of a matrix with four circulant
three-by-three blocks. The character sums all six actual columns, using
products of actual entries at the two prescribed row triples. This source
does not derive the block phase-product cancellation from Hadamard Gram
equations; that separate theorem is a written matrix proof.
-/

noncomputable section
open scoped BigOperators

namespace MUBTriplets.CirculantCharacter

abbrev Triple := Fin 3
abbrev Six := Sum Triple Triple

def blockCirculant (a b c e : Triple → ℂ) : Matrix Six Six ℂ :=
  fun i j => match i, j with
  | Sum.inl i, Sum.inl j => Matrix.circulant a i j
  | Sum.inl i, Sum.inr j => Matrix.circulant b i j
  | Sum.inr i, Sum.inl j => Matrix.circulant c i j
  | Sum.inr i, Sum.inr j => Matrix.circulant e i j

def phaseProduct (a : Triple → ℂ) : ℂ := ∏ i, a i

def balancedCharacter (H : Matrix Six Six ℂ) (n : ℕ) : ℂ :=
  ∑ j, ((∏ i : Triple, H (Sum.inl i) j) /
         (∏ i : Triple, H (Sum.inr i) j)) ^ n

theorem circulant_column_product (a : Triple → ℂ) (j : Triple) :
    (∏ i, Matrix.circulant a i j) = phaseProduct a := by
  have hb : Function.Bijective (fun i : Triple => i - j) := by
    constructor
    · intro i k h
      have h' := congrArg (fun x : Triple => x + j) h
      simpa only [sub_add_cancel] using h'
    · intro k
      exact ⟨k + j, by simp⟩
  exact hb.prod_comp a

theorem circulant_row_product (a : Triple → ℂ) (i : Triple) :
    (∏ j, Matrix.circulant a i j) = phaseProduct a := by
  have hb : Function.Bijective (fun j : Triple => i - j) := by
    constructor
    · intro j k h
      have h' := congrArg (fun x : Triple => i - x) h
      simpa only [sub_sub_cancel] using h'
    · intro k
      exact ⟨i - k, by simp⟩
  exact hb.prod_comp a

theorem balanced_character_formula (a b c e : Triple → ℂ) (n : ℕ) :
    balancedCharacter (blockCirculant a b c e) n =
      3 * ((phaseProduct a / phaseProduct c)^n +
           (phaseProduct b / phaseProduct e)^n) := by
  unfold balancedCharacter
  rw [Fintype.sum_sum_type]
  have hl (j : Triple) :
      ((∏ i : Triple, blockCirculant a b c e (Sum.inl i) (Sum.inl j)) /
        (∏ i : Triple, blockCirculant a b c e (Sum.inr i) (Sum.inl j)))^n =
      (phaseProduct a / phaseProduct c)^n := by
    simp only [blockCirculant, circulant_column_product]
  have hr (j : Triple) :
      ((∏ i : Triple, blockCirculant a b c e (Sum.inl i) (Sum.inr j)) /
        (∏ i : Triple, blockCirculant a b c e (Sum.inr i) (Sum.inr j)))^n =
      (phaseProduct b / phaseProduct e)^n := by
    simp only [blockCirculant, circulant_column_product]
  simp_rw [hl, hr]
  simp
  ring

theorem adjoint_balanced_character_formula (a b c e : Triple → ℂ) (n : ℕ) :
    balancedCharacter (blockCirculant a b c e).conjTranspose n =
      3 * ((star (phaseProduct a) / star (phaseProduct b))^n +
           (star (phaseProduct c) / star (phaseProduct e))^n) := by
  unfold balancedCharacter
  rw [Fintype.sum_sum_type]
  have hp (v : Triple → ℂ) (j : Triple) :
      (∏ i, star (Matrix.circulant v j i)) = star (phaseProduct v) := by
    have h := congrArg (starMulAut : ℂ ≃* ℂ) (circulant_row_product v j)
    simpa only [map_prod, starMulAut_apply] using h
  simp only [Matrix.conjTranspose_apply, blockCirculant]
  simp_rw [hp]
  simp
  ring

theorem phaseProduct_ne_zero (a : Triple → ℂ) (ha : ∀ i, a i ≠ 0) :
    phaseProduct a ≠ 0 := by
  exact Finset.prod_ne_zero_iff.mpr (fun i _ => ha i)

theorem first_character_zero_iff (a b c e : Triple → ℂ)
    (hc : phaseProduct c ≠ 0) (he : phaseProduct e ≠ 0) :
    balancedCharacter (blockCirculant a b c e) 1 = 0 ↔
      phaseProduct a * phaseProduct e + phaseProduct b * phaseProduct c = 0 := by
  rw [balanced_character_formula]
  simp only [pow_one]
  constructor
  · intro h
    have hsum : phaseProduct a / phaseProduct c + phaseProduct b / phaseProduct e = 0 :=
      (mul_eq_zero.mp h).resolve_left (by norm_num)
    field_simp [hc, he] at hsum
    simpa only [mul_comm, mul_left_comm, mul_assoc, zero_mul] using hsum
  · intro h
    have hsum : phaseProduct a / phaseProduct c + phaseProduct b / phaseProduct e = 0 := by
      field_simp [hc, he]
      simpa only [mul_comm, mul_left_comm, mul_assoc, zero_mul] using h
    rw [hsum, mul_zero]

theorem cubic_character_zero_of_product_cancel (a b c e : Triple → ℂ)
    (hc : phaseProduct c ≠ 0) (he : phaseProduct e ≠ 0)
    (h : phaseProduct a * phaseProduct e + phaseProduct b * phaseProduct c = 0) :
    balancedCharacter (blockCirculant a b c e) 3 = 0 := by
  have hsum : phaseProduct a / phaseProduct c + phaseProduct b / phaseProduct e = 0 := by
    field_simp [hc, he]
    simpa only [mul_comm, mul_left_comm, mul_assoc, zero_mul] using h
  have hneg : phaseProduct b / phaseProduct e = -(phaseProduct a / phaseProduct c) :=
    eq_neg_of_add_eq_zero_right hsum
  rw [balanced_character_formula, hneg]
  ring

theorem adjoint_cubic_character_zero_of_product_cancel (a b c e : Triple → ℂ)
    (hb : phaseProduct b ≠ 0) (he : phaseProduct e ≠ 0)
    (h : phaseProduct a * phaseProduct e + phaseProduct b * phaseProduct c = 0) :
    balancedCharacter (blockCirculant a b c e).conjTranspose 3 = 0 := by
  have hsb : star (phaseProduct b) ≠ 0 := by simpa using hb
  have hse : star (phaseProduct e) ≠ 0 := by simpa using he
  have hstar := congrArg star h
  simp only [star_add, star_mul, star_zero] at hstar
  have hsum : star (phaseProduct a) / star (phaseProduct b) +
      star (phaseProduct c) / star (phaseProduct e) = 0 := by
    field_simp [hsb, hse]
    simpa only [mul_comm, mul_left_comm, mul_assoc, zero_mul] using hstar
  have hneg : star (phaseProduct c) / star (phaseProduct e) =
      -(star (phaseProduct a) / star (phaseProduct b)) :=
    eq_neg_of_add_eq_zero_right hsum
  rw [adjoint_balanced_character_formula, hneg]
  ring

theorem both_cubic_characters_zero_of_product_cancel (a b c e : Triple → ℂ)
    (hb : ∀ i, b i ≠ 0) (hc : ∀ i, c i ≠ 0) (he : ∀ i, e i ≠ 0)
    (h : phaseProduct a * phaseProduct e + phaseProduct b * phaseProduct c = 0) :
    balancedCharacter (blockCirculant a b c e) 3 = 0 ∧
      balancedCharacter (blockCirculant a b c e).conjTranspose 3 = 0 := by
  exact ⟨cubic_character_zero_of_product_cancel a b c e
      (phaseProduct_ne_zero c hc) (phaseProduct_ne_zero e he) h,
    adjoint_cubic_character_zero_of_product_cancel a b c e
      (phaseProduct_ne_zero b hb) (phaseProduct_ne_zero e he) h⟩

#print axioms balanced_character_formula
#print axioms adjoint_balanced_character_formula
#print axioms first_character_zero_iff
#print axioms cubic_character_zero_of_product_cancel
#print axioms adjoint_cubic_character_zero_of_product_cancel
#print axioms both_cubic_characters_zero_of_product_cancel

end MUBTriplets.CirculantCharacter
