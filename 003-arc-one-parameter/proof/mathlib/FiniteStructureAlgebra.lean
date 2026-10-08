import FiniteBilinearUnit
import Mathlib.LinearAlgebra.Pi
import Mathlib.Algebra.Algebra.Defs
import Mathlib.LinearAlgebra.StdBasis
import Mathlib.LinearAlgebra.Dimension.Constructions

/-!
# Multiplication from finite structure constants

This generic layer reuses `FiniteBilinear` for associativity and constructs
actual unital semiring, ring and algebra structures from the finite unit
equations. Scalars may belong to any commutative semiring, including
`Polynomial (ZMod 2)`. No bounded encoding or finite enumeration is used
here, and the fixed ARC tables are not instantiated by this file.
-/

namespace ARCFiniteStructure

noncomputable section

variable {R ι : Type*} [CommSemiring R] [Fintype ι]

/-- Structure constants give the product of two basis vectors as a vector. -/
abbrev Constants := ι → ι → (ι → R)

/-- Bilinear extension of the specified basis products to all vectors. -/
def product (C : Constants (R := R) (ι := ι)) (u v : ι → R) : ι → R :=
  ∑ i, ∑ j, (u i * v j) • C i j

/-- The vector sum is exactly the published coordinatewise contraction. -/
theorem product_eq_mul (C : Constants (R := R) (ι := ι)) (u v : ι → R) :
    product C u v = ARCFiniteBilinear.mul C u v := by
  ext k
  simp [product, ARCFiniteBilinear.mul, Finset.sum_apply]

@[simp] theorem product_zero_left (C : Constants (R := R) (ι := ι)) (v : ι → R) :
    product C 0 v = 0 := by
  simp [product]

@[simp] theorem product_zero_right (C : Constants (R := R) (ι := ι)) (u : ι → R) :
    product C u 0 = 0 := by
  simp [product]

theorem product_add_left (C : Constants (R := R) (ι := ι)) (u v w : ι → R) :
    product C (u + v) w = product C u w + product C v w := by
  simp [product, add_mul, add_smul, Finset.sum_add_distrib]

theorem product_add_right (C : Constants (R := R) (ι := ι)) (u v w : ι → R) :
    product C u (v + w) = product C u v + product C u w := by
  simp [product, mul_add, add_smul, Finset.sum_add_distrib]

theorem product_smul_left (C : Constants (R := R) (ι := ι)) (r : R) (u v : ι → R) :
    product C (r • u) v = r • product C u v := by
  simp [product, mul_assoc, mul_smul, Finset.smul_sum]

theorem product_smul_right (C : Constants (R := R) (ι := ι)) (r : R) (u v : ι → R) :
    product C u (r • v) = r • product C u v := by
  simp [product, mul_left_comm, mul_smul, Finset.smul_sum]

theorem product_sum_left {α : Type*} (C : Constants (R := R) (ι := ι))
    (s : Finset α) (u : α → ι → R) (v : ι → R) :
    product C (∑ a ∈ s, u a) v = ∑ a ∈ s, product C (u a) v := by
  classical
  induction s using Finset.induction_on with
  | empty => simp
  | @insert a s ha ih => simp [ha, product_add_left, ih]

theorem product_sum_right {α : Type*} (C : Constants (R := R) (ι := ι))
    (s : Finset α) (u : ι → R) (v : α → ι → R) :
    product C u (∑ a ∈ s, v a) = ∑ a ∈ s, product C u (v a) := by
  classical
  induction s using Finset.induction_on with
  | empty => simp
  | @insert a s ha ih => simp [ha, product_add_right, ih]

variable [DecidableEq ι]

/-- The coordinate basis of the finite free scalar module. -/
def basisVec (i : ι) : ι → R := Pi.single i 1

@[simp] theorem product_basis (C : Constants (R := R) (ι := ι)) (i j : ι) :
    product C (basisVec i) (basisVec j) = C i j := by
  simp [product, basisVec, Pi.single_apply]

theorem product_basis_right (C : Constants (R := R) (ι := ι)) (u : ι → R) (j : ι) :
    product C u (basisVec j) = ∑ i, u i • C i j := by
  simp [product, basisVec, Pi.single_apply]

theorem product_basis_left (C : Constants (R := R) (ι := ι)) (i : ι) (v : ι → R) :
    product C (basisVec i) v = ∑ j, v j • C i j := by
  simp [product, basisVec, Pi.single_apply]

/-- The structure-constant equations, with every coordinate and basis triple
quantified. Coefficients belong to the full scalar semiring. -/
def AssociativeConstants (C : Constants (R := R) (ι := ι)) : Prop :=
  ARCFiniteBilinear.StructureAssociative C

/-- Exact equivalence between structure-constant equations and associativity
on all vectors, without degree or size bounds on their scalar coefficients. -/
theorem product_assoc_iff (C : Constants (R := R) (ι := ι)) :
    (∀ u v w, product C (product C u v) w = product C u (product C v w)) ↔
      AssociativeConstants C := by
  constructor
  · intro h i j k l
    have hb := h (basisVec i) (basisVec j) (basisVec k)
    rw [product_basis, product_basis] at hb
    simp only [product_basis_right, product_basis_left] at hb
    simpa only [Finset.sum_apply, Pi.smul_apply, smul_eq_mul] using
      congrFun hb l
  · intro h u v w
    simpa only [product_eq_mul] using ARCFiniteBilinear.mul_associative C h u v w

/-- Unit-vector equations on the left side of every coordinate basis vector. -/
def LeftUnitConstants (C : Constants (R := R) (ι := ι)) (e : ι → R) : Prop :=
  ARCFiniteBilinear.StructureLeftUnit C e

/-- Unit-vector equations on the right side of every coordinate basis vector. -/
def RightUnitConstants (C : Constants (R := R) (ι := ι)) (e : ι → R) : Prop :=
  ARCFiniteBilinear.StructureRightUnit C e

theorem product_unit_left (C : Constants (R := R) (ι := ι)) (e : ι → R)
    (h : LeftUnitConstants C e) (u : ι → R) : product C e u = u := by
  simpa only [product_eq_mul] using ARCFiniteBilinear.mul_left_unit C e h u

theorem product_unit_right (C : Constants (R := R) (ι := ι)) (e : ι → R)
    (h : RightUnitConstants C e) (u : ι → R) : product C u e = u := by
  simpa only [product_eq_mul] using ARCFiniteBilinear.mul_right_unit C e h u

/-- Sufficient data for a finite free unital algebra. These are proof
obligations, not assumptions silently attached to a concrete ARC table. -/
structure Laws (C : Constants (R := R) (ι := ι)) where
  unit : ι → R
  assoc : AssociativeConstants C
  left_unit : LeftUnitConstants C unit
  right_unit : RightUnitConstants C unit

/-- A separate carrier prevents confusion with pointwise Pi multiplication. -/
def Carrier {C : Constants (R := R) (ι := ι)} (_L : Laws C) := ι → R

variable {C : Constants (R := R) (ι := ι)}

instance carrierAddCommMonoid (L : Laws C) : AddCommMonoid (Carrier L) :=
  inferInstanceAs (AddCommMonoid (ι → R))

instance carrierSemiring (L : Laws C) : Semiring (Carrier L) where
  __ := (inferInstance : AddCommMonoid (Carrier L))
  mul := product C
  one := L.unit
  mul_assoc := (product_assoc_iff C).mpr L.assoc
  one_mul := product_unit_left C L.unit L.left_unit
  mul_one := product_unit_right C L.unit L.right_unit
  left_distrib := product_add_right C
  right_distrib := product_add_left C
  zero_mul := product_zero_left C
  mul_zero := product_zero_right C
  natCast := fun n => n • L.unit
  natCast_zero := zero_nsmul _
  natCast_succ := fun n => succ_nsmul _ _

instance carrierModule (L : Laws C) : Module R (Carrier L) :=
  inferInstanceAs (Module R (ι → R))

/-- The scalar action is the existing coordinatewise action, and the scalar
map is `r ↦ r • L.unit` for the constructed table multiplication. -/
instance carrierAlgebra (L : Laws C) : Algebra R (Carrier L) :=
  Algebra.ofModule (product_smul_left C) (product_smul_right C)

/-- A genuine coordinate basis for the carrier with table multiplication. -/
def carrierBasis (L : Laws C) : Module.Basis ι R (Carrier L) := Pi.basisFun R ι

@[simp] theorem carrierBasis_apply (L : Laws C) (i : ι) :
    carrierBasis L i = basisVec i := by
  exact Pi.basisFun_apply R ι i

instance carrierFree (L : Laws C) : Module.Free R (Carrier L) :=
  Module.Free.of_basis (carrierBasis L)

instance carrierFinite (L : Laws C) : Module.Finite R (Carrier L) :=
  Module.Finite.of_basis (carrierBasis L)

/-- The dimension depends on the coordinate index type, not the multiplication
table. The rank hypothesis excludes degenerate scalar semirings. -/
theorem carrier_finrank [StrongRankCondition R] (L : Laws C) :
    Module.finrank R (Carrier L) = Fintype.card ι :=
  Module.finrank_eq_card_basis (carrierBasis L)

@[simp] theorem carrier_mul (L : Laws C) (u v : Carrier L) :
    u * v = product C u v := rfl

@[simp] theorem carrier_one (L : Laws C) : (1 : Carrier L) = L.unit := rfl

@[simp] theorem carrier_algebraMap (L : Laws C) (r : R) :
    algebraMap R (Carrier L) r = r • L.unit := rfl

@[simp] theorem carrier_basis_mul (L : Laws C) (i j : ι) :
    carrierBasis L i * carrierBasis L j = C i j := by
  rw [carrier_mul, carrierBasis_apply, carrierBasis_apply, product_basis]

/-- Over a commutative ring the additive structure is a group, with the
same coordinatewise operations and the same structure-constant product. -/
instance carrierAddCommGroup {S : Type*} [CommRing S]
    {D : Constants (R := S) (ι := ι)} (L : Laws D) : AddCommGroup (Carrier L) :=
  inferInstanceAs (AddCommGroup (ι → S))

instance carrierRing {S : Type*} [CommRing S]
    {D : Constants (R := S) (ι := ι)} (L : Laws D) : Ring (Carrier L) where
  __ := carrierSemiring L
  __ := carrierAddCommGroup L

#print axioms product_basis
#print axioms product_eq_mul
#print axioms product_assoc_iff
#print axioms product_unit_left
#print axioms product_unit_right
#print axioms carrier_mul
#print axioms carrier_algebraMap
#print axioms carrierSemiring
#print axioms carrierAlgebra
#print axioms carrierRing
#print axioms carrier_basis_mul
#print axioms carrier_finrank

end
end ARCFiniteStructure
