import CirculantCharacter
import UnitTripleZeroSum
import PrimitiveCubicRoot
import NormalizedRawMUBBridge
import Mathlib.Analysis.Real.Sqrt
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.Linarith

/-!
Exact Fourier-block character asymmetry with an actual six-column
permutation, actual complete companion and actual normalized triplet.
No assumed Gram, companion, overlap or character certificate is an input
to the concrete endpoints. Source-specific compiler evidence is recorded
separately from this mathematical statement.

The matrix and phase construction is classical Zauner/Szollosi theory. This
does not refute the cubic-product conjecture, classify all triplets, or assert
historical originality. The underlying written proof is frozen separately.
-/

noncomputable section
open scoped BigOperators
open MUBTriplets.CirculantCharacter

namespace MUBTriplets.FourierAsymmetricTriplet

-- In the pinned Mathlib, the generic vector simproc emits internal diagnostics
-- on these concrete third entries. Use the proved third-entry rewrite instead;
-- the kernel checks the resulting proofs and all linters remain enabled.
attribute [-simp] Matrix.cons_val
attribute [local simp] Matrix.cons_val_two

def sqrtTwo : ℂ := (Real.sqrt 2 : ℝ)
def sqrtFive : ℂ := (Real.sqrt 5 : ℝ)

private theorem sqrtTwo_sq : sqrtTwo ^ 2 = 2 := by
  unfold sqrtTwo
  exact_mod_cast (Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2))

private theorem sqrtFive_sq : sqrtFive ^ 2 = 5 := by
  unfold sqrtFive
  exact_mod_cast (Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 5))

private theorem sqrtTwo_ne_zero : sqrtTwo ≠ 0 := by
  unfold sqrtTwo
  exact_mod_cast (ne_of_gt (Real.sqrt_pos.mpr (by norm_num : (0 : ℝ) < 2)))

private theorem sqrtFive_ne_zero : sqrtFive ≠ 0 := by
  unfold sqrtFive
  exact_mod_cast (ne_of_gt (Real.sqrt_pos.mpr (by norm_num : (0 : ℝ) < 5)))

private theorem sqrtTwo_normSq : Complex.normSq sqrtTwo = 2 := by
  simp only [sqrtTwo, Complex.normSq_ofReal]
  nlinarith [Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2)]

private theorem sqrtFive_normSq : Complex.normSq sqrtFive = 5 := by
  simp only [sqrtFive, Complex.normSq_ofReal]
  nlinarith [Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 5)]

private theorem root_ne_zero (ω : ℂ) (hω : ω ^ 3 = 1) : ω ≠ 0 := by
  intro h
  rw [h] at hω
  norm_num at hω

private theorem root_quadratic (ω : ℂ) (hω : ω ^ 3 = 1) (hne : ω ≠ 1) :
    ω ^ 2 + ω + 1 = 0 := by
  have hp : (ω - 1) * (ω ^ 2 + ω + 1) = 0 := by
    linear_combination hω
  exact (mul_eq_zero.mp hp).resolve_left (sub_ne_zero.mpr hne)

private theorem root_fourth (ω : ℂ) (hω : ω ^ 3 = 1) : ω ^ 4 = ω := by
  calc
    ω ^ 4 = ω ^ 3 * ω := by ring
    _ = ω := by rw [hω]; ring

private theorem root_sixth (ω : ℂ) (hω : ω ^ 3 = 1) : ω ^ 6 = 1 := by
  calc
    ω ^ 6 = (ω ^ 3) ^ 2 := by ring
    _ = 1 := by rw [hω]; norm_num

private theorem root_star (ω : ℂ) (hω : ω ^ 3 = 1) : star ω = ω ^ 2 := by
  have hu : ω * star ω = 1 := by
    simp only [Complex.star_def, Complex.mul_conj,
      UnitTripleZeroSum.normSq_of_cube_root ω hω, Complex.ofReal_one]
  calc
    star ω = ω ^ 3 * star ω := by rw [hω]; ring
    _ = ω ^ 2 * (ω * star ω) := by ring
    _ = ω ^ 2 := by rw [hu]; ring

/-- The true negative-exponent Fourier matrix F[r,k]=ω^(-rk) for Fin 3. -/
def fourier (ω : ℂ) : Matrix Triple Triple ℂ :=
  ![![1, 1, 1], ![1, ω ^ 2, ω], ![1, ω, ω ^ 2]]

def phase (ω : ℂ) : Triple → ℂ :=
  ![(1 - 2 * Complex.I) / sqrtFive,
    ((-1 - Complex.I) / sqrtTwo) * ω,
    ((-1 - Complex.I) / sqrtTwo) * ω ^ 2]

/-- Actual Fourier-block matrix, not a list of character certificates. -/
def fourierBlock (ω : ℂ) (x : Triple → ℂ) : Matrix Six Six ℂ :=
  fun i j => match i, j with
  | Sum.inl r, Sum.inl k => fourier ω r k
  | Sum.inl r, Sum.inr k => fourier ω r k
  | Sum.inr r, Sum.inl k => fourier ω r k * star (x k)
  | Sum.inr r, Sum.inr k => -(fourier ω r k * star (x k))

def columnPermutation : Six ≃ Six where
  toFun := fun j => match j with
    | Sum.inl k => ![Sum.inl 0, Sum.inr 0, Sum.inl 1] k
    | Sum.inr k => ![Sum.inr 1, Sum.inl 2, Sum.inr 2] k
  invFun := fun j => match j with
    | Sum.inl k => ![Sum.inl 0, Sum.inl 2, Sum.inr 1] k
    | Sum.inr k => ![Sum.inl 1, Sum.inr 0, Sum.inr 2] k
  left_inv := by
    intro j
    rcases j with j | j <;> fin_cases j <;> rfl
  right_inv := by
    intro j
    rcases j with j | j <;> fin_cases j <;> rfl

/-- H=KQ, with new column order [inl0,inr0,inl1;inr1,inl2,inr2]. -/
def permutedFourierBlock (ω : ℂ) (x : Triple → ℂ) : Matrix Six Six ℂ :=
  fun i j => fourierBlock ω x i (columnPermutation j)

def actualHadamard (ω : ℂ) : Matrix Six Six ℂ :=
  permutedFourierBlock ω (phase ω)

/-- The seed Hc=[C(1,i,1) C(1,-1,-1); C(1,-1,-1)* -C(1,i,1)*]. -/
def actualCompanion : Matrix Six Six ℂ :=
  fun i j => match i, j with
  | Sum.inl r, Sum.inl k =>
    ![![1, 1, Complex.I], ![Complex.I, 1, 1], ![1, Complex.I, 1]] r k
  | Sum.inl r, Sum.inr k =>
    ![![1, -1, -1], ![-1, 1, -1], ![-1, -1, 1]] r k
  | Sum.inr r, Sum.inl k =>
    ![![1, -1, -1], ![-1, 1, -1], ![-1, -1, 1]] r k
  | Sum.inr r, Sum.inr k =>
    ![![-1, Complex.I, -1], ![-1, -1, Complex.I], ![Complex.I, -1, -1]] r k

theorem companion_as_circulants : actualCompanion =
    blockCirculant ![1, Complex.I, 1] ![1, -1, -1]
      ![1, -1, -1] ![-1, -1, Complex.I] := by
  ext i j
  rcases i with i | i <;> rcases j with j | j <;>
    fin_cases i <;> fin_cases j <;> rfl

private theorem unit_ne_zero (z : ℂ) (hz : Complex.normSq z = 1) : z ≠ 0 := by
  intro h
  rw [h] at hz
  norm_num at hz

private theorem unit_mul_star (z : ℂ) (hz : Complex.normSq z = 1) :
    z * star z = 1 := by
  simp only [Complex.star_def, Complex.mul_conj, hz, Complex.ofReal_one]

theorem phase_unit (ω : ℂ) (hω : ω ^ 3 = 1) :
    ∀ k, Complex.normSq (phase ω k) = 1 := by
  have hw := UnitTripleZeroSum.normSq_of_cube_root ω hω
  have h0 : Complex.normSq (1 - 2 * Complex.I) = 5 := by
    norm_num [Complex.normSq_apply]
  have h1 : Complex.normSq (-1 - Complex.I) = 2 := by
    norm_num [Complex.normSq_apply]
  intro k
  fin_cases k <;>
    norm_num [phase, Complex.normSq_div, Complex.normSq_mul, map_pow,
      sqrtFive_normSq, sqrtTwo_normSq, h0, h1, hw]

theorem fourier_flat (ω : ℂ) (hω : ω ^ 3 = 1) :
    ∀ r k, Complex.normSq (fourier ω r k) = 1 := by
  have hw := UnitTripleZeroSum.normSq_of_cube_root ω hω
  intro r k
  fin_cases r <;> fin_cases k <;> simp [fourier, map_pow, hw]

theorem fourier_gram (ω : ℂ) (hω : ω ^ 3 = 1) (hne : ω ≠ 1) :
    (fourier ω).conjTranspose * fourier ω =
      (3 : ℂ) • (1 : Matrix Triple Triple ℂ) := by
  have hs := root_star ω hω
  have h4 := root_fourth ω hω
  have hq := root_quadratic ω hω hne
  have h2 : ω ^ 2 = -ω - 1 := by linear_combination hq
  have h5 : ω ^ 5 = ω ^ 2 := by
    calc
      ω ^ 5 = ω ^ 3 * ω ^ 2 := by ring
      _ = ω ^ 2 := by rw [hω]; ring
  have h6 := root_sixth ω hω
  have hs2 : star (ω ^ 2) = ω := by
    calc
      star (ω ^ 2) = (star ω) ^ 2 := star_pow ω 2
      _ = (ω ^ 2) ^ 2 := by rw [hs]
      _ = ω ^ 4 := by ring
      _ = ω := h4
  ext r k
  change (∑ t : Triple, star (fourier ω t r) * fourier ω t k) =
    (3 : ℂ) * (if r = k then 1 else 0)
  simp only [Fin.sum_univ_three]
  fin_cases r <;> fin_cases k <;>
    simp only [fourier, Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.cons_val_two, Matrix.cons_val_succ, Matrix.vecHead, Matrix.vecTail, Function.comp_apply]
  all_goals norm_num
  all_goals
    simp (config := { failIfUnchanged := false }) only [starRingEnd_apply, hs]
    ring_nf
    simp (config := { failIfUnchanged := false }) only [hω, h4, h5, h6]
    simp (config := { failIfUnchanged := false }) only [h2]
    ring

private theorem gram_ll (ω : ℂ) (x : Triple → ℂ) (i j : Triple) :
    ((fourierBlock ω x).conjTranspose * fourierBlock ω x) (Sum.inl i) (Sum.inl j) =
      (1 + x i * star (x j)) * ((fourier ω).conjTranspose * fourier ω) i j := by
  simp only [Matrix.mul_apply, Matrix.conjTranspose_apply, Fintype.sum_sum_type,
    Fin.sum_univ_three, fourierBlock, star_mul, star_star]
  ring

private theorem gram_lr (ω : ℂ) (x : Triple → ℂ) (i j : Triple) :
    ((fourierBlock ω x).conjTranspose * fourierBlock ω x) (Sum.inl i) (Sum.inr j) =
      (1 - x i * star (x j)) * ((fourier ω).conjTranspose * fourier ω) i j := by
  simp only [Matrix.mul_apply, Matrix.conjTranspose_apply, Fintype.sum_sum_type,
    Fin.sum_univ_three, fourierBlock, star_mul, star_star]
  ring

private theorem gram_rl (ω : ℂ) (x : Triple → ℂ) (i j : Triple) :
    ((fourierBlock ω x).conjTranspose * fourierBlock ω x) (Sum.inr i) (Sum.inl j) =
      (1 - x i * star (x j)) * ((fourier ω).conjTranspose * fourier ω) i j := by
  simp only [Matrix.mul_apply, Matrix.conjTranspose_apply, Fintype.sum_sum_type,
    Fin.sum_univ_three, fourierBlock, star_mul, star_star, star_neg]
  ring

private theorem gram_rr (ω : ℂ) (x : Triple → ℂ) (i j : Triple) :
    ((fourierBlock ω x).conjTranspose * fourierBlock ω x) (Sum.inr i) (Sum.inr j) =
      (1 + x i * star (x j)) * ((fourier ω).conjTranspose * fourier ω) i j := by
  simp only [Matrix.mul_apply, Matrix.conjTranspose_apply, Fintype.sum_sum_type,
    Fin.sum_univ_three, fourierBlock, star_mul, star_star, star_neg]
  ring

theorem fourierBlock_gram (ω : ℂ) (x : Triple → ℂ)
    (hω : ω ^ 3 = 1) (hne : ω ≠ 1) (hx : ∀ k, Complex.normSq (x k) = 1) :
    (fourierBlock ω x).conjTranspose * fourierBlock ω x =
      (6 : ℂ) • (1 : Matrix Six Six ℂ) := by
  have hF := fourier_gram ω hω hne
  have hu (k : Triple) := unit_mul_star (x k) (hx k)
  ext i j
  rcases i with i | i <;> rcases j with j | j
  · rw [gram_ll, hF]
    by_cases hij : i = j
    · subst j
      simp [Matrix.smul_apply]
      simp only [starRingEnd_apply]
      rw [hu i]
      norm_num
    · simp [Matrix.smul_apply, hij]
  · rw [gram_lr, hF]
    by_cases hij : i = j
    · subst j
      simp [Matrix.smul_apply]
      simp only [starRingEnd_apply]
      rw [hu i]
      norm_num
    · simp [Matrix.smul_apply, hij]
  · rw [gram_rl, hF]
    by_cases hij : i = j
    · subst j
      simp [Matrix.smul_apply]
      simp only [starRingEnd_apply]
      rw [hu i]
      norm_num
    · simp [Matrix.smul_apply, hij]
  · rw [gram_rr, hF]
    by_cases hij : i = j
    · subst j
      simp [Matrix.smul_apply]
      simp only [starRingEnd_apply]
      rw [hu i]
      norm_num
    · simp [Matrix.smul_apply, hij]

theorem actual_flat (ω : ℂ) (hω : ω ^ 3 = 1) :
    ∀ i j, Complex.normSq (actualHadamard ω i j) = 1 := by
  have hF := fourier_flat ω hω
  have hx := phase_unit ω hω
  have hK : ∀ i j, Complex.normSq (fourierBlock ω (phase ω) i j) = 1 := by
    intro i j
    rcases i with i | i <;> rcases j with j | j <;>
      simp [fourierBlock, Complex.normSq_mul, Complex.star_def, hF, hx]
  intro i j
  exact hK i (columnPermutation j)

theorem actual_gram (ω : ℂ) (hω : ω ^ 3 = 1) (hne : ω ≠ 1) :
    (actualHadamard ω).conjTranspose * actualHadamard ω =
      (6 : ℂ) • (1 : Matrix Six Six ℂ) := by
  have hK := fourierBlock_gram ω (phase ω) hω hne (phase_unit ω hω)
  ext i j
  have he := congrArg (fun M : Matrix Six Six ℂ =>
    M (columnPermutation i) (columnPermutation j)) hK
  simpa [actualHadamard, permutedFourierBlock, Matrix.mul_apply,
    Matrix.conjTranspose_apply, Matrix.smul_apply, Matrix.one_apply,
    columnPermutation.injective.eq_iff] using he

private def columnRatio (M : Matrix Six Six ℂ) (j : Six) : ℂ :=
  (∏ i : Triple, M (Sum.inl i) j) / (∏ i : Triple, M (Sum.inr i) j)

private theorem actual_ratio_table (ω : ℂ) (x : Triple → ℂ)
    (hω : ω ^ 3 = 1) (hx : ∀ k, x k ≠ 0) (j : Six) :
    columnRatio (permutedFourierBlock ω x) j =
      match j with
      | Sum.inl k => ![1 / (star (x 0)) ^ 3,
          -(1 / (star (x 0)) ^ 3), 1 / (star (x 1)) ^ 3] k
      | Sum.inr k => ![-(1 / (star (x 1)) ^ 3),
          1 / (star (x 2)) ^ 3, -(1 / (star (x 2)) ^ 3)] k := by
  have hw0 := root_ne_zero ω hω
  have hs0 : star (x 0) ≠ 0 := by simpa using hx 0
  have hs1 : star (x 1) ≠ 0 := by simpa using hx 1
  have hs2 : star (x 2) ≠ 0 := by simpa using hx 2
  rcases j with j | j <;> fin_cases j <;>
    simp [columnRatio, permutedFourierBlock, columnPermutation, fourierBlock,
      fourier, Fin.prod_univ_three] <;>
    field_simp [hs0, hs1, hs2, hw0]

theorem actual_first_and_cubic_zero (ω : ℂ) (hω : ω ^ 3 = 1) :
    balancedCharacter (actualHadamard ω) 1 = 0 ∧
      balancedCharacter (actualHadamard ω) 3 = 0 := by
  have hx (k) := unit_ne_zero (phase ω k) (phase_unit ω hω k)
  have ht := actual_ratio_table ω (phase ω) hω hx
  constructor
  · change (∑ j, columnRatio (permutedFourierBlock ω (phase ω)) j ^ 1) = 0
    simp only [Fintype.sum_sum_type, Fin.sum_univ_three, ht]
    norm_num
  · change (∑ j, columnRatio (permutedFourierBlock ω (phase ω)) j ^ 3) = 0
    simp only [Fintype.sum_sum_type, Fin.sum_univ_three, ht]
    norm_num
    ring

private theorem adjoint_ratio_table (ω : ℂ) (x : Triple → ℂ)
    (hω : ω ^ 3 = 1) (hx : ∀ k, x k ≠ 0) (r : Triple) :
    columnRatio (permutedFourierBlock ω x).conjTranspose (Sum.inl r) =
      ![1, ω ^ 2, ω] r ∧
    columnRatio (permutedFourierBlock ω x).conjTranspose (Sum.inr r) =
      -((x 0 / x 2) ^ 2) * ![1, ω ^ 2, ω] r := by
  have hw0 := root_ne_zero ω hω
  have hs := root_star ω hω
  have h4 := root_fourth ω hω
  have h6 := root_sixth ω hω
  have h5 : ω ^ 5 = ω ^ 2 := by
    calc
      ω ^ 5 = ω ^ 3 * ω ^ 2 := by ring
      _ = ω ^ 2 := by rw [hω]; ring
  have h7 : ω ^ 7 = ω := by
    calc
      ω ^ 7 = (ω ^ 3) ^ 2 * ω := by ring
      _ = ω := by rw [hω]; ring
  have h9 : ω ^ 9 = 1 := by
    calc
      ω ^ 9 = (ω ^ 3) ^ 3 := by ring
      _ = 1 := by rw [hω]; norm_num
  fin_cases r <;> constructor <;>
    norm_num [columnRatio, Matrix.conjTranspose_apply, permutedFourierBlock,
      columnPermutation, fourierBlock, fourier, Fin.prod_univ_three,
      star_mul, star_pow, star_neg, star_star, star_one] <;>
    simp (config := { failIfUnchanged := false }) only [starRingEnd_apply, hs] <;>
    field_simp [hx 0, hx 1, hx 2, hw0] <;> ring_nf (ifUnchanged := .silent) <;>
    simp (config := { failIfUnchanged := false }) only [h6, h9]

theorem adjoint_character_formula (ω : ℂ) (x : Triple → ℂ)
    (hω : ω ^ 3 = 1) (hne : ω ≠ 1) (hx : ∀ k, x k ≠ 0) :
    balancedCharacter (permutedFourierBlock ω x).conjTranspose 1 = 0 ∧
    balancedCharacter (permutedFourierBlock ω x).conjTranspose 3 =
      3 * (1 - (x 0 / x 2) ^ 6) := by
  have ht := adjoint_ratio_table ω x hω hx
  have hq := root_quadratic ω hω hne
  have h6 := root_sixth ω hω
  constructor
  · change (∑ j, columnRatio (permutedFourierBlock ω x).conjTranspose j ^ 1) = 0
    simp only [Fintype.sum_sum_type, Fin.sum_univ_three, pow_one]
    simp only [(ht 0).1, (ht 1).1, (ht 2).1, (ht 0).2, (ht 1).2, (ht 2).2]
    dsimp
    simp only [Matrix.head_cons, Matrix.tail_cons]
    linear_combination (1 - (x 0 / x 2) ^ 2) * hq
  · change (∑ j, columnRatio (permutedFourierBlock ω x).conjTranspose j ^ 3) = _
    simp only [Fintype.sum_sum_type, Fin.sum_univ_three]
    simp only [(ht 0).1, (ht 1).1, (ht 2).1, (ht 0).2, (ht 1).2, (ht 2).2]
    dsimp
    simp only [Matrix.head_cons, Matrix.tail_cons]
    ring_nf
    simp (config := { failIfUnchanged := false }) only [hω, h6]
    ring

private theorem phase_zero_sixth (ω : ℂ) :
    (phase ω 0) ^ 6 = (117 - 44 * Complex.I) / 125 := by
  have h6 : sqrtFive ^ 6 = 125 := by
    calc
      sqrtFive ^ 6 = (sqrtFive ^ 2) ^ 3 := by ring
      _ = 125 := by rw [sqrtFive_sq]; norm_num
  change ((1 - 2 * Complex.I) / sqrtFive) ^ 6 = _
  rw [div_pow]
  rw [h6]
  norm_num [pow_succ, Complex.ext_iff, Complex.mul_re, Complex.mul_im]

private theorem phase_two_sixth (ω : ℂ) (hω : ω ^ 3 = 1) :
    (phase ω 2) ^ 6 = -Complex.I := by
  have h6 : sqrtTwo ^ 6 = 8 := by
    calc
      sqrtTwo ^ 6 = (sqrtTwo ^ 2) ^ 3 := by ring
      _ = 8 := by rw [sqrtTwo_sq]; norm_num
  have hw12 : (ω ^ 2) ^ 6 = 1 := by
    calc
      (ω ^ 2) ^ 6 = (ω ^ 3) ^ 4 := by ring
      _ = 1 := by rw [hω]; norm_num
  change (((-1 - Complex.I) / sqrtTwo) * ω ^ 2) ^ 6 = _
  rw [mul_pow, div_pow]
  rw [h6, hw12]
  norm_num [pow_succ, Complex.ext_iff, Complex.mul_re, Complex.mul_im]

theorem actual_phase_ratio_sixth (ω : ℂ) (hω : ω ^ 3 = 1) :
    (phase ω 0 / phase ω 2) ^ 6 = (44 + 117 * Complex.I) / 125 := by
  rw [div_pow, phase_zero_sixth, phase_two_sixth ω hω]
  norm_num [Complex.ext_iff, Complex.div_re, Complex.div_im, Complex.normSq_apply]

def asymmetricValue : ℂ := (243 - 351 * Complex.I) / 125

theorem asymmetricValue_normSq : Complex.normSq asymmetricValue = 1458 / 125 := by
  norm_num [asymmetricValue, Complex.normSq_div, Complex.normSq_apply]

theorem asymmetricValue_ne_zero : asymmetricValue ≠ 0 := by
  intro h
  have hn := asymmetricValue_normSq
  rw [h] at hn
  norm_num at hn

/-- Actual entry flatness, actual Gram and same-partition character asymmetry.
No complete-companion assertion is included in this first connected endpoint. -/
theorem actual_flat_gram_character_asymmetry (ω : ℂ)
    (hω : ω ^ 3 = 1) (hne : ω ≠ 1) :
    (∀ i j, Complex.normSq (actualHadamard ω i j) = 1) ∧
    (actualHadamard ω).conjTranspose * actualHadamard ω =
      (6 : ℂ) • (1 : Matrix Six Six ℂ) ∧
    balancedCharacter (actualHadamard ω) 1 = 0 ∧
    balancedCharacter (actualHadamard ω) 3 = 0 ∧
    balancedCharacter (actualHadamard ω).conjTranspose 1 = 0 ∧
    balancedCharacter (actualHadamard ω).conjTranspose 3 = asymmetricValue ∧
    Complex.normSq (balancedCharacter (actualHadamard ω).conjTranspose 3) =
      1458 / 125 := by
  have hz := actual_first_and_cubic_zero ω hω
  have hx (k) := unit_ne_zero (phase ω k) (phase_unit ω hω k)
  have ha := adjoint_character_formula ω (phase ω) hω hne hx
  have hv : balancedCharacter (actualHadamard ω).conjTranspose 3 =
      asymmetricValue := by
    change balancedCharacter (permutedFourierBlock ω (phase ω)).conjTranspose 3 = _
    rw [ha.2, actual_phase_ratio_sixth ω hω]
    norm_num [asymmetricValue]
    ring
  refine ⟨actual_flat ω hω, actual_gram ω hω hne, hz.1, hz.2, ha.1, hv, ?_⟩
  rw [hv]
  exact asymmetricValue_normSq

/-- The companion seed has actual unit entries, checked on its real entries. -/
theorem companion_flat : ∀ i j, Complex.normSq (actualCompanion i j) = 1 := by
  intro i j
  rcases i with i | i <;> rcases j with j | j <;>
    fin_cases i <;> fin_cases j <;>
    norm_num [actualCompanion, blockCirculant, Matrix.circulant,
      Complex.normSq_apply]

/-- Actual six-by-six column Gram of the concrete seed. -/
theorem companion_gram : actualCompanion.conjTranspose * actualCompanion =
    (6 : ℂ) • (1 : Matrix Six Six ℂ) := by
  ext i j
  simp only [Matrix.mul_apply, Matrix.conjTranspose_apply,
    Fintype.sum_sum_type, Fin.sum_univ_three, Matrix.smul_apply,
    Matrix.one_apply]
  rcases i with i | i <;> rcases j with j | j <;>
    fin_cases i <;> fin_cases j <;>
    norm_num [actualCompanion, blockCirculant, Matrix.circulant,
      Complex.star_def] <;> ring

/-- These are the actual Fourier coefficients of Hc* K, with no overlap premise. -/
private def overlapFactor (ω : ℂ) (rowSide columnSide : Bool) : Triple → ℂ :=
  match rowSide, columnSide with
  | false, false => ![(2 - Complex.I) * (1 - Complex.I / sqrtFive),
      (-1 - Complex.I) * (1 - sqrtTwo * Complex.I) * ω ^ 2,
      (-1 - Complex.I) * (1 - sqrtTwo * Complex.I) * ω]
  | false, true => ![(2 - Complex.I) * (1 + Complex.I / sqrtFive),
      (-1 - Complex.I) * (1 + sqrtTwo * Complex.I) * ω ^ 2,
      (-1 - Complex.I) * (1 + sqrtTwo * Complex.I) * ω]
  | true, false => ![-1 - sqrtFive * Complex.I,
      2 + sqrtTwo * Complex.I, 2 + sqrtTwo * Complex.I]
  | true, true => ![-1 + sqrtFive * Complex.I,
      2 - sqrtTwo * Complex.I, 2 - sqrtTwo * Complex.I]

private theorem overlapFactor_normSq (ω : ℂ) (hω : ω ^ 3 = 1)
    (rowSide columnSide : Bool) (k : Triple) :
    Complex.normSq (overlapFactor ω rowSide columnSide k) = 6 := by
  have hw := UnitTripleZeroSum.normSq_of_cube_root ω hω
  have h2 : (Real.sqrt 2) ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have h5 : (Real.sqrt 5) ^ 2 = 5 := Real.sq_sqrt (by norm_num)
  have h20 : Real.sqrt 2 ≠ 0 := ne_of_gt (Real.sqrt_pos.mpr (by norm_num))
  have h50 : Real.sqrt 5 ≠ 0 := ne_of_gt (Real.sqrt_pos.mpr (by norm_num))
  have hn0 : Complex.normSq (2 - Complex.I) = 5 := by
    norm_num [Complex.normSq_apply]
  have hn1 : Complex.normSq (-1 - Complex.I) = 2 := by
    norm_num [Complex.normSq_apply]
  have h0m : Complex.normSq ((2 - Complex.I) * (1 - Complex.I / sqrtFive)) = 6 := by
    rw [Complex.normSq_mul, hn0]
    norm_num [Complex.normSq_apply, sqrtFive]
    field_simp [h50]
    nlinarith [h5]
  have h0p : Complex.normSq ((2 - Complex.I) * (1 + Complex.I / sqrtFive)) = 6 := by
    rw [Complex.normSq_mul, hn0]
    norm_num [Complex.normSq_apply, sqrtFive]
    field_simp [h50]
    nlinarith [h5]
  have h1m : Complex.normSq ((-1 - Complex.I) * (1 - sqrtTwo * Complex.I)) = 6 := by
    rw [Complex.normSq_mul, hn1]
    norm_num [Complex.normSq_apply, sqrtTwo]
  have h1p : Complex.normSq ((-1 - Complex.I) * (1 + sqrtTwo * Complex.I)) = 6 := by
    rw [Complex.normSq_mul, hn1]
    norm_num [Complex.normSq_apply, sqrtTwo]
  have h2m : Complex.normSq (-1 - sqrtFive * Complex.I) = 6 := by
    norm_num [Complex.normSq_apply, sqrtFive]
  have h2p : Complex.normSq (-1 + sqrtFive * Complex.I) = 6 := by
    norm_num [Complex.normSq_apply, sqrtFive]
  have h3p : Complex.normSq (2 + sqrtTwo * Complex.I) = 6 := by
    norm_num [Complex.normSq_apply, sqrtTwo]
  have h3m : Complex.normSq (2 - sqrtTwo * Complex.I) = 6 := by
    norm_num [Complex.normSq_apply, sqrtTwo]
  cases rowSide <;> cases columnSide <;> fin_cases k
  all_goals first
    | exact h0m
    | exact h0p
    | exact h2m
    | exact h2p
    | exact h3m
    | exact h3p
    | (change Complex.normSq (((-1 - Complex.I) * (1 - sqrtTwo * Complex.I)) * ω ^ 2) = 6
       rw [Complex.normSq_mul, h1m, map_pow, hw]; norm_num)
    | (change Complex.normSq (((-1 - Complex.I) * (1 - sqrtTwo * Complex.I)) * ω) = 6
       rw [Complex.normSq_mul, h1m, hw]; norm_num)
    | (change Complex.normSq (((-1 - Complex.I) * (1 + sqrtTwo * Complex.I)) * ω ^ 2) = 6
       rw [Complex.normSq_mul, h1p, map_pow, hw]; norm_num)
    | (change Complex.normSq (((-1 - Complex.I) * (1 + sqrtTwo * Complex.I)) * ω) = 6
       rw [Complex.normSq_mul, h1p, hw]; norm_num)

set_option maxHeartbeats 1000000 in
/-- Full actual overlap identity before the harmless six-column permutation. -/
private theorem companion_fourier_overlap_formula (ω : ℂ)
    (hω : ω ^ 3 = 1) (hne : ω ≠ 1) (i j : Six) :
    (actualCompanion.conjTranspose * fourierBlock ω (phase ω)) i j =
      match i, j with
      | Sum.inl r, Sum.inl k => fourier ω r k * overlapFactor ω false false k
      | Sum.inl r, Sum.inr k => fourier ω r k * overlapFactor ω false true k
      | Sum.inr r, Sum.inl k => fourier ω r k * overlapFactor ω true false k
      | Sum.inr r, Sum.inr k => fourier ω r k * overlapFactor ω true true k := by
  have hs := root_star ω hω
  have h4 := root_fourth ω hω
  have h5 : ω ^ 5 = ω ^ 2 := by
    calc
      ω ^ 5 = ω ^ 3 * ω ^ 2 := by ring
      _ = ω ^ 2 := by rw [hω]; ring
  have h6 := root_sixth ω hω
  have hq := root_quadratic ω hω hne
  have h2 : ω ^ 2 = -ω - 1 := by linear_combination hq
  have hsw2 : star (ω ^ 2) = ω := by
    calc
      star (ω ^ 2) = (star ω) ^ 2 := star_pow ω 2
      _ = (ω ^ 2) ^ 2 := by rw [hs]
      _ = ω ^ 4 := by ring
      _ = ω := h4
  have hs2 : star sqrtTwo = sqrtTwo := by simp [sqrtTwo]
  have hs5 : star sqrtFive = sqrtFive := by simp [sqrtFive]
  have hsi : star Complex.I = -Complex.I := by
    change (starRingEnd ℂ) Complex.I = -Complex.I
    exact Complex.conj_I
  simp only [Matrix.mul_apply, Matrix.conjTranspose_apply,
    Fintype.sum_sum_type, Fin.sum_univ_three]
  rcases i with i | i <;> rcases j with j | j <;>
    fin_cases i <;> fin_cases j <;>
    norm_num [actualCompanion, blockCirculant, Matrix.circulant,
      fourierBlock, fourier, phase, overlapFactor]
  all_goals
    simp (config := { failIfUnchanged := false }) only [starRingEnd_apply, hs2, hs5, hs]
    field_simp [sqrtTwo_ne_zero, sqrtFive_ne_zero]
    ring_nf
    simp (config := { failIfUnchanged := false }) only [hω, h4, h5, h6, h2,
      sqrtTwo_sq, sqrtFive_sq, Complex.I_sq]
    ring

theorem companion_fourier_overlap_normSq (ω : ℂ)
    (hω : ω ^ 3 = 1) (hne : ω ≠ 1) :
    ∀ i j, Complex.normSq
      ((actualCompanion.conjTranspose * fourierBlock ω (phase ω)) i j) = 6 := by
  intro i j
  rw [companion_fourier_overlap_formula ω hω hne i j]
  rcases i with i | i <;> rcases j with j | j <;>
    rw [Complex.normSq_mul, fourier_flat ω hω, overlapFactor_normSq ω hω]
  all_goals norm_num

theorem companion_actual_overlap_normSq (ω : ℂ)
    (hω : ω ^ 3 = 1) (hne : ω ≠ 1) :
    ∀ i j, Complex.normSq
      ((actualCompanion.conjTranspose * actualHadamard ω) i j) = 6 := by
  intro i j
  have hf := companion_fourier_overlap_normSq ω hω hne i (columnPermutation j)
  simpa [actualHadamard, permutedFourierBlock, Matrix.mul_apply] using hf

theorem actual_companion_overlap_normSq (ω : ℂ)
    (hω : ω ^ 3 = 1) (hne : ω ≠ 1) :
    ∀ i j, Complex.normSq
      (((actualHadamard ω).conjTranspose * actualCompanion) i j) = 6 := by
  intro i j
  have ht : (actualCompanion.conjTranspose * actualHadamard ω).conjTranspose =
      (actualHadamard ω).conjTranspose * actualCompanion := by
    simp only [Matrix.conjTranspose_mul, Matrix.conjTranspose_conjTranspose]
  have hf := companion_actual_overlap_normSq ω hω hne j i
  rw [← ht, Matrix.conjTranspose_apply]
  simpa only [Complex.star_def, Complex.normSq_conj] using hf

/-- Complete companion and character asymmetry of actual matrices, with no
given Gram, overlap or character-value premise. These are all six columns. -/
theorem actual_raw_triplet_character_asymmetry (ω : ℂ)
    (hω : ω ^ 3 = 1) (hne : ω ≠ 1) :
    (∀ i j, Complex.normSq (actualHadamard ω i j) = 1) ∧
    (actualHadamard ω).conjTranspose * actualHadamard ω =
      (6 : ℂ) • (1 : Matrix Six Six ℂ) ∧
    (∀ i j, Complex.normSq (actualCompanion i j) = 1) ∧
    actualCompanion.conjTranspose * actualCompanion =
      (6 : ℂ) • (1 : Matrix Six Six ℂ) ∧
    (∀ i j, Complex.normSq
      (((actualHadamard ω).conjTranspose * actualCompanion) i j) = 6) ∧
    balancedCharacter (actualHadamard ω) 3 = 0 ∧
    balancedCharacter (actualHadamard ω).conjTranspose 3 = asymmetricValue ∧
    Complex.normSq (balancedCharacter (actualHadamard ω).conjTranspose 3) =
      1458 / 125 := by
  have hc := actual_flat_gram_character_asymmetry ω hω hne
  exact ⟨hc.1, hc.2.1, companion_flat, companion_gram,
    actual_companion_overlap_normSq ω hω hne, hc.2.2.2.1,
    hc.2.2.2.2.2.1, hc.2.2.2.2.2.2⟩

/-- A concrete primitive root gives a closed actual-triplet statement. The
identity basis is implicit in unit entry flatness and the two raw Grams. -/
theorem concrete_raw_triplet_character_asymmetry :
    let H := actualHadamard PrimitiveCubicRoot.omega
    (∀ i j, Complex.normSq (H i j) = 1) ∧
    H.conjTranspose * H = (6 : ℂ) • (1 : Matrix Six Six ℂ) ∧
    (∀ i j, Complex.normSq (actualCompanion i j) = 1) ∧
    actualCompanion.conjTranspose * actualCompanion =
      (6 : ℂ) • (1 : Matrix Six Six ℂ) ∧
    (∀ i j, Complex.normSq ((H.conjTranspose * actualCompanion) i j) = 6) ∧
    balancedCharacter H 3 = 0 ∧
    balancedCharacter H.conjTranspose 3 = asymmetricValue ∧
    Complex.normSq (balancedCharacter H.conjTranspose 3) = 1458 / 125 := by
  exact actual_raw_triplet_character_asymmetry PrimitiveCubicRoot.omega
    PrimitiveCubicRoot.omega_cube PrimitiveCubicRoot.omega_ne_one

/-- The concrete identity/H/companion matrices have all three normalized
column Grams and all three pairwise transition norms, together with the
unequal raw cubic characters at the displayed balanced partition. -/
theorem concrete_normalized_triplet_character_asymmetry :
    let H := actualHadamard PrimitiveCubicRoot.omega
    NormalizedRawMUBBridge.ActualNormalizedTriplet H actualCompanion ∧
    balancedCharacter H 3 = 0 ∧
    balancedCharacter H.conjTranspose 3 = asymmetricValue ∧
    Complex.normSq (balancedCharacter H.conjTranspose 3) = 1458 / 125 := by
  have h := concrete_raw_triplet_character_asymmetry
  refine ⟨NormalizedRawMUBBridge.actual_normalized_triplet_of_raw
    _ _ h.1 h.2.2.1 h.2.1 h.2.2.2.1 h.2.2.2.2.1, ?_⟩
  exact h.2.2.2.2.2

#print axioms phase_unit
#print axioms fourier_gram
#print axioms actual_gram
#print axioms actual_first_and_cubic_zero
#print axioms adjoint_character_formula
#print axioms actual_phase_ratio_sixth
#print axioms asymmetricValue_normSq
#print axioms actual_flat_gram_character_asymmetry
#print axioms companion_gram
#print axioms companion_as_circulants
#print axioms companion_fourier_overlap_normSq
#print axioms actual_companion_overlap_normSq
#print axioms actual_raw_triplet_character_asymmetry
#print axioms concrete_raw_triplet_character_asymmetry
#print axioms concrete_normalized_triplet_character_asymmetry

end MUBTriplets.FourierAsymmetricTriplet
