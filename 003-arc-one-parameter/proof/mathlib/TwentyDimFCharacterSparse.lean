import TwentyDimCharacters

/-!
# The five scalar f-character coefficients of the actual cochain

A finite Nat/List certificate checks the attributed sparse table. Its f-output
has five branches, and the actual trilinear cochain on arbitrary algebra
elements is consequently a five-term coordinate polynomial. The statements
hold at every parameter over any commutative characteristic-two ring.
-/

namespace ARCTwentyDimFCharacterSparse

open ARCFiniteCore ARCBitPolynomial ARCTermSemantics ARCCochainBasisSemantics
open ARCCochainSpecialization ARCTwentyDimAssociativity ARCTwentyDimAlgebra
open ARCTwentyDimCharacters
open scoped BigOperators

noncomputable section

set_option maxRecDepth 20000
set_option maxHeartbeats 0

/-- Only the scalar f-output of the original table is checked, over the
8,000 finite input triples. This is a Nat/List kernel certificate, not a
rerun of the previously frozen four-input cocycle closure certificate. -/
private theorem f_filter_certificate : ∀ a b c : Fin 20,
    (pTerms a.val b.val c.val).filter (fun t => t.1 == 8) =
      (if a = 6 ∧ b = 11 ∧ c = 4 then [(8, 4)] else []) ++
      (if a = 6 ∧ b = 4 ∧ c = 19 then [(8, 4)] else []) ++
      (if a = 19 ∧ b = 6 ∧ c = 4 then [(8, 2)] else []) ++
      (if a = 15 ∧ b = 2 ∧ c = 4 then [(8, 2)] else []) ++
      (if a = 6 ∧ b = 2 ∧ c = 17 then [(8, 8)] else []) := by
  decide

private theorem sumTerms_filter_f (terms : Terms) :
    sumTerms (terms.filter (fun t => t.1 == 8)) 8 = sumTerms terms 8 := by
  induction terms with
  | nil => rfl
  | cons t ts ih =>
      by_cases ht : t.1 = 8
      · simp [ht, sumTerms_cons, ih]
      · simp [ht, sumTerms_cons, ih, singleTerm, Ne.symm ht]

private theorem sumTerms_append_f (xs ys : Terms) :
    sumTerms (xs ++ ys) 8 = sumTerms xs 8 + sumTerms ys 8 := by
  induction xs with
  | nil => simp
  | cons t ts ih =>
      simp only [List.cons_append, sumTerms_cons, Pi.add_apply, ih, add_assoc]

private theorem sumTerms_ite_f (p : Prop) [Decidable p] (xs ys : Terms) :
    sumTerms (if p then xs else ys) 8 =
      if p then sumTerms xs 8 else sumTerms ys 8 := by
  split_ifs <;> rfl

/-- The polynomial f-output coefficients of the original finite table. -/
theorem pTerms_f_sparse (a b c : Fin 20) :
    sumTerms (pTerms a.val b.val c.val) 8 =
      (if a = 6 ∧ b = 11 ∧ c = 4 then decode 4 else 0) +
      (if a = 6 ∧ b = 4 ∧ c = 19 then decode 4 else 0) +
      (if a = 19 ∧ b = 6 ∧ c = 4 then decode 2 else 0) +
      (if a = 15 ∧ b = 2 ∧ c = 4 then decode 2 else 0) +
      (if a = 6 ∧ b = 2 ∧ c = 17 then decode 8 else 0) := by
  rw [← sumTerms_filter_f, f_filter_certificate]
  simp only [sumTerms_append_f, sumTerms_ite_f]
  simp [sumTerms, singleTerm]

variable {R : Type*} [CommRing R] [CharP R 2]

private theorem specialize_decode_two (q : R) : specialize q (decode 2) = q := by
  change ARCScalarEvaluation.evaluate q 2 = q
  exact ARCScalarEvaluation.evaluate_two q

private theorem specialize_decode_four (q : R) : specialize q (decode 4) = q ^ 2 := by
  change ARCScalarEvaluation.evaluate q 4 = q ^ 2
  rw [show (4 : Nat) = 2 * 2 by rfl, ARCScalarEvaluation.evaluate_double,
    ARCScalarEvaluation.evaluate_two, pow_two]

private theorem specialize_decode_eight (q : R) : specialize q (decode 8) = q ^ 3 := by
  change ARCScalarEvaluation.evaluate q 8 = q ^ 3
  rw [show (8 : Nat) = 2 * 4 by rfl, ARCScalarEvaluation.evaluate_double]
  change q * specialize q (decode 4) = q ^ 3
  rw [specialize_decode_four]
  ring

private theorem specialize_ite (q : R) (p : Prop) [Decidable p]
    (s t : Polynomial (ZMod 2)) :
    specialize q (if p then s else t) =
      if p then specialize q s else specialize q t := by
  split_ifs <;> rfl

/-- The actual specialized f-output coefficients; no nonzero parameter or
absence of zero divisors is required. -/
theorem specializedCochainConstants_f_sparse (q : R) (a b c : Fin 20) :
    specializedCochainConstants q a b c 8 =
      (if a = 6 ∧ b = 11 ∧ c = 4 then q ^ 2 else 0) +
      (if a = 6 ∧ b = 4 ∧ c = 19 then q ^ 2 else 0) +
      (if a = 19 ∧ b = 6 ∧ c = 4 then q else 0) +
      (if a = 15 ∧ b = 2 ∧ c = 4 then q else 0) +
      (if a = 6 ∧ b = 2 ∧ c = 17 then q ^ 3 else 0) := by
  unfold specializedCochainConstants pConstants
  change specialize q (sumTerms (pTerms a.val b.val c.val) (8 : Nat)) = _
  rw [pTerms_f_sparse]
  simp only [map_add, specialize_ite, map_zero, specialize_decode_two,
    specialize_decode_four, specialize_decode_eight]

/-- The genuine cochain on the installed table algebra, at arbitrary full
inputs, is the following five-term coordinate polynomial. -/
theorem actualfSimpleP_sparse (q : R) (x y z : TableAlgebra q) :
    actualfSimpleP q x y z =
      q ^ 2 * x.coords 6 * y.coords 11 * z.coords 4 +
      q ^ 2 * x.coords 6 * y.coords 4 * z.coords 19 +
      q * x.coords 19 * y.coords 6 * z.coords 4 +
      q * x.coords 15 * y.coords 2 * z.coords 4 +
      q ^ 3 * x.coords 6 * y.coords 2 * z.coords 17 := by
  change (∑ a : Fin 20, ∑ b : Fin 20, ∑ c : Fin 20,
    x.coords a * y.coords b * z.coords c * specializedCochainConstants q a b c 8) = _
  simp_rw [specializedCochainConstants_f_sparse, mul_add, mul_ite, mul_zero, ite_and]
  simp only [Finset.sum_add_distrib]
  simp
  ring

#print axioms f_filter_certificate
#print axioms pTerms_f_sparse
#print axioms specializedCochainConstants_f_sparse
#print axioms actualfSimpleP_sparse

end
end ARCTwentyDimFCharacterSparse
