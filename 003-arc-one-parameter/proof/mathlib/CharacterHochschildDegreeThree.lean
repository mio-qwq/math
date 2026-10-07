import CharacterHochschildMaps
import LowDegreeCohomology

/-!
Degree-three cycles modulo full degree-two boundaries for the character
bimodule R.  The source is an actual associative R-algebra A and the
character is an actual R-algebra homomorphism A →ₐ[R] R.  Cochains are
all scalar-valued multilinear maps, with no restriction to selected
basis inputs or an augmentation kernel.  This is a cochain quotient;
no bar resolution or comparison with Ext is asserted.
-/

namespace ARCCharacterHochschildDegreeThree

open ARCCharacterHochschildMaps

variable {R A : Type*} [CommRing R] [Ring A] [Algebra R A] [CharP R 2]

noncomputable section

-- Use the standard additive groups one layer at a time to keep nested
-- instance synthesis from accumulating too many pending instances.
local instance scalarCochain1Group : AddCommGroup (A →ₗ[R] R) := LinearMap.addCommGroup
local instance scalarCochain2Group : AddCommGroup (C2S R A) := LinearMap.addCommGroup
local instance scalarCochain3Group : AddCommGroup (C3S R A) := LinearMap.addCommGroup
local instance scalarCochain4Group : AddCommGroup (C4S R A) := LinearMap.addCommGroup

/-- The full character-cochain quotient at degree three. -/
abbrev H3 (eps : A →ₐ[R] R) := ARCLowDegreeCohomology.Cohomology
  (d2 (R := R) (A := A) eps) (d3 (R := R) (A := A) eps)
  (d3_comp_d2 (R := R) (A := A) eps)

variable (eps : A →ₐ[R] R)

/-- The class of a scalar-valued trilinear cocycle. -/
def classOf (F : C3S R A) (hF : d3 (R := R) (A := A) eps F = 0) : H3 eps :=
  ARCLowDegreeCohomology.classOf (d2 (R := R) (A := A) eps)
    (d3 (R := R) (A := A) eps) (d3_comp_d2 (R := R) (A := A) eps) F hF

/-- Vanishing is equivalent to being the full coboundary of an arbitrary
scalar-valued bilinear cochain. -/
theorem classOf_eq_zero_iff (F : C3S R A)
    (hF : d3 (R := R) (A := A) eps F = 0) :
    classOf eps F hF = 0 ↔ ∃ G : C2S R A, d2 (R := R) (A := A) eps G = F :=
  ARCLowDegreeCohomology.classOf_eq_zero_iff (d2 (R := R) (A := A) eps)
    (d3 (R := R) (A := A) eps) (d3_comp_d2 (R := R) (A := A) eps) F hF

/-- A full cocycle excluded from every full bilinear boundary defines
a nonzero class in this quotient. -/
theorem classOf_ne_zero (F : C3S R A)
    (hF : d3 (R := R) (A := A) eps F = 0)
    (hnot : ¬ ∃ G : C2S R A, d2 (R := R) (A := A) eps G = F) :
    classOf eps F hF ≠ 0 :=
  ARCLowDegreeCohomology.classOf_ne_zero (d2 (R := R) (A := A) eps)
    (d3 (R := R) (A := A) eps) (d3_comp_d2 (R := R) (A := A) eps) F hF hnot

#print axioms classOf
#print axioms classOf_eq_zero_iff
#print axioms classOf_ne_zero

end
end ARCCharacterHochschildDegreeThree
