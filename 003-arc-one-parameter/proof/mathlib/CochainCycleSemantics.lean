import CochainData
import TwentyDimAssociativity
import ScalarEvaluation
import Mathlib.Algebra.CharP.Two

/-!
The concrete two-word internal bar cycle is a universal separating
functional for scalar internal coboundaries of the actual table.
Its value on coordinate f of the fixed cochain is X^3, nonzero over F₂[X].
Specialization gives q^3 and preserves this obstruction when q^3 is nonzero.
This does not identify the scalar internal differential with a complete
Hochschild or Ext complex, or prove the complete ARC realization.
-/

namespace ARCCochainCycleSemantics

open ARCFiniteCore ARCBitPolynomial ARCBytePacking ARCTermSemantics
open ARCFiniteTableContraction ARCTwentyDimAssociativity ARCScalarEvaluation
open scoped BigOperators

noncomputable section

set_option maxHeartbeats 1000000

abbrev Poly := Polynomial (ZMod 2)
abbrev ScalarTwoCoChain (R : Type*) := Fin 20 → Fin 20 → R
abbrev ScalarThreeCoChain (R : Type*) := Fin 20 → Fin 20 → Fin 20 → R

private theorem decode_four : decode 4 = (Polynomial.X : Poly) ^ 2 := by
  have h := decode_double 2
  rw [show 2 * 2 = (4 : Nat) by decide] at h
  rw [show decode 2 = (Polynomial.X : Poly) by
    simpa only [Nat.mul_one, decode_one, mul_one] using decode_double 1] at h
  simpa only [pow_two] using h

private theorem decode_eight : decode 8 = (Polynomial.X : Poly) ^ 3 := by
  have h := decode_double 4
  rw [show 2 * 4 = (8 : Nat) by decide, decode_four] at h
  simpa only [pow_succ, mul_comm] using h

/-- The f coordinate of the fixed 179-entry polynomial cochain. -/
def fCoordinate (a b c : Fin 20) : Poly := sumTerms (pTerms a.val b.val c.val) 8

/-- Pair a scalar three-cochain with X²[t|x|J]+[t|y|J]. -/
def polynomialCyclePairing (F : ScalarThreeCoChain Poly) : Poly :=
  Polynomial.X ^ 2 * F 6 1 17 + F 6 2 17

/-- The frozen encoded cycle pairing transports to the actual polynomial scalar. -/
theorem polynomial_cycle_pairing : polynomialCyclePairing fCoordinate = Polynomial.X ^ 3 := by
  have hterms1 : pTerms 6 1 17 = [] := rfl
  have hterms2 : pTerms 6 2 17 = [(8, 8)] := rfl
  have hp1 : ∀ term ∈ pTerms 6 1 17, pMul 4 term.2 < 256 := by
    rw [hterms1]
    simp
  have hp2 : ∀ term ∈ pTerms 6 2 17, term.2 < 256 := by
    rw [hterms2]
    simp
  have h := congrArg decodeVec cycle_pairing
  rw [decodeVec_xor, decode_scaleEncode 4 (pTerms 6 1 17) hp1,
    decode_encode (pTerms 6 2 17) hp2, decodeVec_pack 8 8 (by decide)] at h
  have hc := congrArg (fun v : PolyVector => v 8) h
  change decode 4 * sumTerms (pTerms 6 1 17) 8 + sumTerms (pTerms 6 2 17) 8 = decode 8 at hc
  change Polynomial.X ^ 2 * sumTerms (pTerms 6 1 17) 8 + sumTerms (pTerms 6 2 17) 8 =
    Polynomial.X ^ 3
  simpa only [decode_four, decode_eight] using hc

theorem polynomial_cycle_pairing_nonzero : polynomialCyclePairing fCoordinate ≠ 0 := by
  rw [polynomial_cycle_pairing]
  intro hzero
  have h := congrArg (fun p : Poly => p.coeff 3) hzero
  simp at h

/-- The two internal scalar faces, using the actual finite structure constants. -/
def scalarInternalD2 {R : Type*} [CommSemiring R] (B : Fin 20 → Fin 20 → Fin 20 → R)
    (G : ScalarTwoCoChain R) : ScalarThreeCoChain R :=
  fun a b c => (∑ j : Fin 20, B a b j * G j c) + ∑ j : Fin 20, B b c j * G a j

private theorem tx_constants (j : Fin 20) : tConstants 6 1 j = if j = 7 then 1 else 0 := by
  change sumTerms (tTerms 6 1) j.val = if j = 7 then 1 else 0
  rw [show tTerms 6 1 = [(7, 1)] by rfl]
  simp [sumTerms, singleTerm, decode_one, Fin.ext_iff]

private theorem ty_constants (j : Fin 20) :
    tConstants 6 2 j = if j = 7 then (Polynomial.X : Poly) ^ 2 else 0 := by
  change sumTerms (tTerms 6 2) j.val = if j = 7 then Polynomial.X ^ 2 else 0
  rw [show tTerms 6 2 = [(7, 4)] by rfl]
  simp [sumTerms, singleTerm, decode_four, Fin.ext_iff]

private theorem xJ_constants (j : Fin 20) : tConstants 1 17 j = if j = 16 then 1 else 0 := by
  change sumTerms (tTerms 1 17) j.val = if j = 16 then 1 else 0
  rw [show tTerms 1 17 = [(16, 1)] by rfl]
  simp [sumTerms, singleTerm, decode_one, Fin.ext_iff]

private theorem yJ_constants (j : Fin 20) :
    tConstants 2 17 j = if j = 16 then (Polynomial.X : Poly) ^ 2 else 0 := by
  change sumTerms (tTerms 2 17) j.val = if j = 16 then Polynomial.X ^ 2 else 0
  rw [show tTerms 2 17 = [(16, 4)] by rfl]
  simp [sumTerms, singleTerm, decode_four, Fin.ext_iff]

private theorem internalD2_txJ (G : ScalarTwoCoChain Poly) :
    scalarInternalD2 tConstants G 6 1 17 = G 7 17 + G 6 16 := by
  simp [scalarInternalD2, tx_constants, xJ_constants]

private theorem internalD2_tyJ (G : ScalarTwoCoChain Poly) :
    scalarInternalD2 tConstants G 6 2 17 =
      Polynomial.X ^ 2 * G 7 17 + Polynomial.X ^ 2 * G 6 16 := by
  simp [scalarInternalD2, ty_constants, yJ_constants]

/-- The cycle functional annihilates every scalar internal two-coboundary. -/
theorem polynomial_cycle_annihilates_internalD2 (G : ScalarTwoCoChain Poly) :
    polynomialCyclePairing (scalarInternalD2 tConstants G) = 0 := by
  rw [polynomialCyclePairing, internalD2_txJ, internalD2_tyJ, mul_add]
  rw [← add_assoc, add_assoc (Polynomial.X ^ 2 * G 7 17),
    add_comm (Polynomial.X ^ 2 * G 6 16) (Polynomial.X ^ 2 * G 7 17),
    ← add_assoc, CharTwo.add_self_eq_zero, zero_add, CharTwo.add_self_eq_zero]

/-- Even agreement on the two radical triples of the cycle is impossible. -/
theorem polynomial_fCoordinate_no_cycle_interpolation :
    ¬ ∃ G : ScalarTwoCoChain Poly,
      scalarInternalD2 tConstants G 6 1 17 = fCoordinate 6 1 17 ∧
      scalarInternalD2 tConstants G 6 2 17 = fCoordinate 6 2 17 := by
  rintro ⟨G, hx, hy⟩
  have hzero := polynomial_cycle_annihilates_internalD2 G
  change Polynomial.X ^ 2 * scalarInternalD2 tConstants G 6 1 17 +
    scalarInternalD2 tConstants G 6 2 17 = 0 at hzero
  rw [hx, hy] at hzero
  exact polynomial_cycle_pairing_nonzero hzero

/-- The f coordinate is not an internal scalar two-coboundary. -/
theorem polynomial_fCoordinate_not_internal_coboundary :
    ¬ ∃ G : ScalarTwoCoChain Poly, scalarInternalD2 tConstants G = fCoordinate := by
  rintro ⟨G, hG⟩
  have hzero := polynomial_cycle_annihilates_internalD2 G
  rw [hG] at hzero
  exact polynomial_cycle_pairing_nonzero hzero

variable {R : Type*} [CommRing R] [CharP R 2]

def specializedFCoordinate (q : R) : ScalarThreeCoChain R :=
  fun a b c => specialize q (fCoordinate a b c)

def specializedCyclePairing (q : R) (F : ScalarThreeCoChain R) : R :=
  q ^ 2 * F 6 1 17 + F 6 2 17

/-- The same actual scalar cycle pairs to q³ in every specialization. -/
theorem specialized_cycle_pairing (q : R) :
    specializedCyclePairing q (specializedFCoordinate q) = q ^ 3 := by
  have h := congrArg (specialize q) polynomial_cycle_pairing
  simpa [polynomialCyclePairing, specializedCyclePairing, specializedFCoordinate,
    specialize, Polynomial.eval₂_X_pow] using h

/-- A nonzero parameter over a domain makes the actual specialized pairing nonzero. -/
theorem specialized_cycle_pairing_nonzero [NoZeroDivisors R] (q : R) (hq : q ≠ 0) :
    specializedCyclePairing q (specializedFCoordinate q) ≠ 0 := by
  rw [specialized_cycle_pairing]
  exact pow_ne_zero 3 hq

/-- Specializing the four actual structure constants gives the same cycle cancellation. -/
theorem specialized_cycle_annihilates_internalD2 (q : R) (G : ScalarTwoCoChain R) :
    specializedCyclePairing q (scalarInternalD2 (specializedConstants q) G) = 0 := by
  have htx : ∀ j, specializedConstants q 6 1 j = if j = 7 then 1 else 0 := by
    intro j
    have h := congrArg (specialize q) (tx_constants j)
    split_ifs at h ⊢ <;> simpa only [specializedConstants, map_one, map_zero] using h
  have hty : ∀ j, specializedConstants q 6 2 j = if j = 7 then q ^ 2 else 0 := by
    intro j
    have h := congrArg (specialize q) (ty_constants j)
    split_ifs at h ⊢ <;> simpa [specializedConstants, specialize, Polynomial.eval₂_X_pow] using h
  have hxJ : ∀ j, specializedConstants q 1 17 j = if j = 16 then 1 else 0 := by
    intro j
    have h := congrArg (specialize q) (xJ_constants j)
    split_ifs at h ⊢ <;> simpa only [specializedConstants, map_one, map_zero] using h
  have hyJ : ∀ j, specializedConstants q 2 17 j = if j = 16 then q ^ 2 else 0 := by
    intro j
    have h := congrArg (specialize q) (yJ_constants j)
    split_ifs at h ⊢ <;> simpa [specializedConstants, specialize, Polynomial.eval₂_X_pow] using h
  simp only [specializedCyclePairing, scalarInternalD2, htx, hty, hxJ, hyJ]
  simp only [ite_mul, one_mul, zero_mul, Finset.sum_ite_eq', Finset.mem_univ, ite_true]
  rw [mul_add]
  rw [← add_assoc, add_assoc (q ^ 2 * G 7 17), add_comm (q ^ 2 * G 6 16) (q ^ 2 * G 7 17),
    ← add_assoc, CharTwo.add_self_eq_zero, zero_add, CharTwo.add_self_eq_zero]

/-- The obstruction already applies to just the cycle's two radical triples. -/
theorem specialized_fCoordinate_no_cycle_interpolation (q : R) (hq : q ^ 3 ≠ 0) :
    ¬ ∃ G : ScalarTwoCoChain R,
      scalarInternalD2 (specializedConstants q) G 6 1 17 = specializedFCoordinate q 6 1 17 ∧
      scalarInternalD2 (specializedConstants q) G 6 2 17 = specializedFCoordinate q 6 2 17 := by
  rintro ⟨G, hx, hy⟩
  have hzero := specialized_cycle_annihilates_internalD2 q G
  change q ^ 2 * scalarInternalD2 (specializedConstants q) G 6 1 17 +
    scalarInternalD2 (specializedConstants q) G 6 2 17 = 0 at hzero
  rw [hx, hy] at hzero
  change specializedCyclePairing q (specializedFCoordinate q) = 0 at hzero
  rw [specialized_cycle_pairing] at hzero
  exact hq hzero

/-- A nonzero q³ separates the specialized f coordinate from all internal coboundaries. -/
theorem specialized_fCoordinate_not_internal_coboundary (q : R) (hq : q ^ 3 ≠ 0) :
    ¬ ∃ G : ScalarTwoCoChain R,
      scalarInternalD2 (specializedConstants q) G = specializedFCoordinate q := by
  rintro ⟨G, hG⟩
  have hzero := specialized_cycle_annihilates_internalD2 q G
  rw [hG, specialized_cycle_pairing] at hzero
  exact hq hzero

/-- In every characteristic-two domain, any nonzero parameter supplies the obstruction. -/
theorem specialized_fCoordinate_not_internal_coboundary_of_nonzero
    [NoZeroDivisors R] (q : R) (hq : q ≠ 0) :
    ¬ ∃ G : ScalarTwoCoChain R,
      scalarInternalD2 (specializedConstants q) G = specializedFCoordinate q :=
  specialized_fCoordinate_not_internal_coboundary q (pow_ne_zero 3 hq)

#print axioms polynomial_cycle_pairing
#print axioms polynomial_cycle_pairing_nonzero
#print axioms polynomial_cycle_annihilates_internalD2
#print axioms polynomial_fCoordinate_no_cycle_interpolation
#print axioms polynomial_fCoordinate_not_internal_coboundary
#print axioms specialized_cycle_pairing
#print axioms specialized_cycle_pairing_nonzero
#print axioms specialized_cycle_annihilates_internalD2
#print axioms specialized_fCoordinate_no_cycle_interpolation
#print axioms specialized_fCoordinate_not_internal_coboundary
#print axioms specialized_fCoordinate_not_internal_coboundary_of_nonzero

end
end ARCCochainCycleSemantics
