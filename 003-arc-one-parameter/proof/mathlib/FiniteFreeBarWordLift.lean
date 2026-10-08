import FiniteFreeBarRecursiveContraction
import Mathlib.Algebra.BigOperators.Fin

/-!
Full tensor-coordinate word lifts into the actual recursive finite free
terms. Each input is an arbitrary element of the installed table algebra;
the coefficients are central R-scalars, but the algebra remains
noncommutative. The lift is defined by the actual R-linear insertion.

If adjacent input products and the final character value vanish, its
recursive boundary is the first input acting on the tail lift. This
retains that complete A-valued coefficient. A subsequent A-linear map
to the character module kills it when the first character value also
vanishes. This supplies a nonboundary test, without asserting closure,
a cup-product comparison, higher Yoneda nonvanishing or a full ARC result.
-/

namespace ARCFiniteFreeBarWordLift

open ARCTwentyDimAlgebra ARCFiniteFreeBarModules ARCFiniteFreeBarAugmentation
open ARCFiniteFreeBarInsertion ARCFiniteFreeBarRecursive
open ARCFiniteFreeBarRecursiveContraction ARCCharacterModule
open scoped BigOperators

variable {R : Type*} [CommRing R] [CharP R 2]

noncomputable section

variable (q : R)

/-- Recursively lift all letters using the actual coefficient insertion.
Only insertion's R-linearity is used; no A-linearity is imposed on it. -/
def wordLift : (n : Nat) → (Fin n → TableAlgebra q) → BarTerm q n
  | 0, _ => wordBasis q 0 emptyWord
  | n + 1, x => coefficientInsertion q n
      (x 0 • wordLift n (Fin.tail x))

@[simp] theorem wordLift_zero (x : Fin 0 → TableAlgebra q) :
    wordLift q 0 x = wordBasis q 0 emptyWord := rfl

theorem wordLift_succ (n : Nat) (x : Fin (n + 1) → TableAlgebra q) :
    wordLift q (n + 1) x = coefficientInsertion q n
      (x 0 • wordLift q n (Fin.tail x)) := rfl

@[simp] theorem wordLift_cons (n : Nat) (a : TableAlgebra q)
    (x : Fin n → TableAlgebra q) :
    wordLift q (n + 1) (Fin.cons a x) =
      coefficientInsertion q n (a • wordLift q n x) := by
  simp only [wordLift_succ, Fin.cons_zero, Fin.tail_cons]

/-- Additivity in the displayed first letter, with no expansion of the
word index set. Recursive use supports small finite-support evaluations. -/
theorem wordLift_cons_add (n : Nat) (a b : TableAlgebra q)
    (x : Fin n → TableAlgebra q) :
    wordLift q (n + 1) (Fin.cons (a + b) x) =
      wordLift q (n + 1) (Fin.cons a x) +
        wordLift q (n + 1) (Fin.cons b x) := by
  simp only [wordLift_cons, add_smul, map_add]

/-- R-linearity in the displayed first letter follows from the actual
R/A scalar tower and the R-linear insertion. -/
theorem wordLift_cons_smul (n : Nat) (r : R) (a : TableAlgebra q)
    (x : Fin n → TableAlgebra q) :
    wordLift q (n + 1) (Fin.cons (r • a) x) =
      r • wordLift q (n + 1) (Fin.cons a x) := by
  simp only [wordLift_cons, smul_assoc, map_smul]

@[simp] theorem wordLift_cons_zero (n : Nat) (x : Fin n → TableAlgebra q) :
    wordLift q (n + 1) (Fin.cons 0 x) = 0 := by
  simp only [wordLift_cons, zero_smul, map_zero]

private theorem coords_mul_scalar (a : TableAlgebra q) (r : R) (i : Fin 20) :
    (a * algebraMap R (TableAlgebra q) r).coords i = a.coords i * r := by
  rw [← Algebra.commutes r a, ← Algebra.smul_def, coords_smul]
  change r * a.coords i = a.coords i * r
  exact mul_comm r (a.coords i)

/-- The entire scalar tensor-coordinate formula in every degree.
Its proof uses only centrality of the actual scalar algebra map. -/
theorem wordLift_apply (n : Nat) (x : Fin n → TableAlgebra q) (w : Word n) :
    wordLift q n x w = algebraMap R (TableAlgebra q)
      (∏ i : Fin n, (x i).coords (w i)) := by
  classical
  induction n with
  | zero =>
      rw [wordLift_zero, wordBasis_apply,
        ite_eq_left (Subsingleton.elim w emptyWord)]
      simp
  | succ n ih =>
      simp only [wordLift_succ, coefficientInsertion_apply, barTerm_smul_apply,
        ih, coords_mul_scalar, Fin.prod_univ_succ, Fin.tail]

/-- The finite expansion preserves every word coordinate. It introduces
no support restriction and performs no finite-word enumeration. -/
theorem wordLift_expansion (n : Nat) (x : Fin n → TableAlgebra q) :
    wordLift q n x = ∑ w : Word n,
      (∏ i : Fin n, (x i).coords (w i)) • wordBasis q n w := by
  classical
  simpa only [wordBasis_repr, wordLift_apply, _root_.algebraMap_smul] using
    ((wordBasis q n).sum_repr (wordLift q n x)).symm

/-- On actual coordinate-basis letters the lift is the actual A-basis word. -/
theorem wordLift_coordinateBasis (n : Nat) (w : Word n) :
    wordLift q n (fun i => coordinateBasis q (w i)) = wordBasis q n w := by
  classical
  induction n with
  | zero =>
      rw [wordLift_zero, Subsingleton.elim w emptyWord]
  | succ n ih =>
      change coefficientInsertion q n
        (coordinateBasis q (w 0) • wordLift q n
          (fun i => coordinateBasis q (Fin.tail w i))) = wordBasis q (n + 1) w
      rw [ih, coefficientInsertion_smul_basis]
      have hc (i : Fin 20) :
          (coordinateBasis q (w 0)).coords i = if w 0 = i then 1 else 0 := by
        rw [← coordinateBasis_repr]
        exact (coordinateBasis q).repr_self_apply (w 0) i
      simp only [hc]
      simp

variable (eps : TableAlgebra q →ₐ[R] R)

/-- Evaluation of any actual A-linear character Hom on a full word lift. -/
theorem hom_wordLift_val (n : Nat)
    (phi : BarTerm q n →ₗ[TableAlgebra q] CharacterModule eps)
    (x : Fin n → TableAlgebra q) :
    (phi (wordLift q n x)).val = ∑ w : Word n,
      (∏ i : Fin n, (x i).coords (w i)) * (phi (wordBasis q n w)).val := by
  classical
  change valueLinearEquiv eps (phi (wordLift q n x)) = _
  rw [wordLift_expansion, map_sum, map_sum]
  simp only [phi.map_smul_of_tower, map_smul, valueLinearEquiv_apply, smul_eq_mul]

/-- With zero adjacent products and a zero final character value, the
actual recursive boundary retains precisely its complete first A-coefficient.
The source word itself is not asserted to have zero boundary. -/
theorem recursiveBoundary_wordLift_of_zero_products (n : Nat)
    (x : Fin (n + 1) → TableAlgebra q)
    (hproducts : ∀ i : Fin n, x i.castSucc * x i.succ = 0)
    (hlast : eps (x (Fin.last n)) = 0) :
    recursiveBoundary q eps n (wordLift q (n + 1) x) =
      x 0 • wordLift q n (Fin.tail x) := by
  induction n with
  | zero =>
      rw [wordLift_succ, recursiveBoundary_zero_insertion]
      have hzero : eps (x 0) = 0 := by
        simpa only [Fin.last_zero] using hlast
      have haug : augmentation q eps (x 0 • wordLift q 0 (Fin.tail x)) = 0 := by
        apply CharacterModule.ext
        simpa only [augmentation_val, zeroWordEquiv_apply, wordLift_zero,
          barTerm_smul_apply, wordBasis_apply, ite_true, mul_one, val_zero] using hzero
      rw [haug, map_zero, add_zero]
  | succ n ih =>
      have htail : ∀ i : Fin n,
          Fin.tail x i.castSucc * Fin.tail x i.succ = 0 := by
        intro i
        simpa only [Fin.tail, Fin.castSucc_succ] using hproducts i.succ
      have htailLast : eps (Fin.tail x (Fin.last n)) = 0 := by
        simpa only [Fin.tail, Fin.succ_last] using hlast
      have hfirst : x 0 * Fin.tail x 0 = 0 := by
        simpa only [Fin.castSucc_zero, Fin.tail] using hproducts 0
      rw [wordLift_succ, recursiveBoundary_succ_insertion,
        (recursiveBoundary q eps n).map_smul,
        ih (Fin.tail x) htail htailLast, smul_smul, hfirst, zero_smul,
        map_zero, add_zero]

/-- After evaluation in the actual character module, the remaining
left coefficient vanishes if its character value is zero. This quantifies
all A-linear maps from the full target free term. -/
theorem hom_recursiveBoundary_wordLift_eq_zero (n : Nat)
    (x : Fin (n + 1) → TableAlgebra q)
    (hproducts : ∀ i : Fin n, x i.castSucc * x i.succ = 0)
    (hfirst : eps (x 0) = 0) (hlast : eps (x (Fin.last n)) = 0)
    (phi : BarTerm q n →ₗ[TableAlgebra q] CharacterModule eps) :
    phi (recursiveBoundary q eps n (wordLift q (n + 1) x)) = 0 := by
  rw [recursiveBoundary_wordLift_of_zero_products q eps n x hproducts hlast,
    phi.map_smul]
  apply CharacterModule.ext
  simp only [val_character_smul, hfirst, zero_mul, val_zero]

/-- A nonzero evaluation on such a word excludes every actual preceding
Hom precomposition. Closure and an Ext interpretation are separate obligations. -/
theorem hom_ne_precomp_of_wordLift_val_ne_zero (n : Nat)
    (x : Fin (n + 1) → TableAlgebra q)
    (hproducts : ∀ i : Fin n, x i.castSucc * x i.succ = 0)
    (hfirst : eps (x 0) = 0) (hlast : eps (x (Fin.last n)) = 0)
    (psi : BarTerm q (n + 1) →ₗ[TableAlgebra q] CharacterModule eps)
    (hvalue : (psi (wordLift q (n + 1) x)).val ≠ 0)
    (phi : BarTerm q n →ₗ[TableAlgebra q] CharacterModule eps) :
    psi ≠ phi.comp (recursiveBoundary q eps n) := by
  intro h
  apply hvalue
  rw [h, LinearMap.comp_apply,
    hom_recursiveBoundary_wordLift_eq_zero q eps n x hproducts hfirst hlast phi,
    val_zero]

#print axioms wordLift
#print axioms wordLift_cons_add
#print axioms wordLift_cons_smul
#print axioms wordLift_cons_zero
#print axioms wordLift_apply
#print axioms wordLift_expansion
#print axioms wordLift_coordinateBasis
#print axioms hom_wordLift_val
#print axioms recursiveBoundary_wordLift_of_zero_products
#print axioms hom_recursiveBoundary_wordLift_eq_zero
#print axioms hom_ne_precomp_of_wordLift_val_ne_zero

end
end ARCFiniteFreeBarWordLift
