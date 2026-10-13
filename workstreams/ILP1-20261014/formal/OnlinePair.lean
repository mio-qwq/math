import ROBOperational

/-!
A four-job indistinguishability certificate for initial-window-local
deterministic decisions. This source proves an arbitrary-policy statement,
not only failure of a particular heuristic.

Both programs have n=4, B=3, W=2. Their visible jobs 0,1,2 are roots.
The hidden job 3 depends on job 1 in program A and on job 2 in program B.
Each program has offline optimum 2 cycles. No initial-window-local first
decision can achieve that optimum on both programs.
-/

namespace ILP1

theorem width_two_forbids_three {n : Nat} {t : TimeAssignment n}
    (hw : WidthBound t 2) (i j k : Fin n)
    (hij : i ≠ j) (hik : i ≠ k) (hjk : j ≠ k)
    (htij : t i = t j) (htik : t i = t k) : False := by
  obtain ⟨lane, hl, hc⟩ := hw
  have hli := hl i
  have hlj := hl j
  have hlk := hl k
  have hdij : lane i ≠ lane j := fun heq => hij (hc i j htij heq)
  have hdik : lane i ≠ lane k := fun heq => hik (hc i k htik heq)
  have hdjk : lane j ≠ lane k := fun heq => hjk (hc j k (htij.symm.trans htik) heq)
  omega

namespace OnlinePair

def depA : Dependency 4 := fun i j => i = 1 ∧ j = 3
def depB : Dependency 4 := fun i j => i = 2 ∧ j = 3

def timeA : TimeAssignment 4 := fun i => if i.val < 2 then 0 else 1
def timeB : TimeAssignment 4 := fun i => i.val % 2

theorem forward_A : Forward depA := by unfold Forward depA; decide
theorem forward_B : Forward depB := by unfold Forward depB; decide

theorem timeA_legal : Legal depA 3 2 timeA := by
  refine ⟨?_, ?_, ?_⟩
  · unfold Respects depA timeA
    decide
  · apply (windowEdges_iff_canonicalROB timeA 3).1
    unfold WindowEdges timeA
    decide
  · refine ⟨fun i => i.val % 2, ?_, ?_⟩ <;> decide

theorem timeB_legal : Legal depB 3 2 timeB := by
  refine ⟨?_, ?_, ?_⟩
  · unfold Respects depB timeB
    decide
  · apply (windowEdges_iff_canonicalROB timeB 3).1
    unfold WindowEdges timeB
    decide
  · refine ⟨fun i => i.val / 2, ?_, ?_⟩ <;> decide

theorem feasible_A_two : Feasible depA 3 2 2 :=
  ⟨timeA, timeA_legal, by decide⟩

theorem feasible_B_two : Feasible depB 3 2 2 :=
  ⟨timeB, timeB_legal, by decide⟩

theorem optimal_A_two : Optimal depA 3 2 2 := by
  refine ⟨feasible_A_two, ?_⟩
  rintro k ⟨t, h, hk⟩
  have hedge := h.1 1 3 ⟨rfl, rfl⟩
  have hlast := hk 3
  omega

theorem optimal_B_two : Optimal depB 3 2 2 := by
  refine ⟨feasible_B_two, ?_⟩
  rintro k ⟨t, h, hk⟩
  have hedge := h.1 2 3 ⟨rfl, rfl⟩
  have hlast := hk 3
  omega

/-- Every two-cycle A execution must issue both job 0 and job 1 first. -/
theorem first_A_forced {t : TimeAssignment 4} (h : Legal depA 3 2 t)
    (hk : ∀ i, t i < 2) : t 0 = 0 ∧ t 1 = 0 ∧ t 3 = 1 := by
  have hrob := (windowEdges_iff_canonicalROB t 3).2 h.2.1
  have h03 := hrob 0 3 (by decide)
  have h13 := h.1 1 3 ⟨rfl, rfl⟩
  have h3 := hk 3
  omega

/-- Every two-cycle B execution must issue both job 0 and job 2 first. -/
theorem first_B_forced {t : TimeAssignment 4} (h : Legal depB 3 2 t)
    (hk : ∀ i, t i < 2) : t 0 = 0 ∧ t 2 = 0 ∧ t 3 = 1 := by
  have hrob := (windowEdges_iff_canonicalROB t 3).2 h.2.1
  have h03 := hrob 0 3 (by decide)
  have h23 := h.1 2 3 ⟨rfl, rfl⟩
  have h3 := hk 3
  omega

theorem no_common_first_action {tA tB : TimeAssignment 4}
    (ha : Legal depA 3 2 tA) (hka : ∀ i, tA i < 2)
    (hb : Legal depB 3 2 tB) (hkb : ∀ i, tB i < 2)
    (hsame : ∀ i, tA i = 0 ↔ tB i = 0) : False := by
  obtain ⟨ha0, ha1, _⟩ := first_A_forced ha hka
  obtain ⟨_, hb2, _⟩ := first_B_forced hb hkb
  have ha2 := (hsame 2).2 hb2
  exact width_two_forbids_three ha.2.2 0 1 2 (by decide) (by decide) (by decide)
    (ha0.trans ha1.symm) (ha0.trans ha2.symm)

/-- The dependency data visible at initialization, when B=3. -/
def SameInitialView (d e : Dependency 4) : Prop :=
  ∀ i j : Fin 4, i.val < 3 → j.val < 3 → (d i j ↔ e i j)

theorem same_initial_view : SameInitialView depA depB := by
  unfold SameInitialView depA depB
  decide

/-- A deterministic first-cycle rule. It may be described as a function of the
whole DAG, but `InitialWindowLocal` forces equal actions on equal visible data.
All other known data (n, B, W, initial completion state) agree for the pair. -/
abbrev FirstPolicy := Dependency 4 → Fin 4 → Prop

def InitialWindowLocal (pi : FirstPolicy) : Prop :=
  ∀ d e, SameInitialView d e → ∀ i, pi d i ↔ pi e i

def FollowsFirst (t : TimeAssignment 4) (action : Fin 4 → Prop) : Prop :=
  ∀ i, t i = 0 ↔ action i

def AchievesWithin (pi : FirstPolicy) (dep : Dependency 4) (k : Nat) : Prop :=
  ∃ t : TimeAssignment 4,
    Legal dep 3 2 t ∧ (∀ i, t i < k) ∧ FollowsFirst t (pi dep)

theorem local_policy_cannot_optimize_both (pi : FirstPolicy)
    (hpi : InitialWindowLocal pi) :
    ¬ (AchievesWithin pi depA 2 ∧ AchievesWithin pi depB 2) := by
  rintro ⟨⟨tA, ha, hka, hpa⟩, ⟨tB, hb, hkb, hpb⟩⟩
  apply no_common_first_action ha hka hb hkb
  intro i
  exact (hpa i).trans ((hpi depA depB same_initial_view i).trans (hpb i).symm)

theorem achievesWithin_mono {pi : FirstPolicy} {dep : Dependency 4} {k l : Nat}
    (hkl : k ≤ l) (h : AchievesWithin pi dep k) : AchievesWithin pi dep l := by
  obtain ⟨t, hlegal, hk, hp⟩ := h
  exact ⟨t, hlegal, fun i => Nat.lt_of_lt_of_le (hk i) hkl, hp⟩

/-- General deterministic-policy lower bound for this fixed pair: some input
has offline optimum 2, but every terminating execution with that first action
needs at least 3 cycles. This implies the numerical ratio lower bound 3/2;
the rational-number division is not part of this Std-only statement. -/
theorem local_policy_three_cycles (pi : FirstPolicy) (hpi : InitialWindowLocal pi) :
    ∃ dep : Dependency 4,
      (dep = depA ∨ dep = depB) ∧ Optimal dep 3 2 2 ∧
        ∀ k, AchievesWithin pi dep k → 3 ≤ k := by
  classical
  have hnot := local_policy_cannot_optimize_both pi hpi
  by_cases ha : AchievesWithin pi depA 2
  · refine ⟨depB, Or.inr rfl, optimal_B_two, ?_⟩
    intro k hk
    apply Classical.byContradiction
    intro hlt
    exact hnot ⟨ha, achievesWithin_mono (by omega) hk⟩
  · refine ⟨depA, Or.inl rfl, optimal_A_two, ?_⟩
    intro k hk
    apply Classical.byContradiction
    intro hlt
    exact ha (achievesWithin_mono (by omega) hk)

#print axioms ILP1.width_two_forbids_three
#print axioms forward_A
#print axioms forward_B
#print axioms timeA_legal
#print axioms timeB_legal
#print axioms feasible_A_two
#print axioms feasible_B_two
#print axioms optimal_A_two
#print axioms optimal_B_two
#print axioms first_A_forced
#print axioms first_B_forced
#print axioms no_common_first_action
#print axioms same_initial_view
#print axioms local_policy_cannot_optimize_both
#print axioms achievesWithin_mono
#print axioms local_policy_three_cycles

end OnlinePair
end ILP1
