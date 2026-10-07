import FiniteBilinear

/-!
# Units from finite basis contractions

For any finite coordinate set and any commutative semiring, a vector whose
structure-constant contractions are the Kronecker delta is a left or right
unit for the corresponding bilinear multiplication. No specific table,
enumeration, associativity assumption, or characteristic restriction is used.
-/

namespace ARCFiniteBilinear

open scoped BigOperators

variable {R I : Type*} [CommSemiring R] [Fintype I] [DecidableEq I]

noncomputable section

/-- Contracting the first basis slot with `E` gives the identity matrix. -/
def StructureLeftUnit (B : I → I → I → R) (E : I → R) : Prop :=
  ∀ b k, (∑ a, E a * B a b k) = if b = k then 1 else 0

/-- Contracting the second basis slot with `E` gives the identity matrix. -/
def StructureRightUnit (B : I → I → I → R) (E : I → R) : Prop :=
  ∀ a k, (∑ b, E b * B a b k) = if a = k then 1 else 0

/-- Every first-slot contraction identity extends from the basis to all vectors. -/
theorem mul_left_unit_of_contraction (B : I → I → I → R) (E : I → R)
    (hE : ∀ b k, (∑ a, E a * B a b k) = if b = k then 1 else 0)
    (v : I → R) : mul B E v = v := by
  funext k
  calc
    mul B E v k = ∑ b, ∑ a, E a * v b * B a b k := by
      exact Finset.sum_comm
    _ = ∑ b, v b * (∑ a, E a * B a b k) := by
      apply Finset.sum_congr rfl
      intro b hb
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro a ha
      ac_rfl
    _ = ∑ b, v b * (if b = k then 1 else 0) := by
      apply Finset.sum_congr rfl
      intro b hb
      rw [hE b k]
    _ = v k := by simp

/-- Every second-slot contraction identity extends from the basis to all vectors. -/
theorem mul_right_unit_of_contraction (B : I → I → I → R) (E : I → R)
    (hE : ∀ a k, (∑ b, E b * B a b k) = if a = k then 1 else 0)
    (v : I → R) : mul B v E = v := by
  funext k
  calc
    mul B v E k = ∑ a, v a * (∑ b, E b * B a b k) := by
      dsimp [mul]
      apply Finset.sum_congr rfl
      intro a ha
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro b hb
      ac_rfl
    _ = ∑ a, v a * (if a = k then 1 else 0) := by
      apply Finset.sum_congr rfl
      intro a ha
      rw [hE a k]
    _ = v k := by simp

theorem mul_left_unit (B : I → I → I → R) (E : I → R)
    (hE : StructureLeftUnit B E) (v : I → R) : mul B E v = v :=
  mul_left_unit_of_contraction B E hE v

theorem mul_right_unit (B : I → I → I → R) (E : I → R)
    (hE : StructureRightUnit B E) (v : I → R) : mul B v E = v :=
  mul_right_unit_of_contraction B E hE v

/-- Separate left and right basis contractions give a two-sided unit on all vectors. -/
theorem mul_two_sided_unit (B : I → I → I → R) (E : I → R)
    (hleft : StructureLeftUnit B E) (hright : StructureRightUnit B E)
    (v : I → R) : mul B E v = v ∧ mul B v E = v :=
  ⟨mul_left_unit B E hleft v, mul_right_unit B E hright v⟩

#print axioms mul_left_unit_of_contraction
#print axioms mul_right_unit_of_contraction
#print axioms mul_left_unit
#print axioms mul_right_unit
#print axioms mul_two_sided_unit

end
end ARCFiniteBilinear
