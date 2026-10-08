import CirculantAutocorrelation

/-!
Actual raw three-point mode identities needed by the remaining real-rank
argument: the cubic first-column product and the flat spectral neighbor sum.
No mode values or polynomial identities are supplied in place of actual
triple entries. This source alone does not prove the real-rank conclusion.
-/

noncomputable section
open MUBTriplets.CirculantCharacter MUBTriplets.CubeRootGramModes

namespace MUBTriplets.CirculantSpectralProducts

private theorem root_quadratic (omega : ℂ) (hcube : omega ^ 3 = 1)
    (hone : omega ≠ 1) : omega ^ 2 + omega + 1 = 0 := by
  have h : (omega - 1) * (omega ^ 2 + omega + 1) = 0 := by
    linear_combination hcube
  exact (mul_eq_zero.mp h).resolve_left (sub_ne_zero.mpr hone)

private theorem root_square_square (omega : ℂ) (hcube : omega ^ 3 = 1) :
    (omega ^ 2) ^ 2 = omega := by
  calc
    _ = omega ^ 3 * omega := by ring
    _ = omega := by rw [hcube]; ring

private theorem star_cube_root (theta : ℂ) (htheta : theta ^ 3 = 1) :
    star theta = theta ^ 2 := by
  have hu : theta * star theta = 1 := by
    simp only [Complex.star_def, Complex.mul_conj,
      UnitTripleZeroSum.normSq_of_cube_root theta htheta, Complex.ofReal_one]
  calc
    star theta = theta ^ 3 * star theta := by rw [htheta]; ring
    _ = theta ^ 2 * (theta * star theta) := by ring
    _ = theta ^ 2 := by rw [hu]; ring

/-- The actual raw-mode cubic reconstructs 27 times the true column product. -/
theorem phaseProduct_from_three_modes (a : Triple → ℂ) (omega : ℂ)
    (hcube : omega ^ 3 = 1) (hone : omega ≠ 1) :
    27 * phaseProduct a = (mode a 1) ^ 3 + (mode a omega) ^ 3 +
      (mode a (omega ^ 2)) ^ 3 -
      3 * mode a 1 * mode a omega * mode a (omega ^ 2) := by
  have hs : omega ^ 2 = -omega - 1 := by
    linear_combination root_quadratic omega hcube hone
  have hsq := root_square_square omega hcube
  simp only [mode, one_pow, mul_one, phaseProduct, Fin.prod_univ_three, hsq]
  simp only [hs]
  ring_nf
  simp only [hs]
  ring

private theorem three_mode_neighbor_polynomial (a : Triple → ℂ) (omega : ℂ)
    (hcube : omega ^ 3 = 1) (hone : omega ≠ 1) :
    mode a 1 * star (mode a omega) +
      mode a omega * star (mode a (omega ^ 2)) +
      mode a (omega ^ 2) * star (mode a 1) =
      3 * (a 0 * star (a 0) + omega ^ 2 * a 1 * star (a 1) +
        omega * a 2 * star (a 2)) := by
  have hs : omega ^ 2 = -omega - 1 := by
    linear_combination root_quadratic omega hcube hone
  have hsq := root_square_square omega hcube
  have hstar := star_cube_root omega hcube
  simp only [mode, one_pow, mul_one, star_add, star_mul, star_pow, hsq, hstar]
  simp only [hs]
  ring_nf
  simp only [hs]
  ring

/-- Actual entry flatness forces the true three-mode spectral neighbor sum zero. -/
theorem flat_three_mode_neighbor_sum (a : Triple → ℂ) (omega : ℂ)
    (hcube : omega ^ 3 = 1) (hone : omega ≠ 1)
    (ha : ∀ i, Complex.normSq (a i) = 1) :
    mode a 1 * star (mode a omega) +
      mode a omega * star (mode a (omega ^ 2)) +
      mode a (omega ^ 2) * star (mode a 1) = 0 := by
  have hu (i : Triple) : a i * star (a i) = 1 := by
    simp only [Complex.star_def, Complex.mul_conj, ha i, Complex.ofReal_one]
  rw [three_mode_neighbor_polynomial a omega hcube hone, hu 0]
  have hq := root_quadratic omega hcube hone
  calc
    _ = 3 * (1 + omega ^ 2 * (a 1 * star (a 1)) +
        omega * (a 2 * star (a 2))) := by ring
    _ = 0 := by rw [hu 1, hu 2]; linear_combination 3 * hq

#print axioms phaseProduct_from_three_modes
#print axioms flat_three_mode_neighbor_sum

end MUBTriplets.CirculantSpectralProducts
