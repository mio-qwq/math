import TwentyDimCoreAlgebra
import TwentyDimAlgebra
import Mathlib.Algebra.Algebra.Equiv

/-!
# The actual table as the core dual trivial extension

The comparison uses the actual table algebra and the genuine dual-action
extension of its actual ten-coordinate core. Coordinates are split into
the lower core and the coordinate dual. The linear comparison preserves
multiplication and the unit, giving an actual R-algebra isomorphism. Its
trace and bilinear trace pairing agree with the concrete table trace.
No new finite enumeration is used; no homological realization is asserted.
-/

namespace ARCTwentyDimDualIsomorphism

open ARCTwentyDimDualCorrespondence ARCTwentyDimCoreAlgebra
open ARCTwentyDimAlgebra ARCTwentyDimAssociativity
open scoped BigOperators

noncomputable section

variable {R : Type*} [CommRing R] [CharP R 2]

def indexSplit : Sum (Fin 10) (Fin 10) ≃ Fin 20 where
  toFun := fun i => match i with
    | Sum.inl a => lowerIndex a
    | Sum.inr a => upperIndex a
  invFun := fun i => if h : i.val < 10 then Sum.inl ⟨i.val, h⟩
    else Sum.inr ⟨i.val - 10, by omega⟩
  left_inv := by
    intro i
    cases i with
    | inl a => simp [lowerIndex, a.isLt]
    | inr a =>
      have h : ¬ a.val + 10 < 10 := by omega
      simp [upperIndex, h]
  right_inv := by
    intro i
    apply Fin.ext
    dsimp
    split_ifs
    · rfl
    · dsimp [lowerIndex, upperIndex]
      omega

omit [CharP R 2] in
theorem sum_split (f : Fin 20 → R) :
    (∑ i : Fin 20, f i) =
      (∑ i : Fin 10, f (lowerIndex i)) + ∑ i : Fin 10, f (upperIndex i) := by
  have h : (∑ i : Sum (Fin 10) (Fin 10), f (indexSplit i)) = ∑ i : Fin 20, f i := by
    apply Fintype.sum_equiv indexSplit
    intro i
    rfl
  rw [← h, Fintype.sum_sum_type]
  rfl

/-- Splitting the coordinate module introduces no multiplication by itself. -/
def splitCoordinates (q : R) :
    (Fin 20 → R) ≃ₗ[R] CoreAlgebra q × (Fin 10 → R) where
  toFun := fun x => (fun i => x (lowerIndex i), fun i => x (upperIndex i))
  invFun := fun y i => if h : i.val < 10 then y.1 ⟨i.val, h⟩
    else y.2 ⟨i.val - 10, by omega⟩
  left_inv := by
    intro x
    funext i
    dsimp
    split_ifs
    · rfl
    · congr 1
      apply Fin.ext
      dsimp [upperIndex]
      omega
  right_inv := by
    intro y
    apply Prod.ext
    · funext i
      simp [lowerIndex, i.isLt]
    · funext i
      have h : ¬ i.val + 10 < 10 := by omega
      simp [upperIndex, h]
  map_add' _ _ := rfl
  map_smul' _ _ := rfl

def dualCoordinates (q : R) :
    Module.Dual R (CoreAlgebra q) ≃ₗ[R] (Fin 10 → R) :=
  (coreBasis q).dualBasis.equivFun

theorem dualCoordinates_apply (q : R) (φ : Module.Dual R (CoreAlgebra q)) (i : Fin 10) :
    dualCoordinates q φ i = φ (coreBasis q i) :=
  (coreBasis q).dualBasis_equivFun φ i

theorem dualCoordinates_symm_apply (q : R) (f : Fin 10 → R) (i : Fin 10) :
    (dualCoordinates q).symm f (coreBasis q i) = f i := by
  have h := congrFun ((dualCoordinates q).apply_symm_apply f) i
  simpa only [dualCoordinates_apply] using h

def splitDualCoordinates (q : R) : (Fin 20 → R) ≃ₗ[R] CoreDualExtension q :=
  (splitCoordinates q).trans
    ((LinearEquiv.refl R (CoreAlgebra q)).prodCongr (dualCoordinates q).symm)

/-- The actual table algebra is linearly equivalent to the actual core-dual carrier. -/
def compareLinear (q : R) : TableAlgebra q ≃ₗ[R] CoreDualExtension q :=
  (coordsLinearEquiv q).trans (splitDualCoordinates q)

theorem compare_lower (q : R) (x : TableAlgebra q) (i : Fin 10) :
    (compareLinear q x).1 i = x.coords (lowerIndex i) := rfl

theorem compare_dual (q : R) (x : TableAlgebra q) (i : Fin 10) :
    (compareLinear q x).2 (coreBasis q i) = x.coords (upperIndex i) := by
  change (dualCoordinates q).symm (fun j => x.coords (upperIndex j)) (coreBasis q i) = _
  exact dualCoordinates_symm_apply q _ i

/-- Every core-linear functional evaluates by its actual coordinate-dual values. -/
theorem dual_evaluate (q : R) (φ : Module.Dual R (CoreAlgebra q)) (u : CoreAlgebra q) :
    φ u = ∑ i : Fin 10, u i * φ (coreBasis q i) := by
  have hrepr : (∑ i : Fin 10, u i • coreBasis q i) = u := by
    have hcoords (i : Fin 10) : (coreBasis q).equivFun u i = u i := by
      calc
        (coreBasis q).equivFun u i = (coreBasis q).repr u i :=
          congrFun ((coreBasis q).equivFun_apply u) i
        _ = u i := Pi.basisFun_repr R (Fin 10) u i
    simpa only [hcoords] using (coreBasis q).sum_equivFun u
  calc
    φ u = φ (∑ i : Fin 10, u i • coreBasis q i) := congrArg φ hrepr.symm
    _ = _ := by simp only [map_sum, map_smul, smul_eq_mul]

theorem table_product_lower (q : R) (u v : Fin 20 → R) (k : Fin 10) :
    specializedMul q u v (lowerIndex k) =
      ARCFiniteBilinear.mul (specializedCoreConstants q)
        (fun i => u (lowerIndex i)) (fun i => v (lowerIndex i)) k := by
  unfold specializedMul ARCFiniteBilinear.mul
  rw [sum_split]
  simp_rw [sum_split]
  simp only [specializedConstants, lower_lower_lower, lower_upper_lower,
    upper_lower_lower, upper_upper_lower, map_zero, mul_zero, Finset.sum_const_zero,
    add_zero, specializedCoreConstants]

theorem table_product_upper (q : R) (u v : Fin 20 → R) (k : Fin 10) :
    specializedMul q u v (upperIndex k) =
      (∑ a : Fin 10, ∑ b : Fin 10,
        u (lowerIndex a) * v (upperIndex b) * specializedCoreConstants q k a b) +
      ∑ a : Fin 10, ∑ b : Fin 10,
        u (upperIndex a) * v (lowerIndex b) * specializedCoreConstants q b k a := by
  unfold specializedMul ARCFiniteBilinear.mul
  rw [sum_split]
  simp_rw [sum_split]
  simp only [specializedConstants, lower_lower_upper, lower_upper_upper,
    upper_lower_upper, upper_upper_upper, map_zero, mul_zero, Finset.sum_const_zero,
    zero_add, add_zero, specializedCoreConstants]

theorem core_basis_mul_left (q : R) (i : Fin 10) (u : CoreAlgebra q) :
    coreBasis q i * u =
      ∑ j : Fin 10, u j • (specializedCoreConstants q i j : CoreAlgebra q) := by
  have hb : coreBasis q i = ARCFiniteStructure.basisVec i :=
    ARCFiniteStructure.carrierBasis_apply (coreLaws q) i
  exact (ARCFiniteStructure.carrier_mul (coreLaws q) (coreBasis q i) u).trans
    ((congrArg (fun b => ARCFiniteStructure.product (specializedCoreConstants q) b u) hb).trans
      (ARCFiniteStructure.product_basis_left (specializedCoreConstants q) i u))

theorem core_basis_mul_right (q : R) (u : CoreAlgebra q) (i : Fin 10) :
    u * coreBasis q i =
      ∑ j : Fin 10, u j • (specializedCoreConstants q j i : CoreAlgebra q) := by
  have hb : coreBasis q i = ARCFiniteStructure.basisVec i :=
    ARCFiniteStructure.carrierBasis_apply (coreLaws q) i
  exact (ARCFiniteStructure.carrier_mul (coreLaws q) u (coreBasis q i)).trans
    ((congrArg (fun b => ARCFiniteStructure.product (specializedCoreConstants q) u b) hb).trans
      (ARCFiniteStructure.product_basis_right (specializedCoreConstants q) u i))

set_option backward.isDefEq.respectTransparency false in
theorem dual_core_basis_mul_left (q : R) (φ : Module.Dual R (CoreAlgebra q))
    (i : Fin 10) (u : CoreAlgebra q) :
    φ (coreBasis q i * u) = ∑ a : Fin 10, ∑ b : Fin 10,
      u a * specializedCoreConstants q i a b * φ (coreBasis q b) := by
  calc
    φ (coreBasis q i * u) =
        φ (∑ a : Fin 10, u a • (specializedCoreConstants q i a : CoreAlgebra q)) :=
      congrArg φ (core_basis_mul_left q i u)
    _ = ∑ a : Fin 10, u a * φ (specializedCoreConstants q i a) := by
      simp +instances only [map_sum, map_smul, smul_eq_mul]
    _ = _ := by
      simp_rw [dual_evaluate q φ (specializedCoreConstants q i _), Finset.mul_sum, mul_assoc]

set_option backward.isDefEq.respectTransparency false in
theorem dual_core_basis_mul_right (q : R) (φ : Module.Dual R (CoreAlgebra q))
    (u : CoreAlgebra q) (i : Fin 10) :
    φ (u * coreBasis q i) = ∑ a : Fin 10, ∑ b : Fin 10,
      u a * specializedCoreConstants q a i b * φ (coreBasis q b) := by
  calc
    φ (u * coreBasis q i) =
        φ (∑ a : Fin 10, u a • (specializedCoreConstants q a i : CoreAlgebra q)) :=
      congrArg φ (core_basis_mul_right q u i)
    _ = ∑ a : Fin 10, u a * φ (specializedCoreConstants q a i) := by
      simp +instances only [map_sum, map_smul, smul_eq_mul]
    _ = _ := by
      simp_rw [dual_evaluate q φ (specializedCoreConstants q _ i), Finset.mul_sum, mul_assoc]

set_option backward.isDefEq.respectTransparency false in
/-- The coordinate comparison respects the genuine products on both algebras. -/
theorem compare_mul (q : R) (x y : TableAlgebra q) :
    compareLinear q (x * y) = compareLinear q x * compareLinear q y := by
  apply Prod.ext
  · funext k
    change (compareLinear q (x * y)).1 k =
      ((compareLinear q x).1 * (compareLinear q y).1) k
    rw [compare_lower, coords_mul, core_mul, table_product_lower]
    rfl
  · apply (coreBasis q).ext
    intro k
    change (compareLinear q (x * y)).2 (coreBasis q k) =
      (compareLinear q y).2 (coreBasis q k * (compareLinear q x).1) +
      (compareLinear q x).2 ((compareLinear q y).1 * coreBasis q k)
    rw [compare_dual, coords_mul, table_product_upper,
      dual_core_basis_mul_left, dual_core_basis_mul_right]
    simp_rw [compare_lower, compare_dual]
    congr 1
    · apply Finset.sum_congr rfl
      intro a _
      apply Finset.sum_congr rfl
      intro b _
      ac_rfl
    · rw [Finset.sum_comm]
      apply Finset.sum_congr rfl
      intro a _
      apply Finset.sum_congr rfl
      intro b _
      ac_rfl

set_option backward.isDefEq.respectTransparency false in
/-- The comparison sends the actual two-idempotent table unit to the extension unit. -/
theorem compare_one (q : R) :
    compareLinear q (1 : TableAlgebra q) = 1 := by
  apply Prod.ext
  · funext i
    change (compareLinear q (1 : TableAlgebra q)).1 i = coreUnit q i
    rw [compare_lower, coords_one, ARCTwentyDimUnit.specialized_unit_coordinates]
    have h0 : lowerIndex (0 : Fin 10) = (0 : Fin 20) := rfl
    have h8 : lowerIndex (8 : Fin 10) = (8 : Fin 20) := rfl
    simp [coreUnit, polynomialCoreUnit, ← h0, ← h8, lowerIndex_eq_iff]
  · apply (coreBasis q).ext
    intro i
    change (compareLinear q (1 : TableAlgebra q)).2 (coreBasis q i) = 0
    rw [compare_dual, coords_one, ARCTwentyDimUnit.specialized_unit_coordinates]
    have h0 : upperIndex i ≠ (0 : Fin 20) := by
      intro h
      have hv := congrArg Fin.val h
      dsimp [upperIndex] at hv
      omega
    have h8 : upperIndex i ≠ (8 : Fin 20) := by
      intro h
      have hv := congrArg Fin.val h
      dsimp [upperIndex] at hv
      omega
    simp [h0, h8]

/-- The actual twenty-dimensional table is the actual dual trivial extension of its core. -/
def compareAlgebra (q : R) : TableAlgebra q ≃ₐ[R] CoreDualExtension q :=
  AlgEquiv.ofLinearEquiv (compareLinear q) (compare_one q) (compare_mul q)

theorem core_unit_coordinates (q : R) (i : Fin 10) :
    (1 : CoreAlgebra q) i = (if i = 0 then 1 else 0) + (if i = 8 then 1 else 0) := by
  change coreUnit q i = _
  simp [coreUnit, polynomialCoreUnit]

set_option backward.isDefEq.respectTransparency false in
/-- Evaluation at the core unit becomes precisely the two-coordinate table trace. -/
theorem compare_trace (q : R) (x : TableAlgebra q) :
    ARCDualTrivialExtension.traceLinear (compareAlgebra q x) =
      ARCTracePairSemantics.specializedTrace x.coords := by
  change (compareLinear q x).2 1 = _
  rw [dual_evaluate]
  simp_rw [core_unit_coordinates, compare_dual, add_mul, ite_mul, one_mul, zero_mul]
  rw [Finset.sum_add_distrib]
  simp [ARCTracePairSemantics.specializedTrace, upperIndex]

/-- The actual symmetric bilinear trace forms are identified by the algebra isomorphism. -/
theorem compare_tracePairing (q : R) (x y : TableAlgebra q) :
    ARCDualTrivialExtension.tracePairing (compareAlgebra q x) (compareAlgebra q y) =
      ARCTracePairSemantics.specializedTrace (x * y).coords := by
  change ARCDualTrivialExtension.traceLinear (compareAlgebra q x * compareAlgebra q y) = _
  rw [← map_mul, compare_trace]

#print axioms sum_split
#print axioms compareLinear
#print axioms compare_lower
#print axioms compare_dual
#print axioms dual_evaluate
#print axioms table_product_lower
#print axioms table_product_upper
#print axioms core_basis_mul_left
#print axioms core_basis_mul_right
#print axioms dual_core_basis_mul_left
#print axioms dual_core_basis_mul_right
#print axioms compare_mul
#print axioms compare_one
#print axioms compareAlgebra
#print axioms core_unit_coordinates
#print axioms compare_trace
#print axioms compare_tracePairing

end
end ARCTwentyDimDualIsomorphism
