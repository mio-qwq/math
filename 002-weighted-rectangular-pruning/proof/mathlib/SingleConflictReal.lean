import Mathlib.Basic.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-!
# Exact real-cost classification for a single rectangular conflict

The graph is `zl -- c -- r -- zr`. Its original costs are `x,y`,
its two corner-copy costs are `z`, and its other cross-corner budget is `h`.
The cover theorem needs only `0 ≤ z`; the pruning criterion needs no
sign assumption. Consequently both apply to arbitrary nonnegative real
pair costs, including irrational and zero costs, without a scaling argument.

We prove the exact cover minimum, exact feasibility threshold, equivalence
with pruning, and the actual two-positive-product-system boundary example.
This file does not formalize the general rectangular rank/pruning theorem.
All proofs are checked by Lean's kernel, without `sorry`, new axioms,
or `native_decide`.
-/

namespace RectangularPruning.SingleConflictReal

def IsCover (r c zl zr : Bool) : Prop :=
  (r || c) = true ∧ (r || zr) = true ∧ (zl || c) = true

def coverCost (x y z : ℝ) (r c zl zr : Bool) : ℝ :=
  (if r then x else 0) + (if c then y else 0) +
  (if zl then z else 0) + (if zr then z else 0)

def HasCover (x y h z : ℝ) : Prop :=
  ∃ r c zl zr : Bool,
    IsCover r c zl zr ∧ coverCost x y z r c zl zr ≤ h + z

def IsConflictFreePruning (deleteR deleteC : Bool) : Prop :=
  (deleteR || deleteC) = true

def deletionCost (x y : ℝ) (deleteR deleteC : Bool) : ℝ :=
  (if deleteR then x else 0) + (if deleteC then y else 0)

def uncoveredCost (z : ℝ) (deleteR deleteC : Bool) : ℝ :=
  if deleteR && deleteC then z else 0

def HasPruning (x y h z : ℝ) : Prop :=
  ∃ deleteR deleteC : Bool,
    IsConflictFreePruning deleteR deleteC ∧
      deletionCost x y deleteR deleteC ≤ h + uncoveredCost z deleteR deleteC

/-- Exact feasibility for arbitrary real original costs and nonnegative corner cost. -/
theorem cover_iff (x y h z : ℝ) (hz : 0 ≤ z) :
    HasCover x y h z ↔ x ≤ h ∨ y ≤ h ∨ x + y ≤ h + z := by
  constructor
  · rintro ⟨r, c, zl, zr, hcover, hcost⟩
    cases r <;> cases c <;> cases zl <;> cases zr <;>
      simp [IsCover, coverCost] at hcover hcost <;>
      first | (left; linarith) | (right; left; linarith) | (right; right; linarith)
  · rintro (hx | hy | hxy)
    · refine ⟨true, false, true, false, ?_, ?_⟩
      · simp [IsCover]
      · simp [coverCost]
        linarith
    · refine ⟨false, true, false, true, ?_, ?_⟩
      · simp [IsCover]
      · simp [coverCost]
        linarith
    · refine ⟨true, true, false, false, ?_, ?_⟩
      · simp [IsCover]
      · simpa [coverCost] using hxy

/-- Pruning feasibility is algebraically exact even without sign assumptions. -/
theorem pruning_iff (x y h z : ℝ) :
    HasPruning x y h z ↔ x ≤ h ∨ y ≤ h ∨ x + y ≤ h + z := by
  constructor
  · rintro ⟨deleteR, deleteC, hfree, hcost⟩
    cases deleteR <;> cases deleteC <;>
      simp [IsConflictFreePruning, deletionCost, uncoveredCost] at hfree hcost <;>
      first | (left; linarith) | (right; left; linarith) | (right; right; linarith)
  · rintro (hx | hy | hxy)
    · refine ⟨true, false, ?_, ?_⟩
      · simp [IsConflictFreePruning]
      · simpa [deletionCost, uncoveredCost] using hx
    · refine ⟨false, true, ?_, ?_⟩
      · simp [IsConflictFreePruning]
      · simpa [deletionCost, uncoveredCost] using hy
    · refine ⟨true, true, ?_, ?_⟩
      · simp [IsConflictFreePruning]
      · simpa [deletionCost, uncoveredCost] using hxy

theorem cover_iff_pruning (x y h z : ℝ) (hz : 0 ≤ z) :
    HasCover x y h z ↔ HasPruning x y h z :=
  (cover_iff x y h z hz).trans (pruning_iff x y h z).symm

def threshold (x y z : ℝ) : ℝ := min x (min y (x + y - z))

theorem criterion_iff_threshold (x y h z : ℝ) :
    (x ≤ h ∨ y ≤ h ∨ x + y ≤ h + z) ↔ threshold x y z ≤ h := by
  have harith : x + y ≤ h + z ↔ x + y - z ≤ h := by
    constructor <;> intro hbound <;> linarith
  simp only [threshold, min_le_iff, harith]

/-- The budget threshold is necessary and sufficient, including equality. -/
theorem cover_threshold_iff (x y h z : ℝ) (hz : 0 ≤ z) :
    HasCover x y h z ↔ threshold x y z ≤ h :=
  (cover_iff x y h z hz).trans (criterion_iff_threshold x y h z)

theorem pruning_threshold_iff (x y h z : ℝ) :
    HasPruning x y h z ↔ threshold x y z ≤ h :=
  (pruning_iff x y h z).trans (criterion_iff_threshold x y h z)

/-- The exact minimum among all sixteen cover selections. -/
def minimumCoverCost (x y z : ℝ) : ℝ :=
  min (x + y) (min (x + z) (y + z))

theorem cover_cost_iff (x y z t : ℝ) (hz : 0 ≤ z) :
    (∃ r c zl zr : Bool,
      IsCover r c zl zr ∧ coverCost x y z r c zl zr ≤ t) ↔
    minimumCoverCost x y z ≤ t := by
  simp only [minimumCoverCost, min_le_iff]
  constructor
  · rintro ⟨r, c, zl, zr, hcover, hcost⟩
    cases r <;> cases c <;> cases zl <;> cases zr <;>
      simp [IsCover, coverCost] at hcover hcost <;>
      first | (left; linarith) | (right; left; linarith) | (right; right; linarith)
  · rintro (hxy | hxz | hyz)
    · refine ⟨true, true, false, false, ?_, ?_⟩
      · simp [IsCover]
      · simpa [coverCost] using hxy
    · refine ⟨true, false, true, false, ?_, ?_⟩
      · simp [IsCover]
      · simpa [coverCost] using hxz
    · refine ⟨false, true, false, true, ?_, ?_⟩
      · simp [IsCover]
      · simpa [coverCost] using hyz

theorem minimum_cover_is_attained (x y z : ℝ) (hz : 0 ≤ z) :
    ∃ r c zl zr : Bool,
      IsCover r c zl zr ∧ coverCost x y z r c zl zr = minimumCoverCost x y z := by
  obtain ⟨r, c, zl, zr, hcover, hupper⟩ :=
    (cover_cost_iff x y z (minimumCoverCost x y z) hz).mpr le_rfl
  have hlower : minimumCoverCost x y z ≤ coverCost x y z r c zl zr :=
    (cover_cost_iff x y z (coverCost x y z r c zl zr) hz).mp
      ⟨r, c, zl, zr, hcover, le_rfl⟩
  exact ⟨r, c, zl, zr, hcover, le_antisymm hupper hlower⟩

structure CoordinateWeights where
  a : ℝ
  b : ℝ
  c : ℝ
  d : ℝ

structure PairCosts where
  x : ℝ
  y : ℝ
  h : ℝ
  z : ℝ

def PositiveCoordinates (w : CoordinateWeights) : Prop :=
  0 < w.a ∧ 0 < w.b ∧ 0 < w.c ∧ 0 < w.d

def productCosts (w : CoordinateWeights) : PairCosts :=
  ⟨w.a * w.d, w.b * w.c, w.a * w.c, w.b * w.d⟩

def addCosts (u v : PairCosts) : PairCosts :=
  ⟨u.x + v.x, u.y + v.y, u.h + v.h, u.z + v.z⟩

noncomputable def firstSystem : CoordinateWeights := ⟨1 / 10, 1, 1, 1 / 10⟩
noncomputable def secondSystem : CoordinateWeights := ⟨1, 1 / 10, 1 / 10, 1⟩
noncomputable def summedCosts : PairCosts := addCosts (productCosts firstSystem) (productCosts secondSystem)

theorem both_systems_strictly_positive :
    PositiveCoordinates firstSystem ∧ PositiveCoordinates secondSystem := by
  norm_num [PositiveCoordinates, firstSystem, secondSystem]

theorem actual_summed_costs :
    summedCosts.x = 101 / 100 ∧ summedCosts.y = 101 / 100 ∧
    summedCosts.h = 1 / 5 ∧ summedCosts.z = 1 / 5 := by
  norm_num [summedCosts, addCosts, productCosts, firstSystem, secondSystem]

theorem actual_nonproduct_no_cover :
    ¬ HasCover (101 / 100) (101 / 100) (1 / 5) (1 / 5) := by
  rw [cover_iff _ _ _ _ (by norm_num)]
  norm_num

theorem actual_nonproduct_no_pruning :
    ¬ HasPruning (101 / 100) (101 / 100) (1 / 5) (1 / 5) := by
  rw [pruning_iff]
  norm_num

theorem actual_nonproduct_minimum :
    minimumCoverCost (101 / 100) (101 / 100) (1 / 5) = 121 / 100 := by
  norm_num [minimumCoverCost]

/-- Each positive product system has its own valid cover and pruning. -/
theorem each_component_is_feasible :
    HasCover (productCosts firstSystem).x (productCosts firstSystem).y
      (productCosts firstSystem).h (productCosts firstSystem).z ∧
    HasCover (productCosts secondSystem).x (productCosts secondSystem).y
      (productCosts secondSystem).h (productCosts secondSystem).z ∧
    HasPruning (productCosts firstSystem).x (productCosts firstSystem).y
      (productCosts firstSystem).h (productCosts firstSystem).z ∧
    HasPruning (productCosts secondSystem).x (productCosts secondSystem).y
      (productCosts secondSystem).h (productCosts secondSystem).z := by
  have hfirstz : 0 ≤ (productCosts firstSystem).z := by
    norm_num [productCosts, firstSystem]
  have hsecondz : 0 ≤ (productCosts secondSystem).z := by
    norm_num [productCosts, secondSystem]
  rw [cover_iff _ _ _ _ hfirstz, cover_iff _ _ _ _ hsecondz, pruning_iff, pruning_iff]
  norm_num [productCosts, firstSystem, secondSystem]

/-- The sum of the pair costs of two strictly positive product systems fails both criteria. -/
theorem two_positive_product_systems_fail :
    PositiveCoordinates firstSystem ∧ PositiveCoordinates secondSystem ∧
    ¬ HasCover summedCosts.x summedCosts.y summedCosts.h summedCosts.z ∧
    ¬ HasPruning summedCosts.x summedCosts.y summedCosts.h summedCosts.z := by
  obtain ⟨hx, hy, hh, hz⟩ := actual_summed_costs
  refine ⟨both_systems_strictly_positive.1, both_systems_strictly_positive.2, ?_, ?_⟩
  · rw [hx, hy, hh, hz]
    exact actual_nonproduct_no_cover
  · rw [hx, hy, hh, hz]
    exact actual_nonproduct_no_pruning

def epsilonSystem1 (ε : ℝ) : CoordinateWeights := ⟨ε, 1, 1, ε⟩
def epsilonSystem2 (ε : ℝ) : CoordinateWeights := ⟨1, ε, ε, 1⟩

theorem epsilon_systems_positive (ε : ℝ) (hε : 0 < ε) :
    PositiveCoordinates (epsilonSystem1 ε) ∧
      PositiveCoordinates (epsilonSystem2 ε) := by
  simp [PositiveCoordinates, epsilonSystem1, epsilonSystem2, hε]

theorem epsilon_summed_costs (ε : ℝ) :
    addCosts (productCosts (epsilonSystem1 ε)) (productCosts (epsilonSystem2 ε)) =
      (⟨1 + ε ^ 2, 1 + ε ^ 2, 2 * ε, 2 * ε⟩ : PairCosts) := by
  simp [addCosts, productCosts, epsilonSystem1, epsilonSystem2, pow_two]
  constructor <;> ring

/-- No finite common coefficient repairs either statement for sums of two
strictly positive product systems. All sixteen covers and four prunings
are handled with universally quantified real K and a positive witness. -/
theorem no_uniform_constant (K : ℝ) (hK : 0 ≤ K) :
    ∃ ε : ℝ, 0 < ε ∧ ε < 1 ∧
      (∀ r c zl zr : Bool, IsCover r c zl zr →
        K * (2 * ε + 2 * ε) <
          coverCost (1 + ε ^ 2) (1 + ε ^ 2) (2 * ε) r c zl zr) ∧
      (∀ deleteR deleteC : Bool, IsConflictFreePruning deleteR deleteC →
        K * (2 * ε + uncoveredCost (2 * ε) deleteR deleteC) <
          deletionCost (1 + ε ^ 2) (1 + ε ^ 2) deleteR deleteC) := by
  let ε : ℝ := (4 * (K + 1))⁻¹
  have hd : 0 < 4 * (K + 1) := by linarith
  have hε : 0 < ε := inv_pos.mpr hd
  have hid : (4 * (K + 1)) * ε = 1 := mul_inv_cancel₀ (ne_of_gt hd)
  have hsmall : ε < 1 := by nlinarith
  have hcoverBudget : K * (2 * ε + 2 * ε) < 1 := by nlinarith
  have hpruneBudget : K * (2 * ε) < 1 := by nlinarith
  refine ⟨ε, hε, hsmall, ?_, ?_⟩
  · intro r c zl zr hcover
    cases r <;> cases c <;> cases zl <;> cases zr <;>
      simp [IsCover, coverCost] at hcover ⊢ <;> nlinarith [sq_nonneg ε]
  · intro deleteR deleteC hfree
    cases deleteR <;> cases deleteC <;>
      simp [IsConflictFreePruning, deletionCost, uncoveredCost] at hfree ⊢ <;>
      nlinarith [sq_nonneg ε]

/-- The unbounded obstruction expressed directly as actual coordinate systems,
including their strict positivity and their summed pair-cost construction. -/
theorem no_uniform_constant_positive_systems (K : ℝ) (hK : 0 ≤ K) :
    ∃ u v : CoordinateWeights, PositiveCoordinates u ∧ PositiveCoordinates v ∧
      let w := addCosts (productCosts u) (productCosts v)
      (∀ r c zl zr : Bool, IsCover r c zl zr →
        K * (w.h + w.z) < coverCost w.x w.y w.z r c zl zr) ∧
      (∀ deleteR deleteC : Bool, IsConflictFreePruning deleteR deleteC →
        K * (w.h + uncoveredCost w.z deleteR deleteC) <
          deletionCost w.x w.y deleteR deleteC) := by
  obtain ⟨ε, hε, _, hcover, hprune⟩ := no_uniform_constant K hK
  obtain ⟨hfirst, hsecond⟩ := epsilon_systems_positive ε hε
  refine ⟨epsilonSystem1 ε, epsilonSystem2 ε, hfirst, hsecond, ?_⟩
  dsimp only
  rw [epsilon_summed_costs]
  exact ⟨hcover, hprune⟩

end RectangularPruning.SingleConflictReal

#print axioms RectangularPruning.SingleConflictReal.cover_iff
#print axioms RectangularPruning.SingleConflictReal.pruning_iff
#print axioms RectangularPruning.SingleConflictReal.cover_iff_pruning
#print axioms RectangularPruning.SingleConflictReal.cover_threshold_iff
#print axioms RectangularPruning.SingleConflictReal.pruning_threshold_iff
#print axioms RectangularPruning.SingleConflictReal.cover_cost_iff
#print axioms RectangularPruning.SingleConflictReal.minimum_cover_is_attained
#print axioms RectangularPruning.SingleConflictReal.both_systems_strictly_positive
#print axioms RectangularPruning.SingleConflictReal.actual_summed_costs
#print axioms RectangularPruning.SingleConflictReal.actual_nonproduct_no_cover
#print axioms RectangularPruning.SingleConflictReal.actual_nonproduct_no_pruning
#print axioms RectangularPruning.SingleConflictReal.actual_nonproduct_minimum
#print axioms RectangularPruning.SingleConflictReal.each_component_is_feasible
#print axioms RectangularPruning.SingleConflictReal.two_positive_product_systems_fail
#print axioms RectangularPruning.SingleConflictReal.epsilon_summed_costs
#print axioms RectangularPruning.SingleConflictReal.no_uniform_constant
#print axioms RectangularPruning.SingleConflictReal.no_uniform_constant_positive_systems
