import ROBOperational

/-!
# General finite work bounds from the actual lane-capacity predicate

All counts are lengths of duplicate-free filtered `List.finRange` lists.
The capacity proof maps jobs injectively into actual (cycle,lane) slots.
It does not assume a work inequality, or enumerate a bounded program class.
-/

namespace ILP1.ROBWorkBounds

/-- A general finite injection bound, using only bundled List theorems. -/
theorem list_injection_length_le {α β : Type} (xs : List α) (ys : List β)
    (f : α → β) (hn : xs.Nodup)
    (hinj : ∀ a, a ∈ xs → ∀ b, b ∈ xs → f a = f b → a = b)
    (hmem : ∀ a, a ∈ xs → f a ∈ ys) : xs.length ≤ ys.length := by
  have hmapped : (xs.map f).Nodup := by
    apply List.pairwise_map.mpr
    exact hn.imp_of_mem (fun ha hb hne heq => hne (hinj _ ha _ hb heq))
  have hsub : xs.map f ⊆ ys := by
    intro b hb
    obtain ⟨a, ha, rfl⟩ := List.mem_map.mp hb
    exact hmem a ha
  simpa only [List.length_map] using hmapped.length_le_of_subset hsub

def slots (cycles lanes : Nat) : List (Nat × Nat) :=
  (List.range cycles).flatMap (fun c => (List.range lanes).map (fun l => (c, l)))

theorem slots_length (cycles lanes : Nat) : (slots cycles lanes).length = cycles * lanes := by
  have aux : ∀ xs : List Nat,
      (xs.flatMap (fun c => (List.range lanes).map (fun l => (c, l)))).length = xs.length * lanes := by
    intro xs
    induction xs with
    | nil => simp
    | cons x xs ih => simp [List.flatMap_cons, ih, Nat.add_mul, Nat.add_comm]
  simpa only [slots, List.length_range] using aux (List.range cycles)

theorem mem_slots {c l cycles lanes : Nat} (hc : c < cycles) (hl : l < lanes) :
    (c, l) ∈ slots cycles lanes := by
  exact List.mem_flatMap.mpr ⟨c, List.mem_range.mpr hc,
    List.mem_map.mpr ⟨l, List.mem_range.mpr hl, rfl⟩⟩

def completedJobs {n : Nat} (t : TimeAssignment n) (c : Nat) : List (Fin n) :=
  (List.finRange n).filter (fun i => decide (t i < c))

def pendingJobs {n : Nat} (t : TimeAssignment n) (c : Nat) : List (Fin n) :=
  (List.finRange n).filter (fun i => decide (c ≤ t i))

def completedCount {n : Nat} (t : TimeAssignment n) (c : Nat) : Nat :=
  (completedJobs t c).length

theorem mem_completedJobs {n : Nat} (t : TimeAssignment n) (c : Nat) (i : Fin n) :
    i ∈ completedJobs t c ↔ t i < c := by
  simp [completedJobs, List.mem_finRange]

theorem mem_pendingJobs {n : Nat} (t : TimeAssignment n) (c : Nat) (i : Fin n) :
    i ∈ pendingJobs t c ↔ c ≤ t i := by
  simp [pendingJobs, List.mem_finRange]

theorem completedJobs_nodup {n : Nat} (t : TimeAssignment n) (c : Nat) :
    (completedJobs t c).Nodup :=
  List.Nodup.sublist List.filter_sublist (List.nodup_finRange n)

theorem pendingJobs_nodup {n : Nat} (t : TimeAssignment n) (c : Nat) :
    (pendingJobs t c).Nodup :=
  List.Nodup.sublist List.filter_sublist (List.nodup_finRange n)

theorem completed_pending_partition {n : Nat} (t : TimeAssignment n) (c : Nat) :
    completedCount t c + (pendingJobs t c).length = n := by
  have aux : ∀ xs : List (Fin n),
      (xs.filter (fun i => decide (t i < c))).length +
      (xs.filter (fun i => decide (c ≤ t i))).length = xs.length := by
    intro xs
    induction xs with
    | nil => simp
    | cons i xs ih =>
      by_cases hi : t i < c
      · have hn : ¬ c ≤ t i := by omega
        simp only [List.filter_cons, hi, hn, decide_true, decide_false,
          ite_true, Bool.false_eq_true, ite_false, List.length_cons]
        omega
      · have hc : c ≤ t i := by omega
        simp only [List.filter_cons, hi, hc, decide_true, decide_false,
          ite_true, Bool.false_eq_true, ite_false, List.length_cons]
        omega
  simpa only [completedCount, completedJobs, pendingJobs, List.length_finRange]
    using aux (List.finRange n)

/-- General capacity: completed jobs inject into c*W actual issue slots. -/
theorem completed_count_le {n w : Nat} {t : TimeAssignment n}
    (hw : WidthBound t w) (c : Nat) : completedCount t c ≤ c * w := by
  obtain ⟨lane, hlane, hinj⟩ := hw
  have hb := list_injection_length_le (completedJobs t c) (slots c w)
    (fun i => (t i, lane i)) (completedJobs_nodup t c)
    (fun i _ j _ heq => hinj i j (congrArg Prod.fst heq) (congrArg Prod.snd heq))
    (fun i hi => mem_slots ((mem_completedJobs t c i).1 hi) (hlane i))
  simpa only [completedCount, slots_length] using hb

theorem pending_count_le {n w horizon : Nat} {t : TimeAssignment n}
    (hw : WidthBound t w) (hfinish : ∀ i, t i < horizon) (c : Nat) :
    (pendingJobs t c).length ≤ (horizon - c) * w := by
  obtain ⟨lane, hlane, hinj⟩ := hw
  have hb := list_injection_length_le (pendingJobs t c) (slots (horizon - c) w)
    (fun i => (t i - c, lane i)) (pendingJobs_nodup t c) ?_ ?_
  · simpa only [slots_length] using hb
  · intro i hi j hj heq
    have hi' := (mem_pendingJobs t c i).1 hi
    have hj' := (mem_pendingJobs t c j).1 hj
    have htime := congrArg Prod.fst heq
    exact hinj i j (by omega) (congrArg Prod.snd heq)
  · intro i hi
    have hi' := (mem_pendingJobs t c i).1 hi
    have hfin := hfinish i
    exact mem_slots (by omega) (hlane i)

/-- Every individual cycle contains at most W distinct issued jobs. -/
theorem issued_count_le {n w : Nat} {t : TimeAssignment n}
    (hw : WidthBound t w) (c : Nat) :
    ((List.finRange n).filter (fun i => decide (t i = c))).length ≤ w := by
  obtain ⟨lane, hlane, hinj⟩ := hw
  let xs := (List.finRange n).filter (fun i => decide (t i = c))
  have hnd : xs.Nodup := List.Nodup.sublist List.filter_sublist (List.nodup_finRange n)
  have hb := list_injection_length_le xs (List.range w) lane hnd ?_ ?_
  · simpa only [List.length_range] using hb
  · intro i hi j hj hl
    have hi' : t i = c := by simpa [xs, List.mem_finRange] using hi
    have hj' : t j = c := by simpa [xs, List.mem_finRange] using hj
    exact hinj i j (hi'.trans hj'.symm) hl
  · intro i _
    exact List.mem_range.mpr (hlane i)

theorem horizon_mul_split {horizon c : Nat} (hc : c ≤ horizon) (w : Nat) :
    horizon * w = (horizon - c) * w + c * w := by
  calc
    horizon * w = ((horizon - c) + c) * w :=
      congrArg (fun k => k * w) (Nat.sub_add_cancel hc).symm
    _ = (horizon - c) * w + c * w := Nat.add_mul _ _ _

theorem completed_all {n : Nat} {t : TimeAssignment n} {c : Nat}
    (hfinish : ∀ i, t i < c) : completedCount t c = n := by
  have heq : completedJobs t c = List.finRange n := by
    apply List.filter_eq_self.mpr
    intro i _
    simpa only [decide_eq_true_eq] using hfinish i
  simp only [completedCount, heq, List.length_finRange]

/-- The arbitrary finite-program work bound is derived, not postulated. -/
theorem work_bound {n w horizon : Nat} {t : TimeAssignment n}
    (hw : WidthBound t w) (hfinish : ∀ i, t i < horizon) : n ≤ horizon * w := by
  have h := completed_count_le hw horizon
  rw [completed_all hfinish] at h
  exact h

/-- Finishing by H also limits how many issue slots can remain unused at
any earlier cut. Natural subtraction represents the truncated lower bound. -/
theorem completed_slack_lower {n w horizon : Nat} {t : TimeAssignment n}
    (hw : WidthBound t w) (hfinish : ∀ i, t i < horizon)
    (c : Nat) (hc : c ≤ horizon) :
    c * w - (horizon * w - n) ≤ completedCount t c := by
  have hwork := work_bound hw hfinish
  have hpartition := completed_pending_partition t c
  have hpending := pending_count_le hw hfinish c
  have hsplit := horizon_mul_split hc w
  omega

theorem feasible_work_bound {n b w horizon : Nat} {dep : Dependency n}
    (h : Feasible dep b w horizon) : n ≤ horizon * w := by
  obtain ⟨t, hlegal, hfinish⟩ := h
  exact work_bound hlegal.2.2 hfinish

/-- A true retired prefix is a subset of the actual completed list. -/
theorem retired_le_completed {n c r : Nat} {t : TimeAssignment n}
    (hp : RetirementPrefix t c r) : r ≤ completedCount t c := by
  have hsub : List.range r ⊆ (completedJobs t c).map Fin.val := by
    intro i hi
    have hir := List.mem_range.mp hi
    have hin : i < n := by have := hp.1; omega
    apply List.mem_map.mpr
    exact ⟨⟨i, hin⟩, (mem_completedJobs t c ⟨i, hin⟩).2 (hp.2.1 _ hir), rfl⟩
  have h := List.nodup_range.length_le_of_subset hsub
  simpa only [List.length_range, List.length_map, completedCount] using h

theorem retirement_work_bound {n c r w : Nat} {t : TimeAssignment n}
    (hw : WidthBound t w) (hp : RetirementPrefix t c r) : r ≤ c * w :=
  Nat.le_trans (retired_le_completed hp) (completed_count_le hw c)

theorem trace_completed_list {n b w : Nat} {dep : Dependency n}
    {t : TimeAssignment n} (tr : ROBTrace dep b w t) (c : Nat) (i : Fin n) :
    i ∈ completedJobs t c ↔ (tr.state c).completed i :=
  (mem_completedJobs t c i).trans (trace_completed_iff tr c i).symm

theorem trace_completed_count_le {n b w : Nat} {dep : Dependency n}
    {t : TimeAssignment n} (tr : ROBTrace dep b w t) (c : Nat) :
    completedCount t c ≤ c * w := completed_count_le (trace_legal tr).2.2 c

theorem trace_retired_le {n b w : Nat} {dep : Dependency n}
    {t : TimeAssignment n} (tr : ROBTrace dep b w t) (c : Nat) :
    (tr.state c).retired ≤ c * w :=
  retirement_work_bound (trace_legal tr).2.2 (trace_retirementPrefix tr c)

theorem trace_admission_upper {n b w : Nat} {dep : Dependency n}
    {t : TimeAssignment n} (tr : ROBTrace dep b w t) (c : Nat) :
    (tr.state c).admitted ≤ min n (c * w + b) := by
  have hr := trace_retired_le tr c
  rw [trace_admitted tr c]
  apply Nat.le_min.mpr
  exact ⟨Nat.min_le_left _ _,
    Nat.le_trans (Nat.min_le_right _ _) (Nat.add_le_add_right hr b)⟩

theorem trace_work_bound {n b w horizon : Nat} {dep : Dependency n}
    {t : TimeAssignment n} (tr : ROBTrace dep b w t)
    (hfinish : (tr.state horizon).retired = n) : n ≤ horizon * w :=
  work_bound (trace_legal tr).2.2 ((trace_finished_iff tr horizon).1 hfinish)

#print axioms list_injection_length_le
#print axioms slots_length
#print axioms completed_pending_partition
#print axioms completed_count_le
#print axioms pending_count_le
#print axioms issued_count_le
#print axioms work_bound
#print axioms completed_slack_lower
#print axioms feasible_work_bound
#print axioms retired_le_completed
#print axioms retirement_work_bound
#print axioms trace_completed_list
#print axioms trace_completed_count_le
#print axioms trace_retired_le
#print axioms trace_admission_upper
#print axioms trace_work_bound

end ILP1.ROBWorkBounds
