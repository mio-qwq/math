import ROBOperational

/-!
The exact positive window demand of a fixed time assignment.

Jobs use zero-based `Fin n` indices. A reversal includes equal issue times:
for i<j with t(j)<=t(i), the demand is j-i+1. The seed demand 1 enforces the
positive-resource convention. The pure window theorem needs neither true
data-dependence feasibility nor a separately supplied finite horizon.
-/

namespace ILP1

/-- The assertion that `b` bounds every member of
`{1} union {j-i+1 | i<j and t(j)<=t(i)}`. -/
def FootprintBound {n : Nat} (t : TimeAssignment n) (b : Nat) : Prop :=
  1 ≤ b ∧ ∀ i j : Fin n, i.val < j.val → t j ≤ t i → j.val - i.val + 1 ≤ b

/-- Positive capacity plus all reversal-distance inequalities is exactly the
ROB window condition, including same-cycle reversals. -/
theorem canonicalROB_iff_reversal_bound {n : Nat} (t : TimeAssignment n)
    {b : Nat} (hb : 0 < b) :
    CanonicalROB t b ↔
      ∀ i j : Fin n, i.val < j.val → t j ≤ t i → j.val - i.val + 1 ≤ b := by
  rw [← windowEdges_iff_canonicalROB, windowEdges_iff_blockingDistance]
  constructor
  · intro h i j hij ht
    have hdist := h i j ht
    omega
  · intro h i j ht
    by_cases hij : i.val < j.val
    · have hdist := h i j hij ht
      omega
    · omega

theorem canonicalROB_positive_of_nonempty {n : Nat} (hn : 0 < n)
    {t : TimeAssignment n} {b : Nat} (h : CanonicalROB t b) : 0 < b := by
  have hp := (windowEdges_iff_blockingDistance t b).1
    ((windowEdges_iff_canonicalROB t b).2 h)
  have hdiag := hp ⟨0, hn⟩ ⟨0, hn⟩ (Nat.le_refl _)
  change 0 < 0 + b at hdiag
  omega

theorem canonicalROB_iff_footprintBound {n : Nat} (hn : 0 < n)
    (t : TimeAssignment n) (b : Nat) :
    CanonicalROB t b ↔ FootprintBound t b := by
  constructor
  · intro h
    have hb := canonicalROB_positive_of_nonempty hn h
    exact ⟨hb, (canonicalROB_iff_reversal_bound t hb).1 h⟩
  · rintro ⟨hb, hp⟩
    exact (canonicalROB_iff_reversal_bound t hb).2 hp

theorem footprintBound_mono {n : Nat} {t : TimeAssignment n} {a b : Nat}
    (hab : a ≤ b) (ha : FootprintBound t a) : FootprintBound t b := by
  exact ⟨Nat.le_trans ha.1 hab,
    fun i j hij ht => Nat.le_trans (ha.2 i j hij ht) hab⟩

theorem footprintBound_full {n : Nat} (t : TimeAssignment n) :
    FootprintBound t (max 1 n) := by
  refine ⟨Nat.le_max_left 1 n, ?_⟩
  intro i j hij ht
  have hj := j.isLt
  have hn := Nat.le_max_right 1 n
  omega

/-- `b` is the actual maximum: it bounds all demands and is itself a member
of the seeded finite set. This is stronger than merely being an upper bound. -/
def IsFootprintMax {n : Nat} (t : TimeAssignment n) (b : Nat) : Prop :=
  FootprintBound t b ∧
    (b = 1 ∨ ∃ i j : Fin n,
      i.val < j.val ∧ t j ≤ t i ∧ b = j.val - i.val + 1)

theorem footprint_max_exists {n : Nat} (t : TimeAssignment n) :
    ∃ b, IsFootprintMax t b := by
  classical
  obtain ⟨b, hb, hmin⟩ :=
    exists_least_nat (FootprintBound t) ⟨max 1 n, footprintBound_full t⟩
  refine ⟨b, hb, ?_⟩
  by_cases hb1 : b = 1
  · exact Or.inl hb1
  · apply Or.inr
    apply Classical.byContradiction
    intro hnone
    have hprev : FootprintBound t (b - 1) := by
      refine ⟨by have := hb.1; omega, ?_⟩
      intro i j hij ht
      have hle := hb.2 i j hij ht
      have hne : b ≠ j.val - i.val + 1 := by
        intro heq
        exact hnone ⟨i, j, hij, ht, heq⟩
      omega
    have := hmin (b - 1) hprev
    have := hb.1
    omega

theorem footprint_max_le_iff {n : Nat} {t : TimeAssignment n} {a b : Nat}
    (ha : IsFootprintMax t a) : a ≤ b ↔ FootprintBound t b := by
  constructor
  · intro hab
    exact footprintBound_mono hab ha.1
  · intro hb
    rcases ha.2 with hseed | ⟨i, j, hij, ht, heq⟩
    · simpa only [hseed] using hb.1
    · rw [heq]
      exact hb.2 i j hij ht

theorem footprint_max_unique {n : Nat} {t : TimeAssignment n} {a b : Nat}
    (ha : IsFootprintMax t a) (hb : IsFootprintMax t b) : a = b := by
  have hab := (footprint_max_le_iff ha).2 hb.1
  have hba := (footprint_max_le_iff hb).2 ha.1
  omega

/-- The unique seeded maximum. This definition is noncomputable; the theorem
does not claim an implementation of a fast maximum/resource optimizer. -/
noncomputable def footprint {n : Nat} (t : TimeAssignment n) : Nat :=
  Classical.choose (footprint_max_exists t)

theorem footprint_spec {n : Nat} (t : TimeAssignment n) :
    IsFootprintMax t (footprint t) :=
  Classical.choose_spec (footprint_max_exists t)

theorem footprint_positive {n : Nat} (t : TimeAssignment n) : 1 ≤ footprint t :=
  (footprint_spec t).1.1

theorem footprint_le_iff {n : Nat} (t : TimeAssignment n) (b : Nat) :
    footprint t ≤ b ↔ FootprintBound t b :=
  footprint_max_le_iff (footprint_spec t)

theorem footprint_le_program_length {n : Nat} (hn : 0 < n) (t : TimeAssignment n) :
    footprint t ≤ n := by
  apply (footprint_le_iff t n).2
  simpa only [Nat.max_eq_right hn] using footprintBound_full t

/-- The formula for the exact minimum ROB capacity of a nonempty schedule. -/
theorem canonicalROB_iff_footprint {n : Nat} (hn : 0 < n)
    (t : TimeAssignment n) (b : Nat) :
    CanonicalROB t b ↔ footprint t ≤ b := by
  rw [canonicalROB_iff_footprintBound hn, footprint_le_iff]

/-- Including n=0, the same equivalence holds when capacity is positive.
For n=0 and b=0 the ROB predicate is true while the seeded footprint is 1. -/
theorem canonicalROB_iff_footprint_of_positive {n : Nat}
    (t : TimeAssignment n) {b : Nat} (hb : 0 < b) :
    CanonicalROB t b ↔ footprint t ≤ b := by
  rw [footprint_le_iff, canonicalROB_iff_reversal_bound t hb]
  constructor
  · exact fun h => ⟨hb, h⟩
  · exact fun h => h.2

theorem legal_iff_footprint {n : Nat} (hn : 0 < n) (dep : Dependency n)
    (t : TimeAssignment n) (b w : Nat) :
    Legal dep b w t ↔ Respects dep t ∧ WidthBound t w ∧ footprint t ≤ b := by
  constructor
  · rintro ⟨hd, hb, hw⟩
    exact ⟨hd, hw, (canonicalROB_iff_footprint hn t b).1 hb⟩
  · rintro ⟨hd, hw, hb⟩
    exact ⟨hd, (canonicalROB_iff_footprint hn t b).2 hb, hw⟩

/-- With data legality and issue width fixed, the footprint is feasible and
every feasible window is at least as large. No schedule search is hidden here. -/
theorem fixed_schedule_minimum_window {n : Nat} (hn : 0 < n)
    {dep : Dependency n} {t : TimeAssignment n} {w : Nat}
    (hd : Respects dep t) (hw : WidthBound t w) :
    Legal dep (footprint t) w t ∧
      ∀ b, Legal dep b w t → footprint t ≤ b := by
  refine ⟨(legal_iff_footprint hn dep t (footprint t) w).2
    ⟨hd, hw, Nat.le_refl _⟩, ?_⟩
  intro b hlegal
  exact ((legal_iff_footprint hn dep t b w).1 hlegal).2.2

/-- Strictly program-order issue uses the smallest positive window. -/
theorem footprint_eq_one_of_strict_order {n : Nat} (t : TimeAssignment n)
    (h : ∀ i j : Fin n, i.val < j.val → t i < t j) : footprint t = 1 := by
  have hb : FootprintBound t 1 := by
    refine ⟨Nat.le_refl _, ?_⟩
    intro i j hij ht
    have := h i j hij
    omega
  have hle := (footprint_le_iff t 1).2 hb
  have hge := footprint_positive t
  omega

/-- The seed convention gives footprint 1 for the empty program. -/
theorem empty_footprint (t : TimeAssignment 0) : footprint t = 1 := by
  apply footprint_eq_one_of_strict_order
  intro i
  exact Fin.elim0 i

#print axioms canonicalROB_iff_reversal_bound
#print axioms canonicalROB_positive_of_nonempty
#print axioms canonicalROB_iff_footprintBound
#print axioms footprintBound_mono
#print axioms footprintBound_full
#print axioms footprint_max_exists
#print axioms footprint_max_le_iff
#print axioms footprint_max_unique
#print axioms footprint_spec
#print axioms footprint_positive
#print axioms footprint_le_iff
#print axioms footprint_le_program_length
#print axioms canonicalROB_iff_footprint
#print axioms canonicalROB_iff_footprint_of_positive
#print axioms legal_iff_footprint
#print axioms fixed_schedule_minimum_window
#print axioms footprint_eq_one_of_strict_order
#print axioms empty_footprint

end ILP1
