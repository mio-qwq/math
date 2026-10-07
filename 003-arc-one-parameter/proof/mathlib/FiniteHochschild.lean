import FiniteBilinearLaws
import FiniteTrilinear
import Mathlib.Algebra.BigOperators.GroupWithZero.Action

/-!
# Finite four-linear extension of the unsigned degree-three formula

The five-term expression is unsigned; in characteristic two these are the
signs of the Hochschild differential. This generic file proves linearity
and basis-span extension only. It does not construct a cochain complex or
assert a cocycle property of any particular cochain.
-/

namespace ARCFiniteHochschild

open ARCFiniteBilinear ARCFiniteTrilinear
open scoped BigOperators

variable {R I : Type*} [CommSemiring R] [Fintype I]

noncomputable section

/-- The actual unsigned five-term degree-three expression. -/
def differential3 (B : I → I → I → R) (P : I → I → I → I → R)
    (u v w z : I → R) : I → R :=
  mul B u (eval P v w z) + eval P (mul B u v) w z +
    eval P u (mul B v w) z + eval P u v (mul B w z) + mul B (eval P u v w) z

abbrev D3 := @differential3

theorem differential3_add_first (B : I → I → I → R) (P : I → I → I → I → R)
    (u u' v w z : I → R) :
    differential3 B P (u + u') v w z =
      differential3 B P u v w z + differential3 B P u' v w z := by
  simp only [differential3, mul_add_left, eval_add_first]
  ac_rfl

theorem differential3_add_second (B : I → I → I → R) (P : I → I → I → I → R)
    (u v v' w z : I → R) :
    differential3 B P u (v + v') w z =
      differential3 B P u v w z + differential3 B P u v' w z := by
  simp only [differential3, mul_add_left, mul_add_right,
    eval_add_first, eval_add_second]
  ac_rfl

theorem differential3_add_third (B : I → I → I → R) (P : I → I → I → I → R)
    (u v w w' z : I → R) :
    differential3 B P u v (w + w') z =
      differential3 B P u v w z + differential3 B P u v w' z := by
  simp only [differential3, mul_add_left, mul_add_right,
    eval_add_second, eval_add_third]
  ac_rfl

theorem differential3_add_fourth (B : I → I → I → R) (P : I → I → I → I → R)
    (u v w z z' : I → R) :
    differential3 B P u v w (z + z') =
      differential3 B P u v w z + differential3 B P u v w z' := by
  simp only [differential3, mul_add_right, eval_add_third]
  ac_rfl

theorem differential3_smul_first (B : I → I → I → R) (P : I → I → I → I → R)
    (r : R) (u v w z : I → R) :
    differential3 B P (r • u) v w z = r • differential3 B P u v w z := by
  simp only [differential3, mul_smul_left, eval_smul_first, smul_add]

theorem differential3_smul_second (B : I → I → I → R) (P : I → I → I → I → R)
    (r : R) (u v w z : I → R) :
    differential3 B P u (r • v) w z = r • differential3 B P u v w z := by
  simp only [differential3, mul_smul_left, mul_smul_right,
    eval_smul_first, eval_smul_second, smul_add]

theorem differential3_smul_third (B : I → I → I → R) (P : I → I → I → I → R)
    (r : R) (u v w z : I → R) :
    differential3 B P u v (r • w) z = r • differential3 B P u v w z := by
  simp only [differential3, mul_smul_left, mul_smul_right,
    eval_smul_second, eval_smul_third, smul_add]

theorem differential3_smul_fourth (B : I → I → I → R) (P : I → I → I → I → R)
    (r : R) (u v w z : I → R) :
    differential3 B P u v w (r • z) = r • differential3 B P u v w z := by
  simp only [differential3, mul_smul_right, eval_smul_third, smul_add]

/-- Fix the last three inputs to obtain a linear map in the first input. -/
def firstLinear (B : I → I → I → R) (P : I → I → I → I → R)
    (v w z : I → R) : (I → R) →ₗ[R] (I → R) where
  toFun u := differential3 B P u v w z
  map_add' u u' := differential3_add_first B P u u' v w z
  map_smul' r u := differential3_smul_first B P r u v w z

def secondLinear (B : I → I → I → R) (P : I → I → I → I → R)
    (u w z : I → R) : (I → R) →ₗ[R] (I → R) where
  toFun v := differential3 B P u v w z
  map_add' v v' := differential3_add_second B P u v v' w z
  map_smul' r v := differential3_smul_second B P r u v w z

def thirdLinear (B : I → I → I → R) (P : I → I → I → I → R)
    (u v z : I → R) : (I → R) →ₗ[R] (I → R) where
  toFun w := differential3 B P u v w z
  map_add' w w' := differential3_add_third B P u v w w' z
  map_smul' r w := differential3_smul_third B P r u v w z

def fourthLinear (B : I → I → I → R) (P : I → I → I → I → R)
    (u v w : I → R) : (I → R) →ₗ[R] (I → R) where
  toFun z := differential3 B P u v w z
  map_add' z z' := differential3_add_fourth B P u v w z z'
  map_smul' r z := differential3_smul_fourth B P r u v w z

variable {J : Type*} [Fintype J]

theorem weighted_sum_first (B : I → I → I → R) (P : I → I → I → I → R)
    (U : J → I → R) (r : J → R) (v w z : I → R) :
    differential3 B P (∑ a, r a • U a) v w z =
      ∑ a, r a • differential3 B P (U a) v w z := by
  change firstLinear B P v w z (∑ a, r a • U a) = _
  rw [map_sum]
  simp only [map_smul, firstLinear, LinearMap.coe_mk, AddHom.coe_mk]

theorem weighted_sum_second (B : I → I → I → R) (P : I → I → I → I → R)
    (V : J → I → R) (s : J → R) (u w z : I → R) :
    differential3 B P u (∑ b, s b • V b) w z =
      ∑ b, s b • differential3 B P u (V b) w z := by
  change secondLinear B P u w z (∑ b, s b • V b) = _
  rw [map_sum]
  simp only [map_smul, secondLinear, LinearMap.coe_mk, AddHom.coe_mk]

theorem weighted_sum_third (B : I → I → I → R) (P : I → I → I → I → R)
    (W : J → I → R) (t : J → R) (u v z : I → R) :
    differential3 B P u v (∑ c, t c • W c) z =
      ∑ c, t c • differential3 B P u v (W c) z := by
  change thirdLinear B P u v z (∑ c, t c • W c) = _
  rw [map_sum]
  simp only [map_smul, thirdLinear, LinearMap.coe_mk, AddHom.coe_mk]

theorem weighted_sum_fourth (B : I → I → I → R) (P : I → I → I → I → R)
    (Z : J → I → R) (l : J → R) (u v w : I → R) :
    differential3 B P u v w (∑ d, l d • Z d) =
      ∑ d, l d • differential3 B P u v w (Z d) := by
  change fourthLinear B P u v w (∑ d, l d • Z d) = _
  rw [map_sum]
  simp only [map_smul, fourthLinear, LinearMap.coe_mk, AddHom.coe_mk]

/-- Expand the unsigned formula on four arbitrary finite weighted families. -/
theorem weighted_four_sums (B : I → I → I → R) (P : I → I → I → I → R)
    (U V W Z : J → I → R) (r s t l : J → R) :
    differential3 B P (∑ a, r a • U a) (∑ b, s b • V b)
      (∑ c, t c • W c) (∑ d, l d • Z d) =
      ∑ a, ∑ b, ∑ c, ∑ d, (r a * s b * t c * l d) •
        differential3 B P (U a) (V b) (W c) (Z d) := by
  simp_rw [weighted_sum_first, weighted_sum_second, weighted_sum_third,
    weighted_sum_fourth, Finset.smul_sum, smul_smul, mul_assoc]

section Basis

variable [DecidableEq I]

/-- Finite linear combinations of the selected basis vectors. -/
def span (s : J → I) (U : J → R) : I → R :=
  ∑ a, U a • basis (s a)

/-- Vanishing on selected basis quadruples extends to all their finite spans. -/
theorem basis_span_closure (B : I → I → I → R) (P : I → I → I → I → R)
    (s : J → I)
    (h : ∀ a b c d, differential3 B P (basis (s a)) (basis (s b))
      (basis (s c)) (basis (s d)) = 0)
    (U V W Z : J → R) :
    differential3 B P (span s U) (span s V) (span s W) (span s Z) = 0 := by
  unfold span
  rw [weighted_four_sums]
  simp only [h, smul_zero, Finset.sum_const_zero]

end Basis

#print axioms differential3_add_first
#print axioms differential3_smul_fourth
#print axioms weighted_four_sums
#print axioms basis_span_closure

end
end ARCFiniteHochschild
