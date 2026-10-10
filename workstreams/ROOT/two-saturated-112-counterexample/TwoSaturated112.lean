import Mathlib.Combinatorics.SimpleGraph.Metric
import Mathlib.Combinatorics.SimpleGraph.Finite
import Mathlib.Data.Fin.VecNotation
import Mathlib.Tactic.NormNum
import Lean.Elab.Tactic.Omega

namespace TwoSaturated112

open SimpleGraph

/-- Vertices 0,1,3 are the triangle, 2 is the subdivided-star centre;
6,4,5 subdivide its spokes to 0,1,3 respectively. -/
def adjacent (u v : Fin 7) : Prop :=
  (u.val, v.val) ∈ ([(0,1),(1,0),(0,3),(3,0),(0,6),(6,0),
    (1,3),(3,1),(1,4),(4,1),(2,4),(4,2),(2,5),(5,2),
    (2,6),(6,2),(3,5),(5,3)] : List (ℕ × ℕ))

instance : DecidableRel adjacent := fun u v => by
  unfold adjacent
  infer_instance

def graph : SimpleGraph (Fin 7) where
  Adj := adjacent
  symm := ⟨by decide⟩
  loopless := ⟨by decide⟩

instance : DecidableRel graph.Adj := inferInstanceAs (DecidableRel adjacent)

def Subcubic {V : Type*} [Fintype V] [DecidableEq V]
    (G : SimpleGraph V) [DecidableRel G.Adj] : Prop := ∀ v, G.degree v ≤ 3

/-- The original degree-three neighbour bound, with no local-girth condition. -/
def Saturated {V : Type*} [Fintype V] [DecidableEq V]
    (G : SimpleGraph V) [DecidableRel G.Adj] (k : ℕ) : Prop :=
  ∀ v, G.degree v = 3 → ((G.neighborFinset v).filter (fun w => G.degree w = 3)).card ≤ k

def radius (a : Fin 3) : ℕ := if a = 2 then 2 else 1

/-- Distinct labels 0 and 1 are two independent classes; label 2 is a
2-packing in the actual original graph metric, not an induced deletion. -/
def Packing112 {V : Type*} (G : SimpleGraph V) (c : V → Fin 3) : Prop :=
  ∀ u v, u ≠ v → c u = c v → (radius (c u) : ℕ∞) < G.edist u v

theorem graph_subcubic : Subcubic graph := by
  simp only [Subcubic, SimpleGraph.degree, SimpleGraph.neighborFinset_eq_filter]
  decide

theorem graph_two_saturated : Saturated graph 2 := by
  simp only [Saturated, SimpleGraph.degree, SimpleGraph.neighborFinset_eq_filter]
  decide

theorem graph_min_degree : ∀ v : Fin 7, 2 ≤ graph.degree v := by
  simp only [SimpleGraph.degree, SimpleGraph.neighborFinset_eq_filter]
  decide

theorem common_neighbour : ∀ u v : Fin 7, u ≠ v → ¬graph.Adj u v →
    ∃ w : Fin 7, graph.Adj u w ∧ graph.Adj w v := by decide

theorem short_walk (u v : Fin 7) : ∃ p : graph.Walk u v, p.length ≤ 2 := by
  by_cases h : u = v
  · subst v
    exact ⟨.nil, by simp⟩
  by_cases ha : graph.Adj u v
  · exact ⟨.cons ha .nil, by simp⟩
  obtain ⟨w, hu, hv⟩ := common_neighbour u v h ha
  exact ⟨.cons hu (.cons hv .nil), by simp⟩

theorem graph_connected : graph.Connected where
  preconnected := by
    intro u v
    obtain ⟨p, _⟩ := short_walk u v
    exact ⟨p⟩

theorem edist_le_two (u v : Fin 7) : graph.edist u v ≤ 2 := by
  obtain ⟨p, hp⟩ := short_walk u v
  exact le_trans p.edist_le (by exact_mod_cast hp)

theorem radius_positive (a : Fin 3) : 1 ≤ radius a := by
  unfold radius
  split <;> omega

theorem packing_adj_ne {V : Type*} {G : SimpleGraph V} {c : V → Fin 3}
    (hc : Packing112 G c) {u v : V} (ha : G.Adj u v) : c u ≠ c v := by
  intro he
  have hh := hc u v ha.ne he
  have hd : G.edist u v ≤ 1 := by simpa using (.cons ha .nil : G.Walk u v).edist_le
  have hr : (1 : ℕ∞) ≤ radius (c u) := by exact_mod_cast radius_positive (c u)
  exact (not_lt_of_ge (le_trans hd hr)) hh

theorem unique_two {c : Fin 7 → Fin 3} (hc : Packing112 graph c)
    {u v : Fin 7} (hu : c u = 2) (hv : c v = 2) : u = v := by
  by_contra hn
  have hh := hc u v hn (hu.trans hv.symm)
  have htwo : (2 : ℕ∞) < graph.edist u v := by simpa [hu, radius] using hh
  exact (not_lt_of_ge (edist_le_two u v)) htwo

def triangle : Fin 3 → Fin 7 := ![0,1,3]

theorem triangle_has_two {c : Fin 7 → Fin 3} (hc : Packing112 graph c) :
    ∃ t : Fin 3, c (triangle t) = 2 := by
  by_contra hn
  have low : ∀ t : Fin 3, (c (triangle t)).val < 2 := by
    intro t
    have hlt := (c (triangle t)).is_lt
    have hne : (c (triangle t)).val ≠ 2 := by
      intro he
      exact hn ⟨t, Fin.ext he⟩
    omega
  have h01 := packing_adj_ne hc (show graph.Adj (triangle 0) (triangle 1) by decide)
  have h02 := packing_adj_ne hc (show graph.Adj (triangle 0) (triangle 2) by decide)
  have h12 := packing_adj_ne hc (show graph.Adj (triangle 1) (triangle 2) by decide)
  have v01 : (c (triangle 0)).val ≠ (c (triangle 1)).val := fun h => h01 (Fin.ext h)
  have v02 : (c (triangle 0)).val ≠ (c (triangle 2)).val := fun h => h02 (Fin.ext h)
  have v12 : (c (triangle 1)).val ≠ (c (triangle 2)).val := fun h => h12 (Fin.ext h)
  have l0 := low 0
  have l1 := low 1
  have l2 := low 2
  omega

/-- Actual odd cycles avoiding, respectively, triangle vertices 0,1,3. -/
def fiveCycle : Fin 3 → Fin 5 → Fin 7 :=
  ![![1,3,5,2,4], ![0,3,5,2,6], ![0,1,4,2,6]]

theorem fiveCycle_adj : ∀ t : Fin 3, ∀ i : Fin 5,
    graph.Adj (fiveCycle t i) (fiveCycle t (i + 1)) := by decide

theorem fiveCycle_avoids : ∀ t : Fin 3, ∀ i : Fin 5,
    fiveCycle t i ≠ triangle t := by decide

/-- The elementary parity obstruction, checked by the kernel on 32 maps. -/
theorem odd_five_two_colours (f : Fin 5 → Fin 2) :
    ∃ i : Fin 5, f i = f (i + 1) := by
  revert f
  decide

theorem no_packing112 : ¬ ∃ c : Fin 7 → Fin 3, Packing112 graph c := by
  rintro ⟨c, hc⟩
  obtain ⟨t, ht⟩ := triangle_has_two hc
  have hnot : ∀ i : Fin 5, c (fiveCycle t i) ≠ 2 := by
    intro i hh
    exact fiveCycle_avoids t i (unique_two hc hh ht)
  let f : Fin 5 → Fin 2 := fun i => ⟨(c (fiveCycle t i)).val, by
    have hb := (c (fiveCycle t i)).is_lt
    have hne : (c (fiveCycle t i)).val ≠ 2 := fun he => hnot i (Fin.ext he)
    omega⟩
  obtain ⟨i, hi⟩ := odd_five_two_colours f
  apply packing_adj_ne hc (fiveCycle_adj t i)
  apply Fin.ext
  exact congrArg (fun a : Fin 2 => a.val) hi

/-- Explicit witness violating the original unrestricted Conjecture 3. -/
theorem original_counterexample :
    Subcubic graph ∧ Saturated graph 2 ∧ graph.Connected ∧
      ¬ ∃ c : Fin 7 → Fin 3, Packing112 graph c :=
  ⟨graph_subcubic, graph_two_saturated, graph_connected, no_packing112⟩

#print axioms graph_subcubic
#print axioms graph_two_saturated
#print axioms graph_min_degree
#print axioms common_neighbour
#print axioms graph_connected
#print axioms edist_le_two
#print axioms packing_adj_ne
#print axioms unique_two
#print axioms triangle_has_two
#print axioms fiveCycle_adj
#print axioms fiveCycle_avoids
#print axioms odd_five_two_colours
#print axioms no_packing112
#print axioms original_counterexample

end TwoSaturated112
