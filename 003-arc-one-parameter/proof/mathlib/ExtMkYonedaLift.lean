import ExtMkCanonicalFunctor

/-!
# Actual Yoneda composition from a specified shifted resolution lift

Two equalities of whole shifted complex morphisms identify the given
closed components' Yoneda composition. The resolutions, augmentations,
shift identifications and the supplied small Ext universe are retained.

The lift is an explicit hypothesis. This file does not construct a cup
product lift, prove higher powers nonzero or assert a full Ext profile.
-/

namespace ARCExtMkYonedaLift

open CategoryTheory CategoryTheory.Category CategoryTheory.Localization
open CategoryTheory.Abelian CochainComplex CochainComplex.HomComplex
open ARCExtMkCanonicalFunctor

noncomputable section

section LocalizedComposition

universe w

variable {D : Type*} [Category* D] [HasShift D ℤ]
  (W : MorphismProperty D) [W.IsCompatibleWithShift ℤ]

/-- Passing actual shifted morphisms to the supplied small localization
preserves their actual shifted composition. -/
theorem localized_mk_comp {K Q Z : D} {a b c : ℤ}
    [HasSmallLocalizedShiftedHom.{w} W ℤ K Q]
    [HasSmallLocalizedShiftedHom.{w} W ℤ Q Z]
    [HasSmallLocalizedShiftedHom.{w} W ℤ K Z]
    [HasSmallLocalizedShiftedHom.{w} W ℤ Z Z]
    (L : ShiftedHom K Q a) (g : ShiftedHom Q Z b) (hab : b + a = c) :
    (SmallShiftedHom.mk W L).comp (SmallShiftedHom.mk W g) hab =
      SmallShiftedHom.mk W (L.comp g hab) := by
  apply (SmallShiftedHom.equiv W W.Q).injective
  simp only [SmallShiftedHom.equiv_comp, SmallShiftedHom.equiv_mk,
    ShiftedHom.map_comp]

/-- An actual lift of a single-target shifted morphism cancels the actual
augmentation inverse in the next localized roof. -/
theorem localized_comp_roof {K Q Y Z : D} {a b c : ℤ} [W.RespectsIso]
    [HasSmallLocalizedShiftedHom.{w} W ℤ K Q]
    [HasSmallLocalizedShiftedHom.{w} W ℤ K Y]
    [HasSmallLocalizedShiftedHom.{w} W ℤ K Z]
    [HasSmallLocalizedShiftedHom.{w} W ℤ Q Q]
    [HasSmallLocalizedShiftedHom.{w} W ℤ Q Y]
    [HasSmallLocalizedShiftedHom.{w} W ℤ Q Z]
    [HasSmallLocalizedShiftedHom.{w} W ℤ Y Q]
    [HasSmallLocalizedShiftedHom.{w} W ℤ Y Y]
    [HasSmallLocalizedShiftedHom.{w} W ℤ Y Z]
    [HasSmallLocalizedShiftedHom.{w} W ℤ Z Z]
    (π : Q ⟶ Y) (hπ : W π) (L : ShiftedHom K Q a)
    (f : ShiftedHom K Y a) (g : ShiftedHom Q Z b) (hab : b + a = c)
    (hL : L.comp (ShiftedHom.mk₀ (0 : ℤ) rfl π) (zero_add a) = f) :
    (SmallShiftedHom.mk W f).comp
      ((SmallShiftedHom.mk₀Inv (0 : ℤ) rfl π hπ).comp
        (SmallShiftedHom.mk W g) (add_zero b)) hab =
      SmallShiftedHom.mk W (L.comp g hab) := by
  have hL' : (SmallShiftedHom.mk W L).comp
      (SmallShiftedHom.mk₀ W (0 : ℤ) rfl π) (zero_add a) =
        SmallShiftedHom.mk W f := by
    change (SmallShiftedHom.mk W L).comp
        (SmallShiftedHom.mk W (ShiftedHom.mk₀ (0 : ℤ) rfl π)) (zero_add a) = _
    rw [localized_mk_comp, hL]
  have hcancel : (SmallShiftedHom.mk₀ W (0 : ℤ) rfl π).comp
      ((SmallShiftedHom.mk₀Inv (0 : ℤ) rfl π hπ).comp
        (SmallShiftedHom.mk W g) (add_zero b)) (add_zero b) =
        SmallShiftedHom.mk W g := by
    have ha := SmallShiftedHom.comp_assoc W
      (SmallShiftedHom.mk₀ W (0 : ℤ) rfl π)
      (SmallShiftedHom.mk₀Inv (0 : ℤ) rfl π hπ)
      (SmallShiftedHom.mk W g) (add_zero (0 : ℤ)) (add_zero b)
      (show b + 0 + 0 = b by simp)
    simpa only [SmallShiftedHom.mk₀_comp_mk₀Inv,
      SmallShiftedHom.mk₀_id_comp] using ha.symm
  rw [← hL']
  calc
    _ = (SmallShiftedHom.mk W L).comp
        ((SmallShiftedHom.mk₀ W (0 : ℤ) rfl π).comp
          ((SmallShiftedHom.mk₀Inv (0 : ℤ) rfl π hπ).comp
            (SmallShiftedHom.mk W g) (add_zero b)) (add_zero b)) hab := by
      exact SmallShiftedHom.comp_assoc W (SmallShiftedHom.mk W L)
        (SmallShiftedHom.mk₀ W (0 : ℤ) rfl π)
        ((SmallShiftedHom.mk₀Inv (0 : ℤ) rfl π hπ).comp
          (SmallShiftedHom.mk W g) (add_zero b))
        (zero_add a) (add_zero b) (by simpa using hab)
    _ = (SmallShiftedHom.mk W L).comp (SmallShiftedHom.mk W g) hab :=
      congrArg (fun t => (SmallShiftedHom.mk W L).comp t hab) hcancel
    _ = _ := localized_mk_comp W L g hab

end LocalizedComposition

section SpecifiedResolutions

universe w

variable {C : Type*} [Category* C] [Abelian C] [HasExt.{w} C]
  {X Y Z : C}

set_option backward.isDefEq.respectTransparency false in
set_option backward.isDefEq.respectTransparency.types false in
set_option backward.defeqAttrib.useBackward true in
/-- A supplied whole shifted lift on the given resolutions identifies
the actual Yoneda composition of their specified extMk cocycles. -/
theorem extMk_comp_of_shifted_lift
    (P : ProjectiveResolution X) (Q : ProjectiveResolution Y) {a b c : Nat}
    (f : P.complex.X a ⟶ Y) (hf : P.complex.d (a + 1) a ≫ f = 0)
    (g : Q.complex.X b ⟶ Z) (hg : Q.complex.d (b + 1) b ≫ g = 0)
    (h : P.complex.X c ⟶ Z) (hh : P.complex.d (c + 1) c ≫ h = 0)
    (hab : a + b = c) (L : ShiftedHom P.cochainComplex Q.cochainComplex (a : ℤ))
    (hL : L.comp (ShiftedHom.mk₀ (0 : ℤ) rfl Q.π') (zero_add (a : ℤ)) =
      Cocycle.equivHomShift.symm (resolutionCocycle P f (a + 1) rfl hf))
    (hLg : L.comp
        (Cocycle.equivHomShift.symm (resolutionCocycle Q g (b + 1) rfl hg))
        (show (b : ℤ) + (a : ℤ) = (c : ℤ) by omega) =
      Cocycle.equivHomShift.symm (resolutionCocycle P h (c + 1) rfl hh)) :
    (P.extMk f (a + 1) rfl hf).comp (Q.extMk g (b + 1) rfl hg) hab =
      P.extMk h (c + 1) rfl hh := by
  let W := HomologicalComplex.quasiIso C (ComplexShape.up ℤ)
  let sf := Cocycle.equivHomShift.symm (resolutionCocycle P f (a + 1) rfl hf)
  let sg := Cocycle.equivHomShift.symm (resolutionCocycle Q g (b + 1) rfl hg)
  let sh := Cocycle.equivHomShift.symm (resolutionCocycle P h (c + 1) rfl hh)
  have hP : W P.π' := by
    change HomologicalComplex.quasiIso C (ComplexShape.up ℤ) P.π'
    rw [HomologicalComplex.mem_quasiIso_iff]
    infer_instance
  have hQ : W Q.π' := by
    change HomologicalComplex.quasiIso C (ComplexShape.up ℤ) Q.π'
    rw [HomologicalComplex.mem_quasiIso_iff]
    infer_instance
  have hsmall (A B : C) : HasSmallLocalizedShiftedHom.{w} W ℤ
      ((singleFunctor C 0).obj A) ((singleFunctor C 0).obj B) :=
    inferInstanceAs (HasSmallLocalizedShiftedHom.{w}
      (HomologicalComplex.quasiIso C (ComplexShape.up ℤ)) ℤ _ _)
  have hPto (A : C) : HasSmallLocalizedShiftedHom.{w} W ℤ
      P.cochainComplex ((singleFunctor C 0).obj A) :=
    (hasSmallLocalizedShiftedHom_iff_source W ℤ P.π' hP _).mpr (hsmall X A)
  have htoP (A : C) : HasSmallLocalizedShiftedHom.{w} W ℤ
      ((singleFunctor C 0).obj A) P.cochainComplex :=
    (hasSmallLocalizedShiftedHom_iff_target W ℤ _ P.π' hP).mpr (hsmall A X)
  have hQto (A : C) : HasSmallLocalizedShiftedHom.{w} W ℤ
      Q.cochainComplex ((singleFunctor C 0).obj A) :=
    (hasSmallLocalizedShiftedHom_iff_source W ℤ Q.π' hQ _).mpr (hsmall Y A)
  have htoQ (A : C) : HasSmallLocalizedShiftedHom.{w} W ℤ
      ((singleFunctor C 0).obj A) Q.cochainComplex :=
    (hasSmallLocalizedShiftedHom_iff_target W ℤ _ Q.π' hQ).mpr (hsmall A Y)
  have : HasSmallLocalizedShiftedHom.{w} W ℤ P.cochainComplex Q.cochainComplex :=
    (hasSmallLocalizedShiftedHom_iff_target W ℤ _ Q.π' hQ).mpr (hPto Y)
  have : HasSmallLocalizedShiftedHom.{w} W ℤ Q.cochainComplex Q.cochainComplex :=
    (hasSmallLocalizedShiftedHom_iff_target W ℤ _ Q.π' hQ).mpr (hQto Y)
  have := hPto Y
  have := hPto Z
  have := htoP X
  have := hQto Y
  have := hQto Z
  have := htoQ Y
  have := hsmall X Y
  have := hsmall X Z
  have := hsmall Y Y
  have := hsmall Y Z
  have := hsmall Z Z
  have hc : (b : ℤ) + (a : ℤ) = (c : ℤ) := by omega
  change ((SmallShiftedHom.mk₀Inv (0 : ℤ) rfl P.π' hP).comp
      (SmallShiftedHom.mk W sf) (add_zero (a : ℤ))).comp
      ((SmallShiftedHom.mk₀Inv (0 : ℤ) rfl Q.π' hQ).comp
        (SmallShiftedHom.mk W sg) (add_zero (b : ℤ))) hc =
    (SmallShiftedHom.mk₀Inv (0 : ℤ) rfl P.π' hP).comp
      (SmallShiftedHom.mk W sh) (add_zero (c : ℤ))
  calc
    _ = (SmallShiftedHom.mk₀Inv (0 : ℤ) rfl P.π' hP).comp
        ((SmallShiftedHom.mk W sf).comp
          ((SmallShiftedHom.mk₀Inv (0 : ℤ) rfl Q.π' hQ).comp
            (SmallShiftedHom.mk W sg) (add_zero (b : ℤ))) hc)
        (add_zero (c : ℤ)) := by
      exact SmallShiftedHom.comp_assoc W
        (SmallShiftedHom.mk₀Inv (0 : ℤ) rfl P.π' hP)
        (SmallShiftedHom.mk W sf)
        ((SmallShiftedHom.mk₀Inv (0 : ℤ) rfl Q.π' hQ).comp
          (SmallShiftedHom.mk W sg) (add_zero (b : ℤ)))
        (add_zero (a : ℤ)) hc (by simpa using hc)
    _ = (SmallShiftedHom.mk₀Inv (0 : ℤ) rfl P.π' hP).comp
        (SmallShiftedHom.mk W (L.comp sg hc)) (add_zero (c : ℤ)) := by
      rw [localized_comp_roof W Q.π' hQ L sf sg hc hL]
    _ = _ := by rw [hLg]

end SpecifiedResolutions

#print axioms localized_mk_comp
#print axioms localized_comp_roof
#print axioms extMk_comp_of_shifted_lift

end
end ARCExtMkYonedaLift
