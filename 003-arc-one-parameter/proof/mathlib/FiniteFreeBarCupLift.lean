import FiniteFreeBarRecursiveContraction
import FiniteFreeBarRecursiveLowDegrees

/-!
An explicit suffix lift of the fixed scalar f-character three-cocycle.
Every map P(n+3) -> Pn is extended A-linearly from the complete actual
free basis. The full left A-coefficients are retained. Compatibility with
the R-linear coefficient insertion proves all adjacent lift equations.

Its degree-three component followed by the fixed cocycle is a genuine
degree-six module Hom, closed on the whole actual recursive resolution.
No shifted-complex assembly, Yoneda product identification, nonvanishing,
all-degree self-Ext profile or complete ARC result is asserted here.
-/

namespace ARCFiniteFreeBarCupLift

open ARCTwentyDimAlgebra ARCTwentyDimCochainAlgebra ARCTwentyDimAssociativity
open ARCTwentyDimCharacters ARCCharacterModule ARCFiniteFreeBarModules
open ARCFiniteFreeBarAugmentation ARCFiniteFreeBarInsertion ARCFiniteFreeBarRecursive
open ARCFiniteFreeBarRecursiveContraction ARCFiniteFreeBarRecursiveLowDegrees
open ARCFiniteFreeBarCochains ARCFiniteFreeBarDegreeFour ARCCochainWordEquiv
open scoped BigOperators

variable {R : Type*} [CommRing R] [CharP R 2]

noncomputable section

/-- Keep the first n actual coordinate labels. -/
def prefixWord : (n : Nat) → Word (n + 3) → Word n
  | 0, _ => emptyWord
  | n + 1, w => Fin.cons (w 0) (prefixWord n (Fin.tail w))

variable (q : R)

/-- Evaluate the fixed actual cocycle on precisely the last three letters. -/
def suffixValue : (n : Nat) → Word (n + 3) → R
  | 0, w => actualfSimpleP q (coordinateBasis q (w 0))
      (coordinateBasis q (w 1)) (coordinateBasis q (w 2))
  | n + 1, w => suffixValue n (Fin.tail w)

/-- The actual A-linear suffix map; its scalar coefficient uses the
retained R/A scalar tower, without commutativity of A. -/
def suffixLift (n : Nat) :
    BarTerm q (n + 3) →ₗ[TableAlgebra q] BarTerm q n :=
  (wordBasis q (n + 3)).constr R (fun w =>
    suffixValue q n w • wordBasis q n (prefixWord n w))

/-- The formula on the entire exhibited free basis. -/
theorem suffixLift_basis (n : Nat) (w : Word (n + 3)) :
    suffixLift q n (wordBasis q (n + 3) w) =
      suffixValue q n w • wordBasis q n (prefixWord n w) :=
  (wordBasis q (n + 3)).constr_basis R _ w

/-- Prepending a label leaves the full suffix value unchanged. -/
theorem suffixLift_cons_basis (n : Nat) (i : Fin 20) (w : Word (n + 3)) :
    suffixLift q (n + 1) (wordBasis q (n + 4) (Fin.cons i w)) =
      suffixValue q n w • wordBasis q (n + 1) (Fin.cons i (prefixWord n w)) := by
  rw [suffixLift_basis]
  simp only [suffixValue, prefixWord, Fin.cons_zero, Fin.tail_cons]

private theorem prefixWord_one (w : Word 4) :
    prefixWord 1 w = oneWord (w 0) := by
  funext i
  have hi : i = (0 : Fin 1) := Subsingleton.elim _ _
  subst i
  rfl

private theorem prefixWord_three (w : Word 6) :
    prefixWord 3 w = word3 (w 0) (w 1) (w 2) := by
  change prefixWord 3 w =
    word3 ((prefixWord 3 w) 0) ((prefixWord 3 w) 1) ((prefixWord 3 w) 2)
  exact (word3_eta (prefixWord 3 w)).symm

private theorem suffixValue_word3 (a b c : Fin 20) :
    suffixValue q 0 (word3 a b c) =
      actualfSimpleP q (coordinateBasis q a) (coordinateBasis q b)
        (coordinateBasis q c) := rfl

private theorem scalar_first_expansion (x y z : TableAlgebra q) :
    actualfSimpleP q x y z = ∑ i : Fin 20,
      x.coords i • actualfSimpleP q (coordinateBasis q i) y z := by
  conv_lhs => rw [basis_expansion q x]
  simp only [map_sum, map_smul, LinearMap.sum_apply, LinearMap.smul_apply]

private theorem scalar_second_expansion (x y z : TableAlgebra q) :
    actualfSimpleP q x y z = ∑ i : Fin 20,
      y.coords i • actualfSimpleP q x (coordinateBasis q i) z := by
  conv_lhs => rw [basis_expansion q y]
  simp only [map_sum, map_smul, LinearMap.sum_apply, LinearMap.smul_apply]

private theorem scalar_third_expansion (x y z : TableAlgebra q) :
    actualfSimpleP q x y z = ∑ i : Fin 20,
      z.coords i • actualfSimpleP q x y (coordinateBasis q i) := by
  conv_lhs => rw [basis_expansion q z]
  simp only [map_sum, map_smul]

private theorem scalar_product_first (a b c d : Fin 20) :
    (∑ j : Fin 20, specializedConstants q a b j *
      actualfSimpleP q (coordinateBasis q j) (coordinateBasis q c)
        (coordinateBasis q d)) =
      actualfSimpleP q (coordinateBasis q a * coordinateBasis q b)
        (coordinateBasis q c) (coordinateBasis q d) := by
  have h := scalar_first_expansion q
    (coordinateBasis q a * coordinateBasis q b) (coordinateBasis q c) (coordinateBasis q d)
  rw [coordinateBasis_mul_coords] at h
  simpa only [smul_eq_mul] using h.symm

private theorem scalar_product_second (a b c d : Fin 20) :
    (∑ j : Fin 20, specializedConstants q b c j *
      actualfSimpleP q (coordinateBasis q a) (coordinateBasis q j)
        (coordinateBasis q d)) =
      actualfSimpleP q (coordinateBasis q a)
        (coordinateBasis q b * coordinateBasis q c) (coordinateBasis q d) := by
  have h := scalar_second_expansion q
    (coordinateBasis q a) (coordinateBasis q b * coordinateBasis q c) (coordinateBasis q d)
  rw [coordinateBasis_mul_coords] at h
  simpa only [smul_eq_mul] using h.symm

private theorem scalar_product_third (a b c d : Fin 20) :
    (∑ j : Fin 20, specializedConstants q c d j *
      actualfSimpleP q (coordinateBasis q a) (coordinateBasis q b)
        (coordinateBasis q j)) =
      actualfSimpleP q (coordinateBasis q a) (coordinateBasis q b)
        (coordinateBasis q c * coordinateBasis q d) := by
  have h := scalar_third_expansion q
    (coordinateBasis q a) (coordinateBasis q b) (coordinateBasis q c * coordinateBasis q d)
  rw [coordinateBasis_mul_coords] at h
  simpa only [smul_eq_mul] using h.symm

private theorem suffixLift_zero_sum {I : Type*} [Fintype I]
    (s : I → R) (w : I → Word 3) :
    suffixLift q 0 (∑ i, s i • wordBasis q 3 (w i)) =
      (∑ i, s i * suffixValue q 0 (w i)) • wordBasis q 0 emptyWord := by
  rw [map_sum]
  simp only [(suffixLift q 0).map_smul_of_tower, suffixLift_basis,
    prefixWord, smul_smul]
  rw [Finset.sum_smul]

private theorem boundary_one_word (a : Fin 20) :
    boundary q (fCharacter q) (wordBasis q 1 (oneWord a)) =
      coordinateBasis q a • wordBasis q 0 emptyWord +
        fCharacter q (coordinateBasis q a) • wordBasis q 0 emptyWord := by
  apply (zeroWordEquiv q).injective
  rw [boundary_basis, LinearEquiv.apply_symm_apply]
  change coordinateBasis q a - algebraMap R (TableAlgebra q)
      (fCharacter q (coordinateBasis q a)) =
    (coordinateBasis q a • wordBasis q 0 emptyWord +
      fCharacter q (coordinateBasis q a) • wordBasis q 0 emptyWord) emptyWord
  simp [wordBasis_apply, Algebra.smul_def, CharTwo.sub_eq_add]

/-- Insertion transfers all genuine A-valued coefficients. The suffix
lift commutes with it only as an R-linear operation. -/
theorem suffixLift_insertion_smul_basis (n : Nat) (a : TableAlgebra q)
    (w : Word (n + 3)) :
    suffixLift q (n + 1)
        (coefficientInsertion q (n + 3) (a • wordBasis q (n + 3) w)) =
      coefficientInsertion q n (suffixLift q n (a • wordBasis q (n + 3) w)) := by
  classical
  calc
    _ = ∑ i : Fin 20, a.coords i •
        (suffixValue q n w • wordBasis q (n + 1) (Fin.cons i (prefixWord n w))) := by
      rw [coefficientInsertion_smul_basis, map_sum]
      simp only [(suffixLift q (n + 1)).map_smul_of_tower, suffixLift_cons_basis]
    _ = suffixValue q n w • (∑ i : Fin 20,
        a.coords i • wordBasis q (n + 1) (Fin.cons i (prefixWord n w))) := by
      rw [Finset.smul_sum]
      apply Finset.sum_congr rfl
      intro i hi
      simp only [smul_smul, mul_comm]
    _ = coefficientInsertion q n
        (suffixValue q n w • (a • wordBasis q n (prefixWord n w))) := by
      rw [map_smul, coefficientInsertion_smul_basis]
    _ = _ := by
      rw [(suffixLift q n).map_smul, suffixLift_basis]
      exact congrArg (coefficientInsertion q n)
        (smul_algebra_smul_comm (suffixValue q n w) a
          (wordBasis q n (prefixWord n w))).symm

/-- All vectors and all degrees, with full actual left A-coefficients. -/
theorem suffixLift_insertion (n : Nat) (v : BarTerm q (n + 3)) :
    suffixLift q (n + 1) (coefficientInsertion q (n + 3) v) =
      coefficientInsertion q n (suffixLift q n v) := by
  classical
  have hv : v = ∑ w : Word (n + 3), v w • wordBasis q (n + 3) w := by
    simpa only [wordBasis_repr] using ((wordBasis q (n + 3)).sum_repr v).symm
  calc
    _ = ∑ w : Word (n + 3), suffixLift q (n + 1)
        (coefficientInsertion q (n + 3) (v w • wordBasis q (n + 3) w)) := by
      conv_lhs => rw [hv]
      rw [map_sum, map_sum]
    _ = ∑ w : Word (n + 3), coefficientInsertion q n
        (suffixLift q n (v w • wordBasis q (n + 3) w)) := by
      apply Finset.sum_congr rfl
      intro w hw
      exact suffixLift_insertion_smul_basis q n (v w) w
    _ = coefficientInsertion q n (suffixLift q n
        (∑ w : Word (n + 3), v w • wordBasis q (n + 3) w)) := by
      rw [map_sum, map_sum]
    _ = _ := by rw [← hv]

/-- The degree-one/four lift equation is the full scalar cocycle law,
retaining the first A-valued face in P0. -/
theorem suffixLift_chain_zero :
    (recursiveBoundary q (fCharacter q) 0).comp (suffixLift q 1) =
      (suffixLift q 0).comp (recursiveBoundary q (fCharacter q) 3) := by
  apply (wordBasis q 4).ext
  intro w
  have hleft (a b c d : Fin 20) :
      recursiveBoundary q (fCharacter q) 0
          (suffixLift q 1 (wordBasis q 4 (word4 a b c d))) =
        coordinateBasis q a •
            (actualfSimpleP q (coordinateBasis q b) (coordinateBasis q c)
              (coordinateBasis q d) • wordBasis q 0 emptyWord) +
          (fCharacter q (coordinateBasis q a) *
            actualfSimpleP q (coordinateBasis q b) (coordinateBasis q c)
              (coordinateBasis q d)) • wordBasis q 0 emptyWord := by
    rw [recursiveBoundary_zero, suffixLift_basis, prefixWord_one]
    change boundary q (fCharacter q)
        (actualfSimpleP q (coordinateBasis q b) (coordinateBasis q c)
          (coordinateBasis q d) • wordBasis q 1 (oneWord a)) = _
    rw [(boundary q (fCharacter q)).map_smul_of_tower, boundary_one_word, smul_add]
    congr 1
    · exact (smul_algebra_smul_comm _ _ _).symm
    · rw [smul_smul, mul_comm]
  have hright (a b c d : Fin 20) :
      suffixLift q 0
          (recursiveBoundary q (fCharacter q) 3 (wordBasis q 4 (word4 a b c d))) =
        coordinateBasis q a •
            (actualfSimpleP q (coordinateBasis q b) (coordinateBasis q c)
              (coordinateBasis q d) • wordBasis q 0 emptyWord) +
          (actualfSimpleP q (coordinateBasis q a * coordinateBasis q b)
              (coordinateBasis q c) (coordinateBasis q d) +
            actualfSimpleP q (coordinateBasis q a)
              (coordinateBasis q b * coordinateBasis q c) (coordinateBasis q d) +
            actualfSimpleP q (coordinateBasis q a) (coordinateBasis q b)
              (coordinateBasis q c * coordinateBasis q d) +
            actualfSimpleP q (coordinateBasis q a) (coordinateBasis q b)
              (coordinateBasis q c) * fCharacter q (coordinateBasis q d)) •
                wordBasis q 0 emptyWord := by
    rw [recursiveBoundary_three, boundary4_word4]
    simp only [map_add]
    rw [suffixLift_zero_sum, suffixLift_zero_sum, suffixLift_zero_sum]
    simp only [(suffixLift q 0).map_smul, (suffixLift q 0).map_smul_of_tower,
      suffixLift_basis, suffixValue_word3, prefixWord, smul_smul]
    rw [scalar_product_first, scalar_product_second, scalar_product_third]
    simp only [add_smul, add_assoc]
    rw [mul_comm (fCharacter q (coordinateBasis q d))]
  have hscalar (a b c d : Fin 20) :
      actualfSimpleP q (coordinateBasis q a * coordinateBasis q b)
          (coordinateBasis q c) (coordinateBasis q d) +
        actualfSimpleP q (coordinateBasis q a)
          (coordinateBasis q b * coordinateBasis q c) (coordinateBasis q d) +
        actualfSimpleP q (coordinateBasis q a) (coordinateBasis q b)
          (coordinateBasis q c * coordinateBasis q d) +
        actualfSimpleP q (coordinateBasis q a) (coordinateBasis q b)
          (coordinateBasis q c) * fCharacter q (coordinateBasis q d) =
      fCharacter q (coordinateBasis q a) *
        actualfSimpleP q (coordinateBasis q b) (coordinateBasis q c)
          (coordinateBasis q d) := by
    apply Eq.symm
    apply CharTwo.add_eq_zero.mp
    simpa only [add_assoc] using actualfSimpleP_character_closed q
      (coordinateBasis q a) (coordinateBasis q b)
      (coordinateBasis q c) (coordinateBasis q d)
  have h := hleft (w 0) (w 1) (w 2) (w 3)
  have h' := hright (w 0) (w 1) (w 2) (w 3)
  rw [word4_eta] at h h'
  change recursiveBoundary q (fCharacter q) 0
      (suffixLift q 1 (wordBasis q 4 w)) =
    suffixLift q 0 (recursiveBoundary q (fCharacter q) 3 (wordBasis q 4 w))
  rw [h, h', hscalar]

/-- The complete suffix lift chain law for every natural-number degree.
This is equality before applying the character to the left coefficients. -/
theorem suffixLift_chain (n : Nat) :
    (recursiveBoundary q (fCharacter q) n).comp (suffixLift q (n + 1)) =
      (suffixLift q n).comp (recursiveBoundary q (fCharacter q) (n + 3)) := by
  induction n with
  | zero => exact suffixLift_chain_zero q
  | succ n ih =>
    apply (wordBasis q (n + 5)).ext
    intro w
    have h (i : Fin 20) (v : Word (n + 4)) :
        recursiveBoundary q (fCharacter q) (n + 1)
            (suffixLift q (n + 2) (wordBasis q (n + 5) (Fin.cons i v))) =
          suffixLift q (n + 1)
            (recursiveBoundary q (fCharacter q) (n + 4)
              (wordBasis q (n + 5) (Fin.cons i v))) := by
      calc
        _ = coordinateBasis q i •
              suffixLift q (n + 1) (wordBasis q (n + 4) v) +
            coefficientInsertion q n
              (recursiveBoundary q (fCharacter q) n
                (coordinateBasis q i •
                  suffixLift q (n + 1) (wordBasis q (n + 4) v))) := by
          rw [suffixLift_cons_basis,
            (recursiveBoundary q (fCharacter q) (n + 1)).map_smul_of_tower,
            recursiveBoundary_succ_basis, suffixLift_basis, smul_add]
          congr 1
          · exact (smul_algebra_smul_comm _ _ _).symm
          · rw [← map_smul,
              ← (recursiveBoundary q (fCharacter q) n).map_smul_of_tower,
              ← smul_algebra_smul_comm]
        _ = coordinateBasis q i •
              suffixLift q (n + 1) (wordBasis q (n + 4) v) +
            coefficientInsertion q n
              (suffixLift q n
                (recursiveBoundary q (fCharacter q) (n + 3)
                  (coordinateBasis q i • wordBasis q (n + 4) v))) := by
          have heq := LinearMap.congr_fun ih
            (coordinateBasis q i • wordBasis q (n + 4) v)
          simp only [LinearMap.comp_apply] at heq
          rw [← (suffixLift q (n + 1)).map_smul, heq]
        _ = _ := by
          rw [recursiveBoundary_succ_basis, map_add,
            (suffixLift q (n + 1)).map_smul, suffixLift_insertion]
    simpa only [LinearMap.comp_apply, Fin.cons_self_tail] using h (w 0) (Fin.tail w)

private theorem fCochainHom_basis (w : Word 3) :
    (fCochainHom q (wordBasis q 3 w)).val =
      actualfSimpleP q (coordinateBasis q (w 0))
        (coordinateBasis q (w 1)) (coordinateBasis q (w 2)) := by
  have h := cochain3HomEquiv_symm_basis q (fCharacter q) (actualfSimpleP q)
    (w 0) (w 1) (w 2)
  change (fCochainHom q (wordBasis q 3 (word3 (w 0) (w 1) (w 2)))).val = _ at h
  rw [word3_eta] at h
  exact h

/-- The augmentation of the degree-zero suffix map is exactly the fixed
actual module cocycle, including its actual coefficient character action. -/
theorem augmentation_suffixLift_zero :
    (augmentation q (fCharacter q)).comp (suffixLift q 0) = fCochainHom q := by
  apply (wordBasis q 3).ext
  intro w
  apply CharacterModule.ext
  change (augmentation q (fCharacter q)
    (suffixLift q 0 (wordBasis q 3 w))).val = (fCochainHom q (wordBasis q 3 w)).val
  rw [suffixLift_basis, (augmentation q (fCharacter q)).map_smul_of_tower,
    val_coefficient_smul]
  have haug : (augmentation q (fCharacter q) (wordBasis q 0 emptyWord)).val = 1 := by
    simp [augmentation_val, zeroWordEquiv_apply, wordBasis_apply,
      ARCTwentyDimUnit.specialized_unit_coordinates]
  change suffixValue q 0 w *
    (augmentation q (fCharacter q) (wordBasis q 0 emptyWord)).val = _
  rw [haug, mul_one, fCochainHom_basis]
  rfl

/-- The degree-six actual A-linear Hom, defined by the degree-three
suffix component followed by the original cocycle. -/
def cupSixHom :
    BarTerm q 6 →ₗ[TableAlgebra q] CharacterModule (fCharacter q) :=
  (fCochainHom q).comp (suffixLift q 3)

/-- All actual six-letter basis values have the exact scalar cup formula. -/
theorem cupSixHom_basis (w : Word 6) :
    (cupSixHom q (wordBasis q 6 w)).val =
      actualfSimpleP q (coordinateBasis q (w 0)) (coordinateBasis q (w 1))
        (coordinateBasis q (w 2)) *
      actualfSimpleP q (coordinateBasis q (w 3)) (coordinateBasis q (w 4))
        (coordinateBasis q (w 5)) := by
  rw [cupSixHom, LinearMap.comp_apply, suffixLift_basis,
    (fCochainHom q).map_smul_of_tower, val_coefficient_smul,
    prefixWord_three, fCochainHom]
  rw [cochain3HomEquiv_symm_basis]
  change actualfSimpleP q (coordinateBasis q (w 3)) (coordinateBasis q (w 4))
      (coordinateBasis q (w 5)) *
    actualfSimpleP q (coordinateBasis q (w 0)) (coordinateBasis q (w 1))
      (coordinateBasis q (w 2)) = _
  exact mul_comm _ _

/-- Closure on the whole actual P7 term follows from the full suffix
chain law and the already proved whole-module degree-three cocycle law. -/
theorem cupSixHom_closed :
    (cupSixHom q).comp (recursiveBoundary q (fCharacter q) 6) = 0 := by
  apply LinearMap.ext
  intro v
  change fCochainHom q
    (suffixLift q 3 (recursiveBoundary q (fCharacter q) 6 v)) = 0
  have h := LinearMap.congr_fun (suffixLift_chain q 3) v
  simp only [LinearMap.comp_apply] at h
  rw [← h, recursiveBoundary_three]
  exact LinearMap.congr_fun (fCochainHom_closed q) (suffixLift q 4 v)

#print axioms suffixLift
#print axioms suffixLift_basis
#print axioms suffixLift_cons_basis
#print axioms suffixLift_insertion_smul_basis
#print axioms suffixLift_insertion
#print axioms suffixLift_chain_zero
#print axioms suffixLift_chain
#print axioms augmentation_suffixLift_zero
#print axioms cupSixHom
#print axioms cupSixHom_basis
#print axioms cupSixHom_closed

end
end ARCFiniteFreeBarCupLift
