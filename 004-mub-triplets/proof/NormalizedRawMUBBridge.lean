import CirculantCharacter
import Mathlib.Analysis.Real.Sqrt

/-!
Actual normalization of two raw complex six-by-six matrices.

U0 is the identity, U1 is H divided by sqrt(6), and U2 is R divided by
sqrt(6). The hypotheses are the actual raw entry norm squares, actual
column Gram equations, and actual entry norm squares of H*R. No
normalized certificate is assumed.

The result records the three complete column Grams and all three pairwise
transition entry norms. It does not construct Mathlib OrthonormalBasis
objects. An application to a specified triplet must supply actual proofs
of every raw hypothesis for those specified matrices.
-/

noncomputable section

open MUBTriplets.CirculantCharacter

namespace MUBTriplets.NormalizedRawMUBBridge

abbrev SixMatrix := Matrix Six Six ℂ

/-- The real positive raw-to-unitary scale, regarded as a complex scalar. -/
def normalizationFactor : ℂ := (Real.sqrt (6 : ℝ) : ℂ)⁻¹

/-- U0, the actual standard-coordinate basis matrix. -/
def standardBasisMatrix : SixMatrix := 1

/-- The actual matrix U1 or U2 obtained from a raw matrix. -/
def normalize (H : SixMatrix) : SixMatrix := normalizationFactor • H

private theorem normalizationFactor_normSq :
    Complex.normSq normalizationFactor = (1 / 6 : ℝ) := by
  unfold normalizationFactor
  rw [Complex.normSq_inv, Complex.normSq_ofReal,
    Real.mul_self_sqrt (by norm_num : (0 : ℝ) ≤ 6)]
  norm_num

private theorem normalizationFactor_star_mul :
    star normalizationFactor * normalizationFactor = (1 / 6 : ℂ) := by
  calc
    star normalizationFactor * normalizationFactor =
        (Complex.normSq normalizationFactor : ℂ) := by
      simpa only [Complex.star_def] using
        (Complex.normSq_eq_conj_mul_self (z := normalizationFactor)).symm
    _ = (1 / 6 : ℂ) := by
      rw [normalizationFactor_normSq]
      norm_num

private theorem normalized_cross_gram (H R : SixMatrix) :
    (normalize H).conjTranspose * normalize R =
      (1 / 6 : ℂ) • (H.conjTranspose * R) := by
  unfold normalize
  rw [Matrix.conjTranspose_smul, Matrix.smul_mul, Matrix.mul_smul,
    smul_smul, normalizationFactor_star_mul]

/-- An actual raw column Gram of 6I becomes the complete unit column Gram. -/
theorem normalize_column_gram
    (H : SixMatrix)
    (hgram : H.conjTranspose * H = (6 : ℂ) • (1 : SixMatrix)) :
    (normalize H).conjTranspose * normalize H = (1 : SixMatrix) := by
  rw [normalized_cross_gram, hgram, smul_smul]
  norm_num

private theorem normalized_flat_entries
    (H : SixMatrix)
    (hflat : ∀ i j, Complex.normSq (H i j) = 1) :
    ∀ i j, Complex.normSq (normalize H i j) = (1 / 6 : ℝ) := by
  intro i j
  change Complex.normSq (normalizationFactor * H i j) = (1 / 6 : ℝ)
  rw [Complex.normSq_mul, normalizationFactor_normSq, hflat i j, mul_one]

private theorem normalized_mutual_entries
    (H R : SixMatrix)
    (hoverlap : ∀ i j, Complex.normSq ((H.conjTranspose * R) i j) = 6) :
    ∀ i j,
      Complex.normSq (((normalize H).conjTranspose * normalize R) i j) =
        (1 / 6 : ℝ) := by
  intro i j
  rw [normalized_cross_gram]
  change Complex.normSq ((1 / 6 : ℂ) * (H.conjTranspose * R) i j) =
    (1 / 6 : ℝ)
  rw [Complex.normSq_mul, hoverlap i j]
  norm_num

/-- The actual three matrices are fixed by the parameters:
U0=I, U1=normalize H, U2=normalize R.
All six columns of each matrix have the complete identity Gram.
The three pairwise transitions have actual entry norm squares 1/6. -/
structure ActualNormalizedTriplet (H R : SixMatrix) : Prop where
  gram_standard :
    standardBasisMatrix.conjTranspose * standardBasisMatrix = (1 : SixMatrix)
  gram_first :
    (normalize H).conjTranspose * normalize H = (1 : SixMatrix)
  gram_second :
    (normalize R).conjTranspose * normalize R = (1 : SixMatrix)
  entries_first :
    ∀ i j, Complex.normSq (normalize H i j) = (1 / 6 : ℝ)
  entries_second :
    ∀ i j, Complex.normSq (normalize R i j) = (1 / 6 : ℝ)
  overlap_standard_first :
    ∀ i j,
      Complex.normSq ((standardBasisMatrix.conjTranspose * normalize H) i j) =
        (1 / 6 : ℝ)
  overlap_standard_second :
    ∀ i j,
      Complex.normSq ((standardBasisMatrix.conjTranspose * normalize R) i j) =
        (1 / 6 : ℝ)
  overlap_first_second :
    ∀ i j,
      Complex.normSq (((normalize H).conjTranspose * normalize R) i j) =
        (1 / 6 : ℝ)

/-- Complete actual normalization from raw matrix data, without supplied
normalized Gram or normalized overlap assertions. -/
theorem actual_normalized_triplet_of_raw
    (H R : SixMatrix)
    (hflatH : ∀ i j, Complex.normSq (H i j) = 1)
    (hflatR : ∀ i j, Complex.normSq (R i j) = 1)
    (hgramH : H.conjTranspose * H = (6 : ℂ) • (1 : SixMatrix))
    (hgramR : R.conjTranspose * R = (6 : ℂ) • (1 : SixMatrix))
    (hoverlap : ∀ i j, Complex.normSq ((H.conjTranspose * R) i j) = 6) :
    ActualNormalizedTriplet H R := by
  refine
    { gram_standard := by simp [standardBasisMatrix]
      gram_first := normalize_column_gram H hgramH
      gram_second := normalize_column_gram R hgramR
      entries_first := normalized_flat_entries H hflatH
      entries_second := normalized_flat_entries R hflatR
      overlap_standard_first := ?_
      overlap_standard_second := ?_
      overlap_first_second := normalized_mutual_entries H R hoverlap }
  · simpa [standardBasisMatrix] using normalized_flat_entries H hflatH
  · simpa [standardBasisMatrix] using normalized_flat_entries R hflatR

#print axioms normalize_column_gram
#print axioms actual_normalized_triplet_of_raw

end MUBTriplets.NormalizedRawMUBBridge

