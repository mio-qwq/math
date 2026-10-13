import Std

/-!
# Conditional joint-potential induction for the uniform-younger policy

This module verifies an abstract scalar induction kernel, NOT the complete
randomized ROB theorem. It uses reverse indexing: `n` is the number of jobs
remaining. `f` is a scaled optimal-value sequence, `k` a scaled potential,
and `s>0` a common integer scale. A physical suffix index i becomes N-i+1.

`MacroShape` is the precise unproved interface to the scheduling model.
Its equations are the nine local potential cases and structural successor
equations in RANDOMIZED_FIVE_QUARTERS.md. They do not assume the desired
nonnegativity or adjacent-equality inequalities. In particular the difficult
length-four/zero-difference alternative requires n>=6, avoiding truncated
natural subtraction at a nonexistent suffix.
-/

namespace ILP1.UniformYoungerPotential

inductive MacroShape (s : Int) (f k : Nat → Int) (n : Nat) : Prop
  | singleton (hn : 1 ≤ n)
      (hf : f n = s + f (n - 1))
      (hk : k n = k (n - 1))
  | forcedPair (hn : 2 ≤ n)
      (hk : k n = s + k (n - 2))
  | forcedThree (hn : 3 ≤ n)
      (hk : k n = s + k (n - 3))
  | forcedFour (hn : 4 ≤ n)
      (hk : k n = 2 * s + k (n - 4))
  | choiceThreeEqual (hn : 3 ≤ n)
      (hf : f (n - 2) = f (n - 3))
      (hk : 2 * k n = k (n - 2) + k (n - 3) - s)
      (next : k (n - 1) = s + k (n - 3))
  | choiceThreeOne (hn : 3 ≤ n)
      (hk : 2 * k n = k (n - 2) + k (n - 3) + 2 * s)
  | choiceFourEqual (hn : 4 ≤ n)
      (hk : 2 * k n = k (n - 2) + k (n - 4))
      (next : k (n - 1) = s + k (n - 3) ∨
        (6 ≤ n ∧ 2 * k (n - 1) = k (n - 3) + k (n - 5) + 3 * s))
  | choiceFourOne (hn : 4 ≤ n)
      (hk : 2 * k n = k (n - 2) + k (n - 4) + 3 * s)
  | choiceFourTwo (hn : 4 ≤ n)
      (hk : 2 * k n = k (n - 2) + k (n - 4))
      (next : k (n - 1) = s + k (n - 3))

/-- The actual strong joint induction. Its second assertion is restricted to
nonempty suffixes; it deliberately says nothing at n=0. -/
theorem joint_invariant (s : Int) (hs : 0 < s) (f k : Nat → Int)
    (limit : Nat) (empty : k 0 = 0)
    (cases : ∀ n, 0 < n → n ≤ limit → MacroShape s f k n) :
    ∀ n, n ≤ limit → 0 ≤ k n ∧
      (0 < n → f n = f (n - 1) → s ≤ k n + k (n - 1)) := by
  intro n
  induction n using Nat.strongRecOn with
  | ind n ih =>
    intro hlimit
    by_cases hn0 : n = 0
    · subst n
      refine ⟨by rw [empty]; omega, ?_⟩
      intro hn
      omega
    · have hn : 0 < n := by omega
      have tail : ∀ j, j < n → 0 ≤ k j := fun j hj => (ih j hj (by omega)).1
      have h1 := tail (n - 1) (by omega)
      cases cases n hn hlimit with
      | singleton hlen hf hk =>
        refine ⟨by omega, ?_⟩
        intro _ heq
        omega
      | forcedPair hlen hk =>
        have h2 := tail (n - 2) (by omega)
        exact ⟨by omega, fun _ _ => by omega⟩
      | forcedThree hlen hk =>
        have h3 := tail (n - 3) (by omega)
        exact ⟨by omega, fun _ _ => by omega⟩
      | forcedFour hlen hk =>
        have h4 := tail (n - 4) (by omega)
        exact ⟨by omega, fun _ _ => by omega⟩
      | choiceThreeEqual hlen hf hk hnext =>
        have h3 := tail (n - 3) (by omega)
        have hsub : (n - 2) - 1 = n - 3 := by omega
        have hfeq : f (n - 2) = f ((n - 2) - 1) := by
          simpa only [hsub] using hf
        have hpair := (ih (n - 2) (by omega) (by omega)).2 (by omega) hfeq
        rw [hsub] at hpair
        have hkn : 0 ≤ k n := by omega
        exact ⟨hkn, fun _ _ => by omega⟩
      | choiceThreeOne hlen hk =>
        have h2 := tail (n - 2) (by omega)
        have h3 := tail (n - 3) (by omega)
        exact ⟨by omega, fun _ _ => by omega⟩
      | choiceFourEqual hlen hk hnext =>
        have h2 := tail (n - 2) (by omega)
        have h4 := tail (n - 4) (by omega)
        have hkn : 0 ≤ k n := by omega
        refine ⟨hkn, ?_⟩
        intro _ _
        have h3 := tail (n - 3) (by omega)
        rcases hnext with hf | ⟨h6, hr⟩
        · omega
        · have h5 := tail (n - 5) (by omega)
          omega
      | choiceFourOne hlen hk =>
        have h2 := tail (n - 2) (by omega)
        have h4 := tail (n - 4) (by omega)
        exact ⟨by omega, fun _ _ => by omega⟩
      | choiceFourTwo hlen hk hnext =>
        have h2 := tail (n - 2) (by omega)
        have h3 := tail (n - 3) (by omega)
        have h4 := tail (n - 4) (by omega)
        exact ⟨by omega, fun _ _ => by omega⟩

def potential (s : Int) (f e : Nat → Int) (n : Nat) : Int :=
  3 * f n + s * (n : Int) - 4 * e n

/-- Conditional 4E<=N+3F with all three quantities expressed at scale s.
The scheduling proof must separately establish the MacroShape interface. -/
theorem scaled_expected_bound (s : Int) (hs : 0 < s) (f e : Nat → Int)
    (n : Nat) (empty : potential s f e 0 = 0)
    (cases : ∀ m, 0 < m → m ≤ n → MacroShape s f (potential s f e) m) :
    4 * e n ≤ s * (n : Int) + 3 * f n := by
  have h := (joint_invariant s hs f (potential s f e) n empty cases n (Nat.le_refl n)).1
  unfold potential at h
  omega

/-- Adds the separately supplied width-two work lower bound. The conclusion
is the scaled integer inequality 4E<=5F, not a probability-space theorem. -/
theorem scaled_five_quarters (s : Int) (hs : 0 < s) (f e : Nat → Int)
    (n : Nat) (empty : potential s f e 0 = 0)
    (cases : ∀ m, 0 < m → m ≤ n → MacroShape s f (potential s f e) m)
    (work : s * (n : Int) ≤ 2 * f n) : 4 * e n ≤ 5 * f n := by
  have h := scaled_expected_bound s hs f e n empty cases
  omega

/-- The work term decreases by exactly the number of removed jobs. -/
theorem scaled_length_sub (s : Int) (n d : Nat) (hd : d ≤ n) :
    s * (n : Int) = s * ((n - d : Nat) : Int) + s * (d : Int) := by
  have hn : (n : Int) = ((n - d : Nat) : Int) + (d : Int) := by omega
  rw [hn, Int.mul_add]

/-- Algebraic bridge for every forced macro-action: removing d jobs at
scaled cost a*s increases the potential by (d-a)*s. -/
theorem forced_potential_identity (s a : Int) (f e : Nat → Int)
    (n d : Nat) (hd : d ≤ n)
    (hf : f n = a * s + f (n - d))
    (he : e n = a * s + e (n - d)) :
    potential s f e n = potential s f e (n - d) + s * (d : Int) - a * s := by
  have hlen := scaled_length_sub s n d hd
  unfold potential
  omega

/-- The only negative local potential increment follows from the actual
minimum/mean scalar recurrences; it is not assumed as a positivity claim. -/
theorem choice_three_equal_identity (s : Int) (hs : 0 < s) (f e : Nat → Int)
    (n : Nat) (hn : 3 ≤ n)
    (hx : f (n - 2) = f (n - 3))
    (hf : f n = min (s + f (n - 2)) (2 * s + f (n - 3)))
    (he : 2 * e n = 3 * s + e (n - 2) + e (n - 3)) :
    2 * potential s f e n =
      potential s f e (n - 2) + potential s f e (n - 3) - s := by
  have h2 := scaled_length_sub s n 2 (by omega)
  have h3 := scaled_length_sub s n 3 hn
  have hmin : s + f (n - 2) ≤ 2 * s + f (n - 3) := by omega
  rw [Int.min_eq_left hmin] at hf
  unfold potential
  omega

theorem choice_three_one_identity (s : Int) (_hs : 0 < s) (f e : Nat → Int)
    (n : Nat) (hn : 3 ≤ n)
    (hx : f (n - 2) = s + f (n - 3))
    (hf : f n = min (s + f (n - 2)) (2 * s + f (n - 3)))
    (he : 2 * e n = 3 * s + e (n - 2) + e (n - 3)) :
    2 * potential s f e n =
      potential s f e (n - 2) + potential s f e (n - 3) + 2 * s := by
  have h2 := scaled_length_sub s n 2 (by omega)
  have h3 := scaled_length_sub s n 3 hn
  have hmin : s + f (n - 2) ≤ 2 * s + f (n - 3) := by omega
  rw [Int.min_eq_left hmin] at hf
  unfold potential
  omega

theorem choice_four_equal_identity (s : Int) (hs : 0 < s) (f e : Nat → Int)
    (n : Nat) (hn : 4 ≤ n)
    (hx : f (n - 2) = f (n - 4))
    (hf : f n = min (s + f (n - 2)) (2 * s + f (n - 4)))
    (he : 2 * e n = 3 * s + e (n - 2) + e (n - 4)) :
    2 * potential s f e n = potential s f e (n - 2) + potential s f e (n - 4) := by
  have h2 := scaled_length_sub s n 2 (by omega)
  have h4 := scaled_length_sub s n 4 hn
  have hmin : s + f (n - 2) ≤ 2 * s + f (n - 4) := by omega
  rw [Int.min_eq_left hmin] at hf
  unfold potential
  omega

theorem choice_four_one_identity (s : Int) (_hs : 0 < s) (f e : Nat → Int)
    (n : Nat) (hn : 4 ≤ n)
    (hx : f (n - 2) = s + f (n - 4))
    (hf : f n = min (s + f (n - 2)) (2 * s + f (n - 4)))
    (he : 2 * e n = 3 * s + e (n - 2) + e (n - 4)) :
    2 * potential s f e n =
      potential s f e (n - 2) + potential s f e (n - 4) + 3 * s := by
  have h2 := scaled_length_sub s n 2 (by omega)
  have h4 := scaled_length_sub s n 4 hn
  have hmin : s + f (n - 2) ≤ 2 * s + f (n - 4) := by omega
  rw [Int.min_eq_left hmin] at hf
  unfold potential
  omega

theorem choice_four_two_identity (s : Int) (hs : 0 < s) (f e : Nat → Int)
    (n : Nat) (hn : 4 ≤ n)
    (hx : f (n - 2) = 2 * s + f (n - 4))
    (hf : f n = min (s + f (n - 2)) (2 * s + f (n - 4)))
    (he : 2 * e n = 3 * s + e (n - 2) + e (n - 4)) :
    2 * potential s f e n = potential s f e (n - 2) + potential s f e (n - 4) := by
  have h2 := scaled_length_sub s n 2 (by omega)
  have h4 := scaled_length_sub s n 4 hn
  have hmin : 2 * s + f (n - 4) ≤ s + f (n - 2) := by omega
  rw [Int.min_eq_right hmin] at hf
  unfold potential
  omega

#print axioms joint_invariant
#print axioms scaled_expected_bound
#print axioms scaled_five_quarters
#print axioms scaled_length_sub
#print axioms forced_potential_identity
#print axioms choice_three_equal_identity
#print axioms choice_three_one_identity
#print axioms choice_four_equal_identity
#print axioms choice_four_one_identity
#print axioms choice_four_two_identity

end ILP1.UniformYoungerPotential
