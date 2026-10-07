import TwentyDimDualScale
import FiniteFreeBarProjectiveResolution
import Mathlib.Algebra.Category.ModuleCat.ChangeOfRings
import Mathlib.CategoryTheory.Adjunction.Limits

/-!
# Actual module-category restriction along inverse dual scaling

The actual algebra automorphism gives a self-equivalence of the category
of all left modules by restricting scalars along its inverse. We record
the resulting action on every module, preservation of the base scalar
linearity and finite limits/colimits, and an actual identity-on-elements
isomorphism between the twisted and original f-character modules.

This file constructs the actual module-category objects and morphisms.
It does not compute an Ext action, compare projective resolutions, or
assert any all-degree Ext profile or the complete ARC realization.
-/

namespace ARCTwentyDimDualScaleModule

open CategoryTheory CategoryTheory.Limits
open ARCTwentyDimAlgebra ARCTwentyDimCharacters ARCTwentyDimDualScale
open ARCCharacterModule ARCFiniteFreeBarProjectiveResolution
open scoped ModuleCat.Algebra

universe u
variable {R : Type u} [CommRing R] [CharP R 2]

noncomputable section

/-- Restriction along the inverse automorphism as an actual self-equivalence
of the category of all left modules over the noncommutative algebra. -/
def dualScaleEquivalence (q : R) (H : Rˣ) :
    ModuleCat.{u} (TableAlgebra q) ≌ ModuleCat.{u} (TableAlgebra q) :=
  ModuleCat.restrictScalarsEquivalenceOfRingEquiv
    (dualScale q H).symm.toRingEquiv

/-- The actual inverse-restriction functor underlying the equivalence. -/
def dualScaleFunctor (q : R) (H : Rˣ) :
    ModuleCat.{u} (TableAlgebra q) ⥤ ModuleCat.{u} (TableAlgebra q) :=
  (dualScaleEquivalence q H).functor

instance dualScaleFunctor_isEquivalence (q : R) (H : Rˣ) :
    (dualScaleFunctor q H).IsEquivalence :=
  (dualScaleEquivalence q H).isEquivalence_functor

instance dualScaleFunctor_additive (q : R) (H : Rˣ) :
    (dualScaleFunctor q H).Additive := by
  exact inferInstanceAs
    ((ModuleCat.restrictScalarsEquivalenceOfRingEquiv
      (dualScale q H).symm.toRingEquiv).functor.Additive)

instance dualScaleFunctor_linear (q : R) (H : Rˣ) :
    (dualScaleFunctor q H).Linear R := by
  exact inferInstanceAs
    ((ModuleCat.restrictScalarsEquivalenceOfRingEquiv
      (dualScale q H).symm.toRingEquiv).functor.Linear R)

instance dualScaleFunctor_preservesFiniteLimits (q : R) (H : Rˣ) :
    PreservesFiniteLimits (dualScaleFunctor q H) := by
  infer_instance

instance dualScaleFunctor_preservesFiniteColimits (q : R) (H : Rˣ) :
    PreservesFiniteColimits (dualScaleFunctor q H) := by
  infer_instance

/-- On every actual module, the new action is the old action precomposed
with the inverse algebra automorphism. -/
@[simp] theorem dualScaleFunctor_obj_smul (q : R) (H : Rˣ)
    (M : ModuleCat.{u} (TableAlgebra q)) (a : TableAlgebra q) (x : M) :
    (((dualScaleFunctor q H).obj M).smul a).hom x =
      (M.smul ((dualScale q H).symm a)).hom x := rfl

/-- Restriction preserves the underlying function of every module morphism. -/
@[simp] theorem dualScaleFunctor_map_apply (q : R) (H : Rˣ)
    {M N : ModuleCat.{u} (TableAlgebra q)} (f : M ⟶ N) (x : M) :
    (dualScaleFunctor q H).map f x = f x := rfl

/-- The actual twisted f-character module identifies with the original
one by the underlying identity in both directions. -/
def fCharacterTwistIso (q : R) (H : Rˣ) :
    (dualScaleFunctor q H).obj (characterObject q (fCharacter q)) ≅
      characterObject q (fCharacter q) where
  hom := ModuleCat.ofHom
    (X := (dualScaleFunctor q H).obj (characterObject q (fCharacter q)))
    (Y := characterObject q (fCharacter q))
    { toFun := fun x => x
      map_add' _ _ := rfl
      map_smul' a x := by
        apply CharacterModule.ext
        change fCharacter q ((dualScale q H).symm a) * x.val =
          fCharacter q a * x.val
        rw [dualScale_symm, fCharacter_dualScale] }
  inv := ModuleCat.ofHom
    (X := characterObject q (fCharacter q))
    (Y := (dualScaleFunctor q H).obj (characterObject q (fCharacter q)))
    { toFun := fun x => x
      map_add' _ _ := rfl
      map_smul' a x := by
        apply CharacterModule.ext
        change fCharacter q a * x.val =
          fCharacter q ((dualScale q H).symm a) * x.val
        rw [dualScale_symm, fCharacter_dualScale] }
  hom_inv_id := by
    apply ModuleCat.hom_ext
    ext x
    rfl
  inv_hom_id := by
    apply ModuleCat.hom_ext
    ext x
    rfl

@[simp] theorem fCharacterTwistIso_hom_apply (q : R) (H : Rˣ)
    (x : (dualScaleFunctor q H).obj (characterObject q (fCharacter q))) :
    (fCharacterTwistIso q H).hom x = x := rfl

@[simp] theorem fCharacterTwistIso_inv_apply (q : R) (H : Rˣ)
    (x : characterObject q (fCharacter q)) :
    (fCharacterTwistIso q H).inv x = x := rfl

#print axioms dualScaleEquivalence
#print axioms dualScaleFunctor
#print axioms dualScaleFunctor_isEquivalence
#print axioms dualScaleFunctor_additive
#print axioms dualScaleFunctor_linear
#print axioms dualScaleFunctor_preservesFiniteLimits
#print axioms dualScaleFunctor_preservesFiniteColimits
#print axioms dualScaleFunctor_obj_smul
#print axioms dualScaleFunctor_map_apply
#print axioms fCharacterTwistIso
#print axioms fCharacterTwistIso_hom_apply
#print axioms fCharacterTwistIso_inv_apply

end
end ARCTwentyDimDualScaleModule
