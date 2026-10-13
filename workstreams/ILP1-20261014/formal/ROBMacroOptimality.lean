import ROBForcedPrefix

/-!
# Exact optimality of first-clear macros in the actual ROB model

This proves composition/decomposition and the two directions of the
minimum-over-macros characterization. PrefixMacro denotes concrete finite
ROBStep executions, not externally supplied recurrence data. Executable
enumeration of the macros and its complexity are separate obligations.
-/

namespace ILP1.ROBMacroOptimality

open ROBReady ROBContinuation ROBNonDelay ROBRepresentation ROBForcedPrefix

theorem profile_continuation {n b w : Nat} {dep : Dependency n}
    {condition : ROBState n → Action n → Prop} {s final : ROBState n}
    {actions : List (Action n)} (run : Profile dep b w condition s actions final) :
    Continuation dep b w s actions.length final := by
  induction run with
  | nil s => exact Continuation.nil s
  | cons step _ _ ih => exact Continuation.cons step ih

theorem continuation_includes {n b w k : Nat} {dep : Dependency n} {s final : ROBState n}
    (run : Continuation dep b w s k final) : Includes s final := by
  induction run with
  | nil _ => exact fun _ hi => hi
  | cons step _ ih => exact fun i hi => ih i ((step.complete i).2 (Or.inl hi))

theorem continuation_append {n b w k l : Nat} {dep : Dependency n}
    {s middle final : ROBState n} (first : Continuation dep b w s k middle)
    (rest : Continuation dep b w middle l final) : Continuation dep b w s (k + l) final := by
  induction first with
  | nil _ => simpa only [Nat.zero_add] using rest
  | cons step tail ih =>
    simpa only [Nat.add_assoc, Nat.add_comm 1 l] using Continuation.cons step (ih rest)

theorem clear_completedCount {n b : Nat} {s : ROBState n} (hs : Coherent b s) (hc : Clear s) :
    completedCountOfState s = s.retired :=
  (count_congr hc).trans (count_prefix hs.retirement.1)

theorem forcedTail_length_le {n w : Nat} {dep : Dependency n} {s final : ROBState n}
    {actions : List (Action n)} (run : ForcedTail dep w s actions final)
    (hforward : Forward dep) (hw : 0 < w) :
    Coherent (w + 1) s → actions.length ≤ n - completedCountOfState s := by
  induction run with
  | stop _ => intro _; exact Nat.zero_le _
  | @cons s middle final actions hc step tail ih =>
    intro hs
    have hnd : NonDelay dep w s (CanIssue dep s) :=
      (nonDelay_iff_all_ready (nonclear_ready_le hs hc) _).2 (fun _ => Iff.rfl)
    have hprogress := nonDelay_step_progress hforward (by omega) hw hs
      (nonclear_nonterminal hs hc) hnd step
    have hlen := ih (step_coherent hs step)
    have hcount := count_le_n middle.completed
    change completedCountOfState middle ≤ n at hcount
    simp only [List.length_cons]
    omega

/-- Every macro from a nonterminal coherent clear state strictly advances
the prefix index; no oldest-first rule is used. -/
theorem prefixMacro_progress {n w : Nat} {dep : Dependency n} {s final : ROBState n}
    {actions : List (Action n)} (run : PrefixMacro dep w s actions final)
    (hforward : Forward dep) (hw : 0 < w) (hs : Coherent (w + 1) s)
    (hrn : s.retired < n) : s.retired < final.retired := by
  cases run with
  | mk hc step hnd tail =>
    have hm := step_coherent hs step
    have htail := profile_continuation (forcedTail_profile tail hm)
    have hf := continuation_coherent htail hm
    have hprogress := nonDelay_step_progress hforward (by omega) hw hs hrn hnd step
    have hmono := count_mono (continuation_includes htail)
    have hc0 := clear_completedCount hs hc
    have hcf := clear_completedCount hf (forcedTail_clear tail)
    change completedCountOfState _ ≤ completedCountOfState final at hmono
    omega

theorem prefixMacro_length_le {n w : Nat} {dep : Dependency n} {s final : ROBState n}
    {actions : List (Action n)} (run : PrefixMacro dep w s actions final)
    (hforward : Forward dep) (hw : 0 < w) (hs : Coherent (w + 1) s)
    (hrn : s.retired < n) : actions.length ≤ n - s.retired := by
  cases run with
  | @mk middle _ action rest hc step hnd tail =>
    have hprogress := nonDelay_step_progress hforward (by omega) hw hs hrn hnd step
    have hlen := forcedTail_length_le tail hforward hw (step_coherent hs step)
    have hcount := count_le_n middle.completed
    have hstart := clear_completedCount hs hc
    change completedCountOfState middle ≤ n at hcount
    simp only [List.length_cons]
    omega

/-- Every nonterminal clear state has an actual first-clear macro, with
strictly later prefix endpoint and the stated finite length bound. -/
theorem prefixMacro_exists {n w : Nat} {dep : Dependency n} {s : ROBState n}
    (hforward : Forward dep) (hw : 0 < w) (hs : Coherent (w + 1) s)
    (hc : Clear s) (hrn : s.retired < n) :
    ∃ actions final, PrefixMacro dep w s actions final ∧ Coherent (w + 1) final ∧
      s.retired < final.retired ∧ actions.length ≤ n - s.retired := by
  have hempty : BatchWidth (fun _ : Fin n => False) w :=
    ⟨fun _ => 0, fun _ hi => False.elim hi, fun _ _ hi _ _ => False.elim hi⟩
  obtain ⟨action, hnd, _⟩ := nonDelay_extension (dep := dep) (s := s)
    (fun _ => False) (fun _ hi => False.elim hi) hempty
  let middle := afterAction (w + 1) s action
  have step : ROBStep dep (w + 1) w s action middle :=
    afterAction_step s action (nonDelay_batchWidth hnd) hnd.1
  obtain ⟨rest, final, _, tail, hf⟩ := forcedTail_exists hforward hw middle (step_coherent hs step)
  have hmacro := PrefixMacro.mk hc step hnd tail
  exact ⟨action :: rest, final, hmacro, hf, prefixMacro_progress hmacro hforward hw hs hrn,
    prefixMacro_length_le hmacro hforward hw hs hrn⟩

/-- Actual macro execution followed by any actual finishing continuation
realizes the sum of the two cycle counts. -/
theorem macro_finishes {n w l : Nat} {dep : Dependency n} {s middle : ROBState n}
    {actions : List (Action n)} (run : PrefixMacro dep w s actions middle)
    (hs : Coherent (w + 1) s) (hrest : FinishesFrom dep (w + 1) w middle l) :
    FinishesFrom dep (w + 1) w s (actions.length + l) := by
  obtain ⟨final, rest, hdone⟩ := hrest
  exact ⟨final, continuation_append (profile_continuation (prefixMacro_profile run hs)) rest, hdone⟩

/-- Every feasible horizon has an exact first-macro decomposition after
the previously proved actual non-delay normalization. -/
theorem finishesFrom_first_macro {n w k : Nat} {dep : Dependency n} {s : ROBState n}
    (hs : Coherent (w + 1) s) (hc : Clear s) (hrn : s.retired < n)
    (hfinish : FinishesFrom dep (w + 1) w s k) :
    ∃ actions middle l, PrefixMacro dep w s actions middle ∧
      k = actions.length + l ∧ FinishesFrom dep (w + 1) w middle l := by
  obtain ⟨final, run, hdone⟩ := nonDelay_normalization k s hs hfinish
  obtain ⟨all, hlen, profile⟩ := nonDelayContinuation_profile run
  obtain ⟨first, rest, middle, heq, hmacro, suffix⟩ := profile_first_macro profile hs hc hrn hdone
  refine ⟨first, middle, rest.length, hmacro, ?_, final, profile_continuation suffix, hdone⟩
  rw [heq, List.length_append] at hlen
  exact hlen.symm

theorem finishesFrom_iff_macro {n w k : Nat} {dep : Dependency n} {s : ROBState n}
    (hs : Coherent (w + 1) s) (hc : Clear s) (hrn : s.retired < n) :
    FinishesFrom dep (w + 1) w s k ↔
      ∃ actions middle l, PrefixMacro dep w s actions middle ∧
        k = actions.length + l ∧ FinishesFrom dep (w + 1) w middle l := by
  constructor
  · exact finishesFrom_first_macro hs hc hrn
  · rintro ⟨actions, middle, l, hmacro, heq, rest⟩
    rw [heq]
    exact macro_finishes hmacro hs rest

/-- A globally optimal actual continuation decomposes into a first macro
and an optimal continuation from its endpoint. -/
theorem optimalFrom_first_macro {n w k : Nat} {dep : Dependency n} {s : ROBState n}
    (hs : Coherent (w + 1) s) (hc : Clear s) (hrn : s.retired < n)
    (hk : OptimalFrom dep (w + 1) w s k) :
    ∃ actions middle l, PrefixMacro dep w s actions middle ∧
      k = actions.length + l ∧ OptimalFrom dep (w + 1) w middle l := by
  obtain ⟨actions, middle, l, hmacro, heq, hrest⟩ := finishesFrom_first_macro hs hc hrn hk.1
  refine ⟨actions, middle, l, hmacro, heq, hrest, ?_⟩
  intro l' hl'
  have hbound := hk.2 (actions.length + l') (macro_finishes hmacro hs hl')
  omega

theorem optimalFrom_macro_bound {n w k l : Nat} {dep : Dependency n}
    {s middle : ROBState n} {actions : List (Action n)} (hs : Coherent (w + 1) s)
    (hk : OptimalFrom dep (w + 1) w s k) (run : PrefixMacro dep w s actions middle)
    (hl : OptimalFrom dep (w + 1) w middle l) : k ≤ actions.length + l :=
  hk.2 (actions.length + l) (macro_finishes run hs hl.1)

/-- Exact minimum characterization over actual first-clear macros. It has
an attaining macro with an optimal suffix, and its sum is no larger than
that of any other macro with an optimal suffix. Neither direction assumes
the recurrence it proves. No forwardness assumption is needed once these
continuation optima are quantified; least suffix horizons are constructed
from the actual finishing suffixes in the reverse implication. -/
theorem optimalFrom_iff_macro_min {n w k : Nat} {dep : Dependency n} {s : ROBState n}
    (hs : Coherent (w + 1) s) (hc : Clear s) (hrn : s.retired < n) :
    OptimalFrom dep (w + 1) w s k ↔
      (∃ actions middle l, PrefixMacro dep w s actions middle ∧
        k = actions.length + l ∧ OptimalFrom dep (w + 1) w middle l) ∧
      (∀ actions middle l, PrefixMacro dep w s actions middle →
        OptimalFrom dep (w + 1) w middle l → k ≤ actions.length + l) := by
  constructor
  · intro hk
    exact ⟨optimalFrom_first_macro hs hc hrn hk,
      fun _ _ _ hmacro hl => optimalFrom_macro_bound hs hk hmacro hl⟩
  · rintro ⟨⟨actions, middle, l, hmacro, heq, hl⟩, hmin⟩
    refine ⟨?_, ?_⟩
    · rw [heq]
      exact macro_finishes hmacro hs hl.1
    · intro other hother
      obtain ⟨otherActions, otherMiddle, otherL, otherMacro, hsum, hrest⟩ :=
        finishesFrom_first_macro hs hc hrn hother
      obtain ⟨best, hbest, hleast⟩ :=
        exists_least_nat (FinishesFrom dep (w + 1) w otherMiddle) ⟨otherL, hrest⟩
      have hbound := hmin otherActions otherMiddle best otherMacro ⟨hbest, hleast⟩
      have hle := hleast otherL hrest
      omega

/-- Existence for all N+1 concrete clear-prefix states. -/
theorem prefixOpt_exists {n w : Nat} {dep : Dependency n}
    (hforward : Forward dep) (hw : 0 < w) (r : Fin (n + 1)) :
    ∃ k, OptimalFrom dep (w + 1) w (prefixState n (w + 1) r.val) k := by
  have hr : r.val ≤ n := by have := r.isLt; omega
  obtain ⟨k, _, _, hopt, _, _⟩ :=
    optimal_nonDelay_exists hforward (by omega) hw (prefixState_coherent (b := w + 1) hr)
  exact ⟨k, hopt⟩

/-- Actual optimal remaining cost, chosen from the proved existence theorem.
This is a noncomputable specification, not an implementation of the DP. -/
noncomputable def prefixCost {n w : Nat} {dep : Dependency n}
    (hforward : Forward dep) (hw : 0 < w) (r : Fin (n + 1)) : Nat :=
  Classical.choose (prefixOpt_exists hforward hw r)

theorem prefixCost_optimal {n w : Nat} {dep : Dependency n}
    (hforward : Forward dep) (hw : 0 < w) (r : Fin (n + 1)) :
    OptimalFrom dep (w + 1) w (prefixState n (w + 1) r.val) (prefixCost hforward hw r) :=
  Classical.choose_spec (prefixOpt_exists hforward hw r)

theorem prefixCost_terminal {n w : Nat} {dep : Dependency n}
    (hforward : Forward dep) (hw : 0 < w) :
    prefixCost hforward hw ⟨n, by omega⟩ = 0 := by
  have hopt := prefixCost_optimal hforward hw ⟨n, by omega⟩
  have hfinish : FinishesFrom dep (w + 1) w (prefixState n (w + 1) n) 0 :=
    ⟨prefixState n (w + 1) n, Continuation.nil _, rfl⟩
  have hb := hopt.2 0 hfinish
  omega

theorem prefixState_zero (n b : Nat) : prefixState n b 0 = initialState n b := by
  apply state_eq_of_fields
  · intro i
    change i.val < 0 ↔ False
    exact ⟨Nat.not_lt_zero _, False.elim⟩
  · rfl
  · simp [prefixState, initialState]

/-- Prefix cost at zero is the original global Optimal value. This also
covers N=0, when the zero and terminal prefix are the same state. -/
theorem prefixCost_global_optimal {n w : Nat} {dep : Dependency n}
    (hforward : Forward dep) (hw : 0 < w) :
    Optimal dep (w + 1) w (prefixCost hforward hw ⟨0, by omega⟩) := by
  apply (optimal_iff_optimalFrom dep (w + 1) w _).2
  have hopt := prefixCost_optimal hforward hw ⟨0, by omega⟩
  simpa only [prefixState_zero] using hopt

/-- The closed scalar prefix recurrence over actual first-clear macros:
there is an attaining edge to a strictly later prefix and its cost is no
larger than every other actual macro's length plus that endpoint's actual
optimum. All prefix costs have been derived from original ROB transitions.
This is the mathematical minimum characterization, not a proved executable
enumerator or a complexity bound. -/
theorem prefixCost_recurrence {n w : Nat} {dep : Dependency n}
    (hforward : Forward dep) (hw : 0 < w) (r : Fin (n + 1)) (hrn : r.val < n) :
    ∃ (actions : List (Action n)) (j : Fin (n + 1)),
      r.val < j.val ∧ PrefixMacro dep w (prefixState n (w + 1) r.val) actions
        (prefixState n (w + 1) j.val) ∧
      prefixCost hforward hw r = actions.length + prefixCost hforward hw j ∧
      (∀ (otherActions : List (Action n)) (otherJ : Fin (n + 1)),
        PrefixMacro dep w (prefixState n (w + 1) r.val) otherActions
          (prefixState n (w + 1) otherJ.val) →
        prefixCost hforward hw r ≤ otherActions.length + prefixCost hforward hw otherJ) := by
  have hs := prefixState_coherent (b := w + 1) (Nat.le_of_lt hrn)
  have hopt := prefixCost_optimal hforward hw r
  obtain ⟨actions, middle, l, hmacro, hsum, hl⟩ :=
    optimalFrom_first_macro hs (prefixState_clear n (w + 1) r.val) hrn hopt
  have hm := continuation_coherent (profile_continuation (prefixMacro_profile hmacro hs)) hs
  let j : Fin (n + 1) := ⟨middle.retired, by have := hm.retirement.1; omega⟩
  have heq : middle = prefixState n (w + 1) j.val :=
    clear_state_eq hm (prefixMacro_clear hmacro).2
  have hmacro' : PrefixMacro dep w (prefixState n (w + 1) r.val) actions
      (prefixState n (w + 1) j.val) := by simpa only [heq] using hmacro
  have hl' : OptimalFrom dep (w + 1) w (prefixState n (w + 1) j.val) l := by
    simpa only [heq] using hl
  have hjopt := prefixCost_optimal hforward hw j
  have hlEq : l = prefixCost hforward hw j :=
    Nat.le_antisymm (hl'.2 _ hjopt.1) (hjopt.2 _ hl'.1)
  have hprogress := prefixMacro_progress hmacro hforward hw hs hrn
  refine ⟨actions, j, hprogress, hmacro', ?_, ?_⟩
  · simpa only [hlEq] using hsum
  · intro otherActions otherJ otherMacro
    exact optimalFrom_macro_bound hs hopt otherMacro (prefixCost_optimal hforward hw otherJ)

#print axioms profile_continuation
#print axioms continuation_includes
#print axioms continuation_append
#print axioms clear_completedCount
#print axioms forcedTail_length_le
#print axioms prefixMacro_progress
#print axioms prefixMacro_length_le
#print axioms prefixMacro_exists
#print axioms macro_finishes
#print axioms finishesFrom_first_macro
#print axioms finishesFrom_iff_macro
#print axioms optimalFrom_first_macro
#print axioms optimalFrom_macro_bound
#print axioms optimalFrom_iff_macro_min
#print axioms prefixOpt_exists
#print axioms prefixCost_optimal
#print axioms prefixCost_terminal
#print axioms prefixState_zero
#print axioms prefixCost_global_optimal
#print axioms prefixCost_recurrence

end ILP1.ROBMacroOptimality
