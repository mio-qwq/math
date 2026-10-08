import LowerAlgebraRegularHom
import LowerAlgebraCategoricalResolution
import ExtMkExactFunctor
import Mathlib.LinearAlgebra.Dimension.Finite

/-!
# Actual regular-target Ext over the lower algebra

The Hom evaluation equivalences are applied to the specified actual
projective resolution. A genuine nonzero Ext class in degree two is
constructed. Degree zero and one vanish; with q nonzero, every degree
above two vanishes and the degree-two class has a scalar parametrization.
The right-C module identification and the trivial-extension derived
triangle require further proofs.
-/

namespace ARCLowerAlgebraRegularExt

open ARCLowerAlgebraResolution ARCLowerAlgebraProjective
open ARCLowerAlgebraRegularHom ARCLowerAlgebraCategoricalResolution
open ARCExtMkExactFunctor
open CategoryTheory CategoryTheory.Category CategoryTheory.Limits
open scoped ModuleCat.Algebra

universe u
noncomputable section
set_option backward.isDefEq.respectTransparency false
variable {K : Type u} [Field K] [CharP K 2]

def regularObject (q : K) : ModuleCat.{u} (C q) := ModuleCat.of (C q) (C q)

def regularCocycle (q : K) (hq : PowerCondition q) :
    (projectiveResolution q hq).complex.X 2 ⟶ regularObject q :=
  ModuleCat.ofHom ((evalHomCe q).symm (regularV q))

theorem leftEll_regularV_zero (q : K) (n : Nat) : leftEll q n (regularV q) = 0 := by
  apply (ecCoordsEquiv q).injective
  rw [leftEll_coords, regularV_coords, map_zero]
  funext i
  fin_cases i <;> simp

theorem regularCocycle_closed (q : K) (hq : PowerCondition q) :
    (projectiveResolution q hq).complex.d 3 2 ≫ regularCocycle q hq = 0 := by
  apply ModuleCat.hom_ext
  apply (evalHomCe q).injective
  change evalHomCe q (((evalHomCe q).symm (regularV q)).comp (rightEll q 1)) =
    evalHomCe q 0
  rw [eval_precompose_ell, LinearEquiv.apply_symm_apply, map_zero]
  exact leftEll_regularV_zero q 1

/-- An actual regular-target degree-two Ext class on the specified resolution. -/
def regularExtTwo (q : K) (hq : PowerCondition q) :
    CategoryTheory.Abelian.Ext (simpleObject q) (regularObject q) 2 :=
  (projectiveResolution q hq).extMk (regularCocycle q hq) 3 rfl
    (regularCocycle_closed q hq)

theorem regularExtTwo_ne_zero (q : K) (hq : PowerCondition q) :
    regularExtTwo q hq ≠ 0 := by
  intro hz
  obtain ⟨g, hg⟩ := ((projectiveResolution q hq).extMk_eq_zero_iff
    (regularCocycle q hq) 3 rfl (regularCocycle_closed q hq) 1 rfl).mp hz
  have h := congrArg (fun a => evalHomCe q a.hom) hg
  change evalHomCe q (g.hom.comp (rightEll q 0)) =
    evalHomCe q ((evalHomCe q).symm (regularV q)) at h
  rw [eval_precompose_ell, LinearEquiv.apply_symm_apply] at h
  exact regularV_not_boundary q ⟨evalHomCe q g.hom, h⟩

theorem regularExt_zero_eq_zero (q : K) (hq : PowerCondition q)
    (alpha : CategoryTheory.Abelian.Ext (simpleObject q) (regularObject q) 0) :
    alpha = 0 := by
  obtain ⟨h, hh, halpha⟩ := (projectiveResolution q hq).extMk_surjective alpha 1 rfl
  have hc := congrArg (fun a => evalHomCe q a.hom) hh
  change evalHomCe q (h.hom.comp (rightU q)) = evalHomCe q 0 at hc
  rw [eval_precompose_U, map_zero] at hc
  have he : evalHomCf q h.hom = 0 := (leftU_injective q) (by simpa using hc)
  have hz : h = 0 := ModuleCat.hom_ext ((evalHomCf q).injective (by simpa using he))
  rw [← halpha]
  subst h
  exact (projectiveResolution q hq).extMk_zero 1 rfl

theorem regularExt_one_eq_zero (q : K) (hq : PowerCondition q)
    (alpha : CategoryTheory.Abelian.Ext (simpleObject q) (regularObject q) 1) :
    alpha = 0 := by
  obtain ⟨h, hh, halpha⟩ := (projectiveResolution q hq).extMk_surjective alpha 2 rfl
  have hc := congrArg (fun a => evalHomCe q a.hom) hh
  change evalHomCe q (h.hom.comp (rightEll q 0)) = evalHomCe q 0 at hc
  rw [eval_precompose_ell, map_zero] at hc
  have he : evalHomCe q h.hom ∈ LinearMap.range (leftU q) := by
    rw [← leftEll_zero_ker_eq_range_U q]
    exact hc
  obtain ⟨b, hb⟩ := he
  have hb' : (projectiveResolution q hq).complex.d 1 0 ≫
      ModuleCat.ofHom ((evalHomCf q).symm b) = h := by
    apply ModuleCat.hom_ext
    apply (evalHomCe q).injective
    change evalHomCe q (((evalHomCf q).symm b).comp (rightU q)) = evalHomCe q h.hom
    rw [eval_precompose_U, LinearEquiv.apply_symm_apply]
    exact hb
  rw [← halpha]
  exact ((projectiveResolution q hq).extMk_eq_zero_iff h 2 rfl hh 0 rfl).mpr
    ⟨ModuleCat.ofHom ((evalHomCf q).symm b), hb'⟩

/-- Every actual regular-target extension above degree two vanishes. -/
theorem regularExt_high_eq_zero (q : K) (hq : PowerCondition q) (hqn : q ≠ 0) (n : Nat)
    (alpha : CategoryTheory.Abelian.Ext (simpleObject q) (regularObject q) (n + 3)) :
    alpha = 0 := by
  obtain ⟨h, hh, halpha⟩ := (projectiveResolution q hq).extMk_surjective alpha (n + 4) rfl
  have hh' := hh
  change (lowerComplex q hq).d ((n + 3) + 1) (n + 3) ≫ h = 0 at hh'
  rw [lowerComplex_d] at hh'
  have hc := congrArg (fun a => evalHomCe q a.hom) hh'
  change evalHomCe q (h.hom.comp (rightEll q (n + 2))) = evalHomCe q 0 at hc
  rw [eval_precompose_ell, map_zero] at hc
  have he : evalHomCe q h.hom ∈ LinearMap.range (leftEll q (n + 1)) := by
    rw [← leftEll_succ_succ_ker_eq_range q hqn n (hq n) (hq (n + 1))]
    exact hc
  obtain ⟨b, hb⟩ := he
  have hb' : (projectiveResolution q hq).complex.d (n + 3) (n + 2) ≫
      ModuleCat.ofHom ((evalHomCe q).symm b) = h := by
    change (lowerComplex q hq).d ((n + 2) + 1) (n + 2) ≫
      ModuleCat.ofHom ((evalHomCe q).symm b) = h
    rw [lowerComplex_d]
    apply ModuleCat.hom_ext
    apply (evalHomCe q).injective
    change evalHomCe q (((evalHomCe q).symm b).comp (rightEll q (n + 1))) =
      evalHomCe q h.hom
    rw [eval_precompose_ell, LinearEquiv.apply_symm_apply]
    exact hb
  rw [← halpha]
  exact ((projectiveResolution q hq).extMk_eq_zero_iff h (n + 4) rfl hh (n + 2) rfl).mpr
    ⟨ModuleCat.ofHom ((evalHomCe q).symm b), hb'⟩

theorem regularExt_except_two_eq_zero (q : K) (hq : PowerCondition q) (hqn : q ≠ 0)
    (n : Nat) (hn : n ≠ 2)
    (alpha : CategoryTheory.Abelian.Ext (simpleObject q) (regularObject q) n) :
    alpha = 0 := by
  match n with
  | 0 => exact regularExt_zero_eq_zero q hq alpha
  | 1 => exact regularExt_one_eq_zero q hq alpha
  | 2 => exact (hn rfl).elim
  | n + 3 => exact regularExt_high_eq_zero q hq hqn n alpha

/-- Every actual degree-two extension is a scalar multiple of the specified class. -/
theorem regularExtTwo_spans (q : K) (hq : PowerCondition q) (hqn : q ≠ 0)
    (alpha : CategoryTheory.Abelian.Ext (simpleObject q) (regularObject q) 2) :
    ∃ lambda : K, alpha = lambda • regularExtTwo q hq := by
  obtain ⟨h, hh, halpha⟩ := (projectiveResolution q hq).extMk_surjective alpha 3 rfl
  have hc := congrArg (fun a => evalHomCe q a.hom) hh
  change evalHomCe q (h.hom.comp (rightEll q 1)) = evalHomCe q 0 at hc
  rw [eval_precompose_ell, map_zero] at hc
  obtain ⟨b, lambda, hb⟩ := (leftEll_one_zero_iff_boundary_add_v q hqn
    (ARCLowerAlgebraCategoricalResolution.power_one q hq) _).mp hc
  let g : (projectiveResolution q hq).complex.X 1 ⟶ regularObject q :=
    ModuleCat.ofHom ((evalHomCe q).symm b)
  let boundary := (projectiveResolution q hq).complex.d 2 1 ≫ g
  have hbmap : boundary + lambda • regularCocycle q hq = h := by
    apply ModuleCat.hom_ext
    apply (evalHomCe q).injective
    rw [ModuleCat.hom_add, map_add]
    have hbval : evalHomCe q boundary.hom = leftEll q 0 b := by
      change evalHomCe q (((evalHomCe q).symm b).comp (rightEll q 0)) = _
      rw [eval_precompose_ell, LinearEquiv.apply_symm_apply]
    have hsval : evalHomCe q (lambda • regularCocycle q hq).hom =
        lambda • regularV q := by
      apply Subtype.ext
      change algebraMap K (C q) lambda *
        (((evalHomCe q).symm (regularV q)) (eGenerator q)) = lambda • (regularV q : C q)
      have hv := congrArg (fun a : eC q => (a : C q))
        ((evalHomCe q).apply_symm_apply (regularV q))
      change (((evalHomCe q).symm (regularV q)) (eGenerator q)) = (regularV q : C q) at hv
      rw [hv, ← Algebra.smul_def]
    rw [hbval, hsval]
    exact hb.symm
  have hbclosed : (projectiveResolution q hq).complex.d 3 2 ≫ boundary = 0 := by
    dsimp [boundary]
    rw [← Category.assoc, HomologicalComplex.d_comp_d, zero_comp]
  have hbzero : (projectiveResolution q hq).extMk boundary 3 rfl hbclosed = 0 :=
    ((projectiveResolution q hq).extMk_eq_zero_iff boundary 3 rfl hbclosed 1 rfl).mpr
      ⟨g, rfl⟩
  refine ⟨lambda, ?_⟩
  calc
    alpha = (projectiveResolution q hq).extMk h 3 rfl hh := halpha.symm
    _ = (projectiveResolution q hq).extMk (boundary + lambda • regularCocycle q hq)
        3 rfl (by simp [hbclosed, regularCocycle_closed]) := by congr 1; exact hbmap.symm
    _ = (projectiveResolution q hq).extMk boundary 3 rfl hbclosed +
        (projectiveResolution q hq).extMk (lambda • regularCocycle q hq) 3 rfl
          (by simp [regularCocycle_closed]) :=
      ((projectiveResolution q hq).add_extMk _ _ 3 rfl _ _).symm
    _ = lambda • regularExtTwo q hq := by rw [hbzero, zero_add, extMk_smul]; rfl

/-- A specified bijective linear parametrization of the actual degree-two Ext group. -/
def regularExtTwoLinearEquiv (q : K) (hq : PowerCondition q) (hqn : q ≠ 0) :
    K ≃ₗ[K] CategoryTheory.Abelian.Ext (simpleObject q) (regularObject q) 2 :=
  LinearEquiv.ofBijective (LinearMap.toSpanSingleton K _ (regularExtTwo q hq))
    ⟨smul_left_injective K (regularExtTwo_ne_zero q hq), fun alpha => by
      obtain ⟨lambda, h⟩ := regularExtTwo_spans q hq hqn alpha
      exact ⟨lambda, h.symm⟩⟩

@[simp] theorem regularExtTwoLinearEquiv_apply (q : K) (hq : PowerCondition q)
    (hqn : q ≠ 0) (lambda : K) :
    regularExtTwoLinearEquiv q hq hqn lambda = lambda • regularExtTwo q hq := rfl

theorem regularExtTwo_finrank (q : K) (hq : PowerCondition q) (hqn : q ≠ 0) :
    Module.finrank K (CategoryTheory.Abelian.Ext (simpleObject q) (regularObject q) 2) = 1 := by
  rw [← (regularExtTwoLinearEquiv q hq hqn).finrank_eq]
  exact Module.finrank_self K

#print axioms regularObject
#print axioms regularCocycle
#print axioms leftEll_regularV_zero
#print axioms regularCocycle_closed
#print axioms regularExtTwo
#print axioms regularExtTwo_ne_zero
#print axioms regularExt_zero_eq_zero
#print axioms regularExt_one_eq_zero
#print axioms regularExt_high_eq_zero
#print axioms regularExt_except_two_eq_zero
#print axioms regularExtTwo_spans
#print axioms regularExtTwoLinearEquiv
#print axioms regularExtTwoLinearEquiv_apply
#print axioms regularExtTwo_finrank

end
end ARCLowerAlgebraRegularExt
