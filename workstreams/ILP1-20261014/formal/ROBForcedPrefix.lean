import ROBRepresentation

/-!
# First return to a clear prefix in actual ROB executions

For B=W+1 every non-clear coherent state has only the all-ready non-delay
action. ForcedTail records actual ROBStep transitions and stops at the
first clear state. No macro recurrence is postulated as an interface.
-/

namespace ILP1.ROBForcedPrefix

open ROBReady ROBContinuation ROBNonDelay ROBRepresentation

def Clear {n : Nat} (s : ROBState n) : Prop :=
  ∀ i, s.completed i ↔ i.val < s.retired

def prefixState (n b r : Nat) : ROBState n :=
  { completed := fun i => i.val < r, retired := r, admitted := min n (r + b) }

theorem prefixState_clear (n b r : Nat) : Clear (prefixState n b r) := fun _ => Iff.rfl

theorem prefixState_coherent {n b r : Nat} (hr : r ≤ n) : Coherent b (prefixState n b r) := by
  refine ⟨⟨hr, fun _ hi => hi, ?_⟩, rfl, ?_⟩
  · intro h hi
    change r < r at hi
    omega
  · intro i hi
    change i.val < r at hi
    change i.val < min n (r + b)
    exact Nat.lt_min.mpr ⟨i.isLt, by omega⟩

theorem clear_state_eq {n b : Nat} {s : ROBState n} (hs : Coherent b s) (hc : Clear s) :
    s = prefixState n b s.retired :=
  state_eq_of_fields hc rfl hs.admission

theorem finished_clear {n b : Nat} {s : ROBState n} (hs : Coherent b s) (hdone : s.retired = n) :
    Clear s := by
  intro i
  constructor
  · intro _
    rw [hdone]
    exact i.isLt
  · exact hs.retirement.2.1 i

theorem nonclear_nonterminal {n b : Nat} {s : ROBState n} (hs : Coherent b s) (hc : ¬ Clear s) :
    s.retired < n := by
  have hle := hs.retirement.1
  have hne : s.retired ≠ n := fun h => hc (finished_clear hs h)
  omega

/-- Actual completion union, maximal retirement, and eager admission uniquely
determine the successor of a fixed issue action. No coherent-start premise is
needed for this uniqueness theorem. -/
theorem step_unique {n b w : Nat} {dep : Dependency n} {s next next' : ROBState n}
    {action action' : Action n} (step : ROBStep dep b w s action next)
    (step' : ROBStep dep b w s action' next') (ha : ∀ i, action i ↔ action' i) : next = next' := by
  have hc : ∀ i, next.completed i ↔ next'.completed i := by
    intro i
    rw [step.complete i, step'.complete i, ha i]
  have hle := completedPrefix_mono step.retire step'.retire (fun i hi => (hc i).1 hi)
  have hge := completedPrefix_mono step'.retire step.retire (fun i hi => (hc i).2 hi)
  have hr : next.retired = next'.retired := Nat.le_antisymm hle hge
  apply state_eq_of_fields hc hr
  rw [step.admit, step'.admit, hr]

theorem nonclear_ready_le {n w : Nat} {dep : Dependency n} {s : ROBState n}
    (hs : Coherent (w + 1) s) (hc : ¬ Clear s) : readyCount dep s ≤ w := by
  have hh : 1 ≤ holeCount s := by
    apply Classical.byContradiction
    intro hn
    exact hc ((zero_holes_iff_prefix hs).1 (by omega))
  exact ready_le_width_of_holes hs hh

theorem nonclear_all_ready {n w : Nat} {dep : Dependency n} {s : ROBState n}
    (hs : Coherent (w + 1) s) (hc : ¬ Clear s) {action : Action n}
    (hnd : NonDelay dep w s action) : ∀ i, action i ↔ CanIssue dep s i :=
  (nonDelay_iff_all_ready (nonclear_ready_le hs hc) action).1 hnd

theorem nonclear_step_unique {n w : Nat} {dep : Dependency n} {s next next' : ROBState n}
    {action action' : Action n} (hs : Coherent (w + 1) s) (hc : ¬ Clear s)
    (step : ROBStep dep (w + 1) w s action next) (hnd : NonDelay dep w s action)
    (step' : ROBStep dep (w + 1) w s action' next') (hnd' : NonDelay dep w s action') :
    action = action' ∧ next = next' := by
  have ha : ∀ i, action i ↔ action' i := fun i =>
    (nonclear_all_ready hs hc hnd i).trans (nonclear_all_ready hs hc hnd' i).symm
  exact ⟨funext (fun i => propext (ha i)), step_unique step step' ha⟩

/-- Exactly the all-ready execution until the first clear state. The stop
and cons guards prohibit both stopping too soon and continuing past clear. -/
inductive ForcedTail {n : Nat} (dep : Dependency n) (w : Nat) :
    ROBState n → List (Action n) → ROBState n → Prop where
  | stop {s : ROBState n} (clear : Clear s) : ForcedTail dep w s [] s
  | cons {s middle final : ROBState n} {actions : List (Action n)}
      (nonclear : ¬ Clear s)
      (step : ROBStep dep (w + 1) w s (CanIssue dep s) middle)
      (tail : ForcedTail dep w middle actions final) :
      ForcedTail dep w s (CanIssue dep s :: actions) final

theorem forcedTail_clear {n w : Nat} {dep : Dependency n} {s final : ROBState n}
    {actions : List (Action n)} (run : ForcedTail dep w s actions final) : Clear final := by
  induction run with
  | stop hc => exact hc
  | cons _ _ _ ih => exact ih

theorem forcedTail_profile {n w : Nat} {dep : Dependency n} {s final : ROBState n}
    {actions : List (Action n)} (run : ForcedTail dep w s actions final) :
    Coherent (w + 1) s → Profile dep (w + 1) w (NonDelay dep w) s actions final := by
  induction run with
  | stop _ => intro _; exact Profile.nil _
  | cons hc step tail ih =>
    intro hs
    have hnd : NonDelay dep w _ (CanIssue dep _) :=
      (nonDelay_iff_all_ready (nonclear_ready_le hs hc) _).2 (fun _ => Iff.rfl)
    exact Profile.cons step hnd (ih (step_coherent hs step))

/-- Both actions and endpoint of the first-clear forced tail are unique. -/
theorem forcedTail_unique {n w : Nat} {dep : Dependency n} {s final final' : ROBState n}
    {actions actions' : List (Action n)} (run : ForcedTail dep w s actions final)
    (run' : ForcedTail dep w s actions' final') : actions = actions' ∧ final = final' := by
  induction run generalizing actions' final' with
  | stop hc =>
    cases run' with
    | stop _ => exact ⟨rfl, rfl⟩
    | cons hn _ _ => exact False.elim (hn hc)
  | @cons s middle final actions hn step tail ih =>
    cases run' with
    | stop hc => exact False.elim (hn hc)
    | @cons _ middle' _ actions' hn' step' tail' =>
      have heq := step_unique step step' (fun _ => Iff.rfl)
      subst middle'
      obtain ⟨ha, hf⟩ := ih tail'
      exact ⟨congrArg (List.cons (CanIssue dep s)) ha, hf⟩

/-- Forwardness and positive width guarantee reaching the first clear state
in at most the actual number of unfinished jobs. All intermediate steps are
the original ROBStep relation, constructed from real ready sets. -/
theorem forcedTail_exists {n w : Nat} {dep : Dependency n}
    (hforward : Forward dep) (hw : 0 < w) :
    ∀ s : ROBState n, Coherent (w + 1) s →
      ∃ actions final, actions.length ≤ n - completedCountOfState s ∧
        ForcedTail dep w s actions final ∧ Coherent (w + 1) final := by
  have aux : ∀ remaining, ∀ s : ROBState n, Coherent (w + 1) s →
      n - completedCountOfState s = remaining →
      ∃ actions final, actions.length ≤ remaining ∧ ForcedTail dep w s actions final ∧
        Coherent (w + 1) final := by
    intro remaining
    induction remaining using Nat.strongRecOn with
    | ind remaining ih =>
      intro s hs hrem
      by_cases hc : Clear s
      · exact ⟨[], s, Nat.zero_le _, ForcedTail.stop hc, hs⟩
      · have hrn := nonclear_nonterminal hs hc
        have hnd : NonDelay dep w s (CanIssue dep s) :=
          (nonDelay_iff_all_ready (nonclear_ready_le hs hc) _).2 (fun _ => Iff.rfl)
        let middle := afterAction (w + 1) s (CanIssue dep s)
        have step : ROBStep dep (w + 1) w s (CanIssue dep s) middle :=
          afterAction_step s _ (nonDelay_batchWidth hnd) hnd.1
        have hm := step_coherent hs step
        have hprogress := nonDelay_step_progress hforward (by omega) hw hs hrn hnd step
        have hcount := count_le_n middle.completed
        have hsmaller : n - completedCountOfState middle < remaining := by
          change completedCountOfState middle ≤ n at hcount
          omega
        obtain ⟨actions, final, hlen, tail, hf⟩ :=
          ih (n - completedCountOfState middle) hsmaller middle hm rfl
        refine ⟨CanIssue dep s :: actions, final, ?_, ForcedTail.cons hc step tail, hf⟩
        simp only [List.length_cons]
        omega
  intro s hs
  exact aux (n - completedCountOfState s) s hs rfl

/-- Split a finishing actual non-delay profile at its first clear state.
The suffix is part of the original action list, not a replacement schedule. -/
theorem profile_first_clear {n w : Nat} {dep : Dependency n} {s final : ROBState n}
    {actions : List (Action n)} (run : Profile dep (w + 1) w (NonDelay dep w) s actions final) :
    Coherent (w + 1) s → final.retired = n →
      ∃ first rest middle, actions = first ++ rest ∧ ForcedTail dep w s first middle ∧
        Profile dep (w + 1) w (NonDelay dep w) middle rest final := by
  induction run with
  | nil s =>
    intro hs hdone
    exact ⟨[], [], s, rfl, ForcedTail.stop (finished_clear hs hdone), Profile.nil s⟩
  | @cons s middle final action actions step hnd tail ih =>
    intro hs hdone
    by_cases hc : Clear s
    · exact ⟨[], action :: actions, s, rfl, ForcedTail.stop hc, Profile.cons step hnd tail⟩
    · have ha : action = CanIssue dep s := funext (fun i => propext (nonclear_all_ready hs hc hnd i))
      subst action
      obtain ⟨first, rest, cut, heq, hforced, hrest⟩ := ih (step_coherent hs step) hdone
      refine ⟨CanIssue dep s :: first, rest, cut, ?_, ForcedTail.cons hc step hforced, hrest⟩
      simp only [List.cons_append, heq]

/-- One non-delay decision at a clear prefix, followed by the uniquely
forced first-clear tail. It always contains at least the decision cycle. -/
inductive PrefixMacro {n : Nat} (dep : Dependency n) (w : Nat) :
    ROBState n → List (Action n) → ROBState n → Prop where
  | mk {s middle final : ROBState n} {action : Action n} {actions : List (Action n)}
      (clear : Clear s) (step : ROBStep dep (w + 1) w s action middle)
      (nonDelay : NonDelay dep w s action) (tail : ForcedTail dep w middle actions final) :
      PrefixMacro dep w s (action :: actions) final

theorem prefixMacro_nonempty {n w : Nat} {dep : Dependency n} {s final : ROBState n}
    {actions : List (Action n)} (run : PrefixMacro dep w s actions final) : 0 < actions.length := by
  cases run
  simp

theorem prefixMacro_clear {n w : Nat} {dep : Dependency n} {s final : ROBState n}
    {actions : List (Action n)} (run : PrefixMacro dep w s actions final) : Clear s ∧ Clear final := by
  cases run with
  | mk hc _ _ tail => exact ⟨hc, forcedTail_clear tail⟩

theorem prefixMacro_profile {n w : Nat} {dep : Dependency n} {s final : ROBState n}
    {actions : List (Action n)} (run : PrefixMacro dep w s actions final) (hs : Coherent (w + 1) s) :
    Profile dep (w + 1) w (NonDelay dep w) s actions final := by
  cases run with
  | mk _ step hnd tail => exact Profile.cons step hnd (forcedTail_profile tail (step_coherent hs step))

/-- A completing non-delay profile from a nonterminal clear state decomposes
into its actual first PrefixMacro and its actual remaining suffix. -/
theorem profile_first_macro {n w : Nat} {dep : Dependency n} {s final : ROBState n}
    {actions : List (Action n)} (run : Profile dep (w + 1) w (NonDelay dep w) s actions final)
    (hs : Coherent (w + 1) s) (hc : Clear s) (hrn : s.retired < n) (hdone : final.retired = n) :
    ∃ first rest middle, actions = first ++ rest ∧ PrefixMacro dep w s first middle ∧
      Profile dep (w + 1) w (NonDelay dep w) middle rest final := by
  cases run with
  | nil s => omega
  | @cons _ middle _ action actions step hnd tail =>
    obtain ⟨first, rest, cut, heq, hforced, hrest⟩ :=
      profile_first_clear tail (step_coherent hs step) hdone
    refine ⟨action :: first, rest, cut, ?_, PrefixMacro.mk hc step hnd hforced, hrest⟩
    simp only [List.cons_append, heq]

#print axioms prefixState_clear
#print axioms prefixState_coherent
#print axioms clear_state_eq
#print axioms finished_clear
#print axioms nonclear_nonterminal
#print axioms step_unique
#print axioms nonclear_ready_le
#print axioms nonclear_all_ready
#print axioms nonclear_step_unique
#print axioms forcedTail_clear
#print axioms forcedTail_profile
#print axioms forcedTail_unique
#print axioms forcedTail_exists
#print axioms profile_first_clear
#print axioms prefixMacro_nonempty
#print axioms prefixMacro_clear
#print axioms prefixMacro_profile
#print axioms profile_first_macro

end ILP1.ROBForcedPrefix
