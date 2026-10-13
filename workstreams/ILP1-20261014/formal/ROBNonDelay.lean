import ROBContinuation

/-!
# Non-delay normalization of finite actual ROB continuations

First prove finite action extension from actual batch lanes and readiness.
Then use the already proved real continuation simulation to enlarge each
action without increasing the completion horizon. This module concerns
finite chains of the original ROBStep relation, not the prefix macro DP.
-/

namespace ILP1.ROBNonDelay

open ROBReady ROBContinuation ROBWorkBounds

theorem count_mono {n : Nat} {p q : Fin n → Prop} (h : ∀ i, p i → q i) : count p ≤ count q := by
  have hsub : selected p ⊆ selected q := by
    intro i hi
    exact (mem_selected q i).2 (h i ((mem_selected p i).1 hi))
  exact (selected_nodup p).length_le_of_subset hsub

theorem count_insert {n : Nat} (p : Fin n → Prop) (i : Fin n) (hnot : ¬ p i) :
    count (fun j => j = i ∨ p j) = count p + 1 := by
  have hl := count_strict_inclusion (p := p) (q := fun j => j = i ∨ p j)
    (fun _ hp => Or.inr hp) i (Or.inl rfl) hnot
  have hs : selected (fun j => j = i ∨ p j) ⊆ i :: selected p := by
    intro j hj
    rcases (mem_selected _ j).1 hj with heq | hp
    · exact List.mem_cons.mpr (Or.inl heq)
    · exact List.mem_cons.mpr (Or.inr ((mem_selected p j).2 hp))
  have hu := (selected_nodup (fun j => j = i ∨ p j)).length_le_of_subset hs
  change count (fun j => j = i ∨ p j) ≤ count p + 1 at hu
  omega

/-- Converse of the previously proved count-to-lanes bridge. -/
theorem count_le_of_batchWidth {n w : Nat} {action : Fin n → Prop}
    (hw : BatchWidth action w) : count action ≤ w := by
  obtain ⟨lane, hlane, hinj⟩ := hw
  have h := list_injection_length_le (selected action) (List.range w) lane (selected_nodup action)
    (fun i hi j hj heq => hinj i j ((mem_selected action i).1 hi)
      ((mem_selected action j).1 hj) heq)
    (fun i hi => List.mem_range.mpr (hlane i ((mem_selected action i).1 hi)))
  simpa only [count, List.length_range] using h

/-- Every actual legal ready subset has a non-delay extension. The maximal
cardinality witness is proved via a least unused-slot count; the target
non-delay equality is derived by adding a missing ready job if necessary. -/
theorem nonDelay_extension {n w : Nat} {dep : Dependency n} {s : ROBState n}
    (action : Fin n → Prop) (hready : ∀ i, action i → CanIssue dep s i)
    (hwidth : BatchWidth action w) :
    ∃ extended, NonDelay dep w s extended ∧ ∀ i, action i → extended i := by
  classical
  let P : Nat → Prop := fun gap => ∃ extended : Fin n → Prop,
    (∀ i, action i → extended i) ∧
    (∀ i, extended i → CanIssue dep s i) ∧ count extended ≤ w ∧ gap = w - count extended
  have hbase : P (w - count action) :=
    ⟨action, fun _ hi => hi, hready, count_le_of_batchWidth hwidth, rfl⟩
  obtain ⟨gap, hgap, hmin⟩ := exists_least_nat P ⟨_, hbase⟩
  obtain ⟨extended, hext, hlegal, hcount, hgapEq⟩ := hgap
  refine ⟨extended, ⟨hlegal, ?_⟩, hext⟩
  have hrbound : count extended ≤ readyCount dep s := count_mono hlegal
  apply Classical.byContradiction
  intro hneq
  have hwlt : count extended < w := by
    have hmin1 := Nat.min_le_left w (readyCount dep s)
    have hmin2 := Nat.min_le_right w (readyCount dep s)
    omega
  have hrlt : count extended < readyCount dep s := by
    have hmin1 := Nat.min_le_left w (readyCount dep s)
    have hmin2 := Nat.min_le_right w (readyCount dep s)
    omega
  have hmissing : ∃ i, CanIssue dep s i ∧ ¬ extended i := by
    apply Classical.byContradiction
    intro hn
    have hall : ∀ i, CanIssue dep s i → extended i := by
      intro i hi
      apply Classical.byContradiction
      intro hnot
      exact hn ⟨i, hi, hnot⟩
    have heq := count_congr (fun i => ⟨hlegal i, hall i⟩)
    change count extended = readyCount dep s at heq
    omega
  obtain ⟨i, hi, hnot⟩ := hmissing
  let enlarged : Fin n → Prop := fun j => j = i ∨ extended j
  have hnew : count enlarged = count extended + 1 := count_insert extended i hnot
  have hnewP : P (w - count enlarged) := by
    refine ⟨enlarged, fun j hj => Or.inr (hext j hj), ?_, by omega, rfl⟩
    intro j hj
    rcases hj with heq | hold
    · subst j
      exact hi
    · exact hlegal j hold
  have hless := hmin (w - count enlarged) hnewP
  omega

/-- Finite actual continuation with non-delay at each individual step. -/
inductive NonDelayContinuation {n : Nat} (dep : Dependency n) (b w : Nat) :
    ROBState n → Nat → ROBState n → Prop where
  | nil (s : ROBState n) : NonDelayContinuation dep b w s 0 s
  | cons {s middle final : ROBState n} {k : Nat}
      (step : ROBStep dep b w s action middle) (nonDelay : NonDelay dep w s action)
      (tail : NonDelayContinuation dep b w middle k final) :
      NonDelayContinuation dep b w s (k + 1) final

theorem NonDelayContinuation.toContinuation {n b w k : Nat} {dep : Dependency n}
    {s final : ROBState n} (run : NonDelayContinuation dep b w s k final) :
    Continuation dep b w s k final := by
  induction run with
  | nil s => exact Continuation.nil s
  | cons step _ _ ih => exact Continuation.cons step ih

/-- Every completing finite actual continuation has a non-delay replacement
with the exact same horizon. Empty non-delay steps after completion permit
padding; an optimal horizon therefore has an optimal non-delay witness. -/
theorem nonDelay_normalization {n b w : Nat} {dep : Dependency n} (k : Nat) :
    ∀ s, Coherent b s → FinishesFrom dep b w s k →
      ∃ final, NonDelayContinuation dep b w s k final ∧ final.retired = n := by
  induction k with
  | zero =>
    intro s _ hfinish
    obtain ⟨final, run, hdone⟩ := hfinish
    cases run
    exact ⟨s, NonDelayContinuation.nil s, hdone⟩
  | succ k ih =>
    intro s hs hfinish
    obtain ⟨final, run, hdone⟩ := hfinish
    cases run with
    | @cons action _ middle _ _ step tail =>
      obtain ⟨extended, hnd, hext⟩ := nonDelay_extension action step.eligible step.capacity
      let middle' := afterAction b s extended
      have hstep : ROBStep dep b w s extended middle' :=
        afterAction_step s extended (nonDelay_batchWidth hnd) hnd.1
      have hcoh' := step_coherent hs hstep
      have hsub : Includes middle middle' := by
        intro i hi
        rcases (step.complete i).1 hi with hold | hiss
        · exact (hstep.complete i).2 (Or.inl hold)
        · exact (hstep.complete i).2 (Or.inr (hext i hiss))
      have hrest : FinishesFrom dep b w middle' k :=
        finishesFrom_dominance (step_coherent hs step) hcoh' hsub ⟨final, tail, hdone⟩
      obtain ⟨final', htail, hdone'⟩ := ih middle' hcoh' hrest
      exact ⟨final', NonDelayContinuation.cons hstep hnd htail, hdone'⟩

theorem optimalFrom_nonDelay {n b w k : Nat} {dep : Dependency n} {s : ROBState n}
    (hs : Coherent b s) (hk : OptimalFrom dep b w s k) :
    ∃ final, NonDelayContinuation dep b w s k final ∧ final.retired = n :=
  nonDelay_normalization k s hs hk.1

/-- A known finishing continuation suffices for existence of a least
continuation horizon and a non-delay execution attaining that horizon. -/
theorem optimal_nonDelay_of_finishes {n b w horizon : Nat} {dep : Dependency n} {s : ROBState n}
    (hs : Coherent b s) (hfinish : FinishesFrom dep b w s horizon) :
    ∃ k final, k ≤ horizon ∧ OptimalFrom dep b w s k ∧
      NonDelayContinuation dep b w s k final ∧ final.retired = n := by
  obtain ⟨k, hk, hleast⟩ := exists_least_nat (FinishesFrom dep b w s) ⟨horizon, hfinish⟩
  obtain ⟨final, hrun, hdone⟩ := nonDelay_normalization k s hs hk
  exact ⟨k, final, hleast horizon hfinish, ⟨hk, hleast⟩, hrun, hdone⟩

/-- Applied to a finishing segment of a genuine ROB trace, the optimum
finite continuation from its start state has a non-delay witness. -/
theorem trace_segment_optimal_nonDelay {n b w : Nat} {dep : Dependency n}
    {t : TimeAssignment n} (tr : ROBTrace dep b w t) (c horizon : Nat)
    (hfinish : (tr.state (c + horizon)).retired = n) :
    ∃ k final, k ≤ horizon ∧ OptimalFrom dep b w (tr.state c) k ∧
      NonDelayContinuation dep b w (tr.state c) k final ∧ final.retired = n :=
  optimal_nonDelay_of_finishes (trace_coherent tr c)
    ⟨tr.state (c + horizon), trace_segment tr c horizon, hfinish⟩

/-- Forward dependencies and positive resources supply a finishing non-delay
continuation from every coherent state. Induction is on the actual number
of unfinished jobs; every constructed step is the existing ROBStep. -/
theorem nonDelay_finishes_bounded {n b w : Nat} {dep : Dependency n}
    (hforward : Forward dep) (hb : 0 < b) (hw : 0 < w) :
    ∀ s : ROBState n, Coherent b s →
      ∃ k final, k ≤ n - completedCountOfState s ∧
        NonDelayContinuation dep b w s k final ∧ final.retired = n := by
  have aux : ∀ remaining, ∀ s : ROBState n, Coherent b s →
      n - completedCountOfState s = remaining →
      ∃ k final, k ≤ remaining ∧ NonDelayContinuation dep b w s k final ∧ final.retired = n := by
    intro remaining
    induction remaining using Nat.strongRecOn with
    | ind remaining ih =>
      intro s hs hrem
      by_cases hdone : s.retired = n
      · exact ⟨0, s, Nat.zero_le _, NonDelayContinuation.nil s, hdone⟩
      · have hrn : s.retired < n := by have := hs.retirement.1; omega
        have hempty : BatchWidth (fun _ : Fin n => False) w :=
          ⟨fun _ => 0, fun _ hi => False.elim hi, fun _ _ hi _ _ => False.elim hi⟩
        obtain ⟨action, hnd, _⟩ := nonDelay_extension (dep := dep) (s := s)
          (fun _ => False) (fun _ hi => False.elim hi) hempty
        let next := afterAction b s action
        have hstep : ROBStep dep b w s action next :=
          afterAction_step s action (nonDelay_batchWidth hnd) hnd.1
        have hcoh := step_coherent hs hstep
        have hprogress := nonDelay_step_progress hforward hb hw hs hrn hnd hstep
        have hnextBound : completedCountOfState next ≤ n := count_le_n next.completed
        have hsmaller : n - completedCountOfState next < remaining := by omega
        obtain ⟨k, final, hk, htail, hfinal⟩ :=
          ih (n - completedCountOfState next) hsmaller next hcoh rfl
        exact ⟨k + 1, final, by omega, NonDelayContinuation.cons hstep hnd htail, hfinal⟩
  intro s hs
  exact aux (n - completedCountOfState s) s hs rfl

/-- Closed optimum-existence theorem in the finite actual transition model:
every coherent forward-program state has an optimal non-delay continuation. -/
theorem optimal_nonDelay_exists {n b w : Nat} {dep : Dependency n} {s : ROBState n}
    (hforward : Forward dep) (hb : 0 < b) (hw : 0 < w) (hs : Coherent b s) :
    ∃ k final, k ≤ n - completedCountOfState s ∧ OptimalFrom dep b w s k ∧
      NonDelayContinuation dep b w s k final ∧ final.retired = n := by
  obtain ⟨horizon, firstFinal, hbound, hrun, hdone⟩ := nonDelay_finishes_bounded hforward hb hw s hs
  obtain ⟨k, final, hk, hopt, hnd, hfinal⟩ :=
    optimal_nonDelay_of_finishes hs ⟨firstFinal, hrun.toContinuation, hdone⟩
  exact ⟨k, final, Nat.le_trans hk hbound, hopt, hnd, hfinal⟩

theorem trace_state_optimal_nonDelay {n b w : Nat} {dep : Dependency n}
    {t : TimeAssignment n} (tr : ROBTrace dep b w t) (hforward : Forward dep)
    (hb : 0 < b) (hw : 0 < w) (c : Nat) :
    ∃ k final, k ≤ n - completedCountOfState (tr.state c) ∧
      OptimalFrom dep b w (tr.state c) k ∧
      NonDelayContinuation dep b w (tr.state c) k final ∧ final.retired = n :=
  optimal_nonDelay_exists hforward hb hw (trace_coherent tr c)

#print axioms count_insert
#print axioms count_le_of_batchWidth
#print axioms nonDelay_extension
#print axioms NonDelayContinuation.toContinuation
#print axioms nonDelay_normalization
#print axioms optimalFrom_nonDelay
#print axioms optimal_nonDelay_of_finishes
#print axioms trace_segment_optimal_nonDelay
#print axioms nonDelay_finishes_bounded
#print axioms optimal_nonDelay_exists
#print axioms trace_state_optimal_nonDelay

end ILP1.ROBNonDelay
