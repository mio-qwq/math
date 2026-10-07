import FiniteFreeBarHom
import CochainWordEquiv

/-!
Full scalar bilinear/trilinear cochains correspond to actual A-linear maps
from the degree-two/three free candidate terms to the character module.
The fixed f-character cochain gives an actual A-linear degree-three map
with its q^3 pairing. No bar differential or resolution is assumed.
-/

namespace ARCFiniteFreeBarCochains

open ARCTwentyDimAlgebra ARCFiniteFreeBarModules ARCFiniteFreeBarHom
open ARCCharacterModule ARCCochainWordEquiv ARCCharacterHochschildMaps
open ARCTwentyDimCharacters

variable {R : Type*} [CommRing R] [CharP R 2]

noncomputable section

variable (q : R) (eps : TableAlgebra q →ₐ[R] R)

local instance characterSmulCommReverse :
    SMulCommClass (TableAlgebra q) R (CharacterModule eps) :=
  SMulCommClass.symm R (TableAlgebra q) (CharacterModule eps)

/-- A full equivalence with all scalar-valued bilinear cochains. -/
def cochain2HomEquiv :
    (BarTerm q 2 →ₗ[TableAlgebra q] CharacterModule eps) ≃ₗ[R]
      C2S R (TableAlgebra q) :=
  (barHomEquiv q eps 2).trans (cochain2WordEquiv q).symm

/-- A full equivalence with all scalar-valued trilinear cochains. -/
def cochain3HomEquiv :
    (BarTerm q 3 →ₗ[TableAlgebra q] CharacterModule eps) ≃ₗ[R]
      C3S R (TableAlgebra q) :=
  (barHomEquiv q eps 3).trans (cochain3WordEquiv q).symm

theorem cochain2HomEquiv_basis
    (phi : BarTerm q 2 →ₗ[TableAlgebra q] CharacterModule eps) (a b : Fin 20) :
    cochain2HomEquiv q eps phi (coordinateBasis q a) (coordinateBasis q b) =
      (phi (wordBasis q 2 (word2 a b))).val :=
  congrFun ((cochain2WordEquiv q).apply_symm_apply (barHomEquiv q eps 2 phi))
    (word2 a b)

theorem cochain3HomEquiv_basis
    (phi : BarTerm q 3 →ₗ[TableAlgebra q] CharacterModule eps) (a b c : Fin 20) :
    cochain3HomEquiv q eps phi (coordinateBasis q a) (coordinateBasis q b)
      (coordinateBasis q c) = (phi (wordBasis q 3 (word3 a b c))).val :=
  congrFun ((cochain3WordEquiv q).apply_symm_apply (barHomEquiv q eps 3 phi))
    (word3 a b c)

theorem cochain2HomEquiv_symm_basis (G : C2S R (TableAlgebra q)) (a b : Fin 20) :
    ((cochain2HomEquiv q eps).symm G (wordBasis q 2 (word2 a b))).val =
      G (coordinateBasis q a) (coordinateBasis q b) := by
  change ((barHomEquiv q eps 2).symm (cochain2WordEquiv q G)
    (wordBasis q 2 (word2 a b))).val = _
  rw [barHomEquiv_symm_basis]
  rfl

theorem cochain3HomEquiv_symm_basis (F : C3S R (TableAlgebra q)) (a b c : Fin 20) :
    ((cochain3HomEquiv q eps).symm F (wordBasis q 3 (word3 a b c))).val =
      F (coordinateBasis q a) (coordinateBasis q b) (coordinateBasis q c) := by
  change ((barHomEquiv q eps 3).symm (cochain3WordEquiv q F)
    (wordBasis q 3 (word3 a b c))).val = _
  rw [barHomEquiv_symm_basis]
  rfl

/-- The specified scalar cocycle as an actual A-linear map into the actual
character module, rather than only a scalar array. -/
def fCochainHom : BarTerm q 3 →ₗ[TableAlgebra q] CharacterModule (fCharacter q) :=
  (cochain3HomEquiv q (fCharacter q)).symm (actualfSimpleP q)

/-- The same separating cycle is detected in this actual module homomorphism. -/
theorem fCochainHom_cycle_pairing :
    q ^ 2 * (fCochainHom q (wordBasis q 3 (word3 6 1 17))).val +
      (fCochainHom q (wordBasis q 3 (word3 6 2 17))).val = q ^ 3 := by
  rw [fCochainHom, cochain3HomEquiv_symm_basis, cochain3HomEquiv_symm_basis]
  exact actualfSimpleP_cycle_pairing q

theorem fCochainHom_ne_zero (hq : q ^ 3 ≠ 0) : fCochainHom q ≠ 0 := by
  intro hF
  have h := fCochainHom_cycle_pairing q
  rw [hF] at h
  simp only [LinearMap.zero_apply, val_zero, mul_zero, add_zero] at h
  exact hq h.symm

#print axioms cochain2HomEquiv
#print axioms cochain3HomEquiv
#print axioms cochain2HomEquiv_basis
#print axioms cochain3HomEquiv_basis
#print axioms cochain2HomEquiv_symm_basis
#print axioms cochain3HomEquiv_symm_basis
#print axioms fCochainHom
#print axioms fCochainHom_cycle_pairing
#print axioms fCochainHom_ne_zero

end
end ARCFiniteFreeBarCochains
