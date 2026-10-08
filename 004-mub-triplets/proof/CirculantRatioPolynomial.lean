import CirculantAutocorrelation
import Mathlib.Algebra.Polynomial.Roots

/-!
Actual cyclic ratios of a unit complex triple are
the roots, with their full multiplicities, of the cubic determined by its
cyclic autocorrelation. Equal autocorrelations therefore give equal actual
ratio multisets. The final theorem connects the actual flat six-by-six
four-circulant Gram hypothesis to opposite ratio multisets; its imported
autocorrelation theorem is proved in the preceding source.
No distinct-ratio premise or numerical phase enumeration is used.
This source does not reconstruct shifts/adjoints or prove product cancellation.
The polynomial/root ingredients are classical; historical originality is
not established.
-/

noncomputable section
open MUBTriplets.CirculantCharacter MUBTriplets.CirculantAutocorrelation

namespace MUBTriplets.CirculantRatioPolynomial

/-- Actual neighboring phase quotient, with cyclic Fin 3 indexing. -/
def ratio (v : Triple → ℂ) (i : Triple) : ℂ := v i / v (i + 1)

/-- Three occurrences are retained even when their ratio values coincide. -/
def ratioMultiset (v : Triple → ℂ) : Multiset ℂ :=
  ratio v 0 ::ₘ ratio v 1 ::ₘ ratio v 2 ::ₘ 0

@[simp] private theorem ratio_zero (v : Triple → ℂ) :
    ratio v 0 = v 0 / v 1 := by norm_num [ratio]

@[simp] private theorem ratio_one (v : Triple → ℂ) :
    ratio v 1 = v 1 / v 2 := by norm_num [ratio]

@[simp] private theorem ratio_two (v : Triple → ℂ) :
    ratio v 2 = v 2 / v 0 := by norm_num [ratio]

private theorem unit_ne_zero (x : ℂ) (hx : Complex.normSq x = 1) : x ≠ 0 := by
  intro h
  subst x
  norm_num at hx

private theorem unit_mul_star (x : ℂ) (hx : Complex.normSq x = 1) :
    x * star x = 1 := by
  simp only [Complex.star_def, Complex.mul_conj, hx, Complex.ofReal_one]

private theorem unit_inv_eq_star (x : ℂ) (hx : Complex.normSq x = 1) :
    x⁻¹ = star x := by
  have hx0 := unit_ne_zero x hx
  calc
    x⁻¹ = x⁻¹ * (x * star x) := by rw [unit_mul_star x hx]; simp
    _ = star x := by rw [← mul_assoc, inv_mul_cancel₀ hx0, one_mul]

private theorem ratio_normSq (v : Triple → ℂ)
    (hv : ∀ i, Complex.normSq (v i) = 1) (i : Triple) :
    Complex.normSq (ratio v i) = 1 := by
  rw [ratio, Complex.normSq_div, hv i, hv (i + 1)]
  norm_num

private theorem ratio_product (v : Triple → ℂ)
    (hv : ∀ i, Complex.normSq (v i) = 1) :
    ratio v 0 * ratio v 1 * ratio v 2 = 1 := by
  have h0 := unit_ne_zero (v 0) (hv 0)
  have h1 := unit_ne_zero (v 1) (hv 1)
  have h2 := unit_ne_zero (v 2) (hv 2)
  rw [ratio_zero, ratio_one, ratio_two]
  field_simp [h0, h1, h2]

private theorem ratio_sum_eq_corr (v : Triple → ℂ)
    (hv : ∀ i, Complex.normSq (v i) = 1) :
    ratio v 0 + ratio v 1 + ratio v 2 = corr v := by
  rw [ratio_zero, ratio_one, ratio_two]
  simp only [corr, div_eq_mul_inv, unit_inv_eq_star (v 0) (hv 0),
    unit_inv_eq_star (v 1) (hv 1), unit_inv_eq_star (v 2) (hv 2)]

private theorem pair_eq_star (x y z : ℂ) (hz : Complex.normSq z = 1)
    (hprod : x * y * z = 1) : x * y = star z := by
  calc
    x * y = (x * y) * (z * star z) := by rw [unit_mul_star z hz]; ring
    _ = (x * y * z) * star z := by ring
    _ = star z := by rw [hprod]; ring

private theorem pair_sum_eq_star_sum (x y z : ℂ)
    (hx : Complex.normSq x = 1) (hy : Complex.normSq y = 1)
    (hz : Complex.normSq z = 1) (hprod : x * y * z = 1) :
    x * y + y * z + z * x = star (x + y + z) := by
  have hxy := pair_eq_star x y z hz hprod
  have hyzx : y * z * x = 1 := by
    simpa only [mul_comm, mul_left_comm, mul_assoc] using hprod
  have hzxy : z * x * y = 1 := by
    simpa only [mul_comm, mul_left_comm, mul_assoc] using hprod
  have hyz := pair_eq_star y z x hx hyzx
  have hzx := pair_eq_star z x y hy hzxy
  rw [hxy, hyz, hzx]
  simp only [star_add]
  ring

private theorem cubic_product (x y z : ℂ) :
    (Polynomial.X - Polynomial.C x) * (Polynomial.X - Polynomial.C y) *
        (Polynomial.X - Polynomial.C z) =
      Polynomial.X ^ 3 - Polynomial.C (x + y + z) * Polynomial.X ^ 2 +
        Polynomial.C (x * y + y * z + z * x) * Polynomial.X -
        Polynomial.C (x * y * z) := by
  simp only [Polynomial.C_add, Polynomial.C_mul]
  ring

/-- The complete actual ratio polynomial, without a simple-root assumption. -/
theorem ratio_factorization (v : Triple → ℂ)
    (hv : ∀ i, Complex.normSq (v i) = 1) :
    ((ratioMultiset v).map (fun r => Polynomial.X - Polynomial.C r)).prod =
      Polynomial.X ^ 3 - Polynomial.C (corr v) * Polynomial.X ^ 2 +
        Polynomial.C (star (corr v)) * Polynomial.X - 1 := by
  have hprod := ratio_product v hv
  have hsum := ratio_sum_eq_corr v hv
  have hpair := pair_sum_eq_star_sum (ratio v 0) (ratio v 1) (ratio v 2)
    (ratio_normSq v hv 0) (ratio_normSq v hv 1) (ratio_normSq v hv 2) hprod
  simp only [ratioMultiset, Multiset.map_cons, Multiset.map_zero,
    Multiset.prod_cons, Multiset.prod_zero, mul_one]
  rw [← mul_assoc, cubic_product]
  simp only [hpair, hsum, hprod, Polynomial.C_1]

/-- Equal cyclic autocorrelation determines the whole ratio multiset, including repeats. -/
theorem ratio_multiset_eq_of_corr_eq (v w : Triple → ℂ)
    (hv : ∀ i, Complex.normSq (v i) = 1)
    (hw : ∀ i, Complex.normSq (w i) = 1) (hcorr : corr v = corr w) :
    ratioMultiset v = ratioMultiset w := by
  have hpoly :
      ((ratioMultiset v).map (fun r => Polynomial.X - Polynomial.C r)).prod =
      ((ratioMultiset w).map (fun r => Polynomial.X - Polynomial.C r)).prod := by
    rw [ratio_factorization v hv, ratio_factorization w hw, hcorr]
  have hroots := congrArg Polynomial.roots hpoly
  simpa only [Polynomial.roots_multiset_prod_X_sub_C] using hroots

/-- Actual flat entries and actual Gram yield both opposite ratio multisets. -/
theorem opposite_ratio_multisets_of_actual_flat_gram (a b c e : Triple → ℂ)
    (hflat : ∀ i j, Complex.normSq (blockCirculant a b c e i j) = 1)
    (hgram : (blockCirculant a b c e).conjTranspose * blockCirculant a b c e =
      (6 : ℂ) • (1 : Matrix Six Six ℂ)) :
    ratioMultiset a = ratioMultiset e ∧ ratioMultiset b = ratioMultiset c := by
  have ha (i : Triple) : Complex.normSq (a i) = 1 := by
    simpa [blockCirculant, Matrix.circulant] using hflat (Sum.inl i) (Sum.inl 0)
  have hb (i : Triple) : Complex.normSq (b i) = 1 := by
    simpa [blockCirculant, Matrix.circulant] using hflat (Sum.inl i) (Sum.inr 0)
  have hc (i : Triple) : Complex.normSq (c i) = 1 := by
    simpa [blockCirculant, Matrix.circulant] using hflat (Sum.inr i) (Sum.inl 0)
  have he (i : Triple) : Complex.normSq (e i) = 1 := by
    simpa [blockCirculant, Matrix.circulant] using hflat (Sum.inr i) (Sum.inr 0)
  obtain ⟨hae, hbc⟩ := opposite_corr_of_actual_gram a b c e hgram
  exact ⟨ratio_multiset_eq_of_corr_eq a e ha he hae,
    ratio_multiset_eq_of_corr_eq b c hb hc hbc⟩

#print axioms ratio_factorization
#print axioms ratio_multiset_eq_of_corr_eq
#print axioms opposite_ratio_multisets_of_actual_flat_gram

end MUBTriplets.CirculantRatioPolynomial
