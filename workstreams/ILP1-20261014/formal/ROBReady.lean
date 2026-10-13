import ROBWorkBounds

/-!
# Readiness persistence and forced non-delay actions in actual ROB states

The coherent-state invariant is proved for every state of every ROBTrace.
Finite ready/completed/hole counts use genuine duplicate-free Fin n lists.
No optimum-continuation or macro-DP recurrence is assumed or proved here.
-/

namespace ILP1.ROBReady

open ROBWorkBounds

noncomputable def selected {n : Nat} (p : Fin n → Prop) : List (Fin n) := by
  classical
  exact (List.finRange n).filter (fun i => decide (p i))

noncomputable def count {n : Nat} (p : Fin n → Prop) : Nat := (selected p).length

theorem mem_selected {n : Nat} (p : Fin n → Prop) (i : Fin n) :
    i ∈ selected p ↔ p i := by
  classical
  simp [selected, List.mem_finRange]

theorem selected_nodup {n : Nat} (p : Fin n → Prop) : (selected p).Nodup := by
  classical
  exact List.Nodup.sublist List.filter_sublist (List.nodup_finRange n)

theorem count_congr {n : Nat} {p q : Fin n → Prop} (h : ∀ i, p i ↔ q i) :
    count p = count q := by
  have heq : p = q := funext (fun i => propext (h i))
  rw [heq]

theorem count_true (n : Nat) : count (fun _ : Fin n => True) = n := by
  classical
  have heq : selected (fun _ : Fin n => True) = List.finRange n := by
    apply List.filter_eq_self.mpr
    intro i hi
    simp
  simp only [count, heq, List.length_finRange]

theorem count_le_n {n : Nat} (p : Fin n → Prop) : count p ≤ n := by
  classical
  have h := List.length_filter_le (fun i : Fin n => decide (p i)) (List.finRange n)
  simpa only [count, selected, List.length_finRange] using h

theorem count_strict_inclusion {n : Nat} {p q : Fin n → Prop}
    (hsub : ∀ i, p i → q i) (i : Fin n) (hi : q i) (hnot : ¬ p i) :
    count p + 1 ≤ count q := by
  have hnd : (i :: selected p).Nodup := by
    exact List.nodup_cons.mpr ⟨fun hm => hnot ((mem_selected p i).1 hm), selected_nodup p⟩
  have hs : i :: selected p ⊆ selected q := by
    intro j hj
    rcases List.mem_cons.mp hj with heq | hm
    · subst j
      exact (mem_selected q i).2 hi
    · exact (mem_selected q j).2 (hsub j ((mem_selected p j).1 hm))
  simpa only [List.length_cons, count] using hnd.length_le_of_subset hs

theorem inclusion_count_eq_iff {n : Nat} {p q : Fin n → Prop}
    (hsub : ∀ i, p i → q i) : count p = count q ↔ ∀ i, p i ↔ q i := by
  constructor
  · intro heq i
    refine ⟨hsub i, ?_⟩
    intro hi
    apply Classical.byContradiction
    intro hnot
    have h := count_strict_inclusion hsub i hi hnot
    omega
  · exact count_congr

theorem count_partition {n : Nat} (p q : Fin n → Prop) :
    count (fun i => p i ∧ q i) + count (fun i => p i ∧ ¬ q i) = count p := by
  classical
  have aux : ∀ xs : List (Fin n),
      (xs.filter (fun i => decide (p i ∧ q i))).length +
      (xs.filter (fun i => decide (p i ∧ ¬ q i))).length =
      (xs.filter (fun i => decide (p i))).length := by
    intro xs
    induction xs with
    | nil => simp
    | cons i xs ih =>
      by_cases hp : p i <;> by_cases hq : q i <;>
        simp_all [Nat.add_assoc, Nat.add_comm, Nat.add_left_comm]
  simpa [count, selected] using aux (List.finRange n)

theorem count_prefix {n r : Nat} (hr : r ≤ n) : count (fun i : Fin n => i.val < r) = r := by
  let p : Fin n → Prop := fun i => i.val < r
  have hu := list_injection_length_le (selected p) (List.range r) Fin.val (selected_nodup p)
    (fun _ _ _ _ h => Fin.ext h)
    (fun i hi => List.mem_range.mpr ((mem_selected p i).1 hi))
  have hs : List.range r ⊆ (selected p).map Fin.val := by
    intro i hi
    have hir := List.mem_range.mp hi
    have hin : i < n := by omega
    exact List.mem_map.mpr ⟨⟨i, hin⟩, (mem_selected p ⟨i, hin⟩).2 hir, rfl⟩
  have hl := List.nodup_range.length_le_of_subset hs
  simp only [List.length_map, List.length_range] at hu hl
  change (selected p).length = r
  omega

/-- Exact structural facts obeyed by every reachable eager ROB state. -/
structure Coherent {n : Nat} (b : Nat) (s : ROBState n) : Prop where
  retirement : CompletedPrefix s.completed s.retired
  admission : s.admitted = min n (s.retired + b)
  completed_admitted : ∀ i, s.completed i → i.val < s.admitted

theorem trace_coherent {n b w : Nat} {dep : Dependency n} {t : TimeAssignment n}
    (tr : ROBTrace dep b w t) (c : Nat) : Coherent b (tr.state c) := by
  have hp := trace_retirementPrefix tr c
  refine ⟨?_, trace_admitted tr c, ?_⟩
  · refine ⟨hp.1, ?_, ?_⟩
    · intro i hi
      exact (trace_completed_iff tr c i).2 (hp.2.1 i hi)
    · intro hr hi
      have hl := (trace_completed_iff tr c ⟨(tr.state c).retired, hr⟩).1 hi
      have hu := hp.2.2 hr
      omega
  · intro i hi
    have htime := (trace_completed_iff tr c i).1 hi
    have hu : i.val < (tr.state c).retired + b := by
      apply Classical.byContradiction
      intro hnot
      have hrn : (tr.state c).retired < n := by have := i.isLt; omega
      have hedge := ((windowEdges_iff_canonicalROB t b).2 (trace_legal tr).2.1)
        ⟨(tr.state c).retired, hrn⟩ i (by change (tr.state c).retired + b ≤ i.val; omega)
      have hrtime := hp.2.2 hrn
      omega
    rw [trace_admitted tr c]
    exact Nat.lt_min.mpr ⟨i.isLt, hu⟩

theorem retired_mono {n b : Nat} {s s' : ROBState n}
    (hs : Coherent b s) (hs' : Coherent b s')
    (hsub : ∀ i, s.completed i → s'.completed i) : s.retired ≤ s'.retired := by
  apply Classical.byContradiction
  intro hnot
  have hrn : s'.retired < n := by have := hs.retirement.1; omega
  have ho := hs.retirement.2.1 ⟨s'.retired, hrn⟩ (by change s'.retired < s.retired; omega)
  exact hs'.retirement.2.2 hrn (hsub _ ho)

/-- An uncompleted ready job remains ready after any coherent completion
superset. This includes admission, retirement and true predecessor readiness. -/
theorem canIssue_mono {n b : Nat} {dep : Dependency n} {s s' : ROBState n}
    (hs : Coherent b s) (hs' : Coherent b s')
    (hsub : ∀ i, s.completed i → s'.completed i) (i : Fin n)
    (hi : CanIssue dep s i) (hnot : ¬ s'.completed i) : CanIssue dep s' i := by
  have hr := retired_mono hs hs' hsub
  refine ⟨?_, ?_, hnot, fun j hj => hsub j (hi.2.2.2 j hj)⟩
  · apply Classical.byContradiction
    intro hlt
    exact hnot (hs'.retirement.2.1 i (by omega))
  · have hu := hi.2.1
    rw [hs.admission] at hu
    have hh : i.val < s.retired + b := Nat.lt_of_lt_of_le hu (Nat.min_le_right _ _)
    rw [hs'.admission]
    exact Nat.lt_min.mpr ⟨i.isLt, by omega⟩

theorem trace_canIssue_mono {n b w w' : Nat} {dep : Dependency n}
    {t t' : TimeAssignment n} (tr : ROBTrace dep b w t) (tr' : ROBTrace dep b w' t')
    (c c' : Nat) (hsub : ∀ i, (tr.state c).completed i → (tr'.state c').completed i)
    (i : Fin n) (hi : CanIssue dep (tr.state c) i) (hnot : ¬ (tr'.state c').completed i) :
    CanIssue dep (tr'.state c') i :=
  canIssue_mono (trace_coherent tr c) (trace_coherent tr' c') hsub i hi hnot

noncomputable def completedCountOfState {n : Nat} (s : ROBState n) : Nat := count s.completed

def Hole {n : Nat} (s : ROBState n) (i : Fin n) : Prop := s.completed i ∧ s.retired ≤ i.val

noncomputable def holeCount {n : Nat} (s : ROBState n) : Nat := count (Hole s)

noncomputable def readyCount {n : Nat} (dep : Dependency n) (s : ROBState n) : Nat :=
  count (CanIssue dep s)

theorem hole_count_identity {n b : Nat} {s : ROBState n} (hs : Coherent b s) :
    holeCount s + s.retired = completedCountOfState s := by
  have hp := count_partition s.completed (fun i => i.val < s.retired)
  have hl : count (fun i => s.completed i ∧ i.val < s.retired) = s.retired := by
    calc
      _ = count (fun i : Fin n => i.val < s.retired) := count_congr (fun i =>
        ⟨fun h => h.2, fun h => ⟨hs.retirement.2.1 i h, h⟩⟩)
      _ = s.retired := count_prefix hs.retirement.1
  have hh : count (fun i => s.completed i ∧ ¬ i.val < s.retired) = holeCount s := by
    apply count_congr
    intro i
    unfold Hole
    constructor <;> rintro ⟨hcomp, hcut⟩ <;> exact ⟨hcomp, by omega⟩
  rw [hl, hh] at hp
  change holeCount s + s.retired = count s.completed
  omega

theorem hole_count_eq_sub {n b : Nat} {s : ROBState n} (hs : Coherent b s) :
    holeCount s = completedCountOfState s - s.retired := by
  have h := hole_count_identity hs
  omega

/-- Ready jobs and completed-unretired holes are disjoint occupants of B
window positions, giving the actual ready+holes capacity bound. -/
theorem ready_plus_holes_le {n b : Nat} {dep : Dependency n} {s : ROBState n}
    (hs : Coherent b s) : readyCount dep s + holeCount s ≤ b := by
  let xs := selected (CanIssue dep s) ++ selected (Hole s)
  have hnd : xs.Nodup := by
    apply List.nodup_append.mpr
    refine ⟨selected_nodup _, selected_nodup _, ?_⟩
    intro i hi j hj heq
    have hri := (mem_selected (CanIssue dep s) i).1 hi
    have hhj := (mem_selected (Hole s) j).1 hj
    subst j
    exact hri.2.2.1 hhj.1
  have hwindow : ∀ i, i ∈ xs → s.retired ≤ i.val ∧ i.val < s.retired + b := by
    intro i hi
    have hib : s.admitted ≤ s.retired + b := by rw [hs.admission]; exact Nat.min_le_right _ _
    rcases List.mem_append.mp hi with hi | hi
    · have hri := (mem_selected (CanIssue dep s) i).1 hi
      exact ⟨hri.1, Nat.lt_of_lt_of_le hri.2.1 hib⟩
    · have hhi := (mem_selected (Hole s) i).1 hi
      exact ⟨hhi.2, Nat.lt_of_lt_of_le (hs.completed_admitted i hhi.1) hib⟩
  have hlen := list_injection_length_le xs (List.range b) (fun i => i.val - s.retired) hnd ?_ ?_
  · simpa only [xs, List.length_append, List.length_range, readyCount, holeCount, count] using hlen
  · intro i hi j hj hij
    have hwi := hwindow i hi
    have hwj := hwindow j hj
    apply Fin.ext
    omega
  · intro i hi
    have hwi := hwindow i hi
    apply List.mem_range.mpr
    omega

theorem ready_le_width_of_holes {n w excess : Nat} {dep : Dependency n} {s : ROBState n}
    (hs : Coherent (w + excess) s) (hh : excess ≤ holeCount s) : readyCount dep s ≤ w := by
  have h := ready_plus_holes_le (dep := dep) hs
  omega

theorem trace_ready_le_width_of_holes {n w excess : Nat} {dep : Dependency n}
    {t : TimeAssignment n} (tr : ROBTrace dep (w + excess) w t) (c : Nat)
    (hh : excess ≤ holeCount (tr.state c)) : readyCount dep (tr.state c) ≤ w :=
  ready_le_width_of_holes (trace_coherent tr c) hh

theorem count_pos_iff {n : Nat} (p : Fin n → Prop) : 0 < count p ↔ ∃ i, p i := by
  constructor
  · intro h
    obtain ⟨i, hi⟩ := List.length_pos_iff_exists_mem.mp h
    exact ⟨i, (mem_selected p i).1 hi⟩
  · rintro ⟨i, hi⟩
    exact List.length_pos_iff_exists_mem.mpr ⟨i, (mem_selected p i).2 hi⟩

/-- The finite-cardinality capacity test itself supplies actual issue lanes. -/
theorem batchWidth_of_count_le {n w : Nat} (action : Fin n → Prop)
    (hcount : count action ≤ w) : BatchWidth action w := by
  let xs := selected action
  refine ⟨fun i => xs.idxOf i, ?_, ?_⟩
  · intro i hi
    have hm : i ∈ xs := (mem_selected action i).2 hi
    have hl := List.idxOf_lt_length_of_mem hm
    change xs.length ≤ w at hcount
    change xs.idxOf i < w
    omega
  · intro i j hi hj heq
    have hmi : i ∈ xs := (mem_selected action i).2 hi
    have hmj : j ∈ xs := (mem_selected action j).2 hj
    have hi' := List.getElem_idxOf (List.idxOf_lt_length_of_mem hmi)
    have hj' := List.getElem_idxOf (List.idxOf_lt_length_of_mem hmj)
    change xs.idxOf i = xs.idxOf j at heq
    simp only [heq] at hi'
    exact hi'.symm.trans hj'

/-- A non-delay action chooses as many actually ready jobs as capacity allows.
It specifies cardinality, not a hidden priority or an optimum assumption. -/
def NonDelay {n : Nat} (dep : Dependency n) (w : Nat) (s : ROBState n)
    (action : Fin n → Prop) : Prop :=
  (∀ i, action i → CanIssue dep s i) ∧ count action = min w (readyCount dep s)

theorem nonDelay_batchWidth {n w : Nat} {dep : Dependency n} {s : ROBState n}
    {action : Fin n → Prop} (h : NonDelay dep w s action) : BatchWidth action w := by
  apply batchWidth_of_count_le
  rw [h.2]
  exact Nat.min_le_left _ _

/-- If readiness fits within capacity, non-delay has exactly one action. -/
theorem nonDelay_iff_all_ready {n w : Nat} {dep : Dependency n} {s : ROBState n}
    (hr : readyCount dep s ≤ w) (action : Fin n → Prop) :
    NonDelay dep w s action ↔ ∀ i, action i ↔ CanIssue dep s i := by
  constructor
  · intro h
    apply (inclusion_count_eq_iff h.1).1
    exact h.2.trans (Nat.min_eq_right hr)
  · intro h
    refine ⟨fun i hi => (h i).1 hi, ?_⟩
    rw [Nat.min_eq_right hr]
    exact count_congr h

theorem nonDelay_unique_of_holes {n w excess : Nat} {dep : Dependency n}
    {s : ROBState n} (hs : Coherent (w + excess) s) (hh : excess ≤ holeCount s)
    {a a' : Fin n → Prop} (ha : NonDelay dep w s a) (ha' : NonDelay dep w s a') :
    ∀ i, a i ↔ a' i := by
  have hr := ready_le_width_of_holes (dep := dep) hs hh
  intro i
  exact ((nonDelay_iff_all_ready hr a).1 ha i).trans ((nonDelay_iff_all_ready hr a').1 ha' i).symm

theorem trace_nonDelay_unique_of_holes {n w excess : Nat} {dep : Dependency n}
    {t : TimeAssignment n} (tr : ROBTrace dep (w + excess) w t) (c : Nat)
    (hh : excess ≤ holeCount (tr.state c)) {a a' : Fin n → Prop}
    (ha : NonDelay dep w (tr.state c) a) (ha' : NonDelay dep w (tr.state c) a') :
    ∀ i, a i ↔ a' i := nonDelay_unique_of_holes (trace_coherent tr c) hh ha ha'

theorem trace_branching_requires_few_holes {n w excess : Nat} {dep : Dependency n}
    {t : TimeAssignment n} (tr : ROBTrace dep (w + excess) w t) (c : Nat)
    {a a' : Fin n → Prop} (ha : NonDelay dep w (tr.state c) a)
    (ha' : NonDelay dep w (tr.state c) a') (hne : ∃ i, ¬ (a i ↔ a' i)) :
    holeCount (tr.state c) < excess := by
  apply Classical.byContradiction
  intro hnot
  obtain ⟨i, hi⟩ := hne
  exact hi (trace_nonDelay_unique_of_holes tr c (by omega) ha ha' i)

theorem zero_holes_iff_prefix {n b : Nat} {s : ROBState n} (hs : Coherent b s) :
    holeCount s = 0 ↔ ∀ i, s.completed i ↔ i.val < s.retired := by
  constructor
  · intro hh i
    refine ⟨?_, hs.retirement.2.1 i⟩
    intro hi
    apply Classical.byContradiction
    intro hnot
    have hpos : 0 < holeCount s := (count_pos_iff (Hole s)).2 ⟨i, hi, by omega⟩
    omega
  · intro h
    apply Classical.byContradiction
    intro hnot
    have hpos : 0 < holeCount s := by omega
    obtain ⟨i, hi⟩ := (count_pos_iff (Hole s)).1 hpos
    have hlt := (h i).1 hi.1
    have hge := hi.2
    omega

/-- For B=W+1, a non-prefix actual state has a unique non-delay action. -/
theorem trace_nonprefix_forced {n w : Nat} {dep : Dependency n}
    {t : TimeAssignment n} (tr : ROBTrace dep (w + 1) w t) (c : Nat)
    (hnonprefix : ¬ ∀ i, (tr.state c).completed i ↔ i.val < (tr.state c).retired)
    (action : Fin n → Prop) :
    NonDelay dep w (tr.state c) action ↔ ∀ i, action i ↔ CanIssue dep (tr.state c) i := by
  have hh : 1 ≤ holeCount (tr.state c) := by
    have hz := (zero_holes_iff_prefix (trace_coherent tr c)).1
    apply Classical.byContradiction
    intro hnot
    exact hnonprefix (hz (by omega))
  exact nonDelay_iff_all_ready (trace_ready_le_width_of_holes tr c hh) action

theorem oldest_ready {n b : Nat} {dep : Dependency n} {s : ROBState n}
    (hforward : Forward dep) (hb : 0 < b) (hs : Coherent b s)
    (hrn : s.retired < n) : CanIssue dep s ⟨s.retired, hrn⟩ := by
  refine ⟨Nat.le_refl _, ?_, hs.retirement.2.2 hrn, ?_⟩
  · rw [hs.admission]
    change s.retired < min n (s.retired + b)
    exact Nat.lt_min.mpr ⟨hrn, by omega⟩
  · intro i hi
    exact hs.retirement.2.1 i (hforward i _ hi)

theorem nonDelay_nonempty {n b w : Nat} {dep : Dependency n} {s : ROBState n}
    (hforward : Forward dep) (hb : 0 < b) (hw : 0 < w) (hs : Coherent b s)
    (hrn : s.retired < n) {action : Fin n → Prop} (ha : NonDelay dep w s action) :
    ∃ i, action i := by
  have hrpos : 0 < readyCount dep s :=
    (count_pos_iff (CanIssue dep s)).2 ⟨⟨s.retired, hrn⟩, oldest_ready hforward hb hs hrn⟩
  have hapos : 0 < count action := by
    rw [ha.2]
    exact Nat.lt_min.mpr ⟨hw, hrpos⟩
  exact (count_pos_iff action).1 hapos

/-- Every nonterminal non-delay actual step strictly increases completion. -/
theorem nonDelay_step_progress {n b w : Nat} {dep : Dependency n}
    {s next : ROBState n} {action : Fin n → Prop}
    (hforward : Forward dep) (hb : 0 < b) (hw : 0 < w) (hs : Coherent b s)
    (hrn : s.retired < n) (ha : NonDelay dep w s action)
    (step : ROBStep dep b w s action next) :
    completedCountOfState s + 1 ≤ completedCountOfState next := by
  obtain ⟨i, hi⟩ := nonDelay_nonempty hforward hb hw hs hrn ha
  exact count_strict_inclusion (fun j hj => (step.complete j).2 (Or.inl hj)) i
    ((step.complete i).2 (Or.inr hi)) (step.eligible i hi).2.2.1

theorem nonterminal_count_lt {n b : Nat} {s : ROBState n} (hs : Coherent b s)
    (hrn : s.retired < n) : completedCountOfState s < n := by
  have h := count_strict_inclusion (p := s.completed) (q := fun _ => True)
    (fun _ _ => True.intro) ⟨s.retired, hrn⟩ True.intro (hs.retirement.2.2 hrn)
  rw [count_true] at h
  exact h

/-- An arbitrary non-delay ROB trace finishes within N cycles.
This is a termination bound, not existence or optimality of such a trace. -/
theorem nonDelay_trace_terminates {n b w : Nat} {dep : Dependency n}
    {t : TimeAssignment n} (tr : ROBTrace dep b w t) (hforward : Forward dep)
    (hb : 0 < b) (hw : 0 < w)
    (hnd : ∀ c, NonDelay dep w (tr.state c) (fun i => t i = c)) :
    (tr.state n).retired = n := by
  have growth : ∀ c, (tr.state c).retired = n ∨ c ≤ completedCountOfState (tr.state c) := by
    intro c
    induction c with
    | zero => exact Or.inr (Nat.zero_le _)
    | succ c ih =>
      by_cases hd : (tr.state c).retired = n
      · apply Or.inl
        have hm := retired_mono (trace_coherent tr c) (trace_coherent tr (c + 1))
          (fun i hi => ((tr.step c).complete i).2 (Or.inl hi))
        have hu := (trace_coherent tr (c + 1)).retirement.1
        omega
      · have hrn : (tr.state c).retired < n := by
          have hu := (trace_coherent tr c).retirement.1
          omega
        have hc := ih.resolve_left hd
        have hp := nonDelay_step_progress hforward hb hw (trace_coherent tr c) hrn (hnd c) (tr.step c)
        exact Or.inr (by omega)
  rcases growth n with hd | hc
  · exact hd
  · apply Classical.byContradiction
    intro hd
    have hrn : (tr.state n).retired < n := by
      have hu := (trace_coherent tr n).retirement.1
      omega
    have hlt := nonterminal_count_lt (trace_coherent tr n) hrn
    omega

#print axioms count_strict_inclusion
#print axioms inclusion_count_eq_iff
#print axioms count_partition
#print axioms count_prefix
#print axioms trace_coherent
#print axioms retired_mono
#print axioms canIssue_mono
#print axioms trace_canIssue_mono
#print axioms hole_count_identity
#print axioms hole_count_eq_sub
#print axioms ready_plus_holes_le
#print axioms ready_le_width_of_holes
#print axioms trace_ready_le_width_of_holes
#print axioms batchWidth_of_count_le
#print axioms nonDelay_batchWidth
#print axioms nonDelay_iff_all_ready
#print axioms nonDelay_unique_of_holes
#print axioms trace_nonDelay_unique_of_holes
#print axioms trace_branching_requires_few_holes
#print axioms zero_holes_iff_prefix
#print axioms trace_nonprefix_forced
#print axioms oldest_ready
#print axioms nonDelay_nonempty
#print axioms nonDelay_step_progress
#print axioms nonDelay_trace_terminates

end ILP1.ROBReady
