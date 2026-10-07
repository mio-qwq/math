import Mathlib.LinearAlgebra.Quotient.Defs
import Mathlib.Algebra.Module.Submodule.Range
import Mathlib.Algebra.Module.Submodule.Ker

/-!
The cycles modulo boundaries quotient for two composable linear maps.
The zero-composite hypothesis puts every boundary in the cycle module.
This generic module construction makes no claim about a particular complex.
-/

namespace ARCLowDegreeCohomology

variable {R M₂ M₃ M₄ : Type*} [CommRing R]
variable [AddCommGroup M₂] [Module R M₂]
variable [AddCommGroup M₃] [Module R M₃]
variable [AddCommGroup M₄] [Module R M₄]

noncomputable section

variable (d₂ : M₂ →ₗ[R] M₃) (d₃ : M₃ →ₗ[R] M₄) (h : d₃.comp d₂ = 0)

/-- A zero composite puts each boundary in the actual kernel. -/
def boundaryToCycles : M₂ →ₗ[R] LinearMap.ker d₃ :=
  d₂.codRestrict (LinearMap.ker d₃) (fun x => by
    change d₃ (d₂ x) = 0
    exact LinearMap.congr_fun h x)

/-- The image of the preceding differential, inside the cycle module. -/
def boundaries : Submodule R (LinearMap.ker d₃) :=
  LinearMap.range (boundaryToCycles d₂ d₃ h)

/-- The actual module quotient of cycles by boundaries. -/
abbrev Cohomology := (LinearMap.ker d₃) ⧸ boundaries d₂ d₃ h

/-- The cohomology class of a specified cycle. -/
def classOf (z : M₃) (hz : d₃ z = 0) : Cohomology d₂ d₃ h :=
  Submodule.Quotient.mk (⟨z, hz⟩ : LinearMap.ker d₃)

/-- A class vanishes exactly when its representative is an actual boundary. -/
theorem classOf_eq_zero_iff (z : M₃) (hz : d₃ z = 0) :
    classOf d₂ d₃ h z hz = 0 ↔ ∃ x : M₂, d₂ x = z := by
  change (Submodule.Quotient.mk (⟨z, hz⟩ : LinearMap.ker d₃) :
    (LinearMap.ker d₃) ⧸ boundaries d₂ d₃ h) = 0 ↔ _
  rw [Submodule.Quotient.mk_eq_zero]
  change (∃ x, boundaryToCycles d₂ d₃ h x = ⟨z, hz⟩) ↔ _
  constructor
  · rintro ⟨x, hx⟩
    exact ⟨x, congrArg Subtype.val hx⟩
  · rintro ⟨x, hx⟩
    refine ⟨x, ?_⟩
    apply Subtype.ext
    exact hx

theorem classOf_ne_zero (z : M₃) (hz : d₃ z = 0)
    (hnot : ¬ ∃ x : M₂, d₂ x = z) : classOf d₂ d₃ h z hz ≠ 0 :=
  fun heq => hnot ((classOf_eq_zero_iff d₂ d₃ h z hz).mp heq)

#print axioms boundaryToCycles
#print axioms classOf_eq_zero_iff
#print axioms classOf_ne_zero

end
end ARCLowDegreeCohomology
