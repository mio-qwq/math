import FiniteFreeBarExtThree
import Mathlib.Algebra.Homology.DerivedCategory.Ext.EnoughProjectives
import Mathlib.Algebra.Homology.DerivedCategory.Ext.EnoughInjectives

/-!
# The actual f-character module has a nonzero third Ext obstruction

For every characteristic-two commutative ring, nonzero q cubed makes the
specified actual f-character module neither projective nor injective in
the actual module category of the twenty-dimensional table algebra.

Both obstructions use the previously proved nonzero actual Mathlib Ext
cubed class. This does not assert infinite homological dimension, a full
self-Ext profile or any obstruction for the final ARC algebra/module.
-/

namespace ARCTwentyDimCharacterHomologicalObstruction

open CategoryTheory CategoryTheory.Abelian
open ARCTwentyDimAlgebra ARCTwentyDimCharacters
open ARCFiniteFreeBarProjectiveResolution ARCFiniteFreeBarExtThree

universe u
variable {R : Type u} [CommRing R] [CharP R 2]

/-- The actual f-character object cannot be projective: projectivity
would annihilate the actual nonzero self-Ext cubed class. -/
theorem fCharacter_not_projective (q : R) (hq : q ^ 3 ≠ 0) :
    ¬ Projective (characterObject q (fCharacter q)) := by
  intro hp
  let : Projective (characterObject q (fCharacter q)) := hp
  exact fExtThree_ne_zero q hq (Ext.eq_zero_of_projective (fExtThree q))

/-- The actual f-character object cannot be injective: injectivity
would annihilate the same actual nonzero self-Ext cubed class. -/
theorem fCharacter_not_injective (q : R) (hq : q ^ 3 ≠ 0) :
    ¬ Injective (characterObject q (fCharacter q)) := by
  intro hi
  let : Injective (characterObject q (fCharacter q)) := hi
  exact fExtThree_ne_zero q hq (Ext.eq_zero_of_injective (fExtThree q))

/-- In a ring without zero divisors, nonzero q gives both actual
categorical obstructions, in particular over characteristic-two fields. -/
theorem fCharacter_neither_of_nonzero [NoZeroDivisors R] (q : R) (hq : q ≠ 0) :
    ¬ Projective (characterObject q (fCharacter q)) ∧
      ¬ Injective (characterObject q (fCharacter q)) :=
  ⟨fCharacter_not_projective q (pow_ne_zero 3 hq),
    fCharacter_not_injective q (pow_ne_zero 3 hq)⟩

#print axioms fCharacter_not_projective
#print axioms fCharacter_not_injective
#print axioms fCharacter_neither_of_nonzero

end ARCTwentyDimCharacterHomologicalObstruction
