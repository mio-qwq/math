import TwentyDimDualScaleModule
import Mathlib.Algebra.Category.ModuleCat.Ext.HasExt
import Mathlib.Algebra.Homology.DerivedCategory.Ext.MapBijective
import Mathlib.Algebra.Module.Submodule.Equiv

/-!
# Canonical Ext transport by inverse dual restriction

The actual inverse-restriction module self-equivalence induces the
canonical exact-functor map on Mathlib Ext in every degree. Transporting
its two endpoints by the actual f-character identity isomorphism gives
an R-linear automorphism of the f-character self-Ext group in each degree.

No choice of a projective resolution defines this action. This file does
not compute its value on the fixed degree-three class: the exact-functor
map/extMk comparison and the specific resolution comparison are separate
obligations. No eigenvalue or all-degree Ext dimension/profile is claimed.
-/

namespace ARCTwentyDimDualScaleExtTransport

open CategoryTheory CategoryTheory.Limits CategoryTheory.Abelian
open ARCTwentyDimAlgebra ARCTwentyDimCharacters
open ARCFiniteFreeBarProjectiveResolution ARCTwentyDimDualScaleModule
open scoped ModuleCat.Algebra

universe u
variable {R : Type u} [CommRing R] [CharP R 2]

noncomputable section

/-- Change both endpoints of actual self-Ext by an actual module isomorphism. -/
def extIsoTransport (q : R) {X Y : ModuleCat.{u} (TableAlgebra q)}
    (e : X ≅ Y) (n : Nat) : Ext.{u} X X n ≃ₗ[R] Ext.{u} Y Y n where
  toFun a := ((Ext.mk₀ e.inv).comp a (zero_add n)).comp
    (Ext.mk₀ e.hom) (add_zero n)
  invFun b := ((Ext.mk₀ e.hom).comp b (zero_add n)).comp
    (Ext.mk₀ e.inv) (add_zero n)
  left_inv a := by
    simp only [Ext.comp_assoc_of_third_deg_zero, Ext.mk₀_comp_mk₀,
      Iso.hom_inv_id, Ext.comp_mk₀_id,
      Ext.mk₀_comp_mk₀_assoc, Ext.mk₀_id_comp]
  right_inv b := by
    simp only [Ext.comp_assoc_of_third_deg_zero, Ext.mk₀_comp_mk₀,
      Iso.inv_hom_id, Ext.comp_mk₀_id,
      Ext.mk₀_comp_mk₀_assoc, Ext.mk₀_id_comp]
  map_add' a b := by simp
  map_smul' r a := by simp

/-- The canonical exact-functor map to the two actual twisted endpoints. -/
def dualScaleExtMap (q : R) (H : Rˣ) (n : Nat) :
    Ext.{u} (characterObject q (fCharacter q)) (characterObject q (fCharacter q)) n
      →ₗ[R] Ext.{u}
        ((dualScaleFunctor q H).obj (characterObject q (fCharacter q)))
        ((dualScaleFunctor q H).obj (characterObject q (fCharacter q))) n :=
  (dualScaleFunctor q H).mapExtLinearMap R
    (characterObject q (fCharacter q)) (characterObject q (fCharacter q)) n

/-- The canonical map is bijective because the actual functor is fully
faithful, exact and preserves projective objects. -/
theorem dualScaleExtMap_bijective (q : R) (H : Rˣ) (n : Nat) :
    Function.Bijective (dualScaleExtMap q H n) := by
  change Function.Bijective ((dualScaleFunctor q H).mapExtAddHom
    (characterObject q (fCharacter q)) (characterObject q (fCharacter q)) n)
  exact (dualScaleFunctor q H).mapExt_bijective_of_preservesProjectiveObjects
    (characterObject q (fCharacter q)) (characterObject q (fCharacter q)) n

/-- Canonical inverse-restriction Ext action, with its actual endpoints
transported back to the original f-character module. -/
def dualScaleExtTransportEquiv (q : R) (H : Rˣ) (n : Nat) :
    Ext.{u} (characterObject q (fCharacter q)) (characterObject q (fCharacter q)) n
      ≃ₗ[R] Ext.{u}
        (characterObject q (fCharacter q)) (characterObject q (fCharacter q)) n :=
  (LinearEquiv.ofBijective (dualScaleExtMap q H n)
    (dualScaleExtMap_bijective q H n)).trans
      (extIsoTransport q (fCharacterTwistIso q H) n)

/-- The same canonical transported action, retained as a genuine R-linear map. -/
def dualScaleExtTransportMap (q : R) (H : Rˣ) (n : Nat) :
    Ext.{u} (characterObject q (fCharacter q)) (characterObject q (fCharacter q)) n
      →ₗ[R] Ext.{u}
        (characterObject q (fCharacter q)) (characterObject q (fCharacter q)) n :=
  (dualScaleExtTransportEquiv q H n).toLinearMap

/-- Exact formula identifying the action with the canonical functor map
and the specified endpoint isomorphism in the correct two directions. -/
@[simp] theorem dualScaleExtTransportMap_apply (q : R) (H : Rˣ) (n : Nat)
    (a : Ext.{u} (characterObject q (fCharacter q))
      (characterObject q (fCharacter q)) n) :
    dualScaleExtTransportMap q H n a =
      ((Ext.mk₀ (fCharacterTwistIso q H).inv).comp
        (a.mapExactFunctor (dualScaleFunctor q H)) (zero_add n)).comp
          (Ext.mk₀ (fCharacterTwistIso q H).hom) (add_zero n) := rfl

theorem dualScaleExtTransportMap_zero (q : R) (H : Rˣ) (n : Nat) :
    dualScaleExtTransportMap q H n 0 = 0 :=
  (dualScaleExtTransportMap q H n).map_zero

theorem dualScaleExtTransportMap_add (q : R) (H : Rˣ) (n : Nat)
    (a b : Ext.{u} (characterObject q (fCharacter q))
      (characterObject q (fCharacter q)) n) :
    dualScaleExtTransportMap q H n (a + b) =
      dualScaleExtTransportMap q H n a + dualScaleExtTransportMap q H n b :=
  (dualScaleExtTransportMap q H n).map_add a b

theorem dualScaleExtTransportMap_smul (q : R) (H : Rˣ) (n : Nat) (r : R)
    (a : Ext.{u} (characterObject q (fCharacter q))
      (characterObject q (fCharacter q)) n) :
    dualScaleExtTransportMap q H n (r • a) =
      r • dualScaleExtTransportMap q H n a :=
  (dualScaleExtTransportMap q H n).map_smul r a

theorem dualScaleExtTransportMap_bijective (q : R) (H : Rˣ) (n : Nat) :
    Function.Bijective (dualScaleExtTransportMap q H n) :=
  (dualScaleExtTransportEquiv q H n).bijective

/-- The canonical transported action preserves, and reflects, nonzero
actual Ext classes in every degree. It does not calculate their weights. -/
theorem dualScaleExtTransportMap_ne_zero_iff (q : R) (H : Rˣ) (n : Nat)
    (a : Ext.{u} (characterObject q (fCharacter q))
      (characterObject q (fCharacter q)) n) :
    dualScaleExtTransportMap q H n a ≠ 0 ↔ a ≠ 0 := by
  constructor
  · intro h ha
    apply h
    rw [ha, dualScaleExtTransportMap_zero]
  · intro ha h
    apply ha
    apply (dualScaleExtTransportMap_bijective q H n).injective
    rw [h, dualScaleExtTransportMap_zero]

#print axioms extIsoTransport
#print axioms dualScaleExtMap
#print axioms dualScaleExtMap_bijective
#print axioms dualScaleExtTransportEquiv
#print axioms dualScaleExtTransportMap
#print axioms dualScaleExtTransportMap_apply
#print axioms dualScaleExtTransportMap_zero
#print axioms dualScaleExtTransportMap_add
#print axioms dualScaleExtTransportMap_smul
#print axioms dualScaleExtTransportMap_bijective
#print axioms dualScaleExtTransportMap_ne_zero_iff

end
end ARCTwentyDimDualScaleExtTransport
