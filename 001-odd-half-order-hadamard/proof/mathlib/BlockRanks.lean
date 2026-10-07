import Mathlib.LinearAlgebra.Trace
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.LinearAlgebra.Matrix.ConjTranspose
import Mathlib.LinearAlgebra.Matrix.Rank
import Mathlib.Basic.Complex.Basic
import Std

/-!
Exact ranks of the complex Gram blocks from general-patterns.md.
The assumptions concern actual matrices; no rank or projection trace is assumed.
The Newton and support arguments producing these blocks remain separate.
-/

open scoped Matrix

namespace OddHalfOrder

/-- The Gram equations identify the range rank of `AAᴴ` with the rank of `A`,
without invoking an order on the complex numbers. -/
theorem complex_gram_rank
    (m : Nat) (hm : 0 < m)
    (A B : Matrix (Fin m) (Fin m) ℂ)
    (horth : Aᴴ * B = 0)
    (hgram : A * Aᴴ + B * Bᴴ = (2 * (m : ℂ)) • (1 : Matrix (Fin m) (Fin m) ℂ)) :
    (A * Aᴴ).rank = A.rank := by
  classical
  have hd : (2 * (m : ℂ)) ≠ 0 :=
    mul_ne_zero (by norm_num) (Nat.cast_ne_zero.mpr (Nat.ne_of_gt hm))
  have hrev : Bᴴ * A = 0 := by
    simpa using congrArg Matrix.conjTranspose horth
  have hzero : (B * Bᴴ) * A = 0 := by
    rw [Matrix.mul_assoc, hrev]
    simp
  have hscale : (A * Aᴴ) * A = (2 * (m : ℂ)) • A := by
    calc
      (A * Aᴴ) * A = (A * Aᴴ + B * Bᴴ) * A := by
        rw [Matrix.add_mul, hzero, add_zero]
      _ = ((2 * (m : ℂ)) • (1 : Matrix (Fin m) (Fin m) ℂ)) * A := by rw [hgram]
      _ = (2 * (m : ℂ)) • A := by rw [Matrix.smul_mul, Matrix.one_mul]
  apply le_antisymm (Matrix.rank_mul_le_left A Aᴴ)
  have hle := Matrix.rank_mul_le_left (A * Aᴴ) A
  rw [hscale, Matrix.rank_smul_of_mem_nonZeroDivisors A
    (mem_nonZeroDivisors_of_ne_zero hd)] at hle
  exact hle

/-- The Gram trace is enough for the exact half-rank conclusion. -/
theorem complex_block_rank_from_gram_trace
    (m : Nat) (hm : 0 < m)
    (A B : Matrix (Fin m) (Fin m) ℂ)
    (horth : Aᴴ * B = 0)
    (hgram : A * Aᴴ + B * Bᴴ = (2 * (m : ℂ)) • (1 : Matrix (Fin m) (Fin m) ℂ))
    (htrace : Matrix.trace (A * Aᴴ) = (m : ℂ) * (m : ℂ)) :
    2 * A.rank = m := by
  classical
  have hmc : (m : ℂ) ≠ 0 := Nat.cast_ne_zero.mpr (Nat.ne_of_gt hm)
  have hd : (2 * (m : ℂ)) ≠ 0 := mul_ne_zero (by norm_num) hmc
  let G : Matrix (Fin m) (Fin m) ℂ := A * Aᴴ
  let J : Matrix (Fin m) (Fin m) ℂ := B * Bᴴ
  have hcross : G * J = 0 := by
    dsimp [G, J]
    calc
      (A * Aᴴ) * (B * Bᴴ) = A * (Aᴴ * B) * Bᴴ := by
        simp only [Matrix.mul_assoc]
      _ = 0 := by rw [horth]; simp
  have hsum : G + J = (2 * (m : ℂ)) • (1 : Matrix (Fin m) (Fin m) ℂ) := hgram
  have hsquare : G * G = (2 * (m : ℂ)) • G := by
    calc
      G * G = G * (G + J) := by rw [Matrix.mul_add, hcross, add_zero]
      _ = G * ((2 * (m : ℂ)) • (1 : Matrix (Fin m) (Fin m) ℂ)) := by rw [hsum]
      _ = (2 * (m : ℂ)) • G := by rw [Matrix.mul_smul, Matrix.mul_one]
  let P : Matrix (Fin m) (Fin m) ℂ := (2 * (m : ℂ))⁻¹ • G
  have hP : P * P = P := by
    dsimp [P]
    rw [Matrix.smul_mul, Matrix.mul_smul, smul_smul, hsquare, smul_smul]
    simp only [mul_assoc, inv_mul_cancel₀ hd, mul_one]
  have htraceP : 2 * Matrix.trace P = (m : ℂ) := by
    dsimp [P, G]
    rw [Matrix.trace_smul, smul_eq_mul, htrace]
    calc
      2 * ((2 * (m : ℂ))⁻¹ * ((m : ℂ) * (m : ℂ))) =
          ((2 * (m : ℂ)) * (2 * (m : ℂ))⁻¹) * (m : ℂ) := by ring
      _ = (m : ℂ) := by rw [mul_inv_cancel₀ hd, one_mul]
  let f : Module.End ℂ (Fin m → ℂ) := Matrix.toLinAlgEquiv' P
  have hf : IsIdempotentElem f := by
    change Matrix.toLinAlgEquiv' P * Matrix.toLinAlgEquiv' P = Matrix.toLinAlgEquiv' P
    rw [← map_mul, hP]
  have htf : LinearMap.trace ℂ (Fin m → ℂ) f = Matrix.trace P := by
    change LinearMap.trace ℂ (Fin m → ℂ) P.toLin' = Matrix.trace P
    exact Matrix.trace_toLin'_eq P
  have hrank : Matrix.trace P = (Module.finrank ℂ (LinearMap.range f) : ℂ) := by
    rw [← htf]
    exact (LinearMap.IsIdempotentElem.isProj_range f hf).trace
  have hPrank : P.rank = A.rank := by
    change ((2 * (m : ℂ))⁻¹ • G).rank = A.rank
    rw [Matrix.rank_smul_of_mem_nonZeroDivisors G
      (mem_nonZeroDivisors_of_ne_zero (inv_ne_zero hd))]
    exact complex_gram_rank m hm A B horth hgram
  have hfrank : Module.finrank ℂ (LinearMap.range f) = A.rank := by
    change Module.finrank ℂ (LinearMap.range P.toLin') = A.rank
    rw [Matrix.toLin'_apply']
    exact hPrank
  have hcast : ((2 * A.rank : Nat) : ℂ) = (m : ℂ) := by
    rw [Nat.cast_mul, Nat.cast_ofNat, ← hfrank, ← hrank]
    exact htraceP
  exact Nat.cast_injective hcast

/-- Unit squared moduli supply the Gram trace, so every positive block has
exactly half the ambient rank. -/
theorem complex_block_rank
    (m : Nat) (hm : 0 < m)
    (A B : Matrix (Fin m) (Fin m) ℂ)
    (horth : Aᴴ * B = 0)
    (hgram : A * Aᴴ + B * Bᴴ = (2 * (m : ℂ)) • (1 : Matrix (Fin m) (Fin m) ℂ))
    (hunit : ∀ i j, Complex.normSq (A i j) = 1) :
    2 * A.rank = m := by
  classical
  apply complex_block_rank_from_gram_trace m hm A B horth hgram
  have hentry : ∀ i j, A i j * star (A i j) = (1 : ℂ) := by
    intro i j
    rw [Complex.star_def, Complex.mul_conj, hunit i j]
    rfl
  simp only [Matrix.trace, Matrix.diag_apply, Matrix.mul_apply,
    Matrix.conjTranspose_apply, hentry, Finset.sum_const, Finset.card_univ,
    Fintype.card_fin, nsmul_eq_mul, mul_one]

/-- Only the entries of `A` need unit squared moduli: the total Gram trace
forces the same half-rank for `B`. -/
theorem complex_block_ranks
    (m : Nat) (hm : 0 < m)
    (A B : Matrix (Fin m) (Fin m) ℂ)
    (horth : Aᴴ * B = 0)
    (hgram : A * Aᴴ + B * Bᴴ = (2 * (m : ℂ)) • (1 : Matrix (Fin m) (Fin m) ℂ))
    (hunit : ∀ i j, Complex.normSq (A i j) = 1) :
    2 * A.rank = m ∧ 2 * B.rank = m := by
  classical
  refine ⟨complex_block_rank m hm A B horth hgram hunit, ?_⟩
  have hentry : ∀ i j, A i j * star (A i j) = (1 : ℂ) := by
    intro i j
    rw [Complex.star_def, Complex.mul_conj, hunit i j]
    rfl
  have htraceA : Matrix.trace (A * Aᴴ) = (m : ℂ) * (m : ℂ) := by
    simp only [Matrix.trace, Matrix.diag_apply, Matrix.mul_apply,
      Matrix.conjTranspose_apply, hentry, Finset.sum_const, Finset.card_univ,
      Fintype.card_fin, nsmul_eq_mul, mul_one]
  have htrsum : Matrix.trace (A * Aᴴ) + Matrix.trace (B * Bᴴ) =
      (2 * (m : ℂ)) * (m : ℂ) := by
    have h := congrArg Matrix.trace hgram
    simpa only [Matrix.trace_add, Matrix.trace_smul, smul_eq_mul,
      Matrix.trace_one, Fintype.card_fin] using h
  have htraceB : Matrix.trace (B * Bᴴ) = (m : ℂ) * (m : ℂ) := by
    have hsum : (m : ℂ) * (m : ℂ) + Matrix.trace (B * Bᴴ) =
        (m : ℂ) * (m : ℂ) + (m : ℂ) * (m : ℂ) := by
      calc
        (m : ℂ) * (m : ℂ) + Matrix.trace (B * Bᴴ) =
            Matrix.trace (A * Aᴴ) + Matrix.trace (B * Bᴴ) := by rw [htraceA]
        _ = (2 * (m : ℂ)) * (m : ℂ) := htrsum
        _ = (m : ℂ) * (m : ℂ) + (m : ℂ) * (m : ℂ) := by ring
    exact add_left_cancel hsum
  have hrev : Bᴴ * A = 0 := by
    simpa using congrArg Matrix.conjTranspose horth
  have hgramrev : B * Bᴴ + A * Aᴴ =
      (2 * (m : ℂ)) • (1 : Matrix (Fin m) (Fin m) ℂ) := by
    rw [add_comm]
    exact hgram
  exact complex_block_rank_from_gram_trace m hm B A hrev hgramrev htraceB

/-- Both actual complex blocks are singular whenever their positive size
and the Gram equations admit such blocks. -/
theorem complex_block_determinants_zero
    (m : Nat) (hm : 0 < m)
    (A B : Matrix (Fin m) (Fin m) ℂ)
    (horth : Aᴴ * B = 0)
    (hgram : A * Aᴴ + B * Bᴴ = (2 * (m : ℂ)) • (1 : Matrix (Fin m) (Fin m) ℂ))
    (hunit : ∀ i j, Complex.normSq (A i j) = 1) :
    A.det = 0 ∧ B.det = 0 := by
  classical
  obtain ⟨hA, hB⟩ := complex_block_ranks m hm A B horth hgram hunit
  constructor
  · by_contra hdet
    have hfull := Matrix.rank_of_det_ne_zero hdet
    simp only [Fintype.card_fin] at hfull
    omega
  · by_contra hdet
    have hfull := Matrix.rank_of_det_ne_zero hdet
    simp only [Fintype.card_fin] at hfull
    omega

#print axioms complex_gram_rank
#print axioms complex_block_rank_from_gram_trace
#print axioms complex_block_rank
#print axioms complex_block_ranks
#print axioms complex_block_determinants_zero

end OddHalfOrder
