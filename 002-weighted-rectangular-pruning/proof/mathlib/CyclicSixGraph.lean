import CyclicSixCosts

/-!
# Actual covers and prunings on the full cyclic six-cycle pair

Original and corner coordinates each range over all nine pairs in `Fin 3`.
The graph has separately selected R, C, Z_L and Z_R families. `gridSum`
explicitly sums each of their nine costs exactly once. `Uncovered` uses
actual surviving neighbors. The theorem starts from every actual conflict,
not from an assumed aggregate cost inequality.

This file treats full original families. The partial-family extension and
the exact nine-candidate optimum of the written note remain separate.
-/

namespace RectangularPruning.CyclicSixGraph

open RectangularPruning.CyclicSixCosts

abbrev Selection := Fin 3 → Fin 3 → Bool

def edge (p i : Fin 3) : Prop := i = p ∨ i = p + 1

def gridSum (f : Fin 3 → Fin 3 → ℝ) : ℝ := total (fun i => total (f i))

def ActualLocal (X Y H Z : Fin 3 → ℝ) : Prop :=
  ∀ p i s j, edge p i → edge s j →
    X (j - p) * Y (s - i) ≤ H (s - p) * Z (j - i)

private theorem sub_next (s p : Fin 3) : s - (p + 1) = (s - p) - 1 :=
  (by decide : ∀ s p : Fin 3, s - (p + 1) = (s - p) - 1) s p

private theorem next_sub (s p : Fin 3) : s + 1 - p = (s - p) + 1 :=
  (by decide : ∀ s p : Fin 3, s + 1 - p = (s - p) + 1) s p

private theorem next_sub_next (s p : Fin 3) : s + 1 - (p + 1) = s - p :=
  (by decide : ∀ s p : Fin 3, s + 1 - (p + 1) = s - p) s p

private theorem sub_zero (d : Fin 3) : d - 0 = d :=
  (by decide : ∀ d : Fin 3, d - 0 = d) d

private theorem next_sub_one (d : Fin 3) : d + 1 - 1 = d :=
  (by decide : ∀ d : Fin 3, d + 1 - 1 = d) d

/-- All thirty-six actual inequalities are equivalent to twelve orbit constraints. -/
theorem actual_local_iff (X Y H Z : Fin 3 → ℝ) :
    ActualLocal X Y H Z ↔ Local X Y H Z := by
  constructor
  · intro h d
    have h00 := h 0 0 d d (Or.inl rfl) (Or.inl rfl)
    have h11 := h 0 1 d (d + 1) (Or.inr (by decide)) (Or.inr rfl)
    have h01 := h 0 0 d (d + 1) (Or.inl rfl) (Or.inr rfl)
    have h10 := h 0 1 d d (Or.inr (by decide)) (Or.inl rfl)
    simpa only [sub_zero, next_sub_one] using
      And.intro h00 (And.intro h11 (And.intro h01 h10))
  · intro h p i s j hi hj
    rcases hi with hi | hi <;> rcases hj with hj | hj <;> rw [hi, hj]
    · exact (h (s - p)).1
    · simpa only [next_sub] using (h (s - p)).2.2.1
    · simpa only [sub_next] using (h (s - p)).2.2.2
    · rw [next_sub_next, next_sub, sub_next]
      exact (h (s - p)).2.1

def IsCover (r c zl zr : Selection) : Prop :=
  (∀ p i s j, edge p i → edge s j → r p j = true ∨ c i s = true) ∧
  (∀ p i j, edge p i → r p j = true ∨ zr i j = true) ∧
  (∀ i s j, edge s j → zl i j = true ∨ c i s = true)

def coverCost (X Y Z : Fin 3 → ℝ) (r c zl zr : Selection) : ℝ :=
  gridSum (fun p j => if r p j then X (j - p) else 0) +
  gridSum (fun i s => if c i s then Y (s - i) else 0) +
  gridSum (fun i j => if zl i j then Z (j - i) else 0) +
  gridSum (fun i j => if zr i j then Z (j - i) else 0)

def budget (H Z : Fin 3 → ℝ) : ℝ :=
  gridSum (fun p s => H (s - p)) + gridSum (fun i j => Z (j - i))

def all : Selection := fun _ _ => true
def none : Selection := fun _ _ => false

theorem gridSum_difference (f : Fin 3 → ℝ) :
    gridSum (fun i j => f (j - i)) = 3 * total f := by
  norm_num [gridSum, total]
  ring

theorem three_actual_covers :
    IsCover all all none none ∧ IsCover all none all none ∧
      IsCover none all none all := by
  simp [IsCover, all, none]

/-- An actual cover of the entire 36-vertex graph with the local-cost budget. -/
theorem exists_actual_cover (X Y H Z : Fin 3 → ℝ)
    (hX : ∀ d, 0 ≤ X d) (hY : ∀ d, 0 ≤ Y d)
    (hH : ∀ d, 0 ≤ H d) (hloc : ActualLocal X Y H Z) :
    ∃ r c zl zr : Selection, IsCover r c zl zr ∧
      coverCost X Y Z r c zl zr ≤ budget H Z := by
  have halt := local_cover_alternative X Y H Z hX hY hH
    ((actual_local_iff X Y H Z).mp hloc)
  rcases halt with hx | hy | hxy
  · refine ⟨all, none, all, none, three_actual_covers.2.1, ?_⟩
    simp only [coverCost, budget, all, none, ite_true, Bool.false_eq_true,
      ite_false, gridSum_difference]
    norm_num [gridSum, total]
    dsimp [total] at hx
    linarith
  · refine ⟨none, all, none, all, three_actual_covers.2.2, ?_⟩
    simp only [coverCost, budget, all, none, ite_true, Bool.false_eq_true,
      ite_false, gridSum_difference]
    norm_num [gridSum, total]
    dsimp [total] at hy
    linarith
  · refine ⟨all, all, none, none, three_actual_covers.1, ?_⟩
    simp only [coverCost, budget, all, none, ite_true, Bool.false_eq_true,
      ite_false, gridSum_difference]
    norm_num [gridSum, total]
    dsimp [total] at hxy
    linarith

def ConflictFree (r c : Selection) : Prop :=
  ∀ p i s j, edge p i → edge s j → ¬ (r p j = true ∧ c i s = true)

def Uncovered (r c : Selection) (i j : Fin 3) : Prop :=
  (∀ p, edge p i → r p j = false) ∧ (∀ s, edge s j → c i s = false)

def deletionCost (X Y : Fin 3 → ℝ) (r c : Selection) : ℝ :=
  gridSum (fun p j => if r p j then 0 else X (j - p)) +
  gridSum (fun i s => if c i s then 0 else Y (s - i))

noncomputable def uncoveredCost (Z : Fin 3 → ℝ) (r c : Selection) : ℝ := by
  classical
  exact gridSum (fun i j => if Uncovered r c i j then Z (j - i) else 0)

theorem uncovered_none_none (i j : Fin 3) : Uncovered none none i j := by
  simp [Uncovered, none]

theorem not_uncovered_all_none (i j : Fin 3) : ¬ Uncovered all none i j := by
  intro h
  have hbad := h.1 i (Or.inl rfl)
  simp [all] at hbad

theorem not_uncovered_none_all (i j : Fin 3) : ¬ Uncovered none all i j := by
  intro h
  have hbad := h.2 j (Or.inl rfl)
  simp [all] at hbad

/-- Every full-input original has an actual opposite conflict witness. -/
theorem every_original_has_conflict :
    (∀ p j : Fin 3, ∃ i s, edge p i ∧ edge s j) ∧
    (∀ i s : Fin 3, ∃ p j, edge p i ∧ edge s j) := by
  constructor
  · intro p j; exact ⟨p, j, Or.inl rfl, Or.inl rfl⟩
  · intro i s; exact ⟨i, s, Or.inl rfl, Or.inl rfl⟩

/-- Actual conflict-free survivors and their actual uncovered corner profit. -/
theorem exists_actual_pruning (X Y H Z : Fin 3 → ℝ)
    (hX : ∀ d, 0 ≤ X d) (hY : ∀ d, 0 ≤ Y d)
    (hH : ∀ d, 0 ≤ H d) (hloc : ActualLocal X Y H Z) :
    ∃ r c : Selection, ConflictFree r c ∧
      deletionCost X Y r c ≤
        gridSum (fun p s => H (s - p)) + uncoveredCost Z r c := by
  have halt := local_cover_alternative X Y H Z hX hY hH
    ((actual_local_iff X Y H Z).mp hloc)
  rcases halt with hx | hy | hxy
  · refine ⟨none, all, ?_, ?_⟩
    · simp [ConflictFree, none]
    · simp only [deletionCost, uncoveredCost, not_uncovered_none_all, ite_false,
        all, none, Bool.false_eq_true, ite_true, gridSum_difference]
      norm_num [gridSum, total]
      dsimp [total] at hx
      linarith
  · refine ⟨all, none, ?_, ?_⟩
    · simp [ConflictFree, none]
    · simp only [deletionCost, uncoveredCost, not_uncovered_all_none, ite_false,
        all, none, Bool.false_eq_true, ite_true, gridSum_difference]
      norm_num [gridSum, total]
      dsimp [total] at hy
      linarith
  · refine ⟨none, none, ?_, ?_⟩
    · simp [ConflictFree, none]
    · simp only [deletionCost, uncoveredCost, uncovered_none_none, ite_true,
        none, Bool.false_eq_true, ite_false, gridSum_difference]
      dsimp [total] at hxy ⊢
      linarith

private theorem gridSum_mono (f g : Fin 3 → Fin 3 → ℝ)
    (h : ∀ i j, f i j ≤ g i j) : gridSum f ≤ gridSum g := by
  dsimp [gridSum, total]
  linarith [h 0 0, h 0 1, h 0 2, h 1 0, h 1 1, h 1 2,
    h 2 0, h 2 1, h 2 2]

private theorem gridSum_add (f g : Fin 3 → Fin 3 → ℝ) :
    gridSum (fun i j => f i j + g i j) = gridSum f + gridSum g := by
  dsimp [gridSum, total]
  ring

private theorem bool_pair_cost (a b : Bool) (h : a = true ∨ b = true) :
    (1 : ℝ) ≤ (if a then 1 else 0) + (if b then 1 else 0) := by
  cases a <;> cases b <;> simp_all

/-- The two disjoint diagonal coverage matchings force eighteen unit-cost vertices. -/
theorem unit_cover_lower_bound (r c zl zr : Selection) (h : IsCover r c zl zr) :
    18 ≤ coverCost (fun _ => 1) (fun _ => 1) (fun _ => 1) r c zl zr := by
  have hl := gridSum_mono (fun _ _ => (1 : ℝ))
    (fun i j => (if r i j then 1 else 0) + (if zr i j then 1 else 0))
    (fun i j => bool_pair_cost _ _ (h.2.1 i i j (Or.inl rfl)))
  have hr := gridSum_mono (fun _ _ => (1 : ℝ))
    (fun i j => (if zl i j then 1 else 0) + (if c i j then 1 else 0))
    (fun i j => bool_pair_cost _ _ (h.2.2 i j j (Or.inl rfl)))
  rw [gridSum_add] at hl hr
  norm_num [gridSum, total] at hl hr
  dsimp [coverCost, gridSum, total]
  linarith

/-- The coefficient-one bound is attained on actual unit costs. -/
theorem unit_cover_sharp :
    ActualLocal (fun _ => 1) (fun _ => 1) (fun _ => 1) (fun _ => 1) ∧
    IsCover all all none none ∧
    coverCost (fun _ => 1) (fun _ => 1) (fun _ => 1) all all none none = 18 ∧
    budget (fun _ => 1) (fun _ => 1) = 18 := by
  refine ⟨?_, three_actual_covers.1, ?_, ?_⟩
  · intro p i s j _ _; norm_num
  · norm_num [coverCost, gridSum, total, all, none]
  · norm_num [budget, gridSum, total]

/-- No coefficient smaller than one bounds all these actual covers. -/
theorem no_smaller_cover_coefficient (K : ℝ) (hK : K < 1)
    (r c zl zr : Selection) (h : IsCover r c zl zr) :
    K * budget (fun _ => 1) (fun _ => 1) <
      coverCost (fun _ => 1) (fun _ => 1) (fun _ => 1) r c zl zr := by
  have hlower := unit_cover_lower_bound r c zl zr h
  rw [unit_cover_sharp.2.2.2]
  linarith

end RectangularPruning.CyclicSixGraph

#print axioms RectangularPruning.CyclicSixGraph.actual_local_iff
#print axioms RectangularPruning.CyclicSixGraph.gridSum_difference
#print axioms RectangularPruning.CyclicSixGraph.three_actual_covers
#print axioms RectangularPruning.CyclicSixGraph.exists_actual_cover
#print axioms RectangularPruning.CyclicSixGraph.uncovered_none_none
#print axioms RectangularPruning.CyclicSixGraph.not_uncovered_all_none
#print axioms RectangularPruning.CyclicSixGraph.not_uncovered_none_all
#print axioms RectangularPruning.CyclicSixGraph.every_original_has_conflict
#print axioms RectangularPruning.CyclicSixGraph.exists_actual_pruning
#print axioms RectangularPruning.CyclicSixGraph.unit_cover_lower_bound
#print axioms RectangularPruning.CyclicSixGraph.unit_cover_sharp
#print axioms RectangularPruning.CyclicSixGraph.no_smaller_cover_coefficient
