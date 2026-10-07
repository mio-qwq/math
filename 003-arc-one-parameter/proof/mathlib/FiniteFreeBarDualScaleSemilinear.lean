import TwentyDimDualScale
import FiniteFreeBarRecursive
import Mathlib.Algebra.BigOperators.Fin

/-!
# Forward dual scaling on the actual recursive free resolution

For a unit H, each word receives the product of its letter weights and
each full left coefficient is transformed by the actual algebra
automorphism dualScale H. The resulting maps are R-linear and
dualScale-semilinear over A. They commute with coefficient insertion and
every recursively installed boundary, and fix the character augmentation.

This file keeps the full noncommutative A-coefficients. It constructs no
categorical twist functor or Ext action and asserts no complete ARC.
-/

namespace ARCFiniteFreeBarDualScaleSemilinear

open ARCTwentyDimAlgebra ARCTwentyDimCharacters ARCTwentyDimDualScale
open ARCFiniteFreeBarModules ARCFiniteFreeBarAugmentation ARCCharacterModule
open ARCFiniteFreeBarInsertion ARCFiniteFreeBarRecursive
open scoped BigOperators

noncomputable section

section Weights

variable {R : Type*} [CommRing R]

/-- Product of the forward unit weights of every letter in a word. -/
def wordWeight (H : Rˣ) (n : Nat) (w : Word n) : R :=
  ∏ i : Fin n, dualWeight H (w i).val

@[simp] theorem wordWeight_zero (H : Rˣ) (w : Word 0) :
    wordWeight H 0 w = 1 := by
  simp [wordWeight]

/-- The word weight splits into its first letter and complete tail. -/
theorem wordWeight_succ (H : Rˣ) (n : Nat) (w : Word (n + 1)) :
    wordWeight H (n + 1) w =
      dualWeight H (w 0).val * wordWeight H n (Fin.tail w) := by
  exact Fin.prod_univ_succ (fun i : Fin (n + 1) => dualWeight H (w i).val)

@[simp] theorem wordWeight_one (H : Rˣ) (w : Word 1) :
    wordWeight H 1 w = dualWeight H (w 0).val := by
  rw [wordWeight_succ, wordWeight_zero, mul_one]

end Weights

variable {R : Type*} [CommRing R] [CharP R 2]

/-- Full coefficient and word scaling, as a genuine R-linear map. -/
def termScale (q : R) (H : Rˣ) (n : Nat) : BarTerm q n →ₗ[R] BarTerm q n where
  toFun v w := wordWeight H n w • dualScale q H (v w)
  map_add' v v' := by
    funext w
    simp only [Pi.add_apply, map_add, smul_add]
  map_smul' r v := by
    funext w
    change wordWeight H n w • dualScale q H (r • v w) =
      r • (wordWeight H n w • dualScale q H (v w))
    rw [map_smul]
    exact smul_comm ..

@[simp] theorem termScale_apply (q : R) (H : Rˣ) (n : Nat)
    (v : BarTerm q n) (w : Word n) :
    termScale q H n v w = wordWeight H n w • dualScale q H (v w) := rfl

/-- The transformed actual A-valued coefficient has its full twenty coordinates. -/
theorem termScale_coords (q : R) (H : Rˣ) (n : Nat) (v : BarTerm q n)
    (w : Word n) (i : Fin 20) :
    (termScale q H n v w).coords i =
      wordWeight H n w * (dualWeight H i.val * (v w).coords i) := rfl

/-- Semilinearity retains the whole left A coefficient through the automorphism. -/
theorem termScale_algebra_smul (q : R) (H : Rˣ) (n : Nat)
    (a : TableAlgebra q) (v : BarTerm q n) :
    termScale q H n (a • v) = dualScale q H a • termScale q H n v := by
  funext w
  simp only [termScale_apply, barTerm_smul_apply, map_mul]
  exact (table_mul_smul q (wordWeight H n w) (dualScale q H a)
    (dualScale q H (v w))).symm

/-- On an actual free A-basis word, the left coefficient remains scalar. -/
theorem termScale_basis (q : R) (H : Rˣ) (n : Nat) (w : Word n) :
    termScale q H n (wordBasis q n w) = wordWeight H n w • wordBasis q n w := by
  classical
  funext z
  simp only [termScale_apply, wordBasis_apply, Pi.smul_apply]
  by_cases hz : z = w <;> simp [hz]

private theorem dualScale_coordinateBasis_weight (q : R) (H : Rˣ) (i : Fin 20) :
    dualScale q H (coordinateBasis q i) = dualWeight H i.val • coordinateBasis q i := by
  rw [dualScale_basis]
  by_cases hi : i.val < 10 <;> simp [dualWeight, hi]

/-- A basis-letter coefficient and a basis word scale by their product weight. -/
theorem termScale_coordinateBasis_smul_word (q : R) (H : Rˣ) (n : Nat)
    (i : Fin 20) (w : Word n) :
    termScale q H n (coordinateBasis q i • wordBasis q n w) =
      (dualWeight H i.val * wordWeight H n w) •
        (coordinateBasis q i • wordBasis q n w) := by
  rw [termScale_algebra_smul, dualScale_coordinateBasis_weight, termScale_basis]
  calc
    (dualWeight H i.val • coordinateBasis q i) •
        (wordWeight H n w • wordBasis q n w) =
      dualWeight H i.val • (coordinateBasis q i •
        (wordWeight H n w • wordBasis q n w)) := smul_assoc ..
    _ = dualWeight H i.val • (wordWeight H n w •
        (coordinateBasis q i • wordBasis q n w)) := by
      exact congrArg (fun z => dualWeight H i.val • z)
        (smul_comm (coordinateBasis q i) (wordWeight H n w) (wordBasis q n w))
    _ = _ := (mul_smul ..).symm

/-- Naturality of full coefficient insertion on every input and in every degree. -/
theorem termScale_insertion (q : R) (H : Rˣ) (n : Nat) (v : BarTerm q n) :
    termScale q H (n + 1) (coefficientInsertion q n v) =
      coefficientInsertion q n (termScale q H n v) := by
  funext w
  rw [termScale_apply, coefficientInsertion_apply, (dualScale q H).commutes,
    coefficientInsertion_apply, termScale_coords, wordWeight_succ]
  rw [Algebra.smul_def, ← map_mul]
  congr 1
  ring

@[simp] theorem termScale_zeroWord_symm (q : R) (H : Rˣ) (a : TableAlgebra q) :
    termScale q H 0 ((zeroWordEquiv q).symm a) =
      (zeroWordEquiv q).symm (dualScale q H a) := by
  funext w
  simp only [termScale_apply, wordWeight_zero, one_smul, zeroWordEquiv_symm_apply]

private theorem dualScale_fCharacterDefect (q : R) (H : Rˣ) (a : TableAlgebra q) :
    dualScale q H (characterDefect q (fCharacter q) a) =
      characterDefect q (fCharacter q) (dualScale q H a) := by
  simp only [characterDefect_apply, map_sub, (dualScale q H).commutes,
    fCharacter_dualScale]

private theorem termScale_boundary_basis (q : R) (H : Rˣ) (w : Word 1) :
    termScale q H 0 (boundary q (fCharacter q) (wordBasis q 1 w)) =
      boundary q (fCharacter q) (termScale q H 1 (wordBasis q 1 w)) := by
  simp only [termScale_basis, (boundary q (fCharacter q)).map_smul_of_tower,
    boundary_basis, termScale_zeroWord_symm]
  change (zeroWordEquiv q).symm
      (dualScale q H (characterDefect q (fCharacter q) (coordinateBasis q (w 0)))) =
    wordWeight H 1 w • (zeroWordEquiv q).symm
      (characterDefect q (fCharacter q) (coordinateBasis q (w 0)))
  rw [dualScale_fCharacterDefect, dualScale_coordinateBasis_weight,
    map_smul, wordWeight_one]
  exact LinearMapClass.map_smul_of_tower (zeroWordEquiv q).symm _ _

/-- Extend commutation from the whole A-basis to every full A-valued vector. -/
private theorem commutes_of_basis (q : R) (H : Rˣ) (n : Nat)
    (d : BarTerm q (n + 1) →ₗ[TableAlgebra q] BarTerm q n)
    (hd : ∀ w : Word (n + 1),
      termScale q H n (d (wordBasis q (n + 1) w)) =
        d (termScale q H (n + 1) (wordBasis q (n + 1) w)))
    (v : BarTerm q (n + 1)) :
    termScale q H n (d v) = d (termScale q H (n + 1) v) := by
  classical
  have hv : v = ∑ w : Word (n + 1), v w • wordBasis q (n + 1) w := by
    simpa only [wordBasis_repr] using ((wordBasis q (n + 1)).sum_repr v).symm
  calc
    termScale q H n (d v) =
        ∑ w : Word (n + 1), dualScale q H (v w) •
          termScale q H n (d (wordBasis q (n + 1) w)) := by
      conv_lhs => rw [hv]
      rw [map_sum, map_sum]
      simp only [d.map_smul, termScale_algebra_smul]
    _ = ∑ w : Word (n + 1), dualScale q H (v w) •
        d (termScale q H (n + 1) (wordBasis q (n + 1) w)) := by
      simp only [hd]
    _ = d (termScale q H (n + 1) v) := by
      conv_rhs => rw [hv]
      rw [map_sum, map_sum]
      simp only [termScale_algebra_smul, d.map_smul]

/-- Every actual recursive boundary commutes with forward semilinear scaling. -/
theorem termScale_recursiveBoundary (q : R) (H : Rˣ) (n : Nat)
    (v : BarTerm q (n + 1)) :
    termScale q H n (recursiveBoundary q (fCharacter q) n v) =
      recursiveBoundary q (fCharacter q) n (termScale q H (n + 1) v) := by
  induction n with
  | zero =>
      exact commutes_of_basis q H 0 (boundary q (fCharacter q))
        (termScale_boundary_basis q H) v
  | succ n ih =>
      apply commutes_of_basis q H (n + 1)
        (recursiveBoundary q (fCharacter q) (n + 1)) _ v
      intro w
      rw [termScale_basis, (recursiveBoundary q (fCharacter q) (n + 1)).map_smul_of_tower]
      simp only [recursiveBoundary_succ, nextBoundary_basis, map_add, termScale_insertion,
        ih, termScale_coordinateBasis_smul_word]
      simp only [wordWeight_succ]
      rw [(recursiveBoundary q (fCharacter q) n).map_smul_of_tower, map_smul, smul_add]

/-- The actual f-character augmentation is fixed, with identity on its target. -/
theorem augmentation_termScale_zero (q : R) (H : Rˣ) (v : BarTerm q 0) :
    augmentation q (fCharacter q) (termScale q H 0 v) =
      augmentation q (fCharacter q) v := by
  apply CharacterModule.ext
  simp only [augmentation_val, zeroWordEquiv_apply, termScale_apply,
    wordWeight_zero, one_smul, fCharacter_dualScale]

#print axioms wordWeight_succ
#print axioms termScale
#print axioms termScale_coords
#print axioms termScale_algebra_smul
#print axioms termScale_basis
#print axioms termScale_coordinateBasis_smul_word
#print axioms termScale_insertion
#print axioms termScale_zeroWord_symm
#print axioms termScale_recursiveBoundary
#print axioms augmentation_termScale_zero

end
end ARCFiniteFreeBarDualScaleSemilinear
