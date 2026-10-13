import ROBOperational

/-!
A deliberately elementary executable exact solver, independent of the Python
solvers. It exhaustively enumerates assignments to finite time/lane slots.
Theorems quantify over arbitrary finite job counts, windows, widths and bounds.
No efficiency or novelty claim is attached to exhaustive enumeration.
-/

namespace ILP1
namespace ExactEnumeration

def assignments {α : Type} : (n : Nat) → List α → List (Fin n → α)
  | 0, _ => [fun i => Fin.elim0 i]
  | n + 1, domain =>
      domain.flatMap fun a => (assignments n domain).map fun f => Fin.cases a f

theorem assignments_complete {α : Type} {n : Nat} (domain : List α)
    (f : Fin n → α) (hf : ∀ i, f i ∈ domain) : f ∈ assignments n domain := by
  induction n with
  | zero =>
    have heq : f = (fun i : Fin 0 => Fin.elim0 i) := by
      funext i
      exact Fin.elim0 i
    simp only [assignments, List.mem_singleton, heq]
  | succ n ih =>
    apply List.mem_flatMap.mpr
    refine ⟨f 0, hf 0, ?_⟩
    apply List.mem_map.mpr
    refine ⟨fun i => f i.succ, ih (fun i => f i.succ) (fun i => hf i.succ), ?_⟩
    funext i
    exact Fin.cases rfl (fun _ => rfl) i

def slots (k w : Nat) : List (Fin k × Fin w) :=
  (List.finRange k).flatMap fun c => (List.finRange w).map fun lane => (c, lane)

theorem mem_slots {k w : Nat} (a : Fin k × Fin w) : a ∈ slots k w := by
  apply List.mem_flatMap.mpr
  exact ⟨a.1, List.mem_finRange a.1,
    List.mem_map.mpr ⟨a.2, List.mem_finRange a.2, rfl⟩⟩

abbrev BoolDependency (n : Nat) := Fin n → Fin n → Bool

def toDependency {n : Nat} (dep : BoolDependency n) : Dependency n :=
  fun i j => dep i j = true

def slotCheck {n k w : Nat} (dep : BoolDependency n) (b : Nat)
    (f : Fin n → Fin k × Fin w) : Bool :=
  decide ((∀ i j, dep i j = true ∨ i.val + b ≤ j.val → (f i).1.val < (f j).1.val) ∧
    (∀ i j, (f i).1.val = (f j).1.val → (f i).2.val = (f j).2.val → i = j))

def feasibleCheck {n : Nat} (dep : BoolDependency n) (b w k : Nat) : Bool :=
  (assignments n (slots k w)).any (slotCheck dep b)

theorem slotCheck_sound {n k w : Nat} {dep : BoolDependency n} {b : Nat}
    {f : Fin n → Fin k × Fin w} (hf : slotCheck dep b f = true) :
    Legal (toDependency dep) b w (fun i => (f i).1.val) := by
  have hp : (∀ i j, dep i j = true ∨ i.val + b ≤ j.val → (f i).1.val < (f j).1.val) ∧
      (∀ i j, (f i).1.val = (f j).1.val → (f i).2.val = (f j).2.val → i = j) :=
    of_decide_eq_true hf
  refine ⟨?_, ?_, ?_⟩
  · intro i j hij
    exact hp.1 i j (Or.inl hij)
  · apply (windowEdges_iff_canonicalROB _ b).1
    intro i j hij
    exact hp.1 i j (Or.inr hij)
  · exact ⟨fun i => (f i).2.val, fun i => (f i).2.isLt, hp.2⟩

theorem feasibleCheck_iff {n : Nat} (dep : BoolDependency n) (b w k : Nat) :
    feasibleCheck dep b w k = true ↔ Feasible (toDependency dep) b w k := by
  constructor
  · intro h
    obtain ⟨f, _, hf⟩ := List.any_eq_true.mp h
    exact ⟨fun i => (f i).1.val, slotCheck_sound hf, fun i => (f i).1.isLt⟩
  · rintro ⟨t, h, hk⟩
    obtain ⟨lane, hl, hinj⟩ := h.2.2
    let f : Fin n → Fin k × Fin w := fun i => (⟨t i, hk i⟩, ⟨lane i, hl i⟩)
    apply List.any_eq_true.mpr
    refine ⟨f, assignments_complete (slots k w) f (fun i => mem_slots (f i)), ?_⟩
    apply decide_eq_true
    refine ⟨?_, ?_⟩
    · intro i j hij
      rcases hij with hd | hb
      · exact h.1 i j hd
      · exact (windowEdges_iff_canonicalROB t b).2 h.2.1 i j hb
    · intro i j ht hle
      exact hinj i j ht hle

def firstTrue (p : Nat → Bool) : Nat → Option Nat
  | 0 => if p 0 then some 0 else none
  | m + 1 =>
      match firstTrue p m with
      | some k => some k
      | none => if p (m + 1) then some (m + 1) else none

theorem firstTrue_none {p : Nat → Bool} {m : Nat} (h : firstTrue p m = none) :
    ∀ j, j ≤ m → p j = false := by
  induction m with
  | zero =>
    intro j hj
    have hj0 : j = 0 := by omega
    subst j
    cases hp : p 0 <;> simp_all [firstTrue]
  | succ m ih =>
    cases he : firstTrue p m with
    | some k => simp [firstTrue, he] at h
    | none =>
      have hsmall := ih he
      intro j hj
      by_cases hjm : j ≤ m
      · exact hsmall j hjm
      · have hje : j = m + 1 := by omega
        subst j
        cases hp : p (m + 1) <;> simp_all [firstTrue]

theorem firstTrue_some {p : Nat → Bool} {m k : Nat} (h : firstTrue p m = some k) :
    p k = true ∧ k ≤ m ∧ ∀ j, j < k → p j = false := by
  induction m with
  | zero =>
    cases hp : p 0 with
    | false => simp [firstTrue, hp] at h
    | true =>
      have hk : k = 0 := by simpa [firstTrue, hp] using h.symm
      subst k
      exact ⟨hp, Nat.le_refl 0, fun j hj => False.elim (Nat.not_lt_zero j hj)⟩
  | succ m ih =>
    cases he : firstTrue p m with
    | some l =>
      have hlk : l = k := by simpa [firstTrue, he] using h
      subst l
      obtain ⟨hp, hkm, hmin⟩ := ih he
      exact ⟨hp, by omega, hmin⟩
    | none =>
      have hsmall := firstTrue_none he
      cases hp : p (m + 1) with
      | false => simp [firstTrue, he, hp] at h
      | true =>
        have hk : k = m + 1 := by simpa [firstTrue, he, hp] using h.symm
        subst k
        exact ⟨hp, Nat.le_refl _, fun j hj => hsmall j (by omega)⟩

def optimalSearch {n : Nat} (dep : BoolDependency n) (b w : Nat) : Option Nat :=
  firstTrue (feasibleCheck dep b w) n

theorem optimalSearch_sound {n : Nat} {dep : BoolDependency n} {b w k : Nat}
    (h : optimalSearch dep b w = some k) : Optimal (toDependency dep) b w k := by
  obtain ⟨hf, _, hmin⟩ := firstTrue_some h
  refine ⟨(feasibleCheck_iff dep b w k).1 hf, ?_⟩
  intro l hl
  apply Classical.byContradiction
  intro hkl
  have hp := hmin l (by omega)
  have hq := (feasibleCheck_iff dep b w l).2 hl
  simp [hp] at hq

theorem optimalSearch_complete {n : Nat} {dep : BoolDependency n}
    (hd : Forward (toDependency dep)) {b w : Nat} (hb : 0 < b) (hw : 0 < w) :
    ∃ k, optimalSearch dep b w = some k ∧ Optimal (toDependency dep) b w k := by
  have hserial := (feasibleCheck_iff dep b w n).2 (feasible_serial hd hb hw)
  cases hs : optimalSearch dep b w with
  | none =>
    have hnone := firstTrue_none hs n (Nat.le_refl n)
    simp [hnone] at hserial
  | some k => exact ⟨k, rfl, optimalSearch_sound hs⟩

def scheduleAt {n : Nat} (dep : BoolDependency n) (b w k : Nat) :
    Option (Fin n → Fin k × Fin w) :=
  (assignments n (slots k w)).find? (slotCheck dep b)

theorem scheduleAt_some_iff {n : Nat} (dep : BoolDependency n) (b w k : Nat) :
    (scheduleAt dep b w k).isSome = true ↔ Feasible (toDependency dep) b w k := by
  unfold scheduleAt
  rw [List.isSome_find?]
  exact feasibleCheck_iff dep b w k

theorem scheduleAt_sound {n k w : Nat} {dep : BoolDependency n} {b : Nat}
    {f : Fin n → Fin k × Fin w} (h : scheduleAt dep b w k = some f) :
    Legal (toDependency dep) b w (fun i => (f i).1.val) :=
  slotCheck_sound (List.find?_some h)

structure Solution (n : Nat) where
  horizon : Nat
  time : Fin n → Nat
  lane : Fin n → Nat

def decode {n k w : Nat} (f : Fin n → Fin k × Fin w) : Solution n :=
  ⟨k, fun i => (f i).1.val, fun i => (f i).2.val⟩

def solve {n : Nat} (dep : BoolDependency n) (b w : Nat) : Option (Solution n) := do
  let k ← optimalSearch dep b w
  let f ← scheduleAt dep b w k
  pure (decode f)

theorem solve_sound {n : Nat} {dep : BoolDependency n} {b w : Nat} {s : Solution n}
    (h : solve dep b w = some s) :
    Optimal (toDependency dep) b w s.horizon ∧
      Legal (toDependency dep) b w s.time ∧ (∀ i, s.time i < s.horizon) := by
  cases hs : optimalSearch dep b w with
  | none => simp [solve, hs] at h
  | some k =>
    cases hf : scheduleAt dep b w k with
    | none => simp [solve, hs, hf] at h
    | some f =>
      have heq : decode f = s := by simpa [solve, hs, hf] using h
      subst s
      exact ⟨optimalSearch_sound hs, scheduleAt_sound hf, fun i => (f i).1.isLt⟩

theorem solve_complete {n : Nat} {dep : BoolDependency n}
    (hd : Forward (toDependency dep)) {b w : Nat} (hb : 0 < b) (hw : 0 < w) :
    ∃ s, solve dep b w = some s ∧ Optimal (toDependency dep) b w s.horizon ∧
      Legal (toDependency dep) b w s.time ∧ (∀ i, s.time i < s.horizon) := by
  obtain ⟨k, hk, hopt⟩ := optimalSearch_complete hd hb hw
  have hf := (scheduleAt_some_iff dep b w k).2 hopt.1
  cases he : scheduleAt dep b w k with
  | none => simp [he] at hf
  | some f =>
    have hs : solve dep b w = some (decode f) := by simp [solve, hk, he]
    exact ⟨decode f, hs, solve_sound hs⟩

#print axioms assignments_complete
#print axioms mem_slots
#print axioms slotCheck_sound
#print axioms feasibleCheck_iff
#print axioms firstTrue_none
#print axioms firstTrue_some
#print axioms optimalSearch_sound
#print axioms optimalSearch_complete
#print axioms scheduleAt_some_iff
#print axioms scheduleAt_sound
#print axioms solve_sound
#print axioms solve_complete

-- Actual executions of the verified algorithm; these are demonstrations,
-- not substitutes for the universal soundness and completeness theorems.
#eval (solve (n := 0) (fun _ _ => false) 1 1).map (fun s => s.horizon)
#eval (solve (n := 4) (fun i j => i.val == 1 && j.val == 3) 3 2).map
  (fun s => (s.horizon, (List.finRange 4).map s.time))
#eval (solve (n := 4) (fun i j => i.val + 1 == j.val) 3 2).map
  (fun s => (s.horizon, (List.finRange 4).map s.time))

end ExactEnumeration
end ILP1
