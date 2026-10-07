import TwentyDimAlgebra
import HochschildLowDegrees

/-!
Characteristic two of the installed table ring, proved via its actual
injective scalar algebra map. The cast-equals-zero equivalence is proved
for every natural number, not merely the equation 2=0.
The actual low-degree differential composition then vanishes on all
algebra quadruples, for arbitrary functions and for genuine bilinear maps.
No full Hochschild complex or Ext realization is installed here.
-/

namespace ARCTwentyDimCharacteristic

open ARCTwentyDimAlgebra ARCTwentyDimUnit

variable {R : Type*} [CommRing R] [CharP R 2]

noncomputable section

/-- Coordinate e reflects the scalar map, so that map is injective even
without a field or domain assumption. -/
theorem table_algebraMap_injective (q : R) :
    Function.Injective (algebraMap R (TableAlgebra q)) := by
  intro r s h
  have hv := congrArg (fun x : TableAlgebra q => x.coords 0) h
  simpa [coords_algebraMap, specialized_unit_coordinates] using hv

/-- The actual table ring has characteristic exactly two. -/
instance tableCharP (q : R) : CharP (TableAlgebra q) 2 where
  cast_eq_zero_iff n := by
    constructor
    · intro hn
      have hmap : algebraMap R (TableAlgebra q) (n : R) =
          algebraMap R (TableAlgebra q) 0 := by
        simpa only [map_natCast, map_zero] using hn
      exact (CharP.cast_eq_zero_iff R 2 n).mp (table_algebraMap_injective q hmap)
    · intro hn
      have hR : (n : R) = 0 := (CharP.cast_eq_zero_iff R 2 n).mpr hn
      rw [← map_natCast (algebraMap R (TableAlgebra q)), hR, map_zero]

/-- The full actual-algebra degree-three differential kills every degree-two
boundary, even when the input function has no linearity assumption. -/
theorem actual_differential3_differential2 (q : R)
    (G : TableAlgebra q → TableAlgebra q → TableAlgebra q)
    (x y z w : TableAlgebra q) :
    ARCHochschildLowDegrees.differential3 (ARCHochschildLowDegrees.differential2 G)
      x y z w = 0 :=
  ARCHochschildLowDegrees.differential3_differential2 G x y z w

/-- Actual bilinear coboundaries are closed on every algebra quadruple. -/
theorem actual_bilinear_coboundary_closed (q : R)
    (G : TableAlgebra q →ₗ[R] TableAlgebra q →ₗ[R] TableAlgebra q)
    (x y z w : TableAlgebra q) :
    ARCHochschildLowDegrees.differential3
      (fun a b c => ARCHochschildLowDegrees.differential2Linear G a b c)
      x y z w = 0 :=
  ARCHochschildLowDegrees.bilinear_coboundary_closed G x y z w

#print axioms table_algebraMap_injective
#print axioms tableCharP
#print axioms actual_differential3_differential2
#print axioms actual_bilinear_coboundary_closed

end
end ARCTwentyDimCharacteristic
