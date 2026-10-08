import Mathlib.CategoryTheory.Abelian.Projective.Ext
import Mathlib.Algebra.Homology.DerivedCategory.Ext.Linear
import Mathlib.Algebra.Homology.Embedding.Extend
import Mathlib.CategoryTheory.Limits.Preserves.Shapes.Zero

/-!
# General interfaces for computing mapped projective-resolution Ext classes

This file develops the scalar and extension-of-complex interfaces needed to
compare `ProjectiveResolution.extMk` with exact-functor mapping. The bridge
with `Ext.mapExactFunctor` itself is a separate theorem still to be added.
-/

namespace ARCExtMkExactFunctor

open CategoryTheory CategoryTheory.Limits CategoryTheory.Abelian

universe w v u

noncomputable section

section Scalar

variable {R : Type*} [Ring R]
  {C : Type u} [Category.{v} C] [Abelian C] [Linear R C] [HasExt.{w} C]
  {X Y : C}

/-- The cocycle constructor is scalar compatible in every linear abelian
category. This uses the actual Ext module structure and target composition. -/
theorem extMk_smul (P : ProjectiveResolution X) {n : Nat}
    (f : P.complex.X n ⟶ Y) (m : Nat) (hm : n + 1 = m)
    (hf : P.complex.d m n ≫ f = 0) (r : R) :
    P.extMk (r • f) m hm (by simp [hf]) = r • P.extMk f m hm hf := by
  rw [Ext.smul_eq_comp_mk₀, ProjectiveResolution.extMk_comp_mk₀]
  simp only [Linear.comp_smul, Category.comp_id]

end Scalar

section Extend

set_option backward.isDefEq.respectTransparency false

variable {C D : Type*} [Category* C] [Category* D]
  [HasZeroMorphisms C] [HasZeroMorphisms D]
  [HasZeroObject C] [HasZeroObject D]
  {ι ι' : Type*} {c : ComplexShape ι} {c' : ComplexShape ι'}
  (F : C ⥤ D) [F.PreservesZeroMorphisms]

/-- Mapping the object in an optional extension degree commutes with its
construction; outside the original support this uses the canonical zero iso. -/
def optionMapXIso (K : HomologicalComplex C c) :
    ∀ i : Option ι, F.obj (HomologicalComplex.extend.X K i) ≅
      HomologicalComplex.extend.X ((F.mapHomologicalComplex c).obj K) i
  | none => F.mapZeroObject
  | some _ => Iso.refl _

theorem optionMapXIso_hom_d (K : HomologicalComplex C c) (i j : Option ι) :
    (optionMapXIso F K i).hom ≫
        HomologicalComplex.extend.d ((F.mapHomologicalComplex c).obj K) i j =
      F.map (HomologicalComplex.extend.d K i j) ≫ (optionMapXIso F K j).hom := by
  cases i <;> cases j <;>
    simp [optionMapXIso, HomologicalComplex.extend.d,
      HomologicalComplex.extend.X, Functor.mapHomologicalComplex]

theorem optionMapXIso_naturality {K L : HomologicalComplex C c} (φ : K ⟶ L)
    (i : Option ι) :
    F.map (HomologicalComplex.extend.mapX φ i) ≫ (optionMapXIso F L i).hom =
      (optionMapXIso F K i).hom ≫
        HomologicalComplex.extend.mapX ((F.mapHomologicalComplex c).map φ) i := by
  cases i <;>
    simp [optionMapXIso, HomologicalComplex.extend.mapX,
      HomologicalComplex.extend.X, Functor.mapHomologicalComplex]

private theorem optionMapXIso_hom_supported (K : HomologicalComplex C c)
    {a : Option ι} {i : ι} (ha : a = some i) :
    (optionMapXIso F K a).hom =
      F.map (HomologicalComplex.extend.XIso K ha).hom ≫
        (HomologicalComplex.extend.XIso ((F.mapHomologicalComplex c).obj K) ha).inv := by
  subst a
  simp [optionMapXIso, HomologicalComplex.extend.XIso, HomologicalComplex.extend.X]

/-- Every zero-morphism-preserving functor commutes with extension of a
homological complex along an embedding of its degree shape, up to a genuine
complex isomorphism. No projective resolution or module specialization is
assumed in this statement. -/
def mapExtendIso (K : HomologicalComplex C c) (e : c.Embedding c') :
    (F.mapHomologicalComplex c').obj (K.extend e) ≅
      ((F.mapHomologicalComplex c).obj K).extend e :=
  HomologicalComplex.Hom.isoOfComponents
    (fun j => optionMapXIso F K (e.r j))
    (fun i j _ => optionMapXIso_hom_d F K (e.r i) (e.r j))

theorem mapExtendIso_naturality {K L : HomologicalComplex C c} (φ : K ⟶ L)
    (e : c.Embedding c') :
    (F.mapHomologicalComplex c').map (HomologicalComplex.extendMap φ e) ≫
        (mapExtendIso F L e).hom =
      (mapExtendIso F K e).hom ≫
        HomologicalComplex.extendMap ((F.mapHomologicalComplex c).map φ) e := by
  ext j
  exact optionMapXIso_naturality F φ (e.r j)

/-- The complex isomorphisms constitute a natural comparison of the two
orders of applying a functor and extension by zero. -/
def mapExtendNatIso (e : c.Embedding c') :
    e.extendFunctor C ⋙ F.mapHomologicalComplex c' ≅
      F.mapHomologicalComplex c ⋙ e.extendFunctor D :=
  NatIso.ofComponents (fun K => mapExtendIso F K e)
    (fun φ => mapExtendIso_naturality F φ e)

/-- At a degree in the original support, the extension/map comparison has
the corresponding identity component after the canonical degree identifications. -/
theorem mapExtendIso_hom_f (K : HomologicalComplex C c) (e : c.Embedding c')
    {i : ι} {j : ι'} (h : e.f i = j) :
    (mapExtendIso F K e).hom.f j =
      F.map (K.extendXIso e h).hom ≫
        (((F.mapHomologicalComplex c).obj K).extendXIso e h).inv := by
  change (optionMapXIso F K (e.r j)).hom =
    F.map (HomologicalComplex.extend.XIso K (e.r_eq_some h)).hom ≫
      (HomologicalComplex.extend.XIso ((F.mapHomologicalComplex c).obj K)
        (e.r_eq_some h)).inv
  exact optionMapXIso_hom_supported F K (e.r_eq_some h)

end Extend

#print axioms extMk_smul
#print axioms optionMapXIso
#print axioms optionMapXIso_hom_d
#print axioms optionMapXIso_naturality
#print axioms mapExtendIso
#print axioms mapExtendIso_naturality
#print axioms mapExtendNatIso
#print axioms mapExtendIso_hom_f

end
end ARCExtMkExactFunctor
