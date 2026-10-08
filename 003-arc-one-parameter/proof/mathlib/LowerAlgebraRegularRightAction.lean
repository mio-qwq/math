import LowerAlgebraRegularExt

/-!
# Actual right multiplication on the regular-target degree-two Ext line

Right multiplication is retained as a C-linear regular-module morphism.
The complete v*c formula and an actual boundary for z determine the
postcomposition action on the specified Ext generator and, when it spans,
on every degree-two class. A bundled right-module equivalence is separate.
-/

namespace ARCLowerAlgebraRegularRightAction

open ARCFiniteCore ARCBitPolynomial ARCTermSemantics ARCFiniteTableContraction
open ARCTwentyDimAssociativity ARCTwentyDimAlgebra ARCTwentyDimCochainAlgebra
open ARCTwentyDimFrobenius ARCTwentyDimDualScaleEndomorphism
open ARCTwentyDimTrivialExtension ARCCochainIdempotentClosure
open ARCLowerAlgebraResolution ARCLowerAlgebraProjective
open ARCLowerAlgebraRegularHom ARCLowerAlgebraCategoricalResolution
open ARCLowerAlgebraRegularExt ARCExtMkExactFunctor
open CategoryTheory CategoryTheory.Category CategoryTheory.Limits
open scoped BigOperators
open scoped ModuleCat.Algebra

universe u
noncomputable section
set_option backward.isDefEq.respectTransparency false
variable {K : Type u} [Field K] [CharP K 2]

/-- Actual regular-module endomorphism, C-linear even for a noncentral c. -/
def rightMultiplication (q : K) (c : C q) : C q →ₗ[C q] C q where
  toFun a := a * c
  map_add' a b := add_mul a b c
  map_smul' a b := mul_assoc a b c

theorem rightMultiplication_one (q : K) : rightMultiplication q 1 = LinearMap.id := by
  apply LinearMap.ext
  intro a
  exact mul_one a

theorem rightMultiplication_comp (q : K) (c d : C q) :
    (rightMultiplication q d).comp (rightMultiplication q c) =
      rightMultiplication q (c * d) := by
  apply LinearMap.ext
  intro a
  exact mul_assoc a c d

def rightRegularMap (q : K) (c : C q) : regularObject q ⟶ regularObject q :=
  ModuleCat.ofHom (rightMultiplication q c)

/-- The actual right-e corner remains closed under right multiplication. -/
def rightCornerMultiplication (q : K) (c : C q) : eC q →ₗ[K] eC q where
  toFun a := ⟨(a : C q) * c, by
    change e q * ((a : C q) * c) = _
    rw [← mul_assoc, a.property]⟩
  map_add' a b := by apply Subtype.ext; exact add_mul (a : C q) b c
  map_smul' r a := by apply Subtype.ext; exact smul_mul_assoc r (a : C q) c

theorem evalHomCe_postcompose (q : K) (c : C q) (h : Ce q →ₗ[C q] C q) :
    evalHomCe q ((rightMultiplication q c).comp h) =
      rightCornerMultiplication q c (evalHomCe q h) := by
  apply Subtype.ext
  rfl

/-- Category scalars are the actual central K scalars on the regular algebra. -/
theorem evalHomCe_category_smul (q : K) (r : K)
    (h : ModuleCat.of (C q) (Ce q) ⟶ regularObject q) :
    evalHomCe q (r • h).hom = r • evalHomCe q h.hom := by
  apply Subtype.ext
  change algebraMap K (C q) r * (show C q from h.hom (eGenerator q)) =
    r • (show C q from h.hom (eGenerator q))
  rw [← Algebra.smul_def]

def regularX (q : K) : eC q := ecVector q 1
def regularZ (q : K) : eC q := ecVector q 3

private theorem left_basis_mul_coords (q : K) (a : C q) (b k : Fin 20) :
    (coordinateBasis q b * (a : TableAlgebra q)).coords k =
      ∑ i : Fin 10, (a : TableAlgebra q).coords (Fin.castAdd 10 i) *
        specializedConstants q b (Fin.castAdd 10 i) k := by
  have hfull : (coordinateBasis q b * (a : TableAlgebra q)).coords k =
      ∑ i : Fin 20, (a : TableAlgebra q).coords i * specializedConstants q b i k := by
    change (∑ i : Fin 20, ∑ j : Fin 20,
      (coordinateBasis q b).coords i * (a : TableAlgebra q).coords j *
        specializedConstants q i j k) = _
    simp [coords_coordinateBasis]
  rw [hfull]
  apply Fin.sum_trunc (a := 10) (b := 10)
  intro j
  have hu := (mem_lowerSubalgebra q (a : TableAlgebra q)).mp a.property
  rw [hu _ (by change ¬ 10 + j.val < 10; omega), zero_mul]

private theorem v_table (i : Fin 10) :
    tTerms 5 i.val = if i = 6 then [(3, 2)] else if i = 8 then [(5, 1)] else [] := by
  fin_cases i <;> rfl

private theorem specialize_single (q : K) (j c k : Nat) :
    specialize q (singleTerm j c k) =
      if k = j then specialize q (decode c) else 0 := by
  by_cases h : k = j <;> simp [singleTerm, h]

private theorem specialize_one (q : K) : specialize q (decode 1) = 1 :=
  ARCScalarEvaluation.evaluate_one q

private theorem specialize_two (q : K) : specialize q (decode 2) = q :=
  ARCScalarEvaluation.evaluate_two q

private theorem v_constants (q : K) (i : Fin 10) (k : Fin 20) :
    specializedConstants q 5 (Fin.castAdd 10 i) k =
      if i = 6 ∧ k = 3 then q else if i = 8 ∧ k = 5 then 1 else 0 := by
  change specialize q (sumTerms (tTerms 5 i.val) k.val) = _
  rw [v_table]
  fin_cases i <;> simp [specialize_single, specialize_one, specialize_two, Fin.ext_iff]

/-- The complete installed multiplication of v by any lower-algebra element. -/
theorem regularV_mul (q : K) (c : C q) :
    rightCornerMultiplication q c (regularV q) =
      (lowerCharacter q c) • regularV q +
        (q * (c : TableAlgebra q).coords 6) • regularZ q := by
  apply Subtype.ext
  apply Subtype.ext
  apply ARCTwentyDimAlgebra.ext q
  funext k
  change (coordinateBasis q 5 * (c : TableAlgebra q)).coords k =
    ((c : TableAlgebra q).coords 8 • coordinateBasis q 5 +
      (q * (c : TableAlgebra q).coords 6) • coordinateBasis q 3).coords k
  rw [left_basis_mul_coords]
  simp_rw [v_constants]
  rw [coords_add, coords_smul, coords_smul]
  by_cases h3 : k = 3 <;> by_cases h5 : k = 5 <;>
    simp [h3, h5, coords_coordinateBasis, mul_comm, eq_comm]

/-- z is a specified actual preceding boundary, using the actual x vector. -/
theorem leftEll_zero_regularX (q : K) : leftEll q 0 (regularX q) = regularZ q := by
  apply (ecCoordsEquiv q).injective
  rw [leftEll_coords]
  funext i
  fin_cases i <;>
    simp [regularX, regularZ, ecCoordsEquiv, ecVector, ecLabel, cBasis,
      coords_coordinateBasis, CharTwo.add_self_eq_zero]

def regularZCocycle (q : K) (hq : PowerCondition q) :
    (projectiveResolution q hq).complex.X 2 ⟶ regularObject q :=
  ModuleCat.ofHom ((evalHomCe q).symm (regularZ q))

theorem regularZCocycle_boundary (q : K) (hq : PowerCondition q) :
    (projectiveResolution q hq).complex.d 2 1 ≫
      ModuleCat.ofHom ((evalHomCe q).symm (regularX q)) = regularZCocycle q hq := by
  apply ModuleCat.hom_ext
  apply (evalHomCe q).injective
  change evalHomCe q (((evalHomCe q).symm (regularX q)).comp (rightEll q 0)) =
    evalHomCe q ((evalHomCe q).symm (regularZ q))
  rw [eval_precompose_ell]
  simp only [LinearEquiv.apply_symm_apply]
  exact leftEll_zero_regularX q

theorem regularZCocycle_closed (q : K) (hq : PowerCondition q) :
    (projectiveResolution q hq).complex.d 3 2 ≫ regularZCocycle q hq = 0 := by
  rw [← regularZCocycle_boundary q hq, ← Category.assoc, HomologicalComplex.d_comp_d, zero_comp]

theorem regularZ_extMk_zero (q : K) (hq : PowerCondition q) :
    (projectiveResolution q hq).extMk (regularZCocycle q hq) 3 rfl
      (regularZCocycle_closed q hq) = 0 :=
  ((projectiveResolution q hq).extMk_eq_zero_iff (regularZCocycle q hq) 3 rfl
    (regularZCocycle_closed q hq) 1 rfl).mpr
      ⟨ModuleCat.ofHom ((evalHomCe q).symm (regularX q)), regularZCocycle_boundary q hq⟩

theorem regularCocycle_postcompose (q : K) (hq : PowerCondition q) (c : C q) :
    regularCocycle q hq ≫ rightRegularMap q c =
      (lowerCharacter q c) • regularCocycle q hq +
        (q * (c : TableAlgebra q).coords 6) • regularZCocycle q hq := by
  apply ModuleCat.hom_ext
  apply (evalHomCe q).injective
  change evalHomCe q ((rightMultiplication q c).comp
    ((evalHomCe q).symm (regularV q))) = _
  rw [evalHomCe_postcompose, ModuleCat.hom_add, map_add,
    evalHomCe_category_smul, evalHomCe_category_smul]
  simp only [regularCocycle, regularZCocycle, ModuleCat.hom_ofHom,
    LinearEquiv.apply_symm_apply]
  exact regularV_mul q c

/-- Genuine Ext postcomposition with the actual regular-module endomorphism. -/
def regularExtRightAction (q : K) (c : C q)
    (alpha : CategoryTheory.Abelian.Ext (simpleObject q) (regularObject q) 2) :
    CategoryTheory.Abelian.Ext (simpleObject q) (regularObject q) 2 :=
  alpha.comp (CategoryTheory.Abelian.Ext.mk₀ (rightRegularMap q c)) (add_zero 2)

theorem regularExtTwo_right_action (q : K) (hq : PowerCondition q) (c : C q) :
    regularExtRightAction q c (regularExtTwo q hq) =
      (lowerCharacter q c) • regularExtTwo q hq := by
  change ((projectiveResolution q hq).extMk (regularCocycle q hq) 3 rfl
    (regularCocycle_closed q hq)).comp
      (CategoryTheory.Abelian.Ext.mk₀ (rightRegularMap q c)) (add_zero 2) = _
  rw [CategoryTheory.ProjectiveResolution.extMk_comp_mk₀]
  calc
    _ = (projectiveResolution q hq).extMk
        ((lowerCharacter q c) • regularCocycle q hq +
          (q * (c : TableAlgebra q).coords 6) • regularZCocycle q hq)
        3 rfl (by simp [regularCocycle_closed, regularZCocycle_closed]) := by
      congr 1
      exact regularCocycle_postcompose q hq c
    _ = (projectiveResolution q hq).extMk
        ((lowerCharacter q c) • regularCocycle q hq) 3 rfl
          (by simp [regularCocycle_closed]) +
        (projectiveResolution q hq).extMk
          ((q * (c : TableAlgebra q).coords 6) • regularZCocycle q hq) 3 rfl
            (by simp [regularZCocycle_closed]) :=
      ((projectiveResolution q hq).add_extMk _ _ 3 rfl _ _).symm
    _ = (lowerCharacter q c) • regularExtTwo q hq := by
      rw [extMk_smul _ _ _ _ (regularCocycle_closed q hq),
        extMk_smul _ _ _ _ (regularZCocycle_closed q hq),
        regularZ_extMk_zero, smul_zero, add_zero]
      rfl

/-- Once the actual generator spans, every actual class has the same right character. -/
theorem regularExt_right_action (q : K) (hq : PowerCondition q) (hqn : q ≠ 0)
    (c : C q) (alpha : CategoryTheory.Abelian.Ext (simpleObject q) (regularObject q) 2) :
    regularExtRightAction q c alpha = (lowerCharacter q c) • alpha := by
  obtain ⟨lambda, rfl⟩ := regularExtTwo_spans q hq hqn alpha
  change (lambda • regularExtTwo q hq).comp
    (CategoryTheory.Abelian.Ext.mk₀ (rightRegularMap q c)) (add_zero 2) = _
  rw [CategoryTheory.Abelian.Ext.smul_comp]
  change lambda • regularExtRightAction q c (regularExtTwo q hq) = _
  rw [regularExtTwo_right_action, smul_smul, smul_smul, mul_comm]

#print axioms rightMultiplication
#print axioms rightMultiplication_one
#print axioms rightMultiplication_comp
#print axioms rightRegularMap
#print axioms rightCornerMultiplication
#print axioms evalHomCe_postcompose
#print axioms evalHomCe_category_smul
#print axioms regularX
#print axioms regularZ
#print axioms regularV_mul
#print axioms leftEll_zero_regularX
#print axioms regularZCocycle
#print axioms regularZCocycle_boundary
#print axioms regularZCocycle_closed
#print axioms regularZ_extMk_zero
#print axioms regularCocycle_postcompose
#print axioms regularExtRightAction
#print axioms regularExtTwo_right_action
#print axioms regularExt_right_action

end
end ARCLowerAlgebraRegularRightAction
