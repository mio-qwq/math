import CochainBasisSemantics
import TwentyDimAssociativity

/-!
# Every characteristic-two specialization of the radical-basis identities

The polynomial five-term identities are mapped through the existing ring
homomorphism `specialize q`. The algebra constants are the already defined
`specializedConstants q`; there is no replacement multiplication table.

The coefficient ring may have zero divisors and the parameter may be zero.
The conclusion retains the exact radical-basis scope of the polynomial
theorem. No relative Hochschild complex or Ext class is constructed here.
-/

namespace ARCCochainSpecialization

open ARCCochainBasisSemantics ARCTwentyDimAssociativity
open scoped BigOperators

noncomputable section

variable {R : Type*} [CommRing R] [CharP R 2]

/-- The genuine cochain coefficients after evaluation at the chosen parameter. -/
def specializedCochainConstants (q : R) (a b c k : Fin 20) : R :=
  specialize q (pConstants a b c k)

/-- The five-term finite contraction in the specialized coefficient ring. -/
def specializedFiveTermCoefficient (q : R) (a b c d k : Fin 20) : R :=
  (∑ j : Fin 20, specializedCochainConstants q b c d j * specializedConstants q a j k) +
    ((∑ j : Fin 20, specializedConstants q a b j * specializedCochainConstants q j c d k) +
      ((∑ j : Fin 20, specializedConstants q b c j * specializedCochainConstants q a j d k) +
        ((∑ j : Fin 20, specializedConstants q c d j * specializedCochainConstants q a b j k) +
          (∑ j : Fin 20, specializedCochainConstants q a b c j * specializedConstants q j d k))))

/-- Ring-homomorphic evaluation preserves every displayed finite contraction. -/
theorem specialize_fiveTermCoefficient (q : R) (a b c d k : Fin 20) :
    specialize q (fiveTermCoefficient a b c d k) =
      specializedFiveTermCoefficient q a b c d k := by
  simp only [fiveTermCoefficient, specializedFiveTermCoefficient,
    specializedCochainConstants, specializedConstants, map_add, map_sum, map_mul]

/-- Every radical-basis quadruple remains closed under every specialization. -/
theorem specialized_radical_basis_five_term_zero
    (q : R) (a b c d : Fin 18) (k : Fin 20) :
    specializedFiveTermCoefficient q (radicalBasis a) (radicalBasis b)
      (radicalBasis c) (radicalBasis d) k = 0 := by
  rw [← specialize_fiveTermCoefficient, radical_basis_five_term_zero, map_zero]

/-- Explicit five-term closure using the existing specialized algebra constants. -/
theorem specialized_radical_basis_closure
    (q : R) (a b c d : Fin 18) (k : Fin 20) :
    (∑ j : Fin 20,
      specializedCochainConstants q (radicalBasis b) (radicalBasis c) (radicalBasis d) j *
        specializedConstants q (radicalBasis a) j k) +
    ((∑ j : Fin 20, specializedConstants q (radicalBasis a) (radicalBasis b) j *
      specializedCochainConstants q j (radicalBasis c) (radicalBasis d) k) +
    ((∑ j : Fin 20, specializedConstants q (radicalBasis b) (radicalBasis c) j *
      specializedCochainConstants q (radicalBasis a) j (radicalBasis d) k) +
    ((∑ j : Fin 20, specializedConstants q (radicalBasis c) (radicalBasis d) j *
      specializedCochainConstants q (radicalBasis a) (radicalBasis b) j k) +
    (∑ j : Fin 20,
      specializedCochainConstants q (radicalBasis a) (radicalBasis b) (radicalBasis c) j *
        specializedConstants q j (radicalBasis d) k)))) = 0 :=
  specialized_radical_basis_five_term_zero q a b c d k

#print axioms specialize_fiveTermCoefficient
#print axioms specialized_radical_basis_five_term_zero
#print axioms specialized_radical_basis_closure

end
end ARCCochainSpecialization
