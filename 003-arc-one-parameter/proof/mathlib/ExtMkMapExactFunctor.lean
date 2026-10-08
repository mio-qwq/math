import ExtMkExactFunctor
import Mathlib.Algebra.Homology.DerivedCategory.Ext.Map

/-!
# The specified mapped resolution and the exact-functor cocycle interfaces

The comparisons here retain the given projective resolution, its actual
augmentation and the cocycle on its specified degree. Mapping is the
installed homological-complex functor, not another choice of resolution.

These are intermediate interfaces for the canonical mapExactFunctor/extMk
identity. The final equality in localized shifted Hom is not asserted by
this file. In particular, these interfaces alone do not calculate an Ext
eigenvalue.
-/

namespace ARCExtMkMapExactFunctor

open CategoryTheory CategoryTheory.Category CategoryTheory.Limits
open CategoryTheory.Abelian CochainComplex CochainComplex.HomComplex
open ARCExtMkExactFunctor

noncomputable section

section CocycleMapping

variable {C D : Type*} [Category* C] [Category* D]
  [Preadditive C] [Preadditive D]
  (F : C ⥤ D) [F.Additive]

/-- The actual additive-functor image of every Hom-complex cocycle. -/
def mapCocycle {K L : CochainComplex C ℤ} {n : ℤ} (z : Cocycle K L n) :
    Cocycle ((F.mapHomologicalComplex _).obj K)
      ((F.mapHomologicalComplex _).obj L) n :=
  Cocycle.mk (z.1.map F) (n + 1) rfl (by
    rw [δ_map, z.δ_eq_zero, Cochain.map_zero])

/-- Mapping a cocycle keeps every component as the functor image. -/
theorem mapCocycle_v {K L : CochainComplex C ℤ} {n : ℤ} (z : Cocycle K L n)
    (p q : ℤ) (hpq : p + n = q) :
    (mapCocycle F z).1.v p q hpq = F.map (z.1.v p q hpq) := rfl

/-- Mapping a single-target cochain, then using the specified target
single-complex comparison, gives the single cochain of the mapped component. -/
theorem map_toSingleCochain [HasZeroObject C] [HasZeroObject D]
    {K : CochainComplex C ℤ} {X : C} {p q n : ℤ}
    (f : K.X p ⟶ X) (h : p + n = q) :
    ((Cochain.toSingleMk f h).map F).comp
      (Cochain.ofHom ((HomologicalComplex.singleMapHomologicalComplex F
        (ComplexShape.up ℤ) q).hom.app X)) (add_zero n) =
        Cochain.toSingleMk (F.map f) h := by
  apply (Cochain.toSingleEquiv h).injective
  simp [Cochain.toSingleEquiv, Cochain.map_v]

/-- The same identity for actual closed single-target cocycles, including
their full differential condition and their target endpoint comparison. -/
theorem map_toSingleCocycle [HasZeroObject C] [HasZeroObject D]
    {K : CochainComplex C ℤ} {X : C} {p q n : ℤ}
    (f : K.X p ⟶ X) (h : p + n = q) (p' : ℤ) (hp' : p' + 1 = p)
    (hf : K.d p' p ≫ f = 0) :
    (mapCocycle F (Cocycle.toSingleMk f h p' hp' hf)).postcomp
      ((HomologicalComplex.singleMapHomologicalComplex F
        (ComplexShape.up ℤ) q).hom.app X) =
        Cocycle.toSingleMk (F.map f) h p' hp' (by
          change F.map (K.d p' p) ≫ F.map f = 0
          rw [← F.map_comp, hf, F.map_zero]) := by
  ext : 1
  exact map_toSingleCochain F f h

end CocycleMapping

section SpecifiedResolution

variable {C D : Type*} [Category* C] [Category* D] [Abelian C] [Abelian D]
  (F : C ⥤ D) [F.Additive] [PreservesFiniteLimits F] [PreservesFiniteColimits F]
  [F.PreservesProjectiveObjects] {X Y : C}

/-- Mapping and zero-extending the specified resolution commute as actual
complexes, with the canonical zero-object comparison outside its support. -/
def mapProjectiveCochainIso (P : ProjectiveResolution X) :
    (F.mapHomologicalComplex (ComplexShape.up ℤ)).obj P.cochainComplex ≅
      (F.mapProjectiveResolution P).cochainComplex :=
  mapExtendIso F P.complex ComplexShape.embeddingDownNat

/-- At every retained degree, the comparison is exactly the two specified
degree-identification maps, with the first transported by F. -/
theorem mapProjectiveCochainIso_hom_f (P : ProjectiveResolution X) (n : Nat) :
    (mapProjectiveCochainIso F P).hom.f (-n) =
      F.map (P.cochainComplexXIso (-n) n rfl).hom ≫
        ((F.mapProjectiveResolution P).cochainComplexXIso (-n) n rfl).inv := by
  exact mapExtendIso_hom_f F P.complex ComplexShape.embeddingDownNat rfl

set_option backward.defeqAttrib.useBackward true in
set_option backward.isDefEq.respectTransparency false in
set_option backward.isDefEq.respectTransparency.types false in
/-- Compatibility with the augmentation is an identity of full complex
morphisms, including the exact single-target endpoint comparison. -/
theorem mapProjectiveCochainIso_hom_comp_π' (P : ProjectiveResolution X) :
    (mapProjectiveCochainIso F P).hom ≫ (F.mapProjectiveResolution P).π' =
      (F.mapHomologicalComplex (ComplexShape.up ℤ)).map P.π' ≫
        (F.mapCochainComplexSingleFunctor 0).hom.app X := by
  apply HomologicalComplex.to_single_hom_ext
  have hzero : (mapProjectiveCochainIso F P).hom.f 0 =
      F.map (P.cochainComplexXIso 0 0 rfl).hom ≫
        ((F.mapProjectiveResolution P).cochainComplexXIso 0 0 rfl).inv :=
    mapProjectiveCochainIso_hom_f F P 0
  have hπzero : (F.mapProjectiveResolution P).π.f 0 = F.map (P.π.f 0) := by
    simp only [Functor.mapProjectiveResolution_π, HomologicalComplex.comp_f,
      Functor.mapHomologicalComplex_map_f,
      HomologicalComplex.singleMapHomologicalComplex_hom_app_self,
      ChainComplex.single₀ObjXSelf, Iso.refl_hom, Iso.refl_inv]
    change F.map (P.π.f 0) ≫
        F.map (𝟙 (((ChainComplex.single₀ C).obj X).X 0)) ≫
          𝟙 (F.obj (((ChainComplex.single₀ C).obj X).X 0)) = F.map (P.π.f 0)
    rw [F.map_id, Category.comp_id, Category.comp_id]
  have hsingle : F.map (HomologicalComplex.singleObjXSelf (ComplexShape.up ℤ) 0 X).inv ≫
      F.map (HomologicalComplex.singleObjXSelf (ComplexShape.up ℤ) 0 X).hom =
        𝟙 (F.obj X) := by
    rw [← F.map_comp, Iso.inv_hom_id, F.map_id]
  simp only [HomologicalComplex.comp_f, Functor.mapHomologicalComplex_map_f,
    ProjectiveResolution.π'_f_zero, hzero, hπzero,
    Functor.mapCochainComplexSingleFunctor,
    HomologicalComplex.singleMapHomologicalComplex_hom_app_self,
    Functor.map_comp, Category.assoc, Iso.inv_hom_id_assoc,
    reassoc_of% hsingle]

/-- The prescribed mapped degree-n cocycle is closed on the prescribed
mapped projective resolution; no resolution choice changes the input. -/
theorem mapped_resolution_cocycle_closed (P : ProjectiveResolution X) {n : Nat}
    (f : P.complex.X n ⟶ Y) (m : Nat)
    (hf : P.complex.d m n ≫ f = 0) :
    (F.mapProjectiveResolution P).complex.d m n ≫ F.map f = 0 := by
  change F.map (P.complex.d m n) ≫ F.map f = 0
  rw [← F.map_comp, hf, F.map_zero]

end SpecifiedResolution

section LocalizedRoof

open CategoryTheory.Localization

universe w v u

variable {C : Type u} [Category.{v} C] [Abelian C] [HasExt.{w} C]
  {X Y : C}

/-- The extMk constructor uses exactly the given augmentation inverse
and exactly the given single-target cocycle in localized shifted Hom. -/
theorem extMk_smallShiftedRoof (P : ProjectiveResolution X) {n : Nat}
    (f : P.complex.X n ⟶ Y) (m : Nat) (hm : n + 1 = m)
    (hf : P.complex.d m n ≫ f = 0) :
    P.extMk f m hm hf =
      (SmallShiftedHom.mk₀Inv 0 rfl P.π'
        (by rw [HomologicalComplex.mem_quasiIso_iff]; infer_instance)).comp
          (SmallShiftedHom.mk _ (Cocycle.equivHomShift.symm
            (Cocycle.toSingleMk ((P.cochainComplexXIso (-n) n rfl).hom ≫ f)
              (by simp) (-m) (by lia)
                (by simpa [P.cochainComplex_d _ _ m n rfl rfl]))))
          (add_zero (n : ℤ)) := by
  rfl

end LocalizedRoof

#print axioms mapCocycle
#print axioms mapCocycle_v
#print axioms map_toSingleCochain
#print axioms map_toSingleCocycle
#print axioms mapProjectiveCochainIso
#print axioms mapProjectiveCochainIso_hom_f
#print axioms mapProjectiveCochainIso_hom_comp_π'
#print axioms mapped_resolution_cocycle_closed
#print axioms extMk_smallShiftedRoof

end
end ARCExtMkMapExactFunctor
