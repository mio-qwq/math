import CochainIdempotentClosure
import TwentyDimCochainAlgebra
import TwentyDimCharacteristic
import HochschildDegreeThree

/-!
The attributed cochain is closed on every input of the actual twenty-dimensional
algebra. Its class in the full degree-three Hochschild cochain quotient is
nonzero whenever q^3 is nonzero. No comparison with Ext or all-degree ARC
realization is asserted here.
-/

namespace ARCTwentyDimHochschildClass

open ARCTwentyDimAlgebra ARCTwentyDimCochainAlgebra
open ARCHochschildCochainMaps

variable {R : Type*} [CommRing R] [CharP R 2]

noncomputable section

variable (q : R)

/-- The actual five-face formula vanishes on every algebra quadruple. -/
theorem algebraCochain_closed (x y z w : TableAlgebra q) :
    ARCHochschildLowDegrees.differential3 (fun a b c => algebraCochain q a b c)
      x y z w = 0 := by
  apply ARCTwentyDimAlgebra.ext q
  rw [algebra_differential3_coords]
  exact ARCCochainIdempotentClosure.specialized_all_vector_closure
    q x.coords y.coords z.coords w.coords

/-- Closure as an equality in the full module of four-linear cochains. -/
theorem algebraCochain_d3_zero : d3 (algebraCochain q) = 0 := by
  apply LinearMap.ext
  intro x
  apply LinearMap.ext
  intro y
  apply LinearMap.ext
  intro z
  apply LinearMap.ext
  intro w
  change ARCHochschildLowDegrees.differential3
    (fun a b c => algebraCochain q a b c) x y z w = 0
  exact algebraCochain_closed q x y z w

-- Use the same standard nested additive-group instances as the quotient.
local instance cochain1Group : AddCommGroup (TableAlgebra q →ₗ[R] TableAlgebra q) :=
  LinearMap.addCommGroup
local instance cochain2Group : AddCommGroup (C2 R (TableAlgebra q)) :=
  LinearMap.addCommGroup
local instance cochain3Group : AddCommGroup (C3 R (TableAlgebra q)) :=
  LinearMap.addCommGroup
local instance cochain4Group : AddCommGroup (C4 R (TableAlgebra q)) :=
  LinearMap.addCommGroup

/-- The class of the fixed cochain in degree-three cycles modulo boundaries. -/
def cochainClass : ARCHochschildDegreeThree.H3 R (TableAlgebra q) :=
  ARCHochschildDegreeThree.classOf (algebraCochain q) (algebraCochain_d3_zero q)

/-- The separating q^3 witness excludes every actual bilinear boundary. -/
theorem cochainClass_ne_zero (hq : q ^ 3 ≠ 0) : cochainClass q ≠ 0 := by
  apply ARCHochschildDegreeThree.classOf_ne_zero (algebraCochain q)
    (algebraCochain_d3_zero q)
  change ¬ ∃ G : C2 R (TableAlgebra q),
    ARCHochschildLowDegrees.differential2Linear G = algebraCochain q
  exact algebraCochain_not_coboundary q hq

theorem cochainClass_ne_zero_of_nonzero [NoZeroDivisors R] (hq : q ≠ 0) :
    cochainClass q ≠ 0 :=
  cochainClass_ne_zero q (pow_ne_zero 3 hq)

/-- The actual degree-three cochain quotient is nontrivial under the witness
condition, not merely a space containing a formally named cochain. -/
theorem h3_nontrivial (hq : q ^ 3 ≠ 0) :
    Nontrivial (ARCHochschildDegreeThree.H3 R (TableAlgebra q)) :=
  ⟨⟨cochainClass q, 0, cochainClass_ne_zero q hq⟩⟩

theorem h3_nontrivial_of_nonzero [NoZeroDivisors R] (hq : q ≠ 0) :
    Nontrivial (ARCHochschildDegreeThree.H3 R (TableAlgebra q)) :=
  h3_nontrivial q (pow_ne_zero 3 hq)

#print axioms algebraCochain_closed
#print axioms algebraCochain_d3_zero
#print axioms cochainClass
#print axioms cochainClass_ne_zero
#print axioms cochainClass_ne_zero_of_nonzero
#print axioms h3_nontrivial
#print axioms h3_nontrivial_of_nonzero

end
end ARCTwentyDimHochschildClass
