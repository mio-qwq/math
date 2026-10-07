import FiniteCore
import Mathlib.Algebra.Polynomial.Coeff
import Mathlib.Data.ZMod.Basic
import Mathlib.Tactic.Ring

/-!
# Scalar semantics of the bit-polynomial multiplication

This file connects the exact `pMul` defined in the frozen Std certificate
to actual `Polynomial (ZMod 2)` multiplication, for arbitrary natural
numbers. It does not yet interpret packed coefficient vectors, construct
the algebra over an arbitrary field, or prove the complete ARC theorem.
-/

namespace ARCBitPolynomial

open Polynomial

noncomputable section

/-- The actual F₂ coefficient represented by one Boolean bit. -/
def bitCoeff (b : Bool) : ZMod 2 := if b then 1 else 0

private theorem bitCoeff_support (n i : Nat)
    (h : bitCoeff (n.testBit i) ≠ 0) : i ∈ Finset.range (n.log2 + 1) := by
  apply Finset.mem_range.mpr
  by_contra hi
  have hn : n < 2 ^ i := lt_of_lt_of_le (Nat.lt_log2_self (n := n))
    (Nat.pow_le_pow_right (by decide) (Nat.le_of_not_gt hi))
  have hb := Nat.testBit_lt_two_pow hn
  simp [bitCoeff, hb] at h

/-- Decode binary digits as coefficients of a genuine polynomial over F₂. -/
def decode (n : Nat) : Polynomial (ZMod 2) :=
  .ofFinsupp (.ofCoeff (Finsupp.onFinset (Finset.range (n.log2 + 1))
    (fun i => bitCoeff (n.testBit i)) (bitCoeff_support n)))

@[simp] theorem coeff_decode (n i : Nat) :
    (decode n).coeff i = bitCoeff (n.testBit i) := rfl

@[simp] theorem decode_zero : decode 0 = 0 := by
  ext i
  simp [bitCoeff]

theorem bitCoeff_xor (a b : Bool) :
    bitCoeff (a ^^ b) = bitCoeff a + bitCoeff b := by
  cases a <;> cases b <;> decide

theorem bitCoeff_injective : Function.Injective bitCoeff := by decide

/-- No distinct bit-polynomial codes denote the same F₂ polynomial. -/
theorem decode_injective : Function.Injective decode := by
  intro a b h
  apply Nat.eq_of_testBit_eq
  intro i
  apply bitCoeff_injective
  have hc := congrArg (fun p : Polynomial (ZMod 2) => p.coeff i) h
  simpa only [coeff_decode] using hc

theorem decode_xor (a b : Nat) :
    decode (Nat.xor a b) = decode a + decode b := by
  ext i
  simp only [coeff_decode, coeff_add, Nat.xor_eq, Nat.testBit_xor, bitCoeff_xor]

theorem decode_double (a : Nat) : decode (2 * a) = X * decode a := by
  ext i
  cases i with
  | zero =>
      simp [bitCoeff, Nat.testBit_zero]
  | succ i =>
      rw [coeff_decode, coeff_X_mul]
      have hb : (2 * a).testBit (i + 1) = a.testBit i := by
        simpa using (Nat.testBit_two_pow_mul (i := 1) (a := a) (j := i + 1))
      rw [hb, coeff_decode]

theorem decode_split (b : Nat) :
    decode b = C (bitCoeff (b.testBit 0)) + X * decode (b / 2) := by
  ext i
  cases i with
  | zero => simp
  | succ i => simp [Nat.testBit_succ]

/-- Adequate fuel makes the carryless convolution genuine F₂[X] multiplication. -/
theorem decode_pMulAux (fuel a b : Nat) (hb : b < 2 ^ fuel) :
    decode (ARCFiniteCore.pMulAux fuel a b) = decode a * decode b := by
  induction fuel generalizing a b with
  | zero =>
      have hz : b = 0 := by simpa using hb
      simp [ARCFiniteCore.pMulAux, hz]
  | succ fuel ih =>
      by_cases hz : b = 0
      · simp [ARCFiniteCore.pMulAux, hz]
      · have hhalf : b / 2 < 2 ^ fuel := by
          rw [Nat.div_lt_iff_lt_mul (by decide)]
          simpa [pow_succ, Nat.mul_comm] using hb
        rw [ARCFiniteCore.pMulAux, ite_eq_right hz, decode_xor,
          ih (2 * a) (b / 2) hhalf, decode_double]
        rw [decode_split b]
        by_cases hp : b % 2 = 1
        · simp [hp, Nat.testBit_zero, bitCoeff]
          ring
        · simp [hp, Nat.testBit_zero, bitCoeff]
          ring

/-- The exact frozen certificate's multiplication is sound for all inputs. -/
theorem decode_pMul (a b : Nat) :
    decode (ARCFiniteCore.pMul a b) = decode a * decode b := by
  exact decode_pMulAux (b.log2 + 1) a b (Nat.lt_log2_self (n := b))

/-- The encoded multiplication is associative for every natural-number code. -/
theorem pMul_assoc (a b c : Nat) :
    ARCFiniteCore.pMul (ARCFiniteCore.pMul a b) c =
      ARCFiniteCore.pMul a (ARCFiniteCore.pMul b c) := by
  apply decode_injective
  simp only [decode_pMul, mul_assoc]

theorem pMul_comm (a b : Nat) : ARCFiniteCore.pMul a b = ARCFiniteCore.pMul b a := by
  apply decode_injective
  simp only [decode_pMul, mul_comm]

#print axioms decode_injective
#print axioms decode_xor
#print axioms decode_double
#print axioms decode_pMul
#print axioms pMul_assoc
#print axioms pMul_comm

end
end ARCBitPolynomial
