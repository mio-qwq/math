import TwentyDimAugmentation
import TwentyDimCochainAlgebra
import CochainIdempotentClosure
import Mathlib.Algebra.Algebra.Hom

/-!
# Actual algebra characters and the scalar projection of the cochain

The existing e/f coordinate ring homomorphisms are packaged as R-algebra
homomorphisms. Composing the actual trilinear cochain with the f character
gives a genuinely scalar-valued trilinear map. Its full five-face character
formula vanishes on all algebra inputs and its fixed cycle pairing is q³.

No simple-module, Ext, resolution, or cohomology quotient is constructed
here. The results hold over every commutative characteristic-two ring;
nonzero pairing requires q³ ≠ 0, not merely q ≠ 0 in a ring with zero divisors.
-/

namespace ARCTwentyDimCharacters

open ARCTwentyDimAlgebra ARCTwentyDimUnit ARCTwentyDimAugmentation
open ARCTwentyDimCochainAlgebra ARCCochainSpecialization
open ARCTwentyDimCochain ARCCochainCycleSemantics

variable {R : Type*} [CommRing R] [CharP R 2]

noncomputable section

/-- The e coordinate is an actual R-algebra character. -/
def eCharacter (q : R) : TableAlgebra q →ₐ[R] R where
  __ := eAugmentation q
  commutes' r := by
    change (algebraMap R (TableAlgebra q) r).coords 0 = algebraMap R R r
    simp [coords_algebraMap, specialized_unit_coordinates]

/-- The f coordinate is an independent actual R-algebra character. -/
def fCharacter (q : R) : TableAlgebra q →ₐ[R] R where
  __ := fAugmentation q
  commutes' r := by
    change (algebraMap R (TableAlgebra q) r).coords 8 = algebraMap R R r
    simp [coords_algebraMap, specialized_unit_coordinates]

@[simp] theorem eCharacter_apply (q : R) (x : TableAlgebra q) :
    eCharacter q x = x.coords 0 := rfl

@[simp] theorem fCharacter_apply (q : R) (x : TableAlgebra q) :
    fCharacter q x = x.coords 8 := rfl

/-- Scalar compatibility is the installed table algebra's scalar action. -/
theorem eCharacter_smul (q r : R) (x : TableAlgebra q) :
    eCharacter q (r • x) = r • eCharacter q x :=
  (eCharacter q).toLinearMap.map_smul r x

theorem fCharacter_smul (q r : R) (x : TableAlgebra q) :
    fCharacter q (r • x) = r • fCharacter q x :=
  (fCharacter q).toLinearMap.map_smul r x

@[simp] theorem eCharacter_basis (q : R) (a : Fin 20) :
    eCharacter q (coordinateBasis q a) = if a = 0 then 1 else 0 := by
  rw [eCharacter_apply, coordinateBasis_coords]
  simp [ARCFiniteTrilinear.basis, eq_comm]

@[simp] theorem fCharacter_basis (q : R) (a : Fin 20) :
    fCharacter q (coordinateBasis q a) = if a = 8 then 1 else 0 := by
  rw [fCharacter_apply, coordinateBasis_coords]
  simp [ARCFiniteTrilinear.basis, eq_comm]

/-- The characters distinguish the two orthogonal idempotent basis elements. -/
theorem characters_on_idempotents (q : R) :
    eCharacter q (coordinateBasis q 0) = 1 ∧
    eCharacter q (coordinateBasis q 8) = 0 ∧
    fCharacter q (coordinateBasis q 0) = 0 ∧
    fCharacter q (coordinateBasis q 8) = 1 := by
  rw [eCharacter_basis, eCharacter_basis, fCharacter_basis, fCharacter_basis]
  simp

/-- Projection by the actual f character of the actual algebra cochain.
This is a scalar-valued trilinear map; the name does not install a simple module. -/
def actualfSimpleP (q : R) : TableAlgebra q →ₗ[R] TableAlgebra q →ₗ[R]
    TableAlgebra q →ₗ[R] R where
  toFun x :=
    { toFun y := (fCharacter q).toLinearMap.comp (algebraCochain q x y)
      map_add' y y' := by
        ext z
        change fCharacter q (algebraCochain q x (y + y') z) =
          fCharacter q (algebraCochain q x y z) + fCharacter q (algebraCochain q x y' z)
        simp only [map_add, LinearMap.add_apply]
      map_smul' r y := by
        ext z
        change fCharacter q (algebraCochain q x (r • y) z) =
          r • fCharacter q (algebraCochain q x y z)
        simp only [map_smul, LinearMap.smul_apply] }
  map_add' x x' := by
    ext y z
    change fCharacter q (algebraCochain q (x + x') y z) =
      fCharacter q (algebraCochain q x y z) + fCharacter q (algebraCochain q x' y z)
    simp only [map_add, LinearMap.add_apply]
  map_smul' r x := by
    ext y z
    change fCharacter q (algebraCochain q (r • x) y z) =
      r • fCharacter q (algebraCochain q x y z)
    simp only [map_smul, LinearMap.smul_apply]

@[simp] theorem actualfSimpleP_apply (q : R) (x y z : TableAlgebra q) :
    actualfSimpleP q x y z = (algebraCochain q x y z).coords 8 := rfl

/-- Its basis values are exactly the original specialized f coefficients. -/
theorem actualfSimpleP_basis (q : R) (a b c : Fin 20) :
    actualfSimpleP q (coordinateBasis q a) (coordinateBasis q b)
      (coordinateBasis q c) = specializedCochainConstants q a b c 8 := by
  rw [actualfSimpleP_apply, algebraCochain_basis]

omit [CharP R 2] in
/-- Ring-homomorphic projection sends all five actual algebra faces to
the full scalar formula for the corresponding character bimodule. -/
theorem character_projection_differential3
    {A : Type*} [Ring A] [Algebra R A] (eps : A →ₐ[R] R)
    (F : A → A → A → A) (x y z w : A) :
    eps (ARCHochschildLowDegrees.differential3 F x y z w) =
      eps x * eps (F y z w) + eps (F (x * y) z w) + eps (F x (y * z) w) +
        eps (F x y (z * w)) + eps (F x y z) * eps w := by
  simp only [ARCHochschildLowDegrees.differential3, map_add, map_mul]

/-- Full-input closure for the scalar projection with its actual character
actions. This includes both outer faces and is not only an internal formula. -/
theorem actualfSimpleP_character_closed (q : R) (x y z w : TableAlgebra q) :
    fCharacter q x * actualfSimpleP q y z w +
      actualfSimpleP q (x * y) z w + actualfSimpleP q x (y * z) w +
      actualfSimpleP q x y (z * w) + actualfSimpleP q x y z * fCharacter q w = 0 := by
  have hactual : ARCHochschildLowDegrees.differential3
      (fun a b c => algebraCochain q a b c) x y z w = 0 := by
    apply ARCTwentyDimAlgebra.ext q
    rw [algebra_differential3_coords]
    exact ARCCochainIdempotentClosure.specialized_all_vector_closure
      q x.coords y.coords z.coords w.coords
  have h := congrArg (fCharacter q) hactual
  rw [character_projection_differential3, map_zero] at h
  exact h

/-- The two actual basis triples pair to q³ after every specialization. -/
theorem actualfSimpleP_cycle_pairing (q : R) :
    q ^ 2 * actualfSimpleP q (coordinateBasis q 6) (coordinateBasis q 1)
        (coordinateBasis q 17) +
      actualfSimpleP q (coordinateBasis q 6) (coordinateBasis q 2)
        (coordinateBasis q 17) = q ^ 3 := by
  rw [actualfSimpleP_basis, actualfSimpleP_basis]
  exact specialized_cycle_pairing q

/-- A nonzero cube makes the scalar cochain itself nonzero. This does not
yet construct its cohomology class or compare a bar resolution with Ext. -/
theorem actualfSimpleP_ne_zero (q : R) (hq : q ^ 3 ≠ 0) :
    actualfSimpleP q ≠ 0 := by
  intro hP
  have h := actualfSimpleP_cycle_pairing q
  rw [hP] at h
  simp only [LinearMap.zero_apply, mul_zero, add_zero] at h
  exact hq h.symm

#print axioms eCharacter
#print axioms fCharacter
#print axioms characters_on_idempotents
#print axioms actualfSimpleP
#print axioms character_projection_differential3
#print axioms actualfSimpleP_character_closed
#print axioms actualfSimpleP_cycle_pairing
#print axioms actualfSimpleP_ne_zero

end
end ARCTwentyDimCharacters
