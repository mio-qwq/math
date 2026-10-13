import FiniteSearch

/-!
# Exact Bellman certificates without an acyclic whole-state-space premise

A potential need not decrease on every allowed transition. A lower-bound
inequality must cover every transition, while one attaining successor is
required from each nonterminal state. The attaining path then terminates by
induction on the natural-number potential. Other edges may contain cycles.
-/

namespace ILP1.FiniteSearch

universe u
variable {α : Type u}

structure ExactBellman (step : α → α → Prop) (goal : α → Prop)
    (value : α → Nat) : Prop where
  terminal_zero : ∀ s, goal s → value s = 0
  step_le : ∀ s t, step s t → value s ≤ 1 + value t
  attaining : ∀ s, ¬ goal s → ∃ t, step s t ∧ value s = 1 + value t

/-- Every path is bounded below, including paths using cycles or idling. -/
theorem exactBellman_path_lower {step : α → α → Prop} {goal : α → Prop}
    {value : α → Nat} (cert : ExactBellman step goal value) {s : α} {k : Nat}
    (path : Finishes step goal s k) : value s ≤ k := by
  induction path with
  | @done s hs =>
    rw [cert.terminal_zero s hs]
    exact Nat.le_refl 0
  | @move s t k hst _ ih =>
    have hstep := cert.step_le s t hst
    omega

/-- Local attainment gives a genuine finite finishing witness. This is an
induction on the potential, not an assumption of a pre-existing optimal path. -/
theorem exactBellman_path_attains {step : α → α → Prop} {goal : α → Prop}
    {value : α → Nat} (cert : ExactBellman step goal value) (s : α) :
    Finishes step goal s (value s) := by
  have aux : ∀ k, ∀ s, value s = k → Finishes step goal s k := by
    intro k
    induction k using Nat.strongRecOn with
    | ind k ih =>
      intro s hsk
      by_cases hg : goal s
      · have hz := cert.terminal_zero s hg
        have hk0 : k = 0 := by omega
        rw [hk0]
        exact Finishes.done hg
      · obtain ⟨t, hst, hat⟩ := cert.attaining s hg
        have hlt : value t < k := by omega
        have ht := ih (value t) hlt t rfl
        have hp := Finishes.move hst ht
        have heq : value t + 1 = k := by omega
        simpa only [heq] using hp
  exact aux (value s) s rfl

/-- Thus a locally verified Bellman table gives the exact global minimum. -/
theorem exactBellman_optimum {step : α → α → Prop} {goal : α → Prop}
    {value : α → Nat} (cert : ExactBellman step goal value) (s : α) :
    Finishes step goal s (value s) ∧
      ∀ k, Finishes step goal s k → value s ≤ k := by
  exact ⟨exactBellman_path_attains cert s, fun _ h => exactBellman_path_lower cert h⟩

/-- Local zero values cannot spuriously terminate a nonterminal state. -/
theorem exactBellman_zero_iff {step : α → α → Prop} {goal : α → Prop}
    {value : α → Nat} (cert : ExactBellman step goal value) (s : α) :
    value s = 0 ↔ goal s := by
  constructor
  · intro hz
    apply Classical.byContradiction
    intro hng
    obtain ⟨_, _, hat⟩ := cert.attaining s hng
    omega
  · exact cert.terminal_zero s

/-- Two verified exact Bellman tables necessarily agree at every state. -/
theorem exactBellman_unique {step : α → α → Prop} {goal : α → Prop}
    {value other : α → Nat} (cert : ExactBellman step goal value)
    (cert' : ExactBellman step goal other) (s : α) : value s = other s := by
  have hvo := exactBellman_path_lower cert (exactBellman_path_attains cert' s)
  have hov := exactBellman_path_lower cert' (exactBellman_path_attains cert s)
  omega

/-- A verified enumeration and a sufficient horizon reproduce the exact table.
Enumeration completeness remains an explicit, indispensable interface. -/
theorem exactSearch_eq_bellman {step : α → α → Prop} {goal : α → Bool}
    {next : α → List α} {value : α → Nat}
    (cert : ExactBellman step (fun a => goal a = true) value)
    (enumeration : ∀ s t, t ∈ next s ↔ step s t) {s : α} {bound : Nat}
    (hbound : value s ≤ bound) : exactSearch goal next bound s = some (value s) := by
  have hp := exactBellman_path_attains cert s
  have hgen := (finishes_iff_of_enumeration enumeration s (value s)).2 hp
  obtain ⟨m, hm⟩ := exactSearch_complete hbound hgen
  obtain ⟨_, hmf, hmin⟩ := exactSearch_optimal_of_enumeration enumeration hm
  have hvm := exactBellman_path_lower cert hmf
  have hmv := hmin (value s) hp
  have hmeq : m = value s := by omega
  simpa only [hmeq] using hm

#print axioms exactBellman_path_lower
#print axioms exactBellman_path_attains
#print axioms exactBellman_optimum
#print axioms exactBellman_zero_iff
#print axioms exactBellman_unique
#print axioms exactSearch_eq_bellman

end ILP1.FiniteSearch
