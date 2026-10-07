import FiniteFreeBarModules
import FiniteFreeBarAugmentation
import Mathlib.Data.Fin.Tuple.Basic

/-!
An actual R-linear coefficient-insertion map in every degree. Each
A-valued coefficient is expanded in the full twenty-element R-basis and
inserted as the first word letter, with a central scalar left coefficient.
The installed algebra A remains noncommutative. A-linearity of insertion
is not claimed. This file defines no new differential and proves no
all-degree exactness, projective resolution or Ext comparison.
-/

namespace ARCFiniteFreeBarInsertion

open ARCTwentyDimAlgebra ARCTwentyDimUnit
open ARCFiniteFreeBarModules ARCFiniteFreeBarAugmentation
open scoped BigOperators

variable {R : Type*} [CommRing R] [CharP R 2]

noncomputable section

variable (q : R)

/-- Insert all stored R-coordinates of the left A-coefficient as the first
word letter. The output left coefficient is the actual scalar algebra map. -/
def coefficientInsertion (n : Nat) : BarTerm q n →ₗ[R] BarTerm q (n + 1) where
  toFun v w := algebraMap R (TableAlgebra q) ((v (Fin.tail w)).coords (w 0))
  map_add' v v' := by
    funext w
    change algebraMap R (TableAlgebra q)
        ((v (Fin.tail w) + v' (Fin.tail w)).coords (w 0)) =
      algebraMap R (TableAlgebra q) ((v (Fin.tail w)).coords (w 0)) +
        algebraMap R (TableAlgebra q) ((v' (Fin.tail w)).coords (w 0))
    simp only [coords_add, Pi.add_apply, map_add]
  map_smul' r v := by
    funext w
    change algebraMap R (TableAlgebra q) ((r • v (Fin.tail w)).coords (w 0)) =
      r • algebraMap R (TableAlgebra q) ((v (Fin.tail w)).coords (w 0))
    rw [coords_smul]
    change algebraMap R (TableAlgebra q) (r * (v (Fin.tail w)).coords (w 0)) =
      r • algebraMap R (TableAlgebra q) ((v (Fin.tail w)).coords (w 0))
    rw [map_mul, Algebra.smul_def]

/-- The exact point value at any word, with no support or coefficient bounds. -/
@[simp] theorem coefficientInsertion_apply (n : Nat) (v : BarTerm q n)
    (w : Word (n + 1)) :
    coefficientInsertion q n v w =
      algebraMap R (TableAlgebra q) ((v (Fin.tail w)).coords (w 0)) := rfl

/-- On a displayed first letter and tail, insertion reads exactly that coordinate. -/
@[simp] theorem coefficientInsertion_cons (n : Nat) (v : BarTerm q n)
    (i : Fin 20) (w : Word n) :
    coefficientInsertion q n v (Fin.cons i w) =
      algebraMap R (TableAlgebra q) ((v w).coords i) := by
  simp only [coefficientInsertion_apply, Fin.tail_cons, Fin.cons_zero]

/-- A word is determined by its first letter and its complete tail. -/
theorem word_eq_cons_iff (n : Nat) (z : Word (n + 1)) (i : Fin 20) (w : Word n) :
    z = Fin.cons i w ↔ z 0 = i ∧ Fin.tail z = w := by
  constructor
  · rintro rfl
    simp only [Fin.cons_zero, Fin.tail_cons, and_self]
  · rintro ⟨hi, hw⟩
    have h := Fin.cons_self_tail z
    rw [hi, hw] at h
    exact h.symm

/-- A complete A-valued basis coefficient is transferred, without applying
a character to it or requiring that coefficient to be central. -/
theorem coefficientInsertion_smul_basis_apply (n : Nat) (a : TableAlgebra q)
    (u w : Word n) (i : Fin 20) :
    coefficientInsertion q n (a • wordBasis q n u) (Fin.cons i w) =
      if w = u then algebraMap R (TableAlgebra q) (a.coords i) else 0 := by
  classical
  rw [coefficientInsertion_cons]
  simp only [barTerm_smul_apply, wordBasis_apply]
  by_cases h : w = u <;> simp [h]

/-- On a left A-multiple of any basis word, every one of the twenty stored
R-coordinates occurs in the corresponding first-letter expansion. -/
theorem coefficientInsertion_smul_basis (n : Nat) (a : TableAlgebra q) (w : Word n) :
    coefficientInsertion q n (a • wordBasis q n w) =
      ∑ i : Fin 20, a.coords i • wordBasis q (n + 1) (Fin.cons i w) := by
  classical
  funext z
  simp only [coefficientInsertion_apply, wordBasis_apply,
    Finset.sum_apply, Pi.smul_apply, word_eq_cons_iff]
  by_cases h : Fin.tail z = w <;> simp [h, Algebra.smul_def]

/-- The full finite expansion in every degree retains all original
words and all coordinates of their actual A-valued coefficients. -/
theorem coefficientInsertion_finite_expansion (n : Nat) (v : BarTerm q n) :
    coefficientInsertion q n v =
      ∑ w : Word n, ∑ i : Fin 20,
        (v w).coords i • wordBasis q (n + 1) (Fin.cons i w) := by
  classical
  have hv : v = ∑ w : Word n, v w • wordBasis q n w := by
    simpa only [wordBasis_repr] using ((wordBasis q n).sum_repr v).symm
  calc
    coefficientInsertion q n v =
        coefficientInsertion q n (∑ w : Word n, v w • wordBasis q n w) :=
      congrArg (coefficientInsertion q n) hv
    _ = ∑ w : Word n, coefficientInsertion q n (v w • wordBasis q n w) :=
      map_sum (coefficientInsertion q n) _ Finset.univ
    _ = ∑ w : Word n, ∑ i : Fin 20,
        (v w).coords i • wordBasis q (n + 1) (Fin.cons i w) := by
      simp only [coefficientInsertion_smul_basis]

/-- In this actual algebra the unit is e+f, so inserting a unit basis
coefficient gives exactly the two unit-coordinate first letters. -/
theorem coefficientInsertion_basis (n : Nat) (w : Word n) :
    coefficientInsertion q n (wordBasis q n w) =
      wordBasis q (n + 1) (Fin.cons 0 w) + wordBasis q (n + 1) (Fin.cons 8 w) := by
  classical
  have h := coefficientInsertion_smul_basis q n (1 : TableAlgebra q) w
  simp only [one_smul, coords_one] at h
  rw [h]
  simp only [specialized_unit_coordinates, add_smul, Finset.sum_add_distrib]
  simp

/-- Degree zero agrees with the actual coordinate lift after empty-word evaluation. -/
theorem coefficientInsertion_zero (v : BarTerm q 0) :
    coefficientInsertion q 0 v = coordinateLift q (zeroWordEquiv q v) := by
  funext w
  change algebraMap R (TableAlgebra q) ((v (Fin.tail w)).coords (w 0)) =
    algebraMap R (TableAlgebra q) ((v emptyWord).coords (w 0))
  rw [Subsingleton.elim (Fin.tail w) emptyWord]

#print axioms coefficientInsertion
#print axioms coefficientInsertion_apply
#print axioms coefficientInsertion_cons
#print axioms word_eq_cons_iff
#print axioms coefficientInsertion_smul_basis_apply
#print axioms coefficientInsertion_smul_basis
#print axioms coefficientInsertion_finite_expansion
#print axioms coefficientInsertion_basis
#print axioms coefficientInsertion_zero

end
end ARCFiniteFreeBarInsertion
