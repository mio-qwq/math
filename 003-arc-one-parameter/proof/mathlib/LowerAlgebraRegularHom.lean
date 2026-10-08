import LowerAlgebraProjective

/-!
# Actual regular-target corner Hom maps

The right corners are R-submodules of the installed lower algebra.
Evaluation at the idempotents identifies C-linear maps from the actual
left corners with these right corners. Precomposition becomes actual
left multiplication. The coordinate computations here describe the
regular-target Hom sequence; categorical Ext comparison is separate.
-/

namespace ARCLowerAlgebraRegularHom

open ARCFiniteCore ARCBitPolynomial ARCTermSemantics ARCFiniteTableContraction
open ARCTwentyDimAssociativity ARCTwentyDimAlgebra ARCTwentyDimCochainAlgebra
open ARCTwentyDimFrobenius ARCTwentyDimDualScaleEndomorphism
open ARCTwentyDimTrivialExtension ARCCochainIdempotentClosure
open ARCLowerAlgebraResolution ARCLowerAlgebraProjective
open scoped BigOperators

noncomputable section
variable {R : Type*} [CommRing R] [CharP R 2]

private theorem basis_mul_left_coords (q : R) (a : TableAlgebra q)
    (b k : Fin 20) :
    (coordinateBasis q b * a).coords k =
      ∑ i : Fin 20, a.coords i * specializedConstants q b i k := by
  change (∑ i : Fin 20, ∑ j : Fin 20,
    (coordinateBasis q b).coords i * a.coords j * specializedConstants q i j k) = _
  simp [coords_coordinateBasis]

/-- Whole-vector action of the installed left idempotents. -/
theorem left_idempotent_coords (q : R) (a : TableAlgebra q)
    (s : Fin 2) (k : Fin 20) :
    (coordinateBasis q (idempotentIndex s) * a).coords k =
      if tLeft k.val = (idempotentIndex s).val then a.coords k else 0 := by
  rw [basis_mul_left_coords]
  simp_rw [specializedB_idempotent_left, mul_ite, mul_one, mul_zero]
  rw [Finset.sum_eq_single k]
  · simp
  · intro j hj hne
    simp [hne]
  · simp

/-- A right corner is an R-submodule, with no left-C closure assertion. -/
def eC (q : R) : Submodule R (C q) where
  carrier := {a | e q * a = a}
  zero_mem' := by simp
  add_mem' ha hb := by simp only [Set.mem_ofPred_eq] at *; rw [mul_add, ha, hb]
  smul_mem' r a ha := by
    change e q * a = a at ha
    change e q * (r • a) = r • a
    rw [Algebra.mul_smul_comm, ha]

def fC (q : R) : Submodule R (C q) where
  carrier := {a | f q * a = a}
  zero_mem' := by simp
  add_mem' ha hb := by simp only [Set.mem_ofPred_eq] at *; rw [mul_add, ha, hb]
  smul_mem' r a ha := by
    change f q * a = a at ha
    change f q * (r • a) = r • a
    rw [Algebra.mul_smul_comm, ha]

theorem mem_eC_coords (q : R) (a : C q) :
    a ∈ eC q ↔ ∀ k : Fin 20, tLeft k.val ≠ 0 → (a : TableAlgebra q).coords k = 0 := by
  change e q * a = a ↔ _
  constructor
  · intro h k hk
    have hc := congrArg (fun b : C q => (b : TableAlgebra q).coords k) h
    change (coordinateBasis q 0 * (a : TableAlgebra q)).coords k = _ at hc
    rw [show (0 : Fin 20) = idempotentIndex 0 by rfl, left_idempotent_coords] at hc
    simpa [idempotentIndex, hk] using hc.symm
  · intro h
    apply Subtype.ext
    apply ARCTwentyDimAlgebra.ext q
    funext k
    change (coordinateBasis q 0 * (a : TableAlgebra q)).coords k = _
    rw [show (0 : Fin 20) = idempotentIndex 0 by rfl, left_idempotent_coords]
    by_cases hk : tLeft k.val = 0 <;> simp [idempotentIndex, hk, h]

theorem mem_fC_coords (q : R) (a : C q) :
    a ∈ fC q ↔ ∀ k : Fin 20, tLeft k.val ≠ 8 → (a : TableAlgebra q).coords k = 0 := by
  change f q * a = a ↔ _
  constructor
  · intro h k hk
    have hc := congrArg (fun b : C q => (b : TableAlgebra q).coords k) h
    change (coordinateBasis q 8 * (a : TableAlgebra q)).coords k = _ at hc
    rw [show (8 : Fin 20) = idempotentIndex 1 by rfl, left_idempotent_coords] at hc
    simpa [idempotentIndex, hk] using hc.symm
  · intro h
    apply Subtype.ext
    apply ARCTwentyDimAlgebra.ext q
    funext k
    change (coordinateBasis q 8 * (a : TableAlgebra q)).coords k = _
    rw [show (8 : Fin 20) = idempotentIndex 1 by rfl, left_idempotent_coords]
    by_cases hk : tLeft k.val = 8 <;> simp [idempotentIndex, hk, h]

private theorem lower_basis_left_idempotent (q : R) (i : Fin 10) (s : Fin 2)
    (hi : cLeft i.val = (idempotentIndex s).val) :
    coordinateBasis q (idempotentIndex s) * (cBasis q i : TableAlgebra q) = cBasis q i := by
  apply ARCTwentyDimAlgebra.ext q
  funext k
  rw [left_idempotent_coords, cBasis_val, coords_coordinateBasis]
  by_cases hk : (⟨i.val, by omega⟩ : Fin 20) = k
  · subst k
    simp [tLeft, i.isLt, hi]
  · simp [hk]

def ecLabel : Fin 6 → Fin 10 := ![0, 1, 2, 3, 4, 5]
def fcLabel : Fin 4 → Fin 10 := ![8, 6, 7, 9]

def ecVector (q : R) (i : Fin 6) : eC q :=
  ⟨cBasis q (ecLabel i), by
    apply Subtype.ext
    exact lower_basis_left_idempotent q (ecLabel i) 0 (by fin_cases i <;> rfl)⟩

def fcVector (q : R) (i : Fin 4) : fC q :=
  ⟨cBasis q (fcLabel i), by
    apply Subtype.ext
    exact lower_basis_left_idempotent q (fcLabel i) 1 (by fin_cases i <;> rfl)⟩

/-- Actual right-e corner coordinates, in the order e,x,y,z,u,v. -/
def ecCoordsEquiv (q : R) : eC q ≃ₗ[R] (Fin 6 → R) where
  toFun a i := (((a : C q) : TableAlgebra q)).coords ⟨(ecLabel i).val, by omega⟩
  invFun v := ∑ i : Fin 6, v i • ecVector q i
  map_add' a b := by funext i; rfl
  map_smul' r a := by funext i; rfl
  left_inv a := by
    apply Subtype.ext
    apply Subtype.ext
    apply ARCTwentyDimAlgebra.ext q
    funext k
    have hl := (mem_lowerSubalgebra q ((a : C q) : TableAlgebra q)).mp (a : C q).property
    have hc := (mem_eC_coords q (a : C q)).mp a.property
    fin_cases k <;>
      simp [Fin.sum_univ_succ, ecVector, ecLabel, cBasis, coords_coordinateBasis,
        coords_add, coords_smul] <;>
      first | exact (hc _ (by decide)).symm | exact (hl _ (by decide)).symm
  right_inv v := by
    funext i
    fin_cases i <;>
      simp [Fin.sum_univ_succ, ecVector, ecLabel, cBasis, coords_coordinateBasis,
        coords_add, coords_smul]

/-- Actual right-f corner coordinates, in the order f,t,j,n. -/
def fcCoordsEquiv (q : R) : fC q ≃ₗ[R] (Fin 4 → R) where
  toFun a i := (((a : C q) : TableAlgebra q)).coords ⟨(fcLabel i).val, by omega⟩
  invFun v := ∑ i : Fin 4, v i • fcVector q i
  map_add' a b := by funext i; rfl
  map_smul' r a := by funext i; rfl
  left_inv a := by
    apply Subtype.ext
    apply Subtype.ext
    apply ARCTwentyDimAlgebra.ext q
    funext k
    have hl := (mem_lowerSubalgebra q ((a : C q) : TableAlgebra q)).mp (a : C q).property
    have hc := (mem_fC_coords q (a : C q)).mp a.property
    fin_cases k <;>
      simp [Fin.sum_univ_succ, fcVector, fcLabel, cBasis, coords_coordinateBasis,
        coords_add, coords_smul] <;>
      first | exact (hc _ (by decide)).symm | exact (hl _ (by decide)).symm
  right_inv v := by
    funext i
    fin_cases i <;>
      simp [Fin.sum_univ_succ, fcVector, fcLabel, cBasis, coords_coordinateBasis,
        coords_add, coords_smul]

def ecBasis (q : R) : Module.Basis (Fin 6) R (eC q) := Module.Basis.ofEquivFun (ecCoordsEquiv q)
def fcBasis (q : R) : Module.Basis (Fin 4) R (fC q) := Module.Basis.ofEquivFun (fcCoordsEquiv q)

def fGenerator (q : R) : Cf q := ⟨f q, f_mul_f q⟩

theorem cf_generator_smul (q : R) (a : Cf q) :
    (a : C q) • fGenerator q = a := by
  apply Subtype.ext
  exact a.property

theorem f_generator_fixed (q : R) : f q • fGenerator q = fGenerator q := by
  apply Subtype.ext
  exact f_mul_f q

/-- Evaluation is R-linear; its inverse retains the full actual C-linear map. -/
def evalHomCe (q : R) : (Ce q →ₗ[C q] C q) ≃ₗ[R] eC q where
  toFun h := ⟨h (eGenerator q), by
    change e q • h (eGenerator q) = h (eGenerator q)
    rw [← h.map_smul, e_generator_fixed]⟩
  invFun v := {
    toFun a := (a : C q) * (v : C q)
    map_add' a b := add_mul (a : C q) b (v : C q)
    map_smul' c a := mul_assoc c (a : C q) (v : C q) }
  map_add' h j := by apply Subtype.ext; rfl
  map_smul' r h := by apply Subtype.ext; rfl
  left_inv h := by
    apply LinearMap.ext
    intro a
    change (a : C q) • h (eGenerator q) = h a
    rw [← h.map_smul, ce_generator_smul]
  right_inv v := by
    apply Subtype.ext
    exact v.property

def evalHomCf (q : R) : (Cf q →ₗ[C q] C q) ≃ₗ[R] fC q where
  toFun h := ⟨h (fGenerator q), by
    change f q • h (fGenerator q) = h (fGenerator q)
    rw [← h.map_smul, f_generator_fixed]⟩
  invFun v := {
    toFun a := (a : C q) * (v : C q)
    map_add' a b := add_mul (a : C q) b (v : C q)
    map_smul' c a := mul_assoc c (a : C q) (v : C q) }
  map_add' h j := by apply Subtype.ext; rfl
  map_smul' r h := by apply Subtype.ext; rfl
  left_inv h := by
    apply LinearMap.ext
    intro a
    change (a : C q) • h (fGenerator q) = h a
    rw [← h.map_smul, cf_generator_smul]
  right_inv v := by
    apply Subtype.ext
    exact v.property

theorem e_mul_u (q : R) : e q * u q = u q := by
  apply Subtype.ext
  exact lower_basis_left_idempotent q 4 0 rfl

theorem e_mul_ell (q : R) (n : Nat) : e q * ell q n = ell q n := by
  have hx : e q * cBasis q 1 = cBasis q 1 := by
    apply Subtype.ext
    exact lower_basis_left_idempotent q 1 0 rfl
  have hy : e q * cBasis q 2 = cBasis q 2 := by
    apply Subtype.ext
    exact lower_basis_left_idempotent q 2 0 rfl
  simp only [ell, mul_add, Algebra.mul_smul_comm, hx, hy]

def leftU (q : R) : fC q →ₗ[R] eC q where
  toFun a := ⟨u q * (a : C q), by
    change e q * (u q * (a : C q)) = _
    rw [← mul_assoc, e_mul_u]⟩
  map_add' a b := by apply Subtype.ext; exact mul_add (u q) (a : C q) b
  map_smul' r a := by apply Subtype.ext; exact Algebra.mul_smul_comm r (u q) (a : C q)

def leftEll (q : R) (n : Nat) : eC q →ₗ[R] eC q where
  toFun a := ⟨ell q n * (a : C q), by
    change e q * (ell q n * (a : C q)) = _
    rw [← mul_assoc, e_mul_ell]⟩
  map_add' a b := by apply Subtype.ext; exact mul_add (ell q n) (a : C q) b
  map_smul' r a := by apply Subtype.ext; exact Algebra.mul_smul_comm r (ell q n) (a : C q)

/-- Actual precomposition with the first differential is actual left multiplication. -/
theorem eval_precompose_U (q : R) (h : Cf q →ₗ[C q] C q) :
    evalHomCe q (h.comp (rightU q)) = leftU q (evalHomCf q h) := by
  apply Subtype.ext
  change h (rightU q (eGenerator q)) = u q • h (fGenerator q)
  rw [← h.map_smul]
  congr 1
  apply Subtype.ext
  change e q * u q = u q * f q
  rw [e_mul_u, u_mul_f]

theorem eval_precompose_ell (q : R) (n : Nat) (h : Ce q →ₗ[C q] C q) :
    evalHomCe q (h.comp (rightEll q n)) = leftEll q n (evalHomCe q h) := by
  apply Subtype.ext
  change h (rightEll q n (eGenerator q)) = ell q n • h (eGenerator q)
  rw [← h.map_smul]
  congr 1
  apply Subtype.ext
  change e q * ell q n = ell q n * e q
  rw [e_mul_ell, ell_mul_e]

private theorem specialize_one (q : R) : specialize q (decode 1) = 1 :=
  ARCScalarEvaluation.evaluate_one q

private theorem specialize_two (q : R) : specialize q (decode 2) = q :=
  ARCScalarEvaluation.evaluate_two q

private theorem specialize_single (q : R) (j c k : Nat) :
    specialize q (singleTerm j c k) =
      if k = j then specialize q (decode c) else 0 := by
  by_cases h : k = j <;> simp [singleTerm, h]

private theorem lower_u_table (i : Fin 10) :
    tTerms 4 i.val =
      if i = 6 then [(2, 1), (1, 2)] else if i = 7 then [(3, 1)] else
      if i = 8 then [(4, 1)] else if i = 9 then [(5, 1)] else [] := by
  fin_cases i <;> rfl

private theorem lower_x_table (i : Fin 10) :
    tTerms 1 i.val =
      if i = 0 then [(1, 1)] else if i = 2 then [(3, 2)] else
      if i = 4 then [(5, 1)] else [] := by
  fin_cases i <;> rfl

private theorem lower_y_table (i : Fin 10) :
    tTerms 2 i.val =
      if i = 0 then [(2, 1)] else if i = 1 then [(3, 1)] else
      if i = 4 then [(5, 1)] else [] := by
  fin_cases i <;> rfl

private theorem lower_u_constants (q : R) (i : Fin 10) (k : Fin 20) :
    specializedConstants q 4 (Fin.castAdd 10 i) k =
      (if i = 6 ∧ k = 1 then q else 0) + (if i = 6 ∧ k = 2 then 1 else 0) +
      (if i = 7 ∧ k = 3 then 1 else 0) + (if i = 8 ∧ k = 4 then 1 else 0) +
      (if i = 9 ∧ k = 5 then 1 else 0) := by
  change specialize q (sumTerms (tTerms 4 i.val) k.val) = _
  rw [lower_u_table]
  fin_cases i <;>
    simp [specialize_single, specialize_one, specialize_two, Fin.ext_iff, add_comm]

private theorem lower_x_constants (q : R) (i : Fin 10) (k : Fin 20) :
    specializedConstants q 1 (Fin.castAdd 10 i) k =
      if i = 0 ∧ k = 1 then 1 else if i = 2 ∧ k = 3 then q else
      if i = 4 ∧ k = 5 then 1 else 0 := by
  change specialize q (sumTerms (tTerms 1 i.val) k.val) = _
  rw [lower_x_table]
  fin_cases i <;> simp [specialize_single, specialize_one, specialize_two, Fin.ext_iff]

private theorem lower_y_constants (q : R) (i : Fin 10) (k : Fin 20) :
    specializedConstants q 2 (Fin.castAdd 10 i) k =
      if i = 0 ∧ k = 2 then 1 else if i = 1 ∧ k = 3 then 1 else
      if i = 4 ∧ k = 5 then 1 else 0 := by
  change specialize q (sumTerms (tTerms 2 i.val) k.val) = _
  rw [lower_y_table]
  fin_cases i <;> simp [specialize_single, specialize_one, Fin.ext_iff]

private theorem lower_basis_mul_coords (q : R) (a : C q) (b k : Fin 20) :
    (coordinateBasis q b * (a : TableAlgebra q)).coords k =
      ∑ i : Fin 10, (a : TableAlgebra q).coords (Fin.castAdd 10 i) *
        specializedConstants q b (Fin.castAdd 10 i) k := by
  rw [basis_mul_left_coords]
  apply Fin.sum_trunc (a := 10) (b := 10)
  intro j
  have hu := (mem_lowerSubalgebra q (a : TableAlgebra q)).mp a.property
  rw [hu _ (by change ¬ 10 + j.val < 10; omega), zero_mul]

private theorem mul_u_coords (q : R) (a : C q) (k : Fin 20) :
    (coordinateBasis q 4 * (a : TableAlgebra q)).coords k =
      if k = 1 then q * (a : TableAlgebra q).coords 6 else
      if k = 2 then (a : TableAlgebra q).coords 6 else
      if k = 3 then (a : TableAlgebra q).coords 7 else
      if k = 4 then (a : TableAlgebra q).coords 8 else
      if k = 5 then (a : TableAlgebra q).coords 9 else 0 := by
  rw [lower_basis_mul_coords]
  simp_rw [lower_u_constants]
  by_cases h1 : k = 1 <;> by_cases h2 : k = 2 <;> by_cases h3 : k = 3 <;>
    by_cases h4 : k = 4 <;> by_cases h5 : k = 5 <;>
    simp [h1, h2, h3, h4, h5, mul_comm]

private theorem mul_x_coords (q : R) (a : C q) (k : Fin 20) :
    (coordinateBasis q 1 * (a : TableAlgebra q)).coords k =
      if k = 1 then (a : TableAlgebra q).coords 0 else
      if k = 3 then q * (a : TableAlgebra q).coords 2 else
      if k = 5 then (a : TableAlgebra q).coords 4 else 0 := by
  rw [lower_basis_mul_coords]
  simp_rw [lower_x_constants]
  by_cases h1 : k = 1 <;> by_cases h3 : k = 3 <;> by_cases h5 : k = 5 <;>
    simp [h1, h3, h5, mul_comm]

private theorem mul_y_coords (q : R) (a : C q) (k : Fin 20) :
    (coordinateBasis q 2 * (a : TableAlgebra q)).coords k =
      if k = 2 then (a : TableAlgebra q).coords 0 else
      if k = 3 then (a : TableAlgebra q).coords 1 else
      if k = 5 then (a : TableAlgebra q).coords 4 else 0 := by
  rw [lower_basis_mul_coords]
  simp_rw [lower_y_constants]
  by_cases h2 : k = 2 <;> by_cases h3 : k = 3 <;> by_cases h5 : k = 5 <;>
    simp [h2, h3, h5]

theorem leftU_coords (q : R) (a : fC q) :
    ecCoordsEquiv q (leftU q a) =
      ![0, q * fcCoordsEquiv q a 1, fcCoordsEquiv q a 1,
        fcCoordsEquiv q a 2, fcCoordsEquiv q a 0, fcCoordsEquiv q a 3] := by
  funext i
  fin_cases i <;>
    change (coordinateBasis q 4 * (((a : C q) : TableAlgebra q))).coords _ = _ <;>
    rw [mul_u_coords] <;>
    simp [ecLabel, fcCoordsEquiv, fcLabel]

theorem leftEll_coords (q : R) (n : Nat) (a : eC q) :
    ecCoordsEquiv q (leftEll q n a) =
      ![0, ecCoordsEquiv q a 0, q ^ n * ecCoordsEquiv q a 0,
        q ^ n * ecCoordsEquiv q a 1 + q * ecCoordsEquiv q a 2, 0,
        (1 + q ^ n) * ecCoordsEquiv q a 4] := by
  funext i
  fin_cases i <;>
    change (((coordinateBasis q 1 + q ^ n • coordinateBasis q 2) *
      (((a : C q) : TableAlgebra q))).coords _) = _ <;>
    rw [add_mul, table_smul_mul, coords_add, coords_smul] <;>
    simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul, mul_x_coords, mul_y_coords] <;>
    simp [ecCoordsEquiv, ecLabel] <;> ring

theorem leftU_injective (q : R) : Function.Injective (leftU q) := by
  intro a b h
  apply (fcCoordsEquiv q).injective
  have hc := congrArg (ecCoordsEquiv q) h
  simp only [leftU_coords] at hc
  funext i
  fin_cases i
  · simpa using congrFun hc 4
  · simpa using congrFun hc 2
  · simpa using congrFun hc 3
  · simpa using congrFun hc 5

section Field
variable {K : Type*} [Field K] [CharP K 2]

theorem leftEll_zero_ker_eq_range_U (q : K) :
    LinearMap.ker (leftEll q 0) = LinearMap.range (leftU q) := by
  ext a
  constructor
  · intro ha
    have hc := congrArg (ecCoordsEquiv q) ha
    rw [leftEll_coords, map_zero] at hc
    have h0 : ecCoordsEquiv q a 0 = 0 := by simpa using congrFun hc 1
    have h12 : ecCoordsEquiv q a 1 + q * ecCoordsEquiv q a 2 = 0 := by
      simpa using congrFun hc 3
    have h1 : ecCoordsEquiv q a 1 = q * ecCoordsEquiv q a 2 := CharTwo.add_eq_zero.mp h12
    let v : Fin 4 → K := ![ecCoordsEquiv q a 4, ecCoordsEquiv q a 2,
      ecCoordsEquiv q a 3, ecCoordsEquiv q a 5]
    refine ⟨(fcCoordsEquiv q).symm v, ?_⟩
    apply (ecCoordsEquiv q).injective
    simp only [leftU_coords, (fcCoordsEquiv q).apply_symm_apply]
    funext i
    fin_cases i <;> simp [v, h0, h1]
  · rintro ⟨b, rfl⟩
    apply (ecCoordsEquiv q).injective
    simp only [leftEll_coords, leftU_coords, map_zero]
    funext i
    fin_cases i <;> simp [CharTwo.add_self_eq_zero]

/-- The positive left-map kernel has three free actual corner coordinates. -/
theorem leftEll_succ_zero_iff (q : K) (hq : q ≠ 0) (n : Nat)
    (hs : 1 + q ^ (n + 1) ≠ 0) (a : eC q) :
    leftEll q (n + 1) a = 0 ↔
      ecCoordsEquiv q a 0 = 0 ∧
      ecCoordsEquiv q a 2 = q ^ n * ecCoordsEquiv q a 1 ∧
      ecCoordsEquiv q a 4 = 0 := by
  constructor
  · intro ha
    have hc := congrArg (ecCoordsEquiv q) ha
    rw [leftEll_coords, map_zero] at hc
    have h0 : ecCoordsEquiv q a 0 = 0 := by simpa using congrFun hc 1
    have h12 : q ^ (n + 1) * ecCoordsEquiv q a 1 + q * ecCoordsEquiv q a 2 = 0 := by
      simpa using congrFun hc 3
    have hm : q * (q ^ n * ecCoordsEquiv q a 1 + ecCoordsEquiv q a 2) = 0 := by
      calc
        q * (q ^ n * ecCoordsEquiv q a 1 + ecCoordsEquiv q a 2) =
            q ^ (n + 1) * ecCoordsEquiv q a 1 + q * ecCoordsEquiv q a 2 := by
              rw [pow_succ]
              ring
        _ = 0 := h12
    have hsum := (mul_eq_zero.mp hm).resolve_left hq
    have h2 := (CharTwo.add_eq_zero.mp hsum).symm
    have h4m : (1 + q ^ (n + 1)) * ecCoordsEquiv q a 4 = 0 := by
      simpa using congrFun hc 5
    exact ⟨h0, h2, (mul_eq_zero.mp h4m).resolve_left hs⟩
  · rintro ⟨h0, h2, h4⟩
    apply (ecCoordsEquiv q).injective
    simp only [leftEll_coords, map_zero]
    funext i
    fin_cases i <;> simp [h0, h2, h4, pow_succ, mul_assoc]
    rw [mul_left_comm]
    exact CharTwo.add_self_eq_zero _

/-- Above the exceptional index, actual kernels equal the preceding images. -/
theorem leftEll_succ_succ_ker_eq_range (q : K) (hq : q ≠ 0) (n : Nat)
    (hs : 1 + q ^ (n + 1) ≠ 0) (ht : 1 + q ^ (n + 2) ≠ 0) :
    LinearMap.ker (leftEll q (n + 2)) = LinearMap.range (leftEll q (n + 1)) := by
  ext a
  constructor
  · intro ha
    have he := (leftEll_succ_zero_iff q hq (n + 1) ht a).mp ha
    let v : Fin 6 → K := ![ecCoordsEquiv q a 1, 0, ecCoordsEquiv q a 3 / q, 0,
      ecCoordsEquiv q a 5 / (1 + q ^ (n + 1)), 0]
    refine ⟨(ecCoordsEquiv q).symm v, ?_⟩
    apply (ecCoordsEquiv q).injective
    simp only [leftEll_coords, (ecCoordsEquiv q).apply_symm_apply]
    funext i
    fin_cases i <;> simp [v, he.1, he.2.1, he.2.2]
    · rw [← mul_div_assoc, mul_div_cancel_left₀ _ hq]
    · rw [← mul_div_assoc, mul_div_cancel_left₀ _ hs]
  · rintro ⟨b, rfl⟩
    apply (ecCoordsEquiv q).injective
    simp only [leftEll_coords, map_zero]
    funext i
    fin_cases i <;>
      simp [pow_succ, mul_assoc, mul_comm, CharTwo.add_self_eq_zero]

/-- The actual v basis vector represents the exceptional Hom-sequence class. -/
def regularV (q : K) : eC q := ecVector q 5

theorem regularV_coords (q : K) : ecCoordsEquiv q (regularV q) = ![0, 0, 0, 0, 0, 1] := by
  funext i
  fin_cases i <;>
    simp [regularV, ecCoordsEquiv, ecVector, ecLabel, cBasis, coords_coordinateBasis]

/-- Its coefficient is unchanged when an actual preceding boundary is added. -/
theorem boundary_add_v_coefficient (q : K) (b : eC q) (lambda : K) :
    ecCoordsEquiv q (leftEll q 0 b + lambda • regularV q) 5 = lambda := by
  rw [map_add, map_smul, leftEll_coords, regularV_coords]
  simp [CharTwo.add_self_eq_zero]

/-- Every actual exceptional cycle is a boundary plus one v coefficient. -/
theorem leftEll_one_zero_iff_boundary_add_v (q : K) (hq : q ≠ 0)
    (hs : 1 + q ≠ 0) (a : eC q) :
    leftEll q 1 a = 0 ↔
      ∃ b : eC q, ∃ lambda : K, a = leftEll q 0 b + lambda • regularV q := by
  constructor
  · intro ha
    have he := (leftEll_succ_zero_iff q hq 0 (by simpa using hs) a).mp ha
    let v : Fin 6 → K := ![ecCoordsEquiv q a 1, ecCoordsEquiv q a 3, 0, 0, 0, 0]
    refine ⟨(ecCoordsEquiv q).symm v, ecCoordsEquiv q a 5, ?_⟩
    apply (ecCoordsEquiv q).injective
    rw [map_add, map_smul, leftEll_coords, (ecCoordsEquiv q).apply_symm_apply, regularV_coords]
    funext i
    fin_cases i <;> simp [v, he.1, he.2.1, he.2.2]
  · rintro ⟨b, lambda, rfl⟩
    apply (ecCoordsEquiv q).injective
    rw [map_zero, leftEll_coords, map_add, map_smul, leftEll_coords, regularV_coords]
    funext i
    fin_cases i <;> simp [CharTwo.add_self_eq_zero]

/-- The actual v cycle cannot be any preceding boundary. -/
theorem regularV_not_boundary (q : K) :
    regularV q ∉ LinearMap.range (leftEll q 0) := by
  rintro ⟨b, hb⟩
  have hc := congrArg (fun a : eC q => ecCoordsEquiv q a 5) hb
  rw [leftEll_coords, regularV_coords] at hc
  simp [CharTwo.add_self_eq_zero] at hc

end Field

#print axioms left_idempotent_coords
#print axioms eC
#print axioms fC
#print axioms mem_eC_coords
#print axioms mem_fC_coords
#print axioms ecVector
#print axioms fcVector
#print axioms ecCoordsEquiv
#print axioms fcCoordsEquiv
#print axioms ecBasis
#print axioms fcBasis
#print axioms fGenerator
#print axioms cf_generator_smul
#print axioms f_generator_fixed
#print axioms evalHomCe
#print axioms evalHomCf
#print axioms e_mul_u
#print axioms e_mul_ell
#print axioms leftU
#print axioms leftEll
#print axioms eval_precompose_U
#print axioms eval_precompose_ell
#print axioms leftU_coords
#print axioms leftEll_coords
#print axioms leftU_injective
#print axioms leftEll_zero_ker_eq_range_U
#print axioms leftEll_succ_zero_iff
#print axioms leftEll_succ_succ_ker_eq_range
#print axioms regularV
#print axioms regularV_coords
#print axioms boundary_add_v_coefficient
#print axioms leftEll_one_zero_iff_boundary_add_v
#print axioms regularV_not_boundary

end
end ARCLowerAlgebraRegularHom
