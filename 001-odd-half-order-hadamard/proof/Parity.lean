import Std

/-
The integer obstructions used in the analytic proof in ../paper.md.
This file does NOT formalize the complex-matrix or Newton-identity arguments.
It uses Lean's bundled library only, with no additional dependencies.
-/

namespace OddHalfOrder

def IsOdd (m : Nat) : Prop := ∃ s : Nat, m = 2 * s + 1

theorem odd_not_twice (m r : Nat) (hodd : IsOdd m) : m ≠ 2 * r := by
  obtain ⟨s, hs⟩ := hodd
  omega

theorem support_multiplicity_obstruction (m t : Nat)
    (hodd : IsOdd m) : 2 * t ≠ m := by
  intro h
  exact odd_not_twice m t hodd h.symm

/-- If a rank r satisfies the cleared trace equation, odd m is impossible. -/
theorem projection_trace_obstruction (m r : Nat)
    (hm : 0 < m) (hodd : IsOdd m) : 2 * m * r ≠ m * m := by
  intro htrace
  have hcancel : m * (2 * r) = m * m := by
    simpa only [Nat.mul_comm 2 m, Nat.mul_assoc] using htrace
  have heq : 2 * r = m := Nat.eq_of_mul_eq_mul_left hm hcancel
  exact odd_not_twice m r hodd heq.symm

#print axioms odd_not_twice
#print axioms support_multiplicity_obstruction
#print axioms projection_trace_obstruction

end OddHalfOrder
