import TwentyDimDualScaleModule
import FiniteFreeBarDualScaleSemilinear

/-!
# The actual specified resolution and its inverse-restriction twist

The inverse semilinear scaling becomes an actual A-linear morphism into
the restricted module. Its components form a chain map in every degree,
compatible with the underlying-identity character isomorphism. The target
is the functor image of the specified projective resolution.

This file does not identify the functor map on Ext with extMk. That
generic naturality bridge remains a separate obligation.
-/

namespace ARCFiniteFreeBarDualScaleComparison

open CategoryTheory CategoryTheory.Category CategoryTheory.Limits
open ARCTwentyDimAlgebra ARCTwentyDimCharacters ARCTwentyDimDualScale
open ARCTwentyDimDualScaleModule ARCFiniteFreeBarModules
open ARCFiniteFreeBarAugmentation ARCFiniteFreeBarRecursive
open ARCFiniteFreeBarProjectiveResolution ARCFiniteFreeBarDualScaleSemilinear
open scoped ModuleCat.Algebra

universe u
variable {R : Type u} [CommRing R] [CharP R 2]

noncomputable section

/-- Semilinearity becomes actual A-linearity into the inverse-restricted term. -/
def twistTermHom (q : R) (H : Rˣ) (n : Nat) :
    barModule q n ⟶ (dualScaleFunctor q H).obj (barModule q n) :=
  ModuleCat.ofHom
    (X := barModule q n)
    (Y := (dualScaleFunctor q H).obj (barModule q n))
    { toFun := termScale q H⁻¹ n
      map_add' := (termScale q H⁻¹ n).map_add
      map_smul' a v := by
        change termScale q H⁻¹ n (a • v) =
          (dualScale q H).symm a • termScale q H⁻¹ n v
        rw [dualScale_symm]
        exact termScale_algebra_smul q H⁻¹ n a v }

@[simp] theorem twistTermHom_apply (q : R) (H : Rˣ) (n : Nat)
    (v : BarTerm q n) : twistTermHom q H n v = termScale q H⁻¹ n v := rfl

/-- The actual functor image of the specified resolution, retaining its maps. -/
def twistedResolution (q : R) (H : Rˣ) :
    ProjectiveResolution
      ((dualScaleFunctor q H).obj (characterObject q (fCharacter q))) :=
  (dualScaleFunctor q H).mapProjectiveResolution
    (projectiveResolution q (fCharacter q))

@[simp] theorem twistedResolution_X (q : R) (H : Rˣ) (n : Nat) :
    (twistedResolution q H).complex.X n =
      (dualScaleFunctor q H).obj (barModule q n) := rfl

@[simp] theorem twistedResolution_d (q : R) (H : Rˣ) (n : Nat) :
    (twistedResolution q H).complex.d (n + 1) n =
      (dualScaleFunctor q H).map
        (ModuleCat.ofHom (recursiveBoundary q (fCharacter q) n)) := by
  change (dualScaleFunctor q H).map
    ((projectiveResolution q (fCharacter q)).complex.d (n + 1) n) = _
  rw [projectiveResolution_d]
  rfl

/-- An actual chain morphism on the complete specified recursive complex. -/
def twistChainMap (q : R) (H : Rˣ) :
    (projectiveResolution q (fCharacter q)).complex ⟶
      (twistedResolution q H).complex where
  f n := twistTermHom q H n
  comm' i j hij := by
    change j + 1 = i at hij
    subst i
    rw [projectiveResolution_d, twistedResolution_d]
    apply ModuleCat.hom_ext
    ext v
    exact (termScale_recursiveBoundary q H⁻¹ j v).symm

@[simp] theorem twistChainMap_f (q : R) (H : Rˣ) (n : Nat) :
    (twistChainMap q H).f n = twistTermHom q H n := rfl

set_option backward.isDefEq.respectTransparency false in
/-- The functor image's zero augmentation is precisely the mapped augmentation. -/
@[simp] theorem twistedResolution_π_f_zero (q : R) (H : Rˣ) :
    (twistedResolution q H).π.f 0 =
      (dualScaleFunctor q H).map (ModuleCat.ofHom (augmentation q (fCharacter q))) := by
  simp [twistedResolution, Functor.mapProjectiveResolution_π,
    HomologicalComplex.singleMapHomologicalComplex_hom_app_self]

/-- The all-degree chain map lifts the actual character endpoint identity iso. -/
def twistResolutionHom (q : R) (H : Rˣ) :
    ProjectiveResolution.Hom
      (projectiveResolution q (fCharacter q)) (twistedResolution q H)
      (fCharacterTwistIso q H).inv where
  hom := twistChainMap q H
  hom_f_zero_comp_π_f_zero := by
    rw [twistChainMap_f, twistedResolution_π_f_zero,
      projectiveResolution_π_f_zero, ChainComplex.single₀_map_f_zero]
    apply ModuleCat.hom_ext
    ext v
    exact augmentation_termScale_zero q H⁻¹ v

/-- The complete comparison is a quasi-isomorphism, since it lifts the
actual endpoint isomorphism between the two augmented resolutions. -/
theorem twistChainMap_quasiIso (q : R) (H : Rˣ) :
    QuasiIso (twistChainMap q H) := by
  have h : QuasiIso ((twistChainMap q H) ≫ (twistedResolution q H).π) := by
    change QuasiIso ((twistResolutionHom q H).hom ≫ (twistedResolution q H).π)
    rw [(twistResolutionHom q H).hom_comp_π]
    infer_instance
  let := h
  exact quasiIso_of_comp_right
    (twistChainMap q H) (twistedResolution q H).π

#print axioms twistTermHom
#print axioms twistTermHom_apply
#print axioms twistedResolution
#print axioms twistedResolution_X
#print axioms twistedResolution_d
#print axioms twistChainMap
#print axioms twistChainMap_f
#print axioms twistedResolution_π_f_zero
#print axioms twistResolutionHom
#print axioms twistChainMap_quasiIso

end
end ARCFiniteFreeBarDualScaleComparison
