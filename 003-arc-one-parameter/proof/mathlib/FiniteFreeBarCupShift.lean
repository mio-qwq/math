import FiniteFreeBarCupLift
import FiniteFreeBarExtThree
import ExtMkYonedaLift

/-!
# The actual shifted suffix lift and its Yoneda square

The full suffix maps assemble into a degree-three cocycle on the specified
zero-extended projective resolution. Characteristic two removes the odd
shift sign. The resulting genuine shifted morphism has the specified
augmentation and cup components as equalities of whole complexes.

This identifies the actual Yoneda square with extMk of the full cup Hom.
No nonvanishing of that square or complete self-Ext profile is asserted.
-/

namespace ARCFiniteFreeBarCupShift

open CategoryTheory CategoryTheory.Category CategoryTheory.Limits
open CategoryTheory.Abelian CochainComplex CochainComplex.HomComplex
open ARCTwentyDimAlgebra ARCTwentyDimCharacters ARCCharacterModule
open ARCFiniteFreeBarModules ARCFiniteFreeBarAugmentation ARCFiniteFreeBarRecursive
open ARCFiniteFreeBarProjectiveResolution ARCFiniteFreeBarExtThree
open ARCFiniteFreeBarCupLift ARCExtMkCanonicalFunctor ARCExtMkYonedaLift

universe u
variable {R : Type u} [CommRing R] [CharP R 2]

noncomputable section

set_option backward.defeqAttrib.useBackward true

variable (q : R)

private abbrev P := projectiveResolution q (fCharacter q)
private abbrev K := (P q).cochainComplex

/-- The actual term comparison with its exhibited finite free codomain. -/
private def termIso (i : ℤ) (n : Nat) (hi : -(n : ℤ) = i) :
    (K q).X i ≅ ModuleCat.of (TableAlgebra q) (BarTerm q n) :=
  (P q).cochainComplexXIso i n hi

private theorem term_d (n : Nat) :
    (K q).d (-(n + 1 : Nat)) (-n) =
      (termIso q (-(n + 1 : Nat)) (n + 1) rfl).hom ≫
        ModuleCat.ofHom (recursiveBoundary q (fCharacter q) n) ≫
        (termIso q (-n) n rfl).inv := by
  rw [(P q).cochainComplex_d _ _ (n + 1) n rfl rfl,
    projectiveResolution_d q (fCharacter q) n]
  rfl

private theorem suffixComponent_congr (i j : ℤ) (n m : Nat)
    (hni : -(n + 3 : Nat) = i) (hnj : -(n : ℤ) = j)
    (hmi : -(m + 3 : Nat) = i) (hmj : -(m : ℤ) = j) (hnm : n = m) :
    (termIso q i (n + 3) hni).hom ≫ ModuleCat.ofHom (suffixLift q n) ≫
      (termIso q j n hnj).inv =
    (termIso q i (m + 3) hmi).hom ≫ ModuleCat.ofHom (suffixLift q m) ≫
      (termIso q j m hmj).inv := by
  subst m
  rfl

set_option backward.isDefEq.respectTransparency false in
set_option backward.isDefEq.respectTransparency.types false in
/-- The genuine degree-three cochain. For j<=0 the component is the actual
suffix map with both term comparisons; for j>0 it is the zero map. -/
def suffixCochain : Cochain (K q) (K q) (3 : ℤ) :=
  Cochain.mk (fun i j hij => if hj : j ≤ 0 then
    let n := (-j).toNat
    (termIso q i (n + 3) (by
      have hn : (n : ℤ) = -j := Int.toNat_of_nonneg (by omega)
      omega)).hom ≫ ModuleCat.ofHom (suffixLift q n) ≫
        (termIso q j n (by
          have hn : (n : ℤ) = -j := Int.toNat_of_nonneg (by omega)
          omega)).inv
    else 0)

set_option backward.isDefEq.respectTransparency false in
set_option backward.isDefEq.respectTransparency.types false in
/-- Every supported component retains the actual full A-linear suffix map. -/
theorem suffixCochain_v (n : Nat) :
    (suffixCochain q).v (-(n + 3 : Nat)) (-n) (by omega) =
      (termIso q (-(n + 3 : Nat)) (n + 3) rfl).hom ≫
        ModuleCat.ofHom (suffixLift q n) ≫
        (termIso q (-n) n rfl).inv := by
  dsimp only [suffixCochain, Cochain.mk_v]
  rw [dite_eq_left (by omega : -(n : ℤ) ≤ 0)]
  have hn : (- -(n : ℤ)).toNat = n := by simp only [neg_neg, Int.toNat_natCast]
  exact suffixComponent_congr q _ _ _ _ _ _ _ _ hn

/-- All components beyond the target support vanish. -/
theorem suffixCochain_v_eq_zero (i j : ℤ) (hij : i + 3 = j) (hj : 0 < j) :
    (suffixCochain q).v i j hij = 0 := by
  simp only [suffixCochain, Cochain.mk_v, dite_eq_right (by omega : ¬ j ≤ 0)]

private theorem bar_morphism_add_self {M : ModuleCat.{u} (TableAlgebra q)}
    (n : Nat) (f : M ⟶ barModule q n) : f + f = 0 := by
  apply ModuleCat.hom_ext
  apply LinearMap.ext
  intro v
  funext w
  apply ARCTwentyDimAlgebra.ext q
  funext a
  exact CharTwo.add_self_eq_zero ((f v w).coords a)

set_option backward.isDefEq.respectTransparency false in
set_option backward.isDefEq.respectTransparency.types false in
/-- Closure uses the actual all-degree chain law, including every zero
component outside the source and shifted target supports. -/
theorem suffixCochain_closed : δ 3 4 (suffixCochain q) = 0 := by
  apply Cochain.ext
  intro i j hij
  by_cases hj : j ≤ 0
  · obtain ⟨n, rfl⟩ := Int.exists_eq_neg_ofNat hj
    have hi : i = -(n + 4 : Nat) := by omega
    subst hi
    rw [δ_v 3 4 rfl _ _ _ (by omega) (-(n + 1 : Nat)) (-(n + 3 : Nat))
      (by omega) (by omega), suffixCochain_v q (n + 1), suffixCochain_v q n]
    rw [term_d q n, term_d q (n + 3)]
    have hchain : ModuleCat.ofHom (suffixLift q (n + 1)) ≫
        ModuleCat.ofHom (recursiveBoundary q (fCharacter q) n) =
      ModuleCat.ofHom (recursiveBoundary q (fCharacter q) (n + 3)) ≫
        ModuleCat.ofHom (suffixLift q n) :=
      ModuleCat.hom_ext (suffixLift_chain q n)
    simp only [Int.negOnePow_even 4 (by decide : Even (4 : ℤ)),
      one_smul, assoc, Iso.inv_hom_id_assoc, Cochain.zero_v]
    rw [reassoc_of% hchain]
    rw [← cancel_mono (termIso q (-n) n rfl).hom]
    simp only [Preadditive.add_comp, zero_comp, assoc, Iso.inv_hom_id,
      comp_id]
    exact bar_morphism_add_self q n _
  · exact ((K q).isZero_of_isStrictlyLE 0 j (by omega)).eq_of_tgt _ _

/-- The actual full degree-three cocycle on the installed resolution. -/
def suffixCocycle : Cocycle (K q) (K q) (3 : ℤ) :=
  Cocycle.mk (suffixCochain q) 4 rfl (suffixCochain_closed q)

/-- A genuine whole shifted morphism, constructed from all suffix maps. -/
def suffixShift : ShiftedHom (K q) (K q) (3 : ℤ) :=
  Cocycle.equivHomShift.symm (suffixCocycle q)

set_option backward.isDefEq.respectTransparency false in
set_option backward.isDefEq.respectTransparency.types false in
/-- The whole augmentation equality identifies the original fixed cocycle. -/
theorem suffixCocycle_postcomp_augmentation :
    (suffixCocycle q).postcomp (P q).π' =
      resolutionCocycle (P q) (fCocycle q) 4 rfl (fCocycle_closed q) := by
  apply Cocycle.ext
  apply (Cochain.toSingleEquiv (show (-3 : ℤ) + 3 = 0 by rfl)).injective
  change (suffixCochain q).v (-3) 0 (by rfl) ≫ (P q).π'.f 0 ≫
      (HomologicalComplex.singleObjXSelf (.up ℤ) 0
        (characterObject q (fCharacter q))).hom =
    ((P q).cochainComplexXIso (-3) 3 rfl).hom ≫ fCocycle q
  have hv : (suffixCochain q).v (-3) 0 (by rfl) =
      (termIso q (-3) 3 rfl).hom ≫
        ModuleCat.ofHom (suffixLift q 0) ≫
        (termIso q 0 0 rfl).inv := by
    have h := suffixCochain_v q 0
    exact h
  rw [hv, (P q).π'_f_zero,
    projectiveResolution_π_f_zero q (fCharacter q)]
  have haug : ModuleCat.ofHom (suffixLift q 0) ≫
      ModuleCat.ofHom (augmentation q (fCharacter q)) = fCocycle q :=
    ModuleCat.hom_ext (augmentation_suffixLift_zero q)
  change (termIso q (-3) 3 rfl).hom ≫ ModuleCat.ofHom (suffixLift q 0) ≫
      (termIso q 0 0 rfl).inv ≫ (termIso q 0 0 rfl).hom ≫
        ModuleCat.ofHom (augmentation q (fCharacter q)) ≫
          (HomologicalComplex.singleObjXSelf (.up ℤ) 0
            (characterObject q (fCharacter q))).inv ≫
          (HomologicalComplex.singleObjXSelf (.up ℤ) 0
            (characterObject q (fCharacter q))).hom =
    (termIso q (-3) 3 rfl).hom ≫ fCocycle q
  simp only [Iso.inv_hom_id_assoc, Iso.inv_hom_id, comp_id, haug]

/-- Equality of actual whole shifted morphisms, not just their degree-three values. -/
theorem suffixShift_comp_augmentation :
    (suffixShift q).comp (ShiftedHom.mk₀ (0 : ℤ) rfl (P q).π')
      (zero_add (3 : ℤ)) =
      Cocycle.equivHomShift.symm
        (resolutionCocycle (P q) (fCocycle q) 4 rfl (fCocycle_closed q)) := by
  rw [ShiftedHom.comp_mk₀]
  exact (Cocycle.equivHomShift_symm_postcomp (suffixCocycle q) (P q).π').symm.trans
    (congrArg Cocycle.equivHomShift.symm (suffixCocycle_postcomp_augmentation q))

/-- The actual categorical cup component on P6. -/
def cupSixCocycle : (P q).complex.X 6 ⟶ characterObject q (fCharacter q) :=
  ModuleCat.ofHom (cupSixHom q)

/-- Its whole P7 cocycle law uses the installed recursive differential. -/
theorem cupSixCocycle_closed :
    (P q).complex.d 7 6 ≫ cupSixCocycle q = 0 := by
  rw [projectiveResolution_d q (fCharacter q) 6]
  exact ModuleCat.hom_ext (cupSixHom_closed q)

set_option backward.isDefEq.respectTransparency false in
set_option backward.isDefEq.respectTransparency.types false in
/-- The actual suffix shift followed by the original shifted cocycle is
the whole shifted cocycle of cupSixHom. -/
theorem suffixShift_comp_f :
    (suffixShift q).comp
      (Cocycle.equivHomShift.symm
        (resolutionCocycle (P q) (fCocycle q) 4 rfl (fCocycle_closed q)))
      (show (3 : ℤ) + 3 = 6 by rfl) =
      Cocycle.equivHomShift.symm
        (resolutionCocycle (P q) (cupSixCocycle q) 7 rfl
          (cupSixCocycle_closed q)) := by
  apply HomologicalComplex.hom_ext
  intro i
  by_cases hi : i = -6
  · subst i
    simp only [ShiftedHom.comp, HomologicalComplex.comp_f,
      shiftFunctor_map_f', shiftFunctorAdd'_inv_app_f',
      HomologicalComplex.XIsoOfEq_rfl, Iso.refl_hom,
      suffixShift, equivHomShift_symm_f]
    change (suffixCochain q).v (-6) (-3) rfl ≫
        ((resolutionCocycle (P q) (fCocycle q) 4 rfl
          (fCocycle_closed q)).1.v (-3) 0 rfl) =
      (resolutionCocycle (P q) (cupSixCocycle q) 7 rfl
        (cupSixCocycle_closed q)).1.v (-6) 0 rfl
    have hv := suffixCochain_v q 3
    change (suffixCochain q).v (-6) (-3) rfl =
      (termIso q (-6) 6 rfl).hom ≫ ModuleCat.ofHom (suffixLift q 3) ≫
        (termIso q (-3) 3 rfl).inv at hv
    rw [hv]
    simp only [resolutionCocycle, Cocycle.toSingleMk_coe,
      assoc]
    change (termIso q (-6) 6 rfl).hom ≫ ModuleCat.ofHom (suffixLift q 3) ≫
        (termIso q (-3) 3 rfl).inv ≫ (termIso q (-3) 3 rfl).hom ≫
          fCocycle q ≫ (HomologicalComplex.singleObjXSelf (.up ℤ) 0
            (characterObject q (fCharacter q))).inv =
      (termIso q (-6) 6 rfl).hom ≫ cupSixCocycle q ≫
        (HomologicalComplex.singleObjXSelf (.up ℤ) 0
          (characterObject q (fCharacter q))).inv
    simp only [Iso.inv_hom_id_assoc]
    rfl
  · apply (HomologicalComplex.isZero_single_obj_X (.up ℤ) 0
      (characterObject q (fCharacter q)) (i + 6) (by omega)).eq_of_tgt

/-- The fixed actual Ext3 class squared is the extMk class of the
constructed full degree-six cup Hom on the given resolution. -/
theorem fExtThree_comp_self :
    (fExtThree q).comp (fExtThree q) (show 3 + 3 = 6 by rfl) =
      (P q).extMk (cupSixCocycle q) 7 rfl (cupSixCocycle_closed q) := by
  exact extMk_comp_of_shifted_lift (P q) (P q)
    (fCocycle q) (fCocycle_closed q) (fCocycle q) (fCocycle_closed q)
    (cupSixCocycle q) (cupSixCocycle_closed q) rfl (suffixShift q)
    (suffixShift_comp_augmentation q) (suffixShift_comp_f q)

#print axioms suffixCochain
#print axioms suffixCochain_v
#print axioms suffixCochain_v_eq_zero
#print axioms suffixCochain_closed
#print axioms suffixCocycle
#print axioms suffixShift
#print axioms suffixCocycle_postcomp_augmentation
#print axioms suffixShift_comp_augmentation
#print axioms cupSixCocycle
#print axioms cupSixCocycle_closed
#print axioms suffixShift_comp_f
#print axioms fExtThree_comp_self

end
end ARCFiniteFreeBarCupShift
