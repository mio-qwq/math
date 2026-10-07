import CharacterModule
import Mathlib.Algebra.Field.Basic
import Mathlib.RingTheory.SimpleModule.Basic

/-!
The actual character module is simple over A when the coefficient ring
R is a field.  Every nonzero vector has full A-orbit: a scalar element
algebraMap R A (y/x) sends it to any prescribed vector.  This proves the
standard IsSimpleModule predicate, not merely a name for the carrier.
There is no projective-resolution or Ext assertion.
-/

namespace ARCCharacterModuleSimple

open ARCCharacterModule

variable {R A : Type*} [Field R] [Ring A] [Algebra R A]
variable (eps : A →ₐ[R] R)

/-- Scalar elements of A carry any nonzero vector to every target vector. -/
theorem character_orbit_surjective (x : CharacterModule eps) (hx : x ≠ 0) :
    Function.Surjective (fun a : A => a • x) := by
  have hxv : x.val ≠ 0 := by
    intro hz
    apply hx
    apply CharacterModule.ext
    exact hz
  intro y
  refine ⟨algebraMap R A (y.val / x.val), ?_⟩
  apply CharacterModule.ext
  rw [val_character_smul, eps.commutes]
  change (y.val / x.val) * x.val = y.val
  exact div_mul_cancel₀ y.val hxv

/-- The character action gives a genuine simple A-module over a field. -/
theorem character_isSimpleModule : IsSimpleModule A (CharacterModule eps) := by
  apply (isSimpleModule_iff_toSpanSingleton_surjective
    (R := A) (M := CharacterModule eps)).mpr
  refine ⟨inferInstance, ?_⟩
  intro x hx
  exact character_orbit_surjective eps x hx

instance characterSimpleModule : IsSimpleModule A (CharacterModule eps) :=
  character_isSimpleModule eps

#print axioms character_orbit_surjective
#print axioms character_isSimpleModule
#print axioms characterSimpleModule

end ARCCharacterModuleSimple
