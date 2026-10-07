import TwentyDimNilpotence
import TwentyDimCochainAlgebra
import ScalarEvaluation

/-!
An explicit five-factor nonzero word in the augmentation kernel.

The five small basis products are read from the frozen, attributed table.
They give [u,t,u,t,Z].prod = q*(1+q) • E in the actual table algebra.
Together with the already proved uniform six-factor vanishing, this shows
that the bound six is sharp when q*(1+q) is nonzero. No long-word search,
ideal-power API or identification with the Jacobson radical is used here.
-/

namespace ARCTwentyDimNilpotenceSharp

open ARCFiniteCore ARCBitPolynomial ARCTermSemantics ARCFiniteTableContraction
open ARCTwentyDimAssociativity ARCTwentyDimAlgebra ARCTwentyDimFrobenius
open ARCTwentyDimCochainAlgebra ARCTwentyDimAugmentation ARCTwentyDimNilpotence

/-- Only the five sparse products used by the displayed word. -/
private theorem witness_table :
    tTerms 6 13 = [(15, 2)] ∧
      tTerms 4 15 = [(11, 1), (12, 1)] ∧
      tTerms 6 11 = [(14, 2)] ∧
      tTerms 6 12 = [(14, 1)] ∧
      tTerms 4 14 = [(10, 1)] := by decide

noncomputable section

variable {R : Type*} [CommRing R] [CharP R 2]

private theorem specialize_decode_one (q : R) : specialize q (decode 1) = 1 := by
  change ARCScalarEvaluation.evaluate q 1 = 1
  exact ARCScalarEvaluation.evaluate_one q

private theorem specialize_decode_two (q : R) : specialize q (decode 2) = q := by
  change ARCScalarEvaluation.evaluate q 2 = q
  exact ARCScalarEvaluation.evaluate_two q

/-- Sparse singleton data denotes an actual scalar multiple of a basis vector. -/
private theorem singleton_basis_product (q : R) (a b j : Fin 20) (c : Nat)
    (h : tTerms a.val b.val = [(j.val, c)]) :
    coordinateBasis q a * coordinateBasis q b =
      specialize q (decode c) • coordinateBasis q j := by
  apply ARCTwentyDimAlgebra.ext q
  funext k
  rw [coordinateBasis_mul_coords, coords_smul]
  simp [specializedConstants, tConstants, h, sumTerms, singleTerm,
    coords_coordinateBasis, Fin.val_inj, eq_comm]
  split_ifs <;> simp_all

theorem t_mul_Z (q : R) :
    coordinateBasis q 6 * coordinateBasis q 13 = q • coordinateBasis q 15 := by
  simpa only [specialize_decode_two] using
    singleton_basis_product q 6 13 15 2 witness_table.1

theorem u_mul_V (q : R) :
    coordinateBasis q 4 * coordinateBasis q 15 =
      coordinateBasis q 11 + coordinateBasis q 12 := by
  apply ARCTwentyDimAlgebra.ext q
  funext k
  rw [coordinateBasis_mul_coords]
  simp [specializedConstants, tConstants, witness_table.2.1, sumTerms, singleTerm,
    coords_add, coords_coordinateBasis, ARCScalarEvaluation.decode_one, Fin.ext_iff, eq_comm]

theorem t_mul_X (q : R) :
    coordinateBasis q 6 * coordinateBasis q 11 = q • coordinateBasis q 14 := by
  simpa only [specialize_decode_two] using
    singleton_basis_product q 6 11 14 2 witness_table.2.2.1

theorem t_mul_Y (q : R) :
    coordinateBasis q 6 * coordinateBasis q 12 = coordinateBasis q 14 := by
  simpa only [specialize_decode_one, one_smul] using
    singleton_basis_product q 6 12 14 1 witness_table.2.2.2.1

theorem u_mul_U (q : R) :
    coordinateBasis q 4 * coordinateBasis q 14 = coordinateBasis q 10 := by
  simpa only [specialize_decode_one, one_smul] using
    singleton_basis_product q 4 14 10 1 witness_table.2.2.2.2

/-- The concrete ordered five-letter word u,t,u,t,Z. -/
def witnessWord (q : R) : List (TableAlgebra q) :=
  [coordinateBasis q 4, coordinateBasis q 6, coordinateBasis q 4,
    coordinateBasis q 6, coordinateBasis q 13]

theorem witnessWord_length (q : R) : (witnessWord q).length = 5 := rfl

/-- The list product is the actual noncommutative ring product, whose
right-nested evaluation uses just the five displayed table products. -/
theorem witnessWord_prod (q : R) :
    (witnessWord q).prod = (q * (1 + q)) • coordinateBasis q 10 := by
  simp only [witnessWord, List.prod_cons, List.prod_nil, mul_one,
    t_mul_Z, table_mul_smul, u_mul_V, mul_add, t_mul_X, t_mul_Y,
    u_mul_U, smul_add, smul_smul]
  rw [← add_smul]
  congr 1
  ring

private theorem coordinateBasis_in_kernel (q : R) (a : Fin 20)
    (ha0 : a ≠ 0) (ha8 : a ≠ 8) :
    InAugmentationKernel q (coordinateBasis q a) := by
  rw [augmentation_kernel_iff]
  simp [coords_coordinateBasis, ha0, ha8]

/-- Each of the five actual factors lies in the established kernel. -/
theorem witnessWord_in_kernel (q : R) :
    ∀ x ∈ witnessWord q, InAugmentationKernel q x := by
  intro x hx
  simp only [witnessWord, List.mem_cons, List.not_mem_nil, or_false] at hx
  rcases hx with rfl | rfl | rfl | rfl | rfl <;>
    exact coordinateBasis_in_kernel q _ (by decide) (by decide)

/-- The E coordinate reflects the entire coefficient, including over rings
with zero divisors; nonzero q*(1+q) is the precise witness hypothesis. -/
theorem witnessWord_prod_ne_zero (q : R) (hq : q * (1 + q) ≠ 0) :
    (witnessWord q).prod ≠ 0 := by
  intro hz
  apply hq
  rw [witnessWord_prod] at hz
  have hc := congrArg (fun x : TableAlgebra q => x.coords 10) hz
  simpa [coords_smul, coords_coordinateBasis] using hc

/-- There is a nonzero product of five actual augmentation-kernel elements. -/
theorem exists_five_kernel_word_nonzero (q : R) (hq : q * (1 + q) ≠ 0) :
    ∃ xs : List (TableAlgebra q), xs.length = 5 ∧
      (∀ x ∈ xs, InAugmentationKernel q x) ∧ xs.prod ≠ 0 :=
  ⟨witnessWord q, witnessWord_length q, witnessWord_in_kernel q,
    witnessWord_prod_ne_zero q hq⟩

/-- Every purported word-length vanishing threshold at most five fails
under the witness condition. This complements the frozen threshold six. -/
theorem no_vanishing_threshold_at_most_five (q : R)
    (hq : q * (1 + q) ≠ 0) (n : Nat) (hn : n ≤ 5) :
    ¬ (∀ xs : List (TableAlgebra q),
      (∀ x ∈ xs, InAugmentationKernel q x) → n ≤ xs.length → xs.prod = 0) := by
  intro h
  apply witnessWord_prod_ne_zero q hq
  exact h (witnessWord q) (witnessWord_in_kernel q) (by rw [witnessWord_length]; exact hn)

#print axioms witness_table
#print axioms singleton_basis_product
#print axioms t_mul_Z
#print axioms u_mul_V
#print axioms witnessWord_prod
#print axioms witnessWord_in_kernel
#print axioms witnessWord_prod_ne_zero
#print axioms exists_five_kernel_word_nonzero
#print axioms no_vanishing_threshold_at_most_five

end
end ARCTwentyDimNilpotenceSharp
