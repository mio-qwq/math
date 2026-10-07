import Mathlib.Algebra.Algebra.Defs
import Mathlib.LinearAlgebra.BilinearMap
import Mathlib.Algebra.CharP.Two
import Mathlib.Tactic.Abel

/-!
# An actual low-degree Hochschild cancellation law in characteristic two

The unsigned four- and five-term formulas are defined on an actual
associative algebra. Their composition is zero. The degree-two formula
of an R-bilinear map is also packaged as three actual nested linear maps.
This file does not construct the full Hochschild complex or Ext objects.
-/

namespace ARCHochschildLowDegrees

variable {A : Type*} [Ring A]

/-- The unsigned four-term formula on an actual multiplication. -/
def differential2 (G : A → A → A) (x y z : A) : A :=
  x * G y z + G (x * y) z + G x (y * z) + G x y * z

/-- The unsigned five-term formula on an actual multiplication. -/
def differential3 (F : A → A → A → A) (x y z w : A) : A :=
  x * F y z w + F (x * y) z w + F x (y * z) w + F x y (z * w) + F x y z * w

section CharacteristicTwo

variable [CharP A 2]

/-- Associativity and characteristic-two cancellation give the low-degree
composition law even before imposing linearity on the input function. -/
theorem differential3_differential2 (G : A → A → A) (x y z w : A) :
    differential3 (differential2 G) x y z w = 0 := by
  simp only [differential3, differential2, mul_add, add_mul, mul_assoc]
  abel_nf
  simp only [CharTwo.two_zsmul, zero_add]

end CharacteristicTwo

section Algebra

variable {R : Type*} [CommRing R] [Algebra R A]

noncomputable section

theorem differential2_add_first (G : A →ₗ[R] A →ₗ[R] A) (x x' y z : A) :
    differential2 (fun a b => G a b) (x + x') y z =
      differential2 (fun a b => G a b) x y z +
      differential2 (fun a b => G a b) x' y z := by
  simp only [differential2, add_mul, map_add, LinearMap.add_apply]
  ac_rfl

theorem differential2_add_second (G : A →ₗ[R] A →ₗ[R] A) (x y y' z : A) :
    differential2 (fun a b => G a b) x (y + y') z =
      differential2 (fun a b => G a b) x y z +
      differential2 (fun a b => G a b) x y' z := by
  simp only [differential2, add_mul, mul_add, map_add, LinearMap.add_apply]
  ac_rfl

theorem differential2_add_third (G : A →ₗ[R] A →ₗ[R] A) (x y z z' : A) :
    differential2 (fun a b => G a b) x y (z + z') =
      differential2 (fun a b => G a b) x y z +
      differential2 (fun a b => G a b) x y z' := by
  simp only [differential2, mul_add, map_add]
  ac_rfl

theorem differential2_smul_first (G : A →ₗ[R] A →ₗ[R] A) (r : R) (x y z : A) :
    differential2 (fun a b => G a b) (r • x) y z =
      r • differential2 (fun a b => G a b) x y z := by
  simp only [differential2, smul_mul_assoc,
    map_smul, LinearMap.smul_apply, smul_add]

theorem differential2_smul_second (G : A →ₗ[R] A →ₗ[R] A) (r : R) (x y z : A) :
    differential2 (fun a b => G a b) x (r • y) z =
      r • differential2 (fun a b => G a b) x y z := by
  simp only [differential2, smul_mul_assoc, Algebra.mul_smul_comm,
    map_smul, LinearMap.smul_apply, smul_add]

theorem differential2_smul_third (G : A →ₗ[R] A →ₗ[R] A) (r : R) (x y z : A) :
    differential2 (fun a b => G a b) x y (r • z) =
      r • differential2 (fun a b => G a b) x y z := by
  simp only [differential2, Algebra.mul_smul_comm, map_smul, smul_add]

/-- The actual degree-two formula is trilinear on every associative R-algebra. -/
def differential2Linear (G : A →ₗ[R] A →ₗ[R] A) :
    A →ₗ[R] A →ₗ[R] A →ₗ[R] A where
  toFun x :=
    { toFun y :=
        { toFun z := differential2 (fun a b => G a b) x y z
          map_add' z z' := differential2_add_third G x y z z'
          map_smul' r z := differential2_smul_third G r x y z }
      map_add' y y' := by ext z; exact differential2_add_second G x y y' z
      map_smul' r y := by ext z; exact differential2_smul_second G r x y z }
  map_add' x x' := by ext y z; exact differential2_add_first G x x' y z
  map_smul' r x := by ext y z; exact differential2_smul_first G r x y z

@[simp] theorem differential2Linear_apply (G : A →ₗ[R] A →ₗ[R] A) (x y z : A) :
    differential2Linear G x y z = differential2 (fun a b => G a b) x y z := rfl

variable [CharP A 2]

/-- The unsigned differential of an actual bilinear cochain's coboundary
vanishes on every quadruple of elements of the actual algebra. -/
theorem bilinear_coboundary_closed (G : A →ₗ[R] A →ₗ[R] A) (x y z w : A) :
    differential3 (fun a b c => differential2Linear G a b c) x y z w = 0 :=
  differential3_differential2 (fun a b => G a b) x y z w

#print axioms differential2Linear
#print axioms bilinear_coboundary_closed

end
end Algebra

#print axioms differential3_differential2

end ARCHochschildLowDegrees
