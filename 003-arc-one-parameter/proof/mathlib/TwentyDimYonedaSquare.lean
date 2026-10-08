import FiniteFreeBarCupShift
import TwentyDimCupSquareWitness
import TwentyDimDualScaleYoneda

/-!
The constructed whole shifted cup lift identifies the actual Yoneda
square, and the explicit q^4 witness makes that square nonzero.
No assertion about all higher powers or a full Ext profile is made.
-/

namespace ARCTwentyDimYonedaSquare

open CategoryTheory CategoryTheory.Abelian
open ARCTwentyDimCharacters ARCFiniteFreeBarExtThree
open ARCTwentyDimCupSquareWitness ARCTwentyDimDualScaleYoneda

noncomputable section
universe u
variable {R : Type u} [CommRing R] [CharP R 2]

/-- Identification uses the constructed whole shifted resolution lift. -/
theorem fExtThree_square_eq (q : R) :
    (fExtThree q).comp (fExtThree q) (show 3 + 3 = 6 by rfl) = fCupExtSix q :=
  ARCFiniteFreeBarCupShift.fExtThree_comp_self q

/-- The genuine Yoneda square is detected by the explicit q^4 witness. -/
theorem fExtThree_square_ne_zero (q : R) (hq : q ^ 4 ≠ 0) :
    (fExtThree q).comp (fExtThree q) (show 3 + 3 = 6 by rfl) ≠ 0 := by
  rw [fExtThree_square_eq]
  exact fCupExtSix_ne_zero q hq

theorem fExtThree_square_ne_zero_of_nonzero [NoZeroDivisors R]
    (q : R) (hq : q ≠ 0) :
    (fExtThree q).comp (fExtThree q) (show 3 + 3 = 6 by rfl) ≠ 0 :=
  fExtThree_square_ne_zero q (pow_ne_zero 4 hq)

/-- The previously defined second power is this actual nonzero cup class. -/
theorem fYonedaPower_two_eq (q : R) : fYonedaPower q 2 = fCupExtSix q := by
  change (fYonedaPower q 1).comp (fExtThree q) (show 3 + 3 = 6 by rfl) = fCupExtSix q
  rw [fYonedaPower_one]
  exact fExtThree_square_eq q

theorem fYonedaPower_two_ne_zero (q : R) (hq : q ^ 4 ≠ 0) :
    fYonedaPower q 2 ≠ 0 := by
  rw [fYonedaPower_two_eq]
  exact fCupExtSix_ne_zero q hq

#print axioms fExtThree_square_eq
#print axioms fExtThree_square_ne_zero
#print axioms fExtThree_square_ne_zero_of_nonzero
#print axioms fYonedaPower_two_eq
#print axioms fYonedaPower_two_ne_zero

end
end ARCTwentyDimYonedaSquare
