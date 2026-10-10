import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Algebra.BigOperators.Finsupp.Basic
import Mathlib.Data.Fintype.BigOperators
import Mathlib.Combinatorics.SimpleGraph.Basic
import Mathlib.Basic.Real.Basic
import Mathlib.Tactic.Linarith

/- A main eigenvalue is specified by its actual adjacency eigenvector,
   with nonzero coordinate sum. The cover uses two disjoint copies of
   the vertex set and only cross-layer copies of original edges.
   No spectral theorem, walk counts, finite search or assumed lemma is used. -/
namespace CDCMainEigenvalues

open Finset

variable {V W : Type*} [Fintype V] [Fintype W]

noncomputable def adjAction (G : SimpleGraph V) (x : V → ℝ) (i : V) : ℝ := by
  classical
  exact ∑ j, if G.Adj i j then x j else 0

def MainEigen (G : SimpleGraph V) (r : ℝ) : Prop :=
  ∃ x : V → ℝ, (∑ i, x i) ≠ 0 ∧ ∀ i, adjAction G x i = r * x i

def cover (G : SimpleGraph V) : SimpleGraph (V ⊕ V) where
  Adj a b := match a, b with
    | .inl i, .inr j => G.Adj i j
    | .inr i, .inl j => G.Adj i j
    | _, _ => False
  symm := by
    constructor
    intro a b h
    cases a <;> cases b <;> simp_all only
    all_goals exact h.symm
  loopless := by constructor; intro a; cases a <;> simp

theorem cover_action_left (G : SimpleGraph V) (x y : V → ℝ) (i : V) :
    adjAction (cover G) (Sum.elim x y) (.inl i) = adjAction G y i := by
  classical
  simp [adjAction, cover, Fintype.sum_sum_type]
  rfl

theorem cover_action_right (G : SimpleGraph V) (x y : V → ℝ) (i : V) :
    adjAction (cover G) (Sum.elim x y) (.inr i) = adjAction G x i := by
  classical
  simp [adjAction, cover, Fintype.sum_sum_type]
  rfl

theorem action_add (G : SimpleGraph V) (x y : V → ℝ) (i : V) :
    adjAction G (x + y) i = adjAction G x i + adjAction G y i := by
  classical
  simp only [adjAction, Pi.add_apply]
  rw [← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro j _
  split_ifs <;> simp

theorem cover_main_iff (G : SimpleGraph V) (r : ℝ) :
    MainEigen (cover G) r ↔ MainEigen G r := by
  classical
  constructor
  · rintro ⟨z, hz, he⟩
    let x : V → ℝ := fun i => z (.inl i)
    let y : V → ℝ := fun i => z (.inr i)
    have hsplit : z = Sum.elim x y := by funext i; cases i <;> rfl
    refine ⟨x + y, ?_, ?_⟩
    · simpa [hsplit, Fintype.sum_sum_type, Finset.sum_add_distrib] using hz
    · intro i
      rw [action_add]
      have hx := he (.inr i)
      have hy := he (.inl i)
      rw [hsplit, cover_action_right] at hx
      rw [hsplit, cover_action_left] at hy
      simp only [Sum.elim_inl, Sum.elim_inr] at hx hy
      simp only [Pi.add_apply]
      linarith
  · rintro ⟨x, hx, he⟩
    refine ⟨Sum.elim x x, ?_, ?_⟩
    · rw [Fintype.sum_sum_type]
      simpa only [Sum.elim_inl, Sum.elim_inr, ← two_mul, mul_ne_zero_iff,
        ne_eq, OfNat.ofNat_ne_zero, not_false_eq_true, true_and] using hx
    · intro i
      cases i with
      | inl i => simpa only [cover_action_left, Sum.elim_inl] using he i
      | inr i => simpa only [cover_action_right, Sum.elim_inr] using he i

theorem iso_main_forward {G : SimpleGraph V} {H : SimpleGraph W}
    (f : RelIso G.Adj H.Adj) (r : ℝ) (h : MainEigen G r) : MainEigen H r := by
  classical
  obtain ⟨x, hx, he⟩ := h
  refine ⟨fun j => x (f.symm j), ?_, ?_⟩
  · have hs : (∑ j, x (f.symm j)) = ∑ i, x i := f.symm.toEquiv.sum_comp x
    intro hzero
    exact hx (hs.symm.trans hzero)
  · intro j
    have hj := he (f.symm j)
    simp only [adjAction] at hj ⊢
    rw [← f.toEquiv.sum_comp (fun k => if H.Adj j k then x (f.symm k) else 0)]
    convert hj using 1
    apply Finset.sum_congr rfl
    intro k _
    have hrel : H.Adj j (f k) ↔ G.Adj (f.symm j) k := by
      simpa using (f.map_rel_iff (a := f.symm j) (b := k))
    simp [hrel]

theorem iso_main_iff {G : SimpleGraph V} {H : SimpleGraph W}
    (e : RelIso G.Adj H.Adj) (r : ℝ) : MainEigen G r ↔ MainEigen H r :=
  ⟨iso_main_forward e r, iso_main_forward e.symm r⟩

theorem same_main_of_cover_iso {G : SimpleGraph V} {H : SimpleGraph W}
    (e : RelIso (cover G).Adj (cover H).Adj) (r : ℝ) :
    MainEigen G r ↔ MainEigen H r := by
  rw [← cover_main_iff G r, ← cover_main_iff H r]
  exact iso_main_iff e r

#print axioms cover_action_left
#print axioms cover_action_right
#print axioms action_add
#print axioms cover_main_iff
#print axioms iso_main_forward
#print axioms iso_main_iff
#print axioms same_main_of_cover_iso

end CDCMainEigenvalues
