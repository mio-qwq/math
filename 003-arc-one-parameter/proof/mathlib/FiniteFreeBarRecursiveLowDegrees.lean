import FiniteFreeBarRecursive
import FiniteFreeBarExactTwo
import FiniteFreeBarComposition34

/-!
The recursive full-coefficient family agrees in its first four degrees
with the installed actual boundaries. Its coefficient insertion in degrees
one and two is exactly the previously proved R-linear contraction.

The three new identifications are equalities of genuine A-linear maps on
the whole free terms, not identities after applying a character. Insertion
is used only R-linearly. This file asserts no all-degree bar formula or Ext
comparison, and does not change any installed boundary definition.
-/

namespace ARCFiniteFreeBarRecursiveLowDegrees

open ARCTwentyDimAlgebra ARCTwentyDimCochainAlgebra
open ARCFiniteFreeBarModules ARCFiniteFreeBarAugmentation
open ARCFiniteFreeBarDegreeTwo ARCFiniteFreeBarDegreeThree ARCFiniteFreeBarDegreeFour
open ARCFiniteFreeBarPairLift ARCFiniteFreeBarTripleLift ARCFiniteFreeBarExactOne
open ARCFiniteFreeBarExactTwo ARCFiniteFreeBarInsertion ARCFiniteFreeBarRecursive
open ARCFiniteFreeBarComposition34 ARCCochainWordEquiv
open scoped BigOperators

variable {R : Type*} [CommRing R] [CharP R 2]

noncomputable section

variable (q : R)

private theorem oneWord_cons (j : Fin 20) :
    Fin.cons j (Fin.elim0 : Fin 0 → Fin 20) = oneWord j :=
  (oneWordEquiv.left_inv (Fin.cons j Fin.elim0)).symm

/-- The general degree-one insertion is exactly the frozen first contraction. -/
theorem coefficientInsertion_one_eq_contractingOne :
    coefficientInsertion q 1 = contractingOne q := by
  apply LinearMap.ext
  intro v
  funext w
  have h : coefficientInsertion q 1 v (word2 (w 0) (w 1)) =
      contractingOne q v (word2 (w 0) (w 1)) := by
    rw [contractingOne_word2]
    change algebraMap R (TableAlgebra q)
      ((v (Fin.cons (w 1) Fin.elim0)).coords (w 0)) = _
    rw [oneWord_cons]
  simpa only [word2_eta] using h

private theorem tripleLift_first_basis_expansion (x : TableAlgebra q) (a b : Fin 20) :
    tripleLift q x (coordinateBasis q a) (coordinateBasis q b) =
      ∑ i : Fin 20, x.coords i • wordBasis q 3 (word3 i a b) := by
  conv_lhs => rw [basis_expansion q x]
  simp only [map_sum, map_smul, LinearMap.sum_apply, LinearMap.smul_apply,
    tripleLift_basis]

/-- The general degree-two insertion is exactly the frozen second contraction. -/
theorem coefficientInsertion_two_eq_contractingTwo :
    coefficientInsertion q 2 = contractingTwo q := by
  classical
  apply LinearMap.ext
  intro v
  conv_lhs => rw [barTerm_two_expansion q v]
  simp only [map_sum, coefficientInsertion_smul_basis]
  rw [contractingTwo_apply]
  apply Finset.sum_congr rfl
  intro a ha
  apply Finset.sum_congr rfl
  intro b hb
  rw [tripleLift_first_basis_expansion]
  rfl

private theorem tripleLift_last_two_expansion (x y z : TableAlgebra q) :
    tripleLift q x y z = ∑ a : Fin 20, ∑ b : Fin 20,
      (y.coords a * z.coords b) •
        tripleLift q x (coordinateBasis q a) (coordinateBasis q b) := by
  conv_lhs => rw [basis_expansion q y, basis_expansion q z]
  simp only [map_sum, map_smul, LinearMap.sum_apply, LinearMap.smul_apply,
    Finset.smul_sum, smul_smul]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro a ha
  apply Finset.sum_congr rfl
  intro b hb
  rw [mul_comm]

/-- An arbitrary full pair lift transfers its left A-coefficient to the
first actual input of the triple lift. Only R-linearity is used. -/
theorem coefficientInsertion_two_algebra_smul_pairLift (x y z : TableAlgebra q) :
    coefficientInsertion q 2 (x • pairLift q y z) = tripleLift q x y z := by
  rw [coefficientInsertion_two_eq_contractingTwo, pairLift_apply,
    tripleLift_last_two_expansion]
  simp only [Finset.smul_sum, smul_algebra_smul_comm, map_sum, map_smul]
  simp only [contractingTwo_algebra_smul_basis q]

variable (eps : TableAlgebra q →ₐ[R] R)

private theorem insertion_zero_boundary_basis (x : TableAlgebra q) (j : Fin 20) :
    coefficientInsertion q 0 (boundary q eps (x • wordBasis q 1 (oneWord j))) =
      singleLift q (x * coordinateBasis q j) +
        eps (coordinateBasis q j) • singleLift q x := by
  rw [coefficientInsertion_zero, ← singleLift_apply, (boundary q eps).map_smul,
    boundary_basis, map_smul, LinearEquiv.apply_symm_apply]
  simp only [oneWord, smul_eq_mul, CharTwo.sub_eq_add, mul_add]
  rw [← Algebra.commutes (eps (coordinateBasis q j)) x, ← Algebra.smul_def,
    map_add, map_smul]

/-- The recursive degree-one-indexed map is the whole installed P2 -> P1 map. -/
theorem recursiveBoundary_one : recursiveBoundary q eps 1 = boundary2 q eps := by
  apply (wordBasis q 2).ext
  intro w
  have h := recursiveBoundary_succ_basis q eps 0 (w 0) (oneWord (w 1))
  have hword : Fin.cons (w 0) (oneWord (w 1)) = word2 (w 0) (w 1) := by
    rw [← oneWord_cons]
    rfl
  rw [hword] at h
  change recursiveBoundary q eps 1 (wordBasis q 2 (word2 (w 0) (w 1))) =
    coordinateBasis q (w 0) • wordBasis q 1 (oneWord (w 1)) +
      coefficientInsertion q 0 (recursiveBoundary q eps 0
        (coordinateBasis q (w 0) • wordBasis q 1 (oneWord (w 1)))) at h
  rw [recursiveBoundary_zero, insertion_zero_boundary_basis] at h
  rw [word2_eta] at h
  change recursiveBoundary q eps 1 (wordBasis q 2 w) = boundary2 q eps (wordBasis q 2 w)
  rw [h, boundary2_basis]
  simp only [degreeTwoFaces, _root_.algebraMap_smul, ← singleLift_apply,
    singleLift_basis]
  rw [add_assoc]

private theorem boundary2_algebra_smul_basis (x : TableAlgebra q) (a b : Fin 20) :
    boundary2 q eps (x • wordBasis q 2 (word2 a b)) =
      (x * coordinateBasis q a) • wordBasis q 1 (oneWord b) +
        x • singleLift q (coordinateBasis q a * coordinateBasis q b) +
        eps (coordinateBasis q b) • (x • wordBasis q 1 (oneWord a)) := by
  rw [(boundary2 q eps).map_smul, boundary2_basis]
  change x • degreeTwoFaces q eps a b = _
  simp only [degreeTwoFaces, _root_.algebraMap_smul, smul_add, ← singleLift_apply]
  rw [smul_smul, smul_algebra_smul_comm (eps (coordinateBasis q b)) x
    (wordBasis q 1 (oneWord a))]

/-- The recursive degree-two-indexed map is the whole installed P3 -> P2 map. -/
theorem recursiveBoundary_two : recursiveBoundary q eps 2 = boundary3 q eps := by
  apply (wordBasis q 3).ext
  intro w
  have h := recursiveBoundary_succ_basis q eps 1 (w 0) (word2 (w 1) (w 2))
  change recursiveBoundary q eps 2 (wordBasis q 3 (word3 (w 0) (w 1) (w 2))) =
    coordinateBasis q (w 0) • wordBasis q 2 (word2 (w 1) (w 2)) +
      coefficientInsertion q 1 (recursiveBoundary q eps 1
        (coordinateBasis q (w 0) • wordBasis q 2 (word2 (w 1) (w 2)))) at h
  rw [recursiveBoundary_one, boundary2_algebra_smul_basis,
    coefficientInsertion_one_eq_contractingOne] at h
  simp only [map_add, map_smul] at h
  rw [contractingOne_algebra_smul_basis q, contractingOne_algebra_smul_singleLift q,
    contractingOne_algebra_smul_basis q] at h
  have hs := boundary3_pairLift_basis q eps (w 0) (w 1) (w 2)
  rw [word3_eta] at h hs
  simp only [pairLift_basis] at hs
  change recursiveBoundary q eps 2 (wordBasis q 3 w) = boundary3 q eps (wordBasis q 3 w)
  rw [h, hs]
  simp only [pairLift_basis, add_assoc]

/-- The recursive degree-three-indexed map is the whole installed P4 -> P3 map. -/
theorem recursiveBoundary_three : recursiveBoundary q eps 3 = boundary4 q eps := by
  apply (wordBasis q 4).ext
  intro w
  have h := recursiveBoundary_succ_basis q eps 2 (w 0) (word3 (w 1) (w 2) (w 3))
  change recursiveBoundary q eps 3
      (wordBasis q 4 (word4 (w 0) (w 1) (w 2) (w 3))) =
    coordinateBasis q (w 0) • wordBasis q 3 (word3 (w 1) (w 2) (w 3)) +
      coefficientInsertion q 2 (recursiveBoundary q eps 2
        (coordinateBasis q (w 0) • wordBasis q 3 (word3 (w 1) (w 2) (w 3)))) at h
  rw [recursiveBoundary_two, (boundary3 q eps).map_smul,
    boundary3_pairLift_basis] at h
  simp only [smul_add, smul_smul] at h
  rw [smul_algebra_smul_comm (eps (coordinateBasis q (w 3)))
    (coordinateBasis q (w 0)) (pairLift q (coordinateBasis q (w 1))
      (coordinateBasis q (w 2)))] at h
  simp only [map_add, map_smul, coefficientInsertion_two_algebra_smul_pairLift] at h
  have hs := boundary4_tripleLift_basis q eps (w 0) (w 1) (w 2) (w 3)
  rw [word4_eta] at h hs
  simp only [fiveTripleFaces, tripleLift_basis] at hs
  change recursiveBoundary q eps 3 (wordBasis q 4 w) = boundary4 q eps (wordBasis q 4 w)
  rw [h, hs]
  simp only [tripleLift_basis, add_assoc]

#print axioms coefficientInsertion_one_eq_contractingOne
#print axioms coefficientInsertion_two_eq_contractingTwo
#print axioms coefficientInsertion_two_algebra_smul_pairLift
#print axioms insertion_zero_boundary_basis
#print axioms recursiveBoundary_one
#print axioms recursiveBoundary_two
#print axioms recursiveBoundary_three

end
end ARCFiniteFreeBarRecursiveLowDegrees
