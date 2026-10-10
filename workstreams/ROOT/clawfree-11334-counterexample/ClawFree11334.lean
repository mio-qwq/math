import Mathlib.Combinatorics.SimpleGraph.Metric
import Mathlib.Combinatorics.SimpleGraph.Finite
import Mathlib.Data.Fin.VecNotation
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.FinCases
import Lean.Elab.Tactic.Omega

/-!
A thirty-six-vertex counterexample to arXiv:2608.02566v1, section 6,
Problem 1. Graphs, degrees, walks and distances are the actual Mathlib
objects. The original palette is (1,1,3,3,4). The proof extracts arbitrary
high-coloured representatives and derives a necessary private-neighbour
condition; a structural diamond-ring obstruction contradicts it.
Small kernel decisions check fixed graph data and at most four Fin 3
colour variables. No enumeration of all original or core colourings.
The source's exceptional graph H has twelve vertices.
-/

set_option maxRecDepth 3000
set_option maxHeartbeats 8000000

namespace ClawFree11334

open SimpleGraph

/-- The eighteen undirected edges, with the certificate's vertex numbering. -/
def coreEdges : List (Fin 12 × Fin 12) :=
  [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 11), (3, 6),
   (4, 5), (4, 6), (4, 7), (5, 6), (5, 7), (7, 10),
   (8, 9), (8, 10), (8, 11), (9, 10), (9, 11)]

def coreAdjacent (u v : Fin 12) : Prop :=
  (u, v) ∈ coreEdges ∨ (v, u) ∈ coreEdges

instance coreAdjacent_decidable : DecidableRel coreAdjacent :=
  fun u v =>
    show Decidable ((u, v) ∈ coreEdges ∨ (v, u) ∈ coreEdges) from inferInstance

def core : SimpleGraph (Fin 12) where
  Adj := coreAdjacent
  symm := ⟨by
    intro u v h
    exact h.elim Or.inr Or.inl⟩
  loopless := ⟨by decide⟩

instance coreAdj_decidable : DecidableRel core.Adj := coreAdjacent_decidable

def a : Fin 3 → Fin 12 := ![0, 4, 8]
def b : Fin 3 → Fin 12 := ![1, 5, 9]
def p : Fin 3 → Fin 12 := ![2, 6, 10]
def q : Fin 3 → Fin 12 := ![3, 7, 11]
def prev : Fin 3 → Fin 3 := ![2, 0, 1]

theorem a_b_adj : ∀ i : Fin 3, core.Adj (a i) (b i) := by decide
theorem a_p_adj : ∀ i : Fin 3, core.Adj (a i) (p i) := by decide
theorem a_q_adj : ∀ i : Fin 3, core.Adj (a i) (q i) := by decide
theorem b_p_adj : ∀ i : Fin 3, core.Adj (b i) (p i) := by decide
theorem b_q_adj : ∀ i : Fin 3, core.Adj (b i) (q i) := by decide

theorem p_prev_link : ∀ i : Fin 3, core.Adj (p i) (q (prev i)) := by decide

/-- This complete neighbor list is essential to the private-neighbor argument. -/
theorem p_neighbors : ∀ (i : Fin 3) (w : Fin 12),
    core.Adj (p i) w ↔ w = a i ∨ w = b i ∨ w = q (prev i) := by decide

theorem q_ne_p : ∀ i : Fin 3, q i ≠ p i := by decide
theorem a_prev_ne_p : ∀ i : Fin 3, a (prev i) ≠ p i := by decide
theorem b_prev_ne_p : ∀ i : Fin 3, b (prev i) ≠ p i := by decide

theorem link01 : core.Adj (q 0) (p 1) := by decide
theorem link12 : core.Adj (q 1) (p 2) := by decide
theorem link20 : core.Adj (q 2) (p 0) := by decide

/-- In a properly three-colored diamond, the two nonadjacent tips agree. -/
private theorem diamond_colors :
    ∀ ca cb cp cq : Fin 3,
      ca ≠ cb → ca ≠ cp → cb ≠ cp → ca ≠ cq → cb ≠ cq → cp = cq := by
  decide

/-- If a properly colored triangle's tip is not color 2, one base is color 2. -/
private theorem color_two_among_bases :
    ∀ ca cb ct : Fin 3,
      ca ≠ cb → ca ≠ ct → cb ≠ ct → ct ≠ 2 → ca = 2 ∨ cb = 2 := by
  decide

private theorem no_two_colored_triangle :
    ∀ x y z : Fin 3,
      x ≠ 2 → y ≠ 2 → z ≠ 2 → x ≠ y → y ≠ z → z ≠ x → False := by
  decide

/--
There is no proper three-coloring of this core in which every color-2 vertex
has a neighbor adjacent to no other color-2 vertex.  The full packing-coloring
proof must derive precisely these two hypotheses from its actual graph metric.
-/
theorem core_obstruction (f : Fin 12 → Fin 3)
    (proper : ∀ u v, core.Adj u v → f u ≠ f v)
    (hprivate : ∀ v, f v = 2 →
      ∃ w, core.Adj v w ∧ ∀ u, core.Adj w u → f u = 2 → u = v) : False := by
  have hpq (i : Fin 3) : f (p i) = f (q i) :=
    diamond_colors (f (a i)) (f (b i)) (f (p i)) (f (q i))
      (proper _ _ (a_b_adj i))
      (proper _ _ (a_p_adj i))
      (proper _ _ (b_p_adj i))
      (proper _ _ (a_q_adj i))
      (proper _ _ (b_q_adj i))
  have hp_not_C (i : Fin 3) : f (p i) ≠ 2 := by
    intro hpi
    obtain ⟨w, hw, hw_unique⟩ := hprivate (p i) hpi
    have hqi : f (q i) = 2 := (hpq i).symm.trans hpi
    rcases (p_neighbors i w).mp hw with hwA | hwB | hwQ
    · subst w
      exact q_ne_p i (hw_unique (q i) (a_q_adj i) hqi)
    · subst w
      exact q_ne_p i (hw_unique (q i) (b_q_adj i) hqi)
    · subst w
      have hqprev : f (q (prev i)) ≠ 2 := by
        intro heq
        exact (proper _ _ (p_prev_link i)) (hpi.trans heq.symm)
      have hbase : f (a (prev i)) = 2 ∨ f (b (prev i)) = 2 :=
        color_two_among_bases
          (f (a (prev i))) (f (b (prev i))) (f (q (prev i)))
          (proper _ _ (a_b_adj (prev i)))
          (proper _ _ (a_q_adj (prev i)))
          (proper _ _ (b_q_adj (prev i)))
          hqprev
      rcases hbase with ha | hb
      · exact a_prev_ne_p i
          (hw_unique (a (prev i)) ((a_q_adj (prev i)).symm) ha)
      · exact b_prev_ne_p i
          (hw_unique (b (prev i)) ((b_q_adj (prev i)).symm) hb)
  have h01 : f (p 0) ≠ f (p 1) := by
    intro h
    exact (proper _ _ link01) ((hpq 0).symm.trans h)
  have h12 : f (p 1) ≠ f (p 2) := by
    intro h
    exact (proper _ _ link12) ((hpq 1).symm.trans h)
  have h20 : f (p 2) ≠ f (p 0) := by
    intro h
    exact (proper _ _ link20) ((hpq 2).symm.trans h)
  exact no_two_colored_triangle (f (p 0)) (f (p 1)) (f (p 2))
    (hp_not_C 0) (hp_not_C 1) (hp_not_C 2) h01 h12 h20


/-- The incidence numbered 3*v+i. Its three slots are in the order of
the sorted neighbour labels in counterexample.json. -/
def vertex (v : Fin 12) (i : Fin 3) : Fin 36 :=
  ⟨3 * v.val + i.val, by have hv := v.is_lt; have hi := i.is_lt; omega⟩

def block (x : Fin 36) : Fin 12 :=
  ⟨x.val / 3, by have hx := x.is_lt; omega⟩

def slot (x : Fin 36) : Fin 3 := ⟨x.val % 3, by omega⟩

theorem block_vertex (v : Fin 12) (i : Fin 3) : block (vertex v i) = v := by
  apply Fin.ext
  dsimp [block, vertex]
  have hi := i.is_lt
  omega

theorem vertex_block_slot (x : Fin 36) : vertex (block x) (slot x) = x := by
  apply Fin.ext
  dsimp [vertex, block, slot]
  omega

theorem vertex_ne (v : Fin 12) {i j : Fin 3} (h : i ≠ j) :
    vertex v i ≠ vertex v j := by
  intro he
  apply h
  apply Fin.ext
  have hv := congrArg (fun x : Fin 36 => x.val) he
  dsimp [vertex] at hv
  omega

def partner : Fin 36 → Fin 36 := ![3,6,9,0,7,10,1,4,33,2,5,18,15,19,21,12,20,22,11,13,16,14,17,30,27,31,34,24,32,35,23,25,28,8,26,29]

theorem partner_involutive : ∀ x : Fin 36, partner (partner x) = x := by decide
theorem partner_ne : ∀ x : Fin 36, partner x ≠ x := by decide

def adjacent (x y : Fin 36) : Prop :=
  (block x = block y ∧ x ≠ y) ∨ partner x = y

instance : DecidableRel adjacent := fun x y => by unfold adjacent; infer_instance

def graph : SimpleGraph (Fin 36) where
  Adj := adjacent
  symm := ⟨by
    intro x y h
    rcases h with h | h
    · exact Or.inl ⟨h.1.symm, h.2.symm⟩
    · right
      rw [← h, partner_involutive]⟩
  loopless := ⟨by
    intro x h
    rcases h with h | h
    · exact h.2 rfl
    · exact partner_ne x h⟩

instance : DecidableRel graph.Adj := inferInstanceAs (DecidableRel adjacent)

/-- Direct semantic equality with the frozen certificate, verified by
kernel reduction on vertex pairs; this does not enumerate colorings. -/
theorem graph_matches_edges : ∀ x y : Fin 36, graph.Adj x y ↔
    (x.val,y.val) ∈ ([(0,1),(0,2),(0,3),(1,2),(1,6),(2,9),(3,4),(3,5),(4,5),(4,7),(5,10),(6,7),(6,8),(7,8),(8,33),(9,10),(9,11),(10,11),(11,18),(12,13),(12,14),(12,15),(13,14),(13,19),(14,21),(15,16),(15,17),(16,17),(16,20),(17,22),(18,19),(18,20),(19,20),(21,22),(21,23),(22,23),(23,30),(24,25),(24,26),(24,27),(25,26),(25,31),(26,34),(27,28),(27,29),(28,29),(28,32),(29,35),(30,31),(30,32),(31,32),(33,34),(33,35),(34,35),(1,0),(2,0),(3,0),(2,1),(6,1),(9,2),(4,3),(5,3),(5,4),(7,4),(10,5),(7,6),(8,6),(8,7),(33,8),(10,9),(11,9),(11,10),(18,11),(13,12),(14,12),(15,12),(14,13),(19,13),(21,14),(16,15),(17,15),(17,16),(20,16),(22,17),(19,18),(20,18),(20,19),(22,21),(23,21),(23,22),(30,23),(25,24),(26,24),(27,24),(26,25),(31,25),(34,26),(28,27),(29,27),(29,28),(32,28),(35,29),(31,30),(32,30),(32,31),(34,33),(35,33),(35,34)] : List (ℕ × ℕ)) := by decide

def ClawFree {V : Type*} (G : SimpleGraph V) : Prop :=
  ∀ v x y z, G.Adj v x → G.Adj v y → G.Adj v z →
    x ≠ y → x ≠ z → y ≠ z → G.Adj x y ∨ G.Adj x z ∨ G.Adj y z

theorem graph_claw_free : ClawFree graph := by
  intro v x y z hx hy hz hxy hxz hyz
  change ((block v = block x ∧ v ≠ x) ∨ partner v = x) at hx
  change ((block v = block y ∧ v ≠ y) ∨ partner v = y) at hy
  change ((block v = block z ∧ v ≠ z) ∨ partner v = z) at hz
  rcases hx with hx | hx <;> rcases hy with hy | hy <;> rcases hz with hz | hz
  · exact Or.inl (Or.inl ⟨hx.1.symm.trans hy.1, hxy⟩)
  · exact Or.inl (Or.inl ⟨hx.1.symm.trans hy.1, hxy⟩)
  · exact Or.inr (Or.inl (Or.inl ⟨hx.1.symm.trans hz.1, hxz⟩))
  · exact (hyz (hy.symm.trans hz)).elim
  · exact Or.inr (Or.inr (Or.inl ⟨hy.1.symm.trans hz.1, hyz⟩))
  · exact (hxz (hx.symm.trans hz)).elim
  · exact (hxy (hx.symm.trans hy)).elim
  · exact (hxy (hx.symm.trans hy)).elim

theorem graph_cubic : ∀ x : Fin 36, graph.degree x = 3 := by
  simp only [SimpleGraph.degree, SimpleGraph.neighborFinset_eq_filter]
  decide

theorem root_walks : ∀ v : Fin 36, Nonempty (graph.Walk 0 v) := by
  intro v
  fin_cases v
  · exact ⟨.nil⟩
  · exact ⟨.cons (show graph.Adj 0 1 by decide) (.nil)⟩
  · exact ⟨.cons (show graph.Adj 0 2 by decide) (.nil)⟩
  · exact ⟨.cons (show graph.Adj 0 3 by decide) (.nil)⟩
  · exact ⟨.cons (show graph.Adj 0 3 by decide) (.cons (show graph.Adj 3 4 by decide) (.nil))⟩
  · exact ⟨.cons (show graph.Adj 0 3 by decide) (.cons (show graph.Adj 3 5 by decide) (.nil))⟩
  · exact ⟨.cons (show graph.Adj 0 1 by decide) (.cons (show graph.Adj 1 6 by decide) (.nil))⟩
  · exact ⟨.cons (show graph.Adj 0 1 by decide) (.cons (show graph.Adj 1 6 by decide) (.cons (show graph.Adj 6 7 by decide) (.nil)))⟩
  · exact ⟨.cons (show graph.Adj 0 1 by decide) (.cons (show graph.Adj 1 6 by decide) (.cons (show graph.Adj 6 8 by decide) (.nil)))⟩
  · exact ⟨.cons (show graph.Adj 0 2 by decide) (.cons (show graph.Adj 2 9 by decide) (.nil))⟩
  · exact ⟨.cons (show graph.Adj 0 2 by decide) (.cons (show graph.Adj 2 9 by decide) (.cons (show graph.Adj 9 10 by decide) (.nil)))⟩
  · exact ⟨.cons (show graph.Adj 0 2 by decide) (.cons (show graph.Adj 2 9 by decide) (.cons (show graph.Adj 9 11 by decide) (.nil)))⟩
  · exact ⟨.cons (show graph.Adj 0 2 by decide) (.cons (show graph.Adj 2 9 by decide) (.cons (show graph.Adj 9 11 by decide) (.cons (show graph.Adj 11 18 by decide) (.cons (show graph.Adj 18 19 by decide) (.cons (show graph.Adj 19 13 by decide) (.cons (show graph.Adj 13 12 by decide) (.nil)))))))⟩
  · exact ⟨.cons (show graph.Adj 0 2 by decide) (.cons (show graph.Adj 2 9 by decide) (.cons (show graph.Adj 9 11 by decide) (.cons (show graph.Adj 11 18 by decide) (.cons (show graph.Adj 18 19 by decide) (.cons (show graph.Adj 19 13 by decide) (.nil))))))⟩
  · exact ⟨.cons (show graph.Adj 0 2 by decide) (.cons (show graph.Adj 2 9 by decide) (.cons (show graph.Adj 9 11 by decide) (.cons (show graph.Adj 11 18 by decide) (.cons (show graph.Adj 18 19 by decide) (.cons (show graph.Adj 19 13 by decide) (.cons (show graph.Adj 13 14 by decide) (.nil)))))))⟩
  · exact ⟨.cons (show graph.Adj 0 2 by decide) (.cons (show graph.Adj 2 9 by decide) (.cons (show graph.Adj 9 11 by decide) (.cons (show graph.Adj 11 18 by decide) (.cons (show graph.Adj 18 20 by decide) (.cons (show graph.Adj 20 16 by decide) (.cons (show graph.Adj 16 15 by decide) (.nil)))))))⟩
  · exact ⟨.cons (show graph.Adj 0 2 by decide) (.cons (show graph.Adj 2 9 by decide) (.cons (show graph.Adj 9 11 by decide) (.cons (show graph.Adj 11 18 by decide) (.cons (show graph.Adj 18 20 by decide) (.cons (show graph.Adj 20 16 by decide) (.nil))))))⟩
  · exact ⟨.cons (show graph.Adj 0 2 by decide) (.cons (show graph.Adj 2 9 by decide) (.cons (show graph.Adj 9 11 by decide) (.cons (show graph.Adj 11 18 by decide) (.cons (show graph.Adj 18 20 by decide) (.cons (show graph.Adj 20 16 by decide) (.cons (show graph.Adj 16 17 by decide) (.nil)))))))⟩
  · exact ⟨.cons (show graph.Adj 0 2 by decide) (.cons (show graph.Adj 2 9 by decide) (.cons (show graph.Adj 9 11 by decide) (.cons (show graph.Adj 11 18 by decide) (.nil))))⟩
  · exact ⟨.cons (show graph.Adj 0 2 by decide) (.cons (show graph.Adj 2 9 by decide) (.cons (show graph.Adj 9 11 by decide) (.cons (show graph.Adj 11 18 by decide) (.cons (show graph.Adj 18 19 by decide) (.nil)))))⟩
  · exact ⟨.cons (show graph.Adj 0 2 by decide) (.cons (show graph.Adj 2 9 by decide) (.cons (show graph.Adj 9 11 by decide) (.cons (show graph.Adj 11 18 by decide) (.cons (show graph.Adj 18 20 by decide) (.nil)))))⟩
  · exact ⟨.cons (show graph.Adj 0 2 by decide) (.cons (show graph.Adj 2 9 by decide) (.cons (show graph.Adj 9 11 by decide) (.cons (show graph.Adj 11 18 by decide) (.cons (show graph.Adj 18 19 by decide) (.cons (show graph.Adj 19 13 by decide) (.cons (show graph.Adj 13 14 by decide) (.cons (show graph.Adj 14 21 by decide) (.nil))))))))⟩
  · exact ⟨.cons (show graph.Adj 0 2 by decide) (.cons (show graph.Adj 2 9 by decide) (.cons (show graph.Adj 9 11 by decide) (.cons (show graph.Adj 11 18 by decide) (.cons (show graph.Adj 18 20 by decide) (.cons (show graph.Adj 20 16 by decide) (.cons (show graph.Adj 16 17 by decide) (.cons (show graph.Adj 17 22 by decide) (.nil))))))))⟩
  · exact ⟨.cons (show graph.Adj 0 2 by decide) (.cons (show graph.Adj 2 9 by decide) (.cons (show graph.Adj 9 11 by decide) (.cons (show graph.Adj 11 18 by decide) (.cons (show graph.Adj 18 19 by decide) (.cons (show graph.Adj 19 13 by decide) (.cons (show graph.Adj 13 14 by decide) (.cons (show graph.Adj 14 21 by decide) (.cons (show graph.Adj 21 23 by decide) (.nil)))))))))⟩
  · exact ⟨.cons (show graph.Adj 0 1 by decide) (.cons (show graph.Adj 1 6 by decide) (.cons (show graph.Adj 6 8 by decide) (.cons (show graph.Adj 8 33 by decide) (.cons (show graph.Adj 33 34 by decide) (.cons (show graph.Adj 34 26 by decide) (.cons (show graph.Adj 26 24 by decide) (.nil)))))))⟩
  · exact ⟨.cons (show graph.Adj 0 1 by decide) (.cons (show graph.Adj 1 6 by decide) (.cons (show graph.Adj 6 8 by decide) (.cons (show graph.Adj 8 33 by decide) (.cons (show graph.Adj 33 34 by decide) (.cons (show graph.Adj 34 26 by decide) (.cons (show graph.Adj 26 25 by decide) (.nil)))))))⟩
  · exact ⟨.cons (show graph.Adj 0 1 by decide) (.cons (show graph.Adj 1 6 by decide) (.cons (show graph.Adj 6 8 by decide) (.cons (show graph.Adj 8 33 by decide) (.cons (show graph.Adj 33 34 by decide) (.cons (show graph.Adj 34 26 by decide) (.nil))))))⟩
  · exact ⟨.cons (show graph.Adj 0 1 by decide) (.cons (show graph.Adj 1 6 by decide) (.cons (show graph.Adj 6 8 by decide) (.cons (show graph.Adj 8 33 by decide) (.cons (show graph.Adj 33 35 by decide) (.cons (show graph.Adj 35 29 by decide) (.cons (show graph.Adj 29 27 by decide) (.nil)))))))⟩
  · exact ⟨.cons (show graph.Adj 0 1 by decide) (.cons (show graph.Adj 1 6 by decide) (.cons (show graph.Adj 6 8 by decide) (.cons (show graph.Adj 8 33 by decide) (.cons (show graph.Adj 33 35 by decide) (.cons (show graph.Adj 35 29 by decide) (.cons (show graph.Adj 29 28 by decide) (.nil)))))))⟩
  · exact ⟨.cons (show graph.Adj 0 1 by decide) (.cons (show graph.Adj 1 6 by decide) (.cons (show graph.Adj 6 8 by decide) (.cons (show graph.Adj 8 33 by decide) (.cons (show graph.Adj 33 35 by decide) (.cons (show graph.Adj 35 29 by decide) (.nil))))))⟩
  · exact ⟨.cons (show graph.Adj 0 1 by decide) (.cons (show graph.Adj 1 6 by decide) (.cons (show graph.Adj 6 8 by decide) (.cons (show graph.Adj 8 33 by decide) (.cons (show graph.Adj 33 34 by decide) (.cons (show graph.Adj 34 26 by decide) (.cons (show graph.Adj 26 25 by decide) (.cons (show graph.Adj 25 31 by decide) (.cons (show graph.Adj 31 30 by decide) (.nil)))))))))⟩
  · exact ⟨.cons (show graph.Adj 0 1 by decide) (.cons (show graph.Adj 1 6 by decide) (.cons (show graph.Adj 6 8 by decide) (.cons (show graph.Adj 8 33 by decide) (.cons (show graph.Adj 33 34 by decide) (.cons (show graph.Adj 34 26 by decide) (.cons (show graph.Adj 26 25 by decide) (.cons (show graph.Adj 25 31 by decide) (.nil))))))))⟩
  · exact ⟨.cons (show graph.Adj 0 1 by decide) (.cons (show graph.Adj 1 6 by decide) (.cons (show graph.Adj 6 8 by decide) (.cons (show graph.Adj 8 33 by decide) (.cons (show graph.Adj 33 35 by decide) (.cons (show graph.Adj 35 29 by decide) (.cons (show graph.Adj 29 28 by decide) (.cons (show graph.Adj 28 32 by decide) (.nil))))))))⟩
  · exact ⟨.cons (show graph.Adj 0 1 by decide) (.cons (show graph.Adj 1 6 by decide) (.cons (show graph.Adj 6 8 by decide) (.cons (show graph.Adj 8 33 by decide) (.nil))))⟩
  · exact ⟨.cons (show graph.Adj 0 1 by decide) (.cons (show graph.Adj 1 6 by decide) (.cons (show graph.Adj 6 8 by decide) (.cons (show graph.Adj 8 33 by decide) (.cons (show graph.Adj 33 34 by decide) (.nil)))))⟩
  · exact ⟨.cons (show graph.Adj 0 1 by decide) (.cons (show graph.Adj 1 6 by decide) (.cons (show graph.Adj 6 8 by decide) (.cons (show graph.Adj 8 33 by decide) (.cons (show graph.Adj 33 35 by decide) (.nil)))))⟩

theorem graph_connected : graph.Connected where
  preconnected := by
    intro u v
    obtain ⟨p⟩ := root_walks u
    obtain ⟨q⟩ := root_walks v
    exact ⟨p.reverse.append q⟩

/-- In particular, the 36-vertex witness cannot be the source's exceptional
12-vertex graph H, regardless of its labelling. -/
theorem not_iso_twelve (H : SimpleGraph (Fin 12)) : IsEmpty (graph ≃g H) := by
  refine ⟨fun e => ?_⟩
  have hh := Fintype.card_congr e.toEquiv
  norm_num at hh

theorem same_block_adj {x y : Fin 36} (hb : block x = block y) (hne : x ≠ y) :
    graph.Adj x y := Or.inl ⟨hb, hne⟩

theorem cross_adj (x : Fin 36) : graph.Adj x (partner x) := Or.inr rfl

theorem block_cross_adj : ∀ x : Fin 36, core.Adj (block x) (block (partner x)) :=
  by decide

theorem core_ports : ∀ u v : Fin 12, core.Adj u v →
    ∃ i j : Fin 3, partner (vertex u i) = vertex v j := by decide

theorem same_block_walk (x y : Fin 36) (hb : block x = block y) :
    ∃ p : graph.Walk x y, p.length ≤ 1 := by
  by_cases h : x = y
  · subst y
    exact ⟨.nil, by simp⟩
  exact ⟨.cons (same_block_adj hb h) .nil, by simp⟩

/-- Any selected endpoints in adjacent core triangles have a real walk
of at most three edges. No shortest-path assertion is needed. -/
theorem adjacent_triangles_walk (u v : Fin 12) (i j : Fin 3) (ha : core.Adj u v) :
    ∃ p : graph.Walk (vertex u i) (vertex v j), p.length ≤ 3 := by
  obtain ⟨s, t, hp⟩ := core_ports u v ha
  obtain ⟨left, hl⟩ := same_block_walk (vertex u i) (vertex u s)
    (by rw [block_vertex, block_vertex])
  obtain ⟨right, hr⟩ := same_block_walk (vertex v t) (vertex v j)
    (by rw [block_vertex, block_vertex])
  have hc : graph.Adj (vertex u s) (vertex v t) := by
    rw [← hp]
    exact cross_adj _
  refine ⟨left.append (.cons hc right), ?_⟩
  simp only [SimpleGraph.Walk.length_append, SimpleGraph.Walk.length_cons]
  omega

theorem adjacent_triangles_edist (u v : Fin 12) (i j : Fin 3) (ha : core.Adj u v) :
    graph.edist (vertex u i) (vertex v j) ≤ 3 := by
  obtain ⟨p, hp⟩ := adjacent_triangles_walk u v i j ha
  exact le_trans p.edist_le (by exact_mod_cast hp)

/-- The port points to w. Any representative at a core neighbour of w
can be reached within four original-graph edges. -/
theorem port_neighbour_walk (x : Fin 36) (u : Fin 12) (i : Fin 3)
    (ha : core.Adj (block (partner x)) u) :
    ∃ p : graph.Walk x (vertex u i), p.length ≤ 4 := by
  obtain ⟨p, hp⟩ : ∃ p : graph.Walk (partner x) (vertex u i), p.length ≤ 3 := by
    rw [← vertex_block_slot (partner x)]
    exact adjacent_triangles_walk (block (partner x)) u (slot (partner x)) i ha
  refine ⟨.cons (cross_adj x) p, ?_⟩
  simp only [SimpleGraph.Walk.length_cons]
  omega

theorem port_neighbour_edist (x : Fin 36) (u : Fin 12) (i : Fin 3)
    (ha : core.Adj (block (partner x)) u) : graph.edist x (vertex u i) ≤ 4 := by
  obtain ⟨p, hp⟩ := port_neighbour_walk x u i ha
  exact le_trans p.edist_le (by exact_mod_cast hp)

def radius (a : Fin 5) : ℕ :=
  if a.val < 2 then 1 else if a.val < 4 then 3 else 4

/-- The original five labelled classes, using distance in G itself. -/
def Packing11334 {V : Type*} (G : SimpleGraph V) (c : V → Fin 5) : Prop :=
  ∀ x y, x ≠ y → c x = c y → (radius (c x) : ℕ∞) < G.edist x y

theorem radius_positive (a : Fin 5) : 1 ≤ radius a := by
  unfold radius
  split
  · omega
  · split <;> omega

theorem radius_high (a : Fin 5) (ha : 2 ≤ a.val) : 3 ≤ radius a := by
  unfold radius
  split
  · omega
  · split <;> omega

theorem packing_adj_ne {V : Type*} {G : SimpleGraph V} {c : V → Fin 5}
    (hc : Packing11334 G c) {x y : V} (ha : G.Adj x y) : c x ≠ c y := by
  intro he
  have hh := hc x y ha.ne he
  have hd : G.edist x y ≤ 1 := by simpa using (.cons ha .nil : G.Walk x y).edist_le
  have hr : (1 : ℕ∞) ≤ radius (c x) := by exact_mod_cast radius_positive (c x)
  exact (not_lt_of_ge (le_trans hd hr)) hh

/-- A triangle needs a high colour. We choose an existing high point;
no normalization or uniqueness of high points is assumed. -/
theorem triangle_has_high {c : Fin 36 → Fin 5} (hc : Packing11334 graph c)
    (v : Fin 12) : ∃ i : Fin 3, 2 ≤ (c (vertex v i)).val := by
  by_contra hn
  have low : ∀ i : Fin 3, (c (vertex v i)).val < 2 := by
    intro i
    have hnot : ¬2 ≤ (c (vertex v i)).val := fun he => hn ⟨i, he⟩
    omega
  have adjacent_slots : ∀ i j : Fin 3, i ≠ j → graph.Adj (vertex v i) (vertex v j) := by
    intro i j hij
    exact same_block_adj (by rw [block_vertex, block_vertex]) (vertex_ne v hij)
  have h01 := packing_adj_ne hc (adjacent_slots 0 1 (by decide))
  have h02 := packing_adj_ne hc (adjacent_slots 0 2 (by decide))
  have h12 := packing_adj_ne hc (adjacent_slots 1 2 (by decide))
  have h01v : (c (vertex v 0)).val ≠ (c (vertex v 1)).val := fun h => h01 (Fin.ext h)
  have h02v : (c (vertex v 0)).val ≠ (c (vertex v 2)).val := fun h => h02 (Fin.ext h)
  have h12v : (c (vertex v 1)).val ≠ (c (vertex v 2)).val := fun h => h12 (Fin.ext h)
  have h0 := low 0
  have h1 := low 1
  have h2 := low 2
  omega

/-- Every original coloring, with arbitrary high representatives, forces
a proper core three-coloring and a private neighbour for every label 2.
This is a necessary-condition theorem, not a sufficient construction. -/
theorem packing_core_necessary {c : Fin 36 → Fin 5} (hc : Packing11334 graph c) :
    ∃ f : Fin 12 → Fin 3,
      (∀ u v, core.Adj u v → f u ≠ f v) ∧
      (∀ v, f v = 2 → ∃ w, core.Adj v w ∧
        ∀ u, core.Adj w u → f u = 2 → u = v) := by
  classical
  let r : Fin 12 → Fin 3 := fun v => Classical.choose (triangle_has_high hc v)
  have hr : ∀ v, 2 ≤ (c (vertex v (r v))).val := by
    intro v
    exact Classical.choose_spec (triangle_has_high hc v)
  let f : Fin 12 → Fin 3 := fun v => ⟨(c (vertex v (r v))).val - 2, by
    have hlt := (c (vertex v (r v))).is_lt
    have hhigh := hr v
    omega⟩
  have fv : ∀ v, (f v).val + 2 = (c (vertex v (r v))).val := by
    intro v
    dsimp [f]
    have hhigh := hr v
    omega
  have representative_ne : ∀ u v, u ≠ v → vertex u (r u) ≠ vertex v (r v) := by
    intro u v hne he
    apply hne
    simpa only [block_vertex] using congrArg block he
  refine ⟨f, ?_, ?_⟩
  · intro u v ha he
    have colour_eq : c (vertex u (r u)) = c (vertex v (r v)) := by
      apply Fin.ext
      have hf := congrArg (fun a : Fin 3 => a.val) he
      have fu := fv u
      have fvv := fv v
      omega
    have hh := hc _ _ (representative_ne u v ha.ne) colour_eq
    have hd := adjacent_triangles_edist u v (r u) (r v) ha
    have hradius : (3 : ℕ∞) ≤ radius (c (vertex u (r u))) := by
      exact_mod_cast radius_high _ (hr u)
    exact (not_lt_of_ge (le_trans hd hradius)) hh
  · intro v hv
    let x := vertex v (r v)
    let w := block (partner x)
    have hc_v : c x = 4 := by
      apply Fin.ext
      have hf := congrArg (fun a : Fin 3 => a.val) hv
      have hfv := fv v
      change (c (vertex v (r v))).val = 4
      omega
    refine ⟨w, ?_, ?_⟩
    · simpa only [x, w, block_vertex] using block_cross_adj x
    · intro u ha hu
      by_contra hne
      have hc_u : c (vertex u (r u)) = 4 := by
        apply Fin.ext
        have hf := congrArg (fun a : Fin 3 => a.val) hu
        have hfu := fv u
        omega
      have hxy : x ≠ vertex u (r u) := representative_ne v u (fun he => hne he.symm)
      have hh := hc x _ hxy (hc_v.trans hc_u.symm)
      have hh4 : (4 : ℕ∞) < graph.edist x (vertex u (r u)) := by
        simpa [hc_v, radius] using hh
      have hd := port_neighbour_edist x u (r u) ha
      exact (not_lt_of_ge hd) hh4

theorem no_packing11334 : ¬∃ c : Fin 36 → Fin 5, Packing11334 graph c := by
  rintro ⟨c, hc⟩
  obtain ⟨f, hp, hn⟩ := packing_core_necessary hc
  exact core_obstruction f hp hn

/-- A fully original-metric finite witness against Problem 1. The source's
exception H has twelve vertices; the Lean exclusion covers every such H. -/
theorem original_counterexample :
    graph.Connected ∧ ClawFree graph ∧ (∀ x, graph.degree x = 3) ∧
      (∀ H : SimpleGraph (Fin 12), IsEmpty (graph ≃g H)) ∧
      ¬∃ c : Fin 36 → Fin 5, Packing11334 graph c :=
  ⟨graph_connected, graph_claw_free, graph_cubic, not_iso_twelve, no_packing11334⟩

#print axioms core_obstruction
#print axioms partner_involutive
#print axioms graph_matches_edges
#print axioms graph_cubic
#print axioms graph_claw_free
#print axioms graph_connected
#print axioms not_iso_twelve
#print axioms block_cross_adj
#print axioms core_ports
#print axioms adjacent_triangles_walk
#print axioms adjacent_triangles_edist
#print axioms port_neighbour_walk
#print axioms port_neighbour_edist
#print axioms packing_adj_ne
#print axioms triangle_has_high
#print axioms packing_core_necessary
#print axioms no_packing11334
#print axioms original_counterexample

end ClawFree11334
