import FiniteFreeBarModules
import CharacterModule
import TwentyDimCharacters
import Mathlib.LinearAlgebra.Pi

/-!
Actual A-linear maps from each finite free candidate bar term to an actual
character module are equivalent to all scalar functions on its word basis.
The inverse formula includes the genuine character action on coefficients.
No differential, exact resolution or Ext comparison is constructed here.
-/

namespace ARCFiniteFreeBarHom

open ARCTwentyDimAlgebra ARCFiniteFreeBarModules ARCCharacterModule

variable {R : Type*} [CommRing R] [CharP R 2]

noncomputable section

variable (q : R) (eps : TableAlgebra q →ₐ[R] R) (n : Nat)

local instance characterSmulCommReverse :
    SMulCommClass (TableAlgebra q) R (CharacterModule eps) :=
  SMulCommClass.symm R (TableAlgebra q) (CharacterModule eps)

/-- Taking actual values at each word is an R-linear equivalence. -/
def coefficientEquiv : (Word n → CharacterModule eps) ≃ₗ[R] (Word n → R) :=
  LinearEquiv.piCongrRight (fun _ => valueLinearEquiv eps)

/-- All A-linear maps out of the degree-n free term, without a selected
subspace or an extension hypothesis, correspond to arbitrary word values. -/
def barHomEquiv :
    (BarTerm q n →ₗ[TableAlgebra q] CharacterModule eps) ≃ₗ[R] (Word n → R) :=
  ((wordBasis q n).constr (M' := CharacterModule eps) R).symm.trans
    (coefficientEquiv q eps n)

@[simp] theorem barHomEquiv_apply
    (phi : BarTerm q n →ₗ[TableAlgebra q] CharacterModule eps) (w : Word n) :
    barHomEquiv q eps n phi w = (phi (wordBasis q n w)).val := rfl

/-- The reconstructed A-linear map has exactly the prescribed basis values. -/
theorem barHomEquiv_symm_basis (values : Word n → R) (w : Word n) :
    ((barHomEquiv q eps n).symm values (wordBasis q n w)).val = values w := by
  have h := congrFun ((barHomEquiv q eps n).apply_symm_apply values) w
  exact h

/-- Reconstruction on every free-module element uses its actual A-valued
coordinates and the actual character action, not pointwise R-linearity alone. -/
theorem barHomEquiv_symm_apply (values : Word n → R) (v : BarTerm q n) :
    ((barHomEquiv q eps n).symm values v).val =
      ∑ w : Word n, eps (v w) * values w := by
  change valueLinearEquiv eps
      (((wordBasis q n).constr R (fun w => CharacterModule.mk (values w))) v) = _
  rw [Module.Basis.constr_apply_fintype, map_sum]
  simp only [valueLinearEquiv_apply, val_character_smul,
    Module.Basis.equivFun_apply, wordBasis_repr]

/-- The instance needed by the f-character application uses its actual
coordinate augmentation and actual character-module carrier. -/
def fBarHomEquiv (q : R) (n : Nat) :
    (BarTerm q n →ₗ[TableAlgebra q]
      CharacterModule (ARCTwentyDimCharacters.fCharacter q)) ≃ₗ[R] (Word n → R) :=
  barHomEquiv q (ARCTwentyDimCharacters.fCharacter q) n

#print axioms coefficientEquiv
#print axioms barHomEquiv
#print axioms barHomEquiv_apply
#print axioms barHomEquiv_symm_basis
#print axioms barHomEquiv_symm_apply
#print axioms fBarHomEquiv

end
end ARCFiniteFreeBarHom
