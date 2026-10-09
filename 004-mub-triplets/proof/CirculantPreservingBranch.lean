import CirculantRealRank
import CirculantPhaseRetrieval
import CubeRootGramMatching
import Mathlib.Analysis.Complex.Polynomial.Basic
import Mathlib.Tactic.Linarith

/-!
The remaining preserving/preserving retrieval branch for actual flat Gram.
An actual cyclic shift and an arbitrary unit square root normalize the two
triples to symmetric real-ratio mode equations. The actual flat real-rank
theorem then gives the four first-column product cancellation.
This is a branch theorem; the two genuine preserving alternatives are
explicit hypotheses in addition to the actual flat Gram equation.
-/

noncomputable section
open scoped BigOperators
open MUBTriplets.CirculantCharacter MUBTriplets.CirculantPhaseRetrieval
open MUBTriplets.CubeRootGramModes MUBTriplets.CubeRootGramMatching
open MUBTriplets.CirculantRealRank

namespace MUBTriplets.CirculantPreservingBranch

private theorem unit_ne_zero (z : ℂ) (hz : Complex.normSq z = 1) : z ≠ 0 := by
  intro h
  subst z
  norm_num at hz

private theorem unit_mul_star (z : ℂ) (hz : Complex.normSq z = 1) :
    z * star z = 1 := by
  simp only [Complex.star_def, Complex.mul_conj, hz, Complex.ofReal_one]

private theorem star_cube_root (theta : ℂ) (hcube : theta ^ 3 = 1) :
    star theta = theta ^ 2 := by
  have hu : theta * star theta = 1 := by
    simp only [Complex.star_def, Complex.mul_conj,
      UnitTripleZeroSum.normSq_of_cube_root theta hcube, Complex.ofReal_one]
  calc
    star theta = theta ^ 3 * star theta := by rw [hcube]; ring
    _ = theta ^ 2 * (theta * star theta) := by ring
    _ = theta ^ 2 := by rw [hu]; ring

private theorem shiftMatrix_mul (a : Triple → ℂ) (l : Triple) :
    shiftMatrix l * Matrix.circulant a = Matrix.circulant (shiftVec l a) := by
  ext i j
  have hiff (k : Triple) : i - k = l ↔ k = i - l := by
    constructor
    · intro h
      rw [← h]
      abel
    · intro h
      rw [h]
      abel
  simp only [shiftMatrix, Matrix.mul_apply, Matrix.circulant_apply,
    ite_mul, one_mul, zero_mul, shiftVec]
  simp_rw [hiff]
  simp only [Finset.sum_ite_eq', Finset.mem_univ, ite_true]
  congr 1
  abel

private theorem point_of_preserving (a e : Triple → ℂ) (alpha : ℂ) (l : Triple)
    (hE : Matrix.circulant e = alpha • (shiftMatrix l * Matrix.circulant a)) :
    ∀ i, e i = alpha * shiftVec l a i := by
  intro i
  have hi := congrArg (fun M : Matrix Triple Triple ℂ => M i 0) hE
  rw [shiftMatrix_mul] at hi
  simpa only [Matrix.smul_apply, Matrix.circulant_apply, smul_eq_mul, sub_zero] using hi

private theorem mode_scalar (a : Triple → ℂ) (z theta : ℂ) :
    mode (fun i => z * a i) theta = z * mode a theta := by
  simp only [mode]
  ring

private theorem mode_shift (a : Triple → ℂ) (l : Triple) (theta : ℂ)
    (hcube : theta ^ 3 = 1) :
    mode (shiftVec l a) theta = theta ^ l.val * mode a theta := by
  have h4 : theta ^ 4 = theta := by
    calc
      theta ^ 4 = theta ^ 3 * theta := by ring
      _ = theta := by rw [hcube]; ring
  fin_cases l
  · simp [mode, shiftVec]
  · norm_num [mode, shiftVec]
    rw [show (-1 : Triple) = 2 from rfl]
    ring_nf
    rw [hcube]
    ring
  · norm_num [mode, shiftVec]
    rw [show (-2 : Triple) = 1 from rfl]
    ring_nf
    rw [hcube, h4]
    ring

private theorem mode_of_preserving (a e : Triple → ℂ) (alpha : ℂ) (l : Triple)
    (hE : Matrix.circulant e = alpha • (shiftMatrix l * Matrix.circulant a))
    (theta : ℂ) (hcube : theta ^ 3 = 1) :
    mode e theta = alpha * theta ^ l.val * mode a theta := by
  have he := point_of_preserving a e alpha l hE
  calc
    mode e theta = mode (fun i => alpha * shiftVec l a i) theta :=
      congrArg (fun v => mode v theta) (funext he)
    _ = alpha * mode (shiftVec l a) theta := mode_scalar _ _ _
    _ = alpha * theta ^ l.val * mode a theta := by rw [mode_shift a l theta hcube]; ring

private theorem phaseProduct_shift (a : Triple → ℂ) (l : Triple) :
    phaseProduct (shiftVec l a) = phaseProduct a := by
  simpa only [phaseProduct, shiftVec, Matrix.circulant_apply] using
    circulant_column_product a l

private theorem phaseProduct_scalar (a : Triple → ℂ) (z : ℂ) :
    phaseProduct (fun i => z * a i) = z ^ 3 * phaseProduct a := by
  simp only [phaseProduct, Fin.prod_univ_three]
  ring

private theorem phaseProduct_of_preserving (a e : Triple → ℂ) (alpha : ℂ) (l : Triple)
    (hE : Matrix.circulant e = alpha • (shiftMatrix l * Matrix.circulant a)) :
    phaseProduct e = alpha ^ 3 * phaseProduct a := by
  have he := point_of_preserving a e alpha l hE
  calc
    phaseProduct e = phaseProduct (fun i => alpha * shiftVec l a i) :=
      congrArg phaseProduct (funext he)
    _ = alpha ^ 3 * phaseProduct (shiftVec l a) := phaseProduct_scalar _ _
    _ = alpha ^ 3 * phaseProduct a := by rw [phaseProduct_shift]

private theorem square_of_difference_power (j l : Triple) (theta : ℂ)
    (hcube : theta ^ 3 = 1) :
    (theta ^ (j - l).val) ^ 2 = star (theta ^ j.val) * theta ^ l.val := by
  have hs := star_cube_root theta hcube
  have h4 : theta ^ 4 = theta := by
    calc
      theta ^ 4 = theta ^ 3 * theta := by ring
      _ = theta := by rw [hcube]; ring
  have h5 : theta ^ 5 = theta ^ 2 := by
    calc
      theta ^ 5 = theta ^ 3 * theta ^ 2 := by ring
      _ = theta ^ 2 := by rw [hcube]; ring
  have h6 : theta ^ 6 = 1 := by
    calc
      theta ^ 6 = (theta ^ 3) ^ 2 := by ring
      _ = 1 := by rw [hcube]; norm_num
  rw [star_pow, hs]
  fin_cases j <;> fin_cases l <;> norm_num [Fin.sub_def] <;> ring_nf
  · exact h4
  · rfl
  · exact hcube.symm
  · exact h5.symm
  · exact h6.symm

private theorem unit_square_root (alpha beta : ℂ)
    (halpha : Complex.normSq alpha = 1) (hbeta : Complex.normSq beta = 1) :
    ∃ v : ℂ, Complex.normSq v = 1 ∧ v ^ 2 = -beta / alpha ∧
      v * star beta * alpha = -star v := by
  have ha0 := unit_ne_zero alpha halpha
  obtain ⟨v, hv2⟩ := IsAlgClosed.exists_pow_nat_eq (-beta / alpha) (by decide : 0 < 2)
  have hvnorm := congrArg Complex.normSq hv2
  rw [pow_two, Complex.normSq_mul, Complex.normSq_div, Complex.normSq_neg,
    hbeta, halpha] at hvnorm
  norm_num at hvnorm
  have hv : Complex.normSq v = 1 := by nlinarith [Complex.normSq_nonneg v]
  have hbu := unit_mul_star beta hbeta
  have hvu := unit_mul_star v hv
  have hv2alpha : v ^ 2 * alpha = -beta := (eq_div_iff ha0).mp hv2
  have hvprod : v ^ 2 * star beta * alpha = -1 := by
    linear_combination (star beta) * hv2alpha - hbu
  have hz : v * star beta * alpha + star v = 0 := by
    linear_combination (star v) * hvprod - (v * star beta * alpha) * hvu
  exact ⟨v, hv, hv2, eq_neg_of_add_eq_zero_left hz⟩

/-- The actual preserving/preserving retrieval branch also forces the
four phase products to cancel. The normalization and real-mode equations
are constructed internally from the sole actual column Gram equation. -/
theorem product_cancel_of_actual_flat_gram_preserving_alternatives
    (a b c e : Triple → ℂ)
    (hflat : ∀ i j, Complex.normSq (blockCirculant a b c e i j) = 1)
    (hgram : (blockCirculant a b c e).conjTranspose * blockCirculant a b c e =
      (6 : ℂ) • (1 : Matrix Six Six ℂ))
    (alpha beta : ℂ) (l j : Triple)
    (halpha : Complex.normSq alpha = 1) (hbeta : Complex.normSq beta = 1)
    (hE : Matrix.circulant e = alpha • (shiftMatrix l * Matrix.circulant a))
    (hC : Matrix.circulant c = beta • (shiftMatrix j * Matrix.circulant b)) :
    phaseProduct a * phaseProduct e + phaseProduct b * phaseProduct c = 0 := by
  have ha (i : Triple) : Complex.normSq (a i) = 1 := by
    simpa [blockCirculant, Matrix.circulant] using hflat (Sum.inl i) (Sum.inl 0)
  have hb (i : Triple) : Complex.normSq (b i) = 1 := by
    simpa [blockCirculant, Matrix.circulant] using hflat (Sum.inl i) (Sum.inr 0)
  obtain ⟨v, hv, hv2, hvphase⟩ := unit_square_root alpha beta halpha hbeta
  have hv0 := unit_ne_zero v hv
  let ashift : Triple → ℂ := shiftVec (j - l) a
  let d : Triple → ℂ := fun i => v * b i
  have hflatA (i : Triple) : Complex.normSq (ashift i) = 1 := ha _
  have hflatD (i : Triple) : Complex.normSq (d i) = 1 := by
    change Complex.normSq (v * b i) = 1
    rw [Complex.normSq_mul, hv, hb i, one_mul]
  have hn (theta : ℂ) (hcube : theta ^ 3 = 1) :
      mode ashift theta ≠ 0 ∧ mode d theta ≠ 0 := by
    have htheta0 : theta ≠ 0 := by
      intro hz
      rw [hz] at hcube
      norm_num at hcube
    have hold := four_nonzero_modes_of_actual_flat_gram a b c e hflat hgram theta hcube
    change mode (shiftVec (j - l) a) theta ≠ 0 ∧ mode (fun i => v * b i) theta ≠ 0
    rw [mode_shift a (j - l) theta hcube, mode_scalar b v theta]
    exact ⟨mul_ne_zero (pow_ne_zero _ htheta0) hold.1, mul_ne_zero hv0 hold.2.1⟩
  have hreal (theta : ℂ) (hcube : theta ^ 3 = 1) :
      star (mode ashift theta) * mode d theta =
        star (mode d theta) * mode ashift theta := by
    let s : ℂ := theta ^ (j - l).val
    let k : ℂ := theta ^ j.val
    let h : ℂ := theta ^ l.val
    have hsquare : s ^ 2 = star k * h := square_of_difference_power j l theta hcube
    have hthetaUnit : theta * star theta = 1 :=
      unit_mul_star theta (UnitTripleZeroSum.normSq_of_cube_root theta hcube)
    have hsunit : s * star s = 1 := by
      change theta ^ (j - l).val * star (theta ^ (j - l).val) = 1
      rw [star_pow, ← mul_pow, hthetaUnit]
      simp
    have hcoeff : v * star beta * alpha * star k * h * star s = -star v * s := by
      calc
        _ = (v * star beta * alpha) * (star k * h) * star s := by ring
        _ = (-star v) * s ^ 2 * star s := by rw [hvphase, ← hsquare]
        _ = (-star v * s) * (s * star s) := by ring
        _ = -star v * s := by rw [hsunit, mul_one]
    have hc := cross_mode_zero_of_actual_gram a b c e hgram theta hcube
    rw [mode_of_preserving a e alpha l hE theta hcube,
      mode_of_preserving b c beta j hC theta hcube] at hc
    change star (mode a theta) * mode b theta +
      star (beta * k * mode b theta) * (alpha * h * mode a theta) = 0 at hc
    simp only [star_mul'] at hc
    change star (mode (shiftVec (j - l) a) theta) * mode (fun i => v * b i) theta =
      star (mode (fun i => v * b i) theta) * mode (shiftVec (j - l) a) theta
    rw [mode_shift a (j - l) theta hcube, mode_scalar b v theta]
    change star (s * mode a theta) * (v * mode b theta) =
      star (v * mode b theta) * (s * mode a theta)
    simp only [star_mul']
    apply sub_eq_zero.mp
    linear_combination (v * star s) * hc - (star (mode b theta) * mode a theta) * hcoeff
  let omega : ℂ := Complex.exp (2 * (Real.pi : ℂ) * Complex.I / 3)
  have hw : IsPrimitiveRoot omega 3 := Complex.isPrimitiveRoot_exp 3 (by decide)
  have hsquares := phaseProduct_squares_of_actual_flat_real_modes ashift d omega
    hw.pow_eq_one (hw.ne_one (by decide)) hflatA hflatD hn hreal
  change phaseProduct (shiftVec (j - l) a) ^ 2 =
    phaseProduct (fun i => v * b i) ^ 2 at hsquares
  rw [phaseProduct_shift, phaseProduct_scalar] at hsquares
  have ha0 := unit_ne_zero alpha halpha
  have hvpoly : alpha * v ^ 2 = -beta := by
    have h := (eq_div_iff ha0).mp hv2
    simpa only [mul_comm] using h
  have hvpow := congrArg (fun z : ℂ => z ^ 3) hvpoly
  have hv6 : alpha ^ 3 * v ^ 6 + beta ^ 3 = 0 := by
    linear_combination hvpow
  rw [phaseProduct_of_preserving a e alpha l hE,
    phaseProduct_of_preserving b c beta j hC]
  linear_combination alpha ^ 3 * hsquares + phaseProduct b ^ 2 * hv6

#print axioms product_cancel_of_actual_flat_gram_preserving_alternatives

end MUBTriplets.CirculantPreservingBranch
