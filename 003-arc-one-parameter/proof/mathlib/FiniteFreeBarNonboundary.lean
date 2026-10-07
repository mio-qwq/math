import FiniteFreeBarDegreeThree
import TwentyDimCharacterClass

/-!
The specified degree-three A-linear map into the actual f-character module
is not the precomposition of any degree-two A-linear map with the actual
degree-three boundary, whenever q^3 is nonzero. The proof uses the full
Hom/cochain equivalence and its proved differential compatibility.
No exact resolution or Ext interpretation is asserted.
-/

namespace ARCFiniteFreeBarNonboundary

open ARCTwentyDimAlgebra ARCFiniteFreeBarModules ARCCharacterModule
open ARCFiniteFreeBarCochains ARCFiniteFreeBarDegreeThree
open ARCTwentyDimCharacters ARCTwentyDimCharacterClass

variable {R : Type*} [CommRing R] [CharP R 2]

noncomputable section

variable (q : R)

/-- The actual module map corresponds to exactly the fixed scalar cochain. -/
theorem fCochainHom_cochain :
    cochain3HomEquiv q (fCharacter q) (fCochainHom q) = actualfSimpleP q :=
  (cochain3HomEquiv q (fCharacter q)).apply_symm_apply (actualfSimpleP q)

/-- Every possible actual A-linear degree-two map is excluded, not only
maps obtained by a chosen coefficient ansatz. -/
theorem fCochainHom_not_boundary (hq : q ^ 3 ≠ 0) :
    ¬ ∃ phi : BarTerm q 2 →ₗ[TableAlgebra q] CharacterModule (fCharacter q),
      phi.comp (boundary3 q (fCharacter q)) = fCochainHom q := by
  rintro ⟨phi, hphi⟩
  have h := congrArg (cochain3HomEquiv q (fCharacter q)) hphi
  rw [cochain_precomp_boundary3, fCochainHom_cochain] at h
  exact actualfSimpleP_not_character_boundary q hq
    ⟨cochain2HomEquiv q (fCharacter q) phi, h⟩

theorem fCochainHom_not_boundary_of_nonzero [NoZeroDivisors R] (hq : q ≠ 0) :
    ¬ ∃ phi : BarTerm q 2 →ₗ[TableAlgebra q] CharacterModule (fCharacter q),
      phi.comp (boundary3 q (fCharacter q)) = fCochainHom q :=
  fCochainHom_not_boundary q (pow_ne_zero 3 hq)

#print axioms fCochainHom_cochain
#print axioms fCochainHom_not_boundary
#print axioms fCochainHom_not_boundary_of_nonzero

end
end ARCFiniteFreeBarNonboundary
