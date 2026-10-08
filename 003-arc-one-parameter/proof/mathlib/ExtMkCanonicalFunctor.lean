import ExtMkMapExactFunctor

/-!
# Exact-functor transport on the specified projective-resolution cocycle

The inputs throughout are the given resolution, its specified augmentation,
and the given closed degree component. Both single-complex endpoint
comparisons and the zero-extension comparison are retained explicitly.
-/

namespace ARCExtMkCanonicalFunctor

open CategoryTheory CategoryTheory.Category CategoryTheory.Limits
open CategoryTheory.Abelian CategoryTheory.Localization
open CochainComplex CochainComplex.HomComplex
open ARCExtMkMapExactFunctor

noncomputable section

section ShiftMapping

variable {C D : Type*} [Category* C] [Category* D]
  [Preadditive C] [Preadditive D]

set_option backward.isDefEq.respectTransparency false in
/-- The shifted morphism of a cocycle retains its full component in each degree. -/
theorem equivHomShift_symm_f {K L : CochainComplex C ℤ} {n : ℤ}
    (z : Cocycle K L n) (i : ℤ) :
    (Cocycle.equivHomShift.symm z).f i = z.1.v i (i + n) rfl := by
  change z.1.v i (i + n) rfl ≫
    (L.shiftFunctorObjXIso n i (i + n) rfl).inv = _
  simp only [CochainComplex.shiftFunctorObjXIso,
    HomologicalComplex.XIsoOfEq_rfl, Iso.refl_inv, Category.comp_id]

set_option backward.isDefEq.respectTransparency false in
set_option backward.isDefEq.respectTransparency.types false in
/-- The actual cocycle image represents the image of the actual shifted morphism. -/
theorem equivHomShift_symm_mapCocycle (F : C ⥤ D) [F.Additive]
    {K L : CochainComplex C ℤ} {n : ℤ} (z : Cocycle K L n) :
    Cocycle.equivHomShift.symm (mapCocycle F z) =
      ShiftedHom.map (Cocycle.equivHomShift.symm z)
        (F.mapHomologicalComplex (ComplexShape.up ℤ)) := by
  ext i
  simp only [ShiftedHom.map, HomologicalComplex.comp_f,
    Functor.mapHomologicalComplex_map_f,
    Functor.mapHomologicalComplex_commShiftIso_hom_app_f,
    equivHomShift_symm_f]
  exact (mapCocycle_v F z i (i + n) rfl).trans (Category.comp_id _).symm

end ShiftMapping

section ResolutionCocycle

variable {C D : Type*} [Category* C] [Category* D] [Abelian C] [Abelian D]
  {X Y : C}

/-- The precise single-target cocycle used by extMk on the given resolution. -/
def resolutionCocycle (P : ProjectiveResolution X) {n : Nat}
    (f : P.complex.X n ⟶ Y) (m : Nat) (hm : n + 1 = m)
    (hf : P.complex.d m n ≫ f = 0) :
    Cocycle P.cochainComplex ((singleFunctor C 0).obj Y) (n : ℤ) :=
  Cocycle.toSingleMk ((P.cochainComplexXIso (-n) n rfl).hom ≫ f)
    (by simp) (-m) (by lia)
      (by simpa [P.cochainComplex_d _ _ m n rfl rfl])

variable (F : C ⥤ D) [F.Additive] [PreservesFiniteLimits F]
  [PreservesFiniteColimits F] [F.PreservesProjectiveObjects]

set_option backward.isDefEq.respectTransparency false in
/-- Mapping the prescribed cocycle, including its target endpoint comparison,
intertwines with the prescribed zero-extension comparison of resolutions. -/
theorem map_resolutionCocycle (P : ProjectiveResolution X) {n : Nat}
    (f : P.complex.X n ⟶ Y) (m : Nat) (hm : n + 1 = m)
    (hf : P.complex.d m n ≫ f = 0) :
    (mapCocycle F (resolutionCocycle P f m hm hf)).postcomp
        ((F.mapCochainComplexSingleFunctor 0).hom.app Y) =
      (resolutionCocycle (F.mapProjectiveResolution P) (F.map f) m hm
        (mapped_resolution_cocycle_closed F P f m hf)).precomp
          (mapProjectiveCochainIso F P).hom := by
  ext : 1
  change ((Cochain.toSingleMk ((P.cochainComplexXIso (-n) n rfl).hom ≫ f)
      (show (-n : ℤ) + n = 0 by simp)).map F).comp
        (Cochain.ofHom ((F.mapCochainComplexSingleFunctor 0).hom.app Y)) (add_zero _) =
    (Cochain.ofHom (mapProjectiveCochainIso F P).hom).comp
      (Cochain.toSingleMk
        (((F.mapProjectiveResolution P).cochainComplexXIso (-n) n rfl).hom ≫
          F.map f) (show (-n : ℤ) + n = 0 by simp)) (zero_add _)
  calc
    _ = Cochain.toSingleMk
        (F.map ((P.cochainComplexXIso (-n) n rfl).hom ≫ f))
          (show (-n : ℤ) + n = 0 by simp) :=
      map_toSingleCochain F _ _
    _ = Cochain.toSingleMk
        ((mapProjectiveCochainIso F P).hom.f (-n) ≫
          ((F.mapProjectiveResolution P).cochainComplexXIso (-n) n rfl).hom ≫ F.map f)
          (show (-n : ℤ) + n = 0 by simp) := by
      congr 1
      simp only [mapProjectiveCochainIso_hom_f, Functor.map_comp,
        Category.assoc, Iso.inv_hom_id_assoc]
    _ = _ := Cochain.toSingleMk_precomp _ _ _

/-- The full shifted cocycle square, with the actual mapped complex functor. -/
theorem map_resolutionCocycle_shifted (P : ProjectiveResolution X) {n : Nat}
    (f : P.complex.X n ⟶ Y) (m : Nat) (hm : n + 1 = m)
    (hf : P.complex.d m n ≫ f = 0) :
    ShiftedHom.map (Cocycle.equivHomShift.symm (resolutionCocycle P f m hm hf))
        (F.mapHomologicalComplex (ComplexShape.up ℤ)) ≫
          ((F.mapCochainComplexSingleFunctor 0).hom.app Y)⟦(n : ℤ)⟧' =
      (mapProjectiveCochainIso F P).hom ≫
        Cocycle.equivHomShift.symm
          (resolutionCocycle (F.mapProjectiveResolution P) (F.map f) m hm
            (mapped_resolution_cocycle_closed F P f m hf)) := by
  have h := congrArg Cocycle.equivHomShift.symm
    (map_resolutionCocycle F P f m hm hf)
  simpa only [Cocycle.equivHomShift_symm_postcomp,
    Cocycle.equivHomShift_symm_precomp, equivHomShift_symm_mapCocycle] using h

end ResolutionCocycle

section CanonicalExt

universe w w'

variable {C D : Type*} [Category* C] [Category* D] [Abelian C] [Abelian D]
  [HasExt.{w} C] [HasExt.{w'} D]
  (F : C ⥤ D) [F.Additive] [PreservesFiniteLimits F]
  [PreservesFiniteColimits F] [F.PreservesProjectiveObjects] {X Y : C}

set_option backward.isDefEq.respectTransparency false in
set_option backward.isDefEq.respectTransparency.types false in
set_option backward.defeqAttrib.useBackward true in
/-- The canonical exact-functor map sends extMk on the given resolution to
extMk on that resolution's actual functor image, in every degree. -/
theorem mapExactFunctor_extMk (P : ProjectiveResolution X) {n : Nat}
    (f : P.complex.X n ⟶ Y) (m : Nat) (hm : n + 1 = m)
    (hf : P.complex.d m n ≫ f = 0) :
    (P.extMk f m hm hf).mapExactFunctor F =
      (F.mapProjectiveResolution P).extMk (F.map f) m hm
        (mapped_resolution_cocycle_closed F P f m hf) := by
  let Φ := F.mapHomologicalComplexUpToQuasiIsoLocalizerMorphism (ComplexShape.up ℤ)
  let ψ := mapProjectiveCochainIso F P
  let σX : (F.mapHomologicalComplex (ComplexShape.up ℤ)).obj
      ((singleFunctor C 0).obj X) ≅ (singleFunctor D 0).obj (F.obj X) :=
    (F.mapCochainComplexSingleFunctor 0).app X
  let σY : (F.mapHomologicalComplex (ComplexShape.up ℤ)).obj
      ((singleFunctor C 0).obj Y) ≅ (singleFunctor D 0).obj (F.obj Y) :=
    (F.mapCochainComplexSingleFunctor 0).app Y
  let Q := F.mapProjectiveResolution P
  let z := resolutionCocycle P f m hm hf
  let z' := resolutionCocycle Q (F.map f) m hm
    (mapped_resolution_cocycle_closed F P f m hf)
  let WC := HomologicalComplex.quasiIso C (ComplexShape.up ℤ)
  let WD := HomologicalComplex.quasiIso D (ComplexShape.up ℤ)
  have hP : WC P.π' := by
    change HomologicalComplex.quasiIso C (ComplexShape.up ℤ) P.π'
    rw [HomologicalComplex.mem_quasiIso_iff]
    infer_instance
  have hQ : WD Q.π' := by
    change HomologicalComplex.quasiIso D (ComplexShape.up ℤ) Q.π'
    rw [HomologicalComplex.mem_quasiIso_iff]
    infer_instance
  have hsmallC (A B : C) : HasSmallLocalizedShiftedHom.{w} WC ℤ
      ((singleFunctor C 0).obj A) ((singleFunctor C 0).obj B) :=
    inferInstanceAs (HasSmallLocalizedShiftedHom.{w}
      (HomologicalComplex.quasiIso C (ComplexShape.up ℤ)) ℤ _ _)
  have hsmallD (A B : D) : HasSmallLocalizedShiftedHom.{w'} WD ℤ
      ((singleFunctor D 0).obj A) ((singleFunctor D 0).obj B) :=
    inferInstanceAs (HasSmallLocalizedShiftedHom.{w'}
      (HomologicalComplex.quasiIso D (ComplexShape.up ℤ)) ℤ _ _)
  have hPC (A : C) : HasSmallLocalizedShiftedHom.{w} WC ℤ
      P.cochainComplex ((singleFunctor C 0).obj A) :=
    (hasSmallLocalizedShiftedHom_iff_source WC ℤ P.π' hP _).mpr (hsmallC X A)
  have hCP (A : C) : HasSmallLocalizedShiftedHom.{w} WC ℤ
      ((singleFunctor C 0).obj A) P.cochainComplex :=
    (hasSmallLocalizedShiftedHom_iff_target WC ℤ _ P.π' hP).mpr (hsmallC A X)
  have : HasSmallLocalizedShiftedHom.{w} WC ℤ P.cochainComplex P.cochainComplex :=
    (hasSmallLocalizedShiftedHom_iff_target WC ℤ _ P.π' hP).mpr (hPC X)
  have := hPC X
  have := hPC Y
  have := hCP X
  have hQD (A : D) : HasSmallLocalizedShiftedHom.{w'} WD ℤ
      Q.cochainComplex ((singleFunctor D 0).obj A) :=
    (hasSmallLocalizedShiftedHom_iff_source WD ℤ Q.π' hQ _).mpr (hsmallD (F.obj X) A)
  have hDQ (A : D) : HasSmallLocalizedShiftedHom.{w'} WD ℤ
      ((singleFunctor D 0).obj A) Q.cochainComplex :=
    (hasSmallLocalizedShiftedHom_iff_target WD ℤ _ Q.π' hQ).mpr (hsmallD A (F.obj X))
  have : HasSmallLocalizedShiftedHom.{w'} WD ℤ Q.cochainComplex Q.cochainComplex :=
    (hasSmallLocalizedShiftedHom_iff_target WD ℤ _ Q.π' hQ).mpr (hQD (F.obj X))
  have := hQD (F.obj X)
  have := hQD (F.obj Y)
  have := hDQ (F.obj X)
  have haug : Φ.smallShiftedHomMap ψ σX (SmallShiftedHom.mk₀ WC (0 : ℤ) rfl P.π') =
      SmallShiftedHom.mk₀ WD (0 : ℤ) rfl Q.π' := by
    rw [Φ.smallShiftedHomMap_mk₀]
    congr 1
    change ψ.inv ≫ (F.mapHomologicalComplex (ComplexShape.up ℤ)).map P.π' ≫
      σX.hom = Q.π'
    calc
      _ = ψ.inv ≫ (ψ.hom ≫ Q.π') :=
        congrArg (fun t => ψ.inv ≫ t) (mapProjectiveCochainIso_hom_comp_π' F P).symm
      _ = _ := by simp only [Iso.inv_hom_id_assoc]
  have hcocycle : Φ.smallShiftedHomMap ψ σY
      (SmallShiftedHom.mk WC (Cocycle.equivHomShift.symm z)) =
        SmallShiftedHom.mk WD (Cocycle.equivHomShift.symm z') := by
    rw [Φ.smallShiftedHomMap_mk, ShiftedHom.mk₀_comp, ShiftedHom.comp_mk₀]
    congr 1
    change ψ.inv ≫
      ShiftedHom.map (Cocycle.equivHomShift.symm z)
        (F.mapHomologicalComplex (ComplexShape.up ℤ)) ≫
        σY.hom⟦(n : ℤ)⟧' = Cocycle.equivHomShift.symm z'
    calc
      _ = ψ.inv ≫ (ψ.hom ≫ Cocycle.equivHomShift.symm z') :=
        congrArg (fun t => ψ.inv ≫ t) (map_resolutionCocycle_shifted F P f m hm hf)
      _ = _ := by
        simp only [Iso.inv_hom_id_assoc]
        rfl
  have hcancelP : (SmallShiftedHom.mk₀ WC (0 : ℤ) rfl P.π').comp
      ((SmallShiftedHom.mk₀Inv (0 : ℤ) rfl P.π' hP).comp
        (SmallShiftedHom.mk WC (Cocycle.equivHomShift.symm z)) (add_zero _))
      (add_zero _) = SmallShiftedHom.mk WC (Cocycle.equivHomShift.symm z) := by
    have ha := SmallShiftedHom.comp_assoc WC
      (SmallShiftedHom.mk₀ WC (0 : ℤ) rfl P.π')
      (SmallShiftedHom.mk₀Inv (0 : ℤ) rfl P.π' hP)
      (SmallShiftedHom.mk WC (Cocycle.equivHomShift.symm z))
      (add_zero (0 : ℤ)) (add_zero (n : ℤ))
      (show (n : ℤ) + 0 + 0 = (n : ℤ) by simp)
    simpa only [SmallShiftedHom.mk₀_comp_mk₀Inv,
      SmallShiftedHom.mk₀_id_comp] using ha.symm
  have hcancelQ : (SmallShiftedHom.mk₀ WD (0 : ℤ) rfl Q.π').comp
      ((SmallShiftedHom.mk₀Inv (0 : ℤ) rfl Q.π' hQ).comp
        (SmallShiftedHom.mk WD (Cocycle.equivHomShift.symm z')) (add_zero _))
      (add_zero _) = SmallShiftedHom.mk WD (Cocycle.equivHomShift.symm z') := by
    have ha := SmallShiftedHom.comp_assoc WD
      (SmallShiftedHom.mk₀ WD (0 : ℤ) rfl Q.π')
      (SmallShiftedHom.mk₀Inv (0 : ℤ) rfl Q.π' hQ)
      (SmallShiftedHom.mk WD (Cocycle.equivHomShift.symm z'))
      (add_zero (0 : ℤ)) (add_zero (n : ℤ))
      (show (n : ℤ) + 0 + 0 = (n : ℤ) by simp)
    simpa only [SmallShiftedHom.mk₀_comp_mk₀Inv,
      SmallShiftedHom.mk₀_id_comp] using ha.symm
  apply (SmallShiftedHom.precompEquiv Q.π' hQ).injective
  change (SmallShiftedHom.mk₀ WD (0 : ℤ) rfl Q.π').comp
      (Φ.smallShiftedHomMap σX σY
        ((SmallShiftedHom.mk₀Inv (0 : ℤ) rfl P.π' hP).comp
            (SmallShiftedHom.mk WC (Cocycle.equivHomShift.symm z)) (add_zero _)))
        (add_zero _) =
    (SmallShiftedHom.mk₀ WD (0 : ℤ) rfl Q.π').comp
      ((SmallShiftedHom.mk₀Inv (0 : ℤ) rfl Q.π' hQ).comp
          (SmallShiftedHom.mk WD (Cocycle.equivHomShift.symm z')) (add_zero _))
        (add_zero _)
  calc
    _ = Φ.smallShiftedHomMap ψ σY
        (SmallShiftedHom.mk WC (Cocycle.equivHomShift.symm z)) := by
      rw [← haug, ← Φ.smallShiftedHomMap_comp ψ σX σY]
      exact congrArg (Φ.smallShiftedHomMap ψ σY) hcancelP
    _ = SmallShiftedHom.mk WD (Cocycle.equivHomShift.symm z') := hcocycle
    _ = _ := hcancelQ.symm

end CanonicalExt

#print axioms equivHomShift_symm_f
#print axioms equivHomShift_symm_mapCocycle
#print axioms resolutionCocycle
#print axioms map_resolutionCocycle
#print axioms map_resolutionCocycle_shifted
#print axioms mapExactFunctor_extMk

end
end ARCExtMkCanonicalFunctor
