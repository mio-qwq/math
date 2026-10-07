import TwentyDimAlgebra
import TwentyDimCochain
import TracePairSemantics
import Mathlib.Algebra.Ring.Prod

/-!
The e and f coordinates are actual ring homomorphisms on the installed
table algebra. Their combined augmentation has exactly the eighteen-label
span as its kernel, and that kernel is closed under multiplication by any
table element on either side. No nilpotence or Jacobson radical claim is
made; the coordinate ring can be any commutative characteristic-two ring.
-/

namespace ARCTwentyDimAugmentation

open ARCFiniteCore ARCBitPolynomial ARCTermSemantics ARCFiniteTableContraction
open ARCTracePairSemantics ARCTwentyDimAssociativity ARCTwentyDimUnit
open ARCTwentyDimAlgebra ARCCochainBasisSemantics ARCTwentyDimCochain
open scoped BigOperators

noncomputable section

set_option maxHeartbeats 1000000

/-- Small independent output-coefficient check on the 400 table pairs. -/
private theorem e_coefficient_table : ∀ a b : Fin 20,
    coefficient (tTerms a.val b.val) 0 = if a = 0 ∧ b = 0 then 1 else 0 := by decide

private theorem f_coefficient_table : ∀ a b : Fin 20,
    coefficient (tTerms a.val b.val) 8 = if a = 8 ∧ b = 8 then 1 else 0 := by decide

theorem polynomial_e_constants (a b : Fin 20) :
    tConstants a b 0 = if a = 0 ∧ b = 0 then 1 else 0 := by
  change sumTerms (tTerms a.val b.val) 0 = _
  rw [← decode_coefficient]
  rw [e_coefficient_table]
  split_ifs <;> simp [ARCScalarEvaluation.decode_one]

theorem polynomial_f_constants (a b : Fin 20) :
    tConstants a b 8 = if a = 8 ∧ b = 8 then 1 else 0 := by
  change sumTerms (tTerms a.val b.val) 8 = _
  rw [← decode_coefficient]
  rw [f_coefficient_table]
  split_ifs <;> simp [ARCScalarEvaluation.decode_one]

variable {R : Type*} [CommRing R] [CharP R 2]

theorem specialized_e_constants (q : R) (a b : Fin 20) :
    specializedConstants q a b 0 = if a = 0 ∧ b = 0 then 1 else 0 := by
  unfold specializedConstants
  rw [polynomial_e_constants]
  split_ifs <;> simp

theorem specialized_f_constants (q : R) (a b : Fin 20) :
    specializedConstants q a b 8 = if a = 8 ∧ b = 8 then 1 else 0 := by
  unfold specializedConstants
  rw [polynomial_f_constants]
  split_ifs <;> simp

theorem specialized_mul_e_coordinate (q : R) (u v : Fin 20 → R) :
    specializedMul q u v 0 = u 0 * v 0 := by
  classical
  simp [specializedMul, ARCFiniteBilinear.mul, specialized_e_constants,
    ite_and, mul_ite]

theorem specialized_mul_f_coordinate (q : R) (u v : Fin 20 → R) :
    specializedMul q u v 8 = u 8 * v 8 := by
  classical
  simp [specializedMul, ARCFiniteBilinear.mul, specialized_f_constants,
    ite_and, mul_ite]

/-- The coordinate of e is an actual unital ring homomorphism. -/
def eAugmentation (q : R) : TableAlgebra q →+* R where
  toFun x := x.coords 0
  map_zero' := rfl
  map_one' := by simp [coords_one, specialized_unit_coordinates]
  map_add' x y := rfl
  map_mul' x y := specialized_mul_e_coordinate q x.coords y.coords

/-- The coordinate of f is an actual unital ring homomorphism. -/
def fAugmentation (q : R) : TableAlgebra q →+* R where
  toFun x := x.coords 8
  map_zero' := rfl
  map_one' := by simp [coords_one, specialized_unit_coordinates]
  map_add' x y := rfl
  map_mul' x y := specialized_mul_f_coordinate q x.coords y.coords

/-- The combined augmentation onto the two idempotent coordinates. -/
def augmentation (q : R) : TableAlgebra q →+* R × R :=
  (eAugmentation q).prod (fAugmentation q)

@[simp] theorem augmentation_apply (q : R) (x : TableAlgebra q) :
    augmentation q x = (x.coords 0, x.coords 8) := rfl

/-- Both idempotent coordinates can be prescribed independently. -/
theorem augmentation_surjective (q : R) : Function.Surjective (augmentation q) := by
  rintro ⟨r, s⟩
  refine ⟨⟨fun i => if i = 0 then r else if i = 8 then s else 0⟩, ?_⟩
  rw [augmentation_apply]
  apply Prod.ext <;> simp

/-- The augmentation kernel as an explicit predicate, independent of ideal APIs. -/
def InAugmentationKernel (q : R) (x : TableAlgebra q) : Prop := augmentation q x = 0

theorem augmentation_kernel_iff (q : R) (x : TableAlgebra q) :
    InAugmentationKernel q x ↔ x.coords 0 = 0 ∧ x.coords 8 = 0 := by
  simp [InAugmentationKernel, Prod.ext_iff]

theorem augmentation_kernel_mul_left (q : R) (x y : TableAlgebra q)
    (hy : InAugmentationKernel q y) : InAugmentationKernel q (x * y) := by
  unfold InAugmentationKernel at *
  rw [map_mul, hy, mul_zero]

theorem augmentation_kernel_mul_right (q : R) (x y : TableAlgebra q)
    (hx : InAugmentationKernel q x) : InAugmentationKernel q (x * y) := by
  unfold InAugmentationKernel at *
  rw [map_mul, hx, zero_mul]

theorem augmentation_kernel_add (q : R) (x y : TableAlgebra q)
    (hx : InAugmentationKernel q x) (hy : InAugmentationKernel q y) :
    InAugmentationKernel q (x + y) := by
  unfold InAugmentationKernel at *
  rw [map_add, hx, hy, zero_add]

theorem augmentation_kernel_neg (q : R) (x : TableAlgebra q)
    (hx : InAugmentationKernel q x) : InAugmentationKernel q (-x) := by
  unfold InAugmentationKernel at *
  rw [map_neg, hx, neg_zero]

theorem radicalBasis_ne_e (a : Fin 18) : radicalBasis a ≠ (0 : Fin 20) := by
  intro h
  have hv := congrArg Fin.val h
  change radicalIndex a = 0 at hv
  have hpos : 0 < radicalIndex a := by
    unfold radicalIndex
    split_ifs <;> omega
  omega

theorem radicalBasis_ne_f (a : Fin 18) : radicalBasis a ≠ (8 : Fin 20) := by
  intro h
  have hv := congrArg Fin.val h
  change radicalIndex a = 8 at hv
  unfold radicalIndex at hv
  split_ifs at hv <;> omega

theorem radicalBasis_injective : Function.Injective radicalBasis := by
  intro a b h
  apply Fin.ext
  have hv := congrArg Fin.val h
  change radicalIndex a = radicalIndex b at hv
  unfold radicalIndex at hv
  split_ifs at hv <;> omega

/-- Every coordinate other than e and f occurs exactly once in the list. -/
theorem radicalBasis_covers (k : Fin 20) (hk0 : k ≠ 0) (hk8 : k ≠ 8) :
    ∃ a : Fin 18, radicalBasis a = k := by
  have hk0v : k.val ≠ 0 := fun h => hk0 (Fin.ext h)
  have hk8v : k.val ≠ 8 := fun h => hk8 (Fin.ext h)
  by_cases hlt : k.val < 8
  · refine ⟨⟨k.val - 1, by omega⟩, ?_⟩
    apply Fin.ext
    change (if k.val - 1 < 7 then k.val - 1 + 1 else k.val - 1 + 2) = k.val
    split_ifs <;> omega
  · refine ⟨⟨k.val - 2, by omega⟩, ?_⟩
    apply Fin.ext
    change (if k.val - 2 < 7 then k.val - 2 + 1 else k.val - 2 + 2) = k.val
    split_ifs <;> omega

omit [CharP R 2] in
theorem radicalSum_at_radicalBasis (U : Fin 18 → R) (a : Fin 18) :
    radicalSum U (radicalBasis a) = U a := by
  classical
  simp [radicalSum, ARCFiniteHochschild.span, ARCFiniteTrilinear.basis,
    Finset.sum_apply, radicalBasis_injective.eq_iff]

omit [CharP R 2] in
theorem radicalSum_e_coordinate (U : Fin 18 → R) : radicalSum U 0 = 0 := by
  classical
  simp [radicalSum, ARCFiniteHochschild.span, ARCFiniteTrilinear.basis,
    Finset.sum_apply, Ne.symm (radicalBasis_ne_e _)]

omit [CharP R 2] in
theorem radicalSum_f_coordinate (U : Fin 18 → R) : radicalSum U 8 = 0 := by
  classical
  simp [radicalSum, ARCFiniteHochschild.span, ARCFiniteTrilinear.basis,
    Finset.sum_apply, Ne.symm (radicalBasis_ne_f _)]

omit [CharP R 2] in
/-- The existing radical-label span is exactly the subspace with both
idempotent coordinates zero; this is an equality of actual vectors. -/
theorem exists_radicalSum_iff (v : Fin 20 → R) :
    (∃ U : Fin 18 → R, radicalSum U = v) ↔ v 0 = 0 ∧ v 8 = 0 := by
  constructor
  · rintro ⟨U, rfl⟩
    exact ⟨radicalSum_e_coordinate U, radicalSum_f_coordinate U⟩
  · rintro ⟨h0, h8⟩
    refine ⟨fun a => v (radicalBasis a), ?_⟩
    funext k
    by_cases hk0 : k = 0
    · subst k
      rw [radicalSum_e_coordinate, h0]
    · by_cases hk8 : k = 8
      · subst k
        rw [radicalSum_f_coordinate, h8]
      · obtain ⟨a, rfl⟩ := radicalBasis_covers k hk0 hk8
        exact radicalSum_at_radicalBasis (fun a => v (radicalBasis a)) a

theorem augmentation_kernel_iff_radicalSum (q : R) (x : TableAlgebra q) :
    InAugmentationKernel q x ↔ ∃ U : Fin 18 → R, radicalSum U = x.coords := by
  rw [augmentation_kernel_iff, exists_radicalSum_iff]

/-- The displayed eighteen-label span is closed under actual multiplication. -/
theorem radicalSum_product_closed (q : R) (U V : Fin 18 → R) :
    ∃ W : Fin 18 → R, specializedMul q (radicalSum U) (radicalSum V) = radicalSum W := by
  have hzero : specializedMul q (radicalSum U) (radicalSum V) 0 = 0 ∧
      specializedMul q (radicalSum U) (radicalSum V) 8 = 0 := by
    rw [specialized_mul_e_coordinate, specialized_mul_f_coordinate,
      radicalSum_e_coordinate U, radicalSum_f_coordinate U, zero_mul, zero_mul]
    exact ⟨rfl, rfl⟩
  obtain ⟨W, hW⟩ := (exists_radicalSum_iff _).mpr hzero
  exact ⟨W, hW.symm⟩

#print axioms polynomial_e_constants
#print axioms polynomial_f_constants
#print axioms eAugmentation
#print axioms fAugmentation
#print axioms augmentation
#print axioms augmentation_surjective
#print axioms augmentation_kernel_iff
#print axioms augmentation_kernel_mul_left
#print axioms augmentation_kernel_mul_right
#print axioms exists_radicalSum_iff
#print axioms augmentation_kernel_iff_radicalSum
#print axioms radicalSum_product_closed

end
end ARCTwentyDimAugmentation
