import FiniteFreeBarExactOne
import FiniteFreeBarTripleLift

/-!
An explicit R-linear contraction proves exactness at P2 for the installed
actual finite free boundaries P3 -> P2 -> P1. All word coefficients remain
elements of the noncommutative table algebra A. The preceding contraction
is used only with its proved R-linearity, never with assumed A-linearity.

The contraction identity is an equality in the full A-valued module for
every vector and every actual character. No higher exactness, all-degree
projective resolution or comparison with Ext is asserted.
-/

namespace ARCFiniteFreeBarExactTwo

open ARCTwentyDimAlgebra ARCTwentyDimCochainAlgebra
open ARCFiniteFreeBarModules ARCFiniteFreeBarAugmentation
open ARCFiniteFreeBarDegreeTwo ARCFiniteFreeBarDegreeThree
open ARCFiniteFreeBarPairLift ARCFiniteFreeBarTripleLift ARCFiniteFreeBarExactOne
open ARCCochainWordEquiv
open scoped BigOperators

variable {R : Type*} [CommRing R] [CharP R 2]

noncomputable section

variable (q : R)

private def word2PairEquiv : Word 2 ≃ Fin 20 × Fin 20 where
  toFun w := (w 0, w 1)
  invFun p := word2 p.1 p.2
  left_inv w := word2_eta w
  right_inv _ := rfl

/-- Reindex the complete actual A-basis expansion by ordered label pairs. -/
theorem barTerm_two_expansion (v : BarTerm q 2) :
    v = ∑ a : Fin 20, ∑ b : Fin 20,
      v (word2 a b) • wordBasis q 2 (word2 a b) := by
  classical
  calc
    v = ∑ w : Word 2, v w • wordBasis q 2 w := by
      simpa only [wordBasis_repr] using ((wordBasis q 2).sum_repr v).symm
    _ = ∑ p : Fin 20 × Fin 20,
        v (word2 p.1 p.2) • wordBasis q 2 (word2 p.1 p.2) :=
      (word2PairEquiv.symm.sum_comp (fun w => v w • wordBasis q 2 w)).symm
    _ = _ := Fintype.sum_prod_type _

/-- The preceding R-linear contraction on a full single lift. The central
R-action is essential: the contraction itself need not be A-linear. -/
theorem contractingOne_algebra_smul_singleLift (x y : TableAlgebra q) :
    contractingOne q (x • singleLift q y) = pairLift q x y := by
  classical
  rw [contractingOne_apply]
  conv_rhs => rw [pairLift_second_expansion]
  simp only [barTerm_smul_apply, singleLift_apply, coordinateLift, oneWord]
  apply Finset.sum_congr rfl
  intro j hj
  rw [← Algebra.commutes (y.coords j) x, ← Algebra.smul_def]
  simp only [map_smul, LinearMap.smul_apply]

/-- An arbitrary A coefficient on a one-letter basis vector is retained. -/
theorem contractingOne_algebra_smul_basis (x : TableAlgebra q) (j : Fin 20) :
    contractingOne q (x • wordBasis q 1 (oneWord j)) =
      pairLift q x (coordinateBasis q j) := by
  simpa only [singleLift_basis] using
    contractingOne_algebra_smul_singleLift q x (coordinateBasis q j)

/-- Transfer every A-valued two-word coefficient to the full three-word lift. -/
def contractingTwo : BarTerm q 2 →ₗ[R] BarTerm q 3 where
  toFun v := ∑ a : Fin 20, ∑ b : Fin 20,
    tripleLift q (v (word2 a b)) (coordinateBasis q a) (coordinateBasis q b)
  map_add' v v' := by
    simp only [Pi.add_apply, map_add, LinearMap.add_apply, Finset.sum_add_distrib]
  map_smul' r v := by
    simp only [RingHom.id_apply, Pi.smul_apply, map_smul, LinearMap.smul_apply,
      Finset.smul_sum]

set_option maxRecDepth 4096 in
theorem contractingTwo_apply (v : BarTerm q 2) :
    contractingTwo q v = ∑ a : Fin 20, ∑ b : Fin 20,
      tripleLift q (v (word2 a b)) (coordinateBasis q a) (coordinateBasis q b) := rfl

private theorem word2_eq_iff (a b c d : Fin 20) :
    word2 a b = word2 c d ↔ a = c ∧ b = d := by
  constructor
  · intro h
    exact ⟨congrArg (fun w : Word 2 => w 0) h,
      congrArg (fun w : Word 2 => w 1) h⟩
  · rintro ⟨rfl, rfl⟩
    rfl

/-- The full contraction on a word basis vector with any genuine A coefficient. -/
theorem contractingTwo_algebra_smul_basis (x : TableAlgebra q) (a b : Fin 20) :
    contractingTwo q (x • wordBasis q 2 (word2 a b)) =
      tripleLift q x (coordinateBasis q a) (coordinateBasis q b) := by
  classical
  rw [contractingTwo_apply]
  calc
    (∑ i : Fin 20, ∑ j : Fin 20,
        tripleLift q ((x • wordBasis q 2 (word2 a b)) (word2 i j))
          (coordinateBasis q i) (coordinateBasis q j)) =
        ∑ j : Fin 20,
          tripleLift q ((x • wordBasis q 2 (word2 a b)) (word2 a j))
            (coordinateBasis q a) (coordinateBasis q j) := by
      apply Finset.sum_eq_single a
      · intro i hi hia
        apply Finset.sum_eq_zero
        intro j hj
        have hword : word2 i j ≠ word2 a b := by
          intro h
          exact hia ((word2_eq_iff i j a b).mp h).1
        simp only [barTerm_smul_apply, wordBasis_apply, ite_eq_right hword,
          mul_zero, map_zero, LinearMap.zero_apply]
      · simp
    _ = _ := by
      rw [Finset.sum_eq_single b]
      · simp only [barTerm_smul_apply, wordBasis_apply, ite_true, mul_one]
      · intro j hj hjb
        have hword : word2 a j ≠ word2 a b := by
          intro h
          exact hjb ((word2_eq_iff a j a b).mp h).2
        simp only [barTerm_smul_apply, wordBasis_apply, ite_eq_right hword,
          mul_zero, map_zero, LinearMap.zero_apply]
      · simp

variable (eps : TableAlgebra q →ₐ[R] R)

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

/-- The six extra terms cancel on every full A-weighted word vector. -/
theorem contracting_identity_algebra_smul_basis (x : TableAlgebra q) (a b : Fin 20) :
    boundary3 q eps (contractingTwo q (x • wordBasis q 2 (word2 a b))) +
      contractingOne q (boundary2 q eps (x • wordBasis q 2 (word2 a b))) =
        x • wordBasis q 2 (word2 a b) := by
  rw [contractingTwo_algebra_smul_basis, boundary3_tripleLift,
    boundary2_algebra_smul_basis]
  simp only [map_add, map_smul, contractingOne_algebra_smul_basis,
    contractingOne_algebra_smul_singleLift, pairLift_basis]
  abel_nf
  simp only [barTerm_two_zsmul, add_zero]

/-- The actual degree-two contraction identity on every full vector.
Only R-linearity and additivity of the contractions are used. -/
theorem contracting_identity (v : BarTerm q 2) :
    boundary3 q eps (contractingTwo q v) +
      contractingOne q (boundary2 q eps v) = v := by
  classical
  have hleft : boundary3 q eps (contractingTwo q v) =
      ∑ a : Fin 20, ∑ b : Fin 20,
        boundary3 q eps (contractingTwo q (v (word2 a b) •
          wordBasis q 2 (word2 a b))) := by
    conv_lhs => rw [barTerm_two_expansion q v]
    simp only [map_sum]
  have hright : contractingOne q (boundary2 q eps v) =
      ∑ a : Fin 20, ∑ b : Fin 20,
        contractingOne q (boundary2 q eps (v (word2 a b) •
          wordBasis q 2 (word2 a b))) := by
    conv_lhs => rw [barTerm_two_expansion q v]
    simp only [map_sum]
  rw [hleft, hright]
  simp only [← Finset.sum_add_distrib, contracting_identity_algebra_smul_basis]
  exact (barTerm_two_expansion q v).symm

/-- Every closed degree-two vector has this explicit degree-three preimage. -/
theorem boundary2_zero_contractingTwo (v : BarTerm q 2)
    (hv : boundary2 q eps v = 0) :
    boundary3 q eps (contractingTwo q v) = v := by
  have h := contracting_identity q eps v
  simpa only [hv, map_zero, add_zero] using h

/-- Exactness at P2, for arbitrary actual characters and all A-valued vectors. -/
theorem boundary2_zero_iff_exists_boundary3 (v : BarTerm q 2) :
    boundary2 q eps v = 0 ↔ ∃ u : BarTerm q 3, boundary3 q eps u = v := by
  constructor
  · intro hv
    exact ⟨contractingTwo q v, boundary2_zero_contractingTwo q eps v hv⟩
  · rintro ⟨u, rfl⟩
    exact congrArg (fun F : BarTerm q 3 →ₗ[TableAlgebra q] BarTerm q 1 => F u)
      (boundary2_comp_boundary3 q eps)

/-- The installed A-linear second boundary has precisely the third boundary's image. -/
theorem boundary2_ker_eq_boundary3_range :
    LinearMap.ker (boundary2 q eps) = LinearMap.range (boundary3 q eps) := by
  ext v
  exact boundary2_zero_iff_exists_boundary3 q eps v

#print axioms barTerm_two_expansion
#print axioms contractingOne_algebra_smul_singleLift
#print axioms contractingOne_algebra_smul_basis
#print axioms contractingTwo
#print axioms contractingTwo_algebra_smul_basis
#print axioms contracting_identity_algebra_smul_basis
#print axioms contracting_identity
#print axioms boundary2_zero_iff_exists_boundary3
#print axioms boundary2_ker_eq_boundary3_range

end
end ARCFiniteFreeBarExactTwo
