import FiniteFreeBarRecursive
import TwentyDimCharacteristic

/-!
The full coefficient-insertion identity for a successor boundary, for
every degree and every actual preceding A-linear map. All A-valued word
coefficients are expanded in the actual twenty-element R-basis. Insertion
is used only R-linearly. The resulting identities apply to the recursive
family and to its character augmentation in degree zero.

This file proves contraction identities, without asserting the recursive
chain laws, all-degree exactness, a projective-resolution object, a standard
bar identification or an Ext comparison. A remains noncommutative.
-/

namespace ARCFiniteFreeBarRecursiveContraction

open ARCTwentyDimAlgebra ARCFiniteFreeBarModules ARCFiniteFreeBarAugmentation
open ARCFiniteFreeBarInsertion ARCFiniteFreeBarRecursive ARCCharacterModule
open scoped BigOperators

variable {R : Type*} [CommRing R] [CharP R 2]

noncomputable section

variable (q : R)

/-- Reassemble every actual R-coordinate of a left A-weighted word.
This uses the R/A scalar tower, not commutativity of A. -/
theorem coefficient_expansion_smul_word (n : Nat) (a : TableAlgebra q) (w : Word n) :
    (∑ i : Fin 20, a.coords i • (coordinateBasis q i • wordBasis q n w)) =
      a • wordBasis q n w := by
  classical
  calc
    _ = (∑ i : Fin 20, a.coords i • coordinateBasis q i) • wordBasis q n w := by
      rw [Finset.sum_smul]
      simp only [smul_assoc]
    _ = _ := by rw [coordinate_expansion]

/-- The successor/insertion formula on any genuine A-weighted word. -/
theorem nextBoundary_insertion_smul_basis (n : Nat)
    (d : BarTerm q (n + 1) →ₗ[TableAlgebra q] BarTerm q n)
    (a : TableAlgebra q) (w : Word (n + 1)) :
    nextBoundary q n d (coefficientInsertion q (n + 1) (a • wordBasis q (n + 1) w)) =
      a • wordBasis q (n + 1) w +
        coefficientInsertion q n (d (a • wordBasis q (n + 1) w)) := by
  classical
  rw [coefficientInsertion_smul_basis, map_sum]
  simp only [(nextBoundary q n d).map_smul_of_tower, nextBoundary_cons_basis,
    smul_add, Finset.sum_add_distrib]
  rw [coefficient_expansion_smul_word]
  congr 1
  calc
    (∑ i : Fin 20, a.coords i • coefficientInsertion q n
        (d (coordinateBasis q i • wordBasis q (n + 1) w))) =
        coefficientInsertion q n
          (d (∑ i : Fin 20, a.coords i •
            (coordinateBasis q i • wordBasis q (n + 1) w))) := by
      rw [map_sum, map_sum]
      simp only [map_smul, d.map_smul_of_tower]
    _ = _ := by rw [coefficient_expansion_smul_word]

/-- The generic successor/insertion identity on every vector and every
degree. Its proof retains all actual A-valued coefficients. -/
theorem nextBoundary_insertion (n : Nat)
    (d : BarTerm q (n + 1) →ₗ[TableAlgebra q] BarTerm q n)
    (v : BarTerm q (n + 1)) :
    nextBoundary q n d (coefficientInsertion q (n + 1) v) =
      v + coefficientInsertion q n (d v) := by
  classical
  have hv : v = ∑ w : Word (n + 1), v w • wordBasis q (n + 1) w := by
    simpa only [wordBasis_repr] using ((wordBasis q (n + 1)).sum_repr v).symm
  calc
    nextBoundary q n d (coefficientInsertion q (n + 1) v) =
        ∑ w : Word (n + 1), nextBoundary q n d
          (coefficientInsertion q (n + 1) (v w • wordBasis q (n + 1) w)) := by
      conv_lhs => rw [hv]
      rw [map_sum, map_sum]
    _ = ∑ w : Word (n + 1), (v w • wordBasis q (n + 1) w +
        coefficientInsertion q n (d (v w • wordBasis q (n + 1) w))) := by
      simp only [nextBoundary_insertion_smul_basis]
    _ = v + coefficientInsertion q n (d v) := by
      have hsum : (∑ w : Word (n + 1), coefficientInsertion q n
          (d (v w • wordBasis q (n + 1) w))) = coefficientInsertion q n (d v) := by
        rw [← map_sum, ← map_sum, ← hv]
      rw [Finset.sum_add_distrib, ← hv, hsum]

variable (eps : TableAlgebra q →ₐ[R] R)

/-- The scalar section of augmentation, as an actual R-linear map. It is
not claimed to be A-linear. -/
def augmentationSection : CharacterModule eps →ₗ[R] BarTerm q 0 :=
  ((zeroWordEquiv q).symm.toLinearMap.restrictScalars R).comp
    ((Algebra.linearMap R (TableAlgebra q)).comp (valueLinearEquiv eps).toLinearMap)

@[simp] theorem augmentationSection_apply (x : CharacterModule eps) :
    augmentationSection q eps x =
      (zeroWordEquiv q).symm (algebraMap R (TableAlgebra q) x.val) := rfl

/-- The augmentation has this explicit R-linear right inverse. -/
theorem augmentation_section (x : CharacterModule eps) :
    augmentation q eps (augmentationSection q eps x) = x := by
  apply CharacterModule.ext
  simp

/-- Degree-zero insertion recovers v up to its scalar augmentation section. -/
theorem recursiveBoundary_zero_insertion (v : BarTerm q 0) :
    recursiveBoundary q eps 0 (coefficientInsertion q 0 v) =
      v + augmentationSection q eps (augmentation q eps v) := by
  apply (zeroWordEquiv q).injective
  rw [recursiveBoundary_zero, coefficientInsertion_zero, boundary_coordinateLift]
  simp only [LinearEquiv.apply_symm_apply, map_add, augmentationSection_apply,
    augmentation_val, CharTwo.sub_eq_add]

/-- The successor contraction formula for the whole recursive family. -/
theorem recursiveBoundary_succ_insertion (n : Nat) (v : BarTerm q (n + 1)) :
    recursiveBoundary q eps (n + 1) (coefficientInsertion q (n + 1) v) =
      v + coefficientInsertion q n (recursiveBoundary q eps n v) := by
  rw [recursiveBoundary_succ]
  exact nextBoundary_insertion q n (recursiveBoundary q eps n) v

private theorem two_zsmul_barTerm (n : Nat) (v : BarTerm q n) : (2 : ℤ) • v = 0 := by
  funext w
  change (2 : ℤ) • v w = 0
  exact CharTwo.two_zsmul (v w)

/-- The usual degree-zero contraction identity, in the full actual module. -/
theorem recursive_contraction_zero (v : BarTerm q 0) :
    recursiveBoundary q eps 0 (coefficientInsertion q 0 v) +
      augmentationSection q eps (augmentation q eps v) = v := by
  rw [recursiveBoundary_zero_insertion, add_assoc, ← two_zsmul,
    two_zsmul_barTerm, add_zero]

/-- The usual contraction identity in every positive degree. This by itself
does not assert that the recursively defined adjacent maps compose to zero. -/
theorem recursive_contraction_succ (n : Nat) (v : BarTerm q (n + 1)) :
    recursiveBoundary q eps (n + 1) (coefficientInsertion q (n + 1) v) +
      coefficientInsertion q n (recursiveBoundary q eps n v) = v := by
  rw [recursiveBoundary_succ_insertion, add_assoc, ← two_zsmul,
    two_zsmul_barTerm, add_zero]

#print axioms coefficient_expansion_smul_word
#print axioms nextBoundary_insertion_smul_basis
#print axioms nextBoundary_insertion
#print axioms augmentationSection
#print axioms augmentation_section
#print axioms recursiveBoundary_zero_insertion
#print axioms recursiveBoundary_succ_insertion
#print axioms recursive_contraction_zero
#print axioms recursive_contraction_succ

end
end ARCFiniteFreeBarRecursiveContraction
