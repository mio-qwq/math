import Mathlib.Basic.Complex.Basic
import Mathlib.Data.Fin.Basic
import Mathlib.Data.Fin.Rev
import Mathlib.Data.Fintype.Fin
import Mathlib.Data.Matrix.Mul
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-!
Scope: fixed-spectrum matrix anticommutation and matching support only.

For the fixed simple spectrum -5,-3,-1,1,3,5, the actual matrix
anticommutation equation with its diagonal matrix is equivalent to
support on the opposite-eigenvalue matching i <-> Fin.rev i.

The matrix multiplication in the premise is the usual finite matrix
product. No entrywise support condition is assumed in the forward
direction. The finite case proof below verifies only the fixed spectral
coefficients; it is not a hypothesis about the entries of B.

This does not prove existence of a MUB companion, a spectral witness,
or the general cubic/adjoint coupling. Unitarity and Hermitian conditions
are not needed for this support equivalence and are not supplied here.
-/

noncomputable section

namespace MUBTriplets.SpectralMatching

/-- The values in the order 0,...,5 are -5,-3,-1,1,3,5. -/
def spectralNode (i : Fin 6) : ℂ := 2 * (i.val : ℂ) - 5

/-- Exactly the reverse index has the opposite fixed eigenvalue. -/
theorem spectralNode_add_eq_zero_iff (i j : Fin 6) :
    spectralNode i + spectralNode j = 0 ↔ j = Fin.rev i := by
  fin_cases i <;> fin_cases j <;>
    norm_num [spectralNode, Fin.ext_iff, Fin.val_rev]

/-- Actual finite matrix multiplication gives the anticommutator coefficient. -/
theorem anticommutator_entry (B : Matrix (Fin 6) (Fin 6) ℂ) (i j : Fin 6) :
    (Matrix.diagonal spectralNode * B + B * Matrix.diagonal spectralNode) i j =
      (spectralNode i + spectralNode j) * B i j := by
  rw [Matrix.add_apply, Matrix.diagonal_mul, Matrix.mul_diagonal]
  ring

/-- The actual matrix equation is equivalent to opposite-node matching support. -/
theorem spectral_anticommutation_iff_reverse_support
    (B : Matrix (Fin 6) (Fin 6) ℂ) :
    Matrix.diagonal spectralNode * B + B * Matrix.diagonal spectralNode = 0 ↔
      ∀ i j : Fin 6, j ≠ Fin.rev i → B i j = 0 := by
  constructor
  · intro h i j hij
    have hscalar : (spectralNode i + spectralNode j) * B i j = 0 := by
      calc
        (spectralNode i + spectralNode j) * B i j =
            (Matrix.diagonal spectralNode * B +
              B * Matrix.diagonal spectralNode) i j :=
          (anticommutator_entry B i j).symm
        _ = 0 := by rw [h]; rfl
    have hcoefficient : spectralNode i + spectralNode j ≠ 0 := by
      intro hzero
      exact hij ((spectralNode_add_eq_zero_iff i j).mp hzero)
    exact (mul_eq_zero.mp hscalar).resolve_left hcoefficient
  · intro hsupport
    apply Matrix.ext
    intro i j
    change
      (Matrix.diagonal spectralNode * B +
        B * Matrix.diagonal spectralNode) i j = 0
    rw [anticommutator_entry]
    by_cases hpair : j = Fin.rev i
    · rw [(spectralNode_add_eq_zero_iff i j).mpr hpair, zero_mul]
    · rw [hsupport i j hpair, mul_zero]

#print axioms spectralNode_add_eq_zero_iff
#print axioms anticommutator_entry
#print axioms spectral_anticommutation_iff_reverse_support

end MUBTriplets.SpectralMatching
