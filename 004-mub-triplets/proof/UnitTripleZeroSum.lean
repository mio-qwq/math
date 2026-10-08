import Mathlib.Basic.Complex.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-!
The algebraic zero-mode obstruction for a three-entry complex phase vector.
All statements use actual complex entries and normSq. A unit triple with sum
zero is a phase times (1,r,r^2), for a primitive third root r. At any fixed
primitive third root omega, one of its other two Fourier sums has normSq 9.
The resulting bounded-mode theorem assumes actual three-point Fourier mode
bounds; the separate implication from a six-by-six matrix Gram equation to
these bounds is not proved in this source. These are standard ingredients,
not a resolution of the general MUB problem or a mathematical novelty claim.
-/

noncomputable section

namespace MUBTriplets.UnitTripleZeroSum

private theorem unit_mul_star (x : ℂ) (hx : Complex.normSq x = 1) :
    x * star x = 1 := by
  simp only [Complex.star_def, Complex.mul_conj, hx, Complex.ofReal_one]

private theorem unit_ne_zero (x : ℂ) (hx : Complex.normSq x = 1) : x ≠ 0 := by
  intro h
  subst x
  norm_num at hx

/-- Three unit phases summing to zero satisfy the exact quadratic relation. -/
theorem unit_zero_sum_quadratic (x y z : ℂ)
    (hx : Complex.normSq x = 1) (hy : Complex.normSq y = 1)
    (hz : Complex.normSq z = 1) (hsum : x + y + z = 0) :
    x ^ 2 + x * y + y ^ 2 = 0 := by
  have hx' := unit_mul_star x hx
  have hy' := unit_mul_star y hy
  have hz' := unit_mul_star z hz
  have hc : star x + star y + star z = 0 := by
    simpa only [star_add, star_zero] using congrArg star hsum
  have he : x * y + x * z + y * z = 0 := by
    calc
      x * y + x * z + y * z =
          (x * y) * (z * star z) + (x * z) * (y * star y) +
            (y * z) * (x * star x) := by rw [hx', hy', hz']; ring
      _ = x * y * z * (star x + star y + star z) := by ring
      _ = 0 := by rw [hc]; ring
  linear_combination (x + y) * hsum - he

/-- The cyclic ratio is a primitive cube root, without a genericity assumption. -/
theorem unit_zero_sum_ratio (x y z : ℂ)
    (hx : Complex.normSq x = 1) (hy : Complex.normSq y = 1)
    (hz : Complex.normSq z = 1) (hsum : x + y + z = 0) :
    let r := y / x
    r ^ 2 + r + 1 = 0 ∧ r ^ 3 = 1 ∧ r ≠ 1 ∧
      y = x * r ∧ z = x * r ^ 2 ∧ Complex.normSq r = 1 := by
  dsimp only
  have hx0 := unit_ne_zero x hx
  have hpoly := unit_zero_sum_quadratic x y z hx hy hz hsum
  have hq : (y / x) ^ 2 + y / x + 1 = 0 := by
    field_simp [hx0]
    linear_combination hpoly
  have hcube : (y / x) ^ 3 = 1 := by
    linear_combination (y / x - 1) * hq
  have hn : y / x ≠ 1 := by
    intro h
    rw [h] at hq
    norm_num at hq
  have hyform : y = x * (y / x) := by field_simp [hx0]
  have hzform : z = x * (y / x) ^ 2 := by
    field_simp [hx0]
    linear_combination x * hsum - hpoly
  have hrnorm : Complex.normSq (y / x) = 1 := by
    rw [Complex.normSq_div, hy, hx]
    norm_num
  exact ⟨hq, hcube, hn, hyform, hzform, hrnorm⟩

private theorem primitive_quadratic (omega : ℂ)
    (hcube : omega ^ 3 = 1) (hone : omega ≠ 1) :
    omega ^ 2 + omega + 1 = 0 := by
  have h : (omega - 1) * (omega ^ 2 + omega + 1) = 0 := by
    linear_combination hcube
  exact (mul_eq_zero.mp h).resolve_left (sub_ne_zero.mpr hone)

private theorem primitive_orientation (r omega : ℂ)
    (hr : r ^ 2 + r + 1 = 0)
    (hcube : omega ^ 3 = 1) (hone : omega ≠ 1) :
    r = omega ∨ r = omega ^ 2 := by
  have hq := primitive_quadratic omega hcube hone
  have hs : omega ^ 2 + omega = -1 := by linear_combination hq
  have hf : (r - omega) * (r - omega ^ 2) = 0 := by
    calc
      (r - omega) * (r - omega ^ 2) =
          r ^ 2 - r * (omega ^ 2 + omega) + omega ^ 3 := by ring
      _ = r ^ 2 + r + 1 := by rw [hs, hcube]; ring
      _ = 0 := hr
  simpa only [sub_eq_zero] using mul_eq_zero.mp hf

/-- At a fixed primitive root, a zero unit mode forces another squared mode 9. -/
theorem zero_mode_forces_large_other_mode (x y z omega : ℂ)
    (hx : Complex.normSq x = 1) (hy : Complex.normSq y = 1)
    (hz : Complex.normSq z = 1) (hsum : x + y + z = 0)
    (hcube : omega ^ 3 = 1) (hone : omega ≠ 1) :
    Complex.normSq (x + y * omega + z * omega ^ 2) = 9 ∨
      Complex.normSq (x + y * omega ^ 2 + z * omega) = 9 := by
  obtain ⟨hq, _, _, hyform, hzform, _⟩ := unit_zero_sum_ratio x y z hx hy hz hsum
  have hnorm : Complex.normSq ((3 : ℂ) * x) = 9 := by
    rw [Complex.normSq_mul, hx]
    norm_num
  rcases primitive_orientation (y / x) omega hq hcube hone with hr | hr
  · right
    have h : x + y * omega ^ 2 + z * omega = 3 * x := by
      rw [hyform, hzform, hr]
      calc
        x + x * omega * omega ^ 2 + x * omega ^ 2 * omega =
            x + 2 * x * omega ^ 3 := by ring
        _ = 3 * x := by rw [hcube]; ring
    rw [h]
    exact hnorm
  · left
    have hfour : (omega ^ 2) ^ 2 = omega := by
      calc
        (omega ^ 2) ^ 2 = omega ^ 3 * omega := by ring
        _ = omega := by rw [hcube]; ring
    have h : x + y * omega + z * omega ^ 2 = 3 * x := by
      rw [hyform, hzform, hr, hfour]
      calc
        x + x * omega ^ 2 * omega + x * omega * omega ^ 2 =
            x + 2 * x * omega ^ 3 := by ring
        _ = 3 * x := by rw [hcube]; ring
    rw [h]
    exact hnorm

/-- Actual bounds on the two other modes exclude a zero sum. -/
theorem zero_mode_excluded_of_other_bounds (x y z omega : ℂ)
    (hx : Complex.normSq x = 1) (hy : Complex.normSq y = 1)
    (hz : Complex.normSq z = 1)
    (hcube : omega ^ 3 = 1) (hone : omega ≠ 1)
    (hfirst : Complex.normSq (x + y * omega + z * omega ^ 2) ≤ 6)
    (hsecond : Complex.normSq (x + y * omega ^ 2 + z * omega) ≤ 6) :
    x + y + z ≠ 0 := by
  intro hsum
  rcases zero_mode_forces_large_other_mode x y z omega hx hy hz hsum hcube hone
      with h | h
  · rw [h] at hfirst
    norm_num at hfirst
  · rw [h] at hsecond
    norm_num at hsecond

/-- Every complex cube root of one has normSq one, including the root one. -/
theorem normSq_of_cube_root (theta : ℂ) (htheta : theta ^ 3 = 1) :
    Complex.normSq theta = 1 := by
  have hp : Complex.normSq theta ^ 3 = 1 := by
    simpa only [map_pow, map_one] using congrArg Complex.normSq htheta
  have hpos : 0 < Complex.normSq theta ^ 2 + Complex.normSq theta + 1 := by
    nlinarith [Complex.normSq_nonneg theta, sq_nonneg (Complex.normSq theta)]
  have hf : (Complex.normSq theta - 1) *
      (Complex.normSq theta ^ 2 + Complex.normSq theta + 1) = 0 := by
    linear_combination hp
  have h := (mul_eq_zero.mp hf).resolve_right (ne_of_gt hpos)
  linear_combination h

/-- Cube-root Fourier bounds exclude every zero mode, without selecting exp roots. -/
theorem root_mode_nonzero_of_all_root_bounds (x y z theta : ℂ)
    (hx : Complex.normSq x = 1) (hy : Complex.normSq y = 1)
    (hz : Complex.normSq z = 1) (htheta : theta ^ 3 = 1)
    (hbound : ∀ eta : ℂ, eta ^ 3 = 1 →
      Complex.normSq (x + y * eta + z * eta ^ 2) ≤ 6) :
    x + y * theta + z * theta ^ 2 ≠ 0 := by
  intro hzero
  have htunit := normSq_of_cube_root theta htheta
  have hyunit : Complex.normSq (y * theta) = 1 := by
    rw [Complex.normSq_mul, hy, htunit]; norm_num
  have hzunit : Complex.normSq (z * theta ^ 2) = 1 := by
    rw [Complex.normSq_mul, map_pow, hz, htunit]; norm_num
  let r := (y * theta) / x
  obtain ⟨_, hrcube, _, hyform, hzform, hrunit⟩ :=
    unit_zero_sum_ratio x (y * theta) (z * theta ^ 2) hx hyunit hzunit hzero
  change r ^ 3 = 1 at hrcube
  change y * theta = x * r at hyform
  change z * theta ^ 2 = x * r ^ 2 at hzform
  change Complex.normSq r = 1 at hrunit
  have hr0 := unit_ne_zero r hrunit
  have hetacube : (theta / r) ^ 3 = 1 := by
    rw [div_pow, htheta, hrcube]; norm_num
  have hyeta : y * (theta / r) = x := by
    field_simp [hr0]
    linear_combination hyform
  have hzeta : z * (theta / r) ^ 2 = x := by
    field_simp [hr0]
    linear_combination hzform
  have hamp : x + y * (theta / r) + z * (theta / r) ^ 2 = 3 * x := by
    rw [hyeta, hzeta]; ring
  have hlarge : Complex.normSq (x + y * (theta / r) + z * (theta / r) ^ 2) = 9 := by
    rw [hamp, Complex.normSq_mul, hx]; norm_num
  have hsmall := hbound (theta / r) hetacube
  rw [hlarge] at hsmall
  norm_num at hsmall

#print axioms unit_zero_sum_quadratic
#print axioms unit_zero_sum_ratio
#print axioms zero_mode_forces_large_other_mode
#print axioms zero_mode_excluded_of_other_bounds
#print axioms normSq_of_cube_root
#print axioms root_mode_nonzero_of_all_root_bounds

end MUBTriplets.UnitTripleZeroSum
