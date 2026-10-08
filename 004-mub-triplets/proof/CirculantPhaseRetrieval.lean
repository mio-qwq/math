import CirculantRatioPolynomial

/-!
Full length-three unit phase retrieval from actual cyclic ratio multisets,
including repeated ratios, and its actual four-circulant Gram application.
The final conclusion gives two pairs of genuine matrix shift/adjoint
alternatives. It does not prove the later product cancellation/rank argument
or the general MUB conjecture. The phase-retrieval ingredients are classical;
historical originality is not established.
-/

noncomputable section
open MUBTriplets.CirculantCharacter MUBTriplets.CirculantRatioPolynomial

namespace MUBTriplets.CirculantPhaseRetrieval

/-- Two equal occurrence multisets agree in one of the two possible orders. -/
theorem pair_occurrence_match {α : Type*} (x0 x1 y0 y1 : α)
    (h : x0 ::ₘ x1 ::ₘ (0 : Multiset α) = y0 ::ₘ y1 ::ₘ 0) :
    (x0 = y0 ∧ x1 = y1) ∨ (x0 = y1 ∧ x1 = y0) := by
  have hmem : x0 ∈ y0 ::ₘ y1 ::ₘ (0 : Multiset α) :=
    h ▸ Multiset.mem_cons_self x0 (x1 ::ₘ 0)
  have hhead : x0 = y0 ∨ x0 = y1 := by simpa using hmem
  rcases hhead with h0 | h1
  · have htail : x1 ::ₘ (0 : Multiset α) = y1 ::ₘ 0 :=
      (Multiset.cons_inj_right y0).mp (by simpa only [h0] using h)
    exact Or.inl ⟨h0, (Multiset.cons_inj_left (0 : Multiset α)).mp htail⟩
  · have hswap : x0 ::ₘ x1 ::ₘ (0 : Multiset α) = y1 ::ₘ y0 ::ₘ 0 :=
      h.trans (Multiset.cons_swap y0 y1 0)
    have htail : x1 ::ₘ (0 : Multiset α) = y0 ::ₘ 0 :=
      (Multiset.cons_inj_right y1).mp (by simpa only [h1] using hswap)
    exact Or.inr ⟨h1, (Multiset.cons_inj_left (0 : Multiset α)).mp htail⟩

/-- Equal three-occurrence multisets differ by a cyclic shift or reflection.
The argument does not assume that any two of the values are distinct. -/
theorem three_occurrence_dihedral {α : Type*} (x y : Triple → α)
    (h : x 0 ::ₘ x 1 ::ₘ x 2 ::ₘ (0 : Multiset α) =
      y 0 ::ₘ y 1 ::ₘ y 2 ::ₘ 0) :
    ∃ k : Triple, (∀ i, x i = y (k + i)) ∨ (∀ i, x i = y (k - i)) := by
  have hmem : x 0 ∈ y 0 ::ₘ y 1 ::ₘ y 2 ::ₘ (0 : Multiset α) :=
    h ▸ Multiset.mem_cons_self (x 0) (x 1 ::ₘ x 2 ::ₘ 0)
  have hhead : x 0 = y 0 ∨ x 0 = y 1 ∨ x 0 = y 2 := by
    simpa using hmem
  rcases hhead with h0 | h1 | h2
  · have htail : x 1 ::ₘ x 2 ::ₘ (0 : Multiset α) = y 1 ::ₘ y 2 ::ₘ 0 :=
      (Multiset.cons_inj_right (y 0)).mp (by simpa only [h0] using h)
    rcases pair_occurrence_match (x 1) (x 2) (y 1) (y 2) htail with
      ⟨h11, h22⟩ | ⟨h12, h21⟩
    · refine ⟨(0 : Triple), Or.inl ?_⟩
      intro i
      fin_cases i
      · change x 0 = y 0
        exact h0
      · change x 1 = y 1
        exact h11
      · change x 2 = y 2
        exact h22
    · refine ⟨(0 : Triple), Or.inr ?_⟩
      intro i
      fin_cases i
      · change x 0 = y 0
        exact h0
      · change x 1 = y 2
        exact h12
      · change x 2 = y 1
        exact h21
  · have hswap : x 0 ::ₘ x 1 ::ₘ x 2 ::ₘ (0 : Multiset α) =
        y 1 ::ₘ y 0 ::ₘ y 2 ::ₘ 0 :=
      h.trans (Multiset.cons_swap (y 0) (y 1) (y 2 ::ₘ 0))
    have htail : x 1 ::ₘ x 2 ::ₘ (0 : Multiset α) = y 0 ::ₘ y 2 ::ₘ 0 :=
      (Multiset.cons_inj_right (y 1)).mp (by simpa only [h1] using hswap)
    rcases pair_occurrence_match (x 1) (x 2) (y 0) (y 2) htail with
      ⟨h10, h22⟩ | ⟨h12, h20⟩
    · refine ⟨(1 : Triple), Or.inr ?_⟩
      intro i
      fin_cases i
      · change x 0 = y 1
        exact h1
      · change x 1 = y 0
        exact h10
      · change x 2 = y 2
        exact h22
    · refine ⟨(1 : Triple), Or.inl ?_⟩
      intro i
      fin_cases i
      · change x 0 = y 1
        exact h1
      · change x 1 = y 2
        exact h12
      · change x 2 = y 0
        exact h20
  · have hrotate : y 0 ::ₘ y 1 ::ₘ y 2 ::ₘ (0 : Multiset α) =
        y 2 ::ₘ y 0 ::ₘ y 1 ::ₘ 0 := by
      calc
        _ = y 0 ::ₘ y 2 ::ₘ y 1 ::ₘ 0 :=
          congrArg (fun s : Multiset α => y 0 ::ₘ s)
            (Multiset.cons_swap (y 1) (y 2) 0)
        _ = _ := Multiset.cons_swap (y 0) (y 2) (y 1 ::ₘ 0)
    have htail : x 1 ::ₘ x 2 ::ₘ (0 : Multiset α) = y 0 ::ₘ y 1 ::ₘ 0 :=
      (Multiset.cons_inj_right (y 2)).mp
        (by simpa only [h2] using h.trans hrotate)
    rcases pair_occurrence_match (x 1) (x 2) (y 0) (y 1) htail with
      ⟨h10, h21⟩ | ⟨h11, h20⟩
    · refine ⟨(2 : Triple), Or.inl ?_⟩
      intro i
      fin_cases i
      · change x 0 = y 2
        exact h2
      · change x 1 = y 0
        exact h10
      · change x 2 = y 1
        exact h21
    · refine ⟨(2 : Triple), Or.inr ?_⟩
      intro i
      fin_cases i
      · change x 0 = y 2
        exact h2
      · change x 1 = y 1
        exact h11
      · change x 2 = y 0
        exact h20



def shiftVec (l : Triple) (a : Triple → ℂ) : Triple → ℂ := fun i => a (i - l)

def shiftAdjVec (l : Triple) (a : Triple → ℂ) : Triple → ℂ := fun i => star (a (l - i))

/-- The actual cyclic row-shift permutation matrix, with P_l e_j=e_(j+l). -/
def shiftMatrix (l : Triple) : Matrix Triple Triple ℂ :=
  Matrix.circulant (fun i => if i = l then 1 else 0)

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

private theorem star_div_star_of_unit (x y : ℂ)
    (hx : Complex.normSq x = 1) (hy : Complex.normSq y = 1) :
    star x / star y = y / x := by
  rw [div_eq_mul_inv, ← unit_inv_eq_star x hx]
  have hy' : (star y)⁻¹ = y := by
    rw [← unit_inv_eq_star y hy, inv_inv]
  rw [hy', div_eq_mul_inv]
  ring

private theorem ratio_shiftVec (a : Triple → ℂ) (l i : Triple) :
    ratio (shiftVec l a) i = ratio a (i - l) := by
  unfold ratio shiftVec
  congr 2
  abel

private theorem ratio_shiftAdjVec (a : Triple → ℂ)
    (ha : ∀ i, Complex.normSq (a i) = 1) (l i : Triple) :
    ratio (shiftAdjVec l a) i = ratio a (l - i - 1) := by
  unfold ratio shiftAdjVec
  rw [star_div_star_of_unit _ _ (ha _) (ha _)]
  congr 2 <;> abel

private theorem common_phase_of_ratio_eq (x y : Triple → ℂ)
    (hx : ∀ i, Complex.normSq (x i) = 1)
    (hy : ∀ i, Complex.normSq (y i) = 1)
    (hr : ∀ i, ratio x i = ratio y i) :
    ∃ alpha : ℂ, Complex.normSq alpha = 1 ∧ ∀ i, x i = alpha * y i := by
  have hx1 := unit_ne_zero (x 1) (hx 1)
  have hx2 := unit_ne_zero (x 2) (hx 2)
  have hy0 := unit_ne_zero (y 0) (hy 0)
  have hy1 := unit_ne_zero (y 1) (hy 1)
  have hy2 := unit_ne_zero (y 2) (hy 2)
  have h0 := hr 0
  have h1 := hr 1
  norm_num [ratio] at h0 h1
  have hc0 := (div_eq_div_iff hx1 hy1).mp h0
  have hc1 := (div_eq_div_iff hx2 hy2).mp h1
  have hc2 : x 0 * y 2 = y 0 * x 2 := by
    have hzero : (x 0 * y 2 - y 0 * x 2) * y 1 = 0 := by
      linear_combination y 2 * hc0 + y 0 * hc1
    exact sub_eq_zero.mp ((mul_eq_zero.mp hzero).resolve_right hy1)
  refine ⟨x 0 / y 0, ?_, ?_⟩
  · rw [Complex.normSq_div, hx 0, hy 0]
    norm_num
  · intro i
    fin_cases i
    · simp [hy0]
    · change x 1 = (x 0 / y 0) * y 1
      field_simp [hy0]
      linear_combination -hc0
    · change x 2 = (x 0 / y 0) * y 2
      field_simp [hy0]
      linear_combination -hc2

/-- All length-three unit retrieval alternatives, with repetitions allowed. -/
theorem phase_retrieval_of_ratio_multiset (a e : Triple → ℂ)
    (ha : ∀ i, Complex.normSq (a i) = 1)
    (he : ∀ i, Complex.normSq (e i) = 1)
    (hm : ratioMultiset a = ratioMultiset e) :
    ∃ alpha : ℂ, Complex.normSq alpha = 1 ∧ ∃ l : Triple,
      (∀ i, e i = alpha * a (i - l)) ∨
      (∀ i, e i = alpha * star (a (l - i))) := by
  obtain ⟨h, hp | hr⟩ := three_occurrence_dihedral (ratio e) (ratio a)
    (show ratio e 0 ::ₘ ratio e 1 ::ₘ ratio e 2 ::ₘ (0 : Multiset ℂ) =
      ratio a 0 ::ₘ ratio a 1 ::ₘ ratio a 2 ::ₘ 0 from hm.symm)
  · have hu (i : Triple) : Complex.normSq (shiftVec (-h) a i) = 1 := ha _
    have hs (i : Triple) : ratio e i = ratio (shiftVec (-h) a) i := by
      rw [ratio_shiftVec]
      convert hp i using 2
      abel
    obtain ⟨alpha, halpha, hphase⟩ := common_phase_of_ratio_eq e (shiftVec (-h) a) he hu hs
    exact ⟨alpha, halpha, -h, Or.inl hphase⟩
  · have hu (i : Triple) : Complex.normSq (shiftAdjVec (h + 1) a i) = 1 := by
      simpa only [shiftAdjVec, Complex.star_def, Complex.normSq_conj] using ha (h + 1 - i)
    have hs (i : Triple) : ratio e i = ratio (shiftAdjVec (h + 1) a) i := by
      rw [ratio_shiftAdjVec a ha]
      convert hr i using 2
      abel
    obtain ⟨alpha, halpha, hphase⟩ := common_phase_of_ratio_eq e (shiftAdjVec (h + 1) a) he hu hs
    exact ⟨alpha, halpha, h + 1, Or.inr hphase⟩

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

private theorem shiftMatrix_mul_adjoint (a : Triple → ℂ) (l : Triple) :
    shiftMatrix l * (Matrix.circulant a).conjTranspose =
      Matrix.circulant (shiftAdjVec l a) := by
  rw [Matrix.conjTranspose_circulant, shiftMatrix_mul]
  congr 1
  ext i
  simp only [shiftVec, shiftAdjVec, Pi.star_apply]
  congr 2
  abel

/-- Actual matrix shift/adjoint alternatives, including repeated-ratio cases. -/
theorem circulant_phase_retrieval_of_ratio_multiset (a e : Triple → ℂ)
    (ha : ∀ i, Complex.normSq (a i) = 1)
    (he : ∀ i, Complex.normSq (e i) = 1)
    (hm : ratioMultiset a = ratioMultiset e) :
    ∃ alpha : ℂ, Complex.normSq alpha = 1 ∧ ∃ l : Triple,
      Matrix.circulant e = alpha • (shiftMatrix l * Matrix.circulant a) ∨
      Matrix.circulant e = alpha • (shiftMatrix l * (Matrix.circulant a).conjTranspose) := by
  obtain ⟨alpha, halpha, l, hp | hr⟩ := phase_retrieval_of_ratio_multiset a e ha he hm
  · refine ⟨alpha, halpha, l, Or.inl ?_⟩
    rw [shiftMatrix_mul]
    ext i j
    simpa only [Matrix.circulant_apply, Matrix.smul_apply, smul_eq_mul, shiftVec] using hp (i - j)
  · refine ⟨alpha, halpha, l, Or.inr ?_⟩
    rw [shiftMatrix_mul_adjoint]
    ext i j
    simpa only [Matrix.circulant_apply, Matrix.smul_apply, smul_eq_mul, shiftAdjVec] using hr (i - j)

/-- Both actual matrix retrieval alternatives follow from actual flat Gram. -/
theorem opposite_circulant_alternatives_of_actual_flat_gram
    (a b c e : Triple → ℂ)
    (hflat : ∀ i j, Complex.normSq (blockCirculant a b c e i j) = 1)
    (hgram : (blockCirculant a b c e).conjTranspose * blockCirculant a b c e =
      (6 : ℂ) • (1 : Matrix Six Six ℂ)) :
    (∃ alpha : ℂ, Complex.normSq alpha = 1 ∧ ∃ l : Triple,
      Matrix.circulant e = alpha • (shiftMatrix l * Matrix.circulant a) ∨
      Matrix.circulant e = alpha • (shiftMatrix l * (Matrix.circulant a).conjTranspose)) ∧
    (∃ beta : ℂ, Complex.normSq beta = 1 ∧ ∃ j : Triple,
      Matrix.circulant c = beta • (shiftMatrix j * Matrix.circulant b) ∨
      Matrix.circulant c = beta • (shiftMatrix j * (Matrix.circulant b).conjTranspose)) := by
  have ha (i : Triple) : Complex.normSq (a i) = 1 := by
    simpa [blockCirculant, Matrix.circulant] using hflat (Sum.inl i) (Sum.inl 0)
  have hb (i : Triple) : Complex.normSq (b i) = 1 := by
    simpa [blockCirculant, Matrix.circulant] using hflat (Sum.inl i) (Sum.inr 0)
  have hc (i : Triple) : Complex.normSq (c i) = 1 := by
    simpa [blockCirculant, Matrix.circulant] using hflat (Sum.inr i) (Sum.inl 0)
  have he (i : Triple) : Complex.normSq (e i) = 1 := by
    simpa [blockCirculant, Matrix.circulant] using hflat (Sum.inr i) (Sum.inr 0)
  obtain ⟨hae, hbc⟩ := opposite_ratio_multisets_of_actual_flat_gram a b c e hflat hgram
  exact ⟨circulant_phase_retrieval_of_ratio_multiset a e ha he hae,
    circulant_phase_retrieval_of_ratio_multiset b c hb hc hbc⟩

#print axioms phase_retrieval_of_ratio_multiset
#print axioms circulant_phase_retrieval_of_ratio_multiset
#print axioms opposite_circulant_alternatives_of_actual_flat_gram

end MUBTriplets.CirculantPhaseRetrieval
