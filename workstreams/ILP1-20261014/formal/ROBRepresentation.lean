import ROBNonDelay

/-!
# Finite actual continuations and global time assignments

The action list retains the actual ROBStep labels. An optional condition
is retained on every step, so extracting a time assignment from a
non-delay execution does not silently replace its issue decisions.
-/

namespace ILP1.ROBRepresentation

open ROBReady ROBContinuation ROBNonDelay

abbrev Action (n : Nat) := Fin n → Prop

/-- A labelled finite chain of original ROBStep transitions. -/
inductive Profile {n : Nat} (dep : Dependency n) (b w : Nat)
    (condition : ROBState n → Action n → Prop) :
    ROBState n → List (Action n) → ROBState n → Prop where
  | nil (s : ROBState n) : Profile dep b w condition s [] s
  | cons {s middle final : ROBState n} {action : Action n} {actions : List (Action n)}
      (step : ROBStep dep b w s action middle) (conditionProof : condition s action)
      (tail : Profile dep b w condition middle actions final) :
      Profile dep b w condition s (action :: actions) final

theorem continuation_profile {n b w k : Nat} {dep : Dependency n} {s final : ROBState n}
    (run : Continuation dep b w s k final) :
    ∃ actions, actions.length = k ∧ Profile dep b w (fun _ _ => True) s actions final := by
  induction run with
  | nil s => exact ⟨[], rfl, Profile.nil s⟩
  | @cons action s middle final k step tail ih =>
    obtain ⟨actions, hlen, hp⟩ := ih
    exact ⟨action :: actions, by simp [hlen], Profile.cons step True.intro hp⟩

theorem nonDelayContinuation_profile {n b w k : Nat} {dep : Dependency n}
    {s final : ROBState n} (run : NonDelayContinuation dep b w s k final) :
    ∃ actions, actions.length = k ∧ Profile dep b w (NonDelay dep w) s actions final := by
  induction run with
  | nil s => exact ⟨[], rfl, Profile.nil s⟩
  | @cons action s middle final k step hnd tail ih =>
    obtain ⟨actions, hlen, hp⟩ := ih
    exact ⟨action :: actions, by simp [hlen], Profile.cons step hnd hp⟩

/-- Empty batches beyond the finite list. Cycles are zero based. -/
def Fires {n : Nat} (actions : List (Action n)) (c : Nat) (i : Fin n) : Prop :=
  ((actions[c]?).getD (fun _ => False)) i

@[simp] theorem fires_nil {n : Nat} (c : Nat) (i : Fin n) : ¬ Fires [] c i := by
  simp [Fires]

@[simp] theorem fires_cons_zero {n : Nat} (action : Action n) (actions : List (Action n))
    (i : Fin n) : Fires (action :: actions) 0 i ↔ action i := Iff.rfl

@[simp] theorem fires_cons_succ {n : Nat} (action : Action n) (actions : List (Action n))
    (c : Nat) (i : Fin n) : Fires (action :: actions) (c + 1) i ↔ Fires actions c i := Iff.rfl

/-- Only initially unfinished jobs are assigned meaningful residual times.
The exact issue equivalence also excludes any reissue of initially done jobs. -/
structure ResidualRealization {n : Nat} (dep : Dependency n) (b w : Nat)
    (s : ROBState n) (actions : List (Action n)) (t : TimeAssignment n) : Prop where
  exact_issues : ∀ i c, Fires actions c i ↔ ¬ s.completed i ∧ t i = c
  horizon : ∀ i, ¬ s.completed i → t i < actions.length
  respects : ∀ i j, ¬ s.completed i → ¬ s.completed j → dep i j → t i < t j
  window : ∀ i j, ¬ s.completed i → ¬ s.completed j → i.val + b ≤ j.val → t i < t j
  lanes : ∃ lane : Fin n → Nat,
    (∀ i, ¬ s.completed i → lane i < w) ∧
    (∀ i j, ¬ s.completed i → ¬ s.completed j → t i = t j → lane i = lane j → i = j)

/-- Extraction for arbitrary coherent starting completion sets. The induction
uses the actual eligibility and union fields of each original ROBStep. -/
theorem profile_realization {n b w : Nat} {dep : Dependency n}
    {condition : ROBState n → Action n → Prop} {s final : ROBState n}
    {actions : List (Action n)} (run : Profile dep b w condition s actions final) :
    Coherent b s → final.retired = n → ∃ t, ResidualRealization dep b w s actions t := by
  classical
  induction run with
  | nil s =>
    intro hs hdone
    have hall := (coherent_finished_iff hs).1 hdone
    refine ⟨fun _ => 0, ?_⟩
    constructor
    · intro i c
      simp [hall i]
    · intro i hi
      exact False.elim (hi (hall i))
    · intro i j hi
      exact False.elim (hi (hall i))
    · intro i j hi
      exact False.elim (hi (hall i))
    · exact ⟨fun _ => 0, fun i hi => False.elim (hi (hall i)),
        fun i j hi => False.elim (hi (hall i))⟩
  | @cons s middle final action actions step _ tail ih =>
    intro hs hdone
    obtain ⟨u, hu⟩ := ih (step_coherent hs step) hdone
    obtain ⟨firstLane, hfirst, hinjFirst⟩ := step.capacity
    obtain ⟨tailLane, htail, hinjTail⟩ := hu.lanes
    let t : TimeAssignment n := fun i => if action i then 0 else u i + 1
    have hpend : ∀ i, ¬ s.completed i → ¬ action i → ¬ middle.completed i := by
      intro i hi ha hm
      exact ((step.complete i).1 hm).elim hi ha
    have ha_not : ∀ i, action i → ¬ s.completed i := fun i hi => (step.eligible i hi).2.2.1
    refine ⟨t, ?_⟩
    constructor
    · intro i c
      cases c with
      | zero =>
        rw [fires_cons_zero]
        by_cases ha : action i
        · simp [ha, ha_not i ha, t]
        · simp [ha, t]
      | succ c =>
        rw [fires_cons_succ, hu.exact_issues]
        by_cases ha : action i
        · have hm := (step.complete i).2 (Or.inr ha)
          simp [hm, ha, t]
        · by_cases hd : s.completed i
          · have hm := (step.complete i).2 (Or.inl hd)
            simp [hm, hd]
          · have hm := hpend i hd ha
            simp [hm, hd, ha, t]
    · intro i hi
      by_cases ha : action i
      · simp [t, ha]
      · have hb := hu.horizon i (hpend i hi ha)
        simpa [t, ha] using Nat.succ_lt_succ hb
    · intro i j hi hj hij
      by_cases hjA : action j
      · exact False.elim (hi ((step.eligible j hjA).2.2.2 i hij))
      · by_cases hiA : action i
        · simp [t, hiA, hjA]
        · have hlt := hu.respects i j (hpend i hi hiA) (hpend j hj hjA) hij
          simpa [t, hiA, hjA] using Nat.succ_lt_succ hlt
    · intro i j hi hj hij
      by_cases hjA : action j
      · have hjBound := (step.eligible j hjA).2.1
        rw [hs.admission] at hjBound
        have hjB := Nat.lt_of_lt_of_le hjBound (Nat.min_le_right n (s.retired + b))
        have hiR : s.retired ≤ i.val := by
          apply Nat.le_of_not_gt
          intro hlt
          exact hi (hs.retirement.2.1 i hlt)
        omega
      · by_cases hiA : action i
        · simp [t, hiA, hjA]
        · have hlt := hu.window i j (hpend i hi hiA) (hpend j hj hjA) hij
          simpa [t, hiA, hjA] using Nat.succ_lt_succ hlt
    · refine ⟨fun i => if action i then firstLane i else tailLane i, ?_, ?_⟩
      · intro i hi
        by_cases ha : action i
        · simpa [ha] using hfirst i ha
        · simpa [ha] using htail i (hpend i hi ha)
      · intro i j hi hj ht hl
        by_cases hiA : action i <;> by_cases hjA : action j
        · exact hinjFirst i j hiA hjA (by simpa [hiA, hjA] using hl)
        · simp [t, hiA, hjA] at ht
        · simp [t, hiA, hjA] at ht
        · have htime : u i = u j := by simpa [t, hiA, hjA] using ht
          exact hinjTail i j (hpend i hi hiA) (hpend j hj hjA) htime
            (by simpa [hiA, hjA] using hl)

theorem residual_unique_issue {n b w : Nat} {dep : Dependency n} {s : ROBState n}
    {actions : List (Action n)} {t : TimeAssignment n}
    (h : ResidualRealization dep b w s actions t) (i : Fin n) (hi : ¬ s.completed i) :
    ∃ c, c < actions.length ∧ Fires actions c i ∧ ∀ d, Fires actions d i → d = c := by
  refine ⟨t i, h.horizon i hi, (h.exact_issues i (t i)).2 ⟨hi, rfl⟩, ?_⟩
  intro d hd
  exact ((h.exact_issues i d).1 hd).2.symm

/-- The initial eager ROB state, including the empty-program boundary. -/
def initialState (n b : Nat) : ROBState n :=
  { completed := fun _ => False, retired := 0, admitted := min n b }

theorem initial_coherent (n b : Nat) : Coherent b (initialState n b) := by
  refine ⟨⟨Nat.zero_le n, ?_, fun _ => id⟩, by simp [initialState], ?_⟩
  · intro i hi
    change i.val < 0 at hi
    omega
  · intro i hi
    exact False.elim hi

theorem state_eq_of_fields {n : Nat} {s s' : ROBState n}
    (hc : ∀ i, s.completed i ↔ s'.completed i)
    (hr : s.retired = s'.retired) (ha : s.admitted = s'.admitted) : s = s' := by
  cases s with
  | mk done retired admitted =>
    cases s' with
    | mk done' retired' admitted' =>
      dsimp at hc hr ha
      have hd : done = done' := funext (fun i => propext (hc i))
      cases hd
      cases hr
      cases ha
      rfl

theorem trace_initial_eq {n b w : Nat} {dep : Dependency n} {t : TimeAssignment n}
    (tr : ROBTrace dep b w t) : tr.state 0 = initialState n b := by
  apply state_eq_of_fields
  · intro i
    exact ⟨tr.initially_incomplete i, False.elim⟩
  · exact tr.initially_retired
  · exact tr.initially_admitted

/-- A finishing actual profile from the initial state yields Legal plus an
exact correspondence with all its labelled issue batches. -/
theorem initial_profile_realization {n b w : Nat} {dep : Dependency n}
    {condition : ROBState n → Action n → Prop} {final : ROBState n}
    {actions : List (Action n)}
    (run : Profile dep b w condition (initialState n b) actions final) (hdone : final.retired = n) :
    ∃ t, Legal dep b w t ∧ (∀ i, t i < actions.length) ∧
      ∀ i c, Fires actions c i ↔ t i = c := by
  obtain ⟨t, ht⟩ := profile_realization run (initial_coherent n b) hdone
  have hnot : ∀ i, ¬ (initialState n b).completed i := fun _ => id
  refine ⟨t, ⟨?_, ?_, ?_⟩, fun i => ht.horizon i (hnot i), ?_⟩
  · exact fun i j hij => ht.respects i j (hnot i) (hnot j) hij
  · apply (windowEdges_iff_canonicalROB t b).1
    exact fun i j hij => ht.window i j (hnot i) (hnot j) hij
  · obtain ⟨lane, hl, hinj⟩ := ht.lanes
    exact ⟨lane, fun i => hl i (hnot i), fun i j => hinj i j (hnot i) (hnot j)⟩
  · intro i c
    simpa only [initialState, not_false_eq_true, true_and] using ht.exact_issues i c

/-- Every finishing finite chain of actual ROBStep transitions produces a
global feasible schedule with exactly the same horizon. -/
theorem finishesFrom_feasible {n b w k : Nat} {dep : Dependency n}
    (hfinish : FinishesFrom dep b w (initialState n b) k) : Feasible dep b w k := by
  obtain ⟨final, run, hdone⟩ := hfinish
  obtain ⟨actions, hlen, profile⟩ := continuation_profile run
  obtain ⟨t, hlegal, hhorizon, _⟩ := initial_profile_realization profile hdone
  exact ⟨t, hlegal, fun i => by simpa only [hlen] using hhorizon i⟩

/-- Exact equivalence of the two previously separate feasibility predicates.
No positivity or forward-dependency hypothesis is needed for this bridge. -/
theorem feasible_iff_finishesFrom {n : Nat} (dep : Dependency n) (b w k : Nat) :
    Feasible dep b w k ↔ FinishesFrom dep b w (initialState n b) k := by
  constructor
  · rintro ⟨t, hlegal, hhorizon⟩
    let tr := legalTrace hlegal
    have hrun := trace_segment tr 0 k
    have hdone := (trace_finished_iff tr k).2 hhorizon
    have heq := trace_initial_eq tr
    refine ⟨tr.state k, ?_, hdone⟩
    simpa only [Nat.zero_add, heq] using hrun
  · exact finishesFrom_feasible

/-- The global optimum equals the optimum finite continuation from the
initial eager state, with all horizons quantified identically. -/
theorem optimal_iff_optimalFrom {n : Nat} (dep : Dependency n) (b w k : Nat) :
    Optimal dep b w k ↔ OptimalFrom dep b w (initialState n b) k := by
  constructor
  · intro hk
    exact ⟨(feasible_iff_finishesFrom dep b w k).1 hk.1,
      fun l hl => hk.2 l ((feasible_iff_finishesFrom dep b w l).2 hl)⟩
  · intro hk
    exact ⟨(feasible_iff_finishesFrom dep b w k).2 hk.1,
      fun l hl => hk.2 l ((feasible_iff_finishesFrom dep b w l).1 hl)⟩

/-- Every feasible global optimum is attained by a non-delay actual
profile and the same profile's extracted legal time assignment. -/
theorem global_optimal_nonDelay {n b w k : Nat} {dep : Dependency n}
    (hk : Optimal dep b w k) :
    ∃ (t : TimeAssignment n) (actions : List (Action n)) (final : ROBState n),
      Legal dep b w t ∧ (∀ i, t i < k) ∧ actions.length = k ∧
      Profile dep b w (NonDelay dep w) (initialState n b) actions final ∧
      final.retired = n ∧ (∀ i c, Fires actions c i ↔ t i = c) := by
  have hfrom := (optimal_iff_optimalFrom dep b w k).1 hk
  obtain ⟨final, run, hdone⟩ := optimalFrom_nonDelay (initial_coherent n b) hfrom
  obtain ⟨actions, hlen, profile⟩ := nonDelayContinuation_profile run
  obtain ⟨t, hlegal, hhorizon, hexact⟩ := initial_profile_realization profile hdone
  exact ⟨t, actions, final, hlegal, fun i => by simpa only [hlen] using hhorizon i,
    hlen, profile, hdone, hexact⟩

/-- Closed global existence: arbitrary finite forward programs and positive
resources have a globally optimal non-delay execution, of at most n cycles.
The time assignment and non-delay labels describe the very same execution. -/
theorem global_optimal_nonDelay_exists {n b w : Nat} {dep : Dependency n}
    (hforward : Forward dep) (hb : 0 < b) (hw : 0 < w) :
    ∃ (k : Nat) (t : TimeAssignment n) (actions : List (Action n)) (final : ROBState n),
      k ≤ n ∧ Optimal dep b w k ∧ Legal dep b w t ∧ (∀ i, t i < k) ∧
      actions.length = k ∧ Profile dep b w (NonDelay dep w) (initialState n b) actions final ∧
      final.retired = n ∧ (∀ i c, Fires actions c i ↔ t i = c) := by
  obtain ⟨k, _, hbound, hopt, _, _⟩ :=
    optimal_nonDelay_exists hforward hb hw (initial_coherent n b)
  have hglobal := (optimal_iff_optimalFrom dep b w k).2 hopt
  obtain ⟨t, actions, final, hlegal, hhorizon, hlen, profile, hdone, hexact⟩ :=
    global_optimal_nonDelay hglobal
  exact ⟨k, t, actions, final, Nat.le_trans hbound (Nat.sub_le _ _),
    hglobal, hlegal, hhorizon, hlen, profile, hdone, hexact⟩

#print axioms continuation_profile
#print axioms nonDelayContinuation_profile
#print axioms fires_nil
#print axioms fires_cons_zero
#print axioms fires_cons_succ
#print axioms profile_realization
#print axioms residual_unique_issue
#print axioms initial_coherent
#print axioms state_eq_of_fields
#print axioms trace_initial_eq
#print axioms initial_profile_realization
#print axioms finishesFrom_feasible
#print axioms feasible_iff_finishesFrom
#print axioms optimal_iff_optimalFrom
#print axioms global_optimal_nonDelay
#print axioms global_optimal_nonDelay_exists

end ILP1.ROBRepresentation
