import ROBOperational

/-!
# Bellman lower-bound certificates for the operational ROB

The lower-bound endpoint quantifies over every legal transition, including
empty issue batches.  No non-idling, acyclicity, or candidate-list coverage
assumption is used for that endpoint.  A concrete legal witness attaining
the potential at the explicit empty initial state establishes optimality.
-/

namespace ILP1

/-- The fully specified state before the first issue cycle. -/
def initialROBState (n b : Nat) : ROBState n :=
  { completed := fun _ => False
    retired := 0
    admitted := min n b }

/-- All jobs have completed; retirement is handled by the operational invariant. -/
def ROBComplete {n : Nat} (s : ROBState n) : Prop := ∀ i, s.completed i

theorem trace_initial_eq {n : Nat} {dep : Dependency n} {b w : Nat}
    {t : TimeAssignment n} (tr : ROBTrace dep b w t) :
    tr.state 0 = initialROBState n b := by
  have hc : (tr.state 0).completed = (fun _ => False) := by
    funext i
    exact propext ⟨fun hi => tr.initially_incomplete i hi, False.elim⟩
  have hr := tr.initially_retired
  have ha := tr.initially_admitted
  cases h : tr.state 0 with
  | mk completed retired admitted =>
    simp only [h] at hc hr ha
    simp only [initialROBState]
    cases hc
    cases hr
    cases ha
    rfl

theorem trace_complete_iff {n : Nat} {dep : Dependency n} {b w : Nat}
    {t : TimeAssignment n} (tr : ROBTrace dep b w t) (k : Nat) :
    ROBComplete (tr.state k) ↔ ∀ i, t i < k := by
  constructor
  · intro h i
    exact (trace_completed_iff tr k i).1 (h i)
  · intro h i
    exact (trace_completed_iff tr k i).2 (h i)

/-- A lower bound need only be a Bellman subsolution, not the exact value.
All transitions, including empty cycles and every allowed issue choice,
must satisfy `step_le`. -/
structure ROBPotential {n : Nat} (dep : Dependency n) (b w : Nat)
    (value : ROBState n → Nat) : Prop where
  terminal_zero : ∀ s, ROBComplete s → value s = 0
  step_le : ∀ s issue next, ROBStep dep b w s issue next →
    value s ≤ 1 + value next

/-- Telescope the local inequalities along any prefix of a real ROB trace. -/
theorem potential_trace_prefix {n : Nat} {dep : Dependency n} {b w : Nat}
    {value : ROBState n → Nat} (cert : ROBPotential dep b w value)
    {t : TimeAssignment n} (tr : ROBTrace dep b w t) (k : Nat) :
    value (initialROBState n b) ≤ k + value (tr.state k) := by
  induction k with
  | zero =>
    simpa only [Nat.zero_add, trace_initial_eq tr] using
      Nat.le_refl (value (initialROBState n b))
  | succ k ih =>
    have hs := cert.step_le (tr.state k) (fun i => t i = k)
      (tr.state (k + 1)) (tr.step k)
    omega

/-- A potential bounds every completion horizon, even if the trace idles. -/
theorem potential_trace_lower_bound {n : Nat} {dep : Dependency n} {b w : Nat}
    {value : ROBState n → Nat} (cert : ROBPotential dep b w value)
    {t : TimeAssignment n} (tr : ROBTrace dep b w t) (k : Nat)
    (hfinished : (tr.state k).retired = n) :
    value (initialROBState n b) ≤ k := by
  have hk := (trace_finished_iff tr k).1 hfinished
  have hz := cert.terminal_zero (tr.state k) ((trace_complete_iff tr k).2 hk)
  have hp := potential_trace_prefix cert tr k
  omega

/-- Bridge the operational proof to the existing global feasibility predicate. -/
theorem potential_feasible_lower_bound {n : Nat} {dep : Dependency n} {b w k : Nat}
    {value : ROBState n → Nat} (cert : ROBPotential dep b w value)
    (hk : Feasible dep b w k) : value (initialROBState n b) ≤ k := by
  obtain ⟨t, tr, hfinished⟩ := (feasible_iff_finished_trace dep b w k).1 hk
  exact potential_trace_lower_bound cert tr k hfinished

/-- A schedule attaining any verified potential is globally optimal. -/
theorem potential_witness_optimal {n : Nat} {dep : Dependency n} {b w k : Nat}
    {value : ROBState n → Nat} (cert : ROBPotential dep b w value)
    (hk : Feasible dep b w k) (heq : value (initialROBState n b) = k) :
    Optimal dep b w k := by
  refine ⟨hk, ?_⟩
  intro l hl
  rw [← heq]
  exact potential_feasible_lower_bound cert hl

/-- The witness may be supplied directly as a finishing operational trace. -/
theorem potential_finished_witness_optimal {n : Nat} {dep : Dependency n}
    {b w k : Nat} {value : ROBState n → Nat}
    (cert : ROBPotential dep b w value)
    {t : TimeAssignment n} (tr : ROBTrace dep b w t)
    (hfinished : (tr.state k).retired = n)
    (heq : value (initialROBState n b) = k) : Optimal dep b w k := by
  apply potential_witness_optimal cert _ heq
  exact (feasible_iff_finished_trace dep b w k).2 ⟨t, tr, hfinished⟩

#print axioms trace_initial_eq
#print axioms trace_complete_iff
#print axioms potential_trace_prefix
#print axioms potential_trace_lower_bound
#print axioms potential_feasible_lower_bound
#print axioms potential_witness_optimal
#print axioms potential_finished_witness_optimal

end ILP1
