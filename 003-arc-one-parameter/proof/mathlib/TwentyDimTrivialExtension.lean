import TwentyDimDualScaleEndomorphism
import TwentyDimFrobenius

/-!
# The actual square-zero ideal is the dual of the actual lower algebra

The perfect trace constructs an explicit R-linear equivalence from the upper
kernel to the dual of the lower image. Both multiplication actions are retained
with their correct noncommutative order. An explicit R-linear splitting of the
whole algebra and its full multiplication formula are also proved.

This is an actual split dual square-zero description over every commutative
characteristic-two ring. No derived triangle, complete Ext profile, or ARC
realization is asserted.
-/

namespace ARCTwentyDimTrivialExtension

open ARCFiniteCore ARCTracePairSemantics
open ARCTwentyDimAlgebra ARCTwentyDimFrobenius
open ARCTwentyDimDualScaleEndomorphism
open scoped BigOperators

noncomputable section
variable {R : Type*} [CommRing R] [CharP R 2]

/-- The actual projection, now with its image as codomain. -/
def lowerProjection (q : R) : TableAlgebra q →ₐ[R] lowerSubalgebra q :=
  (rho q 0).rangeRestrict

@[simp] theorem lowerProjection_val (q : R) (a : TableAlgebra q) :
    (lowerProjection q a : TableAlgebra q) = rho q 0 a := rfl

theorem rho_lower_fixed (q : R) (c : lowerSubalgebra q) :
    rho q 0 (c : TableAlgebra q) = c := by
  obtain ⟨a, ha⟩ := c.property
  rw [← ha]
  exact rho_zero_idempotent q a

@[simp] theorem lowerProjection_fixed (q : R) (c : lowerSubalgebra q) :
    lowerProjection q (c : TableAlgebra q) = c := by
  apply Subtype.ext
  exact rho_lower_fixed q c

private theorem dualBasis_lower_iff (i : Fin 20) :
    (dualBasis i).val < 10 ↔ ¬ i.val < 10 := by
  change dualIndex i.val < 10 ↔ ¬ i.val < 10
  dsimp [dualIndex]
  split_ifs <;> omega

private theorem rho_basis_upper (q : R) (i : Fin 20) (hi : ¬ i.val < 10) :
    rho q 0 (coordinateBasis q i) = 0 := by
  apply ARCTwentyDimAlgebra.ext q
  funext j
  by_cases hij : i = j
  · subst j
    simp [coords_rho, coords_coordinateBasis, hi]
  · simp [coords_rho, coords_coordinateBasis, hij]

/-- Lower elements pair to zero under the actual trace. -/
theorem trace_lower_lower (q : R) (c d : lowerSubalgebra q) :
    tracePairing q (c : TableAlgebra q) (d : TableAlgebra q) = 0 := by
  rw [tracePairing_formula]
  apply Finset.sum_eq_zero
  intro i hi
  have hc := (mem_lowerSubalgebra q c).mp c.property
  have hd := (mem_lowerSubalgebra q d).mp d.property
  by_cases hlow : i.val < 10
  · have hdual : ¬ (dualBasis i).val < 10 := by
      rw [dualBasis_lower_iff]
      exact not_not.mpr hlow
    rw [hd (dualBasis i) hdual, mul_zero]
  · rw [hc i hlow, zero_mul]

/-- Trace against lower inputs, on the whole actual algebra. -/
def lowerTrace (q : R) :
    TableAlgebra q →ₗ[R] (lowerSubalgebra q →ₗ[R] R) where
  toFun a := (tracePairing q a).comp (lowerSubalgebra q).val.toLinearMap
  map_add' a b := by
    ext c
    change tracePairing q (a + b) (c : TableAlgebra q) = _
    rw [map_add]
    rfl
  map_smul' r a := by
    ext c
    change tracePairing q (r • a) (c : TableAlgebra q) = _
    rw [map_smul]
    rfl

@[simp] theorem lowerTrace_apply (q : R) (a : TableAlgebra q)
    (c : lowerSubalgebra q) : lowerTrace q a c = tracePairing q a c := rfl

private def extendFunctional (q : R) :
    (lowerSubalgebra q →ₗ[R] R) →ₗ[R] (TableAlgebra q →ₗ[R] R) where
  toFun f := f.comp (lowerProjection q).toLinearMap
  map_add' _ _ := rfl
  map_smul' _ _ := rfl

/-- An explicit inverse candidate, using the already proved perfect trace. -/
def dualInverse (q : R) :
    (lowerSubalgebra q →ₗ[R] R) →ₗ[R] TableAlgebra q :=
  (traceDualEquiv q).symm.toLinearMap.comp (extendFunctional q)

theorem dualInverse_pairing (q : R) (f : lowerSubalgebra q →ₗ[R] R)
    (a : TableAlgebra q) :
    tracePairing q (dualInverse q f) a = f (lowerProjection q a) := by
  exact congrArg (fun g : TableAlgebra q →ₗ[R] R => g a)
    ((traceDualEquiv q).apply_symm_apply (extendFunctional q f))

/-- The inverse lies in the actual upper kernel, not merely a matching dimension. -/
theorem dualInverse_mem_upper (q : R) (f : lowerSubalgebra q →ₗ[R] R) :
    dualInverse q f ∈ upperSubmodule q := by
  change dualInverse q f ∈ (upperIdeal q).restrictScalars R
  apply (mem_upperIdeal q (dualInverse q f)).mpr
  intro i hi
  change f (lowerProjection q (coordinateBasis q (dualBasis i))) = 0
  have hdual : ¬ (dualBasis i).val < 10 := by
    rw [dualBasis_lower_iff]
    exact not_not.mpr hi
  have hz : lowerProjection q (coordinateBasis q (dualBasis i)) = 0 := by
    apply Subtype.ext
    exact rho_basis_upper q (dualBasis i) hdual
  rw [hz, map_zero]

theorem upperPart_mem (q : R) (a : TableAlgebra q) :
    a - rho q 0 a ∈ upperIdeal q := by
  change rho q 0 (a - rho q 0 a) = 0
  rw [map_sub, rho_zero_idempotent, sub_self]

/-- An upper element pairs only with the lower projection of its second input. -/
theorem upper_pairing_projection (q : R) (x : upperSubmodule q)
    (a : TableAlgebra q) :
    tracePairing q (x : TableAlgebra q) (rho q 0 a) =
      tracePairing q (x : TableAlgebra q) a := by
  have hx : (x : TableAlgebra q) ∈ upperIdeal q := x.property
  have hz := upperIdeal_mul_eq_zero q x (a - rho q 0 a) hx (upperPart_mem q a)
  have ht := congrArg (traceLinear q) hz
  rw [map_zero] at ht
  change tracePairing q (x : TableAlgebra q) (a - rho q 0 a) = 0 at ht
  rw [map_sub] at ht
  exact (sub_eq_zero.mp ht).symm

theorem dualInverse_left (q : R) (x : upperSubmodule q) :
    dualInverse q (lowerTrace q x) = (x : TableAlgebra q) := by
  apply (traceDualEquiv q).injective
  ext a
  change tracePairing q (dualInverse q (lowerTrace q x)) a = tracePairing q x a
  rw [dualInverse_pairing, lowerTrace_apply, lowerProjection_val]
  exact upper_pairing_projection q x a

theorem dualInverse_right (q : R) (f : lowerSubalgebra q →ₗ[R] R) :
    lowerTrace q (dualInverse q f) = f := by
  ext c
  rw [lowerTrace_apply, dualInverse_pairing, lowerProjection_fixed]

/-- A genuine linear identification of the square-zero ideal with the lower dual. -/
def upperDualEquiv (q : R) :
    upperSubmodule q ≃ₗ[R] (lowerSubalgebra q →ₗ[R] R) where
  toFun x := lowerTrace q x
  map_add' x y := (lowerTrace q).map_add x y
  map_smul' r x := (lowerTrace q).map_smul r x
  invFun f := ⟨dualInverse q f, dualInverse_mem_upper q f⟩
  left_inv x := Subtype.ext (dualInverse_left q x)
  right_inv f := dualInverse_right q f

/-- Actual left multiplication by a lower element on the upper kernel. -/
def upperLeft (q : R) (c : lowerSubalgebra q) : upperSubmodule q →ₗ[R] upperSubmodule q where
  toFun x := ⟨(c : TableAlgebra q) * x, by
    change rho q 0 ((c : TableAlgebra q) * x) = 0
    rw [map_mul]
    have hx : rho q 0 (x : TableAlgebra q) = 0 := x.property
    rw [hx, mul_zero]⟩
  map_add' x y := by
    apply Subtype.ext
    exact mul_add (c : TableAlgebra q) x y
  map_smul' r x := by
    apply Subtype.ext
    exact table_mul_smul q r c x

/-- Actual right multiplication, retaining the noncommutative side. -/
def upperRight (q : R) (c : lowerSubalgebra q) : upperSubmodule q →ₗ[R] upperSubmodule q where
  toFun x := ⟨(x : TableAlgebra q) * c, by
    change rho q 0 ((x : TableAlgebra q) * c) = 0
    rw [map_mul]
    have hx : rho q 0 (x : TableAlgebra q) = 0 := x.property
    rw [hx, zero_mul]⟩
  map_add' x y := by
    apply Subtype.ext
    exact add_mul (x : TableAlgebra q) y c
  map_smul' r x := by
    apply Subtype.ext
    exact table_smul_mul q r x c

theorem upperDualEquiv_left (q : R) (c b : lowerSubalgebra q)
    (x : upperSubmodule q) :
    upperDualEquiv q (upperLeft q c x) b = upperDualEquiv q x (b * c) := by
  change tracePairing q ((c : TableAlgebra q) * x) (b : TableAlgebra q) =
    tracePairing q x ((b : TableAlgebra q) * c)
  calc
    _ = tracePairing q (b : TableAlgebra q) ((c : TableAlgebra q) * x) :=
      tracePairing_symmetric q _ _
    _ = tracePairing q ((b : TableAlgebra q) * c) x :=
      (tracePairing_invariant q _ _ _).symm
    _ = _ := tracePairing_symmetric q _ _

theorem upperDualEquiv_right (q : R) (c b : lowerSubalgebra q)
    (x : upperSubmodule q) :
    upperDualEquiv q (upperRight q c x) b = upperDualEquiv q x (c * b) :=
  tracePairing_invariant q x c b

/-- The trace retains both lower multiplication actions with their actual order. -/
theorem lowerTrace_bimodule (q : R) (c d b : lowerSubalgebra q)
    (x : TableAlgebra q) :
    lowerTrace q ((c : TableAlgebra q) * x * d) b =
      lowerTrace q x (d * b * c) := by
  change tracePairing q ((c : TableAlgebra q) * x * (d : TableAlgebra q))
      (b : TableAlgebra q) =
    tracePairing q x (((d : TableAlgebra q) * b) * c)
  calc
    _ = tracePairing q ((c : TableAlgebra q) * x)
        ((d : TableAlgebra q) * b) := tracePairing_invariant q _ _ _
    _ = tracePairing q ((d : TableAlgebra q) * b)
        ((c : TableAlgebra q) * x) := tracePairing_symmetric q _ _
    _ = tracePairing q (((d : TableAlgebra q) * b) * c) x :=
      (tracePairing_invariant q _ _ _).symm
    _ = _ := tracePairing_symmetric q _ _

/-- The actual algebra splits explicitly into a lower element and a dual functional. -/
def splitDualLinearEquiv (q : R) :
    TableAlgebra q ≃ₗ[R]
      (lowerSubalgebra q × (lowerSubalgebra q →ₗ[R] R)) where
  toFun a := ⟨lowerProjection q a, lowerTrace q a⟩
  map_add' a b := by simp only [map_add, Prod.mk_add_mk]
  map_smul' r a := by simp only [map_smul, RingHom.id_apply, Prod.smul_mk]
  invFun p := (p.1 : TableAlgebra q) + dualInverse q p.2
  left_inv a := by
    let x : upperSubmodule q := ⟨a - rho q 0 a, upperPart_mem q a⟩
    have htrace : lowerTrace q x = lowerTrace q a := by
      ext c
      change tracePairing q (a - rho q 0 a) (c : TableAlgebra q) = _
      rw [map_sub, LinearMap.sub_apply]
      have hz := trace_lower_lower q (lowerProjection q a) c
      change tracePairing q (rho q 0 a) (c : TableAlgebra q) = 0 at hz
      rw [hz, sub_zero]
      rfl
    change rho q 0 a + dualInverse q (lowerTrace q a) = a
    rw [← htrace, dualInverse_left]
    dsimp [x]
    abel
  right_inv p := by
    apply Prod.ext
    · apply Subtype.ext
      change rho q 0 ((p.1 : TableAlgebra q) + dualInverse q p.2) = p.1
      rw [map_add, rho_lower_fixed]
      have hu := dualInverse_mem_upper q p.2
      change rho q 0 (dualInverse q p.2) = 0 at hu
      rw [hu, add_zero]
    · change lowerTrace q ((p.1 : TableAlgebra q) + dualInverse q p.2) = p.2
      rw [map_add, dualInverse_right]
      have hz : lowerTrace q (p.1 : TableAlgebra q) = 0 := by
        ext c
        exact trace_lower_lower q p.1 c
      rw [hz, zero_add]

@[simp] theorem splitDualLinearEquiv_apply (q : R) (a : TableAlgebra q) :
    splitDualLinearEquiv q a = (lowerProjection q a, lowerTrace q a) := rfl

/-- The actual algebra unit is the lower unit with zero dual component. -/
theorem splitDualLinearEquiv_one (q : R) :
    splitDualLinearEquiv q 1 = (1, 0) := by
  rw [splitDualLinearEquiv_apply, map_one]
  congr 1
  ext c
  change tracePairing q (1 : TableAlgebra q) (c : TableAlgebra q) = 0
  exact trace_lower_lower q 1 c

/-- Complete multiplication on arbitrary split elements, evaluated on any lower input.
The two dual actions have opposite precomposition orders because C is noncommutative. -/
theorem split_dual_mul (q : R) (c d t : lowerSubalgebra q)
    (x y : upperSubmodule q) :
    lowerTrace q (((c : TableAlgebra q) + x) * ((d : TableAlgebra q) + y)) t =
      lowerTrace q y (t * c) + lowerTrace q x (d * t) := by
  have hxy : (x : TableAlgebra q) * (y : TableAlgebra q) = 0 :=
    upperIdeal_mul_eq_zero q x y x.property y.property
  change tracePairing q (((c : TableAlgebra q) + x) * ((d : TableAlgebra q) + y))
    (t : TableAlgebra q) = _
  rw [add_mul, mul_add, mul_add, hxy, add_zero]
  simp only [map_add, LinearMap.add_apply]
  have hcd := trace_lower_lower q (c * d) t
  change tracePairing q ((c : TableAlgebra q) * (d : TableAlgebra q))
    (t : TableAlgebra q) = 0 at hcd
  rw [hcd, zero_add]
  have hcy : tracePairing q ((c : TableAlgebra q) * y) (t : TableAlgebra q) =
      lowerTrace q y (t * c) := by
    calc
      _ = tracePairing q (t : TableAlgebra q) ((c : TableAlgebra q) * y) :=
        tracePairing_symmetric q _ _
      _ = tracePairing q ((t : TableAlgebra q) * c) y :=
        (tracePairing_invariant q _ _ _).symm
      _ = _ := tracePairing_symmetric q _ _
  rw [hcy, tracePairing_invariant q (x : TableAlgebra q) d t]
  rfl

/-- The lower component of full split multiplication is the actual product in C. -/
theorem split_lower_mul (q : R) (c d : lowerSubalgebra q)
    (x y : upperSubmodule q) :
    lowerProjection q (((c : TableAlgebra q) + x) * ((d : TableAlgebra q) + y)) =
      c * d := by
  have hx : lowerProjection q (x : TableAlgebra q) = 0 := Subtype.ext x.property
  have hy : lowerProjection q (y : TableAlgebra q) = 0 := Subtype.ext y.property
  rw [map_mul, map_add, map_add, lowerProjection_fixed, lowerProjection_fixed,
    hx, hy, add_zero, add_zero]

/-- Whole algebra multiplication in the explicit C × dual(C) coordinates. -/
theorem splitDualLinearEquiv_mul (q : R) (a b : TableAlgebra q)
    (t : lowerSubalgebra q) :
    (splitDualLinearEquiv q (a * b)).1 =
        (splitDualLinearEquiv q a).1 * (splitDualLinearEquiv q b).1 ∧
    (splitDualLinearEquiv q (a * b)).2 t =
      (splitDualLinearEquiv q b).2 (t * (splitDualLinearEquiv q a).1) +
      (splitDualLinearEquiv q a).2 ((splitDualLinearEquiv q b).1 * t) := by
  simp only [splitDualLinearEquiv_apply]
  constructor
  · exact (lowerProjection q).map_mul a b
  · let pa := splitDualLinearEquiv q a
    let pb := splitDualLinearEquiv q b
    let x : upperSubmodule q := ⟨dualInverse q pa.2, dualInverse_mem_upper q pa.2⟩
    let y : upperSubmodule q := ⟨dualInverse q pb.2, dualInverse_mem_upper q pb.2⟩
    have ha : (pa.1 : TableAlgebra q) + x = a :=
      (splitDualLinearEquiv q).symm_apply_apply a
    have hb : (pb.1 : TableAlgebra q) + y = b :=
      (splitDualLinearEquiv q).symm_apply_apply b
    have h := split_dual_mul q pa.1 pb.1 t x y
    rw [ha, hb] at h
    have hx : lowerTrace q (x : TableAlgebra q) = pa.2 := dualInverse_right q pa.2
    have hy : lowerTrace q (y : TableAlgebra q) = pb.2 := dualInverse_right q pb.2
    simpa only [hx, hy, pa, pb, splitDualLinearEquiv_apply] using h

#print axioms lowerProjection
#print axioms rho_lower_fixed
#print axioms trace_lower_lower
#print axioms lowerTrace
#print axioms dualInverse
#print axioms dualInverse_pairing
#print axioms dualInverse_mem_upper
#print axioms upperPart_mem
#print axioms upper_pairing_projection
#print axioms dualInverse_left
#print axioms dualInverse_right
#print axioms upperDualEquiv
#print axioms upperLeft
#print axioms upperRight
#print axioms upperDualEquiv_left
#print axioms upperDualEquiv_right
#print axioms lowerTrace_bimodule
#print axioms splitDualLinearEquiv
#print axioms splitDualLinearEquiv_one
#print axioms split_dual_mul
#print axioms split_lower_mul
#print axioms splitDualLinearEquiv_mul

end
end ARCTwentyDimTrivialExtension
