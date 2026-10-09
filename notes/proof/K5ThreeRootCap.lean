import Mathlib.Basic.Real.Basic
import Mathlib.Algebra.Order.Ring.Abs
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring
import Mathlib.Algebra.BigOperators.Fin
import Lean.Elab.Tactic.Omega

/- Continuous real-coordinate obstruction for one deletion from D5.
   Scaled coordinates have squared norm 2 and pairwise inner product <= 1.
   No finite-grid or polytope enumeration assumption is used. -/
namespace K5ThreeRootCap

abbrev V5 := Fin 5 → ℝ

def normSq (x : V5) : ℝ :=
  x 0 ^ 2 + x 1 ^ 2 + x 2 ^ 2 + x 3 ^ 2 + x 4 ^ 2

def dot (x y : V5) : ℝ :=
  x 0 * y 0 + x 1 * y 1 + x 2 * y 2 + x 3 * y 3 + x 4 * y 4

def sign (b : Bool) : ℝ := if b then 1 else -1

def rootVector (i j : Fin 5) (s t : Bool) : V5 := fun k =>
  (if k = i then sign s else 0) + (if k = j then sign t else 0)

lemma dot_as_sum (x y : V5) : dot x y = ∑ i : Fin 5, x i*y i := by
  simp [dot, Fin.sum_univ_succ, add_assoc]

theorem dot_rootVector (x : V5) (i j : Fin 5) (s t : Bool) :
    dot x (rootVector i j s t) = sign s*x i+sign t*x j := by
  rw [dot_as_sum]
  simp [rootVector, mul_add, mul_ite, Finset.sum_add_distrib, mul_comm]

/- Exactly the signed root inequalities for i<j, except the three roots
   e0+e1, e0+e2, e1+e2. -/
def RootCompatible (x : V5) : Prop :=
  ∀ (i j : Fin 5), i < j → ∀ (s t : Bool),
    ¬ (i.val < 3 ∧ j.val < 3 ∧ s = true ∧ t = true) →
    sign s * x i + sign t * x j ≤ 1

def GeometricCompatible (x : V5) : Prop :=
  ∀ (i j : Fin 5), i < j → ∀ (s t : Bool),
    ¬ (i.val < 3 ∧ j.val < 3 ∧ s = true ∧ t = true) →
    dot x (rootVector i j s t) ≤ 1

theorem geometric_iff_root (x : V5) : GeometricCompatible x ↔ RootCompatible x := by
  simp only [GeometricCompatible, RootCompatible, dot_rootVector]

structure Reduced (p q r d e : ℝ) : Prop where
  diff01 : |p-q| ≤ 1
  diff02 : |p-r| ≤ 1
  diff12 : |q-r| ≤ 1
  minus01 : -p-q ≤ 1
  minus02 : -p-r ≤ 1
  minus12 : -q-r ≤ 1
  cross03 : |p|+|d| ≤ 1
  cross04 : |p|+|e| ≤ 1
  cross13 : |q|+|d| ≤ 1
  cross14 : |q|+|e| ≤ 1
  cross23 : |r|+|d| ≤ 1
  cross24 : |r|+|e| ≤ 1
  tail34 : |d|+|e| ≤ 1

lemma abs_sum_of_four {a b : ℝ} (hpp : a+b ≤ 1) (hpm : a-b ≤ 1)
    (hmp : -a+b ≤ 1) (hmm : -a-b ≤ 1) : |a|+|b| ≤ 1 := by
  rcases le_total 0 a with ha | ha <;> rcases le_total 0 b with hb | hb
  · simpa only [abs_of_nonneg ha, abs_of_nonneg hb] using hpp
  · simpa only [abs_of_nonneg ha, abs_of_nonpos hb, sub_eq_add_neg] using hpm
  · simpa only [abs_of_nonpos ha, abs_of_nonneg hb] using hmp
  · simpa only [abs_of_nonpos ha, abs_of_nonpos hb, sub_eq_add_neg] using hmm

theorem root_reduced (x : V5) (h : RootCompatible x) :
    Reduced (x 0) (x 1) (x 2) (x 3) (x 4) := by
  have pair (i j : Fin 5) (hij : i < j) (hlarge : 3 ≤ j.val) :
      |x i|+|x j| ≤ 1 := by
    apply abs_sum_of_four
    · simpa [sign] using
        h i j hij true true (by omega)
    · simpa [sign, sub_eq_add_neg] using h i j hij true false (by simp)
    · simpa [sign] using
        h i j hij false true (by simp)
    · simpa [sign, sub_eq_add_neg] using h i j hij false false (by simp)
  have dif (i j : Fin 5) (hij : i < j) : |x i-x j| ≤ 1 := by
    apply abs_le.mpr
    constructor
    · have hm := h i j hij false true (by simp)
      simp only [sign, Bool.false_eq_true, ↓reduceIte, neg_one_mul, one_mul] at hm
      linarith
    · simpa only [sign, Bool.false_eq_true, ↓reduceIte, neg_one_mul, one_mul,
        sub_eq_add_neg] using h i j hij true false (by simp)
  have neg (i j : Fin 5) (hij : i < j) : -x i-x j ≤ 1 := by
    simpa only [sign, Bool.false_eq_true, ↓reduceIte, neg_one_mul,
      sub_eq_add_neg] using h i j hij false false (by simp)
  exact ⟨dif 0 1 (by decide), dif 0 2 (by decide), dif 1 2 (by decide),
    neg 0 1 (by decide), neg 0 2 (by decide), neg 1 2 (by decide),
    pair 0 3 (by decide) (by decide), pair 0 4 (by decide) (by decide),
    pair 1 3 (by decide) (by decide), pair 1 4 (by decide) (by decide),
    pair 2 3 (by decide) (by decide), pair 2 4 (by decide) (by decide),
    pair 3 4 (by decide) (by decide)⟩

lemma square_le {a b : ℝ} (ha : 0 ≤ a) (hab : a ≤ b) : a^2 ≤ b^2 :=
  (sq_le_sq₀ ha (le_trans ha hab)).2 hab

/- Two distinguished coordinates may lack their mutual constraint.
   The other three must vanish if the squared norm is 2. -/
lemma ordered_rest_zero {p q d b c : ℝ}
    (hp : 0 ≤ p) (hq : 0 ≤ q) (hd : 0 ≤ d) (hb : 0 ≤ b) (hc : 0 ≤ c)
    (hbd : b ≤ d) (hcd : c ≤ d)
    (hpd : p+d ≤ 1) (hqd : q+d ≤ 1)
    (hdb : d+b ≤ 1) (hdc : d+c ≤ 1)
    (hn : p^2+q^2+d^2+b^2+c^2 = 2) : d = 0 := by
  have hd1 : d ≤ 1 := by linarith
  by_cases half : d ≤ 1/2
  · have hps := square_le hp (show p ≤ 1-d by linarith)
    have hqs := square_le hq (show q ≤ 1-d by linarith)
    have hbs := square_le hb hbd
    have hcs := square_le hc hcd
    have hprod := mul_nonneg hd (show 0 ≤ 1/2-d by linarith)
    nlinarith
  · have hps := square_le hp (show p ≤ 1-d by linarith)
    have hqs := square_le hq (show q ≤ 1-d by linarith)
    have hbs := square_le hb (show b ≤ 1-d by linarith)
    have hcs := square_le hc (show c ≤ 1-d by linarith)
    have hprod := mul_nonneg (show 0 ≤ d-1/2 by linarith) (show 0 ≤ 1-d by linarith)
    nlinarith

theorem single_missing_pair_rest_zero {p q a b c : ℝ}
    (hp : 0 ≤ p) (hq : 0 ≤ q) (ha : 0 ≤ a) (hb : 0 ≤ b) (hc : 0 ≤ c)
    (hpa : p+a ≤ 1) (hpb : p+b ≤ 1) (hpc : p+c ≤ 1)
    (hqa : q+a ≤ 1) (hqb : q+b ≤ 1) (hqc : q+c ≤ 1)
    (hab : a+b ≤ 1) (hac : a+c ≤ 1) (hbc : b+c ≤ 1)
    (hn : p^2+q^2+a^2+b^2+c^2 = 2) : a = 0 ∧ b = 0 ∧ c = 0 := by
  by_cases hba : b ≤ a
  · by_cases hca : c ≤ a
    · have hz := ordered_rest_zero hp hq ha hb hc hba hca hpa hqa hab hac hn
      exact ⟨hz, by linarith, by linarith⟩
    · have hz := ordered_rest_zero hp hq hc ha hb
        (by linarith) (by linarith) hpc hqc (by linarith) (by linarith)
        (by nlinarith [hn])
      exact ⟨by linarith, by linarith, hz⟩
  · by_cases hcb : c ≤ b
    · have hz := ordered_rest_zero hp hq hb ha hc (by linarith) hcb
        hpb hqb (by linarith) hbc (by nlinarith [hn])
      exact ⟨by linarith, hz, by linarith⟩
    · have hz := ordered_rest_zero hp hq hc ha hb
        (by linarith) (by linarith) hpc hqc (by linarith) (by linarith)
        (by nlinarith [hn])
      exact ⟨by linarith, by linarith, hz⟩

lemma abs_pair_of_nonpos {a b : ℝ} (hb : b ≤ 0)
    (hdiff : |a-b| ≤ 1) (hminus : -a-b ≤ 1) : |a|+|b| ≤ 1 := by
  rcases le_total 0 a with ha | ha
  · have h := le_trans (le_abs_self (a-b)) hdiff
    simpa only [abs_of_nonneg ha, abs_of_nonpos hb, sub_eq_add_neg] using h
  · simpa only [abs_of_nonpos ha, abs_of_nonpos hb, sub_eq_add_neg] using hminus

lemma coordinate_nonnegative {p q r d e : ℝ}
    (hdpq : |q-p| ≤ 1) (hdpr : |r-p| ≤ 1)
    (hmpq : -q-p ≤ 1) (hmpr : -r-p ≤ 1)
    (hpd : |p|+|d| ≤ 1) (hpe : |p|+|e| ≤ 1)
    (hqd : |q|+|d| ≤ 1) (hqe : |q|+|e| ≤ 1)
    (hrd : |r|+|d| ≤ 1) (hre : |r|+|e| ≤ 1)
    (hde : |d|+|e| ≤ 1)
    (hn : p^2+q^2+r^2+d^2+e^2 = 2) : 0 ≤ p := by
  by_contra hneg
  have hp : p ≤ 0 := by linarith
  have hqp := abs_pair_of_nonpos hp hdpq hmpq
  have hrp := abs_pair_of_nonpos hp hdpr hmpr
  have hnabs : |q|^2+|r|^2+|p|^2+|d|^2+|e|^2 = 2 := by
    simp only [sq_abs]
    nlinarith [hn]
  have hz := single_missing_pair_rest_zero (abs_nonneg q) (abs_nonneg r)
    (abs_nonneg p) (abs_nonneg d) (abs_nonneg e)
    hqp hqd hqe hrp hrd hre hpd hpe hde hnabs
  have hp0 := abs_eq_zero.mp hz.1
  linarith

theorem first_three_nonnegative {p q r d e : ℝ}
    (h : Reduced p q r d e) (hn : p^2+q^2+r^2+d^2+e^2 = 2) :
    0 ≤ p ∧ 0 ≤ q ∧ 0 ≤ r := by
  have hp := coordinate_nonnegative
    (by simpa only [abs_sub_comm] using h.diff01)
    (by simpa only [abs_sub_comm] using h.diff02)
    (by linarith [h.minus01]) (by linarith [h.minus02])
    h.cross03 h.cross04 h.cross13 h.cross14 h.cross23 h.cross24 h.tail34 hn
  have hq := coordinate_nonnegative h.diff01
    (by simpa only [abs_sub_comm] using h.diff12)
    (by linarith [h.minus01]) (by linarith [h.minus12])
    h.cross13 h.cross14 h.cross03 h.cross04 h.cross23 h.cross24 h.tail34
    (by nlinarith [hn])
  have hr := coordinate_nonnegative h.diff02 h.diff12
    (by linarith [h.minus02]) (by linarith [h.minus12])
    h.cross23 h.cross24 h.cross03 h.cross04 h.cross13 h.cross14 h.tail34
    (by nlinarith [hn])
  exact ⟨hp, hq, hr⟩

lemma positive_cap_ordered {p q r b c : ℝ}
    (hp : 0 ≤ p) (hq : 0 ≤ q) (hr : 0 ≤ r) (hb : 0 ≤ b) (hc : 0 ≤ c)
    (hcb : c ≤ b) (hpb : p+b ≤ 1) (hqb : q+b ≤ 1) (hrb : r+b ≤ 1)
    (hbc : b+c ≤ 1) (hn : p^2+q^2+r^2+b^2+c^2 = 2) : 2 ≤ p+q+r := by
  have hb1 : b ≤ 1 := by linarith
  have pbound := mul_nonneg hp (show 0 ≤ 1-b-p by linarith)
  have qbound := mul_nonneg hq (show 0 ≤ 1-b-q by linarith)
  have rbound := mul_nonneg hr (show 0 ≤ 1-b-r by linarith)
  have cbound := mul_nonneg hc (show 0 ≤ b-c by linarith)
  have tail := mul_nonneg hb (show 0 ≤ 1-b-c by linarith only [hbc])
  have hnorm : 2 ≤ (1-b)*(p+q+r)+b := by nlinarith [hn]
  by_contra hs
  have hs' : p+q+r < 2 := by linarith
  have hprod := mul_nonneg (show 0 ≤ 1-b by linarith)
    (show 0 ≤ 2-(p+q+r) by linarith)
  have bzero : b = 0 := by nlinarith
  rw [bzero] at hnorm
  norm_num at hnorm
  linarith

theorem reduced_cap {p q r d e : ℝ} (h : Reduced p q r d e)
    (hn : p^2+q^2+r^2+d^2+e^2 = 2) : 2 ≤ p+q+r := by
  obtain ⟨hp,hq,hr⟩ := first_three_nonnegative h hn
  have hpd : p+|d| ≤ 1 := by simpa only [abs_of_nonneg hp] using h.cross03
  have hpe : p+|e| ≤ 1 := by simpa only [abs_of_nonneg hp] using h.cross04
  have hqd : q+|d| ≤ 1 := by simpa only [abs_of_nonneg hq] using h.cross13
  have hqe : q+|e| ≤ 1 := by simpa only [abs_of_nonneg hq] using h.cross14
  have hrd : r+|d| ≤ 1 := by simpa only [abs_of_nonneg hr] using h.cross23
  have hre : r+|e| ≤ 1 := by simpa only [abs_of_nonneg hr] using h.cross24
  rcases le_total |e| |d| with hed | hde
  · exact positive_cap_ordered hp hq hr (abs_nonneg d) (abs_nonneg e) hed
      hpd hqd hrd h.tail34 (by simpa only [sq_abs] using hn)
  · exact positive_cap_ordered hp hq hr (abs_nonneg e) (abs_nonneg d) hde
      hpe hqe hre (by linarith [h.tail34]) (by simp only [sq_abs]; nlinarith [hn])

theorem cap_sum (x : V5) (hc : RootCompatible x) (hn : normSq x = 2) :
    2 ≤ x 0+x 1+x 2 := reduced_cap (root_reduced x hc) hn

lemma positive_boundary_ordered {p q r b c : ℝ}
    (hp : 0 ≤ p) (hq : 0 ≤ q) (hr : 0 ≤ r) (hb : 0 ≤ b) (hc : 0 ≤ c)
    (hcb : c ≤ b) (hpb : p+b ≤ 1) (hqb : q+b ≤ 1) (hrb : r+b ≤ 1)
    (hbc : b+c ≤ 1) (hn : p^2+q^2+r^2+b^2+c^2 = 2) (hs : p+q+r = 2) :
    (p=0 ∨ p=1) ∧ (q=0 ∨ q=1) ∧ (r=0 ∨ r=1) ∧ b=0 ∧ c=0 := by
  have pbound := mul_nonneg hp (show 0 ≤ 1-b-p by linarith)
  have qbound := mul_nonneg hq (show 0 ≤ 1-b-q by linarith)
  have rbound := mul_nonneg hr (show 0 ≤ 1-b-r by linarith)
  have cbound := mul_nonneg hc (show 0 ≤ b-c by linarith)
  have tail := mul_nonneg hb (show 0 ≤ 1-b-c by linarith only [hbc])
  have hnorm : 2 ≤ (1-b)*(p+q+r)+b := by nlinarith only [hn,pbound,qbound,rbound,cbound,tail]
  rw [hs] at hnorm
  have bz : b=0 := by linarith
  have cz : c=0 := by linarith
  have psq : p^2=p := by nlinarith only [hn,hs,pbound,qbound,rbound,bz,cz]
  have qsq : q^2=q := by nlinarith only [hn,hs,pbound,qbound,rbound,bz,cz]
  have rsq : r^2=r := by nlinarith only [hn,hs,pbound,qbound,rbound,bz,cz]
  have binary (u : ℝ) (hu : u^2=u) : u=0 ∨ u=1 := by
    have hprod : u*(u-1)=0 := by nlinarith only [hu]
    rcases mul_eq_zero.mp hprod with hz | hz
    · exact Or.inl hz
    · exact Or.inr (by linarith)
  exact ⟨binary p psq,binary q qsq,binary r rsq,bz,cz⟩

def Removed (x : V5) : Prop :=
  (x 0=1 ∧ x 1=1 ∧ x 2=0 ∧ x 3=0 ∧ x 4=0) ∨
  (x 0=1 ∧ x 1=0 ∧ x 2=1 ∧ x 3=0 ∧ x 4=0) ∨
  (x 0=0 ∧ x 1=1 ∧ x 2=1 ∧ x 3=0 ∧ x 4=0)

theorem cap_boundary (x : V5) (hc : RootCompatible x) (hn : normSq x=2)
    (hs : x 0+x 1+x 2=2) : Removed x := by
  have h := root_reduced x hc
  obtain ⟨hp,hq,hr⟩ := first_three_nonnegative h hn
  have hpd : x 0+|x 3| ≤ 1 := by simpa only [abs_of_nonneg hp] using h.cross03
  have hpe : x 0+|x 4| ≤ 1 := by simpa only [abs_of_nonneg hp] using h.cross04
  have hqd : x 1+|x 3| ≤ 1 := by simpa only [abs_of_nonneg hq] using h.cross13
  have hqe : x 1+|x 4| ≤ 1 := by simpa only [abs_of_nonneg hq] using h.cross14
  have hrd : x 2+|x 3| ≤ 1 := by simpa only [abs_of_nonneg hr] using h.cross23
  have hre : x 2+|x 4| ≤ 1 := by simpa only [abs_of_nonneg hr] using h.cross24
  have boundary : (x 0=0 ∨ x 0=1) ∧ (x 1=0 ∨ x 1=1) ∧
      (x 2=0 ∨ x 2=1) ∧ x 3=0 ∧ x 4=0 := by
    rcases le_total |x 4| |x 3| with hed | hde
    · obtain ⟨pbin,qbin,rbin,dz,ez⟩ := positive_boundary_ordered hp hq hr
        (abs_nonneg _) (abs_nonneg _) hed hpd hqd hrd h.tail34
        (by simpa only [normSq, sq_abs] using hn) hs
      exact ⟨pbin,qbin,rbin,abs_eq_zero.mp dz,abs_eq_zero.mp ez⟩
    · obtain ⟨pbin,qbin,rbin,ez,dz⟩ := positive_boundary_ordered hp hq hr
        (abs_nonneg _) (abs_nonneg _) hde hpe hqe hre (by linarith [h.tail34])
        (by simp only [sq_abs]; dsimp [normSq] at hn; nlinarith only [hn]) hs
      exact ⟨pbin,qbin,rbin,abs_eq_zero.mp dz,abs_eq_zero.mp ez⟩
  obtain ⟨hpbin,hqbin,hrbin,hdz,hez⟩ := boundary
  rcases hpbin with hpz | hpo <;> rcases hqbin with hqz | hqo <;>
    rcases hrbin with hrz | hro <;> simp_all [Removed]
  norm_num at hs

lemma three_coordinate_square (a b c : ℝ) : (a+b+c)^2 ≤ 3*(a^2+b^2+c^2) := by
  nlinarith [sq_nonneg (a-b), sq_nonneg (a-c), sq_nonneg (b-c)]

theorem four_continuous_points_impossible (a b c d : V5)
    (ha : RootCompatible a) (hb : RootCompatible b)
    (hc : RootCompatible c) (hd : RootCompatible d)
    (hna : normSq a = 2) (hnb : normSq b = 2)
    (hnc : normSq c = 2) (hnd : normSq d = 2)
    (hab : dot a b ≤ 1) (hac : dot a c ≤ 1) (had : dot a d ≤ 1)
    (hbc : dot b c ≤ 1) (hbd : dot b d ≤ 1) (hcd : dot c d ≤ 1) : False := by
  have sa := cap_sum a ha hna
  have sb := cap_sum b hb hnb
  have sc := cap_sum c hc hnc
  have sd := cap_sum d hd hnd
  let s : V5 := fun i => a i+b i+c i+d i
  have total : 8 ≤ s 0+s 1+s 2 := by dsimp [s]; linarith
  have low : 64 ≤ (s 0+s 1+s 2)^2 := by nlinarith only [total]
  have identity : normSq s = normSq a+normSq b+normSq c+normSq d +
      2*(dot a b+dot a c+dot a d+dot b c+dot b d+dot c d) := by
    dsimp [normSq, dot, s]
    ring
  have upper : normSq s ≤ 20 := by
    rw [identity, hna, hnb, hnc, hnd]
    linarith only [hab, hac, had, hbc, hbd, hcd]
  have cs := three_coordinate_square (s 0) (s 1) (s 2)
  have tail : 0 ≤ s 3^2+s 4^2 := add_nonneg (sq_nonneg _) (sq_nonneg _)
  dsimp [normSq] at upper
  nlinarith only [low, cs, tail, upper]

theorem three_completion_members (a b c : V5)
    (ha : RootCompatible a) (hb : RootCompatible b) (hc : RootCompatible c)
    (hna : normSq a=2) (hnb : normSq b=2) (hnc : normSq c=2)
    (hab : dot a b ≤ 1) (hac : dot a c ≤ 1) (hbc : dot b c ≤ 1) :
    Removed a ∧ Removed b ∧ Removed c := by
  have sa := cap_sum a ha hna
  have sb := cap_sum b hb hnb
  have sc := cap_sum c hc hnc
  let s : V5 := fun i => a i+b i+c i
  have total : 6 ≤ s 0+s 1+s 2 := by dsimp [s]; linarith only [sa,sb,sc]
  have identity : normSq s=normSq a+normSq b+normSq c+2*(dot a b+dot a c+dot b c) := by
    dsimp [normSq,dot,s]
    ring
  have upper : normSq s ≤ 12 := by
    rw [identity,hna,hnb,hnc]
    linarith only [hab,hac,hbc]
  have cs := three_coordinate_square (s 0) (s 1) (s 2)
  have tail : 0 ≤ s 3^2+s 4^2 := add_nonneg (sq_nonneg _) (sq_nonneg _)
  dsimp [normSq] at upper
  have total_eq : s 0+s 1+s 2=6 := by nlinarith only [total,upper,cs,tail]
  have saeq : a 0+a 1+a 2=2 := by dsimp [s] at total_eq; linarith only [sa,sb,sc,total_eq]
  have sbeq : b 0+b 1+b 2=2 := by dsimp [s] at total_eq; linarith only [sa,sb,sc,total_eq]
  have sceq : c 0+c 1+c 2=2 := by dsimp [s] at total_eq; linarith only [sa,sb,sc,total_eq]
  exact ⟨cap_boundary a ha hna saeq,cap_boundary b hb hnb sbeq,cap_boundary c hc hnc sceq⟩

theorem geometric_four_points_impossible (a b c d : V5)
    (ha : GeometricCompatible a) (hb : GeometricCompatible b)
    (hc : GeometricCompatible c) (hd : GeometricCompatible d)
    (hna : normSq a=2) (hnb : normSq b=2) (hnc : normSq c=2) (hnd : normSq d=2)
    (hab : dot a b ≤ 1) (hac : dot a c ≤ 1) (had : dot a d ≤ 1)
    (hbc : dot b c ≤ 1) (hbd : dot b d ≤ 1) (hcd : dot c d ≤ 1) : False :=
  four_continuous_points_impossible a b c d
    ((geometric_iff_root a).mp ha) ((geometric_iff_root b).mp hb)
    ((geometric_iff_root c).mp hc) ((geometric_iff_root d).mp hd)
    hna hnb hnc hnd hab hac had hbc hbd hcd

theorem geometric_three_completion_members (a b c : V5)
    (ha : GeometricCompatible a) (hb : GeometricCompatible b) (hc : GeometricCompatible c)
    (hna : normSq a=2) (hnb : normSq b=2) (hnc : normSq c=2)
    (hab : dot a b ≤ 1) (hac : dot a c ≤ 1) (hbc : dot b c ≤ 1) :
    Removed a ∧ Removed b ∧ Removed c :=
  three_completion_members a b c ((geometric_iff_root a).mp ha)
    ((geometric_iff_root b).mp hb) ((geometric_iff_root c).mp hc) hna hnb hnc hab hac hbc

#print axioms root_reduced
#print axioms single_missing_pair_rest_zero
#print axioms first_three_nonnegative
#print axioms reduced_cap
#print axioms cap_sum
#print axioms four_continuous_points_impossible
#print axioms dot_rootVector
#print axioms geometric_iff_root
#print axioms cap_boundary
#print axioms three_completion_members
#print axioms geometric_four_points_impossible
#print axioms geometric_three_completion_members

end K5ThreeRootCap
