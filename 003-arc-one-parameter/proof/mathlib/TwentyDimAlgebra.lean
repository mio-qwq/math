import TwentyDimUnit
import FiniteBilinearLaws
import Mathlib.Algebra.Module.TransferInstance
import Mathlib.Algebra.Algebra.Defs
import Mathlib.LinearAlgebra.Dimension.Constructions
import Mathlib.LinearAlgebra.StdBasis

/-!
# The actual specialized twenty-coordinate algebra

A separate wrapper type carries the table multiplication, rather than the
pointwise multiplication of a function space. All ring and algebra laws
come from the frozen semantic table proofs and generic bilinear laws.
This does not construct a Hochschild complex, Ext groups, or the ARC realization.
-/

namespace ARCTwentyDimAlgebra

open ARCTwentyDimAssociativity ARCTwentyDimUnit

variable {R : Type*} [CommRing R] [CharP R 2]

/-- Coordinates of the actual algebra at parameter `q`, with distinct table multiplication. -/
structure TableAlgebra (q : R) where
  coords : Fin 20 → R

noncomputable section

variable (q : R)

def coordsEquiv : TableAlgebra q ≃ (Fin 20 → R) where
  toFun := TableAlgebra.coords
  invFun := TableAlgebra.mk
  left_inv _ := rfl
  right_inv _ := rfl

omit [CommRing R] [CharP R 2] in
@[ext] theorem ext {x y : TableAlgebra q} (h : x.coords = y.coords) : x = y :=
  (coordsEquiv q).injective h

instance tableAddCommGroup : AddCommGroup (TableAlgebra q) :=
  (coordsEquiv q).addCommGroup

omit [CharP R 2] in
@[simp] theorem coords_zero : (0 : TableAlgebra q).coords = 0 := rfl
omit [CharP R 2] in
@[simp] theorem coords_add (x y : TableAlgebra q) : (x + y).coords = x.coords + y.coords := rfl
omit [CharP R 2] in
@[simp] theorem coords_neg (x : TableAlgebra q) : (-x).coords = -x.coords := rfl

instance tableMul : Mul (TableAlgebra q) :=
  ⟨fun x y => ⟨specializedMul q x.coords y.coords⟩⟩

instance tableOne : One (TableAlgebra q) := ⟨⟨specializedUnit q⟩⟩

@[simp] theorem coords_mul (x y : TableAlgebra q) :
    (x * y).coords = specializedMul q x.coords y.coords := rfl

@[simp] theorem coords_one : (1 : TableAlgebra q).coords = specializedUnit q := rfl

/-- A genuine unital ring with the table multiplication; commutativity is not asserted. -/
instance tableRing : Ring (TableAlgebra q) where
  __ := tableAddCommGroup q
  __ := tableMul q
  __ := tableOne q
  mul_assoc x y z := ext q (specialized_mul_associative q x.coords y.coords z.coords)
  one_mul x := ext q (specialized_left_unit q x.coords)
  mul_one x := ext q (specialized_right_unit q x.coords)
  left_distrib x y z := ext q
    (ARCFiniteBilinear.mul_add_right (specializedConstants q) x.coords y.coords z.coords)
  right_distrib x y z := ext q
    (ARCFiniteBilinear.mul_add_left (specializedConstants q) x.coords y.coords z.coords)
  zero_mul x := ext q (ARCFiniteBilinear.mul_zero_left (specializedConstants q) x.coords)
  mul_zero x := ext q (ARCFiniteBilinear.mul_zero_right (specializedConstants q) x.coords)

def coordsAddEquiv : TableAlgebra q ≃+ (Fin 20 → R) where
  __ := coordsEquiv q
  map_add' _ _ := rfl

instance tableModule : Module R (TableAlgebra q) := (coordsAddEquiv q).module R

@[simp] theorem coords_smul (r : R) (x : TableAlgebra q) :
    (r • x).coords = r • x.coords := rfl

def coordsLinearEquiv : TableAlgebra q ≃ₗ[R] (Fin 20 → R) :=
  (coordsAddEquiv q).linearEquiv R

theorem table_smul_mul (r : R) (x y : TableAlgebra q) :
    (r • x) * y = r • (x * y) := by
  apply ext q
  exact ARCFiniteBilinear.mul_smul_left (specializedConstants q) r x.coords y.coords

theorem table_mul_smul (r : R) (x y : TableAlgebra q) :
    x * (r • y) = r • (x * y) := by
  apply ext q
  exact ARCFiniteBilinear.mul_smul_right (specializedConstants q) r x.coords y.coords

/-- The existing pointwise scalar module and table ring form a genuine R-algebra. -/
instance tableAlgebra : Algebra R (TableAlgebra q) :=
  Algebra.ofModule (table_smul_mul q) (table_mul_smul q)

theorem coords_algebraMap (r : R) :
    (algebraMap R (TableAlgebra q) r).coords = r • specializedUnit q := rfl

/-- The actual table algebra has the usual twenty-coordinate module basis. -/
def coordinateBasis : Module.Basis (Fin 20) R (TableAlgebra q) :=
  (Pi.basisFun R (Fin 20)).map (coordsLinearEquiv q).symm

instance tableModuleFree : Module.Free R (TableAlgebra q) :=
  Module.Free.of_basis (coordinateBasis q)

instance tableModuleFinite : Module.Finite R (TableAlgebra q) :=
  Module.Finite.equiv (coordsLinearEquiv q).symm

#print axioms tableRing
#print axioms tableAlgebra
#print axioms coordsLinearEquiv
#print axioms coords_mul
#print axioms coords_one
#print axioms coords_algebraMap
#print axioms coordinateBasis

section Field

variable {K : Type*} [Field K] [CharP K 2] (parameter : K)

/-- In every characteristic-two field the actual table algebra has dimension twenty. -/
theorem table_finrank : Module.finrank K (TableAlgebra parameter) = 20 :=
  (coordsLinearEquiv parameter).finrank_eq.trans (Module.finrank_fin_fun K)

#print axioms table_finrank

end Field

end
end ARCTwentyDimAlgebra
