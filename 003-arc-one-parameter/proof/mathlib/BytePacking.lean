import BitPolynomial

/-!
# Eight-bit coordinate semantics

The fixed certificates allocate eight bits to each basis coordinate. These
generic theorems decode XOR coordinatewise and a packed single coefficient
without overlap, whenever that coefficient fits in eight bits. They do not
yet construct a finite-dimensional algebra or a Hochschild complex.
-/

namespace ARCBytePacking

open ARCBitPolynomial

/-- The eight bits allocated to coordinate `i` of the natural-number code. -/
def byte (code i : Nat) : Nat := (code / 2 ^ (8 * i)) % 2 ^ 8

/-- Extracting a coordinate commutes with XOR on arbitrary natural numbers. -/
theorem byte_xor (a b i : Nat) :
    byte (Nat.xor a b) i = Nat.xor (byte a i) (byte b i) := by
  simp only [byte, Nat.xor_eq, Nat.xor_div_two_pow, Nat.xor_mod_two_pow]

@[simp] theorem byte_zero (i : Nat) : byte 0 i = 0 := by simp [byte]

/-- A coefficient that fits in one byte occupies exactly its assigned coordinate. -/
theorem byte_pack (j c i : Nat) (hc : c < 256) :
    byte (ARCFiniteCore.pack j c) i = if i = j then c else 0 := by
  apply Nat.eq_of_testBit_eq
  intro k
  rw [byte, Nat.testBit_mod_two_pow, Nat.testBit_div_two_pow]
  by_cases hk : k < 8
  · simp only [hk, decide_true, Bool.true_and]
    rw [ARCFiniteCore.pack, Nat.testBit_mul_two_pow]
    by_cases hij : i = j
    · subst i
      simp
    · rw [ite_eq_right hij]
      by_cases hlt : i < j
      · have hpos : ¬8 * j ≤ k + 8 * i := by omega
        simp [hpos]
      · have hji : j < i := by omega
        have hdiff : 8 ≤ k + 8 * i - 8 * j := by omega
        have hpow : 2 ^ 8 ≤ 2 ^ (k + 8 * i - 8 * j) :=
          Nat.pow_le_pow_right (by decide) hdiff
        have hc' : c < 2 ^ (k + 8 * i - 8 * j) :=
          lt_of_lt_of_le (by simpa using hc) hpow
        rw [Nat.testBit_lt_two_pow hc']
        simp
  · simp only [hk, decide_false, Bool.false_and]
    split_ifs
    · exact (Nat.testBit_lt_two_pow
        (lt_of_lt_of_le (by simpa using hc)
          (Nat.pow_le_pow_right (by decide) (Nat.le_of_not_gt hk)))).symm
    · simp

noncomputable section

/-- Decode every allocated coordinate as a genuine F₂ polynomial.
This is a function on natural-number coordinates, not an algebra instance. -/
def decodeVec (code : Nat) : Nat → Polynomial (ZMod 2) :=
  fun i => decode (byte code i)

/-- Packed XOR denotes coordinatewise addition of actual F₂ polynomials. -/
theorem decodeVec_xor (a b : Nat) :
    decodeVec (Nat.xor a b) = decodeVec a + decodeVec b := by
  funext i
  exact (congrArg decode (byte_xor a b i)).trans (decode_xor (byte a i) (byte b i))

@[simp] theorem decodeVec_zero : decodeVec 0 = 0 := by
  funext i
  simp [decodeVec]

/-- A packed coefficient denotes one polynomial coordinate, without truncation. -/
theorem decodeVec_pack (j c : Nat) (hc : c < 256) :
    decodeVec (ARCFiniteCore.pack j c) = fun i => if i = j then decode c else 0 := by
  funext i
  dsimp [decodeVec]
  rw [byte_pack j c i hc]
  split_ifs <;> simp

#print axioms byte_xor
#print axioms byte_pack
#print axioms decodeVec_xor
#print axioms decodeVec_pack

end
end ARCBytePacking
