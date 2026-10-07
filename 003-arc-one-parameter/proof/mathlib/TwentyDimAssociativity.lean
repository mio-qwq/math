import FiniteTableContraction
import FiniteBilinear
import Mathlib.Algebra.Polynomial.Eval.Defs

/-!
Associativity on every vector of the actual twenty-coordinate table.
The polynomial structure constants come from the attributed fixed table,
through the frozen exact certificates and their semantic bridges.
Specialization works in every commutative characteristic-two ring.
This file does not install an algebra instance, prove the unit/trace laws,
or construct Hochschild/Ext objects or the complete ARC realization.
-/

namespace ARCTwentyDimAssociativity

open ARCFiniteTableContraction ARCFiniteBilinear
open scoped BigOperators

noncomputable section

abbrev PolynomialVector := Fin 20 → Polynomial (ZMod 2)

def polynomialMul (u v : PolynomialVector) : PolynomialVector :=
  ARCFiniteBilinear.mul tConstants u v

/-- The table's actual polynomial constants satisfy the required premise. -/
theorem polynomial_structure_associative : StructureAssociative tConstants :=
  fun a b c k => t_structure_constants_associativity a b c k

/-- All vectors, with arbitrary polynomial coefficients, have associativity. -/
theorem polynomial_mul_associative (u v w : PolynomialVector) :
    polynomialMul (polynomialMul u v) w = polynomialMul u (polynomialMul v w) :=
  mul_associative tConstants polynomial_structure_associative u v w

variable {R : Type*} [CommRing R] [CharP R 2]

/-- The canonical coefficient map and evaluation at the chosen parameter. -/
def specialize (q : R) : Polynomial (ZMod 2) →+* R :=
  Polynomial.eval₂RingHom (ZMod.castHom (dvd_refl 2) R) q

def specializedConstants (q : R) (a b k : Fin 20) : R :=
  specialize q (tConstants a b k)

def specializedMul (q : R) (u v : Fin 20 → R) : Fin 20 → R :=
  ARCFiniteBilinear.mul (specializedConstants q) u v

/-- Specialization preserves the finite table's contraction identities. -/
theorem specialized_structure_associative (q : R) :
    StructureAssociative (specializedConstants q) := by
  intro a b c k
  have h := congrArg (specialize q) (t_structure_constants_associativity a b c k)
  simpa only [map_sum, map_mul, specializedConstants] using h

/-- Every characteristic-two specialization is associative on all vectors. -/
theorem specialized_mul_associative (q : R) (u v w : Fin 20 → R) :
    specializedMul q (specializedMul q u v) w =
      specializedMul q u (specializedMul q v w) :=
  mul_associative (specializedConstants q) (specialized_structure_associative q) u v w

#print axioms polynomial_structure_associative
#print axioms polynomial_mul_associative
#print axioms specialized_structure_associative
#print axioms specialized_mul_associative

end
end ARCTwentyDimAssociativity
