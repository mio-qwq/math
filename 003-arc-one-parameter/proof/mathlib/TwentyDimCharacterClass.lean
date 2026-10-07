import TwentyDimCharacters
import CharacterHochschildDegreeThree

/-!
# A nonzero full degree-three class for the actual f character

The scalar cochain is the f-character projection of the attributed actual
algebra cochain. Every scalar-valued bilinear cochain is excluded as a
boundary by the two-triple cycle functional. Thus its class is nonzero in
the full character-cochain kernel/image quotient whenever q³ is nonzero.

No bar resolution, module-resolution exactness, comparison with Ext, or
all-degree ARC assertion is made. In a ring with zero divisors the exact
witness hypothesis remains q³ ≠ 0; q ≠ 0 suffices over a domain.
-/

namespace ARCTwentyDimCharacterClass

open ARCTwentyDimAlgebra ARCTwentyDimCochainAlgebra ARCTwentyDimCharacters
open ARCTwentyDimAssociativity ARCCochainCycleSemantics
open ARCCharacterHochschildMaps
open scoped BigOperators

variable {R : Type*} [CommRing R] [CharP R 2]

noncomputable section

variable (q : R)

/-- All scalar-valued bilinear cochains have actual, unrestricted basis values. -/
def scalarBilinearBasisValues (G : C2S R (TableAlgebra q)) : ScalarTwoCoChain R :=
  fun a b => G (coordinateBasis q a) (coordinateBasis q b)

/-- First-slot expansion of an arbitrary actual scalar-valued bilinear map. -/
theorem scalar_bilinear_first_expansion (G : C2S R (TableAlgebra q))
    (x y : TableAlgebra q) :
    G x y = ∑ i : Fin 20, x.coords i • G (coordinateBasis q i) y := by
  conv_lhs => rw [basis_expansion q x]
  simp only [map_sum, map_smul, LinearMap.sum_apply, LinearMap.smul_apply]

/-- Second-slot expansion, with no extension assumption on the scalar map. -/
theorem scalar_bilinear_second_expansion (G : C2S R (TableAlgebra q))
    (x y : TableAlgebra q) :
    G x y = ∑ i : Fin 20, y.coords i • G x (coordinateBasis q i) := by
  conv_lhs => rw [basis_expansion q y]
  simp only [map_sum, map_smul]

/-- On the cycle triples the character outer faces vanish. The remaining
two faces are the exact finite internal contraction for the scalar map's
own basis values, for every actual scalar-valued bilinear cochain. -/
theorem character_d2_cycle_basis (G : C2S R (TableAlgebra q)) (b : Fin 20) :
    d2 (fCharacter q) G (coordinateBasis q 6) (coordinateBasis q b)
      (coordinateBasis q 17) =
      scalarInternalD2 (specializedConstants q) (scalarBilinearBasisValues q G) 6 b 17 := by
  have hfirst := scalar_bilinear_first_expansion q G
    (coordinateBasis q 6 * coordinateBasis q b) (coordinateBasis q 17)
  rw [coordinateBasis_mul_coords] at hfirst
  have hsecond := scalar_bilinear_second_expansion q G
    (coordinateBasis q 6) (coordinateBasis q b * coordinateBasis q 17)
  rw [coordinateBasis_mul_coords] at hsecond
  rw [d2_apply]
  simp only [ARCCharacterHochschildMaps.differential2, fCharacter_basis,
    show (6 : Fin 20) ≠ 8 by decide, show (17 : Fin 20) ≠ 8 by decide,
    ite_false, zero_mul, mul_zero, zero_add, add_zero]
  rw [hfirst, hsecond]
  simp only [scalarInternalD2, scalarBilinearBasisValues, smul_eq_mul]

/-- The actual two-triple cycle annihilates every full character boundary. -/
theorem character_boundary_cycle_zero (G : C2S R (TableAlgebra q)) :
    q ^ 2 * d2 (fCharacter q) G (coordinateBasis q 6) (coordinateBasis q 1)
        (coordinateBasis q 17) +
      d2 (fCharacter q) G (coordinateBasis q 6) (coordinateBasis q 2)
        (coordinateBasis q 17) = 0 := by
  rw [character_d2_cycle_basis, character_d2_cycle_basis]
  exact specialized_cycle_annihilates_internalD2 q (scalarBilinearBasisValues q G)

/-- Even interpolation on just the two actual cycle triples is impossible
for every scalar-valued bilinear cochain when the cube witness is nonzero. -/
theorem actualfSimpleP_no_character_boundary_interpolation (hq : q ^ 3 ≠ 0) :
    ¬ ∃ G : C2S R (TableAlgebra q),
      d2 (fCharacter q) G (coordinateBasis q 6) (coordinateBasis q 1)
        (coordinateBasis q 17) =
        actualfSimpleP q (coordinateBasis q 6) (coordinateBasis q 1)
          (coordinateBasis q 17) ∧
      d2 (fCharacter q) G (coordinateBasis q 6) (coordinateBasis q 2)
        (coordinateBasis q 17) =
        actualfSimpleP q (coordinateBasis q 6) (coordinateBasis q 2)
          (coordinateBasis q 17) := by
  rintro ⟨G, hx, hy⟩
  have hzero := character_boundary_cycle_zero q G
  rw [hx, hy, actualfSimpleP_cycle_pairing] at hzero
  exact hq hzero

/-- The projected scalar cochain is not the full character boundary of
any actual scalar-valued bilinear map. This is proved independently of
the earlier vector-valued nonboundary statement. -/
theorem actualfSimpleP_not_character_boundary (hq : q ^ 3 ≠ 0) :
    ¬ ∃ G : C2S R (TableAlgebra q), d2 (fCharacter q) G = actualfSimpleP q := by
  rintro ⟨G, hG⟩
  apply actualfSimpleP_no_character_boundary_interpolation q hq
  refine ⟨G, ?_, ?_⟩
  · exact congrArg (fun F => F (coordinateBasis q 6) (coordinateBasis q 1)
      (coordinateBasis q 17)) hG
  · exact congrArg (fun F => F (coordinateBasis q 6) (coordinateBasis q 2)
      (coordinateBasis q 17)) hG

/-- Full-input closure as an equality of actual four-linear scalar cochains. -/
theorem actualfSimpleP_d3_zero : d3 (fCharacter q) (actualfSimpleP q) = 0 := by
  apply LinearMap.ext
  intro x
  apply LinearMap.ext
  intro y
  apply LinearMap.ext
  intro z
  apply LinearMap.ext
  intro w
  exact actualfSimpleP_character_closed q x y z w

-- Match the standard nested additive groups used by the quotient, one
-- layer at a time; no new mathematical assumptions are introduced.
local instance scalarCochain1Group : AddCommGroup (TableAlgebra q →ₗ[R] R) :=
  LinearMap.addCommGroup
local instance scalarCochain2Group : AddCommGroup (C2S R (TableAlgebra q)) :=
  LinearMap.addCommGroup
local instance scalarCochain3Group : AddCommGroup (C3S R (TableAlgebra q)) :=
  LinearMap.addCommGroup
local instance scalarCochain4Group : AddCommGroup (C4S R (TableAlgebra q)) :=
  LinearMap.addCommGroup

/-- The actual full degree-three class for the actual f character. -/
def fCharacterClass : ARCCharacterHochschildDegreeThree.H3 (fCharacter q) :=
  ARCCharacterHochschildDegreeThree.classOf (fCharacter q) (actualfSimpleP q)
    (actualfSimpleP_d3_zero q)

/-- The cube pairing witness proves that this full scalar class is nonzero. -/
theorem fCharacterClass_ne_zero (hq : q ^ 3 ≠ 0) : fCharacterClass q ≠ 0 :=
  ARCCharacterHochschildDegreeThree.classOf_ne_zero (fCharacter q) (actualfSimpleP q)
    (actualfSimpleP_d3_zero q) (actualfSimpleP_not_character_boundary q hq)

theorem fCharacterClass_ne_zero_of_nonzero [NoZeroDivisors R] (hq : q ≠ 0) :
    fCharacterClass q ≠ 0 :=
  fCharacterClass_ne_zero q (pow_ne_zero 3 hq)

/-- The full scalar character cochain quotient is genuinely nontrivial. -/
theorem fCharacter_h3_nontrivial (hq : q ^ 3 ≠ 0) :
    Nontrivial (ARCCharacterHochschildDegreeThree.H3 (fCharacter q)) :=
  ⟨⟨fCharacterClass q, 0, fCharacterClass_ne_zero q hq⟩⟩

theorem fCharacter_h3_nontrivial_of_nonzero [NoZeroDivisors R] (hq : q ≠ 0) :
    Nontrivial (ARCCharacterHochschildDegreeThree.H3 (fCharacter q)) :=
  fCharacter_h3_nontrivial q (pow_ne_zero 3 hq)

#print axioms character_d2_cycle_basis
#print axioms character_boundary_cycle_zero
#print axioms actualfSimpleP_no_character_boundary_interpolation
#print axioms actualfSimpleP_not_character_boundary
#print axioms actualfSimpleP_d3_zero
#print axioms fCharacterClass
#print axioms fCharacterClass_ne_zero
#print axioms fCharacterClass_ne_zero_of_nonzero
#print axioms fCharacter_h3_nontrivial
#print axioms fCharacter_h3_nontrivial_of_nonzero

end
end ARCTwentyDimCharacterClass
