import Mathlib.Data.Fintype.Card
import Mathlib.Data.Fintype.EquivFin
import Mathlib.Data.Fintype.Sets
import Mathlib.Logic.Relation
import Mathlib.Order.WellFounded
import Lean.Elab.Tactic.Omega

/-!
One structural obstruction for the actual adjacency relation of a finite digraph.
This file does not prove Bermond--Thomassen or its feedback-core special case.
The reduction to an oriented arc-dominated minimal counterexample is not formalized here.
The argument is a short consequence of classical arc-domination; no novelty is claimed.
-/

noncomputable section

namespace DirectedCycleResearch

variable {V : Type*} [Fintype V]

/-- The distinct actual out-neighbors; parallel arcs cannot inflate this count. -/
def outNeighbors (Adj : V → V → Prop) (v : V) : Finset V := by
  classical
  exact Finset.univ.filter (Adj v)

/-- Every actual arc has a vertex entering both endpoints. -/
def ArcDominated (Adj : V → V → Prop) : Prop :=
  ∀ u v, Adj u v → ∃ w, Adj w u ∧ Adj w v

/-- Deletion leaves no nonempty directed closed walk on the actual remaining vertices. -/
def AcyclicAfterDeletion (Adj : V → V → Prop) (S : Finset V) : Prop :=
  ∀ v : {v : V // v ∉ S},
    ¬ Relation.TransGen (fun u w : {v : V // v ∉ S} => Adj u.val w.val) v v

private theorem wf_of_no_closed_walk {W : Type*} [Finite W]
    (R : W → W → Prop) (h : ∀ w, ¬ Relation.TransGen R w w) : WellFounded R := by
  let : Std.Irrefl (Relation.TransGen R) := ⟨h⟩
  exact (Finite.wellFounded_of_trans_of_irrefl (Relation.TransGen R)).mono
    (fun _ _ hxy => Relation.TransGen.single hxy)

/-- A nonempty oriented arc-dominated digraph of minimum out-degree `r > 0`
requires strictly more than `r` vertices in every acyclic deletion set. -/
theorem feedback_set_card_gt_min_outdegree [Nonempty V]
    (Adj : V → V → Prop) (r : ℕ) (hr : 0 < r)
    (oriented : ∀ u v, Adj u v → ¬ Adj v u)
    (dominated : ArcDominated Adj)
    (degree : ∀ v, r ≤ (outNeighbors Adj v).card)
    (S : Finset V) (acyclic : AcyclicAfterDeletion Adj S) : r < S.card := by
  classical
  by_contra hnot
  have hcard : S.card ≤ r := Nat.le_of_not_gt hnot
  have hloop (v : V) : ¬ Adj v v := fun hv => oriented v v hv hv
  have outside : ∃ v : V, v ∉ S := by
    by_contra hempty
    have hall (v : V) : v ∈ S := by
      by_contra hv
      exact hempty ⟨v, hv⟩
    let v : V := Classical.arbitrary V
    have hsub : outNeighbors Adj v ⊆ S := fun w _ => hall w
    have hne : outNeighbors Adj v ≠ S := by
      intro heq
      have hv : v ∈ outNeighbors Adj v := heq.symm ▸ hall v
      exact hloop v (Finset.mem_filter.mp hv).2
    have hlt := Finset.card_lt_card (Finset.ssubset_iff_subset_ne.mpr ⟨hsub, hne⟩)
    have hdeg := degree v
    omega
  let U := {v : V // v ∉ S}
  let R : U → U → Prop := fun u v => Adj u.val v.val
  have forward : WellFounded R := wf_of_no_closed_walk R acyclic
  have backward : WellFounded (Function.swap R) := wf_of_no_closed_walk _ (by
    intro v hv
    exact acyclic v (Relation.transGen_swap.mp hv))
  obtain ⟨v, hv⟩ := outside
  have huniv : (Set.univ : Set U).Nonempty := ⟨⟨v, hv⟩, Set.mem_univ _⟩
  obtain ⟨x, _, hsink⟩ := backward.has_min Set.univ huniv
  have hsub : outNeighbors Adj x.val ⊆ S := by
    intro y hy
    by_contra hynot
    exact hsink ⟨y, hynot⟩ (Set.mem_univ _) (Finset.mem_filter.mp hy).2
  have heq : outNeighbors Adj x.val = S :=
    Finset.eq_of_subset_of_card_le hsub (hcard.trans (degree x.val))
  have allS (y : V) (hy : y ∈ S) : Adj x.val y :=
    (Finset.mem_filter.mp (heq.symm ▸ hy)).2
  have parent_outside (y : V) (hy : Adj y x.val) : y ∉ S := by
    intro hys
    exact oriented y x.val hy (allS y hys)
  obtain ⟨y, hy⟩ := Finset.card_pos.mp (hr.trans_le (degree x.val))
  obtain ⟨p, hpx, _⟩ := dominated x.val y (Finset.mem_filter.mp hy).2
  let parents : Set U := {y | Adj y.val x.val}
  have hparents : parents.Nonempty := ⟨⟨p, parent_outside p hpx⟩, hpx⟩
  obtain ⟨q, hqx, hsource⟩ := forward.has_min parents hparents
  obtain ⟨w, hwq, hwx⟩ := dominated q.val x.val hqx
  exact hsource ⟨w, parent_outside w hwx⟩ hwx hwq

end DirectedCycleResearch

#print axioms DirectedCycleResearch.feedback_set_card_gt_min_outdegree
