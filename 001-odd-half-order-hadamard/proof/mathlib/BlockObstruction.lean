import Mathlib.LinearAlgebra.Trace
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.LinearAlgebra.Matrix.ConjTranspose
import Mathlib.Basic.Complex.Basic
import Std

/-!
The actual complex-matrix block obstruction used in paper.md, Section 4.
Starting with two Gram blocks and unit squared moduli, this file constructs
the idempotent, computes its trace, identifies that trace with an integer
rank, and proves that the block size cannot be odd.
The preceding Newton/support arguments yielding these blocks are separate.
-/

open scoped Matrix

namespace OddHalfOrder

theorem complex_block_obstruction
    (m : Nat) (hodd : ∃ s : Nat, m = 2 * s + 1)
    (A B : Matrix (Fin m) (Fin m) ℂ)
    (horth : Aᴴ * B = 0)
    (hgram : A * Aᴴ + B * Bᴴ = (2 * (m : ℂ)) • (1 : Matrix (Fin m) (Fin m) ℂ))
    (hunit : ∀ i j, Complex.normSq (A i j) = 1) : False := by
  classical
  have hm : 0 < m := by
    obtain ⟨s, hs⟩ := hodd
    omega
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
  have hentry : ∀ i j, A i j * star (A i j) = (1 : ℂ) := by
    intro i j
    rw [Complex.star_def, Complex.mul_conj, hunit i j]
    rfl
  have htraceG : Matrix.trace G = (m : ℂ) * (m : ℂ) := by
    dsimp [G]
    simp only [Matrix.trace, Matrix.diag_apply, Matrix.mul_apply,
      Matrix.conjTranspose_apply, hentry,
      Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul, mul_one]
  have htraceP : 2 * Matrix.trace P = (m : ℂ) := by
    dsimp [P]
    rw [Matrix.trace_smul, smul_eq_mul, htraceG]
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
  have hcast : ((2 * Module.finrank ℂ (LinearMap.range f) : Nat) : ℂ) = (m : ℂ) := by
    rw [Nat.cast_mul, Nat.cast_ofNat, ← hrank]
    exact htraceP
  have heq : 2 * Module.finrank ℂ (LinearMap.range f) = m := Nat.cast_injective hcast
  obtain ⟨s, hs⟩ := hodd
  omega

#print axioms complex_block_obstruction

end OddHalfOrder
