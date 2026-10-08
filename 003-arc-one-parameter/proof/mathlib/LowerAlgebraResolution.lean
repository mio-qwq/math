import TwentyDimTrivialExtension
import CochainIdempotentClosure
import ScalarEvaluation
import Mathlib.Algebra.CharP.Two

/-!
# Actual left corners and right-multiplication maps over the lower algebra

The corners here are genuine left submodules of the actual lower-image
algebra. Their definitions retain the installed multiplication and the
specified idempotents, rather than assuming a coordinate matrix model.
The existing idempotent support theorems are reused without new full-table
enumerations. An entire projective resolution and Ext calculation require
additional exactness and homological bridges.
-/

namespace ARCLowerAlgebraResolution

open ARCFiniteCore ARCBitPolynomial ARCTermSemantics ARCFiniteTableContraction
open ARCTwentyDimAssociativity ARCTwentyDimAlgebra ARCTwentyDimCochainAlgebra
open ARCTwentyDimFrobenius ARCTwentyDimDualScaleEndomorphism
open ARCTwentyDimTrivialExtension ARCCochainIdempotentClosure
open scoped BigOperators

noncomputable section
variable {R : Type*} [CommRing R] [CharP R 2]

abbrev C (q : R) := lowerSubalgebra q

/-- The actual lower basis vector, as an element of the lower subalgebra. -/
def cBasis (q : R) (i : Fin 10) : C q :=
  ⟨coordinateBasis q ⟨i.val, by omega⟩, by
    apply (mem_lowerSubalgebra q _).mpr
    intro j hj
    rw [coords_coordinateBasis]
    have hne : (⟨i.val, by omega⟩ : Fin 20) ≠ j := by
      intro h
      have hv := congrArg Fin.val h
      change i.val = j.val at hv
      have hi := i.isLt
      omega
    simp [hne]⟩

@[simp] theorem cBasis_val (q : R) (i : Fin 10) :
    (cBasis q i : TableAlgebra q) = coordinateBasis q ⟨i.val, by omega⟩ := rfl

def e (q : R) : C q := cBasis q 0
def f (q : R) : C q := cBasis q 8
def u (q : R) : C q := cBasis q 4
def ell (q : R) (n : Nat) : C q := cBasis q 1 + q ^ n • cBasis q 2

private theorem mul_basis_right_coords (q : R) (a : TableAlgebra q)
    (b k : Fin 20) :
    (a * coordinateBasis q b).coords k =
      ∑ i : Fin 20, a.coords i * specializedConstants q i b k := by
  change (∑ i : Fin 20, ∑ j : Fin 20,
    a.coords i * (coordinateBasis q b).coords j * specializedConstants q i j k) = _
  simp [coords_coordinateBasis]

/-- Whole-vector action of either installed right idempotent. -/
theorem right_idempotent_coords (q : R) (a : TableAlgebra q)
    (s : Fin 2) (k : Fin 20) :
    (a * coordinateBasis q (idempotentIndex s)).coords k =
      if tRight k.val = (idempotentIndex s).val then a.coords k else 0 := by
  rw [mul_basis_right_coords]
  simp_rw [specializedB_idempotent_right, mul_ite, mul_one, mul_zero]
  rw [Finset.sum_eq_single k]
  · simp
  · intro j hj hne
    simp [hne]
  · simp

theorem e_mul_e (q : R) : e q * e q = e q := by
  apply Subtype.ext
  apply ARCTwentyDimAlgebra.ext q
  funext k
  change (coordinateBasis q 0 * coordinateBasis q 0).coords k = (coordinateBasis q 0).coords k
  rw [show (0 : Fin 20) = idempotentIndex 0 by rfl, right_idempotent_coords]
  simp only [coords_coordinateBasis]
  by_cases hk : k = 0
  · subst k
    simp [idempotentIndex, tRight, cRight]
  · simp [idempotentIndex, Ne.symm hk]

theorem f_mul_f (q : R) : f q * f q = f q := by
  apply Subtype.ext
  apply ARCTwentyDimAlgebra.ext q
  funext k
  change (coordinateBasis q 8 * coordinateBasis q 8).coords k = (coordinateBasis q 8).coords k
  rw [show (8 : Fin 20) = idempotentIndex 1 by rfl, right_idempotent_coords]
  simp only [coords_coordinateBasis]
  by_cases hk : k = 8
  · subst k
    simp [idempotentIndex, tRight, cRight]
  · simp [idempotentIndex, Ne.symm hk]

/-- The fixed right-e corner is a genuine left C-submodule. -/
def Ce (q : R) : Submodule (C q) (C q) where
  carrier := {a | a * e q = a}
  zero_mem' := by simp
  add_mem' ha hb := by simp only [Set.mem_ofPred_eq] at *; rw [add_mul, ha, hb]
  smul_mem' c a ha := by
    change a * e q = a at ha
    change (c * a) * e q = c * a
    rw [mul_assoc, ha]

/-- The fixed right-f corner is a genuine left C-submodule. -/
def Cf (q : R) : Submodule (C q) (C q) where
  carrier := {a | a * f q = a}
  zero_mem' := by simp
  add_mem' ha hb := by simp only [Set.mem_ofPred_eq] at *; rw [add_mul, ha, hb]
  smul_mem' c a ha := by
    change a * f q = a at ha
    change (c * a) * f q = c * a
    rw [mul_assoc, ha]

/-- Corner support is proved on all coordinates of every actual lower element. -/
theorem mem_Ce_coords (q : R) (a : C q) :
    a ∈ Ce q ↔ ∀ k : Fin 20, tRight k.val ≠ 0 → (a : TableAlgebra q).coords k = 0 := by
  change a * e q = a ↔ _
  constructor
  · intro h k hk
    have hc := congrArg (fun b : C q => (b : TableAlgebra q).coords k) h
    change ((a : TableAlgebra q) * coordinateBasis q 0).coords k = _ at hc
    rw [show (0 : Fin 20) = idempotentIndex 0 by rfl, right_idempotent_coords] at hc
    simpa [idempotentIndex, hk] using hc.symm
  · intro h
    apply Subtype.ext
    apply ARCTwentyDimAlgebra.ext q
    funext k
    change ((a : TableAlgebra q) * coordinateBasis q 0).coords k = _
    rw [show (0 : Fin 20) = idempotentIndex 0 by rfl, right_idempotent_coords]
    by_cases hk : tRight k.val = 0 <;> simp [idempotentIndex, hk, h]

theorem mem_Cf_coords (q : R) (a : C q) :
    a ∈ Cf q ↔ ∀ k : Fin 20, tRight k.val ≠ 8 → (a : TableAlgebra q).coords k = 0 := by
  change a * f q = a ↔ _
  constructor
  · intro h k hk
    have hc := congrArg (fun b : C q => (b : TableAlgebra q).coords k) h
    change ((a : TableAlgebra q) * coordinateBasis q 8).coords k = _ at hc
    rw [show (8 : Fin 20) = idempotentIndex 1 by rfl, right_idempotent_coords] at hc
    simpa [idempotentIndex, hk] using hc.symm
  · intro h
    apply Subtype.ext
    apply ARCTwentyDimAlgebra.ext q
    funext k
    change ((a : TableAlgebra q) * coordinateBasis q 8).coords k = _
    rw [show (8 : Fin 20) = idempotentIndex 1 by rfl, right_idempotent_coords]
    by_cases hk : tRight k.val = 8 <;> simp [idempotentIndex, hk, h]

private theorem lower_basis_right_idempotent (q : R) (i : Fin 10) (s : Fin 2)
    (hi : cRight i.val = (idempotentIndex s).val) :
    (cBasis q i : TableAlgebra q) * coordinateBasis q (idempotentIndex s) = cBasis q i := by
  apply ARCTwentyDimAlgebra.ext q
  funext k
  rw [right_idempotent_coords, cBasis_val, coords_coordinateBasis]
  by_cases hk : (⟨i.val, by omega⟩ : Fin 20) = k
  · subst k
    simp [tRight, i.isLt, hi]
  · simp [hk]

theorem u_mul_f (q : R) : u q * f q = u q := by
  apply Subtype.ext
  exact lower_basis_right_idempotent q 4 1 rfl

theorem ell_mul_e (q : R) (n : Nat) : ell q n * e q = ell q n := by
  have hx : cBasis q 1 * e q = cBasis q 1 := by
    apply Subtype.ext
    exact lower_basis_right_idempotent q 1 0 rfl
  have hy : cBasis q 2 * e q = cBasis q 2 := by
    apply Subtype.ext
    exact lower_basis_right_idempotent q 2 0 rfl
  simp only [ell, add_mul, smul_mul_assoc, hx, hy]

/-- Actual right multiplication by u on the left corners, C-linear by associativity. -/
def rightU (q : R) : Ce q →ₗ[C q] Cf q where
  toFun a := ⟨(a : C q) * u q, by change ((a : C q) * u q) * f q = _; rw [mul_assoc, u_mul_f]⟩
  map_add' a b := by apply Subtype.ext; exact add_mul (a : C q) b (u q)
  map_smul' c a := by apply Subtype.ext; exact mul_assoc c a (u q)

/-- Actual right multiplication by ell_n on every degree of the e corner. -/
def rightEll (q : R) (n : Nat) : Ce q →ₗ[C q] Ce q where
  toFun a := ⟨(a : C q) * ell q n, by change ((a : C q) * ell q n) * e q = _; rw [mul_assoc, ell_mul_e]⟩
  map_add' a b := by apply Subtype.ext; exact add_mul (a : C q) b (ell q n)
  map_smul' c a := by apply Subtype.ext; exact mul_assoc c a (ell q n)

/-- The specified e-corner basis order e,x,y,z,t,j. -/
def ceLabel : Fin 6 → Fin 10 := ![0, 1, 2, 3, 6, 7]

/-- The specified f-corner basis order f,u,v,n. -/
def cfLabel : Fin 4 → Fin 10 := ![8, 4, 5, 9]

def ceVector (q : R) (i : Fin 6) : Ce q :=
  ⟨cBasis q (ceLabel i), by
    apply Subtype.ext
    exact lower_basis_right_idempotent q (ceLabel i) 0 (by fin_cases i <;> rfl)⟩

def cfVector (q : R) (i : Fin 4) : Cf q :=
  ⟨cBasis q (cfLabel i), by
    apply Subtype.ext
    exact lower_basis_right_idempotent q (cfLabel i) 1 (by fin_cases i <;> rfl)⟩

/-- A genuine coordinate equivalence of the actual left e-corner. -/
def ceCoordsEquiv (q : R) : Ce q ≃ₗ[R] (Fin 6 → R) where
  toFun a i := (((a : C q) : TableAlgebra q)).coords ⟨(ceLabel i).val, by omega⟩
  invFun v := ∑ i : Fin 6, v i • ceVector q i
  map_add' a b := by funext i; rfl
  map_smul' r a := by funext i; rfl
  left_inv a := by
    apply Subtype.ext
    apply Subtype.ext
    apply ARCTwentyDimAlgebra.ext q
    funext k
    have hl := (mem_lowerSubalgebra q ((a : C q) : TableAlgebra q)).mp (a : C q).property
    have hc := (mem_Ce_coords q (a : C q)).mp a.property
    fin_cases k <;>
      simp [Fin.sum_univ_succ, ceVector, ceLabel, cBasis, coords_coordinateBasis,
        coords_add, coords_smul] <;>
      first | exact (hc _ (by decide)).symm | exact (hl _ (by decide)).symm
  right_inv v := by
    funext i
    fin_cases i <;>
      simp [Fin.sum_univ_succ, ceVector, ceLabel, cBasis, coords_coordinateBasis,
        coords_add, coords_smul]

/-- A genuine coordinate equivalence of the actual left f-corner. -/
def cfCoordsEquiv (q : R) : Cf q ≃ₗ[R] (Fin 4 → R) where
  toFun a i := (((a : C q) : TableAlgebra q)).coords ⟨(cfLabel i).val, by omega⟩
  invFun v := ∑ i : Fin 4, v i • cfVector q i
  map_add' a b := by funext i; rfl
  map_smul' r a := by funext i; rfl
  left_inv a := by
    apply Subtype.ext
    apply Subtype.ext
    apply ARCTwentyDimAlgebra.ext q
    funext k
    have hl := (mem_lowerSubalgebra q ((a : C q) : TableAlgebra q)).mp (a : C q).property
    have hc := (mem_Cf_coords q (a : C q)).mp a.property
    fin_cases k <;>
      simp [Fin.sum_univ_succ, cfVector, cfLabel, cBasis, coords_coordinateBasis,
        coords_add, coords_smul] <;>
      first | exact (hc _ (by decide)).symm | exact (hl _ (by decide)).symm
  right_inv v := by
    funext i
    fin_cases i <;>
      simp [Fin.sum_univ_succ, cfVector, cfLabel, cBasis, coords_coordinateBasis,
        coords_add, coords_smul]

/-- The actual R-basis in the stated e-corner order. -/
def ceBasis (q : R) : Module.Basis (Fin 6) R (Ce q) := Module.Basis.ofEquivFun (ceCoordsEquiv q)

/-- The actual R-basis in the stated f-corner order. -/
def cfBasis (q : R) : Module.Basis (Fin 4) R (Cf q) := Module.Basis.ofEquivFun (cfCoordsEquiv q)

private theorem specialize_one (q : R) : specialize q (decode 1) = 1 :=
  ARCScalarEvaluation.evaluate_one q

private theorem specialize_two (q : R) : specialize q (decode 2) = q :=
  ARCScalarEvaluation.evaluate_two q

private theorem specialize_three (q : R) : specialize q (decode 3) = 1 + q := by
  change ARCScalarEvaluation.evaluate q (Nat.xor 1 2) = 1 + q
  rw [ARCScalarEvaluation.evaluate_xor, ARCScalarEvaluation.evaluate_one,
    ARCScalarEvaluation.evaluate_two]

private theorem specialize_four (q : R) : specialize q (decode 4) = q ^ 2 := by
  change ARCScalarEvaluation.evaluate q (2 * 2) = q ^ 2
  rw [ARCScalarEvaluation.evaluate_double, ARCScalarEvaluation.evaluate_two, pow_two]

private theorem lower_u_table (i : Fin 10) :
    tTerms i.val 4 =
      if i = 0 then [(4, 1)] else if i = 1 ∨ i = 2 then [(5, 1)] else
      if i = 6 then [(9, 3)] else [] := by
  fin_cases i <;> rfl

private theorem lower_x_table (i : Fin 10) :
    tTerms i.val 1 =
      if i = 0 then [(1, 1)] else if i = 2 then [(3, 1)] else
      if i = 6 then [(7, 1)] else [] := by
  fin_cases i <;> rfl

private theorem lower_y_table (i : Fin 10) :
    tTerms i.val 2 =
      if i = 0 then [(2, 1)] else if i = 1 then [(3, 2)] else
      if i = 6 then [(7, 4)] else [] := by
  fin_cases i <;> rfl

private theorem specialize_sparse_one (q : R) (j c k : Nat) :
    specialize q (singleTerm j c k) =
      if k = j then specialize q (decode c) else 0 := by
  by_cases h : k = j <;> simp [singleTerm, h]

private theorem lower_u_constants (q : R) (i : Fin 10) (k : Fin 20) :
    specializedConstants q (Fin.castAdd 10 i) 4 k =
      if i = 0 ∧ k = 4 then 1 else
      if (i = 1 ∨ i = 2) ∧ k = 5 then 1 else
      if i = 6 ∧ k = 9 then 1 + q else 0 := by
  change specialize q (sumTerms (tTerms i.val 4) k.val) = _
  rw [lower_u_table]
  fin_cases i <;>
    simp [specialize_sparse_one, specialize_one, specialize_three, Fin.ext_iff]

private theorem lower_x_constants (q : R) (i : Fin 10) (k : Fin 20) :
    specializedConstants q (Fin.castAdd 10 i) 1 k =
      if i = 0 ∧ k = 1 then 1 else
      if i = 2 ∧ k = 3 then 1 else
      if i = 6 ∧ k = 7 then 1 else 0 := by
  change specialize q (sumTerms (tTerms i.val 1) k.val) = _
  rw [lower_x_table]
  fin_cases i <;> simp [specialize_sparse_one, specialize_one, Fin.ext_iff]

private theorem lower_y_constants (q : R) (i : Fin 10) (k : Fin 20) :
    specializedConstants q (Fin.castAdd 10 i) 2 k =
      if i = 0 ∧ k = 2 then 1 else
      if i = 1 ∧ k = 3 then q else
      if i = 6 ∧ k = 7 then q ^ 2 else 0 := by
  change specialize q (sumTerms (tTerms i.val 2) k.val) = _
  rw [lower_y_table]
  fin_cases i <;>
    simp [specialize_sparse_one, specialize_one, specialize_two, specialize_four, Fin.ext_iff]

private theorem mul_lower_basis_coords (q : R) (a : C q) (b k : Fin 20) :
    ((a : TableAlgebra q) * coordinateBasis q b).coords k =
      ∑ i : Fin 10, (a : TableAlgebra q).coords (Fin.castAdd 10 i) *
        specializedConstants q (Fin.castAdd 10 i) b k := by
  rw [mul_basis_right_coords]
  apply Fin.sum_trunc (a := 10) (b := 10)
  intro j
  have hu := (mem_lowerSubalgebra q (a : TableAlgebra q)).mp a.property
  rw [hu _ (by change ¬ 10 + j.val < 10; omega), zero_mul]

/-- A whole lower-algebra input right-multiplied by u; only three output labels survive. -/
private theorem mul_u_coords (q : R) (a : C q) (k : Fin 20) :
    ((a : TableAlgebra q) * coordinateBasis q 4).coords k =
      if k = 4 then (a : TableAlgebra q).coords 0 else
      if k = 5 then (a : TableAlgebra q).coords 1 + (a : TableAlgebra q).coords 2 else
      if k = 9 then (1 + q) * (a : TableAlgebra q).coords 6 else 0 := by
  rw [mul_lower_basis_coords]
  simp_rw [lower_u_constants]
  by_cases h4 : k = 4 <;> by_cases h5 : k = 5 <;> by_cases h9 : k = 9 <;>
    simp [Fin.sum_univ_succ, h4, h5, h9, mul_comm]

private theorem mul_x_coords (q : R) (a : C q) (k : Fin 20) :
    ((a : TableAlgebra q) * coordinateBasis q 1).coords k =
      if k = 1 then (a : TableAlgebra q).coords 0 else
      if k = 3 then (a : TableAlgebra q).coords 2 else
      if k = 7 then (a : TableAlgebra q).coords 6 else 0 := by
  rw [mul_lower_basis_coords]
  simp_rw [lower_x_constants]
  by_cases h1 : k = 1 <;> by_cases h3 : k = 3 <;> by_cases h7 : k = 7 <;>
    simp [h1, h3, h7]

private theorem mul_y_coords (q : R) (a : C q) (k : Fin 20) :
    ((a : TableAlgebra q) * coordinateBasis q 2).coords k =
      if k = 2 then (a : TableAlgebra q).coords 0 else
      if k = 3 then q * (a : TableAlgebra q).coords 1 else
      if k = 7 then q ^ 2 * (a : TableAlgebra q).coords 6 else 0 := by
  rw [mul_lower_basis_coords]
  simp_rw [lower_y_constants]
  by_cases h2 : k = 2 <;> by_cases h3 : k = 3 <;> by_cases h7 : k = 7 <;>
    simp [h2, h3, h7, mul_comm]

/-- Entire actual u map in the constructed corner coordinate equivalences. -/
theorem rightU_coords (q : R) (a : Ce q) :
    cfCoordsEquiv q (rightU q a) =
      ![0, ceCoordsEquiv q a 0,
        ceCoordsEquiv q a 1 + ceCoordsEquiv q a 2,
        (1 + q) * ceCoordsEquiv q a 4] := by
  funext i
  fin_cases i <;>
    change (((a : C q) : TableAlgebra q) * coordinateBasis q 4).coords _ = _ <;>
    rw [mul_u_coords] <;>
    simp [ceCoordsEquiv, ceLabel, cfLabel]

/-- Entire actual ell_n map, including arbitrary n and every corner component. -/
theorem rightEll_coords (q : R) (n : Nat) (a : Ce q) :
    ceCoordsEquiv q (rightEll q n a) =
      ![0, ceCoordsEquiv q a 0, q ^ n * ceCoordsEquiv q a 0,
        q ^ (n + 1) * ceCoordsEquiv q a 1 + ceCoordsEquiv q a 2, 0,
        (1 + q ^ (n + 2)) * ceCoordsEquiv q a 4] := by
  funext i
  fin_cases i <;>
    change ((((a : C q) : TableAlgebra q) *
      (coordinateBasis q 1 + q ^ n • coordinateBasis q 2)).coords _) = _ <;>
    rw [mul_add, table_mul_smul, coords_add, coords_smul] <;>
    simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul, mul_x_coords, mul_y_coords] <;>
    simp [ceCoordsEquiv, ceLabel, pow_succ] <;> ring

section Field
variable {K : Type*} [Field K] [CharP K 2]

/-- Every actual kernel element of the first map has an explicit corner preimage. -/
theorem rightU_zero_iff_exists (q : K)
    (h1 : 1 + q ≠ 0) (h2 : 1 + q ^ 2 ≠ 0) (a : Ce q) :
    rightU q a = 0 ↔ ∃ b : Ce q, rightEll q 0 b = a := by
  constructor
  · intro ha
    have hc := congrArg (cfCoordsEquiv q) ha
    rw [rightU_coords, map_zero] at hc
    have h0 : ceCoordsEquiv q a 0 = 0 := by simpa using congrFun hc 1
    have h12 : ceCoordsEquiv q a 1 + ceCoordsEquiv q a 2 = 0 := by
      simpa using congrFun hc 2
    have h4m : (1 + q) * ceCoordsEquiv q a 4 = 0 := by
      simpa using congrFun hc 3
    have h21 : ceCoordsEquiv q a 2 = ceCoordsEquiv q a 1 :=
      (CharTwo.add_eq_zero.mp h12).symm
    have h4 : ceCoordsEquiv q a 4 = 0 := (mul_eq_zero.mp h4m).resolve_left h1
    let v : Fin 6 → K := ![ceCoordsEquiv q a 1, 0, ceCoordsEquiv q a 3, 0,
      ceCoordsEquiv q a 5 / (1 + q ^ 2), 0]
    refine ⟨(ceCoordsEquiv q).symm v, ?_⟩
    apply (ceCoordsEquiv q).injective
    simp only [rightEll_coords, (ceCoordsEquiv q).apply_symm_apply]
    funext i
    fin_cases i <;> simp [v, h0, h21, h4]
    rw [← mul_div_assoc, mul_div_cancel_left₀ _ h2]
  · rintro ⟨b, rfl⟩
    apply (cfCoordsEquiv q).injective
    simp only [rightU_coords, rightEll_coords, map_zero]
    funext i
    fin_cases i <;> simp [CharTwo.add_self_eq_zero]

/-- Actual kernel and image equality for the first two right-multiplication maps. -/
theorem rightU_ker_eq_range (q : K)
    (h1 : 1 + q ≠ 0) (h2 : 1 + q ^ 2 ≠ 0) :
    LinearMap.ker (rightU q) = LinearMap.range (rightEll q 0) := by
  ext a
  exact rightU_zero_iff_exists q h1 h2 a

/-- Every degree of the actual right-multiplication sequence has an explicit preimage. -/
theorem rightEll_zero_iff_exists (q : K) (n : Nat)
    (h2 : 1 + q ^ (n + 2) ≠ 0) (h3 : 1 + q ^ (n + 3) ≠ 0) (a : Ce q) :
    rightEll q n a = 0 ↔ ∃ b : Ce q, rightEll q (n + 1) b = a := by
  constructor
  · intro ha
    have hc := congrArg (ceCoordsEquiv q) ha
    rw [rightEll_coords, map_zero] at hc
    have h0 : ceCoordsEquiv q a 0 = 0 := by simpa using congrFun hc 1
    have h12 : q ^ (n + 1) * ceCoordsEquiv q a 1 + ceCoordsEquiv q a 2 = 0 := by
      simpa using congrFun hc 3
    have h4m : (1 + q ^ (n + 2)) * ceCoordsEquiv q a 4 = 0 := by
      simpa using congrFun hc 5
    have h21 : ceCoordsEquiv q a 2 = q ^ (n + 1) * ceCoordsEquiv q a 1 :=
      (CharTwo.add_eq_zero.mp h12).symm
    have h4 : ceCoordsEquiv q a 4 = 0 := (mul_eq_zero.mp h4m).resolve_left h2
    let v : Fin 6 → K := ![ceCoordsEquiv q a 1, 0, ceCoordsEquiv q a 3, 0,
      ceCoordsEquiv q a 5 / (1 + q ^ (n + 3)), 0]
    refine ⟨(ceCoordsEquiv q).symm v, ?_⟩
    apply (ceCoordsEquiv q).injective
    simp only [rightEll_coords, (ceCoordsEquiv q).apply_symm_apply]
    funext i
    fin_cases i <;> simp [v, h0, h21, h4, Nat.add_assoc]
    rw [← mul_div_assoc, mul_div_cancel_left₀ _ h3]
  · rintro ⟨b, rfl⟩
    apply (ceCoordsEquiv q).injective
    simp only [rightEll_coords, map_zero]
    funext i
    fin_cases i <;> simp [CharTwo.add_self_eq_zero]

/-- All degrees of the actual corner sequence are exact under the indicated factors. -/
theorem rightEll_ker_eq_range (q : K) (n : Nat)
    (h2 : 1 + q ^ (n + 2) ≠ 0) (h3 : 1 + q ^ (n + 3) ≠ 0) :
    LinearMap.ker (rightEll q n) = LinearMap.range (rightEll q (n + 1)) := by
  ext a
  exact rightEll_zero_iff_exists q n h2 h3 a

end Field

#print axioms cBasis
#print axioms right_idempotent_coords
#print axioms e_mul_e
#print axioms f_mul_f
#print axioms Ce
#print axioms Cf
#print axioms mem_Ce_coords
#print axioms mem_Cf_coords
#print axioms u_mul_f
#print axioms ell_mul_e
#print axioms rightU
#print axioms rightEll
#print axioms ceVector
#print axioms cfVector
#print axioms ceCoordsEquiv
#print axioms cfCoordsEquiv
#print axioms ceBasis
#print axioms cfBasis
#print axioms rightU_coords
#print axioms rightEll_coords
#print axioms rightU_zero_iff_exists
#print axioms rightU_ker_eq_range
#print axioms rightEll_zero_iff_exists
#print axioms rightEll_ker_eq_range

end
end ARCLowerAlgebraResolution
