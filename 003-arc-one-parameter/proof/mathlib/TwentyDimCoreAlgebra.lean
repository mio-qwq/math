import TwentyDimDualCorrespondence
import FiniteStructureAlgebra
import DualTrivialExtension
import TwentyDimUnit

/-!
# The actual ten-coordinate core and its genuine dual extension

The core constants inherit associativity from the existing polynomial
basis theorem and units from the concrete twenty-coordinate unit theorem.
The generic verified construction then supplies the actual core algebra,
its coordinate basis and the genuine dual-action extension. This does not
yet construct the comparison isomorphism to the twenty-coordinate table.
-/

namespace ARCTwentyDimCoreAlgebra

open ARCFiniteCore ARCTermSemantics ARCTableBasisSemantics
open ARCFiniteTableContraction ARCTwentyDimDualCorrespondence
open ARCFiniteBilinear ARCTwentyDimAssociativity ARCTwentyDimUnit
open scoped BigOperators

noncomputable section

@[simp] theorem lowerIndex_eq_iff (a b : Fin 10) : lowerIndex a = lowerIndex b ↔ a = b := by
  constructor
  · intro h
    apply Fin.ext
    exact congrArg (fun i : Fin 20 => i.val) h
  · intro h
    subst b
    rfl

/-- The frozen core basis theorem yields every actual core contraction identity. -/
theorem core_structure_associative : StructureAssociative coreConstants := by
  intro a b c k
  have hab : ∀ term ∈ cTerms a.val b.val, term.1 < 10 := by
    simpa only [List.all_eq_true, decide_eq_true_eq] using c_output_basis_bound a b
  have hbc : ∀ term ∈ cTerms b.val c.val, term.1 < 10 := by
    simpa only [List.all_eq_true, decide_eq_true_eq] using c_output_basis_bound b c
  have h := congrArg (fun v : PolyVector => v k.val) (c_basis_polynomial_associativity a b c)
  rw [leftVectorProduct_finite 10 cTerms a.val b.val c.val hab,
    rightVectorProduct_finite 10 cTerms a.val b.val c.val hbc] at h
  exact h

def polynomialCoreUnit : Fin 10 → Polynomial (ZMod 2) :=
  fun i => (if i = 0 then 1 else 0) + (if i = 8 then 1 else 0)

theorem core_left_basis_unit (b k : Fin 10) :
    coreConstants 0 b k + coreConstants 8 b k = if b = k then 1 else 0 := by
  have h := polynomial_left_basis_unit (lowerIndex b) (lowerIndex k)
  change tConstants (lowerIndex (0 : Fin 10)) (lowerIndex b) (lowerIndex k) +
      tConstants (lowerIndex (8 : Fin 10)) (lowerIndex b) (lowerIndex k) =
    if lowerIndex b = lowerIndex k then 1 else 0 at h
  simpa only [lower_lower_lower, lowerIndex_eq_iff] using h

theorem core_right_basis_unit (a k : Fin 10) :
    coreConstants a 0 k + coreConstants a 8 k = if a = k then 1 else 0 := by
  have h := polynomial_right_basis_unit (lowerIndex a) (lowerIndex k)
  change tConstants (lowerIndex a) (lowerIndex (0 : Fin 10)) (lowerIndex k) +
      tConstants (lowerIndex a) (lowerIndex (8 : Fin 10)) (lowerIndex k) =
    if lowerIndex a = lowerIndex k then 1 else 0 at h
  simpa only [lower_lower_lower, lowerIndex_eq_iff] using h

theorem core_structure_left_unit : StructureLeftUnit coreConstants polynomialCoreUnit := by
  intro b k
  simp_rw [polynomialCoreUnit, add_mul, ite_mul, one_mul, zero_mul]
  rw [Finset.sum_add_distrib]
  simpa using core_left_basis_unit b k

theorem core_structure_right_unit : StructureRightUnit coreConstants polynomialCoreUnit := by
  intro a k
  simp_rw [polynomialCoreUnit, add_mul, ite_mul, one_mul, zero_mul]
  rw [Finset.sum_add_distrib]
  simpa using core_right_basis_unit a k

variable {R : Type*} [CommRing R] [CharP R 2]

def coreUnit (q : R) : Fin 10 → R := fun i => specialize q (polynomialCoreUnit i)

theorem specialized_core_associative (q : R) :
    StructureAssociative (specializedCoreConstants q) := by
  intro a b c k
  have h := congrArg (specialize q) (core_structure_associative a b c k)
  simpa only [map_sum, map_mul, specializedCoreConstants] using h

theorem specialized_core_left_unit (q : R) :
    StructureLeftUnit (specializedCoreConstants q) (coreUnit q) := by
  intro b k
  have h := congrArg (specialize q) (core_structure_left_unit b k)
  simpa only [map_sum, map_mul, apply_ite, map_one, map_zero,
    specializedCoreConstants, coreUnit] using h

theorem specialized_core_right_unit (q : R) :
    StructureRightUnit (specializedCoreConstants q) (coreUnit q) := by
  intro a k
  have h := congrArg (specialize q) (core_structure_right_unit a k)
  simpa only [map_sum, map_mul, apply_ite, map_one, map_zero,
    specializedCoreConstants, coreUnit] using h

/-- The actual ten-coordinate constants satisfy all generic algebra obligations. -/
def coreLaws (q : R) : ARCFiniteStructure.Laws (specializedCoreConstants q) where
  unit := coreUnit q
  assoc := specialized_core_associative q
  left_unit := specialized_core_left_unit q
  right_unit := specialized_core_right_unit q

abbrev CoreAlgebra (q : R) := ARCFiniteStructure.Carrier (coreLaws q)

def coreBasis (q : R) : Module.Basis (Fin 10) R (CoreAlgebra q) :=
  ARCFiniteStructure.carrierBasis (coreLaws q)

theorem core_basis_mul (q : R) (a b : Fin 10) :
    coreBasis q a * coreBasis q b = specializedCoreConstants q a b :=
  ARCFiniteStructure.carrier_basis_mul (coreLaws q) a b

theorem core_mul (q : R) (a b : CoreAlgebra q) :
    a * b = ARCFiniteBilinear.mul (specializedCoreConstants q) a b := by
  exact (ARCFiniteStructure.carrier_mul (coreLaws q) a b).trans
    (ARCFiniteStructure.product_eq_mul (specializedCoreConstants q) a b)

theorem core_finrank [StrongRankCondition R] (q : R) :
    Module.finrank R (CoreAlgebra q) = 10 := by
  simpa using ARCFiniteStructure.carrier_finrank (coreLaws q)

/-- A genuine dual-action algebra, ready as the comparison target. -/
abbrev CoreDualExtension (q : R) := ARCDualTrivialExtension.Carrier R (CoreAlgebra q)

theorem core_extension_finrank [StrongRankCondition R] (q : R) :
    Module.finrank R (CoreDualExtension q) = 20 := by
  simpa using ARCDualTrivialExtension.carrier_finrank (coreBasis q)

theorem core_extension_trace_nondegenerate (q : R) (x : CoreDualExtension q)
    (hx : ∀ y : CoreDualExtension q, ARCDualTrivialExtension.tracePairing x y = 0) : x = 0 :=
  ARCDualTrivialExtension.tracePairing_nondegenerate x hx

#print axioms core_structure_associative
#print axioms core_structure_left_unit
#print axioms core_structure_right_unit
#print axioms coreLaws
#print axioms core_basis_mul
#print axioms core_mul
#print axioms core_finrank
#print axioms core_extension_finrank
#print axioms core_extension_trace_nondegenerate

end
end ARCTwentyDimCoreAlgebra
