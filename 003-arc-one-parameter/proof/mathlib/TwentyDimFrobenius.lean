import TwentyDimAlgebra
import TraceInvariance
import Mathlib.LinearAlgebra.BilinearMap

/-!
# Perfect invariant trace pairing on the actual table algebra

The trace is packaged as a genuine linear map on `TableAlgebra q`, and
trace of multiplication as a genuine bilinear form. The established
coordinate formulas yield symmetry, invariance and nondegeneracy.
No Frobenius typeclass, Hochschild complex or ARC realization is asserted.
-/

namespace ARCTwentyDimFrobenius

open ARCTwentyDimAlgebra ARCTwentyDimAssociativity ARCTracePairSemantics ARCTraceInvariance
open scoped BigOperators

variable {R : Type*} [CommRing R] [CharP R 2]

noncomputable section

variable (q : R)

/-- The actual algebra trace as an R-linear functional. -/
def traceLinear : TableAlgebra q →ₗ[R] R where
  toFun x := specializedTrace x.coords
  map_add' x y := specialized_trace_add x.coords y.coords
  map_smul' r x := specialized_trace_smul r x.coords

@[simp] theorem traceLinear_apply (x : TableAlgebra q) :
    traceLinear q x = x.coords 10 + x.coords 18 := rfl

/-- Actual multiplication followed by the linear trace is an R-bilinear form. -/
def tracePairing : LinearMap.BilinForm R (TableAlgebra q) where
  toFun x :=
    { toFun y := traceLinear q (x * y)
      map_add' y z := by rw [mul_add, map_add]
      map_smul' r y := by rw [table_mul_smul, map_smul]; rfl }
  map_add' x y := by
    ext z
    change traceLinear q ((x + y) * z) = traceLinear q (x * z) + traceLinear q (y * z)
    rw [add_mul, map_add]
  map_smul' r x := by
    ext y
    change traceLinear q ((r • x) * y) = r • traceLinear q (x * y)
    rw [table_smul_mul, map_smul]

@[simp] theorem tracePairing_apply (x y : TableAlgebra q) :
    tracePairing q x y = traceLinear q (x * y) := rfl

/-- The exact anti-diagonal formula holds on the installed algebra object. -/
theorem tracePairing_formula (x y : TableAlgebra q) :
    tracePairing q x y = ∑ a : Fin 20, x.coords a * y.coords (dualBasis a) :=
  specialized_trace_mul q x.coords y.coords

theorem tracePairing_symmetric (x y : TableAlgebra q) :
    tracePairing q x y = tracePairing q y x :=
  specialized_trace_symmetric q x.coords y.coords

theorem tracePairing_invariant (x y z : TableAlgebra q) :
    tracePairing q (x * y) z = tracePairing q x (y * z) :=
  specialized_pairing_invariant q x.coords y.coords z.coords

theorem tracePairing_left_nondegenerate (x : TableAlgebra q)
    (h : ∀ y, tracePairing q x y = 0) : x = 0 := by
  apply ARCTwentyDimAlgebra.ext q
  exact specialized_trace_left_nondegenerate q x.coords (fun v => h ⟨v⟩)

theorem tracePairing_right_nondegenerate (y : TableAlgebra q)
    (h : ∀ x, tracePairing q x y = 0) : y = 0 := by
  apply ARCTwentyDimAlgebra.ext q
  exact specialized_trace_right_nondegenerate q y.coords (fun u => h ⟨u⟩)

theorem coords_coordinateBasis (a b : Fin 20) :
    (coordinateBasis q a).coords b = if a = b then 1 else 0 := by
  change (Pi.basisFun R (Fin 20) a) b = if a = b then 1 else 0
  simp [Pi.basisFun_apply, Pi.single_apply, eq_comm]

/-- Evaluating the pairing on a basis vector extracts the dual coordinate. -/
theorem tracePairing_basis_right (x : TableAlgebra q) (b : Fin 20) :
    tracePairing q x (coordinateBasis q b) = x.coords (dualBasis b) := by
  rw [tracePairing_formula, paired_sum_symmetric]
  simp [coords_coordinateBasis]

/-- Explicit inverse to the trace-pairing map into the R-linear dual. -/
def inverseTraceDual : (TableAlgebra q →ₗ[R] R) →ₗ[R] TableAlgebra q where
  toFun f := ⟨fun i => f (coordinateBasis q (dualBasis i))⟩
  map_add' f g := by
    apply ARCTwentyDimAlgebra.ext q
    rfl
  map_smul' r f := by
    apply ARCTwentyDimAlgebra.ext q
    rfl

theorem inverseTraceDual_left (x : TableAlgebra q) :
    inverseTraceDual q (tracePairing q x) = x := by
  apply ARCTwentyDimAlgebra.ext q
  funext a
  change tracePairing q x (coordinateBasis q (dualBasis a)) = x.coords a
  rw [tracePairing_basis_right, dualBasis_involutive]

theorem inverseTraceDual_right (f : TableAlgebra q →ₗ[R] R) :
    tracePairing q (inverseTraceDual q f) = f := by
  apply (coordinateBasis q).ext
  intro b
  rw [tracePairing_basis_right]
  change f (coordinateBasis q (dualBasis (dualBasis b))) = f (coordinateBasis q b)
  rw [dualBasis_involutive]

/-- The actual trace pairing is perfect over every commutative characteristic-two ring. -/
def traceDualEquiv : TableAlgebra q ≃ₗ[R] (TableAlgebra q →ₗ[R] R) where
  __ := tracePairing q
  invFun := inverseTraceDual q
  left_inv := inverseTraceDual_left q
  right_inv := inverseTraceDual_right q

theorem traceDualEquiv_apply (x y : TableAlgebra q) :
    traceDualEquiv q x y = traceLinear q (x * y) := rfl

#print axioms traceLinear
#print axioms tracePairing
#print axioms tracePairing_symmetric
#print axioms tracePairing_invariant
#print axioms tracePairing_left_nondegenerate
#print axioms tracePairing_right_nondegenerate
#print axioms traceDualEquiv
#print axioms traceDualEquiv_apply

end
end ARCTwentyDimFrobenius
