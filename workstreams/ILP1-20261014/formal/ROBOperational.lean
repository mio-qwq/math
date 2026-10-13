import ROBModel

/-!
An explicit cycle-transition model and its equivalence to `ILP1.Legal`.
Every cycle starts after eager admission. The issue batch completes at the
cycle boundary; all contiguous completed jobs retire; admission then fills
the ROB before the next cycle. This is the exact one-cycle-latency model.
-/

namespace ILP1

structure ROBState (n : Nat) where
  completed : Fin n → Prop
  retired : Nat
  admitted : Nat

def CompletedPrefix {n : Nat} (completed : Fin n → Prop) (r : Nat) : Prop :=
  r ≤ n ∧ (∀ i : Fin n, i.val < r → completed i) ∧
    (∀ h : r < n, ¬ completed ⟨r, h⟩)

theorem completedPrefix_iff {n : Nat} (t : TimeAssignment n) (c r : Nat) :
    CompletedPrefix (fun i => t i < c) r ↔ RetirementPrefix t c r := by
  constructor
  · rintro ⟨hr, hd, hu⟩
    exact ⟨hr, hd, fun h => Nat.le_of_not_lt (hu h)⟩
  · rintro ⟨hr, hd, hu⟩
    exact ⟨hr, hd, fun h => Nat.not_lt_of_ge (hu h)⟩

def BatchWidth {n : Nat} (issue : Fin n → Prop) (w : Nat) : Prop :=
  ∃ lane : Fin n → Nat,
    (∀ i, issue i → lane i < w) ∧
    (∀ i j, issue i → issue j → lane i = lane j → i = j)

def CanIssue {n : Nat} (dep : Dependency n) (s : ROBState n) (i : Fin n) : Prop :=
  s.retired ≤ i.val ∧ i.val < s.admitted ∧ ¬ s.completed i ∧
    ∀ j, dep j i → s.completed j

structure ROBStep {n : Nat} (dep : Dependency n) (b w : Nat)
    (s : ROBState n) (issue : Fin n → Prop) (next : ROBState n) : Prop where
  capacity : BatchWidth issue w
  eligible : ∀ i, issue i → CanIssue dep s i
  complete : ∀ i, next.completed i ↔ s.completed i ∨ issue i
  retire : CompletedPrefix next.completed next.retired
  admit : next.admitted = min n (next.retired + b)

/-- A trace issues exactly the jobs assigned to each natural-number cycle. -/
structure ROBTrace {n : Nat} (dep : Dependency n) (b w : Nat)
    (t : TimeAssignment n) where
  state : Nat → ROBState n
  initially_incomplete : ∀ i, ¬ (state 0).completed i
  initially_retired : (state 0).retired = 0
  initially_admitted : (state 0).admitted = min n b
  step : ∀ c, ROBStep dep b w (state c) (fun i => t i = c) (state (c + 1))

theorem trace_completed_iff {n : Nat} {dep : Dependency n} {b w : Nat}
    {t : TimeAssignment n} (tr : ROBTrace dep b w t) (c : Nat) (i : Fin n) :
    (tr.state c).completed i ↔ t i < c := by
  induction c with
  | zero =>
    constructor
    · intro hc
      exact False.elim (tr.initially_incomplete i hc)
    · intro hc
      omega
  | succ c ih =>
    rw [(tr.step c).complete i, ih]
    omega

theorem trace_retirementPrefix {n : Nat} {dep : Dependency n} {b w : Nat}
    {t : TimeAssignment n} (tr : ROBTrace dep b w t) (c : Nat) :
    RetirementPrefix t c (tr.state c).retired := by
  cases c with
  | zero =>
    rw [tr.initially_retired]
    refine ⟨Nat.zero_le n, ?_, ?_⟩
    · intro i hi
      omega
    · intro h
      exact Nat.zero_le _
  | succ c =>
    have hp := (tr.step c).retire
    refine ⟨hp.1, ?_, ?_⟩
    · intro i hir
      exact (trace_completed_iff tr (c + 1) i).1 (hp.2.1 i hir)
    · intro hr
      have hnot := hp.2.2 hr
      have hiff := trace_completed_iff tr (c + 1) ⟨(tr.state (c + 1)).retired, hr⟩
      exact Nat.le_of_not_lt (fun hlt => hnot (hiff.mpr hlt))

theorem trace_admitted {n : Nat} {dep : Dependency n} {b w : Nat}
    {t : TimeAssignment n} (tr : ROBTrace dep b w t) (c : Nat) :
    (tr.state c).admitted = min n ((tr.state c).retired + b) := by
  cases c with
  | zero => simp only [tr.initially_retired, tr.initially_admitted, Nat.zero_add]
  | succ c => exact (tr.step c).admit

theorem trace_legal {n : Nat} {dep : Dependency n} {b w : Nat}
    {t : TimeAssignment n} (tr : ROBTrace dep b w t) : Legal dep b w t := by
  classical
  refine ⟨?_, ?_, ?_⟩
  · intro i j hij
    have hi := (tr.step (t j)).eligible j rfl
    exact (trace_completed_iff tr (t j) i).1 (hi.2.2.2 i hij)
  · intro j r hr
    have hi := (tr.step (t j)).eligible j rfl
    have heq := retirementPrefix_unique hr (trace_retirementPrefix tr (t j))
    rw [heq]
    refine ⟨hi.1, ?_⟩
    have hu := hi.2.1
    rw [trace_admitted tr (t j)] at hu
    exact Nat.lt_of_lt_of_le hu (Nat.min_le_right _ _)
  · let lanes : Nat → Fin n → Nat := fun c => Classical.choose (tr.step c).capacity
    have hlanes : ∀ c, (∀ i, t i = c → lanes c i < w) ∧
        (∀ i j, t i = c → t j = c → lanes c i = lanes c j → i = j) :=
      fun c => Classical.choose_spec (tr.step c).capacity
    refine ⟨fun i => lanes (t i) i, ?_, ?_⟩
    · intro i
      exact (hlanes (t i)).1 i rfl
    · intro i j ht hl
      have hlj : lanes (t i) i = lanes (t i) j := by simpa only [ht] using hl
      exact (hlanes (t i)).2 i j rfl ht.symm hlj

noncomputable def retirementCount {n : Nat} (t : TimeAssignment n) (c : Nat) : Nat :=
  Classical.choose (retirementPrefix_exists t c)

theorem retirementCount_spec {n : Nat} (t : TimeAssignment n) (c : Nat) :
    RetirementPrefix t c (retirementCount t c) :=
  Classical.choose_spec (retirementPrefix_exists t c)

theorem retirementCount_zero {n : Nat} (t : TimeAssignment n) :
    retirementCount t 0 = 0 := by
  apply retirementPrefix_unique (retirementCount_spec t 0)
  refine ⟨Nat.zero_le n, ?_, ?_⟩
  · intro i hi
    omega
  · intro h
    exact Nat.zero_le _

noncomputable def canonicalState {n : Nat} (t : TimeAssignment n) (b c : Nat) : ROBState n :=
  { completed := fun i => t i < c
    retired := retirementCount t c
    admitted := min n (retirementCount t c + b) }

theorem legal_canonical_step {n : Nat} {dep : Dependency n} {b w : Nat}
    {t : TimeAssignment n} (h : Legal dep b w t) (c : Nat) :
    ROBStep dep b w (canonicalState t b c) (fun i => t i = c)
      (canonicalState t b (c + 1)) := by
  refine ⟨?_, ?_, ?_, ?_, rfl⟩
  · obtain ⟨lane, hl, hi⟩ := h.2.2
    refine ⟨lane, fun i _ => hl i, ?_⟩
    intro i j hic hjc hlane
    exact hi i j (hic.trans hjc.symm) hlane
  · intro i hic
    have hp : RetirementPrefix t (t i) (retirementCount t c) := by
      simpa only [hic] using retirementCount_spec t c
    have hwin := h.2.1 i (retirementCount t c) hp
    refine ⟨hwin.1, ?_, ?_, ?_⟩
    · change i.val < min n (retirementCount t c + b)
      exact Nat.lt_min.mpr ⟨i.isLt, hwin.2⟩
    · change ¬ t i < c
      omega
    · intro j hji
      change t j < c
      have := h.1 j i hji
      omega
  · intro i
    change t i < c + 1 ↔ t i < c ∨ t i = c
    omega
  · exact (completedPrefix_iff t (c + 1) (retirementCount t (c + 1))).2
      (retirementCount_spec t (c + 1))

noncomputable def legalTrace {n : Nat} {dep : Dependency n} {b w : Nat}
    {t : TimeAssignment n} (h : Legal dep b w t) : ROBTrace dep b w t where
  state := canonicalState t b
  initially_incomplete := fun _ => Nat.not_lt_zero _
  initially_retired := retirementCount_zero t
  initially_admitted := by
    change min n (retirementCount t 0 + b) = min n b
    rw [retirementCount_zero, Nat.zero_add]
  step := legal_canonical_step h

/-- Full equivalence between the time-assignment predicates and a sequential
eager ROB trace. This covers arbitrary finite programs and cycle counts. -/
theorem legal_iff_operational {n : Nat} (dep : Dependency n) (b w : Nat)
    (t : TimeAssignment n) : Legal dep b w t ↔ Nonempty (ROBTrace dep b w t) := by
  constructor
  · intro h
    exact ⟨legalTrace h⟩
  · rintro ⟨tr⟩
    exact trace_legal tr

theorem trace_finished_iff {n : Nat} {dep : Dependency n} {b w : Nat}
    {t : TimeAssignment n} (tr : ROBTrace dep b w t) (k : Nat) :
    (tr.state k).retired = n ↔ ∀ i, t i < k := by
  have hp := trace_retirementPrefix tr k
  constructor
  · intro hr i
    exact hp.2.1 i (by rw [hr]; exact i.isLt)
  · intro hf
    apply Classical.byContradiction
    intro hneq
    have hrle := hp.1
    have hrn : (tr.state k).retired < n := by omega
    have hi := hf ⟨(tr.state k).retired, hrn⟩
    have hu := hp.2.2 hrn
    omega

/-- The horizon feasibility predicate is exactly existence of a legal ROB
execution whose entire program has retired at that cycle boundary. -/
theorem feasible_iff_finished_trace {n : Nat} (dep : Dependency n) (b w k : Nat) :
    Feasible dep b w k ↔
      ∃ (t : TimeAssignment n) (tr : ROBTrace dep b w t),
        (tr.state k).retired = n := by
  constructor
  · rintro ⟨t, h, hk⟩
    exact ⟨t, legalTrace h, (trace_finished_iff (legalTrace h) k).2 hk⟩
  · rintro ⟨t, tr, hk⟩
    exact ⟨t, trace_legal tr, (trace_finished_iff tr k).1 hk⟩

#print axioms completedPrefix_iff
#print axioms trace_completed_iff
#print axioms trace_retirementPrefix
#print axioms trace_admitted
#print axioms trace_legal
#print axioms retirementCount_spec
#print axioms retirementCount_zero
#print axioms legal_canonical_step
#print axioms legal_iff_operational
#print axioms trace_finished_iff
#print axioms feasible_iff_finished_trace

end ILP1
