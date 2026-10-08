import CubeRootGramModes
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.RingTheory.RootsOfUnity.Complex

/-!
Actual invertibility of the four three-by-three circulant blocks of a flat
complex Hadamard6. The source factors the actual matrix determinant into
the three raw Fourier modes, chooses an actual complex primitive cube root,
uses bounds/nonzero modes derived from the actual six-by-six Gram equation,
and constructs four inverses with both matrix multiplication equations.
It does not formalize phase retrieval, product cancellation or general MUB
companion selection. The determinant/Fourier ingredients are classical.
-/

noncomputable section
open MUBTriplets.CirculantCharacter MUBTriplets.CubeRootGramModes

namespace MUBTriplets.CirculantInvertibility

/-- Actual determinant factorization at any primitive third root. -/
theorem circulant_det_factorization (a : Triple → ℂ) (omega : ℂ)
    (hcube : omega ^ 3 = 1) (hone : omega ≠ 1) :
    (Matrix.circulant a).det = mode a 1 * mode a omega * mode a (omega ^ 2) := by
  have hq : omega ^ 2 + omega + 1 = 0 := by
    have h : (omega - 1) * (omega ^ 2 + omega + 1) = 0 := by
      linear_combination hcube
    exact (mul_eq_zero.mp h).resolve_left (sub_ne_zero.mpr hone)
  have hs : omega ^ 2 = -omega - 1 := by linear_combination hq
  have h4 : omega ^ 4 = omega := by
    calc
      omega ^ 4 = omega ^ 3 * omega := by ring
      _ = omega := by rw [hcube]; ring
  have h5 : omega ^ 5 = omega ^ 2 := by
    calc
      omega ^ 5 = omega ^ 3 * omega ^ 2 := by ring
      _ = omega ^ 2 := by rw [hcube]; ring
  have h6 : omega ^ 6 = 1 := by
    calc
      omega ^ 6 = (omega ^ 3) ^ 2 := by ring
      _ = 1 := by rw [hcube]; norm_num
  have hn1 : (-1 : Triple) = 2 := by decide
  have hn2 : (-2 : Triple) = 1 := by decide
  rw [Matrix.det_fin_three]
  norm_num [Matrix.circulant, hn1, hn2, mode]
  simp only [hn1, hn2]
  ring_nf
  simp only [hcube, h4, h5, h6, hs]
  ring

/-- All four actual matrix determinants are nonzero from flatness and Gram. -/
theorem four_block_determinants_nonzero (a b c e : Triple → ℂ)
    (hflat : ∀ i j, Complex.normSq (blockCirculant a b c e i j) = 1)
    (hgram : (blockCirculant a b c e).conjTranspose * blockCirculant a b c e =
      (6 : ℂ) • (1 : Matrix Six Six ℂ)) :
    (Matrix.circulant a).det ≠ 0 ∧ (Matrix.circulant b).det ≠ 0 ∧
      (Matrix.circulant c).det ≠ 0 ∧ (Matrix.circulant e).det ≠ 0 := by
  let omega : ℂ := Complex.exp (2 * (Real.pi : ℂ) * Complex.I / 3)
  have hw : IsPrimitiveRoot omega 3 := Complex.isPrimitiveRoot_exp 3 (by decide)
  have hc : omega ^ 3 = 1 := hw.pow_eq_one
  have hn : omega ≠ 1 := hw.ne_one (by decide)
  have hc2 : (omega ^ 2) ^ 3 = 1 := by
    calc
      (omega ^ 2) ^ 3 = (omega ^ 3) ^ 2 := by ring
      _ = 1 := by rw [hc]; norm_num
  have h0 := four_nonzero_modes_of_actual_flat_gram a b c e hflat hgram 1 (by norm_num)
  have h1 := four_nonzero_modes_of_actual_flat_gram a b c e hflat hgram omega hc
  have h2 := four_nonzero_modes_of_actual_flat_gram a b c e hflat hgram (omega ^ 2) hc2
  have hdet (v : Triple → ℂ) (hv0 : mode v 1 ≠ 0)
      (hv1 : mode v omega ≠ 0) (hv2 : mode v (omega ^ 2) ≠ 0) :
      (Matrix.circulant v).det ≠ 0 := by
    rw [circulant_det_factorization v omega hc hn]
    exact mul_ne_zero (mul_ne_zero hv0 hv1) hv2
  exact ⟨hdet a h0.1 h1.1 h2.1,
    hdet b h0.2.1 h1.2.1 h2.2.1,
    hdet c h0.2.2.1 h1.2.2.1 h2.2.2.1,
    hdet e h0.2.2.2 h1.2.2.2 h2.2.2.2⟩

private theorem inverse_of_det_ne_zero (A : Matrix Triple Triple ℂ) (hdet : A.det ≠ 0) :
    ∃ N : Matrix Triple Triple ℂ, A * N = 1 ∧ N * A = 1 := by
  have hu : IsUnit A := (Matrix.isUnit_iff_isUnit_det A).mpr (isUnit_iff_ne_zero.mpr hdet)
  obtain ⟨u, hu⟩ := hu
  refine ⟨↑(u⁻¹), ?_, ?_⟩
  · rw [← hu]
    simp
  · rw [← hu]
    simp

/-- Four actual inverses, with all eight left/right matrix equations. -/
theorem four_block_inverses_of_actual_flat_gram (a b c e : Triple → ℂ)
    (hflat : ∀ i j, Complex.normSq (blockCirculant a b c e i j) = 1)
    (hgram : (blockCirculant a b c e).conjTranspose * blockCirculant a b c e =
      (6 : ℂ) • (1 : Matrix Six Six ℂ)) :
    ∃ A' B' C' E' : Matrix Triple Triple ℂ,
      Matrix.circulant a * A' = 1 ∧ A' * Matrix.circulant a = 1 ∧
      Matrix.circulant b * B' = 1 ∧ B' * Matrix.circulant b = 1 ∧
      Matrix.circulant c * C' = 1 ∧ C' * Matrix.circulant c = 1 ∧
      Matrix.circulant e * E' = 1 ∧ E' * Matrix.circulant e = 1 := by
  obtain ⟨ha, hb, hc, he⟩ := four_block_determinants_nonzero a b c e hflat hgram
  obtain ⟨A', hA, hA'⟩ := inverse_of_det_ne_zero (Matrix.circulant a) ha
  obtain ⟨B', hB, hB'⟩ := inverse_of_det_ne_zero (Matrix.circulant b) hb
  obtain ⟨C', hC, hC'⟩ := inverse_of_det_ne_zero (Matrix.circulant c) hc
  obtain ⟨E', hE, hE'⟩ := inverse_of_det_ne_zero (Matrix.circulant e) he
  exact ⟨A', B', C', E', hA, hA', hB, hB', hC, hC', hE, hE'⟩

#print axioms circulant_det_factorization
#print axioms four_block_determinants_nonzero
#print axioms four_block_inverses_of_actual_flat_gram

end MUBTriplets.CirculantInvertibility
