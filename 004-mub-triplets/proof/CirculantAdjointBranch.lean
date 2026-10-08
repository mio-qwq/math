import CirculantPhaseRetrieval
import CirculantInvertibility

/-!
One actual adjoint retrieval alternative forces
the opposite block to be the adjoint with the same shift and opposite phase.
This closes all three adjoint-containing branches of product cancellation
from the actual column Gram equation. The preserving/preserving branch and
its real-rank argument are not proved here.
-/

noncomputable section
open scoped BigOperators
open MUBTriplets.CirculantCharacter MUBTriplets.CirculantPhaseRetrieval
open MUBTriplets.CirculantInvertibility

namespace MUBTriplets.CirculantAdjointBranch

private theorem unit_mul_star (z : ℂ) (hz : Complex.normSq z = 1) :
    z * star z = 1 := by
  simp only [Complex.star_def, Complex.mul_conj, hz, Complex.ofReal_one]

private theorem column_cross_of_actual_gram (a b c e : Triple → ℂ)
    (hgram : (blockCirculant a b c e).conjTranspose * blockCirculant a b c e =
      (6 : ℂ) • (1 : Matrix Six Six ℂ)) :
    (Matrix.circulant a).conjTranspose * Matrix.circulant b +
      (Matrix.circulant c).conjTranspose * Matrix.circulant e = 0 := by
  ext i j
  have h := congrArg (fun M : Matrix Six Six ℂ => M (Sum.inl i) (Sum.inr j)) hgram
  simpa [Matrix.mul_apply, Matrix.conjTranspose_apply, Fintype.sum_sum_type,
    blockCirculant, Matrix.smul_apply, Matrix.one_apply] using h

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

private theorem partner_of_column_cross (a b c e : Triple → ℂ)
    (alpha : ℂ) (l : Triple) (halpha : Complex.normSq alpha = 1)
    (N : Matrix Triple Triple ℂ) (hN : Matrix.circulant a * N = 1)
    (hcross : (Matrix.circulant a).conjTranspose * Matrix.circulant b +
      (Matrix.circulant c).conjTranspose * Matrix.circulant e = 0)
    (hE : Matrix.circulant e =
      alpha • (shiftMatrix l * (Matrix.circulant a).conjTranspose)) :
    Matrix.circulant c =
      (-alpha) • (shiftMatrix l * (Matrix.circulant b).conjTranspose) := by
  let A := Matrix.circulant a
  let B := Matrix.circulant b
  let C := Matrix.circulant c
  let E := Matrix.circulant e
  let P := shiftMatrix l
  change A * N = 1 at hN
  change A.conjTranspose * B + C.conjTranspose * E = 0 at hcross
  change E = alpha • (P * A.conjTranspose) at hE
  have hPA : P * A.conjTranspose = A.conjTranspose * P := by
    dsimp [A, P, shiftMatrix]
    simp only [Matrix.conjTranspose_circulant]
    exact Matrix.circulant_mul_comm _ _
  have hCA : C.conjTranspose * A.conjTranspose = A.conjTranspose * C.conjTranspose := by
    dsimp [A, C]
    simp only [Matrix.conjTranspose_circulant]
    exact Matrix.circulant_mul_comm _ _
  have hCP : C.conjTranspose * P = P * C.conjTranspose := by
    dsimp [C, P, shiftMatrix]
    simp only [Matrix.conjTranspose_circulant]
    exact Matrix.circulant_mul_comm _ _
  have hmove : C.conjTranspose * (P * A.conjTranspose) =
      A.conjTranspose * (P * C.conjTranspose) := by
    calc
      _ = C.conjTranspose * (A.conjTranspose * P) := by rw [hPA]
      _ = (C.conjTranspose * A.conjTranspose) * P := (Matrix.mul_assoc _ _ _).symm
      _ = (A.conjTranspose * C.conjTranspose) * P := by rw [hCA]
      _ = A.conjTranspose * (C.conjTranspose * P) := Matrix.mul_assoc _ _ _
      _ = _ := by rw [hCP]
  have hterm : C.conjTranspose * (alpha • (P * A.conjTranspose)) =
      A.conjTranspose * (alpha • (P * C.conjTranspose)) := by
    simp only [Matrix.mul_smul, hmove]
  have hfactor := hcross
  rw [hE, hterm, ← Matrix.mul_add] at hfactor
  have hleft : N.conjTranspose * A.conjTranspose = 1 := by
    simpa only [Matrix.conjTranspose_mul, Matrix.conjTranspose_one] using
      congrArg Matrix.conjTranspose hN
  have htail : B + alpha • (P * C.conjTranspose) = 0 := by
    calc
      _ = (N.conjTranspose * A.conjTranspose) *
          (B + alpha • (P * C.conjTranspose)) := by rw [hleft, one_mul]
      _ = N.conjTranspose * (A.conjTranspose *
          (B + alpha • (P * C.conjTranspose))) := Matrix.mul_assoc _ _ _
      _ = 0 := by rw [hfactor, mul_zero]
  change Matrix.circulant b +
    alpha • (shiftMatrix l * (Matrix.circulant c).conjTranspose) = 0 at htail
  rw [shiftMatrix_mul_adjoint] at htail
  have hpoint (i : Triple) : b i + alpha * star (c (l - i)) = 0 := by
    have hi := congrArg (fun M : Matrix Triple Triple ℂ => M i 0) htail
    simpa only [Matrix.add_apply, Matrix.smul_apply, Matrix.circulant_apply,
      shiftAdjVec, sub_zero, smul_eq_mul, Matrix.zero_apply] using hi
  have hc (i : Triple) : c i = (-alpha) * star (b (l - i)) := by
    have hi : b (l - i) + alpha * star (c i) = 0 := by
      simpa only [sub_sub_cancel] using hpoint (l - i)
    have hs : star (b (l - i)) + star alpha * c i = 0 := by
      simpa only [star_add, star_mul, star_star, star_zero, mul_comm] using congrArg star hi
    have hs' := eq_neg_of_add_eq_zero_right hs
    calc
      c i = (alpha * star alpha) * c i := by rw [unit_mul_star alpha halpha, one_mul]
      _ = alpha * (star alpha * c i) := by ring
      _ = alpha * (-star (b (l - i))) := by rw [hs']
      _ = (-alpha) * star (b (l - i)) := by ring
  rw [shiftMatrix_mul_adjoint]
  ext i j
  simpa only [Matrix.circulant_apply, Matrix.smul_apply, smul_eq_mul, shiftAdjVec]
    using hc (i - j)

private theorem phaseProduct_of_shift_adjoint (a e : Triple → ℂ)
    (alpha : ℂ) (l : Triple)
    (hE : Matrix.circulant e =
      alpha • (shiftMatrix l * (Matrix.circulant a).conjTranspose)) :
    phaseProduct e = alpha ^ 3 * star (phaseProduct a) := by
  have he (i : Triple) : e i = alpha * star (a (l - i)) := by
    have hi := congrArg (fun M : Matrix Triple Triple ℂ => M i 0) hE
    rw [shiftMatrix_mul_adjoint] at hi
    simpa only [Matrix.smul_apply, Matrix.circulant_apply, smul_eq_mul,
      shiftAdjVec, sub_zero] using hi
  have hb : Function.Bijective (fun i : Triple => l - i) := by
    constructor
    · intro i j h
      have h' := congrArg (fun k : Triple => l - k) h
      simpa only [sub_sub_cancel] using h'
    · intro i
      exact ⟨l - i, by simp only [sub_sub_cancel]⟩
  calc
    phaseProduct e = ∏ i : Triple, alpha * star (a (l - i)) := by
      unfold phaseProduct
      exact Finset.prod_congr rfl (fun i _ => he i)
    _ = (∏ _i : Triple, alpha) * (∏ i : Triple, star (a (l - i))) :=
      Finset.prod_mul_distrib
    _ = alpha ^ 3 * (∏ i : Triple, star (a i)) := by
      rw [Fin.prod_const, hb.prod_comp (fun i => star (a i))]
    _ = alpha ^ 3 * star (phaseProduct a) := by
      simp only [phaseProduct, Fin.prod_univ_three, star_mul]
      ring

private theorem unit_phaseProduct (a : Triple → ℂ)
    (ha : ∀ i, Complex.normSq (a i) = 1) :
    phaseProduct a * star (phaseProduct a) = 1 := by
  apply unit_mul_star
  simp only [phaseProduct, Fin.prod_univ_three, Complex.normSq_mul, ha, one_mul]

/-- A genuine adjoint alternative in either opposite pair already forces
the actual four phase products to cancel. This closes all three branches
containing an adjoint; no second Gram equation is supplied. -/
theorem product_cancel_of_actual_flat_gram_adjoint_alternative
    (a b c e : Triple → ℂ)
    (hflat : ∀ i j, Complex.normSq (blockCirculant a b c e i j) = 1)
    (hgram : (blockCirculant a b c e).conjTranspose * blockCirculant a b c e =
      (6 : ℂ) • (1 : Matrix Six Six ℂ))
    (hadjoint :
      (∃ alpha : ℂ, Complex.normSq alpha = 1 ∧ ∃ l : Triple,
        Matrix.circulant e = alpha •
          (shiftMatrix l * (Matrix.circulant a).conjTranspose)) ∨
      (∃ beta : ℂ, Complex.normSq beta = 1 ∧ ∃ j : Triple,
        Matrix.circulant c = beta •
          (shiftMatrix j * (Matrix.circulant b).conjTranspose))) :
    phaseProduct a * phaseProduct e + phaseProduct b * phaseProduct c = 0 := by
  obtain ⟨N, Q, _, _, hA, _, hB, _⟩ :=
    four_block_inverses_of_actual_flat_gram a b c e hflat hgram
  have hcross := column_cross_of_actual_gram a b c e hgram
  have ha (i : Triple) : Complex.normSq (a i) = 1 := by
    simpa [blockCirculant, Matrix.circulant] using hflat (Sum.inl i) (Sum.inl 0)
  have hb (i : Triple) : Complex.normSq (b i) = 1 := by
    simpa [blockCirculant, Matrix.circulant] using hflat (Sum.inl i) (Sum.inr 0)
  have hpa := unit_phaseProduct a ha
  have hpb := unit_phaseProduct b hb
  rcases hadjoint with ⟨alpha, halpha, l, hE⟩ | ⟨beta, hbeta, j, hC⟩
  · have hC := partner_of_column_cross a b c e alpha l halpha N hA hcross hE
    rw [phaseProduct_of_shift_adjoint a e alpha l hE,
      phaseProduct_of_shift_adjoint b c (-alpha) l hC]
    calc
      _ = alpha ^ 3 * (phaseProduct a * star (phaseProduct a)) -
          alpha ^ 3 * (phaseProduct b * star (phaseProduct b)) := by ring
      _ = 0 := by rw [hpa, hpb]; ring
  · have hcross' : (Matrix.circulant b).conjTranspose * Matrix.circulant a +
        (Matrix.circulant e).conjTranspose * Matrix.circulant c = 0 := by
      simpa only [Matrix.conjTranspose_add, Matrix.conjTranspose_mul,
        Matrix.conjTranspose_conjTranspose, Matrix.conjTranspose_zero] using
        congrArg Matrix.conjTranspose hcross
    have hE := partner_of_column_cross b a e c beta j hbeta Q hB hcross' hC
    rw [phaseProduct_of_shift_adjoint a e (-beta) j hE,
      phaseProduct_of_shift_adjoint b c beta j hC]
    calc
      _ = -beta ^ 3 * (phaseProduct a * star (phaseProduct a)) +
          beta ^ 3 * (phaseProduct b * star (phaseProduct b)) := by ring
      _ = 0 := by rw [hpa, hpb]; ring

#print axioms product_cancel_of_actual_flat_gram_adjoint_alternative

end MUBTriplets.CirculantAdjointBranch
