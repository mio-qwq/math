import LowerAlgebraResolution
import TwentyDimCharacters
import CharacterModule
import Mathlib.Algebra.Category.ModuleCat.Projective

/-!
# Actual projective corners of the lower algebra

The specified left corners are split summands of the actual regular
lower-algebra module. Their projectivity is over that noncommutative
algebra, not inferred from their bases over the coefficient ring.
The actual lower f-character module and its corner augmentation are
retained, together with vanishing of every e-corner map into that module.
No categorical resolution or derived Ext identification is asserted here.
-/

namespace ARCLowerAlgebraProjective

open ARCTwentyDimAlgebra ARCTwentyDimDualScaleEndomorphism
open ARCTwentyDimFrobenius
open ARCTwentyDimCharacters ARCCharacterModule ARCLowerAlgebraResolution
open CategoryTheory

universe u
noncomputable section
variable {R : Type u} [CommRing R] [CharP R 2]

/-- The actual retraction onto the left e-corner. -/
def projectE (q : R) : C q →ₗ[C q] Ce q where
  toFun a := ⟨a * e q, by change (a * e q) * e q = _; rw [mul_assoc, e_mul_e]⟩
  map_add' a b := by apply Subtype.ext; exact add_mul a b (e q)
  map_smul' c a := by apply Subtype.ext; exact mul_assoc c a (e q)

/-- The actual retraction onto the left f-corner. -/
def projectF (q : R) : C q →ₗ[C q] Cf q where
  toFun a := ⟨a * f q, by change (a * f q) * f q = _; rw [mul_assoc, f_mul_f]⟩
  map_add' a b := by apply Subtype.ext; exact add_mul a b (f q)
  map_smul' c a := by apply Subtype.ext; exact mul_assoc c a (f q)

theorem projectE_retract (q : R) :
    (projectE q).comp (Ce q).subtype = LinearMap.id := by
  apply LinearMap.ext
  intro a
  apply Subtype.ext
  exact a.property

theorem projectF_retract (q : R) :
    (projectF q).comp (Cf q).subtype = LinearMap.id := by
  apply LinearMap.ext
  intro a
  apply Subtype.ext
  exact a.property

/-- Projectivity over the lower algebra follows from a specified split summand. -/
theorem ce_module_projective (q : R) : Module.Projective (C q) (Ce q) :=
  Module.Projective.of_split (Ce q).subtype (projectE q) (projectE_retract q)

theorem cf_module_projective (q : R) : Module.Projective (C q) (Cf q) :=
  Module.Projective.of_split (Cf q).subtype (projectF q) (projectF_retract q)

theorem ce_category_projective (q : R) :
    Projective (ModuleCat.of (C q) (Ce q)) := by
  let := ce_module_projective q
  infer_instance

theorem cf_category_projective (q : R) :
    Projective (ModuleCat.of (C q) (Cf q)) := by
  let := cf_module_projective q
  infer_instance

/-- The restriction of the installed f-character along the actual subalgebra. -/
def lowerCharacter (q : R) : C q →ₐ[R] R :=
  (fCharacter q).comp (lowerSubalgebra q).val

abbrev Simple (q : R) := CharacterModule (lowerCharacter q)

/-- The augmentation of the actual f-corner retains its installed C-action. -/
def augmentation (q : R) : Cf q →ₗ[C q] Simple q where
  toFun a := ⟨lowerCharacter q (a : C q)⟩
  map_add' a b := by apply CharacterModule.ext; exact map_add (lowerCharacter q) _ _
  map_smul' c a := by
    apply CharacterModule.ext
    change lowerCharacter q (c * (a : C q)) =
      lowerCharacter q c * lowerCharacter q (a : C q)
    exact map_mul (lowerCharacter q) c (a : C q)

@[simp] theorem augmentation_val (q : R) (a : Cf q) :
    (augmentation q a).val = (((a : C q) : TableAlgebra q)).coords 8 := rfl

theorem augmentation_surjective (q : R) : Function.Surjective (augmentation q) := by
  intro s
  refine ⟨s.val • cfVector q 0, ?_⟩
  apply CharacterModule.ext
  rw [augmentation_val]
  simp [cfVector, cfLabel, cBasis, coords_smul, coords_coordinateBasis]

theorem e_simple_zero (q : R) (s : Simple q) : e q • s = 0 := by
  apply CharacterModule.ext
  change lowerCharacter q (e q) * s.val = 0
  simp [lowerCharacter, e, cBasis, coords_coordinateBasis]

/-- The e-corner is generated over C by the actual idempotent e. -/
def eGenerator (q : R) : Ce q := ⟨e q, e_mul_e q⟩

theorem ce_generator_smul (q : R) (a : Ce q) :
    (a : C q) • eGenerator q = a := by
  apply Subtype.ext
  exact a.property

theorem e_generator_fixed (q : R) : e q • eGenerator q = eGenerator q := by
  apply Subtype.ext
  exact e_mul_e q

/-- Every C-linear map from the actual e-corner to the f-character is zero. -/
theorem hom_ce_simple_zero (q : R) (h : Ce q →ₗ[C q] Simple q) : h = 0 := by
  have hz : h (eGenerator q) = 0 := by
    calc
      h (eGenerator q) = h (e q • eGenerator q) := by rw [e_generator_fixed]
      _ = e q • h (eGenerator q) := h.map_smul _ _
      _ = 0 := e_simple_zero q _
  apply LinearMap.ext
  intro a
  calc
    h a = h ((a : C q) • eGenerator q) := by rw [ce_generator_smul]
    _ = (a : C q) • h (eGenerator q) := h.map_smul _ _
    _ = 0 := by rw [hz, smul_zero]

#print axioms projectE
#print axioms projectF
#print axioms projectE_retract
#print axioms projectF_retract
#print axioms ce_module_projective
#print axioms cf_module_projective
#print axioms ce_category_projective
#print axioms cf_category_projective
#print axioms lowerCharacter
#print axioms augmentation
#print axioms augmentation_surjective
#print axioms e_simple_zero
#print axioms eGenerator
#print axioms ce_generator_smul
#print axioms e_generator_fixed
#print axioms hom_ce_simple_zero

end
end ARCLowerAlgebraProjective
