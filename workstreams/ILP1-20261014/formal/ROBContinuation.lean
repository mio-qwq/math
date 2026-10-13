import ROBReady

/-!
# Finite actual ROB continuations and completion dominance

Continuations below consist of the existing ROBStep transitions, not an
abstract recurrence. Replaying after deleting already-completed jobs gives
a genuine continuation of the same length from any coherent completion
superset; terminal idle steps are allowed by the original processor model.
This is not yet a proof of existence of an optimal non-delay continuation.
-/

namespace ILP1.ROBContinuation

open ROBReady

theorem completedPrefix_mono {n r r' : Nat} {p p' : Fin n → Prop}
    (hp : CompletedPrefix p r) (hp' : CompletedPrefix p' r')
    (hsub : ∀ i, p i → p' i) : r ≤ r' := by
  apply Classical.byContradiction
  intro hnot
  have hrn : r' < n := by have := hp.1; omega
  have hold := hp.2.1 ⟨r', hrn⟩ (by change r' < r; omega)
  exact hp'.2.2 hrn (hsub _ hold)

/-- The already established actual-state invariant is preserved by every
actual step, without assuming a surrounding completed ROBTrace. -/
theorem step_coherent {n b w : Nat} {dep : Dependency n}
    {s next : ROBState n} {action : Fin n → Prop} (hs : Coherent b s)
    (step : ROBStep dep b w s action next) : Coherent b next := by
  have hr := completedPrefix_mono hs.retirement step.retire
    (fun i hi => (step.complete i).2 (Or.inl hi))
  refine ⟨step.retire, step.admit, ?_⟩
  intro i hi
  have hadm : i.val < s.admitted := by
    rcases (step.complete i).1 hi with hold | hiss
    · exact hs.completed_admitted i hold
    · exact (step.eligible i hiss).2.1
  have hbnd : i.val < s.retired + b := by
    rw [hs.admission] at hadm
    exact Nat.lt_of_lt_of_le hadm (Nat.min_le_right _ _)
  rw [step.admit]
  exact Nat.lt_min.mpr ⟨i.isLt, by omega⟩

theorem completedPrefix_exists {n : Nat} (p : Fin n → Prop) :
    ∃ r, CompletedPrefix p r := by
  classical
  let time : TimeAssignment n := fun i => if p i then 0 else 1
  obtain ⟨r, hp⟩ := retirementPrefix_exists time 1
  refine ⟨r, hp.1, ?_, ?_⟩
  · intro i hi
    have ht := hp.2.1 i hi
    apply Classical.byContradiction
    intro hnot
    simp [time, hnot] at ht
  · intro hr hi
    have ht := hp.2.2 hr
    simp [time, hi] at ht

noncomputable def firstIncomplete {n : Nat} (p : Fin n → Prop) : Nat :=
  Classical.choose (completedPrefix_exists p)

theorem firstIncomplete_spec {n : Nat} (p : Fin n → Prop) :
    CompletedPrefix p (firstIncomplete p) := Classical.choose_spec (completedPrefix_exists p)

/-- A canonical next state whose completion set is the actual step union. -/
noncomputable def afterAction {n : Nat} (b : Nat) (s : ROBState n)
    (action : Fin n → Prop) : ROBState n :=
  let done : Fin n → Prop := fun i => s.completed i ∨ action i
  { completed := done
    retired := firstIncomplete done
    admitted := min n (firstIncomplete done + b) }

/-- Width and actual readiness suffice to construct an existing-model step. -/
theorem afterAction_step {n b w : Nat} {dep : Dependency n} (s : ROBState n)
    (action : Fin n → Prop) (hwidth : BatchWidth action w)
    (hready : ∀ i, action i → CanIssue dep s i) :
    ROBStep dep b w s action (afterAction b s action) := by
  refine ⟨hwidth, hready, fun _ => Iff.rfl, ?_, rfl⟩
  exact firstIncomplete_spec _

theorem coherent_finished_iff {n b : Nat} {s : ROBState n} (hs : Coherent b s) :
    s.retired = n ↔ ∀ i, s.completed i := by
  constructor
  · intro hr i
    exact hs.retirement.2.1 i (by rw [hr]; exact i.isLt)
  · intro hall
    apply Classical.byContradiction
    intro hnot
    have hrn : s.retired < n := by have := hs.retirement.1; omega
    exact hs.retirement.2.2 hrn (hall ⟨s.retired, hrn⟩)

def Includes {n : Nat} (s s' : ROBState n) : Prop :=
  ∀ i, s.completed i → s'.completed i

def residualAction {n : Nat} (s' : ROBState n) (action : Fin n → Prop) : Fin n → Prop :=
  fun i => action i ∧ ¬ s'.completed i

/-- One-step actual simulation, deleting exactly the jobs already complete
in the dominating state. The resulting state again dominates the original. -/
theorem step_dominance {n b w : Nat} {dep : Dependency n}
    {s next s' : ROBState n} {action : Fin n → Prop}
    (hs : Coherent b s) (hs' : Coherent b s') (hsub : Includes s s')
    (step : ROBStep dep b w s action next) :
    ∃ next', ROBStep dep b w s' (residualAction s' action) next' ∧
      Coherent b next' ∧ Includes next next' := by
  have hwidth : BatchWidth (residualAction s' action) w := by
    obtain ⟨lane, hlane, hinj⟩ := step.capacity
    exact ⟨lane, fun i hi => hlane i hi.1,
      fun i j hi hj heq => hinj i j hi.1 hj.1 heq⟩
  have hready : ∀ i, residualAction s' action i → CanIssue dep s' i := by
    intro i hi
    exact canIssue_mono hs hs' hsub i (step.eligible i hi.1) hi.2
  let next' := afterAction b s' (residualAction s' action)
  have hstep : ROBStep dep b w s' (residualAction s' action) next' := afterAction_step s' _ hwidth hready
  refine ⟨next', hstep, step_coherent hs' hstep, ?_⟩
  intro i hi
  apply (hstep.complete i).2
  by_cases hdone : s'.completed i
  · exact Or.inl hdone
  · apply Or.inr
    refine ⟨?_, hdone⟩
    rcases (step.complete i).1 hi with hold | hiss
    · exact False.elim (hdone (hsub i hold))
    · exact hiss

/-- A finite chain of the actual ROBStep relation; exactly k cycles. -/
inductive Continuation {n : Nat} (dep : Dependency n) (b w : Nat) :
    ROBState n → Nat → ROBState n → Prop where
  | nil (s : ROBState n) : Continuation dep b w s 0 s
  | cons {s middle final : ROBState n} {k : Nat}
      (step : ROBStep dep b w s action middle)
      (tail : Continuation dep b w middle k final) : Continuation dep b w s (k + 1) final

theorem continuation_coherent {n b w k : Nat} {dep : Dependency n} {s final : ROBState n}
    (run : Continuation dep b w s k final) : Coherent b s → Coherent b final := by
  induction run with
  | nil _ => intro hs; exact hs
  | cons step _ ih => intro hs; exact ih (step_coherent hs step)

/-- Completion dominance for a whole finite actual continuation. The
simulation may end earlier but can retain the original exact cycle count. -/
theorem continuation_dominance {n b w k : Nat} {dep : Dependency n} {s final : ROBState n}
    (run : Continuation dep b w s k final) :
    Coherent b s → ∀ s', Coherent b s' → Includes s s' →
      ∃ final', Continuation dep b w s' k final' ∧ Coherent b final' ∧ Includes final final' := by
  induction run with
  | nil s =>
    intro _ s' hs' hsub
    exact ⟨s', Continuation.nil s', hs', hsub⟩
  | cons step tail ih =>
    intro hs s' hs' hsub
    obtain ⟨middle', hstep, hmid, hsubmid⟩ := step_dominance hs hs' hsub step
    obtain ⟨final', htail, hfinal, hsubfinal⟩ := ih (step_coherent hs step) middle' hmid hsubmid
    exact ⟨final', Continuation.cons hstep htail, hfinal, hsubfinal⟩

def FinishesFrom {n : Nat} (dep : Dependency n) (b w : Nat) (s : ROBState n) (k : Nat) : Prop :=
  ∃ final, Continuation dep b w s k final ∧ final.retired = n

theorem finishesFrom_dominance {n b w k : Nat} {dep : Dependency n} {s s' : ROBState n}
    (hs : Coherent b s) (hs' : Coherent b s') (hsub : Includes s s')
    (hfinish : FinishesFrom dep b w s k) : FinishesFrom dep b w s' k := by
  obtain ⟨final, run, hdone⟩ := hfinish
  obtain ⟨final', run', hcoh', hsubfinal⟩ := continuation_dominance run hs s' hs' hsub
  have hcoh := continuation_coherent run hs
  have hall := (coherent_finished_iff hcoh).1 hdone
  exact ⟨final', run', (coherent_finished_iff hcoh').2 (fun i => hsubfinal i (hall i))⟩

/-- Every finite segment of an actual ROBTrace is such a continuation. -/
theorem trace_segment {n b w : Nat} {dep : Dependency n} {t : TimeAssignment n}
    (tr : ROBTrace dep b w t) (c k : Nat) :
    Continuation dep b w (tr.state c) k (tr.state (c + k)) := by
  induction k generalizing c with
  | zero => simpa only [Nat.add_zero] using Continuation.nil (tr.state c)
  | succ k ih =>
    have htail := ih (c + 1)
    have hrun := Continuation.cons (tr.step c) htail
    simpa only [Nat.add_assoc, Nat.add_comm 1 k] using hrun

/-- Model-connected endpoint: from a reachable completion superset, any
finishing segment of the original actual trace can be completed in the
same number of cycles, regardless of how the superset was reached. -/
theorem trace_finishing_segment_dominance {n b w : Nat} {dep : Dependency n}
    {t t' : TimeAssignment n} (tr : ROBTrace dep b w t) (tr' : ROBTrace dep b w t')
    (c c' k : Nat) (hsub : Includes (tr.state c) (tr'.state c'))
    (hfinish : (tr.state (c + k)).retired = n) : FinishesFrom dep b w (tr'.state c') k := by
  exact finishesFrom_dominance (trace_coherent tr c) (trace_coherent tr' c') hsub
    ⟨tr.state (c + k), trace_segment tr c k, hfinish⟩

def OptimalFrom {n : Nat} (dep : Dependency n) (b w : Nat) (s : ROBState n) (k : Nat) : Prop :=
  FinishesFrom dep b w s k ∧ ∀ l, FinishesFrom dep b w s l → k ≤ l

/-- Whenever both state optima exist, completion inclusion can only improve
the optimum. Existence of a finishing continuation is not assumed secretly. -/
theorem optimalFrom_dominance {n b w k k' : Nat} {dep : Dependency n} {s s' : ROBState n}
    (hs : Coherent b s) (hs' : Coherent b s') (hsub : Includes s s')
    (hk : OptimalFrom dep b w s k) (hk' : OptimalFrom dep b w s' k') : k' ≤ k :=
  hk'.2 k (finishesFrom_dominance hs hs' hsub hk.1)

#print axioms completedPrefix_mono
#print axioms step_coherent
#print axioms completedPrefix_exists
#print axioms afterAction_step
#print axioms coherent_finished_iff
#print axioms step_dominance
#print axioms continuation_coherent
#print axioms continuation_dominance
#print axioms finishesFrom_dominance
#print axioms trace_segment
#print axioms trace_finishing_segment_dominance
#print axioms optimalFrom_dominance

end ILP1.ROBContinuation
