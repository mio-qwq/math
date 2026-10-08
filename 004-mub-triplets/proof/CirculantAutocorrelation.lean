import CubeRootGramMatching
import Mathlib.RingTheory.RootsOfUnity.Complex

/-!
Three actual Fourier powers recover cyclic autocorrelation, including for
non-flat triples. The final theorem derives opposite block correlations
from a single actual six-by-six column Gram equation with no extra premises.
Ratio multiset/phase retrieval and product cancellation remain separate.
-/

noncomputable section
open MUBTriplets.CirculantCharacter MUBTriplets.CubeRootGramModes

namespace MUBTriplets.CirculantAutocorrelation

def corr (v : Triple → ℂ) : ℂ :=
  v 0 * star (v 1) + v 1 * star (v 2) + v 2 * star (v 0)

def energy (v : Triple → ℂ) : ℝ :=
  Complex.normSq (v 0) + Complex.normSq (v 1) + Complex.normSq (v 2)

private theorem star_cube_root (theta : ℂ) (htheta : theta ^ 3 = 1) :
    star theta = theta ^ 2 := by
  have hu : theta * star theta = 1 := by
    simp only [Complex.star_def, Complex.mul_conj,
      UnitTripleZeroSum.normSq_of_cube_root theta htheta, Complex.ofReal_one]
  calc
    star theta = theta ^ 3 * star theta := by rw [htheta]; ring
    _ = theta ^ 2 * (theta * star theta) := by ring
    _ = theta ^ 2 := by rw [hu]; ring

/-- Actual raw Fourier power as the cyclic correlation polynomial. -/
theorem mode_normSq_autocorrelation (v : Triple → ℂ) (theta : ℂ)
    (htheta : theta ^ 3 = 1) :
    (Complex.normSq (mode v theta) : ℂ) =
      (energy v : ℂ) + theta * star (corr v) + theta ^ 2 * corr v := by
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
  simp only [energy, Complex.ofReal_add, hcast, mode, corr, star_add, star_mul,
    star_star, hs, hs2]
  ring_nf
  rw [htheta, hfour]
  ring

/-- Three raw mode powers recover the actual cyclic correlation. -/
theorem corr_from_three_mode_powers (v : Triple → ℂ) (omega : ℂ)
    (hcube : omega ^ 3 = 1) (hone : omega ≠ 1) :
    3 * corr v = (Complex.normSq (mode v 1) : ℂ) +
      omega * (Complex.normSq (mode v omega) : ℂ) +
      omega ^ 2 * (Complex.normSq (mode v (omega ^ 2)) : ℂ) := by
  have hq : omega ^ 2 + omega + 1 = 0 := by
    have h : (omega - 1) * (omega ^ 2 + omega + 1) = 0 := by
      linear_combination hcube
    exact (mul_eq_zero.mp h).resolve_left (sub_ne_zero.mpr hone)
  have hs : omega ^ 2 = -omega - 1 := by linear_combination hq
  have h4 : omega ^ 4 = omega := by
    calc
      omega ^ 4 = omega ^ 3 * omega := by ring
      _ = omega := by rw [hcube]; ring
  have h6 : omega ^ 6 = 1 := by
    calc
      omega ^ 6 = (omega ^ 3) ^ 2 := by ring
      _ = 1 := by rw [hcube]; norm_num
  have hc2 : (omega ^ 2) ^ 3 = 1 := by
    calc
      (omega ^ 2) ^ 3 = (omega ^ 3) ^ 2 := by ring
      _ = 1 := by rw [hcube]; norm_num
  rw [mode_normSq_autocorrelation v 1 (by norm_num),
    mode_normSq_autocorrelation v omega hcube,
    mode_normSq_autocorrelation v (omega ^ 2) hc2]
  norm_num
  ring_nf
  simp only [hcube, h4, h6, hs]
  ring

/-- Actual opposite block correlations agree from just the original column Gram. -/
theorem opposite_corr_of_actual_gram (a b c e : Triple → ℂ)
    (hgram : (blockCirculant a b c e).conjTranspose * blockCirculant a b c e =
      (6 : ℂ) • (1 : Matrix Six Six ℂ)) :
    corr a = corr e ∧ corr b = corr c := by
  let omega : ℂ := Complex.exp (2 * (Real.pi : ℂ) * Complex.I / 3)
  have hw : IsPrimitiveRoot omega 3 := Complex.isPrimitiveRoot_exp 3 (by decide)
  have hc : omega ^ 3 = 1 := hw.pow_eq_one
  have hn : omega ≠ 1 := hw.ne_one (by decide)
  have hc2 : (omega ^ 2) ^ 3 = 1 := by
    calc
      (omega ^ 2) ^ 3 = (omega ^ 3) ^ 2 := by ring
      _ = 1 := by rw [hc]; norm_num
  have h0 := CubeRootGramMatching.opposite_mode_normSq_of_actual_gram
    a b c e hgram 1 (by norm_num)
  have h1 := CubeRootGramMatching.opposite_mode_normSq_of_actual_gram
    a b c e hgram omega hc
  have h2 := CubeRootGramMatching.opposite_mode_normSq_of_actual_gram
    a b c e hgram (omega ^ 2) hc2
  have hca := corr_from_three_mode_powers a omega hc hn
  have hcb := corr_from_three_mode_powers b omega hc hn
  have hcc := corr_from_three_mode_powers c omega hc hn
  have hce := corr_from_three_mode_powers e omega hc hn
  rw [h0.1, h1.1, h2.1] at hca
  rw [h0.2, h1.2, h2.2] at hcb
  constructor
  · linear_combination (1 / 3 : ℂ) * (hca - hce)
  · linear_combination (1 / 3 : ℂ) * (hcb - hcc)

#print axioms mode_normSq_autocorrelation
#print axioms corr_from_three_mode_powers
#print axioms opposite_corr_of_actual_gram

end MUBTriplets.CirculantAutocorrelation
