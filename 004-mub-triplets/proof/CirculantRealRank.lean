import CirculantSpectralProducts
import Mathlib.Tactic.LinearCombination

/-!
The algebraic real-rank core for two nonzero three-point spectra.

The first theorem takes explicit spectral identities. The final theorem
derives the neighbour sums and cubic products from actual flat triples;
nonzero modes and symmetric cross equations remain explicit hypotheses.
The proof uses the star determinant instead of real-coordinate coercions.
It does not yet derive these hypotheses from a four-block preserving case.
-/

noncomputable section

namespace MUBTriplets.CirculantRealRank

private theorem fixed_ratio_of_cross (m n : ℂ) (hm : m ≠ 0)
    (hcross : star m * n = star n * m) :
    star (n / m) = n / m := by
  have hsm : star m ≠ 0 := by simpa using hm
  rw [star_div₀]
  apply (div_eq_div_iff hsm hm).mpr
  simpa only [mul_comm] using hcross.symm

private theorem unit_square_of_common_real_ray (p d c : ℂ) (hc : c ≠ 0)
    (hp : p * star p = 1) (hd : d * star d = 1)
    (hpc : star (p / c) = p / c) (hdc : star (d / c) = d / c) :
    p ^ 2 = d ^ 2 := by
  have hsc : star c ≠ 0 := by simpa using hc
  rw [star_div₀] at hpc hdc
  have hpc' := (div_eq_div_iff hsc hc).mp hpc
  have hdc' := (div_eq_div_iff hsc hc).mp hdc
  have hzero : c * (star p * d - star d * p) = 0 := by
    linear_combination d * hpc' - p * hdc'
  have hcross : star p * d = star d * p :=
    sub_eq_zero.mp ((mul_eq_zero.mp hzero).resolve_left hc)
  linear_combination d ^ 2 * hp - p ^ 2 * hd - (p * d) * hcross

/-- Two unit products have equal squares under the exact three-spectrum
neighbour, cubic-product and real-ratio equations. Every denominator used
internally is proved nonzero from these explicit nonzero mode hypotheses. -/
theorem product_squares_of_real_spectral_ratios
    (m0 m1 m2 n0 n1 n2 pa pd : ℂ)
    (hm0 : m0 ≠ 0) (hm1 : m1 ≠ 0) (hm2 : m2 ≠ 0)
    (hn0 : n0 ≠ 0) (hn1 : n1 ≠ 0) (hn2 : n2 ≠ 0)
    (hc0 : star m0 * n0 = star n0 * m0)
    (hc1 : star m1 * n1 = star n1 * m1)
    (hc2 : star m2 * n2 = star n2 * m2)
    (hma : m0 * star m1 + m1 * star m2 + m2 * star m0 = 0)
    (hnd : n0 * star n1 + n1 * star n2 + n2 * star n0 = 0)
    (hpa : 27 * pa = m0 ^ 3 + m1 ^ 3 + m2 ^ 3 - 3 * m0 * m1 * m2)
    (hpd : 27 * pd = n0 ^ 3 + n1 ^ 3 + n2 ^ 3 - 3 * n0 * n1 * n2)
    (hua : pa * star pa = 1) (hud : pd * star pd = 1) :
    pa ^ 2 = pd ^ 2 := by
  let q0 : ℂ := n0 / m0
  let q1 : ℂ := n1 / m1
  let q2 : ℂ := n2 / m2
  have hq0 : star q0 = q0 := fixed_ratio_of_cross m0 n0 hm0 hc0
  have hq1 : star q1 = q1 := fixed_ratio_of_cross m1 n1 hm1 hc1
  have hq2 : star q2 = q2 := fixed_ratio_of_cross m2 n2 hm2 hc2
  have hqNonzero : q0 ≠ 0 ∧ q1 ≠ 0 ∧ q2 ≠ 0 :=
    ⟨div_ne_zero hn0 hm0, div_ne_zero hn1 hm1, div_ne_zero hn2 hm2⟩
  have hq00 : q0 ≠ 0 := hqNonzero.1
  have hq20 : q2 ≠ 0 := hqNonzero.2.2
  have hn0q : n0 = q0 * m0 := (div_mul_cancel₀ n0 hm0).symm
  have hn1q : n1 = q1 * m1 := (div_mul_cancel₀ n1 hm1).symm
  have hn2q : n2 = q2 * m2 := (div_mul_cancel₀ n2 hm2).symm
  let w0 : ℂ := m0 * star m1
  let w1 : ℂ := m1 * star m2
  let w2 : ℂ := m2 * star m0
  have hsm0 : star m0 ≠ 0 := by simpa using hm0
  have hsm1 : star m1 ≠ 0 := by simpa using hm1
  have hw00 : w0 ≠ 0 := mul_ne_zero hm0 hsm1
  have hw20 : w2 ≠ 0 := mul_ne_zero hm2 hsm0
  have hw : w0 + w1 + w2 = 0 := hma
  have hweighted : q0 * q1 * w0 + q1 * q2 * w1 + q2 * q0 * w2 = 0 := by
    rw [hn0q, hn1q, hn2q] at hnd
    simp only [star_mul', hq0, hq1, hq2] at hnd
    simp only [w0, w1, w2]
    linear_combination hnd
  let K : ℂ := w0 * star w1 - star w0 * w1
  by_cases hK : K = 0
  · -- Collinear neighbour products: both cubic products lie on one real ray.
    have hsw0 : star w0 ≠ 0 := by simpa using hw00
    have hu0 : star (w1 / w0) = w1 / w0 := by
      rw [star_div₀]
      apply (div_eq_div_iff hsw0 hw00).mpr
      change w0 * star w1 - star w0 * w1 = 0 at hK
      linear_combination hK
    have hw2ratio : w2 / w0 = -1 - w1 / w0 := by
      field_simp [hw00]
      linear_combination hw
    have ht0 : star (w2 / w0) = w2 / w0 := by
      rw [hw2ratio]
      simp only [star_sub, star_neg, star_one, hu0]
    let r : ℂ := m1 / m0
    let s : ℂ := m2 / m0
    let t : ℂ := s / star r
    let u : ℂ := r * star s / star r
    have hr0 : r ≠ 0 := div_ne_zero hm1 hm0
    have hsr0 : star r ≠ 0 := by simpa using hr0
    have htratio : t = w2 / w0 := by
      simp only [t, r, s, w2, w0, star_div₀]
      field_simp [hm0, hsm0, hsm1]
    have huratio : u = w1 / w0 := by
      simp only [u, r, s, w1, w0, star_div₀]
      field_simp [hm0, hsm0, hsm1]
    have ht : star t = t := by rw [htratio]; exact ht0
    have hu : star u = u := by rw [huratio]; exact hu0
    have htne : t ≠ 0 := by rw [htratio]; exact div_ne_zero hw20 hw00
    have hs : s = t * star r := (div_mul_cancel₀ s hsr0).symm
    have hss : star s = t * r := by
      rw [hs, star_mul', ht, star_star]
    have hnu : (r * star r) * u = t * r ^ 3 := by
      change (r * star r) * (r * star s / star r) = t * r ^ 3
      rw [hss]
      field_simp [hsr0]
    have hnuStar := congrArg star hnu
    simp only [star_mul', star_star, hu, ht, star_pow] at hnuStar
    have hr3zero : t * (star (r ^ 3) - r ^ 3) = 0 := by
      simp only [star_pow]
      linear_combination hnu - hnuStar
    have hr3 : star (r ^ 3) = r ^ 3 :=
      sub_eq_zero.mp ((mul_eq_zero.mp hr3zero).resolve_left htne)
    have hr3' : star r ^ 3 = r ^ 3 := by simpa only [star_pow] using hr3
    have hs3 : star (s ^ 3) = s ^ 3 := by
      rw [hs, star_pow, star_mul', ht, star_star]
      calc
        (t * r) ^ 3 = t ^ 3 * r ^ 3 := by ring
        _ = t ^ 3 * star r ^ 3 := by rw [hr3']
        _ = (t * star r) ^ 3 := by ring
    have hrs : star (r * s) = r * s := by
      rw [hs, star_mul', star_mul', ht, star_star]
      ring
    have hm1r : m1 = r * m0 := (div_mul_cancel₀ m1 hm0).symm
    have hm2s : m2 = s * m0 := (div_mul_cancel₀ m2 hm0).symm
    have hpaRatio : pa / m0 ^ 3 = (1 + r ^ 3 + s ^ 3 - 3 * (r * s)) / 27 := by
      rw [hm1r, hm2s] at hpa
      field_simp [hm0]
      linear_combination hpa
    have hpdRatio : pd / m0 ^ 3 =
        (q0 ^ 3 + q1 ^ 3 * r ^ 3 + q2 ^ 3 * s ^ 3 -
          3 * (q0 * q1 * q2) * (r * s)) / 27 := by
      rw [hn0q, hn1q, hn2q, hm1r, hm2s] at hpd
      field_simp [hm0]
      linear_combination hpd
    have hnuma : star (1 + r ^ 3 + s ^ 3 - 3 * (r * s)) =
        1 + r ^ 3 + s ^ 3 - 3 * (r * s) := by
      simp only [star_sub, star_add, star_one]
      rw [hr3, hs3, star_mul', star_ofNat, hrs]
    have hnumd : star (q0 ^ 3 + q1 ^ 3 * r ^ 3 + q2 ^ 3 * s ^ 3 -
        3 * (q0 * q1 * q2) * (r * s)) =
        q0 ^ 3 + q1 ^ 3 * r ^ 3 + q2 ^ 3 * s ^ 3 -
          3 * (q0 * q1 * q2) * (r * s) := by
      simp only [star_sub, star_add]
      rw [star_pow, hq0, star_mul', star_pow, hq1, hr3,
        star_mul', star_pow, hq2, hs3, star_mul', hrs]
      simp only [star_mul', star_ofNat, hq0, hq1, hq2]
    have hpFixed : star (pa / m0 ^ 3) = pa / m0 ^ 3 := by
      calc
        star (pa / m0 ^ 3) = star ((1 + r ^ 3 + s ^ 3 - 3 * (r * s)) / 27) :=
          congrArg star hpaRatio
        _ = (1 + r ^ 3 + s ^ 3 - 3 * (r * s)) / 27 := by
          rw [star_div₀, hnuma, star_ofNat]
        _ = pa / m0 ^ 3 := hpaRatio.symm
    have hdFixed : star (pd / m0 ^ 3) = pd / m0 ^ 3 := by
      calc
        star (pd / m0 ^ 3) = star ((q0 ^ 3 + q1 ^ 3 * r ^ 3 + q2 ^ 3 * s ^ 3 -
            3 * (q0 * q1 * q2) * (r * s)) / 27) := congrArg star hpdRatio
        _ = (q0 ^ 3 + q1 ^ 3 * r ^ 3 + q2 ^ 3 * s ^ 3 -
            3 * (q0 * q1 * q2) * (r * s)) / 27 := by
          rw [star_div₀, hnumd, star_ofNat]
        _ = pd / m0 ^ 3 := hpdRatio.symm
    exact unit_square_of_common_real_ray pa pd (m0 ^ 3)
      (pow_ne_zero 3 hm0) hua hud hpFixed hdFixed
  · -- Two independent neighbour products force all three real ratios equal.
    let x : ℂ := q0 * q1 - q2 * q0
    let y : ℂ := q1 * q2 - q2 * q0
    have hx : star x = x := by simp only [x, star_sub, star_mul', hq0, hq1, hq2]
    have hy : star y = y := by simp only [y, star_sub, star_mul', hq0, hq1, hq2]
    have hlin : x * w0 + y * w1 = 0 := by
      dsimp [x, y]
      linear_combination hweighted - (q2 * q0) * hw
    have hlinStar := congrArg star hlin
    simp only [star_add, star_mul', hx, hy, star_zero] at hlinStar
    have hxK : x * K = 0 := by
      change x * (w0 * star w1 - star w0 * w1) = 0
      linear_combination (star w1) * hlin - w1 * hlinStar
    have hyK : y * K = 0 := by
      change y * (w0 * star w1 - star w0 * w1) = 0
      linear_combination w0 * hlinStar - (star w0) * hlin
    have hx0 : x = 0 := (mul_eq_zero.mp hxK).resolve_right hK
    have hy0 : y = 0 := (mul_eq_zero.mp hyK).resolve_right hK
    have h12zero : q0 * (q1 - q2) = 0 := by
      dsimp [x] at hx0
      linear_combination hx0
    have h10zero : q2 * (q1 - q0) = 0 := by
      dsimp [y] at hy0
      linear_combination hy0
    have h12 : q1 = q2 :=
      sub_eq_zero.mp ((mul_eq_zero.mp h12zero).resolve_left hq00)
    have h10 : q1 = q0 :=
      sub_eq_zero.mp ((mul_eq_zero.mp h10zero).resolve_left hq20)
    have h20 : q2 = q0 := h12.symm.trans h10
    have hscale : pd = q0 ^ 3 * pa := by
      rw [hn0q, hn1q, hn2q, h10, h20] at hpd
      linear_combination (1 / 27 : ℂ) * (hpd - q0 ^ 3 * hpa)
    have hpstar : star pd = q0 ^ 3 * star pa := by
      rw [hscale, star_mul', star_pow, hq0]
    have hdu : (q0 ^ 3 * pa) * (q0 ^ 3 * star pa) = 1 := by
      rw [← hscale, ← hpstar]
      exact hud
    have hq6 : q0 ^ 6 = 1 := by
      calc
        q0 ^ 6 = q0 ^ 6 * (pa * star pa) := by rw [hua, mul_one]
        _ = (q0 ^ 3 * pa) * (q0 ^ 3 * star pa) := by ring
        _ = 1 := hdu
    rw [hscale]
    calc
      pa ^ 2 = q0 ^ 6 * pa ^ 2 := by rw [hq6, one_mul]
      _ = (q0 ^ 3 * pa) ^ 2 := by ring

#print axioms product_squares_of_real_spectral_ratios

open MUBTriplets.CirculantCharacter MUBTriplets.CubeRootGramModes
open MUBTriplets.CirculantSpectralProducts

/-- Actual flat triples with nonzero, pairwise real-ratio Fourier modes
have equal squared first-column products. Spectral product and neighbour
identities are derived from the actual entries, not assumed as certificates. -/
theorem phaseProduct_squares_of_actual_flat_real_modes
    (a d : Triple → ℂ) (omega : ℂ)
    (hcube : omega ^ 3 = 1) (hone : omega ≠ 1)
    (ha : ∀ i, Complex.normSq (a i) = 1)
    (hd : ∀ i, Complex.normSq (d i) = 1)
    (hn : ∀ theta : ℂ, theta ^ 3 = 1 → mode a theta ≠ 0 ∧ mode d theta ≠ 0)
    (hcross : ∀ theta : ℂ, theta ^ 3 = 1 →
      star (mode a theta) * mode d theta = star (mode d theta) * mode a theta) :
    phaseProduct a ^ 2 = phaseProduct d ^ 2 := by
  have h1 : (1 : ℂ) ^ 3 = 1 := by norm_num
  have hc2 : (omega ^ 2) ^ 3 = 1 := by
    calc
      _ = (omega ^ 3) ^ 2 := by ring
      _ = 1 := by rw [hcube]; norm_num
  have hpunit (v : Triple → ℂ) (hv : ∀ i, Complex.normSq (v i) = 1) :
      phaseProduct v * star (phaseProduct v) = 1 := by
    have hu : Complex.normSq (phaseProduct v) = 1 := by
      simp only [phaseProduct, Fin.prod_univ_three, Complex.normSq_mul, hv, one_mul]
    simp only [Complex.star_def, Complex.mul_conj, hu, Complex.ofReal_one]
  exact product_squares_of_real_spectral_ratios
    (mode a 1) (mode a omega) (mode a (omega ^ 2))
    (mode d 1) (mode d omega) (mode d (omega ^ 2)) (phaseProduct a) (phaseProduct d)
    (hn 1 h1).1 (hn omega hcube).1 (hn (omega ^ 2) hc2).1
    (hn 1 h1).2 (hn omega hcube).2 (hn (omega ^ 2) hc2).2
    (hcross 1 h1) (hcross omega hcube) (hcross (omega ^ 2) hc2)
    (flat_three_mode_neighbor_sum a omega hcube hone ha)
    (flat_three_mode_neighbor_sum d omega hcube hone hd)
    (phaseProduct_from_three_modes a omega hcube hone)
    (phaseProduct_from_three_modes d omega hcube hone)
    (hpunit a ha) (hpunit d hd)

#print axioms phaseProduct_squares_of_actual_flat_real_modes

end MUBTriplets.CirculantRealRank
