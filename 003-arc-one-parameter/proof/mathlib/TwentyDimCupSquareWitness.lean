import FiniteFreeBarCupLift
import FiniteFreeBarWordLift
import FiniteFreeBarExtThree
import TwentyDimFCharacterSparse
import ScalarEvaluation

/-!
A six-letter evaluation of the actual closed cup Hom is q^4, and kills
every preceding A-linear character Hom boundary. It gives a genuine
nonzero Ext^6 class on the specified resolution when q^4 is nonzero.
The lifted word's resolution boundary retains its first A coefficient.
Identification of this Ext class with the Yoneda square is separate.
-/

namespace ARCTwentyDimCupSquareWitness

open CategoryTheory CategoryTheory.Category
open ARCFiniteCore ARCBitPolynomial ARCTermSemantics ARCFiniteTableContraction
open ARCTwentyDimAssociativity ARCTwentyDimAlgebra ARCTwentyDimFrobenius
open ARCTwentyDimCochainAlgebra ARCTwentyDimCharacters ARCTwentyDimFCharacterSparse
open ARCCharacterModule ARCFiniteFreeBarModules ARCFiniteFreeBarCochains
open ARCFiniteFreeBarInsertion ARCFiniteFreeBarRecursive ARCFiniteFreeBarWordLift
open ARCFiniteFreeBarCupLift ARCFiniteFreeBarProjectiveResolution

private theorem witness_table :
    tTerms 6 1 = [(7, 1)] ∧ tTerms 6 2 = [(7, 4)] ∧
    tTerms 1 17 = [(16, 1)] ∧ tTerms 2 17 = [(16, 4)] ∧
    tTerms 17 15 = [] ∧ tTerms 15 1 = [(14, 1)] ∧
    tTerms 15 2 = [(14, 1)] ∧ tTerms 1 4 = [(5, 1)] ∧
    tTerms 2 4 = [(5, 1)] := by decide

noncomputable section
universe u
variable {R : Type u} [CommRing R] [CharP R 2]

private theorem specialize_one (q : R) : specialize q (decode 1) = 1 := by
  exact ARCScalarEvaluation.evaluate_one q

private theorem specialize_four (q : R) : specialize q (decode 4) = q ^ 2 := by
  change ARCScalarEvaluation.evaluate q 4 = q ^ 2
  rw [show (4 : Nat) = 2 * 2 by rfl, ARCScalarEvaluation.evaluate_double,
    ARCScalarEvaluation.evaluate_two, pow_two]

private theorem singleton_product (q : R) (a b j : Fin 20) (c : Nat)
    (h : tTerms a.val b.val = [(j.val, c)]) :
    coordinateBasis q a * coordinateBasis q b =
      specialize q (decode c) • coordinateBasis q j := by
  apply ARCTwentyDimAlgebra.ext q
  funext k
  rw [coordinateBasis_mul_coords, coords_smul]
  simp [specializedConstants, tConstants, h, sumTerms, singleTerm,
    coords_coordinateBasis, Fin.val_inj, eq_comm]
  split_ifs <;> simp_all

private theorem empty_product (q : R) (a b : Fin 20)
    (h : tTerms a.val b.val = []) :
    coordinateBasis q a * coordinateBasis q b = 0 := by
  apply ARCTwentyDimAlgebra.ext q
  funext k
  rw [coordinateBasis_mul_coords]
  simp [specializedConstants, tConstants, h, sumTerms]

private theorem add_self_table (q : R) (x : TableAlgebra q) : x + x = 0 := by
  apply ARCTwentyDimAlgebra.ext q
  funext i
  change x.coords i + x.coords i = 0
  have htwo : (2 : R) = 0 := by exact_mod_cast (CharP.cast_eq_zero R 2)
  rw [← two_mul, htwo, zero_mul]

/-- The two linear combinations and the four basis letters retain the
actual installed noncommutative multiplication. -/
def cupWitnessLetters (q : R) : Fin 6 → TableAlgebra q :=
  ![coordinateBasis q 6, coordinateBasis q 2 + q ^ 2 • coordinateBasis q 1,
    coordinateBasis q 17, coordinateBasis q 15,
    coordinateBasis q 1 + coordinateBasis q 2, coordinateBasis q 4]

/-- All five adjacent products vanish in the actual table algebra. -/
theorem cupWitnessLetters_products (q : R) :
    ∀ i : Fin 5, cupWitnessLetters q i.castSucc * cupWitnessLetters q i.succ = 0 := by
  have h61 := singleton_product q 6 1 7 1 witness_table.1
  have h62 := singleton_product q 6 2 7 4 witness_table.2.1
  have h117 := singleton_product q 1 17 16 1 witness_table.2.2.1
  have h217 := singleton_product q 2 17 16 4 witness_table.2.2.2.1
  have h1715 := empty_product q 17 15 witness_table.2.2.2.2.1
  have h151 := singleton_product q 15 1 14 1 witness_table.2.2.2.2.2.1
  have h152 := singleton_product q 15 2 14 1 witness_table.2.2.2.2.2.2.1
  have h14 := singleton_product q 1 4 5 1 witness_table.2.2.2.2.2.2.2.1
  have h24 := singleton_product q 2 4 5 1 witness_table.2.2.2.2.2.2.2.2
  simp only [specialize_one, specialize_four, one_smul] at h61 h62 h117 h217 h151 h152 h14 h24
  intro i
  fin_cases i
  · change coordinateBasis q 6 * (coordinateBasis q 2 + q ^ 2 • coordinateBasis q 1) = 0
    rw [mul_add, table_mul_smul, h62, h61, add_self_table]
  · change (coordinateBasis q 2 + q ^ 2 • coordinateBasis q 1) * coordinateBasis q 17 = 0
    rw [add_mul, table_smul_mul, h217, h117, add_self_table]
  · exact h1715
  · change coordinateBasis q 15 * (coordinateBasis q 1 + coordinateBasis q 2) = 0
    rw [mul_add, h151, h152, add_self_table]
  · change (coordinateBasis q 1 + coordinateBasis q 2) * coordinateBasis q 4 = 0
    rw [add_mul, h14, h24, add_self_table]

/-- Both character endpoint values vanish. -/
theorem cupWitnessLetters_endpoints (q : R) :
    fCharacter q (cupWitnessLetters q 0) = 0 ∧
      fCharacter q (cupWitnessLetters q (Fin.last 5)) = 0 := by
  change fCharacter q (coordinateBasis q 6) = 0 ∧ fCharacter q (coordinateBasis q 4) = 0
  simp only [fCharacter_basis, show (6 : Fin 20) ≠ 8 by decide,
    show (4 : Fin 20) ≠ 8 by decide, ite_false, and_self, eq_self]

private theorem wordLift_basis_six (q : R) (a b c d e f : Fin 20) :
    wordLift q 6 ![coordinateBasis q a, coordinateBasis q b, coordinateBasis q c,
      coordinateBasis q d, coordinateBasis q e, coordinateBasis q f] =
      wordBasis q 6 ![a, b, c, d, e, f] := by
  have heq : ![coordinateBasis q a, coordinateBasis q b, coordinateBasis q c,
      coordinateBasis q d, coordinateBasis q e, coordinateBasis q f] =
      (fun i : Fin 6 => coordinateBasis q (![a, b, c, d, e, f] i)) := by
    funext i
    fin_cases i <;> rfl
  rw [heq]
  exact wordLift_coordinateBasis q 6 _

/-- Only four actual basis words occur; no six-word enumeration is used. -/
theorem cupWitness_wordLift_expansion (q : R) :
    wordLift q 6 (cupWitnessLetters q) =
      q ^ 2 • wordBasis q 6 ![6, 1, 17, 15, 1, 4] +
      q ^ 2 • wordBasis q 6 ![6, 1, 17, 15, 2, 4] +
      wordBasis q 6 ![6, 2, 17, 15, 1, 4] +
      wordBasis q 6 ![6, 2, 17, 15, 2, 4] := by
  have h : wordLift q 6 (cupWitnessLetters q) =
      q ^ 2 • wordLift q 6 ![coordinateBasis q 6, coordinateBasis q 1,
        coordinateBasis q 17, coordinateBasis q 15, coordinateBasis q 1, coordinateBasis q 4] +
      q ^ 2 • wordLift q 6 ![coordinateBasis q 6, coordinateBasis q 1,
        coordinateBasis q 17, coordinateBasis q 15, coordinateBasis q 2, coordinateBasis q 4] +
      wordLift q 6 ![coordinateBasis q 6, coordinateBasis q 2,
        coordinateBasis q 17, coordinateBasis q 15, coordinateBasis q 1, coordinateBasis q 4] +
      wordLift q 6 ![coordinateBasis q 6, coordinateBasis q 2,
        coordinateBasis q 17, coordinateBasis q 15, coordinateBasis q 2, coordinateBasis q 4] := by
    simp only [cupWitnessLetters, Matrix.vecCons, wordLift_cons, wordLift_zero, add_smul,
      smul_add, smul_assoc, map_add, map_smul, smul_algebra_smul_comm]
    abel
  simpa only [wordLift_basis_six] using h

/-- The actual closed module Hom detects q^4 on the full six-letter lift. -/
theorem cupSixHom_witness_pairing (q : R) :
    (cupSixHom q (wordLift q 6 (cupWitnessLetters q))).val = q ^ 4 := by
  rw [cupWitness_wordLift_expansion]
  simp only [map_add, (cupSixHom q).map_smul_of_tower, val_add, val_coefficient_smul,
    cupSixHom_basis]
  simp only [Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.cons_val_two,
    Matrix.cons_val_three]
  simp only [actualfSimpleP_sparse, coords_coordinateBasis]
  norm_num
  ring

/-- Every actual A-linear map from P5 kills the boundary of the witness. -/
theorem cupWitness_boundary_evaluation_zero (q : R)
    (phi : BarTerm q 5 →ₗ[TableAlgebra q] CharacterModule (fCharacter q)) :
    phi (recursiveBoundary q (fCharacter q) 5
      (wordLift q 6 (cupWitnessLetters q))) = 0 :=
  hom_recursiveBoundary_wordLift_eq_zero q (fCharacter q) 5 _
    (cupWitnessLetters_products q) (cupWitnessLetters_endpoints q).1
    (cupWitnessLetters_endpoints q).2 phi

/-- The closed actual cup Hom is not any full preceding-Hom boundary. -/
theorem cupSixHom_not_boundary (q : R) (hq : q ^ 4 ≠ 0) :
    ¬ ∃ phi : BarTerm q 5 →ₗ[TableAlgebra q] CharacterModule (fCharacter q),
      phi.comp (recursiveBoundary q (fCharacter q) 5) = cupSixHom q := by
  rintro ⟨phi, h⟩
  have hp := cupSixHom_witness_pairing q
  rw [← h, LinearMap.comp_apply, cupWitness_boundary_evaluation_zero, val_zero] at hp
  exact hq hp.symm

def cupSixCocycle (q : R) : (projectiveResolution q (fCharacter q)).complex.X 6 ⟶
    characterObject q (fCharacter q) := ModuleCat.ofHom (cupSixHom q)

theorem cupSixCocycle_closed (q : R) :
    (projectiveResolution q (fCharacter q)).complex.d 7 6 ≫ cupSixCocycle q = 0 := by
  rw [projectiveResolution_d q (fCharacter q) 6]
  exact ModuleCat.hom_ext (cupSixHom_closed q)

/-- Actual Ext^6 of the specified resolution; square identification is separate. -/
def fCupExtSix (q : R) : CategoryTheory.Abelian.Ext
    (characterObject q (fCharacter q)) (characterObject q (fCharacter q)) 6 :=
  (projectiveResolution q (fCharacter q)).extMk (cupSixCocycle q) 7 rfl
    (cupSixCocycle_closed q)

theorem fCupExtSix_ne_zero (q : R) (hq : q ^ 4 ≠ 0) : fCupExtSix q ≠ 0 := by
  intro hzero
  obtain ⟨g, hg⟩ := ((projectiveResolution q (fCharacter q)).extMk_eq_zero_iff
    (cupSixCocycle q) 7 rfl (cupSixCocycle_closed q) 5 rfl).mp hzero
  apply cupSixHom_not_boundary q hq
  refine ⟨g.hom, ?_⟩
  rw [projectiveResolution_d q (fCharacter q) 5] at hg
  exact congrArg (fun h => h.hom) hg

theorem fCupExtSix_ne_zero_of_nonzero [NoZeroDivisors R] (q : R) (hq : q ≠ 0) :
    fCupExtSix q ≠ 0 := fCupExtSix_ne_zero q (pow_ne_zero 4 hq)

#print axioms cupWitnessLetters_products
#print axioms cupWitnessLetters_endpoints
#print axioms cupWitness_wordLift_expansion
#print axioms cupSixHom_witness_pairing
#print axioms cupWitness_boundary_evaluation_zero
#print axioms cupSixHom_not_boundary
#print axioms cupSixCocycle_closed
#print axioms fCupExtSix
#print axioms fCupExtSix_ne_zero
#print axioms fCupExtSix_ne_zero_of_nonzero

end
end ARCTwentyDimCupSquareWitness
