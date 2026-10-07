import TwentyDimAssociativity
import FiniteBilinearUnit
import ScalarEvaluation
import CochainData

/-!
# The actual twenty-coordinate unit

The frozen packed certificate for `e + f` is transported to genuine
polynomial vectors, using the independently certified coefficient bound.
Generic finite contraction lemmas then extend both unit actions to all
vectors. No new enumeration or algebra instance is introduced.
-/

namespace ARCTwentyDimUnit

open ARCFiniteCore ARCBitPolynomial ARCBytePacking ARCTermSemantics
open ARCFiniteTableContraction ARCTwentyDimAssociativity ARCFiniteBilinear

open scoped BigOperators

noncomputable section

private theorem table_coefficient_byte_bound (a b : Fin 20) :
    ∀ term ∈ tTerms a.val b.val, term.2 < 256 := by
  have h : ∀ term ∈ tTerms a.val b.val, term.2 < 16 := by
    simpa only [List.all_eq_true, decide_eq_true_eq] using t_coefficient_bound a b
  intro term ht
  exact Nat.lt_trans (h term ht) (by omega)

/-- The actual polynomial-vector unit is the sum of coordinates e and f. -/
def polynomialUnit : PolynomialVector :=
  fun i => (if i = 0 then 1 else 0) + (if i = 8 then 1 else 0)

/-- The frozen left unit action now holds in genuine polynomial coefficients. -/
theorem polynomial_left_basis_unit (b k : Fin 20) :
    tConstants 0 b k + tConstants 8 b k = if b = k then 1 else 0 := by
  have h0 : ∀ term ∈ tTerms 0 b.val, term.2 < 256 := by
    simpa using table_coefficient_byte_bound 0 b
  have h8 : ∀ term ∈ tTerms 8 b.val, term.2 < 256 := by
    simpa using table_coefficient_byte_bound 8 b
  have h := congrArg decodeVec (t_unit_actions b).1
  rw [decodeVec_xor, decode_encode _ h0, decode_encode _ h8,
    decodeVec_pack b.val 1 (by omega)] at h
  have hk := congrArg (fun v : PolyVector => v k.val) h
  change tConstants 0 b k + tConstants 8 b k =
    if k.val = b.val then decode 1 else 0 at hk
  simpa only [ARCScalarEvaluation.decode_one, Fin.val_inj, eq_comm] using hk

/-- The independent right unit action is transported through the same semantics. -/
theorem polynomial_right_basis_unit (a k : Fin 20) :
    tConstants a 0 k + tConstants a 8 k = if a = k then 1 else 0 := by
  have h0 : ∀ term ∈ tTerms a.val 0, term.2 < 256 := by
    simpa using table_coefficient_byte_bound a 0
  have h8 : ∀ term ∈ tTerms a.val 8, term.2 < 256 := by
    simpa using table_coefficient_byte_bound a 8
  have h := congrArg decodeVec (t_unit_actions a).2
  rw [decodeVec_xor, decode_encode _ h0, decode_encode _ h8,
    decodeVec_pack a.val 1 (by omega)] at h
  have hk := congrArg (fun v : PolyVector => v k.val) h
  change tConstants a 0 k + tConstants a 8 k =
    if k.val = a.val then decode 1 else 0 at hk
  simpa only [ARCScalarEvaluation.decode_one, Fin.val_inj, eq_comm] using hk

theorem polynomial_structure_left_unit : StructureLeftUnit tConstants polynomialUnit := by
  intro b k
  simp_rw [polynomialUnit, add_mul, ite_mul, one_mul, zero_mul]
  rw [Finset.sum_add_distrib]
  simpa using polynomial_left_basis_unit b k

theorem polynomial_structure_right_unit : StructureRightUnit tConstants polynomialUnit := by
  intro a k
  simp_rw [polynomialUnit, add_mul, ite_mul, one_mul, zero_mul]
  rw [Finset.sum_add_distrib]
  simpa using polynomial_right_basis_unit a k

/-- e+f is a left identity for every actual twenty-coordinate polynomial vector. -/
theorem polynomial_left_unit (v : PolynomialVector) :
    polynomialMul polynomialUnit v = v :=
  mul_left_unit tConstants polynomialUnit polynomial_structure_left_unit v

/-- e+f is a right identity for every actual twenty-coordinate polynomial vector. -/
theorem polynomial_right_unit (v : PolynomialVector) :
    polynomialMul v polynomialUnit = v :=
  mul_right_unit tConstants polynomialUnit polynomial_structure_right_unit v

variable {R : Type*} [CommRing R] [CharP R 2]

/-- Specialize the proved polynomial unit by the same map as the multiplication. -/
def specializedUnit (q : R) : Fin 20 → R :=
  fun i => specialize q (polynomialUnit i)

theorem specialized_unit_coordinates (q : R) (i : Fin 20) :
    specializedUnit q i = (if i = 0 then 1 else 0) + (if i = 8 then 1 else 0) := by
  simp [specializedUnit, polynomialUnit]

theorem specialized_structure_left_unit (q : R) :
    StructureLeftUnit (specializedConstants q) (specializedUnit q) := by
  intro b k
  have h := congrArg (specialize q) (polynomial_structure_left_unit b k)
  simpa only [map_sum, map_mul, apply_ite, map_one, map_zero,
    specializedConstants, specializedUnit] using h

theorem specialized_structure_right_unit (q : R) :
    StructureRightUnit (specializedConstants q) (specializedUnit q) := by
  intro a k
  have h := congrArg (specialize q) (polynomial_structure_right_unit a k)
  simpa only [map_sum, map_mul, apply_ite, map_one, map_zero,
    specializedConstants, specializedUnit] using h

/-- e+f remains a left identity for every characteristic-two specialization. -/
theorem specialized_left_unit (q : R) (v : Fin 20 → R) :
    specializedMul q (specializedUnit q) v = v :=
  mul_left_unit (specializedConstants q) (specializedUnit q)
    (specialized_structure_left_unit q) v

/-- e+f remains a right identity for every characteristic-two specialization. -/
theorem specialized_right_unit (q : R) (v : Fin 20 → R) :
    specializedMul q v (specializedUnit q) = v :=
  mul_right_unit (specializedConstants q) (specializedUnit q)
    (specialized_structure_right_unit q) v

#print axioms polynomial_left_basis_unit
#print axioms polynomial_right_basis_unit
#print axioms polynomial_left_unit
#print axioms polynomial_right_unit
#print axioms specialized_unit_coordinates
#print axioms specialized_structure_left_unit
#print axioms specialized_structure_right_unit
#print axioms specialized_left_unit
#print axioms specialized_right_unit

end
end ARCTwentyDimUnit
