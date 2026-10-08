import CubeRootGramModes

/-!
Actual off-diagonal six-by-six Gram equations match opposite circulant
mode norm squares. These are consequences of the single actual H*H=6I
equation, without flatness, inverses, or a second supplied Gram equation.
This supplies the actual equal-power premise for future phase retrieval;
it does not yet classify ratio multisets or prove product cancellation.
-/

noncomputable section
open MUBTriplets.CirculantCharacter MUBTriplets.CubeRootGramModes

namespace MUBTriplets.CubeRootGramMatching

private theorem star_cube_root (theta : ℂ) (htheta : theta ^ 3 = 1) :
    star theta = theta ^ 2 := by
  have hu : theta * star theta = 1 := by
    simp only [Complex.star_def, Complex.mul_conj,
      UnitTripleZeroSum.normSq_of_cube_root theta htheta, Complex.ofReal_one]
  calc
    star theta = theta ^ 3 * star theta := by rw [htheta]; ring
    _ = theta ^ 2 * (theta * star theta) := by ring
    _ = theta ^ 2 := by rw [hu]; ring

/-- Exact cross-mode polynomial with the three actual cross-Gram coefficients. -/
theorem cross_mode_polynomial (a b c e : Triple → ℂ) (theta : ℂ)
    (htheta : theta ^ 3 = 1) :
    star (mode a theta) * mode b theta + star (mode c theta) * mode e theta =
      (star (a 0) * b 0 + star (a 1) * b 1 + star (a 2) * b 2) +
      (star (c 0) * e 0 + star (c 1) * e 1 + star (c 2) * e 2) +
      theta ^ 2 * ((star (a 0) * b 2 + star (a 1) * b 0 + star (a 2) * b 1) +
        (star (c 0) * e 2 + star (c 1) * e 0 + star (c 2) * e 1)) +
      theta * ((star (a 0) * b 1 + star (a 1) * b 2 + star (a 2) * b 0) +
        (star (c 0) * e 1 + star (c 1) * e 2 + star (c 2) * e 0)) := by
  have hs := star_cube_root theta htheta
  have hfour : theta ^ 4 = theta := by
    calc
      theta ^ 4 = theta ^ 3 * theta := by ring
      _ = theta := by rw [htheta]; ring
  have hs2 : star (theta ^ 2) = theta := by
    rw [star_pow, hs]
    calc
      (theta ^ 2) ^ 2 = theta ^ 4 := by ring
      _ = theta := hfour
  simp only [mode, star_add, star_mul, hs, hs2]
  ring_nf
  rw [htheta, hfour]
  ring

/-- Actual cross-block Gram entries force each two-by-two mode's orthogonality. -/
theorem cross_mode_zero_of_actual_gram (a b c e : Triple → ℂ)
    (hgram : (blockCirculant a b c e).conjTranspose * blockCirculant a b c e =
      (6 : ℂ) • (1 : Matrix Six Six ℂ))
    (theta : ℂ) (htheta : theta ^ 3 = 1) :
    star (mode a theta) * mode b theta + star (mode c theta) * mode e theta = 0 := by
  have h0 := congrArg (fun M : Matrix Six Six ℂ => M (Sum.inl 0) (Sum.inr 0)) hgram
  have h1 := congrArg (fun M : Matrix Six Six ℂ => M (Sum.inl 0) (Sum.inr 1)) hgram
  have h2 := congrArg (fun M : Matrix Six Six ℂ => M (Sum.inl 0) (Sum.inr 2)) hgram
  norm_num [Matrix.mul_apply, Matrix.conjTranspose_apply, Fintype.sum_sum_type,
    Fin.sum_univ_three, blockCirculant, Matrix.circulant, Matrix.smul_apply,
    Matrix.one_apply] at h0 h1 h2
  have hn1 : (-1 : Triple) = 2 := by decide
  have hn2 : (-2 : Triple) = 1 := by decide
  simp only [starRingEnd_apply, hn1, hn2] at h0 h1 h2
  have hp := cross_mode_polynomial a b c e theta htheta
  rw [h0, h1, h2] at hp
  simpa using hp

/-- Opposite actual block Fourier powers match, derived from just one Gram equation. -/
theorem opposite_mode_normSq_of_actual_gram (a b c e : Triple → ℂ)
    (hgram : (blockCirculant a b c e).conjTranspose * blockCirculant a b c e =
      (6 : ℂ) • (1 : Matrix Six Six ℂ))
    (theta : ℂ) (htheta : theta ^ 3 = 1) :
    Complex.normSq (mode a theta) = Complex.normSq (mode e theta) ∧
      Complex.normSq (mode b theta) = Complex.normSq (mode c theta) := by
  have hl := left_mode_energy_of_actual_gram a b c e hgram theta htheta
  have hr := right_mode_energy_of_actual_gram a b c e hgram theta htheta
  have hc := cross_mode_zero_of_actual_gram a b c e hgram theta htheta
  have hp : star (mode a theta) * mode b theta =
      -(star (mode c theta) * mode e theta) := eq_neg_of_add_eq_zero_left hc
  have hprod := congrArg Complex.normSq hp
  simp only [Complex.normSq_neg, Complex.normSq_mul, Complex.star_def,
    Complex.normSq_conj] at hprod
  have hz : Complex.normSq (mode c theta) = 6 - Complex.normSq (mode a theta) := by
    linarith
  have hw : Complex.normSq (mode e theta) = 6 - Complex.normSq (mode b theta) := by
    linarith
  rw [hz, hw] at hprod
  have hs : Complex.normSq (mode a theta) + Complex.normSq (mode b theta) = 6 := by
    nlinarith [hprod]
  constructor <;> linarith

#print axioms cross_mode_polynomial
#print axioms cross_mode_zero_of_actual_gram
#print axioms opposite_mode_normSq_of_actual_gram

end MUBTriplets.CubeRootGramMatching
