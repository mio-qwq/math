import HochschildCochainMaps
import LowDegreeCohomology

/-!
The degree-three Hochschild cochain quotient in characteristic two,
using actual multilinear cochains and the full displayed differentials.
This constructs the degree-three cycles-modulo-boundaries module, not
an all-degree resolution or an identification with an Ext construction.
-/

namespace ARCHochschildDegreeThree

open ARCHochschildCochainMaps

variable (R A : Type*) [CommRing R] [Ring A] [Algebra R A] [CharP A 2]

noncomputable section

-- Supply the standard additive group instances one layer at a time so
-- nested typeclass synthesis does not defer too many pending instances.
local instance cochain1Group : AddCommGroup (A →ₗ[R] A) := LinearMap.addCommGroup
local instance cochain2Group : AddCommGroup (C2 R A) := LinearMap.addCommGroup
local instance cochain3Group : AddCommGroup (C3 R A) := LinearMap.addCommGroup
local instance cochain4Group : AddCommGroup (C4 R A) := LinearMap.addCommGroup

/-- Degree-three cycles modulo degree-two boundaries for the actual
Hochschild cochain formulas. All signs are positive in characteristic two. -/
abbrev H3 := ARCLowDegreeCohomology.Cohomology
  (d2 (R := R) (A := A)) (d3 (R := R) (A := A))
  (d3_comp_d2 (R := R) (A := A))

variable {R A}

/-- The class of a trilinear cochain whose full differential is zero. -/
def classOf (F : C3 R A) (hF : d3 F = 0) : H3 R A :=
  ARCLowDegreeCohomology.classOf (d2 (R := R) (A := A))
    (d3 (R := R) (A := A)) (d3_comp_d2 (R := R) (A := A)) F hF

/-- Vanishing is equivalent to being the full coboundary of a bilinear map. -/
theorem classOf_eq_zero_iff (F : C3 R A) (hF : d3 F = 0) :
    classOf F hF = 0 ↔ ∃ G : C2 R A, d2 G = F :=
  ARCLowDegreeCohomology.classOf_eq_zero_iff (d2 (R := R) (A := A))
    (d3 (R := R) (A := A)) (d3_comp_d2 (R := R) (A := A)) F hF

theorem classOf_ne_zero (F : C3 R A) (hF : d3 F = 0)
    (hnot : ¬ ∃ G : C2 R A, d2 G = F) : classOf F hF ≠ 0 :=
  ARCLowDegreeCohomology.classOf_ne_zero (d2 (R := R) (A := A))
    (d3 (R := R) (A := A)) (d3_comp_d2 (R := R) (A := A)) F hF hnot

#print axioms classOf
#print axioms classOf_eq_zero_iff
#print axioms classOf_ne_zero

end
end ARCHochschildDegreeThree
