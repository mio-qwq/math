import BytePacking
import Mathlib.Algebra.Polynomial.Eval.Defs

/-!
# Evaluation of scalar and byte codes in characteristic two

The frozen scalar code denotes an F₂ polynomial. Evaluating that polynomial
at any element `q` of any commutative ring of characteristic two gives a
sound interpretation of XOR, carryless multiplication, and doubling.
Eight-bit packed coordinates are interpreted using the same evaluation.

These theorems are generic semantic bridges for arbitrary codes, rings,
and parameters. They do not construct the ARC algebra or prove its full
Hochschild complex. Evaluation is not asserted to be injective: the file
proves explicitly that evaluation at zero is not injective on scalar codes.
-/

namespace ARCScalarEvaluation

open ARCBitPolynomial ARCBytePacking

noncomputable section

variable {R : Type*} [CommRing R] [CharP R 2]

/-- Interpret a binary scalar polynomial code at `q` in characteristic two. -/
def evaluate (q : R) (code : Nat) : R :=
  Polynomial.eval₂ (ZMod.castHom (dvd_refl 2) R) q (decode code)

/-- XOR is addition after evaluation, for all natural-number codes. -/
theorem evaluate_xor (q : R) (a b : Nat) :
    evaluate q (Nat.xor a b) = evaluate q a + evaluate q b := by
  simp only [evaluate, decode_xor, Polynomial.eval₂_add]

/-- The exact frozen carryless multiplication denotes ring multiplication. -/
theorem evaluate_pMul (q : R) (a b : Nat) :
    evaluate q (ARCFiniteCore.pMul a b) = evaluate q a * evaluate q b := by
  simp only [evaluate, decode_pMul, Polynomial.eval₂_mul]

/-- A bit shift doubles the code and multiplies its value by the parameter. -/
theorem evaluate_double (q : R) (a : Nat) :
    evaluate q (2 * a) = q * evaluate q a := by
  simp only [evaluate, decode_double, Polynomial.eval₂_mul, Polynomial.eval₂_X]

@[simp] theorem evaluate_zero (q : R) : evaluate q 0 = 0 := by
  simp [evaluate]

/-- The unit binary code is the unit polynomial; no extra decoding axiom. -/
theorem decode_one : decode 1 = 1 := by
  rw [decode_split 1]
  simp [bitCoeff]

@[simp] theorem evaluate_one (q : R) : evaluate q 1 = 1 := by
  simp [evaluate, decode_one]

/-- Code two is the polynomial variable, so its value is the chosen parameter. -/
@[simp] theorem evaluate_two (q : R) : evaluate q 2 = q := by
  simpa using evaluate_double q 1

/-- Evaluate the allocated eight-bit coefficient at coordinate `i`. -/
def evalVec (q : R) (code : Nat) (i : Nat) : R :=
  evaluate q (byte code i)

theorem evalVec_xor_coordinate (q : R) (a b i : Nat) :
    evalVec q (Nat.xor a b) i = evalVec q a i + evalVec q b i := by
  simp only [evalVec, byte_xor, evaluate_xor]

/-- Packed XOR denotes pointwise vector addition after specialization. -/
theorem evalVec_xor (q : R) (a b : Nat) :
    evalVec q (Nat.xor a b) = evalVec q a + evalVec q b := by
  funext i
  exact evalVec_xor_coordinate q a b i

@[simp] theorem evalVec_zero (q : R) : evalVec q 0 = 0 := by
  funext i
  simp [evalVec]

/-- A coefficient fitting in its eight allocated bits specializes in one coordinate. -/
theorem evalVec_pack_coordinate (q : R) (j c i : Nat) (hc : c < 256) :
    evalVec q (ARCFiniteCore.pack j c) i = if i = j then evaluate q c else 0 := by
  dsimp [evalVec]
  rw [byte_pack j c i hc]
  split_ifs <;> simp

theorem evalVec_pack (q : R) (j c : Nat) (hc : c < 256) :
    evalVec q (ARCFiniteCore.pack j c) =
      fun i => if i = j then evaluate q c else 0 := by
  funext i
  exact evalVec_pack_coordinate q j c i hc

/-- A concrete universal limitation: specialization at zero identifies codes 0 and 2. -/
theorem evaluate_at_zero_not_injective :
    ¬ Function.Injective (evaluate (0 : R)) := by
  intro hinjective
  have hequal : evaluate (0 : R) 0 = evaluate (0 : R) 2 := by simp
  have hcodes : (0 : Nat) = 2 := hinjective hequal
  omega

#print axioms evaluate_xor
#print axioms evaluate_pMul
#print axioms evaluate_double
#print axioms evaluate_zero
#print axioms decode_one
#print axioms evaluate_one
#print axioms evaluate_two
#print axioms evalVec_xor_coordinate
#print axioms evalVec_xor
#print axioms evalVec_zero
#print axioms evalVec_pack_coordinate
#print axioms evalVec_pack
#print axioms evaluate_at_zero_not_injective

end
end ARCScalarEvaluation
