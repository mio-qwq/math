import FiniteFreeBarDegreeTwo
import FiniteFreeBarDegreeThree

/-!
Actual R-linear single-word and R-bilinear two-word lifts of arbitrary
elements of the installed noncommutative algebra. The second boundary on
these full lifts has its three genuine faces. This proves that the actual
second and third A-linear boundaries compose to zero on the whole free
module, by algebra and module identities rather than character separation.
No higher exactness, full projective resolution or Ext comparison is stated.
-/

namespace ARCFiniteFreeBarPairLift

open ARCTwentyDimAlgebra ARCTwentyDimCochainAlgebra ARCTwentyDimAssociativity
open ARCFiniteFreeBarModules ARCFiniteFreeBarAugmentation ARCFiniteFreeBarDegreeTwo
open ARCFiniteFreeBarDegreeThree ARCCochainWordEquiv
open scoped BigOperators

variable {R : Type*} [CommRing R] [CharP R 2]

noncomputable section

variable (q : R)

/-- The full single-word lift as an actual R-linear map. -/
def singleLift : TableAlgebra q →ₗ[R] BarTerm q 1 :=
  (coordinateBasis q).constr R (fun a => wordBasis q 1 (oneWord a))

@[simp] theorem singleLift_basis (a : Fin 20) :
    singleLift q (coordinateBasis q a) = wordBasis q 1 (oneWord a) := by
  simp [singleLift]

/-- This linear map is exactly the previously used full coordinate lift. -/
theorem singleLift_apply (x : TableAlgebra q) :
    singleLift q x = coordinateLift q x := by
  rw [singleLift, Module.Basis.constr_apply_fintype, coordinateLift_sum]
  simp only [Module.Basis.equivFun_apply, coordinateBasis_repr]

/-- The actual two-input tensor-coordinate lift, R-linear in both inputs. -/
def pairLift : TableAlgebra q →ₗ[R] TableAlgebra q →ₗ[R] BarTerm q 2 :=
  (coordinateBasis q).constr R (fun a =>
    (coordinateBasis q).constr R (fun b => wordBasis q 2 (word2 a b)))

@[simp] theorem pairLift_basis (a b : Fin 20) :
    pairLift q (coordinateBasis q a) (coordinateBasis q b) =
      wordBasis q 2 (word2 a b) := by
  simp [pairLift]

/-- Every pair lift has the full finite two-coordinate formula. -/
theorem pairLift_apply (x y : TableAlgebra q) :
    pairLift q x y = ∑ a : Fin 20, ∑ b : Fin 20,
      (x.coords a * y.coords b) • wordBasis q 2 (word2 a b) := by
  conv_lhs => rw [basis_expansion q x, basis_expansion q y]
  simp only [map_sum, map_smul, LinearMap.sum_apply, LinearMap.smul_apply,
    pairLift_basis, Finset.smul_sum, smul_smul]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro a ha
  apply Finset.sum_congr rfl
  intro b hb
  rw [mul_comm]

/-- Expansion in the first actual algebra input. -/
theorem pairLift_first_expansion (x y : TableAlgebra q) :
    pairLift q x y = ∑ a : Fin 20, x.coords a • pairLift q (coordinateBasis q a) y := by
  conv_lhs => rw [basis_expansion q x]
  simp only [map_sum, map_smul, LinearMap.sum_apply, LinearMap.smul_apply]

/-- Expansion in the second actual algebra input. -/
theorem pairLift_second_expansion (x y : TableAlgebra q) :
    pairLift q x y = ∑ b : Fin 20, y.coords b • pairLift q x (coordinateBasis q b) := by
  conv_lhs => rw [basis_expansion q y]
  simp only [map_sum, map_smul]

variable (eps : TableAlgebra q →ₐ[R] R)

/-- The three-face expression, packaged as a genuine R-bilinear map. -/
def pairFaces : TableAlgebra q →ₗ[R] TableAlgebra q →ₗ[R] BarTerm q 1 where
  toFun x :=
    { toFun y := x • singleLift q y + singleLift q (x * y) + eps y • singleLift q x
      map_add' y y' := by
        simp only [map_add, mul_add, smul_add, add_smul]
        abel
      map_smul' r y := by
        simp only [RingHom.id_apply, map_smul, Algebra.mul_smul_comm,
          smul_add, smul_smul, smul_eq_mul]
        rw [smul_algebra_smul_comm r x (singleLift q y)] }
  map_add' x x' := by
    apply LinearMap.ext
    intro y
    change (x + x') • singleLift q y + singleLift q ((x + x') * y) +
      eps y • singleLift q (x + x') =
        (x • singleLift q y + singleLift q (x * y) + eps y • singleLift q x) +
          (x' • singleLift q y + singleLift q (x' * y) + eps y • singleLift q x')
    simp only [map_add, add_mul, smul_add, add_smul]
    abel
  map_smul' r x := by
    apply LinearMap.ext
    intro y
    change (r • x) • singleLift q y + singleLift q ((r • x) * y) +
      eps y • singleLift q (r • x) =
        r • (x • singleLift q y + singleLift q (x * y) + eps y • singleLift q x)
    have hs (a : TableAlgebra q) (v : BarTerm q 1) : (r • a) • v = r • (a • v) :=
      smul_assoc r a v
    simp only [map_smul, Algebra.smul_mul_assoc, smul_add, hs, smul_smul]
    rw [mul_comm (eps y) r]

/-- The actual second boundary postcomposed with the bilinear lift. -/
def boundary2PairLift : TableAlgebra q →ₗ[R] TableAlgebra q →ₗ[R] BarTerm q 1 where
  toFun x := ((boundary2 q eps).restrictScalars R).comp (pairLift q x)
  map_add' x x' := by
    apply LinearMap.ext
    intro y
    simp only [LinearMap.comp_apply, map_add, LinearMap.add_apply]
  map_smul' r x := by
    apply LinearMap.ext
    intro y
    simp only [RingHom.id_apply, LinearMap.comp_apply, map_smul, LinearMap.smul_apply]

/-- Equality of full bilinear maps, proved from the complete actual basis. -/
theorem boundary2PairLift_eq_pairFaces : boundary2PairLift q eps = pairFaces q eps := by
  apply (coordinateBasis q).ext
  intro a
  apply (coordinateBasis q).ext
  intro b
  change boundary2 q eps (pairLift q (coordinateBasis q a) (coordinateBasis q b)) = _
  rw [pairLift_basis, boundary2_basis]
  change degreeTwoFaces q eps a b =
    coordinateBasis q a • singleLift q (coordinateBasis q b) +
      singleLift q (coordinateBasis q a * coordinateBasis q b) +
        eps (coordinateBasis q b) • singleLift q (coordinateBasis q a)
  rw [singleLift_basis, singleLift_basis, singleLift_apply]
  simp only [degreeTwoFaces, _root_.algebraMap_smul]

/-- The exact three faces on arbitrary elements, in the genuine free module. -/
theorem boundary2_pairLift (x y : TableAlgebra q) :
    boundary2 q eps (pairLift q x y) =
      x • coordinateLift q y + coordinateLift q (x * y) + eps y • coordinateLift q x := by
  have h := congrArg (fun F : TableAlgebra q →ₗ[R] TableAlgebra q →ₗ[R] BarTerm q 1 => F x y)
    (boundary2PairLift_eq_pairFaces q eps)
  change boundary2 q eps (pairLift q x y) =
    x • singleLift q y + singleLift q (x * y) + eps y • singleLift q x at h
  simpa only [singleLift_apply] using h

theorem pairLift_product_first_basis (a b c : Fin 20) :
    pairLift q (coordinateBasis q a * coordinateBasis q b) (coordinateBasis q c) =
      ∑ j : Fin 20, specializedConstants q a b j • wordBasis q 2 (word2 j c) := by
  rw [pairLift_first_expansion, coordinateBasis_mul_coords]
  simp only [pairLift_basis]

theorem pairLift_product_second_basis (a b c : Fin 20) :
    pairLift q (coordinateBasis q a) (coordinateBasis q b * coordinateBasis q c) =
      ∑ j : Fin 20, specializedConstants q b c j • wordBasis q 2 (word2 a j) := by
  rw [pairLift_second_expansion, coordinateBasis_mul_coords]
  simp only [pairLift_basis]

/-- Rewriting the third boundary's actual basis formula in full pair-lift semantics. -/
theorem boundary3_pairLift_basis (a b c : Fin 20) :
    boundary3 q eps (wordBasis q 3 (word3 a b c)) =
      coordinateBasis q a • pairLift q (coordinateBasis q b) (coordinateBasis q c) +
        pairLift q (coordinateBasis q a * coordinateBasis q b) (coordinateBasis q c) +
        pairLift q (coordinateBasis q a) (coordinateBasis q b * coordinateBasis q c) +
        eps (coordinateBasis q c) • pairLift q (coordinateBasis q a) (coordinateBasis q b) := by
  rw [boundary3_word3, pairLift_product_first_basis,
    pairLift_product_second_basis, pairLift_basis, pairLift_basis]

/-- Characteristic-two cancellation holds on the entire actual free term.
Only its additive structure is used; no commutative multiplication on A is installed. -/
theorem barTerm_two_zsmul (n : Nat) (v : BarTerm q n) : (2 : ℤ) • v = 0 := by
  funext w
  change (2 : ℤ) • v w = 0
  exact CharTwo.two_zsmul (v w)

/-- The actual second and third A-linear boundaries compose to zero.
All coefficients are retained in A; no character-value separation is used. -/
theorem boundary2_comp_boundary3 :
    (boundary2 q eps).comp (boundary3 q eps) = 0 := by
  apply (wordBasis q 3).ext
  intro w
  have h := boundary3_pairLift_basis q eps (w 0) (w 1) (w 2)
  rw [word3_eta] at h
  change boundary2 q eps (boundary3 q eps (wordBasis q 3 w)) = 0
  rw [h]
  simp only [map_add, (boundary2 q eps).map_smul,
    (boundary2 q eps).map_smul_of_tower, boundary2_pairLift,
    smul_add, smul_smul, map_mul, mul_assoc]
  rw [smul_algebra_smul_comm (eps (coordinateBasis q (w 2)))
    (coordinateBasis q (w 0)) (coordinateLift q (coordinateBasis q (w 1))),
    mul_comm (eps (coordinateBasis q (w 2))) (eps (coordinateBasis q (w 1)))]
  abel_nf
  simp only [barTerm_two_zsmul, zero_add]

#print axioms singleLift
#print axioms singleLift_apply
#print axioms pairLift
#print axioms pairLift_basis
#print axioms pairLift_apply
#print axioms boundary2PairLift_eq_pairFaces
#print axioms boundary2_pairLift
#print axioms boundary3_pairLift_basis
#print axioms barTerm_two_zsmul
#print axioms boundary2_comp_boundary3

end
end ARCFiniteFreeBarPairLift
