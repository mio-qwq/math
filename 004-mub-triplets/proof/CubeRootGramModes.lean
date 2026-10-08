import CirculantCharacter
import UnitTripleZeroSum

/-!
Actual four-circulant six-by-six Gram equations imply cube-root Fourier mode
bounds. Combining these derived bounds with unit entries excludes all four
blocks' zero modes. No Fourier bound, nonzero mode or block inverse is supplied
as a hypothesis. This does not yet construct block inverses or prove the full
phase-retrieval/product-cancellation theorem or general MUB coupling.
-/

noncomputable section
open scoped BigOperators
open MUBTriplets.CirculantCharacter

namespace MUBTriplets.CubeRootGramModes

private theorem triple_neg_one : (-1 : Triple) = 2 := by decide
private theorem triple_neg_two : (-2 : Triple) = 1 := by decide

/-- The actual raw three-point circulant Fourier amplitude. -/
def mode (a : Triple → ℂ) (theta : ℂ) : ℂ :=
  a 0 + a 1 * theta + a 2 * theta ^ 2

private theorem star_cube_root (theta : ℂ) (htheta : theta ^ 3 = 1) :
    star theta = theta ^ 2 := by
  have hu : theta * star theta = 1 := by
    simp only [Complex.star_def, Complex.mul_conj,
      UnitTripleZeroSum.normSq_of_cube_root theta htheta, Complex.ofReal_one]
  calc
    star theta = theta ^ 3 * star theta := by rw [htheta]; ring
    _ = theta ^ 2 * (theta * star theta) := by ring
    _ = theta ^ 2 := by rw [hu]; ring

/-- The exact polynomial identity matching three actual Gram entries. -/
theorem mode_norm_polynomial (a c : Triple → ℂ) (theta : ℂ)
    (htheta : theta ^ 3 = 1) :
    ((Complex.normSq (mode a theta) + Complex.normSq (mode c theta) : ℝ) : ℂ) =
      (star (a 0) * a 0 + star (a 1) * a 1 + star (a 2) * a 2) +
      (star (c 0) * c 0 + star (c 1) * c 1 + star (c 2) * c 2) +
      theta ^ 2 * ((star (a 0) * a 2 + star (a 1) * a 0 + star (a 2) * a 1) +
        (star (c 0) * c 2 + star (c 1) * c 0 + star (c 2) * c 1)) +
      theta * ((star (a 0) * a 1 + star (a 1) * a 2 + star (a 2) * a 0) +
        (star (c 0) * c 1 + star (c 1) * c 2 + star (c 2) * c 0)) := by
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
  have hcast (z : ℂ) : (Complex.normSq z : ℂ) = star z * z := by
    simpa only [Complex.star_def] using (Complex.normSq_eq_conj_mul_self (z := z))
  rw [Complex.ofReal_add, hcast, hcast]
  simp only [mode, star_add, star_mul, hs, hs2]
  ring_nf
  rw [htheta, hfour]
  ring

/-- Extract the left pair's exact mode energy from the actual six-by-six Gram. -/
theorem left_mode_energy_of_actual_gram (a b c e : Triple → ℂ)
    (hgram : (blockCirculant a b c e).conjTranspose * blockCirculant a b c e =
      (6 : ℂ) • (1 : Matrix Six Six ℂ))
    (theta : ℂ) (htheta : theta ^ 3 = 1) :
    Complex.normSq (mode a theta) + Complex.normSq (mode c theta) = 6 := by
  have h0 := congrArg (fun M : Matrix Six Six ℂ => M (Sum.inl 0) (Sum.inl 0)) hgram
  have h1 := congrArg (fun M : Matrix Six Six ℂ => M (Sum.inl 0) (Sum.inl 1)) hgram
  have h2 := congrArg (fun M : Matrix Six Six ℂ => M (Sum.inl 0) (Sum.inl 2)) hgram
  norm_num [Matrix.mul_apply, Matrix.conjTranspose_apply, Fintype.sum_sum_type,
    Fin.sum_univ_three, blockCirculant, Matrix.circulant, Matrix.smul_apply,
    Matrix.one_apply] at h0 h1 h2
  simp only [starRingEnd_apply, triple_neg_one, triple_neg_two] at h0 h1 h2
  have hp := mode_norm_polynomial a c theta htheta
  rw [h0, h1, h2] at hp
  norm_num at hp
  simpa using congrArg Complex.re hp

/-- The right actual columns likewise give the second pair's exact mode energy. -/
theorem right_mode_energy_of_actual_gram (a b c e : Triple → ℂ)
    (hgram : (blockCirculant a b c e).conjTranspose * blockCirculant a b c e =
      (6 : ℂ) • (1 : Matrix Six Six ℂ))
    (theta : ℂ) (htheta : theta ^ 3 = 1) :
    Complex.normSq (mode b theta) + Complex.normSq (mode e theta) = 6 := by
  have h0 := congrArg (fun M : Matrix Six Six ℂ => M (Sum.inr 0) (Sum.inr 0)) hgram
  have h1 := congrArg (fun M : Matrix Six Six ℂ => M (Sum.inr 0) (Sum.inr 1)) hgram
  have h2 := congrArg (fun M : Matrix Six Six ℂ => M (Sum.inr 0) (Sum.inr 2)) hgram
  norm_num [Matrix.mul_apply, Matrix.conjTranspose_apply, Fintype.sum_sum_type,
    Fin.sum_univ_three, blockCirculant, Matrix.circulant, Matrix.smul_apply,
    Matrix.one_apply] at h0 h1 h2
  simp only [starRingEnd_apply, triple_neg_one, triple_neg_two] at h0 h1 h2
  have hp := mode_norm_polynomial b e theta htheta
  rw [h0, h1, h2] at hp
  norm_num at hp
  simpa using congrArg Complex.re hp

/-- All four mode bounds are conclusions from actual Gram, not extra premises. -/
theorem four_mode_bounds_of_actual_gram (a b c e : Triple → ℂ)
    (hgram : (blockCirculant a b c e).conjTranspose * blockCirculant a b c e =
      (6 : ℂ) • (1 : Matrix Six Six ℂ))
    (theta : ℂ) (htheta : theta ^ 3 = 1) :
    Complex.normSq (mode a theta) ≤ 6 ∧ Complex.normSq (mode b theta) ≤ 6 ∧
      Complex.normSq (mode c theta) ≤ 6 ∧ Complex.normSq (mode e theta) ≤ 6 := by
  have hl := left_mode_energy_of_actual_gram a b c e hgram theta htheta
  have hr := right_mode_energy_of_actual_gram a b c e hgram theta htheta
  refine ⟨?_, ?_, ?_, ?_⟩
  · linarith [Complex.normSq_nonneg (mode c theta)]
  · linarith [Complex.normSq_nonneg (mode e theta)]
  · linarith [Complex.normSq_nonneg (mode a theta)]
  · linarith [Complex.normSq_nonneg (mode b theta)]

/-- Actual flatness and actual Gram exclude every zero cube-root mode. -/
theorem four_nonzero_modes_of_actual_flat_gram (a b c e : Triple → ℂ)
    (hflat : ∀ i j, Complex.normSq (blockCirculant a b c e i j) = 1)
    (hgram : (blockCirculant a b c e).conjTranspose * blockCirculant a b c e =
      (6 : ℂ) • (1 : Matrix Six Six ℂ))
    (theta : ℂ) (htheta : theta ^ 3 = 1) :
    mode a theta ≠ 0 ∧ mode b theta ≠ 0 ∧
      mode c theta ≠ 0 ∧ mode e theta ≠ 0 := by
  have ha (i : Triple) : Complex.normSq (a i) = 1 := by
    simpa [blockCirculant, Matrix.circulant] using hflat (Sum.inl i) (Sum.inl 0)
  have hb (i : Triple) : Complex.normSq (b i) = 1 := by
    simpa [blockCirculant, Matrix.circulant] using hflat (Sum.inl i) (Sum.inr 0)
  have hc (i : Triple) : Complex.normSq (c i) = 1 := by
    simpa [blockCirculant, Matrix.circulant] using hflat (Sum.inr i) (Sum.inl 0)
  have he (i : Triple) : Complex.normSq (e i) = 1 := by
    simpa [blockCirculant, Matrix.circulant] using hflat (Sum.inr i) (Sum.inr 0)
  refine ⟨?_, ?_, ?_, ?_⟩
  · exact UnitTripleZeroSum.root_mode_nonzero_of_all_root_bounds
      (a 0) (a 1) (a 2) theta (ha 0) (ha 1) (ha 2) htheta
      (fun eta heta => (four_mode_bounds_of_actual_gram a b c e hgram eta heta).1)
  · exact UnitTripleZeroSum.root_mode_nonzero_of_all_root_bounds
      (b 0) (b 1) (b 2) theta (hb 0) (hb 1) (hb 2) htheta
      (fun eta heta => (four_mode_bounds_of_actual_gram a b c e hgram eta heta).2.1)
  · exact UnitTripleZeroSum.root_mode_nonzero_of_all_root_bounds
      (c 0) (c 1) (c 2) theta (hc 0) (hc 1) (hc 2) htheta
      (fun eta heta => (four_mode_bounds_of_actual_gram a b c e hgram eta heta).2.2.1)
  · exact UnitTripleZeroSum.root_mode_nonzero_of_all_root_bounds
      (e 0) (e 1) (e 2) theta (he 0) (he 1) (he 2) htheta
      (fun eta heta => (four_mode_bounds_of_actual_gram a b c e hgram eta heta).2.2.2)

#print axioms mode_norm_polynomial
#print axioms left_mode_energy_of_actual_gram
#print axioms right_mode_energy_of_actual_gram
#print axioms four_mode_bounds_of_actual_gram
#print axioms four_nonzero_modes_of_actual_flat_gram

end MUBTriplets.CubeRootGramModes
