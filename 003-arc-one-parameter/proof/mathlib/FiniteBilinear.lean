import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Algebra.BigOperators.Group.Finset.Sigma

/-!
# Associativity from finite structure constants

This independent generic theorem works over every commutative semiring.
It does not assert that the sparse ARC table has already been converted
to its finite contraction hypothesis. That bridge remains separate.
-/

namespace ARCFiniteBilinear

open scoped BigOperators

variable {R I : Type*} [CommSemiring R] [Fintype I]

noncomputable section

/-- Bilinear multiplication specified by finite structure constants. -/
def mul (B : I → I → I → R) (u v : I → R) : I → R :=
  fun k => ∑ a, ∑ b, u a * v b * B a b k

/-- The usual finite contraction identity for associativity of basis products. -/
def StructureAssociative (B : I → I → I → R) : Prop :=
  ∀ a b c k, (∑ j, B a b j * B j c k) = ∑ j, B b c j * B a j k

private theorem sum4_reorder_left (f : I → I → I → I → R) :
    (∑ j, ∑ c, ∑ a, ∑ b, f a b c j) = ∑ a, ∑ b, ∑ c, ∑ j, f a b c j := by
  classical
  calc
    _ = ∑ c, ∑ j, ∑ a, ∑ b, f a b c j := Finset.sum_comm
    _ = ∑ c, ∑ a, ∑ j, ∑ b, f a b c j := by
      apply Finset.sum_congr rfl
      intro c hc
      exact Finset.sum_comm
    _ = ∑ a, ∑ c, ∑ j, ∑ b, f a b c j := Finset.sum_comm
    _ = ∑ a, ∑ c, ∑ b, ∑ j, f a b c j := by
      apply Finset.sum_congr rfl
      intro a ha
      apply Finset.sum_congr rfl
      intro c hc
      exact Finset.sum_comm
    _ = ∑ a, ∑ b, ∑ c, ∑ j, f a b c j := by
      apply Finset.sum_congr rfl
      intro a ha
      exact Finset.sum_comm

private theorem sum4_reorder_right (f : I → I → I → I → R) :
    (∑ a, ∑ j, ∑ b, ∑ c, f a b c j) = ∑ a, ∑ b, ∑ c, ∑ j, f a b c j := by
  classical
  apply Finset.sum_congr rfl
  intro a ha
  calc
    _ = ∑ b, ∑ j, ∑ c, f a b c j := Finset.sum_comm
    _ = ∑ b, ∑ c, ∑ j, f a b c j := by
      apply Finset.sum_congr rfl
      intro b hb
      exact Finset.sum_comm

theorem mul_left_expansion (B : I → I → I → R) (u v w : I → R) (k : I) :
    mul B (mul B u v) w k =
      ∑ a, ∑ b, ∑ c, (u a * v b * w c) * (∑ j, B a b j * B j c k) := by
  classical
  calc
    _ = ∑ j, ∑ c, ∑ a, ∑ b, (u a * v b * B a b j) * w c * B j c k := by
      simp only [mul, Finset.sum_mul]
    _ = ∑ a, ∑ b, ∑ c, ∑ j, (u a * v b * B a b j) * w c * B j c k :=
      sum4_reorder_left _
    _ = _ := by
      apply Finset.sum_congr rfl
      intro a ha
      apply Finset.sum_congr rfl
      intro b hb
      apply Finset.sum_congr rfl
      intro c hc
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro j hj
      ac_rfl

theorem mul_right_expansion (B : I → I → I → R) (u v w : I → R) (k : I) :
    mul B u (mul B v w) k =
      ∑ a, ∑ b, ∑ c, (u a * v b * w c) * (∑ j, B b c j * B a j k) := by
  classical
  calc
    _ = ∑ a, ∑ j, ∑ b, ∑ c, (u a * (v b * w c * B b c j)) * B a j k := by
      simp only [mul, Finset.mul_sum, Finset.sum_mul]
    _ = ∑ a, ∑ b, ∑ c, ∑ j, (u a * (v b * w c * B b c j)) * B a j k :=
      sum4_reorder_right _
    _ = _ := by
      apply Finset.sum_congr rfl
      intro a ha
      apply Finset.sum_congr rfl
      intro b hb
      apply Finset.sum_congr rfl
      intro c hc
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro j hj
      ac_rfl

/-- Basis contraction identities imply associativity for all finite vectors. -/
theorem mul_associative (B : I → I → I → R) (hB : StructureAssociative B)
    (u v w : I → R) : mul B (mul B u v) w = mul B u (mul B v w) := by
  funext k
  rw [mul_left_expansion, mul_right_expansion]
  apply Finset.sum_congr rfl
  intro a ha
  apply Finset.sum_congr rfl
  intro b hb
  apply Finset.sum_congr rfl
  intro c hc
  rw [hB a b c k]

#print axioms mul_associative

end
end ARCFiniteBilinear
