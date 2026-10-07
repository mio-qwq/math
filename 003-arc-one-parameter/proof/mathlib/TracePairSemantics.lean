import TwentyDimAssociativity

/-!
Scalar coefficient extraction and the frozen trace-pairing certificate are
interpreted in genuine F₂[X]. The trace on all twenty-coordinate vectors
and its nondegeneracy are proved for the explicit double-sum multiplication.
No Algebra instance, Hochschild complex, Ext object or full ARC realization
is constructed here.
-/

namespace ARCTracePairSemantics

open ARCFiniteCore ARCBitPolynomial ARCTermSemantics ARCFiniteTableContraction
open ARCTwentyDimAssociativity
open scoped BigOperators

noncomputable section

/-- Scalar coefficient extraction accumulates the genuine polynomial
coefficient, without any byte-size bound and allowing repeated labels. -/
theorem coefficientFoldl_semantics (terms : Terms) (i : Nat) :
    ∀ acc : Nat,
      decode (terms.foldl (fun acc term =>
        if term.1 = i then Nat.xor acc term.2 else acc) acc) =
      decode acc + sumTerms terms i := by
  induction terms with
  | nil =>
      intro acc
      simp
  | cons term terms ih =>
      intro acc
      rw [List.foldl_cons, ih]
      by_cases h : term.1 = i
      · rw [ite_eq_left h, decode_xor, sumTerms_cons]
        simp [h, singleTerm, add_assoc]
      · have h' : i ≠ term.1 := Ne.symm h
        simp [h, h', sumTerms_cons, singleTerm]

/-- The actual polynomial value of a frozen sparse coefficient extraction. -/
theorem decode_coefficient (terms : Terms) (i : Nat) :
    decode (coefficient terms i) = sumTerms terms i := by
  simpa only [coefficient, decode_zero, zero_add] using coefficientFoldl_semantics terms i 0

private theorem decode_unit : decode 1 = 1 := by
  rw [decode_split 1]
  simp [bitCoeff]

/-- The certified basis trace pairing is a true polynomial identity. -/
theorem t_basis_trace_pairing (a b : Fin 20) :
    tConstants a b (10 : Fin 20) + tConstants a b (18 : Fin 20) =
      if b.val = dualIndex a.val then 1 else 0 := by
  change sumTerms (tTerms a.val b.val) 10 + sumTerms (tTerms a.val b.val) 18 =
    if b.val = dualIndex a.val then 1 else 0
  have h := congrArg decode (t_trace_pairing a b)
  rw [tracePair, decode_xor, decode_coefficient, decode_coefficient] at h
  split_ifs at h ⊢ <;> simpa only [decode_unit, decode_zero] using h

/-- The explicit dual basis swaps the two ten-coordinate halves. -/
def dualBasis (a : Fin 20) : Fin 20 :=
  ⟨dualIndex a.val, by dsimp [dualIndex]; split_ifs <;> omega⟩

@[simp] theorem dualBasis_val (a : Fin 20) : (dualBasis a).val = dualIndex a.val := rfl

/-- The dual basis map is an involution, established by arithmetic. -/
@[simp] theorem dualBasis_involutive (a : Fin 20) : dualBasis (dualBasis a) = a := by
  apply Fin.ext
  change dualIndex (dualIndex a.val) = a.val
  dsimp [dualIndex]
  split_ifs <;> omega

theorem dualBasis_injective : Function.Injective dualBasis :=
  (show Function.Involutive dualBasis from dualBasis_involutive).injective

/-- Reindex finite sums by the involutive dual-basis permutation. -/
def dualBasisEquiv : Fin 20 ≃ Fin 20 where
  toFun := dualBasis
  invFun := dualBasis
  left_inv := dualBasis_involutive
  right_inv := dualBasis_involutive

/-- The anti-diagonal pairing is symmetric over every commutative semiring. -/
theorem paired_sum_symmetric {R : Type*} [CommSemiring R] (u v : Fin 20 → R) :
    (∑ a : Fin 20, u a * v (dualBasis a)) = ∑ a : Fin 20, v a * u (dualBasis a) := by
  apply Fintype.sum_equiv dualBasisEquiv
  intro a
  change u a * v (dualBasis a) = v (dualBasis a) * u (dualBasis (dualBasis a))
  rw [dualBasis_involutive, mul_comm]

theorem t_basis_trace_pairing_fin (a b : Fin 20) :
    tConstants a b (10 : Fin 20) + tConstants a b (18 : Fin 20) =
      if b = dualBasis a then 1 else 0 := by
  have hb : (b.val = dualIndex a.val) ↔ b = dualBasis a :=
    ⟨fun h => Fin.ext h, fun h => congrArg Fin.val h⟩
  simpa only [hb] using t_basis_trace_pairing a b

/-- The polynomial trace selects the two dual idempotent coordinates. -/
def polynomialTrace (v : PolynomialVector) : Polynomial (ZMod 2) := v 10 + v 18

/-- Exact trace pairing on every vector, not just the twenty basis vectors. -/
theorem polynomial_trace_mul (u v : PolynomialVector) :
    polynomialTrace (polynomialMul u v) = ∑ a : Fin 20, u a * v (dualBasis a) := by
  classical
  unfold polynomialTrace polynomialMul ARCFiniteBilinear.mul
  rw [← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro a ha
  rw [← Finset.sum_add_distrib]
  simp_rw [← mul_add, t_basis_trace_pairing_fin]
  simp

/-- The actual table multiplication has symmetric polynomial trace pairing. -/
theorem polynomial_trace_symmetric (u v : PolynomialVector) :
    polynomialTrace (polynomialMul u v) = polynomialTrace (polynomialMul v u) := by
  rw [polynomial_trace_mul, polynomial_trace_mul]
  exact paired_sum_symmetric u v

/-- Vanishing against every right vector forces the left vector to vanish. -/
theorem polynomial_trace_left_nondegenerate (u : PolynomialVector)
    (hzero : ∀ v, polynomialTrace (polynomialMul u v) = 0) : u = 0 := by
  classical
  funext a
  let v : PolynomialVector := fun b => if b = dualBasis a then 1 else 0
  have h := hzero v
  rw [polynomial_trace_mul] at h
  simpa [v, dualBasis_injective.eq_iff] using h

/-- Vanishing against every left vector forces the right vector to vanish. -/
theorem polynomial_trace_right_nondegenerate (v : PolynomialVector)
    (hzero : ∀ u, polynomialTrace (polynomialMul u v) = 0) : v = 0 := by
  classical
  funext a
  let u : PolynomialVector := fun b => if b = dualBasis a then 1 else 0
  have h := hzero u
  rw [polynomial_trace_mul] at h
  simpa [u] using h

variable {R : Type*} [CommRing R] [CharP R 2]

/-- Trace pairing of the actual specialized structure constants. -/
theorem specialized_basis_trace_pairing (q : R) (a b : Fin 20) :
    specializedConstants q a b (10 : Fin 20) + specializedConstants q a b (18 : Fin 20) =
      if b = dualBasis a then 1 else 0 := by
  have h := congrArg (specialize q) (t_basis_trace_pairing_fin a b)
  rw [map_add] at h
  split_ifs at h ⊢ <;> simpa only [specializedConstants, map_one, map_zero] using h

/-- The two-coordinate trace after specialization in characteristic two. -/
def specializedTrace (v : Fin 20 → R) : R := v 10 + v 18

/-- All vectors satisfy the exact trace formula in every characteristic-two
commutative ring, at every parameter, without a nonvanishing assumption. -/
theorem specialized_trace_mul (q : R) (u v : Fin 20 → R) :
    specializedTrace (specializedMul q u v) = ∑ a : Fin 20, u a * v (dualBasis a) := by
  classical
  unfold specializedTrace specializedMul ARCFiniteBilinear.mul
  rw [← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro a ha
  rw [← Finset.sum_add_distrib]
  simp_rw [← mul_add, specialized_basis_trace_pairing]
  simp

theorem specialized_trace_symmetric (q : R) (u v : Fin 20 → R) :
    specializedTrace (specializedMul q u v) = specializedTrace (specializedMul q v u) := by
  rw [specialized_trace_mul, specialized_trace_mul]
  exact paired_sum_symmetric u v

/-- Specialized trace is left nondegenerate even over a ring with zero divisors. -/
theorem specialized_trace_left_nondegenerate (q : R) (u : Fin 20 → R)
    (hzero : ∀ v, specializedTrace (specializedMul q u v) = 0) : u = 0 := by
  classical
  funext a
  let v : Fin 20 → R := fun b => if b = dualBasis a then 1 else 0
  have h := hzero v
  rw [specialized_trace_mul] at h
  simpa [v, dualBasis_injective.eq_iff] using h

/-- Specialized trace is right nondegenerate over the same general rings. -/
theorem specialized_trace_right_nondegenerate (q : R) (v : Fin 20 → R)
    (hzero : ∀ u, specializedTrace (specializedMul q u v) = 0) : v = 0 := by
  classical
  funext a
  let u : Fin 20 → R := fun b => if b = dualBasis a then 1 else 0
  have h := hzero u
  rw [specialized_trace_mul] at h
  simpa [u] using h

#print axioms decode_coefficient
#print axioms t_basis_trace_pairing
#print axioms dualBasis_involutive
#print axioms polynomial_trace_mul
#print axioms polynomial_trace_symmetric
#print axioms polynomial_trace_left_nondegenerate
#print axioms polynomial_trace_right_nondegenerate
#print axioms specialized_basis_trace_pairing
#print axioms specialized_trace_mul
#print axioms specialized_trace_symmetric
#print axioms specialized_trace_left_nondegenerate
#print axioms specialized_trace_right_nondegenerate

end
end ARCTracePairSemantics
