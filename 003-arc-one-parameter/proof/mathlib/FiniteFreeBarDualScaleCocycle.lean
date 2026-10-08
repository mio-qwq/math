import FiniteFreeBarDualScaleComparison
import TwentyDimDualScaleCochain
import FiniteFreeBarExtThree
import ExtMkExactFunctor
import Mathlib.Algebra.Homology.DerivedCategory.Ext.Linear

/-!
# The full degree-three module cocycle under the actual comparison

The complete comparison on degree three, followed by the mapped actual
module cocycle and character endpoint identity, equals inverse-unit
scaling of the original actual module morphism. This is a whole A-linear
morphism equality, with arbitrary left coefficients retained.

It is not the missing generic exact-functor/extMk naturality theorem and
does not itself identify the canonical functor action on the Ext class.
-/

namespace ARCFiniteFreeBarDualScaleCocycle

open CategoryTheory CategoryTheory.Category
open ARCTwentyDimAlgebra ARCTwentyDimCharacters ARCTwentyDimDualScale
open ARCTwentyDimDualScaleModule ARCTwentyDimDualScaleCochain
open ARCCharacterModule ARCFiniteFreeBarModules ARCFiniteFreeBarCochains
open ARCCochainWordEquiv ARCFiniteFreeBarExtThree
open ARCFiniteFreeBarDualScaleSemilinear ARCFiniteFreeBarDualScaleComparison
open ARCFiniteFreeBarProjectiveResolution ARCExtMkExactFunctor
open scoped ModuleCat.Algebra BigOperators

universe u
variable {R : Type u} [CommRing R] [CharP R 2]

noncomputable section

private theorem dualScale_coordinateBasis_weight (q : R) (H : Rˣ) (i : Fin 20) :
    dualScale q H (coordinateBasis q i) = dualWeight H i.val • coordinateBasis q i := by
  rw [dualScale_basis]
  by_cases hi : i.val < 10 <;> simp [dualWeight, hi]

/-- The complete word weight agrees with the fixed cocycle eigenvalue
on every actual free A-basis word, without a support enumeration. -/
theorem wordWeight_mul_fCochainHom_basis (q : R) (H : Rˣ) (w : Word 3) :
    wordWeight H 3 w * (fCochainHom q (wordBasis q 3 w)).val =
      (H : R) * (fCochainHom q (wordBasis q 3 w)).val := by
  have hv : (fCochainHom q (wordBasis q 3 w)).val =
      actualfSimpleP q (coordinateBasis q (w 0))
        (coordinateBasis q (w 1)) (coordinateBasis q (w 2)) := by
    conv_lhs => rw [← word3_eta w]
    rw [fCochainHom, cochain3HomEquiv_symm_basis]
  rw [hv]
  have hp := actualfSimpleP_pullback q H
    (coordinateBasis q (w 0)) (coordinateBasis q (w 1)) (coordinateBasis q (w 2))
  rw [dualScale_coordinateBasis_weight, dualScale_coordinateBasis_weight,
    dualScale_coordinateBasis_weight] at hp
  simpa [wordWeight, Fin.prod_univ_three, mul_assoc, mul_comm, mul_left_comm] using hp

set_option backward.isDefEq.respectTransparency false in
/-- Equality of complete actual module-Hom cocycles, after the complete
inverse-twist comparison and the two actual character endpoints. -/
theorem twist_fCocycle (q : R) (H : Rˣ) :
    twistTermHom q H 3 ≫ (dualScaleFunctor q H).map (fCocycle q) ≫
      (fCharacterTwistIso q H).hom = (↑(H⁻¹) : R) • fCocycle q := by
  apply ModuleCat.hom_ext
  apply (wordBasis q 3).ext
  intro w
  apply CharacterModule.ext
  dsimp only [ModuleCat.hom_comp, LinearMap.comp_apply,
    ModuleCat.hom_smul, LinearMap.smul_apply]
  change (fCochainHom q (termScale q H⁻¹ 3 (wordBasis q 3 w))).val =
    ((↑(H⁻¹) : R) • fCochainHom q (wordBasis q 3 w)).val
  rw [val_coefficient_smul]
  rw [termScale_basis, (fCochainHom q).map_smul_of_tower, val_coefficient_smul]
  exact wordWeight_mul_fCochainHom_basis q H⁻¹ w

/-- The mapped cocycle is closed on the actual specified mapped resolution. -/
theorem mapped_fCocycle_closed (q : R) (H : Rˣ) :
    (twistedResolution q H).complex.d 4 3 ≫
      (dualScaleFunctor q H).map (fCocycle q) = 0 := by
  change (dualScaleFunctor q H).map
    ((projectiveResolution q (fCharacter q)).complex.d 4 3) ≫
      (dualScaleFunctor q H).map (fCocycle q) = 0
  rw [← Functor.map_comp, fCocycle_closed, Functor.map_zero]

/-- The actual Ext class represented by the mapped cocycle on the mapped
specified resolution. Identifying it with canonical functor transport is
a separate obligation. -/
def twisted_fExtThree (q : R) (H : Rˣ) : CategoryTheory.Abelian.Ext
    ((dualScaleFunctor q H).obj (characterObject q (fCharacter q)))
    ((dualScaleFunctor q H).obj (characterObject q (fCharacter q))) 3 :=
  (twistedResolution q H).extMk ((dualScaleFunctor q H).map (fCocycle q))
    4 rfl (mapped_fCocycle_closed q H)

set_option backward.isDefEq.respectTransparency false in
/-- Genuine Ext equality for the class represented on the mapped specified
resolution, using both actual endpoint isomorphisms and the all-degree
resolution comparison. This does not yet compute Ext.mapExactFunctor. -/
theorem twisted_fExtThree_endpoints (q : R) (H : Rˣ) :
    ((CategoryTheory.Abelian.Ext.mk₀ (fCharacterTwistIso q H).inv).comp
      (twisted_fExtThree q H) (zero_add 3)).comp
      (CategoryTheory.Abelian.Ext.mk₀ (fCharacterTwistIso q H).hom) (add_zero 3) =
        (↑(H⁻¹) : R) • fExtThree q := by
  rw [twisted_fExtThree,
    ProjectiveResolution.mk₀_comp_extMk _ _ _ _ (twistResolutionHom q H),
    ProjectiveResolution.extMk_comp_mk₀]
  change (projectiveResolution q (fCharacter q)).extMk
    ((twistTermHom q H 3 ≫ (dualScaleFunctor q H).map (fCocycle q)) ≫
      (fCharacterTwistIso q H).hom) 4 rfl _ = _
  simpa only [Category.assoc, twist_fCocycle, fExtThree] using
    extMk_smul (projectiveResolution q (fCharacter q))
      (fCocycle q) 4 rfl (fCocycle_closed q) (↑(H⁻¹) : R)

/-- The represented mapped-resolution class is nonzero whenever q cubed
is nonzero, over an arbitrary characteristic-two commutative ring. -/
theorem twisted_fExtThree_ne_zero (q : R) (H : Rˣ) (hq : q ^ 3 ≠ 0) :
    twisted_fExtThree q H ≠ 0 := by
  intro hz
  have hz' : (↑(H⁻¹) : R) • fExtThree q = 0 := by
    rw [← twisted_fExtThree_endpoints, hz]
    simp
  have hx := congrArg (fun x => (↑H : R) • x) hz'
  simp only [smul_smul, Units.mul_inv, one_smul, smul_zero] at hx
  exact fExtThree_ne_zero q hq hx

#print axioms wordWeight_mul_fCochainHom_basis
#print axioms twist_fCocycle
#print axioms mapped_fCocycle_closed
#print axioms twisted_fExtThree
#print axioms twisted_fExtThree_endpoints
#print axioms twisted_fExtThree_ne_zero

end
end ARCFiniteFreeBarDualScaleCocycle
