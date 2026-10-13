import ROBBellman

/-!
# Executable finite-branching bounded search and its optimum certificate

The algorithm here is an actual Lean definition. It permits cycles; a fuel
bound is the only termination mechanism. Its generated transition relation
is literal list membership. Application to an independently specified
relation requires a proved `u ∈ next s ↔ step s u` interface. No such interface
to the Python enumerator, or to a finite ROB-state encoding, is asserted.
-/

namespace ILP1.FiniteSearch

universe u
variable {α : Type u}

/-- An execution finishes after exactly `k` transitions. -/
inductive Finishes (step : α → α → Prop) (goal : α → Prop) : α → Nat → Prop
  | done {s : α} : goal s → Finishes step goal s 0
  | move {s t : α} {k : Nat} :
      step s t → Finishes step goal t k → Finishes step goal s (k + 1)

/-- Exhaustive bounded reachability over the supplied complete successor list. -/
def within (goal : α → Bool) (next : α → List α) : Nat → α → Bool
  | 0, s => goal s
  | k + 1, s => goal s || (next s).any (within goal next k)

/-- Soundness and completeness, with no acyclicity or non-idling assumption. -/
theorem within_iff (goal : α → Bool) (next : α → List α) (fuel : Nat) (s : α) :
    within goal next fuel s = true ↔
      ∃ k, k ≤ fuel ∧ Finishes (fun a z => z ∈ next a) (fun a => goal a = true) s k := by
  induction fuel generalizing s with
  | zero =>
    change goal s = true ↔ _
    constructor
    · intro h
      exact ⟨0, Nat.le_refl 0, Finishes.done h⟩
    · rintro ⟨k, hk, h⟩
      have hk0 : k = 0 := by omega
      subst k
      cases h with
      | done hgoal => exact hgoal
  | succ fuel ih =>
    simp only [within, Bool.or_eq_true, List.any_eq_true]
    constructor
    · intro h
      rcases h with hgoal | ⟨t, hmem, ht⟩
      · exact ⟨0, Nat.zero_le _, Finishes.done hgoal⟩
      · obtain ⟨k, hk, hfinish⟩ := (ih t).1 ht
        exact ⟨k + 1, by omega, Finishes.move hmem hfinish⟩
    · rintro ⟨k, hk, h⟩
      cases h with
      | done hgoal => exact Or.inl hgoal
      | @move a t k hmem hfinish =>
        exact Or.inr ⟨t, hmem, (ih t).2 ⟨k, by omega, hfinish⟩⟩

/-- Search all horizons from zero through the bound, retaining the first hit. -/
def firstTrue (p : Nat → Bool) : Nat → Option Nat
  | 0 => if p 0 then some 0 else none
  | k + 1 => match firstTrue p k with
    | some m => some m
    | none => if p (k + 1) then some (k + 1) else none

def FirstSpec (p : Nat → Bool) (bound : Nat) : Option Nat → Prop
  | none => ∀ j, j ≤ bound → p j = false
  | some m => m ≤ bound ∧ p m = true ∧ ∀ j, p j = true → m ≤ j

/-- First-hit search both excludes earlier answers and detects bounded failure. -/
theorem firstTrue_spec (p : Nat → Bool) (bound : Nat) :
    FirstSpec p bound (firstTrue p bound) := by
  induction bound with
  | zero =>
    cases hp : p 0 with
    | false =>
      simp only [firstTrue, hp, Bool.false_eq_true, ↓reduceIte, FirstSpec]
      intro j hj
      have hj0 : j = 0 := by omega
      simpa only [hj0] using hp
    | true =>
      simp only [firstTrue, hp, ↓reduceIte, FirstSpec]
      exact ⟨Nat.le_refl _, True.intro, fun j _ => Nat.zero_le j⟩
  | succ bound ih =>
    cases hprev : firstTrue p bound with
    | some m =>
      have hm : m ≤ bound ∧ p m = true ∧ ∀ j, p j = true → m ≤ j := by
        simpa only [hprev, FirstSpec] using ih
      simp only [firstTrue, hprev, FirstSpec]
      exact ⟨by omega, hm.2.1, hm.2.2⟩
    | none =>
      have hn : ∀ j, j ≤ bound → p j = false := by
        simpa only [hprev, FirstSpec] using ih
      cases hp : p (bound + 1) with
      | false =>
        simp only [firstTrue, hprev, hp, Bool.false_eq_true, ↓reduceIte, FirstSpec]
        intro j hj
        by_cases hjb : j ≤ bound
        · exact hn j hjb
        · have hjexact : j = bound + 1 := by omega
          simpa only [hjexact] using hp
      | true =>
        simp only [firstTrue, hprev, hp, ↓reduceIte, FirstSpec]
        refine ⟨Nat.le_refl _, True.intro, ?_⟩
        intro j hj
        by_cases hbj : bound + 1 ≤ j
        · exact hbj
        · have hfalse := hn j (by omega)
          rw [hj] at hfalse
          cases hfalse

def exactSearch (goal : α → Bool) (next : α → List α) (bound : Nat) (s : α) : Option Nat :=
  firstTrue (fun k => within goal next k s) bound

/-- The returned horizon admits a finishing execution and is globally minimal,
not merely minimal among the searched horizons. -/
theorem exactSearch_sound {goal : α → Bool} {next : α → List α} {bound m : Nat}
    {s : α} (hresult : exactSearch goal next bound s = some m) :
    m ≤ bound ∧
      Finishes (fun a z => z ∈ next a) (fun a => goal a = true) s m ∧
      ∀ k, Finishes (fun a z => z ∈ next a) (fun a => goal a = true) s k → m ≤ k := by
  have hspec := firstTrue_spec (fun k => within goal next k s) bound
  change FirstSpec _ _ (exactSearch goal next bound s) at hspec
  rw [hresult] at hspec
  rcases hspec with ⟨hmb, hfound, hmin⟩
  obtain ⟨k, hkm, hk⟩ := (within_iff goal next m s).1 hfound
  have hmk := hmin k ((within_iff goal next k s).2 ⟨k, Nat.le_refl _, hk⟩)
  have hkeq : k = m := by omega
  subst k
  refine ⟨hmb, hk, ?_⟩
  intro l hl
  exact hmin l ((within_iff goal next l s).2 ⟨l, Nat.le_refl _, hl⟩)

/-- Every witness within the supplied bound forces search success. -/
theorem exactSearch_complete {goal : α → Bool} {next : α → List α} {bound k : Nat}
    {s : α} (hk : k ≤ bound)
    (hfinish : Finishes (fun a z => z ∈ next a) (fun a => goal a = true) s k) :
    ∃ m, exactSearch goal next bound s = some m := by
  have hspec := firstTrue_spec (fun l => within goal next l s) bound
  change FirstSpec _ _ (exactSearch goal next bound s) at hspec
  cases hresult : exactSearch goal next bound s with
  | some m => exact ⟨m, rfl⟩
  | none =>
    rw [hresult] at hspec
    have hf := hspec k hk
    have ht := (within_iff goal next k s).2 ⟨k, Nat.le_refl _, hfinish⟩
    change within goal next k s = false at hf
    rw [ht] at hf
    cases hf

/-- A failed bounded search is a complete exclusion certificate for that bound. -/
theorem exactSearch_none_iff {goal : α → Bool} {next : α → List α} {bound : Nat}
    {s : α} : exactSearch goal next bound s = none ↔
      ∀ k, k ≤ bound → ¬ Finishes (fun a z => z ∈ next a) (fun a => goal a = true) s k := by
  constructor
  · intro hn k hk hf
    obtain ⟨m, hm⟩ := exactSearch_complete hk hf
    rw [hn] at hm
    cases hm
  · intro hn
    cases hr : exactSearch goal next bound s with
    | none => rfl
    | some m =>
      have hs := exactSearch_sound hr
      exact False.elim (hn m hs.1 hs.2.1)

/-- Transport generated paths to an externally specified complete relation. -/
theorem finishes_iff_of_enumeration {next : α → List α} {step : α → α → Prop}
    {goal : α → Prop} (enumeration : ∀ s t, t ∈ next s ↔ step s t) (s : α) (k : Nat) :
    Finishes (fun a z => z ∈ next a) goal s k ↔ Finishes step goal s k := by
  constructor
  · intro h
    induction h with
    | done hg => exact Finishes.done hg
    | @move s t k hst _ ih => exact Finishes.move ((enumeration s t).1 hst) ih
  · intro h
    induction h with
    | done hg => exact Finishes.done hg
    | @move s t k hst _ ih => exact Finishes.move ((enumeration s t).2 hst) ih

/-- Explicit final API: successor coverage is a checked premise, never inferred
from tests. The returned answer is optimal for every path in `step`. -/
theorem exactSearch_optimal_of_enumeration {goal : α → Bool} {next : α → List α}
    {step : α → α → Prop} {bound m : Nat} {s : α}
    (enumeration : ∀ a z, z ∈ next a ↔ step a z)
    (hresult : exactSearch goal next bound s = some m) :
    m ≤ bound ∧ Finishes step (fun a => goal a = true) s m ∧
      ∀ k, Finishes step (fun a => goal a = true) s k → m ≤ k := by
  obtain ⟨hmb, hf, hmin⟩ := exactSearch_sound hresult
  refine ⟨hmb, (finishes_iff_of_enumeration enumeration s m).1 hf, ?_⟩
  intro k hk
  exact hmin k ((finishes_iff_of_enumeration enumeration s k).2 hk)

#print axioms within_iff
#print axioms firstTrue_spec
#print axioms exactSearch_sound
#print axioms exactSearch_complete
#print axioms exactSearch_none_iff
#print axioms finishes_iff_of_enumeration
#print axioms exactSearch_optimal_of_enumeration

end ILP1.FiniteSearch
