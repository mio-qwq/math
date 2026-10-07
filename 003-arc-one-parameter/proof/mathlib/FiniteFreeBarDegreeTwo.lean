import FiniteFreeBarAugmentation
import TwentyDimCharacteristic
import TwentyDimCochainAlgebra
import CochainWordEquiv

/-!
The actual degree-two bar boundary for the table algebra and a character.
Its three faces use genuine left multiplication, the full coordinate
expansion of the interior product, and the right character coefficient.
The adjacent boundaries compose to zero. Precomposition on an arbitrary
A-linear map to the character module has the actual scalar three-face
formula on every ordered basis pair. No higher exactness or full projective
resolution, and no comparison with Ext, is asserted here.
-/

namespace ARCFiniteFreeBarDegreeTwo

open ARCTwentyDimAlgebra ARCFiniteFreeBarModules ARCCharacterModule
open ARCFiniteFreeBarAugmentation ARCTwentyDimCochainAlgebra
open ARCTwentyDimAssociativity ARCCochainWordEquiv
open scoped BigOperators

variable {R : Type*} [CommRing R] [CharP R 2]

noncomputable section

variable (q : R) (eps : TableAlgebra q →ₐ[R] R)

/-- The lift is the full actual basis expansion, with central scalar coefficients. -/
theorem coordinateLift_sum (a : TableAlgebra q) :
    coordinateLift q a = ∑ i : Fin 20, a.coords i • wordBasis q 1 (oneWord i) := by
  classical
  calc
    coordinateLift q a = ∑ w : Word 1,
        (algebraMap R (TableAlgebra q) (a.coords (w 0))) • wordBasis q 1 w := by
      simpa only [wordBasis_repr, coordinateLift] using
        ((wordBasis q 1).sum_repr (coordinateLift q a)).symm
    _ = ∑ w : Word 1, a.coords (w 0) • wordBasis q 1 w := by
      simp only [_root_.algebraMap_smul]
    _ = ∑ w : Word 1, a.coords (w 0) • wordBasis q 1 (oneWord (w 0)) := by
      apply Finset.sum_congr rfl
      intro w hw
      have heq : oneWord (w 0) = w := oneWordEquiv.left_inv w
      rw [heq]
    _ = ∑ i : Fin 20, a.coords i • wordBasis q 1 (oneWord i) :=
      oneWordEquiv.sum_comp (fun i => a.coords i • wordBasis q 1 (oneWord i))

/-- The three actual faces on an ordered pair of input labels. -/
def degreeTwoFaces (a b : Fin 20) : BarTerm q 1 :=
  coordinateBasis q a • wordBasis q 1 (oneWord b) +
    coordinateLift q (coordinateBasis q a * coordinateBasis q b) +
    (algebraMap R (TableAlgebra q) (eps (coordinateBasis q b))) •
      wordBasis q 1 (oneWord a)

/-- A genuine map of left A-modules, extended from the whole word basis.
The outer scalar in Basis.constr is R rather than the noncommutative A. -/
def boundary2 : BarTerm q 2 →ₗ[TableAlgebra q] BarTerm q 1 :=
  (wordBasis q 2).constr R (fun w => degreeTwoFaces q eps (w 0) (w 1))

@[simp] theorem boundary2_basis (w : Word 2) :
    boundary2 q eps (wordBasis q 2 w) = degreeTwoFaces q eps (w 0) (w 1) := by
  simp [boundary2]

/-- The interior face has exactly the frozen table's actual structure constants. -/
theorem boundary2_basis_structureConstants (a b : Fin 20) :
    boundary2 q eps (wordBasis q 2 (word2 a b)) =
      coordinateBasis q a • wordBasis q 1 (oneWord b) +
        (∑ j : Fin 20, specializedConstants q a b j • wordBasis q 1 (oneWord j)) +
        eps (coordinateBasis q b) • wordBasis q 1 (oneWord a) := by
  rw [boundary2_basis]
  change degreeTwoFaces q eps a b = _
  simp only [degreeTwoFaces,
    coordinateLift_sum, coordinateBasis_mul_coords, _root_.algebraMap_smul]

/-- Character multiplicativity, scalar centrality and characteristic two
cancel the three genuine faces after applying the degree-one boundary. -/
theorem boundary_comp_boundary2 :
    (boundary q eps).comp (boundary2 q eps) = 0 := by
  apply (wordBasis q 2).ext
  intro w
  apply (zeroWordEquiv q).injective
  change zeroWordEquiv q (boundary q eps (boundary2 q eps (wordBasis q 2 w))) = 0
  rw [boundary2_basis]
  simp only [degreeTwoFaces, map_add, map_smul, boundary_basis,
    boundary_coordinateLift, LinearEquiv.apply_symm_apply, oneWord,
    smul_eq_mul, map_mul, CharTwo.sub_eq_add, mul_add]
  rw [Algebra.commutes (eps (coordinateBasis q (w 1))) (coordinateBasis q (w 0)),
    Algebra.commutes (eps (coordinateBasis q (w 1)))
      (algebraMap R (TableAlgebra q) (eps (coordinateBasis q (w 0))))]
  abel_nf
  simp only [CharTwo.two_zsmul, zero_add]

/-- Every A-linear degree-one map is evaluated on an arbitrary lifted
algebra element by the full coordinate contraction. -/
theorem hom_coordinateLift
    (phi : BarTerm q 1 →ₗ[TableAlgebra q] CharacterModule eps)
    (a : TableAlgebra q) :
    (phi (coordinateLift q a)).val =
      ∑ j : Fin 20, a.coords j * (phi (wordBasis q 1 (oneWord j))).val := by
  classical
  change valueLinearEquiv eps (phi (coordinateLift q a)) = _
  rw [coordinateLift_sum]
  simp_rw [algebra_compatible_smul (TableAlgebra q)]
  rw [map_sum, map_sum]
  simp only [map_smul, valueLinearEquiv_apply, val_character_smul]
  simp

/-- The full scalar linear cochain reconstructed from an arbitrary Hom(P1,S). -/
def scalarLinearCochain
    (phi : BarTerm q 1 →ₗ[TableAlgebra q] CharacterModule eps) :
    TableAlgebra q →ₗ[R] R :=
  (coordinateBasis q).constr R (fun j => (phi (wordBasis q 1 (oneWord j))).val)

@[simp] theorem scalarLinearCochain_basis
    (phi : BarTerm q 1 →ₗ[TableAlgebra q] CharacterModule eps) (j : Fin 20) :
    scalarLinearCochain q eps phi (coordinateBasis q j) =
      (phi (wordBasis q 1 (oneWord j))).val := by
  simp [scalarLinearCochain]

theorem scalarLinearCochain_apply
    (phi : BarTerm q 1 →ₗ[TableAlgebra q] CharacterModule eps) (a : TableAlgebra q) :
    scalarLinearCochain q eps phi a =
      ∑ j : Fin 20, a.coords j * (phi (wordBasis q 1 (oneWord j))).val := by
  rw [scalarLinearCochain, Module.Basis.constr_apply_fintype]
  simp only [Module.Basis.equivFun_apply, coordinateBasis_repr, smul_eq_mul]

/-- Precomposition with the actual degree-two boundary has the usual
three character faces on all ordered actual basis pairs. -/
theorem hom_boundary2_basis
    (phi : BarTerm q 1 →ₗ[TableAlgebra q] CharacterModule eps) (a b : Fin 20) :
    ((phi.comp (boundary2 q eps)) (wordBasis q 2 (word2 a b))).val =
      eps (coordinateBasis q a) * scalarLinearCochain q eps phi (coordinateBasis q b) +
        scalarLinearCochain q eps phi (coordinateBasis q a * coordinateBasis q b) +
        scalarLinearCochain q eps phi (coordinateBasis q a) * eps (coordinateBasis q b) := by
  change valueLinearEquiv eps
    (phi (boundary2 q eps (wordBasis q 2 (word2 a b)))) = _
  rw [boundary2_basis]
  change valueLinearEquiv eps (phi (degreeTwoFaces q eps a b)) = _
  rw [scalarLinearCochain_basis, scalarLinearCochain_basis]
  simp only [degreeTwoFaces, map_add, map_smul,
    valueLinearEquiv_apply, val_character_smul]
  rw [hom_coordinateLift, ← scalarLinearCochain_apply]
  simp only [AlgHom.commutes, Algebra.algebraMap_self_apply]
  rw [mul_comm (eps (coordinateBasis q b))]

#print axioms coordinateLift_sum
#print axioms boundary2
#print axioms boundary2_basis
#print axioms boundary2_basis_structureConstants
#print axioms boundary_comp_boundary2
#print axioms hom_coordinateLift
#print axioms scalarLinearCochain
#print axioms scalarLinearCochain_apply
#print axioms hom_boundary2_basis

end
end ARCFiniteFreeBarDegreeTwo
