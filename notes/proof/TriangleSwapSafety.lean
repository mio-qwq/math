import Mathlib.Combinatorics.SimpleGraph.Basic
import Mathlib.Data.Finset.Prod
import Mathlib.Data.Finset.Powerset
import Mathlib.Data.Finset.Lattice.Fold
import Mathlib.Data.Fintype.Powerset
import Mathlib.Data.Finset.Disjoint

/-!
An actual seven-vertex simple graph in which a locally improving two-triangle
swap is not compatible with a retained triangle of the global packing.

The local condition is the literal vertex-induced condition displayed in
Sheng--Xiao, arXiv:2308.16515v1, Section 4.2, Reduction Rule 8.
This file does not refute Tuza's conjecture, a corrected swapping rule, or
the entire kernelization argument. The graph's covering number and the
inapplicability of earlier reductions are not formalized here.

Every finite check below uses ordinary kernel-reduced `decide`.
-/

set_option maxRecDepth 10000
set_option maxHeartbeats 2000000

namespace TriangleSwapSafety

abbrev V := Fin 7
abbrev Triangle := Finset V
abbrev Family := Finset Triangle

def u : V := 0
def v : V := 1
def w : V := 2
def x : V := 3
def y : V := 4
def z : V := 5
def f : V := 6

/-- Twelve specified unordered edges; diagonal pairs are absent. -/
def edgeList : Finset (Sym2 V) :=
  {s(u,v), s(u,w), s(v,w), s(v,x), s(v,y), s(x,y),
   s(u,x), s(u,z), s(x,z), s(u,f), s(x,f), s(w,y)}

def graph : SimpleGraph V where
  Adj a b := a ≠ b ∧ s(a,b) ∈ edgeList
  symm := ⟨by
    intro a b h
    refine ⟨h.1.symm, ?_⟩
    rw [Sym2.eq_swap]
    exact h.2⟩
  loopless := ⟨by
    intro a h
    exact h.1 rfl⟩

instance graphAdjDecidable : DecidableRel graph.Adj :=
  fun a b => inferInstanceAs (Decidable (a ≠ b ∧ s(a,b) ∈ edgeList))

/-- The standard complete-three-vertex condition expressed with finite sets. -/
def IsTriangle (t : Triangle) : Prop :=
  t.card = 3 ∧ ∀ a ∈ t, ∀ b ∈ t, a ≠ b → graph.Adj a b

instance triangleDecidable (t : Triangle) : Decidable (IsTriangle t) := by
  unfold IsTriangle
  infer_instance

/-- All unordered pairs of distinct vertices of `t`. -/
def triangleEdges (t : Triangle) : Finset (Sym2 V) :=
  t.offDiag.image (fun ab => s(ab.1, ab.2))

/-- All members are actual graph triangles, and their unordered edges are disjoint. -/
def IsPacking (S : Family) : Prop :=
  (∀ t ∈ S, IsTriangle t) ∧
    ∀ t ∈ S, ∀ t' ∈ S, t ≠ t' → Disjoint (triangleEdges t) (triangleEdges t')

instance packingDecidable (S : Family) : Decidable (IsPacking S) := by
  unfold IsPacking
  infer_instance

def support (S : Family) : Finset V := S.biUnion id
def outside (S : Family) : Finset V := Finset.univ \ support S

def uvw : Triangle := {u,v,w}
def uvx : Triangle := {u,v,x}
def uxz : Triangle := {u,x,z}
def uxf : Triangle := {u,x,f}
def vwy : Triangle := {v,w,y}
def vxy : Triangle := {v,x,y}

def allTriangles : Family := {uvw, uvx, uxz, uxf, vwy, vxy}
def oldPacking : Family := {uvw, vxy, uxz}
def oldPair : Family := {uvw, vxy}
def newPair : Family := {uxf, vwy}
def retained : Family := {uxz}
def replacement (S P N : Family) : Family := (S \ P) ∪ N

/-- Literal local swap hypotheses: no global compatibility is assumed. -/
def LocalCondition (S P N : Family) : Prop :=
  P ⊆ S ∧ P.card = 2 ∧ N.card = 2 ∧ IsPacking P ∧ IsPacking N ∧
    support N ⊆ outside S ∪ support P ∧ (support P).card < (support N).card

instance localConditionDecidable (S P N : Family) : Decidable (LocalCondition S P N) := by
  unfold LocalCondition
  infer_instance

theorem no_diagonal_edge : ∀ a : V, s(a,a) ∉ edgeList := by decide

/-- The graph's actual Mathlib edge set is precisely the displayed edge list. -/
theorem graph_edgeSet_eq : graph.edgeSet = (edgeList : Set (Sym2 V)) := by
  ext e
  refine Sym2.inductionOn e ?_
  intro a b
  change (a ≠ b ∧ s(a,b) ∈ edgeList) ↔ s(a,b) ∈ edgeList
  constructor
  · exact And.right
  · intro h
    refine ⟨?_, h⟩
    intro hab
    subst b
    exact no_diagonal_edge a h

/-- The finite triangle representation uses the actual graph adjacency. -/
theorem triangle_edges_in_graph (t : Triangle) (ht : IsTriangle t) :
    ∀ e ∈ triangleEdges t, e ∈ graph.edgeSet := by
  intro e he
  obtain ⟨⟨a,b⟩, hab, rfl⟩ := Finset.mem_image.mp he
  obtain ⟨ha, hb, hne⟩ := Finset.mem_offDiag.mp hab
  exact graph.mem_edgeSet.mpr (ht.2 a ha b hb hne)

/-- All actual graph triangles, without a restricted candidate assumption. -/
theorem complete_triangle_list :
    ∀ t : Triangle, IsTriangle t ↔ t ∈ allTriangles := by decide

theorem old_packing_valid : IsPacking oldPacking := by decide
theorem old_packing_card : oldPacking.card = 3 := by decide
theorem old_support_card : (support oldPacking).card = 6 := by decide
theorem outside_old : outside oldPacking = {f} := by decide

/-- Only 64 subsets of the complete six-triangle list are checked. -/
theorem finite_packing_bounds :
    ∀ S ∈ allTriangles.powerset, IsPacking S →
      S.card ≤ 3 ∧ (S.card = 3 → (support S).card ≤ 6) := by
  let : Decidable (∀ S ∈ allTriangles.powerset, IsPacking S →
      S.card ≤ 3 ∧ (S.card = 3 → (support S).card ≤ 6)) :=
    Finset.decidableDforallFinset
  decide

/-- The old packing is maximum in the actual graph. -/
theorem packing_card_le_three (S : Family) (hS : IsPacking S) : S.card ≤ 3 := by
  have hsub : S ⊆ allTriangles := by
    intro t ht
    exact (complete_triangle_list t).mp (hS.1 t ht)
  exact (finite_packing_bounds S (Finset.mem_powerset.mpr hsub) hS).1

/-- Its vertex support is also maximum among all maximum-size packings. -/
theorem maximum_packing_support_le_six (S : Family) (hS : IsPacking S)
    (hcard : S.card = 3) : (support S).card ≤ 6 := by
  have hsub : S ⊆ allTriangles := by
    intro t ht
    exact (complete_triangle_list t).mp (hS.1 t ht)
  exact (finite_packing_bounds S (Finset.mem_powerset.mpr hsub) hS).2 hcard

theorem local_condition_holds : LocalCondition oldPacking oldPair newPair := by
  decide

theorem local_support_improves :
    (support oldPair).card = 5 ∧ (support newPair).card = 6 := by decide

theorem retained_triangle_exact : oldPacking \ oldPair = retained := by decide

/-- The offending unordered edge belongs to the actual graph and both triangles. -/
theorem shared_actual_edge :
    s(u,x) ∈ graph.edgeSet ∧
    s(u,x) ∈ triangleEdges uxf ∧ s(u,x) ∈ triangleEdges uxz := by decide

theorem replacement_not_packing :
    ¬ IsPacking (replacement oldPacking oldPair newPair) := by decide

theorem replacement_support_card :
    (support (replacement oldPacking oldPair newPair)).card = 7 := by decide

/-- A global, maximum-support packing meets every local hypothesis and fails after the swap. -/
theorem maximum_support_local_swap_counterexample :
    IsPacking oldPacking ∧ oldPacking.card = 3 ∧
    (∀ S : Family, IsPacking S → S.card ≤ oldPacking.card) ∧
    (∀ S : Family, IsPacking S → S.card = oldPacking.card →
      (support S).card ≤ (support oldPacking).card) ∧
    LocalCondition oldPacking oldPair newPair ∧
    ¬ IsPacking (replacement oldPacking oldPair newPair) := by
  refine ⟨old_packing_valid, old_packing_card, ?_, ?_,
    local_condition_holds, replacement_not_packing⟩
  · intro S hS
    simpa only [old_packing_card] using packing_card_le_three S hS
  · intro S hS hc
    rw [old_packing_card] at hc
    simpa only [old_support_card] using maximum_packing_support_le_six S hS hc

/-- The literal local condition does not imply global packing safety. -/
theorem local_condition_not_sufficient :
    ¬ (∀ S P N : Family, IsPacking S → LocalCondition S P N →
      IsPacking (replacement S P N)) := by
  intro h
  exact replacement_not_packing
    (h oldPacking oldPair newPair old_packing_valid local_condition_holds)

end TriangleSwapSafety

#print axioms TriangleSwapSafety.no_diagonal_edge
#print axioms TriangleSwapSafety.graph_edgeSet_eq
#print axioms TriangleSwapSafety.triangle_edges_in_graph
#print axioms TriangleSwapSafety.complete_triangle_list
#print axioms TriangleSwapSafety.old_packing_valid
#print axioms TriangleSwapSafety.old_packing_card
#print axioms TriangleSwapSafety.old_support_card
#print axioms TriangleSwapSafety.outside_old
#print axioms TriangleSwapSafety.finite_packing_bounds
#print axioms TriangleSwapSafety.packing_card_le_three
#print axioms TriangleSwapSafety.maximum_packing_support_le_six
#print axioms TriangleSwapSafety.local_condition_holds
#print axioms TriangleSwapSafety.local_support_improves
#print axioms TriangleSwapSafety.retained_triangle_exact
#print axioms TriangleSwapSafety.shared_actual_edge
#print axioms TriangleSwapSafety.replacement_not_packing
#print axioms TriangleSwapSafety.replacement_support_card
#print axioms TriangleSwapSafety.maximum_support_local_swap_counterexample
#print axioms TriangleSwapSafety.local_condition_not_sufficient
