import SpectralMatchingSupport
import Mathlib.LinearAlgebra.Matrix.ConjTranspose

/-!
Fixed-spectrum Hermitian unitary matrices and their reverse-pairing phases.

The imported support theorem concerns ordinary complex matrix multiplication.
Right unitarity B * B.conjTranspose = 1 forces the surviving partner
entry to have normSq one; no nonzero-entry or phase assumption is used in
that forward argument. Hermitian symmetry then gives conjugate partner
phases. The phase-family theorem describes the complete unitary Hermitian family
anticommuting with diag(-5,-3,-1,1,3,5) as diagonal phases times the actual
reverse permutation matrix. It includes both matrix unitarity equations.

The fixed-node classification does not construct a MUB companion, provide
the conjugation bridge from an actual companion, or prove general cubic
or adjoint coupling.
-/

noncomputable section

open scoped BigOperators

namespace MUBTriplets.SpectralMatching

/-- The ordinary permutation matrix for the fixed involution i |-> Fin.rev i. -/
def reversePermutation : Matrix (Fin 6) (Fin 6) ℂ :=
  fun i j => if j = Fin.rev i then 1 else 0

/-- The whole matrix product of diagonal phases and the reverse permutation. -/
def reversePhaseMatrix (p : Fin 6 → ℂ) : Matrix (Fin 6) (Fin 6) ℂ :=
  Matrix.diagonal p * reversePermutation

@[simp] theorem reversePhaseMatrix_apply (p : Fin 6 → ℂ) (i j : Fin 6) :
    reversePhaseMatrix p i j = if j = Fin.rev i then p i else 0 := by
  rw [reversePhaseMatrix, Matrix.diagonal_mul]
  simp only [reversePermutation, mul_ite, mul_one, mul_zero]

theorem reversePhaseMatrix_support (p : Fin 6 → ℂ) :
    ∀ i j : Fin 6, j ≠ Fin.rev i → reversePhaseMatrix p i j = 0 := by
  intro i j hij
  simp only [reversePhaseMatrix_apply, ite_eq_right hij]

/-- Collapse an actual Gram product by support, without assuming any phases. -/
theorem gram_entry_of_reverse_support
    (B : Matrix (Fin 6) (Fin 6) ℂ)
    (hsupport : ∀ i j : Fin 6, j ≠ Fin.rev i → B i j = 0)
    (i j : Fin 6) :
    (B * B.conjTranspose) i j =
      B i (Fin.rev i) * star (B j (Fin.rev i)) := by
  rw [Matrix.mul_apply]
  have hsum :
      (∑ k : Fin 6, B i k * B.conjTranspose k j) =
        B i (Fin.rev i) * B.conjTranspose (Fin.rev i) j := by
    apply Finset.sum_eq_single (Fin.rev i)
    · intro k _ hk
      rw [hsupport i k hk, zero_mul]
    · intro hnot
      exact (hnot (Finset.mem_univ _)).elim
  simpa only [Matrix.conjTranspose_apply] using hsum

/-- Actual right unitarity forces a unit phase at every reverse partner. -/
theorem partner_normSq_of_actual_gram
    (B : Matrix (Fin 6) (Fin 6) ℂ)
    (hsupport : ∀ i j : Fin 6, j ≠ Fin.rev i → B i j = 0)
    (hgram : B * B.conjTranspose = 1) (i : Fin 6) :
    Complex.normSq (B i (Fin.rev i)) = 1 := by
  have hentry : (B * B.conjTranspose) i i = 1 := by
    simpa only [Matrix.one_apply_eq] using
      congrArg (fun M : Matrix (Fin 6) (Fin 6) ℂ => M i i) hgram
  rw [gram_entry_of_reverse_support B hsupport i i] at hentry
  have hnorm : (Complex.normSq (B i (Fin.rev i)) : ℂ) = 1 := by
    simpa only [Complex.star_def, Complex.mul_conj] using hentry
  exact Complex.ofReal_eq_one.mp hnorm

/-- Hermitian symmetry yields the conjugate phase on the partner row. -/
theorem hermitian_partner_phases
    (B : Matrix (Fin 6) (Fin 6) ℂ)
    (hhermitian : B.conjTranspose = B) (i : Fin 6) :
    B (Fin.rev i) i = star (B i (Fin.rev i)) := by
  have hentry := congrArg
    (fun M : Matrix (Fin 6) (Fin 6) ℂ => M (Fin.rev i) i) hhermitian
  simpa only [Matrix.conjTranspose_apply] using hentry.symm

/-- Support yields the entire matrix factorization, not just selected entries. -/
theorem eq_reversePhaseMatrix_of_support
    (B : Matrix (Fin 6) (Fin 6) ℂ)
    (hsupport : ∀ i j : Fin 6, j ≠ Fin.rev i → B i j = 0) :
    B = reversePhaseMatrix (fun i => B i (Fin.rev i)) := by
  apply Matrix.ext
  intro i j
  by_cases hij : j = Fin.rev i
  · subst j
    simp [reversePhaseMatrix_apply]
  · rw [hsupport i j hij, reversePhaseMatrix_apply, ite_eq_right hij]

/-- Unit phases construct the full actual right Gram equation. -/
theorem reversePhaseMatrix_right_unitary
    (p : Fin 6 → ℂ) (hnorm : ∀ i, Complex.normSq (p i) = 1) :
    reversePhaseMatrix p * (reversePhaseMatrix p).conjTranspose = 1 := by
  apply Matrix.ext
  intro i j
  rw [gram_entry_of_reverse_support
    (reversePhaseMatrix p) (reversePhaseMatrix_support p) i j]
  by_cases hij : i = j
  · subst j
    simp [reversePhaseMatrix_apply, Complex.star_def, Complex.mul_conj, hnorm i]
  · have hrev : Fin.rev i ≠ Fin.rev j := fun h => hij (Fin.rev_injective h)
    simp [reversePhaseMatrix_apply, hrev, hij]

/-- Conjugate partners construct the whole actual Hermitian equation. -/
theorem reversePhaseMatrix_hermitian
    (p : Fin 6 → ℂ) (hphases : ∀ i, p (Fin.rev i) = star (p i)) :
    (reversePhaseMatrix p).conjTranspose = reversePhaseMatrix p := by
  apply Matrix.ext
  intro i j
  change star (reversePhaseMatrix p j i) = reversePhaseMatrix p i j
  by_cases hij : j = Fin.rev i
  · subst j
    simp [reversePhaseMatrix_apply, Fin.rev_rev, hphases i]
  · have hji : i ≠ Fin.rev j := by
      intro h
      apply hij
      simpa only [Fin.rev_rev] using (congrArg Fin.rev h).symm
    simp only [reversePhaseMatrix_apply, ite_eq_right hij, ite_eq_right hji, star_zero]

/-- The whole phase matrix anticommutes with the actual fixed diagonal matrix. -/
theorem reversePhaseMatrix_anticommutes (p : Fin 6 → ℂ) :
    Matrix.diagonal spectralNode * reversePhaseMatrix p +
      reversePhaseMatrix p * Matrix.diagonal spectralNode = 0 := by
  exact (spectral_anticommutation_iff_reverse_support (reversePhaseMatrix p)).mpr
    (reversePhaseMatrix_support p)

/-- Exact phase-family classification with both actual unitarity equations. -/
theorem unitary_hermitian_anticommutation_iff_phase_family
    (B : Matrix (Fin 6) (Fin 6) ℂ) :
    (B * B.conjTranspose = 1 ∧ B.conjTranspose * B = 1 ∧
      B.conjTranspose = B ∧
      Matrix.diagonal spectralNode * B + B * Matrix.diagonal spectralNode = 0) ↔
    ∃ p : Fin 6 → ℂ,
      (∀ i, Complex.normSq (p i) = 1) ∧
      (∀ i, p (Fin.rev i) = star (p i)) ∧
      B = reversePhaseMatrix p := by
  constructor
  · rintro ⟨hgram, _, hhermitian, hanti⟩
    have hsupport := (spectral_anticommutation_iff_reverse_support B).mp hanti
    refine ⟨(fun i => B i (Fin.rev i)), ?_, ?_,
      eq_reversePhaseMatrix_of_support B hsupport⟩
    · intro i
      exact partner_normSq_of_actual_gram B hsupport hgram i
    · intro i
      simpa only [Fin.rev_rev] using hermitian_partner_phases B hhermitian i
  · rintro ⟨p, hnorm, hphases, rfl⟩
    have hhermitian := reversePhaseMatrix_hermitian p hphases
    have hright := reversePhaseMatrix_right_unitary p hnorm
    have hleft :
        (reversePhaseMatrix p).conjTranspose * reversePhaseMatrix p = 1 := by
      simpa only [hhermitian] using hright
    exact ⟨hright, hleft, hhermitian, reversePhaseMatrix_anticommutes p⟩

#print axioms partner_normSq_of_actual_gram
#print axioms hermitian_partner_phases
#print axioms unitary_hermitian_anticommutation_iff_phase_family

end MUBTriplets.SpectralMatching
