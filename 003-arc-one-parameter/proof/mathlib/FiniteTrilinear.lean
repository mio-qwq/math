import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Algebra.Module.LinearMap.Defs
import Mathlib.Algebra.Module.Pi

/-!
# Trilinear evaluation of finite structure constants

Generic finite-coordinate trilinear laws over every commutative semiring.
No particular cochain, multiplication table, cocycle identity, or finite
enumeration is assumed or introduced.
-/

namespace ARCFiniteTrilinear

open scoped BigOperators

variable {R I : Type*} [CommSemiring R] [Fintype I]

noncomputable section

/-- Evaluate four-index structure constants on three input vectors. -/
def eval (P : I → I → I → I → R) (u v w : I → R) : I → R :=
  fun k => ∑ a, ∑ b, ∑ c, u a * v b * w c * P a b c k

theorem eval_add_first (P : I → I → I → I → R) (u v w z : I → R) :
    eval P (u + v) w z = eval P u w z + eval P v w z := by
  funext k
  simp only [eval, Pi.add_apply, add_mul, Finset.sum_add_distrib]

theorem eval_add_second (P : I → I → I → I → R) (u v w z : I → R) :
    eval P u (v + w) z = eval P u v z + eval P u w z := by
  funext k
  simp only [eval, Pi.add_apply, mul_add, add_mul, Finset.sum_add_distrib]

theorem eval_add_third (P : I → I → I → I → R) (u v w z : I → R) :
    eval P u v (w + z) = eval P u v w + eval P u v z := by
  funext k
  simp only [eval, Pi.add_apply, mul_add, add_mul, Finset.sum_add_distrib]

theorem eval_smul_first (P : I → I → I → I → R) (r : R) (u v w : I → R) :
    eval P (r • u) v w = r • eval P u v w := by
  funext k
  simp only [eval, Pi.smul_apply, smul_eq_mul, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro a ha
  apply Finset.sum_congr rfl
  intro b hb
  apply Finset.sum_congr rfl
  intro c hc
  ac_rfl

theorem eval_smul_second (P : I → I → I → I → R) (r : R) (u v w : I → R) :
    eval P u (r • v) w = r • eval P u v w := by
  funext k
  simp only [eval, Pi.smul_apply, smul_eq_mul, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro a ha
  apply Finset.sum_congr rfl
  intro b hb
  apply Finset.sum_congr rfl
  intro c hc
  ac_rfl

theorem eval_smul_third (P : I → I → I → I → R) (r : R) (u v w : I → R) :
    eval P u v (r • w) = r • eval P u v w := by
  funext k
  simp only [eval, Pi.smul_apply, smul_eq_mul, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro a ha
  apply Finset.sum_congr rfl
  intro b hb
  apply Finset.sum_congr rfl
  intro c hc
  ac_rfl

@[simp] theorem eval_zero_first (P : I → I → I → I → R) (v w : I → R) :
    eval P 0 v w = 0 := by funext k; simp [eval]

@[simp] theorem eval_zero_second (P : I → I → I → I → R) (u w : I → R) :
    eval P u 0 w = 0 := by funext k; simp [eval]

@[simp] theorem eval_zero_third (P : I → I → I → I → R) (u v : I → R) :
    eval P u v 0 = 0 := by funext k; simp [eval]

section Basis

variable [DecidableEq I]

/-- One standard input basis vector. -/
def basis (i : I) : I → R := fun j => if j = i then 1 else 0

/-- Three input basis vectors recover the prescribed structure constants. -/
theorem eval_basis (P : I → I → I → I → R) (a b c : I) :
    eval P (basis a) (basis b) (basis c) = P a b c := by
  funext k
  simp [eval, basis, ite_mul, mul_ite]

end Basis

/-- Actual nested R-linear maps package the three separately linear slots. -/
def trilinearMap (P : I → I → I → I → R) :
    (I → R) →ₗ[R] (I → R) →ₗ[R] (I → R) →ₗ[R] (I → R) where
  toFun u :=
    { toFun v :=
        { toFun w := eval P u v w
          map_add' w z := eval_add_third P u v w z
          map_smul' r w := eval_smul_third P r u v w }
      map_add' v z := by ext w k; exact congrFun (eval_add_second P u v z w) k
      map_smul' r v := by ext w k; exact congrFun (eval_smul_second P r u v w) k }
  map_add' u z := by ext v w k; exact congrFun (eval_add_first P u z v w) k
  map_smul' r u := by ext v w k; exact congrFun (eval_smul_first P r u v w) k

@[simp] theorem trilinearMap_apply (P : I → I → I → I → R) (u v w : I → R) :
    trilinearMap P u v w = eval P u v w := rfl

#print axioms eval_add_first
#print axioms eval_add_second
#print axioms eval_add_third
#print axioms eval_smul_first
#print axioms eval_smul_second
#print axioms eval_smul_third
#print axioms eval_basis
#print axioms trilinearMap

end
end ARCFiniteTrilinear
