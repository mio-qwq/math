import CirculantPreservingBranch
import CirculantAdjointBranch

/-!
Product cancellation and the first/cubic balanced characters from the
actual flat six-by-six column Gram equation. The actual phase-retrieval
alternatives are conclusions of that equation, rather than additional
hypotheses. Both preserving and adjoint branches are included.
The result is for these displayed four-circulant blocks and fixed balanced
partitions; general MUB and arbitrary companion symmetry are not asserted.
-/

noncomputable section
open MUBTriplets.CirculantCharacter MUBTriplets.CirculantPhaseRetrieval
open MUBTriplets.CirculantPreservingBranch MUBTriplets.CirculantAdjointBranch

namespace MUBTriplets.CirculantCancellation

/-- The four actual first-column products cancel under just actual flatness
and the original column Gram equation. Repeated retrieval ratios are allowed. -/
theorem product_cancel_of_actual_flat_gram
    (a b c e : Triple → ℂ)
    (hflat : ∀ i j, Complex.normSq (blockCirculant a b c e i j) = 1)
    (hgram : (blockCirculant a b c e).conjTranspose * blockCirculant a b c e =
      (6 : ℂ) • (1 : Matrix Six Six ℂ)) :
    phaseProduct a * phaseProduct e + phaseProduct b * phaseProduct c = 0 := by
  obtain ⟨hae, hbc⟩ := opposite_circulant_alternatives_of_actual_flat_gram
    a b c e hflat hgram
  obtain ⟨alpha, halpha, l, hE | hE⟩ := hae
  · obtain ⟨beta, hbeta, j, hC | hC⟩ := hbc
    · exact product_cancel_of_actual_flat_gram_preserving_alternatives
        a b c e hflat hgram alpha beta l j halpha hbeta hE hC
    · exact product_cancel_of_actual_flat_gram_adjoint_alternative
        a b c e hflat hgram (Or.inr ⟨beta, hbeta, j, hC⟩)
  · exact product_cancel_of_actual_flat_gram_adjoint_alternative
      a b c e hflat hgram (Or.inl ⟨alpha, halpha, l, hE⟩)

private theorem unit_ne_zero (z : ℂ) (hz : Complex.normSq z = 1) : z ≠ 0 := by
  intro h
  subst z
  norm_num at hz

/-- The first and cubic actual balanced characters vanish for both the
matrix and its adjoint under the same flat column Gram hypotheses. -/
theorem first_and_cubic_characters_zero_of_actual_flat_gram
    (a b c e : Triple → ℂ)
    (hflat : ∀ i j, Complex.normSq (blockCirculant a b c e i j) = 1)
    (hgram : (blockCirculant a b c e).conjTranspose * blockCirculant a b c e =
      (6 : ℂ) • (1 : Matrix Six Six ℂ)) :
    balancedCharacter (blockCirculant a b c e) 1 = 0 ∧
      balancedCharacter (blockCirculant a b c e) 3 = 0 ∧
      balancedCharacter (blockCirculant a b c e).conjTranspose 1 = 0 ∧
      balancedCharacter (blockCirculant a b c e).conjTranspose 3 = 0 := by
  have hb (i : Triple) : b i ≠ 0 := by
    apply unit_ne_zero
    simpa [blockCirculant, Matrix.circulant] using hflat (Sum.inl i) (Sum.inr 0)
  have hc (i : Triple) : c i ≠ 0 := by
    apply unit_ne_zero
    simpa [blockCirculant, Matrix.circulant] using hflat (Sum.inr i) (Sum.inl 0)
  have he (i : Triple) : e i ≠ 0 := by
    apply unit_ne_zero
    simpa [blockCirculant, Matrix.circulant] using hflat (Sum.inr i) (Sum.inr 0)
  have hpb := phaseProduct_ne_zero b hb
  have hpc := phaseProduct_ne_zero c hc
  have hpe := phaseProduct_ne_zero e he
  have hcancel := product_cancel_of_actual_flat_gram a b c e hflat hgram
  have hfirst := (first_character_zero_iff a b c e hpc hpe).mpr hcancel
  obtain ⟨hcubic, hadjointCubic⟩ :=
    both_cubic_characters_zero_of_product_cancel a b c e hb hc he hcancel
  have hsb : star (phaseProduct b) ≠ 0 := by simpa using hpb
  have hse : star (phaseProduct e) ≠ 0 := by simpa using hpe
  have hstar := congrArg star hcancel
  simp only [star_add, star_mul, star_zero] at hstar
  have hsum : star (phaseProduct a) / star (phaseProduct b) +
      star (phaseProduct c) / star (phaseProduct e) = 0 := by
    field_simp [hsb, hse]
    simpa only [mul_comm, mul_left_comm, mul_assoc, zero_mul] using hstar
  have hadjointFirst : balancedCharacter (blockCirculant a b c e).conjTranspose 1 = 0 := by
    rw [adjoint_balanced_character_formula]
    simp only [pow_one, hsum, mul_zero]
  exact ⟨hfirst, hcubic, hadjointFirst, hadjointCubic⟩

#print axioms product_cancel_of_actual_flat_gram
#print axioms first_and_cubic_characters_zero_of_actual_flat_gram

end MUBTriplets.CirculantCancellation
