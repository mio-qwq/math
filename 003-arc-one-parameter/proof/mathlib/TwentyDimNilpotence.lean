import TwentyDimAugmentation
import Mathlib.Algebra.BigOperators.Group.List.Defs

/-!
Positive-degree filtration of the explicit table algebra.

The grading is attributed to OpenAI family 199, `03-algebra.tex`, at the
pinned upstream commit recorded in the package attribution. Lower-case
degrees are 0,2,2,4,1,3,1,3,0,2; dual degrees are five minus these degrees.
Only the 400 pairs of the frozen multiplication table are checked here.
The semantic proof then handles arbitrary actual algebra elements and
arbitrarily long lists. No long-word enumeration or identification with
the Jacobson radical is used.
-/

namespace ARCTwentyDimNilpotence

open ARCFiniteCore ARCBitPolynomial ARCTermSemantics ARCFiniteTableContraction
open ARCTwentyDimAssociativity ARCTwentyDimAlgebra ARCTwentyDimAugmentation
open scoped BigOperators

/-- Degrees of e,x,y,z,u,v,t,j,f,n in the attributed positive grading. -/
def cDegree : Nat → Nat
  | 0 => 0
  | 1 => 2
  | 2 => 2
  | 3 => 4
  | 4 => 1
  | 5 => 3
  | 6 => 1
  | 7 => 3
  | 8 => 0
  | 9 => 2
  | _ => 0

/-- The dual label a* has degree five minus the degree of a. -/
def tDegree (a : Nat) : Nat :=
  if a < 10 then cDegree a else 5 - cDegree (a - 10)

/-- Each listed output of a basis product has exactly the sum degree. -/
theorem t_degree_homogeneity : ∀ a b : Fin 20,
    (tTerms a.val b.val).all (fun t =>
      tDegree t.1 = tDegree a.val + tDegree b.val) = true := by
  decide

theorem t_degree_bound : ∀ a : Fin 20, tDegree a.val ≤ 5 := by decide

theorem t_degree_zero_iff : ∀ a : Fin 20,
    tDegree a.val = 0 ↔ a = 0 ∨ a = 8 := by decide

noncomputable section

private theorem sumTerms_zero_no_output (terms : Terms) (k : Nat)
    (h : ∀ t ∈ terms, t.1 ≠ k) : sumTerms terms k = 0 := by
  induction terms with
  | nil => rfl
  | cons t terms ih =>
      have ht := h t (List.mem_cons_self ..)
      have htail : ∀ x ∈ terms, x.1 ≠ k := fun x hx => h x (List.mem_cons_of_mem _ hx)
      simp [sumTerms_cons, singleTerm, Ne.symm ht, ih htail]

/-- Homogeneity of the sparse data gives a genuine polynomial support law. -/
theorem polynomial_constant_degree_zero (a b k : Fin 20)
    (hdeg : tDegree k.val ≠ tDegree a.val + tDegree b.val) :
    tConstants a b k = 0 := by
  have hterms : ∀ t ∈ tTerms a.val b.val,
      tDegree t.1 = tDegree a.val + tDegree b.val := by
    simpa only [List.all_eq_true, decide_eq_true_eq] using t_degree_homogeneity a b
  apply sumTerms_zero_no_output
  intro t ht htk
  apply hdeg
  simpa only [htk] using hterms t ht

variable {R : Type*} [CommRing R] [CharP R 2]

/-- An actual element has degree at least n when all lower-degree
coordinates vanish. No parameter-dependent choice of basis is involved. -/
def InDegreeAtLeast (q : R) (n : Nat) (x : TableAlgebra q) : Prop :=
  ∀ k : Fin 20, tDegree k.val < n → x.coords k = 0

/-- The established augmentation kernel is precisely the positive part. -/
theorem augmentation_kernel_iff_degree_one (q : R) (x : TableAlgebra q) :
    InAugmentationKernel q x ↔ InDegreeAtLeast q 1 x := by
  rw [augmentation_kernel_iff]
  constructor
  · rintro ⟨h0, h8⟩ k hk
    have hd : tDegree k.val = 0 := by omega
    rcases (t_degree_zero_iff k).mp hd with rfl | rfl
    · exact h0
    · exact h8
  · intro h
    exact ⟨h 0 (by decide), h 8 (by decide)⟩

theorem specialized_constant_degree_zero (q : R) (a b k : Fin 20)
    (hdeg : tDegree k.val ≠ tDegree a.val + tDegree b.val) :
    specializedConstants q a b k = 0 := by
  unfold specializedConstants
  rw [polynomial_constant_degree_zero a b k hdeg, map_zero]

/-- Multiplication of arbitrary actual elements adds filtration indices. -/
theorem degree_mul (q : R) (m n : Nat) (x y : TableAlgebra q)
    (hx : InDegreeAtLeast q m x) (hy : InDegreeAtLeast q n y) :
    InDegreeAtLeast q (m + n) (x * y) := by
  classical
  intro k hk
  rw [coords_mul]
  unfold specializedMul ARCFiniteBilinear.mul
  apply Finset.sum_eq_zero
  intro a _
  apply Finset.sum_eq_zero
  intro b _
  by_cases ha : tDegree a.val < m
  · simp only [hx a ha, zero_mul]
  by_cases hb : tDegree b.val < n
  · simp only [hy b hb, mul_zero, zero_mul]
  have hdeg : tDegree k.val ≠ tDegree a.val + tDegree b.val := by omega
  rw [specialized_constant_degree_zero q a b k hdeg, mul_zero]

/-- There is no coordinate in degree greater than five. -/
theorem degree_eq_zero (q : R) (n : Nat) (hn : 5 < n) (x : TableAlgebra q)
    (hx : InDegreeAtLeast q n x) : x = 0 := by
  apply ARCTwentyDimAlgebra.ext q
  funext k
  exact hx k (by have hk := t_degree_bound k; omega)

/-- Each positive factor contributes at least one degree to a word. -/
theorem augmentation_kernel_word_degree (q : R) (xs : List (TableAlgebra q))
    (hx : ∀ x ∈ xs, InAugmentationKernel q x) :
    InDegreeAtLeast q xs.length xs.prod := by
  revert hx
  induction xs with
  | nil =>
      intro _ k hk
      exact (Nat.not_lt_zero _ hk).elim
  | cons x xs ih =>
      intro hx
      have hhead : InDegreeAtLeast q 1 x :=
        (augmentation_kernel_iff_degree_one q x).mp (hx x (List.mem_cons_self ..))
      have htail := ih (fun y hy => hx y (List.mem_cons_of_mem _ hy))
      simpa only [List.length_cons, List.prod_cons, Nat.add_comm] using
        degree_mul q 1 xs.length x xs.prod hhead htail

/-- Every word of at least six augmentation-kernel elements vanishes.
This holds over arbitrary commutative characteristic-two coefficient
rings and for every specialization parameter q. -/
theorem augmentation_kernel_word_zero (q : R) (xs : List (TableAlgebra q))
    (hx : ∀ x ∈ xs, InAugmentationKernel q x) (hlen : 6 ≤ xs.length) :
    xs.prod = 0 :=
  degree_eq_zero q xs.length (by omega) xs.prod (augmentation_kernel_word_degree q xs hx)

/-- In particular, every actual kernel element has sixth power zero. -/
theorem augmentation_kernel_pow_six_zero (q : R) (x : TableAlgebra q)
    (hx : InAugmentationKernel q x) : x ^ 6 = 0 := by
  have hword := augmentation_kernel_word_zero q (List.replicate 6 x)
    (by
      intro y hy
      have hyx : y = x := List.eq_of_mem_replicate hy
      simpa only [hyx] using hx)
    (by simp)
  simpa only [List.prod_replicate] using hword

#print axioms t_degree_homogeneity
#print axioms t_degree_bound
#print axioms t_degree_zero_iff
#print axioms polynomial_constant_degree_zero
#print axioms augmentation_kernel_iff_degree_one
#print axioms degree_mul
#print axioms degree_eq_zero
#print axioms augmentation_kernel_word_degree
#print axioms augmentation_kernel_word_zero
#print axioms augmentation_kernel_pow_six_zero

end
end ARCTwentyDimNilpotence
