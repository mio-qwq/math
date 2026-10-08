import TwentyDimDualScaleExtEigenvalue

/-!
# Canonical dual twist and actual graded Yoneda powers

The canonical transported action preserves every degree of actual Yoneda
composition and its degree-zero identity. Its weight on the m-fold power
of the fixed actual Ext cubed class is the m-th power of the inverse unit.

The recursively defined powers live in the actual Mathlib Ext groups of
degree 3*m. Powers with m at least two are not asserted to be nonzero.
No whole-Ext dimension, stable profile or complete ARC is asserted.
-/

namespace ARCTwentyDimDualScaleYoneda

open CategoryTheory CategoryTheory.Abelian
open ARCTwentyDimAlgebra ARCTwentyDimCharacters ARCCharacterModule
open ARCFiniteFreeBarProjectiveResolution ARCFiniteFreeBarExtThree
open ARCTwentyDimDualScaleModule
open ARCTwentyDimDualScaleExtTransport ARCTwentyDimDualScaleExtEigenvalue
open scoped ModuleCat.Algebra

universe u
variable {R : Type u} [CommRing R] [CharP R 2]

noncomputable section

/-- Conjugation by any actual endpoint isomorphism preserves all graded
Yoneda compositions, including the cancellation of its middle endpoints. -/
theorem extIsoTransport_comp (q : R) {X Y : ModuleCat.{u} (TableAlgebra q)}
    (e : X ≅ Y) {a b c : Nat} (α : Ext.{u} X X a) (β : Ext.{u} X X b)
    (h : a + b = c) :
    extIsoTransport q e c (α.comp β h) =
      (extIsoTransport q e a α).comp (extIsoTransport q e b β) h := by
  change ((Ext.mk₀ e.inv).comp (α.comp β h) (zero_add c)).comp
      (Ext.mk₀ e.hom) (add_zero c) =
    (((Ext.mk₀ e.inv).comp α (zero_add a)).comp
      (Ext.mk₀ e.hom) (add_zero a)).comp
      (((Ext.mk₀ e.inv).comp β (zero_add b)).comp
        (Ext.mk₀ e.hom) (add_zero b)) h
  rw [← Ext.comp_assoc_of_third_deg_zero, Ext.comp_assoc_of_second_deg_zero,
    Ext.mk₀_comp_mk₀_assoc, Iso.hom_inv_id, Ext.mk₀_id_comp]
  exact congrArg (fun γ => γ.comp (Ext.mk₀ e.hom) (add_zero c))
    (Ext.comp_assoc (Ext.mk₀ e.inv) α β (zero_add a) h
      (show 0 + a + b = c by simpa using h)).symm

/-- Transport by any actual endpoint isomorphism preserves the identity
element in actual degree-zero self-Ext. -/
theorem extIsoTransport_mk₀_id (q : R) {X Y : ModuleCat.{u} (TableAlgebra q)}
    (e : X ≅ Y) :
    extIsoTransport q e 0 (Ext.mk₀ (𝟙 X)) = Ext.mk₀ (𝟙 Y) := by
  change ((Ext.mk₀ e.inv).comp (Ext.mk₀ (𝟙 X)) (zero_add 0)).comp
      (Ext.mk₀ e.hom) (add_zero 0) = Ext.mk₀ (𝟙 Y)
  rw [Ext.comp_mk₀_id, Ext.mk₀_comp_mk₀, Iso.inv_hom_id]

/-- The genuine canonical transported action preserves actual Yoneda
composition in every pair of nonnegative degrees. -/
theorem dualScaleExtTransportMap_comp (q : R) (H : Rˣ) {a b c : Nat}
    (α : Ext.{u} (characterObject q (fCharacter q))
      (characterObject q (fCharacter q)) a)
    (β : Ext.{u} (characterObject q (fCharacter q))
      (characterObject q (fCharacter q)) b) (h : a + b = c) :
    dualScaleExtTransportMap q H c (α.comp β h) =
      (dualScaleExtTransportMap q H a α).comp
        (dualScaleExtTransportMap q H b β) h := by
  change extIsoTransport q (fCharacterTwistIso q H) c
      ((α.comp β h).mapExactFunctor (dualScaleFunctor q H)) =
    (extIsoTransport q (fCharacterTwistIso q H) a
      (α.mapExactFunctor (dualScaleFunctor q H))).comp
      (extIsoTransport q (fCharacterTwistIso q H) b
        (β.mapExactFunctor (dualScaleFunctor q H))) h
  rw [Ext.mapExactFunctor_comp, extIsoTransport_comp]

/-- The canonical transported action fixes the actual degree-zero identity. -/
theorem dualScaleExtTransportMap_mk₀_id (q : R) (H : Rˣ) :
    dualScaleExtTransportMap q H 0
      (Ext.mk₀ (𝟙 (characterObject q (fCharacter q)))) =
        Ext.mk₀ (𝟙 (characterObject q (fCharacter q))) := by
  change extIsoTransport q (fCharacterTwistIso q H) 0
    ((Ext.mk₀ (𝟙 (characterObject q (fCharacter q)))).mapExactFunctor
      (dualScaleFunctor q H)) = _
  rw [Ext.mapExactFunctor_mk₀, CategoryTheory.Functor.map_id, extIsoTransport_mk₀_id]

/-- Actual m-fold Yoneda power of the fixed f-character Ext cubed class.
The zero-th power is the degree-zero identity. No nonvanishing is assumed. -/
def fYonedaPower (q : R) : (m : Nat) →
    Ext.{u} (characterObject q (fCharacter q))
      (characterObject q (fCharacter q)) (3 * m)
  | 0 => Ext.mk₀ (𝟙 (characterObject q (fCharacter q)))
  | m + 1 => (fYonedaPower q m).comp (fExtThree q) (by omega)

@[simp] theorem fYonedaPower_zero (q : R) :
    fYonedaPower q 0 = Ext.mk₀ (𝟙 (characterObject q (fCharacter q))) := rfl

@[simp] theorem fYonedaPower_succ (q : R) (m : Nat) :
    fYonedaPower q (m + 1) =
      (fYonedaPower q m).comp (fExtThree q) (by omega) := rfl

/-- The first graded power is exactly the specified genuine Ext cubed class. -/
@[simp] theorem fYonedaPower_one (q : R) : fYonedaPower q 1 = fExtThree q := by
  change (Ext.mk₀ (𝟙 (characterObject q (fCharacter q)))).comp
    (fExtThree q) (zero_add 3) = fExtThree q
  exact Ext.mk₀_id_comp (fExtThree q)

/-- Canonical inverse-dual restriction has the inverse unit's m-th power
as its weight on the actual m-fold Yoneda power in degree 3*m. -/
theorem dualScaleExtTransport_fYonedaPower (q : R) (H : Rˣ) (m : Nat) :
    dualScaleExtTransportMap q H (3 * m) (fYonedaPower q m) =
      (↑(H⁻¹) : R) ^ m • fYonedaPower q m := by
  induction m with
  | zero =>
    simpa only [Nat.mul_zero, fYonedaPower_zero, pow_zero, one_smul] using
      dualScaleExtTransportMap_mk₀_id q H
  | succ m ih =>
    rw [fYonedaPower_succ, dualScaleExtTransportMap_comp, ih,
      dualScaleExtTransport_fExtThree]
    simp only [Ext.smul_comp, Ext.comp_smul, smul_smul, pow_succ']

/-- The same canonical weight calculation on every scalar multiple of
each specified power, without an Ext dimension or nonvanishing claim. -/
theorem dualScaleExtTransport_fYonedaPower_smul (q : R) (H : Rˣ)
    (m : Nat) (r : R) :
    dualScaleExtTransportMap q H (3 * m) (r • fYonedaPower q m) =
      (r * (↑(H⁻¹) : R) ^ m) • fYonedaPower q m := by
  rw [dualScaleExtTransportMap_smul, dualScaleExtTransport_fYonedaPower, smul_smul]

#print axioms extIsoTransport_comp
#print axioms extIsoTransport_mk₀_id
#print axioms dualScaleExtTransportMap_comp
#print axioms dualScaleExtTransportMap_mk₀_id
#print axioms fYonedaPower
#print axioms fYonedaPower_zero
#print axioms fYonedaPower_succ
#print axioms fYonedaPower_one
#print axioms dualScaleExtTransport_fYonedaPower
#print axioms dualScaleExtTransport_fYonedaPower_smul

end
end ARCTwentyDimDualScaleYoneda
