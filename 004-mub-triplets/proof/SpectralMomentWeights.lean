import Mathlib.Basic.Real.Basic
import Mathlib.Data.Fin.Basic
import Mathlib.Data.Fintype.Fin
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-!
The fixed spectral nodes are -5,-3,-1,1,3,5. This proves the exact
six-weight reconstruction used in a complete-companion spectral reduction.
It is not a formalization of spectral diagonalization, the Hadamard matrix
conditions, or the MUB coupling conjecture. No sign assumption on weights
is needed: the finite linear system alone forces flat weights.
-/

namespace MUBTriplets.SpectralMoments

def weightedMoment (w : Fin 6 → ℝ) (m : ℕ) : ℝ :=
  w 0 * (-5 : ℝ)^m + w 1 * (-3 : ℝ)^m + w 2 * (-1 : ℝ)^m +
  w 3 * (1 : ℝ)^m + w 4 * (3 : ℝ)^m + w 5 * (5 : ℝ)^m

def traceMoment (m : ℕ) : ℝ :=
  (-5 : ℝ)^m + (-3 : ℝ)^m + (-1 : ℝ)^m +
  (1 : ℝ)^m + (3 : ℝ)^m + (5 : ℝ)^m

def FlatMoments (w : Fin 6 → ℝ) : Prop :=
  ∀ m : Fin 6, 6 * weightedMoment w m.val = traceMoment m.val

theorem flat_weights_of_moments {w : Fin 6 → ℝ} (h : FlatMoments w) :
    ∀ i, w i = (1 : ℝ) / 6 := by
  have h0 := h 0
  have h1 := h 1
  have h2 := h 2
  have h3 := h 3
  have h4 := h 4
  have h5 := h 5
  norm_num [weightedMoment, traceMoment] at h0 h1 h2 h3 h4 h5
  have a0 : w 0 = (1 : ℝ) / 6 := by linarith
  have a1 : w 1 = (1 : ℝ) / 6 := by linarith
  have a2 : w 2 = (1 : ℝ) / 6 := by linarith
  have a3 : w 3 = (1 : ℝ) / 6 := by linarith
  have a4 : w 4 = (1 : ℝ) / 6 := by linarith
  have a5 : w 5 = (1 : ℝ) / 6 := by linarith
  intro i
  fin_cases i <;> assumption

theorem moments_of_flat_weights {w : Fin 6 → ℝ}
    (h : ∀ i, w i = (1 : ℝ) / 6) : FlatMoments w := by
  intro m
  simp only [weightedMoment, traceMoment, h]
  ring

theorem flat_moments_iff_weights (w : Fin 6 → ℝ) :
    FlatMoments w ↔ ∀ i, w i = (1 : ℝ) / 6 :=
  ⟨flat_weights_of_moments, moments_of_flat_weights⟩

#print axioms flat_weights_of_moments
#print axioms moments_of_flat_weights
#print axioms flat_moments_iff_weights

end MUBTriplets.SpectralMoments
