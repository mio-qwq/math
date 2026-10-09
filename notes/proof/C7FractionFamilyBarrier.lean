import Mathlib.Data.Nat.Basic
import Mathlib.Data.Nat.ModEq
import Mathlib.Algebra.Order.GroupWithZero.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Positivity
import Lean.Elab.Tactic.Omega

/-!
Arithmetic barrier for the explicit parameter family of Theorem 1.7 in
Buys--Polak--Zuiddam, arXiv:2506.14654v1.

This file proves a restriction on the displayed numerators. It does not
formalize that paper's lattice construction or its cohomomorphism theorem,
and it gives no upper bound on the unrestricted Shannon capacity of C7.
-/

namespace C7FractionFamilyBarrier

def a (n k b r s : ℕ) : ℕ := k * b ^ n + s * b + r
def denominator (n k b r : ℕ) : ℕ := r + k * b ^ n
def pNumerator (n k b r s : ℕ) : ℕ :=
  r * s ^ n + k * (a n k b r s) ^ n
def qNumerator (n k b r s : ℕ) : ℕ :=
  r * s ^ (n - 1) + k * b * (a n k b r s) ^ (n - 1)

theorem denominator_dvd_p (n k b r s : ℕ) :
    denominator n k b r ∣ pNumerator n k b r s := by
  have ha : a n k b r s = denominator n k b r + s * b := by
    unfold a denominator
    omega
  have hmod : Nat.ModEq (denominator n k b r) (a n k b r s) (s * b) := by
    rw [ha]
    simp [Nat.ModEq]
  have hpmod := ((hmod.pow n).mul_left k).add_left (r * s ^ n)
  have hid : r * s ^ n + k * (s * b) ^ n =
      s ^ n * denominator n k b r := by
    unfold denominator
    rw [mul_pow]
    ring
  rw [hid] at hpmod
  have hz : Nat.ModEq (denominator n k b r)
      (s ^ n * denominator n k b r) 0 := by simp [Nat.ModEq]
  exact Nat.modEq_zero_iff_dvd.mp (hpmod.trans hz)

theorem denominator_dvd_q (n k b r s : ℕ) (hn : 1 ≤ n) :
    denominator n k b r ∣ qNumerator n k b r s := by
  cases n with
  | zero => omega
  | succ m =>
    have ha : a (m + 1) k b r s = denominator (m + 1) k b r + s * b := by
      unfold a denominator
      omega
    have hmod : Nat.ModEq (denominator (m + 1) k b r)
        (a (m + 1) k b r s) (s * b) := by
      rw [ha]
      simp [Nat.ModEq]
    have hqmod := ((hmod.pow m).mul_left (k * b)).add_left (r * s ^ m)
    have hid : r * s ^ m + k * b * (s * b) ^ m =
        s ^ m * denominator (m + 1) k b r := by
      unfold denominator
      rw [mul_pow, pow_succ]
      ring
    rw [hid] at hqmod
    have hz : Nat.ModEq (denominator (m + 1) k b r)
        (s ^ m * denominator (m + 1) k b r) 0 := by simp [Nat.ModEq]
    simpa only [qNumerator, Nat.succ_eq_add_one, Nat.add_sub_cancel] using
      Nat.modEq_zero_iff_dvd.mp (hqmod.trans hz)

theorem denominator_pos (n k b r : ℕ) (hk : 1 ≤ k) (hb : 1 ≤ b) :
    0 < denominator n k b r := by
  unfold denominator
  positivity

theorem q_pos (m k b r s : ℕ) (hk : 1 ≤ k) (hb : 1 ≤ b) :
    0 < qNumerator (m + 1) k b r s := by
  have ha : 0 < a (m + 1) k b r s := by
    unfold a
    positivity
  unfold qNumerator
  positivity

theorem ratio_floor (m k b r s : ℕ) :
    (k * b ^ m + s) * qNumerator (m + 1) k b r s ≤
      pNumerator (m + 1) k b r s := by
  have hbase : s * b ≤ a (m + 1) k b r s := by unfold a; omega
  have hpow : (s * b) ^ m ≤ (a (m + 1) k b r s) ^ m :=
    Nat.pow_le_pow_left hbase m
  have hmul := Nat.mul_le_mul_left (k * r) hpow
  have hid :
      (k * b ^ m + s) * qNumerator (m + 1) k b r s +
        k * r * (a (m + 1) k b r s) ^ m =
      pNumerator (m + 1) k b r s + k * r * (s * b) ^ m := by
    simp only [qNumerator, pNumerator, Nat.add_sub_cancel, pow_succ, mul_pow]
    unfold a
    simp only [pow_succ]
    ring
  omega

theorem parameter_floor (m k b r s : ℕ) (hk : 1 ≤ k) (hb : 1 ≤ b)
    (hc7 : 2 * pNumerator (m + 1) k b r s ≤
      7 * qNumerator (m + 1) k b r s) :
    k * b ^ m + s ≤ 3 := by
  have hfloor := ratio_floor m k b r s
  have hq := q_pos m k b r s hk hb
  have hscaled : (2 * (k * b ^ m + s)) * qNumerator (m + 1) k b r s ≤
      7 * qNumerator (m + 1) k b r s := by nlinarith
  have hsmall := Nat.le_of_mul_le_mul_right hscaled hq
  omega

theorem high_dimension_base (m k b r s : ℕ) (hm : 2 ≤ m)
    (hk : 1 ≤ k) (hb : 1 ≤ b)
    (hc7 : 2 * pNumerator (m + 1) k b r s ≤
      7 * qNumerator (m + 1) k b r s) :
    b = 1 := by
  have hfloor := parameter_floor m k b r s hk hb hc7
  have hpow : b ^ 2 ≤ b ^ m := pow_le_pow_right₀ hb hm
  have hmul : b ^ m ≤ k * b ^ m := by nlinarith
  have hb2 : b ≤ 1 := by
    by_contra hx
    have hbge : 2 ≤ b := by omega
    have hfour : 4 ≤ b ^ 2 := by
      simpa using (Nat.pow_le_pow_left hbge 2)
    omega
  omega

theorem four_base_excluded (m k s : ℕ) (hm : 2 ≤ m)
    (hk : 1 ≤ k) (hks : k + s = 3) :
    7 * qNumerator (m + 1) k 1 1 s <
      2 * pNumerator (m + 1) k 1 1 s := by
  have ha : a (m + 1) k 1 1 s = 4 := by simp [a]; omega
  have hs : s = 0 ∨ s = 1 ∨ s = 2 := by omega
  rcases hs with hs | hs | hs
  · subst s
    have hk3 : k = 3 := by omega
    subst k
    have hm0 : m ≠ 0 := by omega
    simp only [qNumerator, pNumerator, ha, Nat.add_sub_cancel, pow_succ,
      zero_pow hm0, mul_zero, zero_add, mul_one]
    have hpos : 0 < (4 : ℕ) ^ m := by positivity
    nlinarith
  · subst s
    have hk2 : k = 2 := by omega
    subst k
    have hp : 16 ≤ (4 : ℕ) ^ m :=
      by simpa using (pow_le_pow_right₀ (by norm_num : 1 ≤ (4 : ℕ)) hm)
    simp only [qNumerator, pNumerator, ha, Nat.add_sub_cancel, pow_succ,
      one_pow, mul_one]
    nlinarith
  · subst s
    have hk1 : k = 1 := by omega
    subst k
    have hp : 4 ≤ (2 : ℕ) ^ m :=
      by simpa using (pow_le_pow_right₀ (by norm_num : 1 ≤ (2 : ℕ)) hm)
    have hdouble : (4 : ℕ) ^ m = 2 ^ m * 2 ^ m := by
      simpa using (mul_pow (2 : ℕ) 2 m)
    simp only [qNumerator, pNumerator, ha, Nat.add_sub_cancel, pow_succ, one_mul,
      mul_one]
    nlinarith

theorem high_dimension_a (m k b r s : ℕ) (hm : 2 ≤ m)
    (hk : 1 ≤ k) (hb : 1 ≤ b) (hr : r ≤ b)
    (hc7 : 2 * pNumerator (m + 1) k b r s ≤
      7 * qNumerator (m + 1) k b r s) :
    b = 1 ∧ a (m + 1) k b r s ≤ 3 := by
  have hb1 := high_dimension_base m k b r s hm hk hb hc7
  subst b
  have hfloor := parameter_floor m k 1 r s hk (by omega) hc7
  simp only [one_pow, mul_one] at hfloor
  have ha : a (m + 1) k 1 r s = k + s + r := by simp [a]
  have hbad : ¬(k + s = 3 ∧ r = 1) := by
    rintro ⟨hks, hr1⟩
    subst r
    have hx := four_base_excluded m k s hm hk hks
    omega
  constructor
  · rfl
  · omega

theorem high_dimension_size (m k b r s : ℕ) (hm : 2 ≤ m)
    (hk : 1 ≤ k) (hb : 1 ≤ b) (hr : r ≤ b)
    (hc7 : 2 * pNumerator (m + 1) k b r s ≤
      7 * qNumerator (m + 1) k b r s) :
    pNumerator (m + 1) k b r s ≤
      3 ^ (m + 1) * denominator (m + 1) k b r := by
  obtain ⟨hb1, ha⟩ := high_dimension_a m k b r s hm hk hb hr hc7
  subst b
  have hs : s ≤ 3 := by simp [a] at ha; omega
  have hsp := Nat.pow_le_pow_left hs (m + 1)
  have hap := Nat.pow_le_pow_left ha (m + 1)
  have hsprod := Nat.mul_le_mul_left r hsp
  have haprod := Nat.mul_le_mul_left k hap
  unfold pNumerator denominator
  simp only [one_pow, mul_one]
  nlinarith

theorem one_dimension_size (k b r s : ℕ)
    (hc7 : 2 * pNumerator 1 k b r s ≤ 7 * qNumerator 1 k b r s) :
    pNumerator 1 k b r s ≤ 3 * denominator 1 k b r := by
  have hp : pNumerator 1 k b r s = (k + s) * denominator 1 k b r := by
    simp [pNumerator, denominator, a]; ring
  have hq : qNumerator 1 k b r s = denominator 1 k b r := by
    simp [qNumerator, denominator]
  rw [hq, hp] at hc7
  rw [hp]
  by_cases hd : denominator 1 k b r = 0
  · simp [hd]
  · have hdpos : 0 < denominator 1 k b r := by omega
    have hscaled : (2 * (k + s)) * denominator 1 k b r ≤
        7 * denominator 1 k b r := by nlinarith
    have hh := Nat.le_of_mul_le_mul_right hscaled hdpos
    have hks : k + s ≤ 3 := by omega
    nlinarith

theorem two_dimension_size (k b r s : ℕ) (hk : 1 ≤ k) (hb : 1 ≤ b)
    (hc7 : 2 * pNumerator 2 k b r s ≤ 7 * qNumerator 2 k b r s) :
    pNumerator 2 k b r s ≤ 10 * denominator 2 k b r := by
  have hp : pNumerator 2 k b r s =
      ((k * b + s) ^ 2 + k * r) * denominator 2 k b r := by
    simp [pNumerator, denominator, a]; ring
  have hq : qNumerator 2 k b r s = (k * b + s) * denominator 2 k b r := by
    simp [qNumerator, denominator, a]; ring
  have hf := parameter_floor 1 k b r s hk hb hc7
  simp only [pow_one] at hf
  have hdpos : 0 < denominator 2 k b r := by unfold denominator; positivity
  rw [hp, hq] at hc7
  have hscaled :
      (2 * ((k * b + s) ^ 2 + k * r)) * denominator 2 k b r ≤
      (7 * (k * b + s)) * denominator 2 k b r := by nlinarith
  have hh := Nat.le_of_mul_le_mul_right hscaled hdpos
  have hsize : (k * b + s) ^ 2 + k * r ≤ 10 := by omega
  rw [hp]
  exact Nat.mul_le_mul_right _ hsize

theorem all_dimension_squared (n k b r s : ℕ) (hn : 1 ≤ n)
    (hk : 1 ≤ k) (hb : 1 ≤ b) (hr : r ≤ b)
    (hc7 : 2 * pNumerator n k b r s ≤ 7 * qNumerator n k b r s) :
    (pNumerator n k b r s) ^ 2 ≤
      10 ^ n * (denominator n k b r) ^ 2 := by
  have hcases : n = 1 ∨ n = 2 ∨ 3 ≤ n := by omega
  rcases hcases with hn1 | hn2 | hn3
  · subst n
    have hp := one_dimension_size k b r s hc7
    calc
      (pNumerator 1 k b r s) ^ 2 ≤ (3 * denominator 1 k b r) ^ 2 :=
        Nat.pow_le_pow_left hp 2
      _ = 9 * (denominator 1 k b r) ^ 2 := by ring
      _ ≤ 10 ^ 1 * (denominator 1 k b r) ^ 2 :=
        Nat.mul_le_mul_right _ (by norm_num)
  · subst n
    have hp := two_dimension_size k b r s hk hb hc7
    calc
      (pNumerator 2 k b r s) ^ 2 ≤ (10 * denominator 2 k b r) ^ 2 :=
        Nat.pow_le_pow_left hp 2
      _ = 10 ^ 2 * (denominator 2 k b r) ^ 2 := by ring
  · have hm : 2 ≤ n - 1 := by omega
    have hnre : n - 1 + 1 = n := by omega
    have hp := high_dimension_size (n - 1) k b r s hm hk hb hr (by simpa [hnre])
    rw [hnre] at hp
    have heq : ((3 : ℕ) ^ n) ^ 2 = (9 : ℕ) ^ n := by
      rw [← pow_mul, Nat.mul_comm n 2, pow_mul]
      norm_num
    calc
      (pNumerator n k b r s) ^ 2 ≤ (3 ^ n * denominator n k b r) ^ 2 :=
        Nat.pow_le_pow_left hp 2
      _ = 9 ^ n * (denominator n k b r) ^ 2 := by rw [mul_pow, heq]
      _ ≤ 10 ^ n * (denominator n k b r) ^ 2 :=
        Nat.mul_le_mul_right _ (Nat.pow_le_pow_left (by norm_num : 9 ≤ 10) n)

theorem certificate_squared_bound (n k b r s p : ℕ) (hn : 1 ≤ n)
    (hk : 1 ≤ k) (hb : 1 ≤ b) (hr : r ≤ b)
    (hc7 : 2 * pNumerator n k b r s ≤ 7 * qNumerator n k b r s)
    (hp : pNumerator n k b r s = p * denominator n k b r) :
    p ^ 2 ≤ 10 ^ n := by
  have h := all_dimension_squared n k b r s hn hk hb hr hc7
  rw [hp, mul_pow] at h
  have hd := denominator_pos n k b r hk hb
  have hd2 : 0 < (denominator n k b r) ^ 2 := by positivity
  exact Nat.le_of_mul_le_mul_right h hd2

theorem exact_certificate_squared_bound (n k b r s : ℕ) (hn : 1 ≤ n)
    (hk : 1 ≤ k) (hb : 1 ≤ b) (hr : r ≤ b)
    (hc7 : 2 * pNumerator n k b r s ≤ 7 * qNumerator n k b r s) :
    (pNumerator n k b r s / denominator n k b r) ^ 2 ≤ 10 ^ n := by
  exact certificate_squared_bound n k b r s _ hn hk hb hr hc7
    (Nat.div_mul_cancel (denominator_dvd_p n k b r s)).symm

end C7FractionFamilyBarrier

#print axioms C7FractionFamilyBarrier.denominator_dvd_p
#print axioms C7FractionFamilyBarrier.denominator_dvd_q
#print axioms C7FractionFamilyBarrier.denominator_pos
#print axioms C7FractionFamilyBarrier.q_pos
#print axioms C7FractionFamilyBarrier.ratio_floor
#print axioms C7FractionFamilyBarrier.parameter_floor
#print axioms C7FractionFamilyBarrier.high_dimension_base
#print axioms C7FractionFamilyBarrier.four_base_excluded
#print axioms C7FractionFamilyBarrier.high_dimension_a
#print axioms C7FractionFamilyBarrier.high_dimension_size
#print axioms C7FractionFamilyBarrier.one_dimension_size
#print axioms C7FractionFamilyBarrier.two_dimension_size
#print axioms C7FractionFamilyBarrier.all_dimension_squared
#print axioms C7FractionFamilyBarrier.certificate_squared_bound
#print axioms C7FractionFamilyBarrier.exact_certificate_squared_bound
