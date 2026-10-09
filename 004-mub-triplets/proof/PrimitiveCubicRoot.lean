import Mathlib.Basic.Complex.Basic
import Mathlib.Analysis.Real.Sqrt
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.LinearCombination

noncomputable section

namespace MUBTriplets.PrimitiveCubicRoot

/-- The positive-imaginary primitive cube root used by the concrete matrices. -/
def omega : ℂ := ⟨-1 / 2, Real.sqrt 3 / 2⟩

theorem omega_quadratic : omega ^ 2 + omega + 1 = 0 := by
  have hs : Real.sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  apply Complex.ext
  · simp [omega, pow_two, Complex.mul_re]
    nlinarith [hs]
  · simp [omega, pow_two, Complex.mul_im]
    ring

theorem omega_cube : omega ^ 3 = 1 := by
  linear_combination (omega - 1) * omega_quadratic

theorem omega_ne_one : omega ≠ 1 := by
  intro h
  have he := congrArg Complex.re h
  norm_num [omega] at he

theorem omega_star : star omega = omega ^ 2 := by
  have hs : Real.sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  apply Complex.ext
  · simp [omega, pow_two, Complex.mul_re, Complex.star_def]
    nlinarith [hs]
  · simp [omega, pow_two, Complex.mul_im, Complex.star_def]
    ring

theorem omega_normSq : Complex.normSq omega = 1 := by
  have hs : Real.sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  simp [omega, Complex.normSq_apply]
  nlinarith [hs]

#print axioms omega_cube
#print axioms omega_ne_one
#print axioms omega_star
#print axioms omega_normSq

end MUBTriplets.PrimitiveCubicRoot
