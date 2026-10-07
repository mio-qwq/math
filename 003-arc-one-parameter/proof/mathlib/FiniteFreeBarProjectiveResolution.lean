import FiniteFreeBarRecursiveExact
import Mathlib.Algebra.Category.ModuleCat.Abelian
import Mathlib.Algebra.Homology.ShortComplex.ModuleCat
import Mathlib.CategoryTheory.Preadditive.Projective.Resolution

/-!
The specified recursive finite free terms and differentials, assembled as
an actual chain complex in the category of left modules over the actual
noncommutative algebra. Its actual character augmentation is a
quasi-isomorphism, and all specified terms are projective. They give a
Mathlib ProjectiveResolution of the actual character module.

No automatically chosen projective resolution replaces these terms.
This file does not prove the comparison to the earlier low-degree maps,
construct an Ext class, or assert the ARC homological realization.
-/

namespace ARCFiniteFreeBarProjectiveResolution

open CategoryTheory CategoryTheory.Category CategoryTheory.Limits
open ARCTwentyDimAlgebra ARCFiniteFreeBarModules ARCFiniteFreeBarAugmentation
open ARCFiniteFreeBarRecursive ARCFiniteFreeBarRecursiveExact ARCCharacterModule

universe u
variable {R : Type u} [CommRing R] [CharP R 2]

noncomputable section

variable (q : R) (eps : TableAlgebra q →ₐ[R] R)

/-- The actual character module, retained as an object of the left module category. -/
def characterObject : ModuleCat.{u} (TableAlgebra q) :=
  ModuleCat.of (TableAlgebra q) (CharacterModule eps)

/-- The specified recursive differential as an actual categorical module morphism. -/
def recursiveDifferential (n : Nat) : barModule q (n + 1) ⟶ barModule q n :=
  ModuleCat.ofHom (recursiveBoundary q eps n)

/-- The actual recursive free chain complex, without changing any term or map. -/
def recursiveComplex : ChainComplex (ModuleCat.{u} (TableAlgebra q)) ℕ :=
  ChainComplex.of (barModule q) (recursiveDifferential q eps)
    (fun n => ModuleCat.hom_ext (recursiveBoundary_comp q eps n))

@[simp] theorem recursiveComplex_X (n : Nat) :
    (recursiveComplex q eps).X n = barModule q n := rfl

@[simp] theorem recursiveComplex_d (n : Nat) :
    (recursiveComplex q eps).d (n + 1) n = recursiveDifferential q eps n := by
  simp only [recursiveComplex, ChainComplex.of_d]

set_option backward.isDefEq.respectTransparency false in
/-- All positive-degree homology vanishes by the already proved full kernel/image identity. -/
theorem recursiveComplex_exactAt_succ (n : Nat) :
    (recursiveComplex q eps).ExactAt (n + 1) := by
  rw [HomologicalComplex.exactAt_iff' (recursiveComplex q eps) (n + 2) (n + 1) n
    (by simp) (by simp)]
  apply (CategoryTheory.ShortComplex.moduleCat_exact_iff_range_eq_ker _).mpr
  simpa only [HomologicalComplex.shortComplexFunctor'_obj_f,
    HomologicalComplex.shortComplexFunctor'_obj_g,
    HomologicalComplex.shortComplexFunctor'_obj_X₂, recursiveComplex_X,
    recursiveComplex_d, recursiveDifferential, barModule, ModuleCat.hom_ofHom] using
    (recursiveBoundary_ker_eq_range q eps n).symm

/-- The true augmentation, as a chain map to the actual character module in degree zero. -/
def augmentationMap : recursiveComplex q eps ⟶
    (ChainComplex.single₀ (ModuleCat.{u} (TableAlgebra q))).obj (characterObject q eps) :=
  (ChainComplex.toSingle₀Equiv (recursiveComplex q eps) (characterObject q eps)).symm
    ⟨ModuleCat.ofHom (augmentation q eps), by
      rw [recursiveComplex_d]
      exact ModuleCat.hom_ext (augmentation_comp_recursiveBoundary_zero q eps)⟩

set_option backward.isDefEq.respectTransparency false in
/-- The chain-map's zero component is exactly the specified actual augmentation. -/
@[simp] theorem augmentationMap_f_zero :
    (augmentationMap q eps).f 0 = ModuleCat.ofHom (augmentation q eps) := by
  exact ChainComplex.toSingle₀Equiv_symm_apply_f_zero _ _

/-- The actual augmented short complex. -/
def augmentedShortComplex : CategoryTheory.ShortComplex (ModuleCat.{u} (TableAlgebra q)) :=
  CategoryTheory.ShortComplex.moduleCatMk (recursiveBoundary q eps 0)
    (augmentation q eps) (augmentation_comp_recursiveBoundary_zero q eps)

theorem augmentedShortComplex_exact : (augmentedShortComplex q eps).Exact := by
  apply (CategoryTheory.ShortComplex.moduleCat_exact_iff_range_eq_ker _).mpr
  exact (augmentation_ker_eq_recursiveBoundary_zero_range q eps).symm

theorem augmentation_epi : Epi (ModuleCat.ofHom (augmentation q eps)) :=
  (ModuleCat.epi_iff_surjective _).mpr (augmentation_surjective q eps)

set_option backward.isDefEq.respectTransparency false in
/-- The augmentation is a quasi-isomorphism, including its zero-degree
exactness and surjectivity, rather than only positive-degree acyclicity. -/
theorem augmentationMap_quasiIso : QuasiIso (augmentationMap q eps) := by
  constructor
  intro n
  cases n with
  | zero =>
    rw [ChainComplex.quasiIsoAt₀_iff, CategoryTheory.ShortComplex.quasiIso_iff_of_zeros']
    · refine (CategoryTheory.ShortComplex.exact_and_epi_g_iff_of_iso ?_).2
        ⟨augmentedShortComplex_exact q eps, augmentation_epi q eps⟩
      exact CategoryTheory.ShortComplex.isoMk (Iso.refl _) (Iso.refl _) (Iso.refl _)
        (by simp [augmentedShortComplex, recursiveDifferential])
        (by simp [augmentedShortComplex])
    all_goals rfl
  | succ n =>
    rw [quasiIsoAt_iff_exactAt' (augmentationMap q eps) (n + 1)
      (ChainComplex.exactAt_succ_single_obj _ _)]
    exact recursiveComplex_exactAt_succ q eps n

/-- The actual Mathlib projective-resolution object with the specified finite
free terms, specified recursive maps and specified character augmentation. -/
def projectiveResolution : CategoryTheory.ProjectiveResolution (characterObject q eps) where
  complex := recursiveComplex q eps
  projective n := barModule_projective q n
  hasHomology _n := inferInstance
  π := augmentationMap q eps
  quasiIso := augmentationMap_quasiIso q eps

/-- Every term of the bundled resolution is the originally exhibited finite free term. -/
@[simp] theorem projectiveResolution_X (n : Nat) :
    (projectiveResolution q eps).complex.X n = barModule q n := rfl

/-- Its adjacent differential is exactly the specified recursive A-linear map. -/
@[simp] theorem projectiveResolution_d (n : Nat) :
    (projectiveResolution q eps).complex.d (n + 1) n =
      ModuleCat.ofHom (recursiveBoundary q eps n) := recursiveComplex_d q eps n

/-- The bundled resolution retains the actual specified augmentation. -/
@[simp] theorem projectiveResolution_π_f_zero :
    (projectiveResolution q eps).π.f 0 = ModuleCat.ofHom (augmentation q eps) :=
  augmentationMap_f_zero q eps

#print axioms recursiveComplex
#print axioms recursiveComplex_exactAt_succ
#print axioms augmentationMap
#print axioms augmentationMap_f_zero
#print axioms augmentedShortComplex_exact
#print axioms augmentation_epi
#print axioms augmentationMap_quasiIso
#print axioms projectiveResolution
#print axioms projectiveResolution_X
#print axioms projectiveResolution_d
#print axioms projectiveResolution_π_f_zero

end
end ARCFiniteFreeBarProjectiveResolution
