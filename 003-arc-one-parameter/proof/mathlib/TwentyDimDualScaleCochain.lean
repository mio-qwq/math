import TwentyDimDualScale
import TwentyDimFCharacterSparse
import TwentyDimCharacterClass

/-!
The fixed actual scalar f-character cochain is an eigenvector of
simultaneous input pullback along the actual dual-scaling automorphism.
The identity holds on all actual algebra inputs over any commutative
characteristic-two ring, including zero parameters and zero divisors.

The inverse automorphism has eigenvalue the inverse unit. This statement
is about the actual trilinear cochain and its closed/nonboundary status.
It is not an assertion about the action of a module-category functor on
Ext, the whole Ext group, or the complete ARC realization.
-/

namespace ARCTwentyDimDualScaleCochain

open ARCTwentyDimAlgebra ARCTwentyDimCharacters ARCTwentyDimCharacterClass
open ARCTwentyDimDualScale ARCTwentyDimFCharacterSparse
open ARCCharacterHochschildMaps

variable {R : Type*} [CommRing R] [CharP R 2]

noncomputable section

/-- Input pullback of an arbitrary genuine scalar trilinear cochain. -/
def pullbackThree (q : R) (e : TableAlgebra q ≃ₐ[R] TableAlgebra q)
    (F : C3S R (TableAlgebra q)) : C3S R (TableAlgebra q) where
  toFun x :=
    { toFun y := (F (e x) (e y)).comp e.toLinearMap
      map_add' y y' := by
        ext z
        change F (e x) (e (y + y')) (e z) =
          F (e x) (e y) (e z) + F (e x) (e y') (e z)
        simp
      map_smul' r y := by
        ext z
        change F (e x) (e (r • y)) (e z) = r • F (e x) (e y) (e z)
        simp }
  map_add' x x' := by
    ext y z
    change F (e (x + x')) (e y) (e z) =
      F (e x) (e y) (e z) + F (e x') (e y) (e z)
    simp
  map_smul' r x := by
    ext y z
    change F (e (r • x)) (e y) (e z) = r • F (e x) (e y) (e z)
    simp

@[simp] theorem pullbackThree_apply (q : R)
    (e : TableAlgebra q ≃ₐ[R] TableAlgebra q) (F : C3S R (TableAlgebra q))
    (x y z : TableAlgebra q) : pullbackThree q e F x y z = F (e x) (e y) (e z) := rfl

/-- The five surviving terms each contain exactly one dual coordinate. -/
theorem actualfSimpleP_pullback (q : R) (H : Rˣ) (x y z : TableAlgebra q) :
    actualfSimpleP q (dualScale q H x) (dualScale q H y) (dualScale q H z) =
      (H : R) * actualfSimpleP q x y z := by
  rw [actualfSimpleP_sparse, actualfSimpleP_sparse]
  simp [coords_dualScale_apply]
  ring

/-- Equality of whole genuine scalar trilinear maps. -/
theorem pullbackThree_fixed (q : R) (H : Rˣ) :
    pullbackThree q (dualScale q H) (actualfSimpleP q) = (H : R) • actualfSimpleP q := by
  ext x y z
  exact actualfSimpleP_pullback q H x y z

/-- The inverse-input convention has the inverse-unit eigenvalue. -/
theorem actualfSimpleP_pullback_inverse (q : R) (H : Rˣ) (x y z : TableAlgebra q) :
    actualfSimpleP q ((dualScale q H).symm x) ((dualScale q H).symm y)
      ((dualScale q H).symm z) = (↑(H⁻¹) : R) * actualfSimpleP q x y z := by
  rw [dualScale_symm]
  exact actualfSimpleP_pullback q H⁻¹ x y z

theorem pullbackThree_fixed_inverse (q : R) (H : Rˣ) :
    pullbackThree q (dualScale q H).symm (actualfSimpleP q) =
      (↑(H⁻¹) : R) • actualfSimpleP q := by
  rw [dualScale_symm]
  exact pullbackThree_fixed q H⁻¹

/-- The pulled-back representative is still closed for the full character differential. -/
theorem pullback_fixed_closed (q : R) (H : Rˣ) :
    d3 (fCharacter q) (pullbackThree q (dualScale q H) (actualfSimpleP q)) = 0 := by
  rw [pullbackThree_fixed, map_smul, actualfSimpleP_d3_zero, smul_zero]

/-- Unit scaling preserves exclusion of every full scalar bilinear boundary. -/
theorem pullback_fixed_not_boundary (q : R) (H : Rˣ) (hq : q ^ 3 ≠ 0) :
    ¬ ∃ G : C2S R (TableAlgebra q),
      d2 (fCharacter q) G = pullbackThree q (dualScale q H) (actualfSimpleP q) := by
  rintro ⟨G, hG⟩
  apply actualfSimpleP_not_character_boundary q hq
  refine ⟨(↑(H⁻¹) : R) • G, ?_⟩
  rw [map_smul, hG, pullbackThree_fixed, smul_smul]
  simp

#print axioms pullbackThree
#print axioms actualfSimpleP_pullback
#print axioms pullbackThree_fixed
#print axioms actualfSimpleP_pullback_inverse
#print axioms pullbackThree_fixed_inverse
#print axioms pullback_fixed_closed
#print axioms pullback_fixed_not_boundary

end
end ARCTwentyDimDualScaleCochain
