import FiniteBilinear
import Mathlib.Algebra.Module.LinearMap.Defs
import Mathlib.Algebra.Module.Pi

/-!
# Additive and scalar laws of finite structure-constant multiplication

These are universally quantified laws over every commutative semiring and
every finite coordinate set. They use the existing `ARCFiniteBilinear.mul`
definition. No specific table, enumeration, characteristic restriction,
unit, or associativity assumption is needed.

The laws are intended to support a later algebra construction; this file
does not install an algebra instance or prove the full ARC theorem.
-/

namespace ARCFiniteBilinear

open scoped BigOperators

variable {R I : Type*} [CommSemiring R] [Fintype I]

noncomputable section

/-- Finite structure-constant multiplication is additive in its first argument. -/
theorem mul_add_left (B : I → I → I → R) (u v w : I → R) :
    mul B (u + v) w = mul B u w + mul B v w := by
  funext k
  simp only [mul, Pi.add_apply, add_mul, Finset.sum_add_distrib]

/-- Finite structure-constant multiplication is additive in its second argument. -/
theorem mul_add_right (B : I → I → I → R) (u v w : I → R) :
    mul B u (v + w) = mul B u v + mul B u w := by
  funext k
  simp only [mul, Pi.add_apply, mul_add, add_mul, Finset.sum_add_distrib]

@[simp] theorem mul_zero_left (B : I → I → I → R) (v : I → R) :
    mul B 0 v = 0 := by
  funext k
  simp [mul]

@[simp] theorem mul_zero_right (B : I → I → I → R) (u : I → R) :
    mul B u 0 = 0 := by
  funext k
  simp [mul]

/-- Scalar multiplication of the first vector factors out of the product. -/
theorem mul_smul_left (B : I → I → I → R) (c : R) (u v : I → R) :
    mul B (c • u) v = c • mul B u v := by
  funext k
  simp only [mul, Pi.smul_apply, smul_eq_mul, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro a ha
  apply Finset.sum_congr rfl
  intro b hb
  ac_rfl

/-- Scalar multiplication of the second vector factors out of the product. -/
theorem mul_smul_right (B : I → I → I → R) (c : R) (u v : I → R) :
    mul B u (c • v) = c • mul B u v := by
  funext k
  simp only [mul, Pi.smul_apply, smul_eq_mul, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro a ha
  apply Finset.sum_congr rfl
  intro b hb
  ac_rfl

/-- Both scalars can be factored simultaneously. -/
theorem mul_smul_smul (B : I → I → I → R) (c d : R) (u v : I → R) :
    mul B (c • u) (d • v) = (c * d) • mul B u v := by
  rw [mul_smul_left, mul_smul_right]
  funext k
  simp only [Pi.smul_apply, smul_eq_mul]
  exact (mul_assoc c d (mul B u v k)).symm

/-- Multiplication by a fixed right vector as an actual linear map. -/
def leftLinearMap (B : I → I → I → R) (v : I → R) : (I → R) →ₗ[R] (I → R) where
  toFun u := mul B u v
  map_add' u w := mul_add_left B u w v
  map_smul' c u := mul_smul_left B c u v

/-- Multiplication by a fixed left vector as an actual linear map. -/
def rightLinearMap (B : I → I → I → R) (u : I → R) : (I → R) →ₗ[R] (I → R) where
  toFun v := mul B u v
  map_add' v w := mul_add_right B u v w
  map_smul' c v := mul_smul_right B c u v

@[simp] theorem leftLinearMap_apply (B : I → I → I → R) (u v : I → R) :
    leftLinearMap B v u = mul B u v := rfl

@[simp] theorem rightLinearMap_apply (B : I → I → I → R) (u v : I → R) :
    rightLinearMap B u v = mul B u v := rfl

#print axioms mul_add_left
#print axioms mul_add_right
#print axioms mul_zero_left
#print axioms mul_zero_right
#print axioms mul_smul_left
#print axioms mul_smul_right
#print axioms mul_smul_smul
#print axioms leftLinearMap_apply
#print axioms rightLinearMap_apply

end
end ARCFiniteBilinear
