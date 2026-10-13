import ROBOperational

/-! General resource identities for the first ROB model. No novelty claimed. -/

namespace ILP1

/-- At a fixed issue cycle, the offset from the retirement frontier is a
collision-free lane in `[0,B)`. Thus no ROB-legal batch has more than B jobs. -/
theorem canonicalROB_widthBound {n : Nat} {t : TimeAssignment n} {b : Nat}
    (h : CanonicalROB t b) : WidthBound t b := by
  refine ⟨fun i => i.val - retirementCount t (t i), ?_, ?_⟩
  · intro i
    change i.val - retirementCount t (t i) < b
    have hi := h i (retirementCount t (t i)) (retirementCount_spec t (t i))
    omega
  · intro i j ht hl
    have hi := h i (retirementCount t (t i)) (retirementCount_spec t (t i))
    have hj := h j (retirementCount t (t j)) (retirementCount_spec t (t j))
    simp only [ht] at hi hl
    apply Fin.ext
    omega

theorem legal_iff_when_width_ge_window {n : Nat} (dep : Dependency n)
    (t : TimeAssignment n) {b w : Nat} (hbw : b ≤ w) :
    Legal dep b w t ↔ Respects dep t ∧ CanonicalROB t b := by
  constructor
  · intro h
    exact ⟨h.1, h.2.1⟩
  · rintro ⟨hd, hb⟩
    exact ⟨hd, hb, width_mono hbw (canonicalROB_widthBound hb)⟩

theorem legal_width_cap {n : Nat} (dep : Dependency n)
    (t : TimeAssignment n) (b w : Nat) :
    Legal dep b w t ↔ Legal dep b (min b w) t := by
  constructor
  · intro h
    by_cases hbw : b ≤ w
    · rw [Nat.min_eq_left hbw]
      exact ⟨h.1, h.2.1, canonicalROB_widthBound h.2.1⟩
    · rw [Nat.min_eq_right (by omega)]
      exact h
  · intro h
    exact ⟨h.1, h.2.1, width_mono (Nat.min_le_right b w) h.2.2⟩

theorem feasible_width_cap {n : Nat} (dep : Dependency n) (b w k : Nat) :
    Feasible dep b w k ↔ Feasible dep b (min b w) k := by
  constructor
  · rintro ⟨t, h, hk⟩
    exact ⟨t, (legal_width_cap dep t b w).1 h, hk⟩
  · rintro ⟨t, h, hk⟩
    exact ⟨t, (legal_width_cap dep t b w).2 h, hk⟩

theorem optimal_width_cap {n : Nat} (dep : Dependency n) (b w k : Nat) :
    Optimal dep b w k ↔ Optimal dep b (min b w) k := by
  constructor
  · rintro ⟨hk, hmin⟩
    exact ⟨(feasible_width_cap dep b w k).1 hk,
      fun l hl => hmin l ((feasible_width_cap dep b w l).2 hl)⟩
  · rintro ⟨hk, hmin⟩
    exact ⟨(feasible_width_cap dep b w k).2 hk,
      fun l hl => hmin l ((feasible_width_cap dep b w l).1 hl)⟩

theorem canonicalROB_of_full_window {n : Nat} (t : TimeAssignment n)
    {b : Nat} (hnb : n ≤ b) : CanonicalROB t b := by
  apply (windowEdges_iff_canonicalROB t b).1
  intro i j hij
  have hjn := j.isLt
  omega

theorem legal_iff_when_full_window {n : Nat} (dep : Dependency n)
    (t : TimeAssignment n) {b w : Nat} (hnb : n ≤ b) :
    Legal dep b w t ↔ Respects dep t ∧ WidthBound t w := by
  constructor
  · intro h
    exact ⟨h.1, h.2.2⟩
  · rintro ⟨hd, hw⟩
    exact ⟨hd, canonicalROB_of_full_window t hnb, hw⟩

#print axioms canonicalROB_widthBound
#print axioms legal_iff_when_width_ge_window
#print axioms legal_width_cap
#print axioms feasible_width_cap
#print axioms optimal_width_cap
#print axioms canonicalROB_of_full_window
#print axioms legal_iff_when_full_window

end ILP1
