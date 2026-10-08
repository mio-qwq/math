import LowerAlgebraProjective
import Mathlib.Algebra.Category.ModuleCat.Abelian
import Mathlib.Algebra.Homology.ShortComplex.ModuleCat
import Mathlib.CategoryTheory.Preadditive.Projective.Resolution
import Mathlib.Algebra.Category.ModuleCat.Ext.HasExt
import Mathlib.CategoryTheory.Abelian.Projective.Ext

/-!
# The specified all-degree projective resolution over the actual lower algebra

The first term is the actual f-corner; every positive term is the actual
e-corner. The installed right-multiplication differentials and actual
f-character augmentation are retained. Exactness and projectivity are
assembled as a genuine Mathlib ProjectiveResolution.
Every positive actual self-Ext group of this character over the lower
algebra vanishes, using cocycle surjectivity for that specified resolution.
The regular-target Hom calculation, its right-module cohomology and the
trivial-extension derived triangle require further proofs.
-/

namespace ARCLowerAlgebraCategoricalResolution

open ARCTwentyDimAlgebra ARCCharacterModule ARCLowerAlgebraResolution
open ARCLowerAlgebraProjective
open CategoryTheory CategoryTheory.Category CategoryTheory.Limits

universe u
noncomputable section
variable {K : Type u} [Field K] [CharP K 2]

/-- Only these nonzero factors are needed for the specified right-map resolution. -/
def PowerCondition (q : K) : Prop := ∀ n : Nat, 1 + q ^ (n + 1) ≠ 0

omit [CharP K 2] in
theorem power_one (q : K) (hq : PowerCondition q) : 1 + q ≠ 0 := by
  simpa using hq 0

omit [CharP K 2] in
theorem power_two (q : K) (hq : PowerCondition q) : 1 + q ^ 2 ≠ 0 := hq 1

/-- Augmentation exactness includes every vector in the actual f-corner. -/
theorem augmentation_ker_eq_range (q : K) (hq : PowerCondition q) :
    LinearMap.ker (augmentation q) = LinearMap.range (rightU q) := by
  ext a
  constructor
  · intro ha
    have h0 : cfCoordsEquiv q a 0 = 0 := by
      have hv := congrArg CharacterModule.val ha
      exact hv
    let v : Fin 6 → K := ![cfCoordsEquiv q a 1, cfCoordsEquiv q a 2, 0, 0,
      cfCoordsEquiv q a 3 / (1 + q), 0]
    refine ⟨(ceCoordsEquiv q).symm v, ?_⟩
    apply (cfCoordsEquiv q).injective
    simp only [rightU_coords, (ceCoordsEquiv q).apply_symm_apply]
    funext i
    fin_cases i
    · simpa [v] using h0.symm
    · simp [v]
    · simp [v]
    · change (1 + q) * (cfCoordsEquiv q a 3 / (1 + q)) = cfCoordsEquiv q a 3
      rw [← mul_div_assoc, mul_div_cancel_left₀ _ (power_one q hq)]
  · rintro ⟨b, rfl⟩
    apply CharacterModule.ext
    change cfCoordsEquiv q (rightU q b) 0 = 0
    rw [rightU_coords]
    rfl

theorem augmentation_comp_rightU (q : K) :
    (augmentation q).comp (rightU q) = 0 := by
  apply LinearMap.ext
  intro a
  apply CharacterModule.ext
  change cfCoordsEquiv q (rightU q a) 0 = 0
  rw [rightU_coords]
  rfl

/-- Actual corner objects with their installed C actions. -/
def term (q : K) : Nat → ModuleCat.{u} (C q)
  | 0 => ModuleCat.of (C q) (Cf q)
  | _ + 1 => ModuleCat.of (C q) (Ce q)

def simpleObject (q : K) : ModuleCat.{u} (C q) :=
  ModuleCat.of (C q) (Simple q)

/-- Actual right multiplication by u, followed by ell_0, ell_1, ... . -/
def differential (q : K) : (n : Nat) → term q (n + 1) ⟶ term q n
  | 0 => ModuleCat.ofHom (rightU q)
  | n + 1 => ModuleCat.ofHom (rightEll q n)

theorem differential_comp (q : K) (hq : PowerCondition q) (n : Nat) :
    differential q (n + 1) ≫ differential q n = 0 := by
  cases n with
  | zero =>
    apply ModuleCat.hom_ext
    apply LinearMap.range_le_ker_iff.mp
    exact le_of_eq (rightU_ker_eq_range q (power_one q hq) (power_two q hq)).symm
  | succ n =>
    apply ModuleCat.hom_ext
    apply LinearMap.range_le_ker_iff.mp
    exact le_of_eq (rightEll_ker_eq_range q n (hq (n + 1)) (hq (n + 2))).symm

def lowerComplex (q : K) (hq : PowerCondition q) :
    ChainComplex (ModuleCat.{u} (C q)) Nat :=
  ChainComplex.of (term q) (differential q) (differential_comp q hq)

@[simp] theorem lowerComplex_X (q : K) (hq : PowerCondition q) (n : Nat) :
    (lowerComplex q hq).X n = term q n := rfl

@[simp] theorem lowerComplex_d (q : K) (hq : PowerCondition q) (n : Nat) :
    (lowerComplex q hq).d (n + 1) n = differential q n := by
  simp only [lowerComplex, ChainComplex.of_d]

set_option backward.isDefEq.respectTransparency false in
theorem lowerComplex_exactAt_succ (q : K) (hq : PowerCondition q) (n : Nat) :
    (lowerComplex q hq).ExactAt (n + 1) := by
  rw [HomologicalComplex.exactAt_iff' (lowerComplex q hq) (n + 2) (n + 1) n
    (by simp) (by simp)]
  apply (CategoryTheory.ShortComplex.moduleCat_exact_iff_range_eq_ker _).mpr
  simp only [HomologicalComplex.shortComplexFunctor'_obj_f,
    HomologicalComplex.shortComplexFunctor'_obj_g,
    lowerComplex_d]
  cases n with
  | zero => exact (rightU_ker_eq_range q (power_one q hq) (power_two q hq)).symm
  | succ n => exact (rightEll_ker_eq_range q n (hq (n + 1)) (hq (n + 2))).symm

def augmentationMap (q : K) (hq : PowerCondition q) : lowerComplex q hq ⟶
    (ChainComplex.single₀ (ModuleCat.{u} (C q))).obj (simpleObject q) :=
  (ChainComplex.toSingle₀Equiv (lowerComplex q hq) (simpleObject q)).symm
    ⟨ModuleCat.ofHom (augmentation q), by
      rw [lowerComplex_d]
      exact ModuleCat.hom_ext (augmentation_comp_rightU q)⟩

set_option backward.isDefEq.respectTransparency false in
@[simp] theorem augmentationMap_f_zero (q : K) (hq : PowerCondition q) :
    (augmentationMap q hq).f 0 = ModuleCat.ofHom (augmentation q) :=
  ChainComplex.toSingle₀Equiv_symm_apply_f_zero _ _

def augmentedShortComplex (q : K) : CategoryTheory.ShortComplex (ModuleCat.{u} (C q)) :=
  CategoryTheory.ShortComplex.moduleCatMk (rightU q) (augmentation q)
    (augmentation_comp_rightU q)

theorem augmentedShortComplex_exact (q : K) (hq : PowerCondition q) :
    (augmentedShortComplex q).Exact := by
  apply (CategoryTheory.ShortComplex.moduleCat_exact_iff_range_eq_ker _).mpr
  exact (augmentation_ker_eq_range q hq).symm

theorem augmentation_epi (q : K) : Epi (ModuleCat.ofHom (augmentation q)) :=
  (ModuleCat.epi_iff_surjective _).mpr (augmentation_surjective q)

set_option backward.isDefEq.respectTransparency false in
theorem augmentationMap_quasiIso (q : K) (hq : PowerCondition q) :
    QuasiIso (augmentationMap q hq) := by
  constructor
  intro n
  cases n with
  | zero =>
    rw [ChainComplex.quasiIsoAt₀_iff, CategoryTheory.ShortComplex.quasiIso_iff_of_zeros']
    · refine (CategoryTheory.ShortComplex.exact_and_epi_g_iff_of_iso ?_).2
        ⟨augmentedShortComplex_exact q hq, augmentation_epi q⟩
      exact CategoryTheory.ShortComplex.isoMk (Iso.refl _) (Iso.refl _) (Iso.refl _)
        (by simp [augmentedShortComplex, differential])
        (by simp [augmentedShortComplex])
    all_goals rfl
  | succ n =>
    rw [quasiIsoAt_iff_exactAt' (augmentationMap q hq) (n + 1)
      (ChainComplex.exactAt_succ_single_obj _ _)]
    exact lowerComplex_exactAt_succ q hq n

/-- The specified actual corner resolution, with all-degree exactness and projectivity. -/
def projectiveResolution (q : K) (hq : PowerCondition q) :
    CategoryTheory.ProjectiveResolution (simpleObject q) where
  complex := lowerComplex q hq
  projective n := by
    cases n with
    | zero => exact cf_category_projective q
    | succ n => exact ce_category_projective q
  π := augmentationMap q hq
  quasiIso := augmentationMap_quasiIso q hq

/-- Every actual positive self-extension is zero, through the specified resolution. -/
theorem positive_selfExt_eq_zero (q : K) (hq : PowerCondition q) (n : Nat)
    (alpha : CategoryTheory.Abelian.Ext (simpleObject q) (simpleObject q) (n + 1)) :
    alpha = 0 := by
  obtain ⟨h, hh, halpha⟩ := (projectiveResolution q hq).extMk_surjective alpha (n + 2) rfl
  have hz : h = 0 := by
    apply ModuleCat.hom_ext
    exact hom_ce_simple_zero q h.hom
  rw [← halpha]
  subst h
  exact (projectiveResolution q hq).extMk_zero (n + 2) rfl

theorem positive_selfExt_subsingleton (q : K) (hq : PowerCondition q) (n : Nat) :
    Subsingleton (CategoryTheory.Abelian.Ext (simpleObject q) (simpleObject q) (n + 1)) :=
  ⟨fun a b => by rw [positive_selfExt_eq_zero q hq n a, positive_selfExt_eq_zero q hq n b]⟩

#print axioms PowerCondition
#print axioms augmentation_ker_eq_range
#print axioms augmentation_comp_rightU
#print axioms term
#print axioms differential
#print axioms differential_comp
#print axioms lowerComplex
#print axioms lowerComplex_exactAt_succ
#print axioms augmentationMap
#print axioms augmentationMap_f_zero
#print axioms augmentedShortComplex_exact
#print axioms augmentation_epi
#print axioms augmentationMap_quasiIso
#print axioms projectiveResolution
#print axioms positive_selfExt_eq_zero
#print axioms positive_selfExt_subsingleton

end
end ARCLowerAlgebraCategoricalResolution
