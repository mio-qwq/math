import TracePairSemantics

/-!
Linearity, invariant pairing and cyclic triple trace for the actual
twenty-coordinate multiplication. Both polynomial and arbitrary
commutative characteristic-two specializations are covered. These use
the established associativity and symmetry, without new enumeration.
No algebra typeclass or homological construction is installed here.
-/

namespace ARCTraceInvariance

open ARCTwentyDimAssociativity ARCTracePairSemantics

noncomputable section

@[simp] theorem polynomial_trace_zero : polynomialTrace 0 = 0 := by
  simp [polynomialTrace]

theorem polynomial_trace_add (u v : PolynomialVector) :
    polynomialTrace (u + v) = polynomialTrace u + polynomialTrace v := by
  simp only [polynomialTrace, Pi.add_apply]
  ring

theorem polynomial_trace_smul (s : Polynomial (ZMod 2)) (u : PolynomialVector) :
    polynomialTrace (s • u) = s * polynomialTrace u := by
  simp only [polynomialTrace, Pi.smul_apply, smul_eq_mul, mul_add]

/-- The actual trace pairing, with the prescribed multiplication. -/
def polynomialPairing (u v : PolynomialVector) : Polynomial (ZMod 2) :=
  polynomialTrace (polynomialMul u v)

theorem polynomial_pairing_invariant (u v w : PolynomialVector) :
    polynomialPairing (polynomialMul u v) w = polynomialPairing u (polynomialMul v w) := by
  exact congrArg polynomialTrace (polynomial_mul_associative u v w)

/-- Cyclic rotation of three factors preserves their actual polynomial trace. -/
theorem polynomial_trace_cyclic (u v w : PolynomialVector) :
    polynomialTrace (polynomialMul (polynomialMul u v) w) =
      polynomialTrace (polynomialMul (polynomialMul v w) u) := by
  rw [polynomial_mul_associative, polynomial_trace_symmetric u (polynomialMul v w)]

variable {R : Type*} [CommRing R]

@[simp] theorem specialized_trace_zero : specializedTrace (0 : Fin 20 → R) = 0 := by
  simp [specializedTrace]

theorem specialized_trace_add (u v : Fin 20 → R) :
    specializedTrace (u + v) = specializedTrace u + specializedTrace v := by
  simp only [specializedTrace, Pi.add_apply]
  ring

theorem specialized_trace_smul (s : R) (u : Fin 20 → R) :
    specializedTrace (s • u) = s * specializedTrace u := by
  simp only [specializedTrace, Pi.smul_apply, smul_eq_mul, mul_add]

variable [CharP R 2]

def specializedPairing (q : R) (u v : Fin 20 → R) : R :=
  specializedTrace (specializedMul q u v)

theorem specialized_pairing_invariant (q : R) (u v w : Fin 20 → R) :
    specializedPairing q (specializedMul q u v) w =
      specializedPairing q u (specializedMul q v w) := by
  exact congrArg specializedTrace (specialized_mul_associative q u v w)

/-- Every characteristic-two specialization has the same cyclic trace law. -/
theorem specialized_trace_cyclic (q : R) (u v w : Fin 20 → R) :
    specializedTrace (specializedMul q (specializedMul q u v) w) =
      specializedTrace (specializedMul q (specializedMul q v w) u) := by
  rw [specialized_mul_associative, specialized_trace_symmetric q u (specializedMul q v w)]

#print axioms polynomial_trace_add
#print axioms polynomial_trace_smul
#print axioms polynomial_pairing_invariant
#print axioms polynomial_trace_cyclic
#print axioms specialized_trace_add
#print axioms specialized_trace_smul
#print axioms specialized_pairing_invariant
#print axioms specialized_trace_cyclic

end
end ARCTraceInvariance
