import Std

/-!
The abstract four-phase collapse and odd support-count obstruction.
The phase laws are explicit structure fields, not new Lean axioms.
The passage from actual complex row ratios to these hypotheses is not yet
formalized here; see the analytical proof in paper.md, Section 3.
-/

namespace OddHalfOrder.Support

/-- Exactly the algebraic laws needed in the four-phase argument. -/
structure PhaseCancellation (α : Type) where
  one : α
  mul : α → α → α
  right_identity : ∀ x, mul x one = x
  left_cancel : ∀ x y z, mul x y = mul x z → y = z

/-- A list has no three pairwise distinct values. -/
def AtMostTwo {α : Type} (values : List α) : Prop :=
  ∀ a b c, a ∈ values → b ∈ values → c ∈ values →
    a = b ∨ a = c ∨ b = c

theorem four_phase_collapse {α : Type} (g : PhaseCancellation α)
    (x y : α) (hx : x ≠ g.one) (hy : y ≠ g.one)
    (hsmall : AtMostTwo [g.one, x, y, g.mul x y]) :
    y = x ∧ g.mul x y = g.one := by
  have hxy : y = x := by
    have h := hsmall g.one x y (by simp) (by simp) (by simp)
    rcases h with h | h | h
    · exact False.elim (hx h.symm)
    · exact False.elim (hy h.symm)
    · exact h.symm
  have hproduct : g.mul x y = g.one := by
    have h := hsmall g.one x (g.mul x y) (by simp) (by simp) (by simp)
    rcases h with h | h | h
    · exact False.elim (hx h.symm)
    · exact h.symm
    · have heq : g.mul x y = g.mul x g.one := by
        rw [g.right_identity]
        exact h.symm
      have hyone := g.left_cancel x y g.one heq
      exact False.elim (hy hyone)
  exact ⟨hxy, hproduct⟩

def weightedCount {α : Type} [DecidableEq α] (target : α) : List (α × Nat) → Nat
  | [] => 0
  | (value, multiplicity) :: rest =>
      (if value = target then multiplicity else 0) + weightedCount target rest

/-- The two complementary intersection blocks both have phase one. -/
theorem four_phase_one_count {α : Type} [DecidableEq α]
    (g : PhaseCancellation α) (x y : α)
    (hx : x ≠ g.one) (hy : y ≠ g.one)
    (hsmall : AtMostTwo [g.one, x, y, g.mul x y]) (m t : Nat) :
    weightedCount g.one
      [(g.one, t), (x, m - t), (y, m - t), (g.mul x y, t)] = 2 * t := by
  have hproduct := (four_phase_collapse g x y hx hy hsmall).2
  simp [weightedCount, hx, hy, hproduct, Nat.mul_comm, Nat.mul_two]

/-- The entire abstract support intersection argument, for every odd m. -/
theorem mismatched_support_obstruction {α : Type} [DecidableEq α]
    (g : PhaseCancellation α) (x y : α) (m t : Nat)
    (hx : x ≠ g.one) (hy : y ≠ g.one)
    (hodd : ∃ s : Nat, m = 2 * s + 1)
    (hsmall : AtMostTwo [g.one, x, y, g.mul x y]) :
    weightedCount g.one
      [(g.one, t), (x, m - t), (y, m - t), (g.mul x y, t)] ≠ m := by
  rw [four_phase_one_count g x y hx hy hsmall]
  obtain ⟨s, hs⟩ := hodd
  omega

#print axioms four_phase_collapse
#print axioms four_phase_one_count
#print axioms mismatched_support_obstruction

end OddHalfOrder.Support
