import Mathlib.Combinatorics.SimpleGraph.Acyclic
import Mathlib.Data.Nat.Find
import Mathlib.Data.Finset.Card
import Lean.Elab.Tactic.Omega
import Mathlib.Data.Set.Basic
import Mathlib.Logic.Equiv.Option
import Mathlib.Data.Fintype.Option
import Mathlib.Combinatorics.SimpleGraph.Walk.Maps
import Mathlib.Data.Finset.Image

/-!
# General-position spectra of finite trees

For every finite undirected tree, the general-position numbers of all its
edge orientations form an integer interval. General position is defined using
all actual shortest directed simple paths; unreachable ordered pairs impose
no constraint. The theorem is `TreeGPSpectrumFinal.finite_tree_spectrum_interval`.

This standalone file includes the forest rank characterization, the actual
one-leaf cardinality step, finite-tree deletion induction and graph-isomorphism
transport. It proves the tree case of arXiv:2604.15909v1 Conjecture 4.30.
It does not settle the conjecture for arbitrary graphs.

Toolchain: Lean 4.34.1; Mathlib d13f23b723b8a846827a245b89c10fc7d3f11612.
-/


namespace TreeGPRank

open SimpleGraph

universe u
variable {V : Type u} {G : SimpleGraph V}

/-- Exactly one direction on every actual undirected edge. -/
structure Orientation (G : SimpleGraph V) where
  Arc : V → V → Prop
  arc_adj : ∀ {u v}, Arc u v → G.Adj u v
  complete : ∀ {u v}, G.Adj u v → Arc u v ∨ Arc v u
  asymmetric : ∀ {u v}, Arc u v → ¬ Arc v u

/-- Each successive edge of the actual underlying walk follows R. -/
def Follows (R : V → V → Prop) : {u v : V} → G.Walk u v → Prop
  | _, _, .nil => True
  | u, _, .cons (v := w) _ p => R u w ∧ Follows R p

@[simp] theorem follows_nil (R : V → V → Prop) (v : V) :
    Follows R (SimpleGraph.Walk.nil : G.Walk v v) := True.intro

theorem follows_append {R : V → V → Prop} {u v w : V}
    (p : G.Walk u v) (q : G.Walk v w) :
    Follows R p → Follows R q → Follows R (p.append q) := by
  induction p with
  | nil => intro _ hq; exact hq
  | cons e p ih =>
      intro hp hq
      exact ⟨hp.1, ih q hp.2 hq⟩

theorem follows_concat {R : V → V → Prop} {u v w : V}
    (p : G.Walk u v) (e : G.Adj v w) (hp : Follows R p) (he : R v w) :
    Follows R (p.concat e) :=
  follows_append p (.cons e .nil) hp ⟨he, True.intro⟩

/-- The tree/forest and single-orientation assumptions really prove simplicity. -/
theorem follows_isPath (hG : G.IsAcyclic) (O : Orientation G)
    {u v : V} (p : G.Walk u v) : Follows O.Arc p → p.IsPath := by
  induction p with
  | nil => intro _; exact SimpleGraph.Walk.IsPath.nil
  | @cons u v w e p ih =>
      intro hp
      have htail : p.IsPath := ih hp.2
      apply htail.cons
      intro hu
      have hs : u = p.snd := hG.eq_snd_of_adj_start htail e.symm hu
      cases p with
      | nil =>
          have huv : u = v := by simpa using hs
          exact e.ne huv
      | cons e' q =>
          simp only [SimpleGraph.Walk.snd_cons] at hs
          exact O.asymmetric hp.1 (by simpa only [hs] using hp.2.1)

/-- An actual finite directed simple path, with its ordered vertex support. -/
structure DirectedSimplePath (O : Orientation G) (u v : V) where
  walk : G.Walk u v
  isPath : walk.IsPath
  follows : Follows O.Arc walk

def IsShortest {O : Orientation G} {u v : V} (p : DirectedSimplePath O u v) : Prop :=
  ∀ q : DirectedSimplePath O u v, p.walk.length ≤ q.walk.length

theorem every_path_shortest (hG : G.IsAcyclic) (O : Orientation G)
    {u v : V} (p : DirectedSimplePath O u v) : IsShortest p := by
  intro q
  have heq : (⟨p.walk, p.isPath⟩ : G.Path u v) = ⟨q.walk, q.isPath⟩ :=
    (hG.subsingleton_path u v).elim _ _
  have hw : p.walk = q.walk := congrArg Subtype.val heq
  exact Nat.le_of_eq (congrArg (fun r : G.Walk u v => r.length) hw)

/-- The original definition on one actual shortest directed simple path.
An unreachable ordered pair has no such path and creates no constraint. -/
def OriginalGeneralPosition (O : Orientation G) (S : Set V) : Prop :=
  ∀ {u v : V} (p : DirectedSimplePath O u v), u ∈ S → v ∈ S → IsShortest p →
    ∀ {w : V}, w ∈ p.walk.support → w ∈ S → w = u ∨ w = v

noncomputable def hit (S : Set V) (v : V) : ℕ := by
  classical
  exact if v ∈ S then 1 else 0

noncomputable def selectedList (S : Set V) {u v : V} (p : G.Walk u v) : List V := by
  classical
  exact p.support.filter (fun w => decide (w ∈ S))

noncomputable def selectedCount (S : Set V) {u v : V} (p : G.Walk u v) : ℕ :=
  (selectedList S p).length

@[simp] theorem mem_selectedList (S : Set V) {u v w : V} (p : G.Walk u v) :
    w ∈ selectedList S p ↔ w ∈ p.support ∧ w ∈ S := by
  classical
  simp [selectedList]

theorem selectedList_nodup (S : Set V) {u v : V} {p : G.Walk u v}
    (hp : p.IsPath) : (selectedList S p).Nodup := by
  classical
  exact hp.support_nodup.filter _

theorem hit_le_one (S : Set V) (v : V) : hit S v ≤ 1 := by
  classical
  by_cases hv : v ∈ S <;> simp [hit, hv]

@[simp] theorem selectedCount_nil (S : Set V) (v : V) :
    selectedCount S (SimpleGraph.Walk.nil : G.Walk v v) = hit S v := by
  classical
  by_cases hv : v ∈ S <;> simp [selectedCount, selectedList, hit, hv]

@[simp] theorem selectedCount_cons (S : Set V) {u v w : V}
    (e : G.Adj u v) (p : G.Walk v w) :
    selectedCount S (.cons e p) = hit S u + selectedCount S p := by
  classical
  by_cases hu : u ∈ S <;> simp [selectedCount, selectedList, hit, hu, Nat.add_comm]

@[simp] theorem selectedCount_concat (S : Set V) {u v w : V}
    (p : G.Walk u v) (e : G.Adj v w) :
    selectedCount S (p.concat e) = selectedCount S p + hit S w := by
  classical
  by_cases hw : w ∈ S <;> simp [selectedCount, selectedList, hit, hw]

/-- Trim after the last selected vertex, preserving all selected occurrences.
This lemma constructs a real directed prefix rather than postulating a trim. -/
theorem prefix_selected (R : V → V → Prop) (S : Set V)
    {u v : V} (p : G.Walk u v) : Follows R p → 0 < selectedCount S p →
      ∃ w, ∃ q : G.Walk u w,
        Follows R q ∧ w ∈ S ∧ selectedCount S q = selectedCount S p := by
  classical
  induction p with
  | @nil u =>
      intro _ hpos
      have hu : u ∈ S := by
        by_contra h
        simp [selectedCount_nil, hit, h] at hpos
      exact ⟨u, .nil, True.intro, hu, rfl⟩
  | @cons u v w e p ih =>
      intro hp hpos
      by_cases ht : 0 < selectedCount S p
      · obtain ⟨z, q, hq, hz, hcount⟩ := ih hp.2 ht
        refine ⟨z, .cons e q, ⟨hp.1, hq⟩, hz, ?_⟩
        simp only [selectedCount_cons, hcount]
      · have hz : selectedCount S p = 0 := by omega
        have hu : u ∈ S := by
          by_contra h
          simp [selectedCount_cons, hit, h, hz] at hpos
        refine ⟨u, .nil, True.intro, hu, ?_⟩
        simp [selectedCount_cons, hz]

theorem selected_endpoint_count_le_two (hG : G.IsAcyclic) (O : Orientation G)
    (S : Set V) (hS : OriginalGeneralPosition O S)
    {u v : V} (p : G.Walk u v) (hp : Follows O.Arc p) (hu : u ∈ S) (hv : v ∈ S) :
    selectedCount S p ≤ 2 := by
  classical
  let q : DirectedSimplePath O u v := ⟨p, follows_isPath hG O p hp, hp⟩
  have hsub : (selectedList S p).toFinset ⊆ ({u, v} : Finset V) := by
    intro w hw
    have hw' : w ∈ p.support ∧ w ∈ S :=
      (mem_selectedList S p).mp (List.mem_toFinset.mp hw)
    have he := hS q hu hv (every_path_shortest hG O q) hw'.1 hw'.2
    simpa only [Finset.mem_insert, Finset.mem_singleton] using he
  have hc := Finset.card_le_card hsub
  rw [List.toFinset_card_of_nodup (selectedList_nodup S q.isPath)] at hc
  have hpair : ({u, v} : Finset V).card ≤ 2 := by
    by_cases h : u = v <;> simp [h]
  exact hc.trans hpair

def PathCountBound (O : Orientation G) (S : Set V) : Prop :=
  ∀ {u v : V} (p : G.Walk u v), Follows O.Arc p → selectedCount S p ≤ 2

theorem original_implies_path_count (hG : G.IsAcyclic) (O : Orientation G)
    (S : Set V) (hS : OriginalGeneralPosition O S) : PathCountBound O S := by
  classical
  intro u v p
  induction p with
  | nil =>
      intro _
      simpa only [selectedCount_nil] using (hit_le_one S _).trans (by omega : 1 ≤ 2)
  | @cons u v w e p ih =>
      intro hp
      by_cases hu : u ∈ S
      · have hpos : 0 < selectedCount S (.cons e p) := by
          simp [selectedCount_cons, hit, hu]
        obtain ⟨z, q, hq, hz, hcount⟩ := prefix_selected O.Arc S (.cons e p) hp hpos
        rw [← hcount]
        exact selected_endpoint_count_le_two hG O S hS q hq hu hz
      · have ht := ih hp.2
        simpa [selectedCount_cons, hit, hu] using ht

/-- This implication is valid in any oriented graph: it uses actual paths,
not the forest assumption. The converse below is restricted to forests. -/
theorem path_count_implies_original (O : Orientation G) (S : Set V)
    (hS : PathCountBound O S) : OriginalGeneralPosition O S := by
  classical
  intro u v p hu hv _ w hw hwS
  by_cases hwu : w = u
  · exact Or.inl hwu
  by_cases hwv : w = v
  · exact Or.inr hwv
  by_cases huv : u = v
  · subst v
    have hn : p.walk = .nil := (SimpleGraph.Walk.isPath_iff_nil.mp p.isPath).eq_nil
    have he : w = u := by simpa [hn] using hw
    exact (hwu he).elim
  have hsub : ({u, v, w} : Finset V) ⊆ (selectedList S p.walk).toFinset := by
    intro z hz
    simp only [Finset.mem_insert, Finset.mem_singleton] at hz
    rcases hz with rfl | rfl | rfl
    · simp [hu]
    · simp [hv]
    · simp [hw, hwS]
  have hc := Finset.card_le_card hsub
  rw [List.toFinset_card_of_nodup (selectedList_nodup S p.isPath)] at hc
  have hthree : ({u, v, w} : Finset V).card = 3 := by
    simp [huv, Ne.symm hwu, Ne.symm hwv]
  rw [hthree] at hc
  have hb := hS p.walk p.follows
  change (selectedList S p.walk).length ≤ 2 at hb
  omega

theorem original_iff_path_count (hG : G.IsAcyclic) (O : Orientation G) (S : Set V) :
    OriginalGeneralPosition O S ↔ PathCountBound O S :=
  ⟨original_implies_path_count hG O S, path_count_implies_original O S⟩

/-- Bounded rank labels for a selected vertex set. -/
def Feasible (R : V → V → Prop) (S : Set V) (y : V → ℕ) : Prop :=
  (∀ v, y v ≤ 2 ∧ hit S v ≤ y v) ∧
    ∀ u v, R u v → y u + hit S v ≤ y v

theorem count_add_rank_le (R : V → V → Prop) (S : Set V) (y : V → ℕ)
    (hy : Feasible R S y) {u v : V} (p : G.Walk u v) :
    Follows R p → selectedCount S p + y u ≤ y v + hit S u := by
  induction p with
  | nil => intro _; simp [Nat.add_comm]
  | @cons u v w e p ih =>
      intro hp
      have ht := ih hp.2
      have he := hy.2 u v hp.1
      rw [selectedCount_cons]
      omega

theorem feasible_implies_path_count (O : Orientation G) (S : Set V) (y : V → ℕ)
    (hy : Feasible O.Arc S y) : PathCountBound O S := by
  intro u v p hp
  have ht := count_add_rank_le O.Arc S y hy p hp
  have hu := (hy.1 u).2
  have hv := (hy.1 v).1
  omega

/-- Only three candidate values are needed, but the witness is an actual walk. -/
def Attained (O : Orientation G) (S : Set V) (v : V) (n : ℕ) : Prop :=
  ∃ u, ∃ p : G.Walk u v, Follows O.Arc p ∧ selectedCount S p = n

noncomputable def endpointRank (O : Orientation G) (S : Set V) (v : V) : ℕ := by
  classical
  exact Nat.findGreatest (Attained O S v) 2

theorem singleton_attained (O : Orientation G) (S : Set V) (v : V) :
    Attained O S v (hit S v) :=
  ⟨v, .nil, True.intro, selectedCount_nil S v⟩

theorem endpointRank_le_two (O : Orientation G) (S : Set V) (v : V) :
    endpointRank O S v ≤ 2 := by
  classical
  exact Nat.findGreatest_le 2

theorem endpointRank_attained (O : Orientation G) (S : Set V) (v : V) :
    Attained O S v (endpointRank O S v) := by
  classical
  exact Nat.findGreatest_spec ((hit_le_one S v).trans (by omega : 1 ≤ 2))
    (singleton_attained O S v)

theorem count_le_endpointRank (O : Orientation G) (S : Set V)
    (hS : PathCountBound O S) {u v : V} (p : G.Walk u v) (hp : Follows O.Arc p) :
    selectedCount S p ≤ endpointRank O S v := by
  classical
  exact Nat.le_findGreatest (hS p hp) ⟨u, p, hp, rfl⟩

theorem endpointRank_feasible (O : Orientation G) (S : Set V)
    (hS : PathCountBound O S) : Feasible O.Arc S (endpointRank O S) := by
  constructor
  · intro v
    refine ⟨endpointRank_le_two O S v, ?_⟩
    simpa only [selectedCount_nil] using
      count_le_endpointRank O S hS (SimpleGraph.Walk.nil : G.Walk v v) True.intro
  · intro v w hvw
    obtain ⟨u, p, hp, hcount⟩ := endpointRank_attained O S v
    have hc := count_le_endpointRank O S hS (p.concat (O.arc_adj hvw))
      (follows_concat p (O.arc_adj hvw) hp hvw)
    simpa only [selectedCount_concat, hcount] using hc

theorem path_count_iff_feasible (O : Orientation G) (S : Set V) :
    PathCountBound O S ↔ ∃ y : V → ℕ, Feasible O.Arc S y := by
  constructor
  · intro hS
    exact ⟨endpointRank O S, endpointRank_feasible O S hS⟩
  · rintro ⟨y, hy⟩
    exact feasible_implies_path_count O S y hy

/-- Full candidate bridge from the original single-shortest-path definition.
No GP/rank equivalence is assumed as an input hypothesis. -/
theorem forest_original_iff_feasible (hG : G.IsAcyclic) (O : Orientation G) (S : Set V) :
    OriginalGeneralPosition O S ↔ ∃ y : V → ℕ, Feasible O.Arc S y :=
  (original_iff_path_count hG O S).trans (path_count_iff_feasible O S)

theorem tree_original_iff_feasible (hG : G.IsTree) (O : Orientation G) (S : Set V) :
    OriginalGeneralPosition O S ↔ ∃ y : V → ℕ, Feasible O.Arc S y :=
  forest_original_iff_feasible hG.isAcyclic O S


end TreeGPRank

/- A necessary kernel step for the all-tree GP spectrum argument.
   This section proves extension/restriction for the actual one-leaf arc relations.
   Labels alone describe all-path selection, not general shortest-path GP.
   The original oriented-tree GP/rank bridge is a separate required theorem.
   The graph-spectrum conclusion is proved in the final section below. -/
namespace TreeGPLeafLabels

variable {V : Type*}

noncomputable def chosen (S : Set V) (v : V) : ℕ := by
  classical
  exact if v ∈ S then 1 else 0

structure Feasible (R : V → V → Prop) (S : Set V) (y : V → ℕ) : Prop where
  bounded : ∀ v, y v ≤ 2
  selected_le : ∀ v, chosen S v ≤ y v
  arc : ∀ u v, R u v → y u + chosen S v ≤ y v

def leafSet (S : Set V) : Set (Option V)
  | none => True
  | some v => v ∈ S

@[simp] theorem none_mem_leafSet (S : Set V) : none ∈ leafSet S := True.intro

@[simp] theorem some_mem_leafSet (S : Set V) (v : V) :
    some v ∈ leafSet S ↔ v ∈ S := Iff.rfl

def outRel (R : V → V → Prop) (p : V) : Option V → Option V → Prop
  | some u, some v => R u v
  | some u, none => u = p
  | _, _ => False

def inRel (R : V → V → Prop) (p : V) : Option V → Option V → Prop
  | some u, some v => R u v
  | none, some v => v = p
  | _, _ => False

def outLabels (y : V → ℕ) (p : V) : Option V → ℕ
  | some v => y v
  | none => y p + 1

def inLabels (y : V → ℕ) : Option V → ℕ
  | some v => y v
  | none => 1

theorem chosen_le_one (S : Set V) (v : V) : chosen S v ≤ 1 := by
  classical
  simp only [chosen]
  split <;> omega

theorem out_feasible {R : V → V → Prop} {S : Set V} {y : V → ℕ}
    (h : Feasible R S y) (p : V) (hp : y p ≤ 1) :
    Feasible (outRel R p) (leafSet S) (outLabels y p) := by
  classical
  constructor
  · intro v
    cases v with
    | none => simpa only [outLabels] using (show y p + 1 ≤ 2 by omega)
    | some v => exact h.bounded v
  · intro v
    cases v with
    | none => simp [chosen, outLabels]
    | some v => simpa [chosen, outLabels] using h.selected_le v
  · intro u v huv
    cases u with
    | none => simp [outRel] at huv
    | some u =>
      cases v with
      | none =>
        have hup : u = p := huv
        subst u
        simp [chosen, outLabels]
      | some v =>
        simpa [chosen, outLabels] using h.arc u v huv

theorem in_feasible {R : V → V → Prop} {S : Set V} {y : V → ℕ}
    (h : Feasible R S y) (p : V) (hp : y p = 2) :
    Feasible (inRel R p) (leafSet S) (inLabels y) := by
  classical
  constructor
  · intro v
    cases v with
    | none => simp [inLabels]
    | some v => exact h.bounded v
  · intro v
    cases v with
    | none => simp [chosen, inLabels]
    | some v => simpa [chosen, inLabels] using h.selected_le v
  · intro u v huv
    cases u with
    | none =>
      cases v with
      | none => simp [inRel] at huv
      | some v =>
        have hvp : v = p := huv
        subst v
        have hs := chosen_le_one S p
        change 1 + chosen (leafSet S) (some p) ≤ y p
        have heq : chosen (leafSet S) (some p) = chosen S p := by
          simp [chosen]
        rw [heq, hp]
        omega
    | some u =>
      cases v with
      | none => simp [inRel] at huv
      | some v =>
        simpa [chosen, inLabels] using h.arc u v huv

theorem leaf_extension_exists {R : V → V → Prop} {S : Set V} {y : V → ℕ}
    (h : Feasible R S y) (p : V) :
    (∃ y', Feasible (outRel R p) (leafSet S) y' ∧ ∀ v, y' (some v) = y v) ∨
    (∃ y', Feasible (inRel R p) (leafSet S) y' ∧ ∀ v, y' (some v) = y v) := by
  by_cases hp : y p ≤ 1
  · exact Or.inl ⟨outLabels y p, out_feasible h p hp, fun _ => rfl⟩
  · have hb := h.bounded p
    have heq : y p = 2 := by omega
    exact Or.inr ⟨inLabels y, in_feasible h p heq, fun _ => rfl⟩

theorem out_restrict {R : V → V → Prop} {S : Set V} {y' : Option V → ℕ}
    (p : V) (h : Feasible (outRel R p) (leafSet S) y') :
    Feasible R S (fun v => y' (some v)) := by
  classical
  constructor
  · exact fun v => h.bounded (some v)
  · intro v
    simpa [chosen] using h.selected_le (some v)
  · intro u v huv
    simpa [chosen] using h.arc (some u) (some v) huv

theorem in_restrict {R : V → V → Prop} {S : Set V} {y' : Option V → ℕ}
    (p : V) (h : Feasible (inRel R p) (leafSet S) y') :
    Feasible R S (fun v => y' (some v)) := by
  classical
  constructor
  · exact fun v => h.bounded (some v)
  · intro v
    simpa [chosen] using h.selected_le (some v)
  · intro u v huv
    simpa [chosen] using h.arc (some u) (some v) huv


end TreeGPLeafLabels
namespace TreeGPLeafCardinality

open SimpleGraph TreeGPRank

universe u
variable {V : Type u} {G : SimpleGraph V}

/-- Attach a single new vertex, adjacent only to p. -/
def leafGraph (G : SimpleGraph V) (p : V) : SimpleGraph (Option V) where
  Adj a b := match a, b with
    | some v, some w => G.Adj v w
    | none, some w => w = p
    | some v, none => v = p
    | none, none => False
  symm := ⟨by
    intro a b h
    cases a <;> cases b
    · exact h
    · exact h
    · exact h
    · exact h.symm⟩
  loopless := ⟨by
    intro a
    cases a with
    | none => exact not_false
    | some a => exact G.irrefl⟩

@[simp] theorem leafGraph_some_some (p : V) (v w : V) :
    (leafGraph G p).Adj (some v) (some w) ↔ G.Adj v w := Iff.rfl

@[simp] theorem leafGraph_none_some (p : V) (v : V) :
    (leafGraph G p).Adj none (some v) ↔ v = p := Iff.rfl

@[simp] theorem leafGraph_some_none (p : V) (v : V) :
    (leafGraph G p).Adj (some v) none ↔ v = p := Iff.rfl

def restrictOrientation (p : V) (O : Orientation (leafGraph G p)) : Orientation G where
  Arc v w := O.Arc (some v) (some w)
  arc_adj := fun h => O.arc_adj h
  complete := fun h => O.complete h
  asymmetric := fun h => O.asymmetric h

def outOrientation (O : Orientation G) (p : V) : Orientation (leafGraph G p) where
  Arc := TreeGPLeafLabels.outRel O.Arc p
  arc_adj := by
    intro a b h
    cases a <;> cases b
    · exact h.elim
    · exact h.elim
    · exact h
    · exact O.arc_adj h
  complete := by
    intro a b h
    cases a <;> cases b
    · exact h.elim
    · exact Or.inr h
    · exact Or.inl h
    · exact O.complete h
  asymmetric := by
    intro a b h
    cases a <;> cases b
    · exact h.elim
    · exact h.elim
    · exact not_false
    · exact O.asymmetric h

def inOrientation (O : Orientation G) (p : V) : Orientation (leafGraph G p) where
  Arc := TreeGPLeafLabels.inRel O.Arc p
  arc_adj := by
    intro a b h
    cases a <;> cases b
    · exact h.elim
    · exact h
    · exact h.elim
    · exact O.arc_adj h
  complete := by
    intro a b h
    cases a <;> cases b
    · exact h.elim
    · exact Or.inl h
    · exact Or.inr h
    · exact O.complete h
  asymmetric := by
    intro a b h
    cases a <;> cases b
    · exact h.elim
    · exact not_false
    · exact h.elim
    · exact O.asymmetric h

theorem feasible_adapter (R : V → V → Prop) (S : Set V) (y : V → ℕ) :
    TreeGPRank.Feasible R S y ↔ TreeGPLeafLabels.Feasible R S y := by
  constructor
  · rintro ⟨hv, he⟩
    exact ⟨fun v => (hv v).1, fun v => (hv v).2, he⟩
  · intro h
    exact ⟨fun v => ⟨h.bounded v, h.selected_le v⟩, h.arc⟩

theorem gp_empty (O : Orientation G) : OriginalGeneralPosition O ∅ := by
  intro u v q hu
  exact hu.elim

theorem gp_mono (O : Orientation G) {S T : Set V} (hST : S ⊆ T)
    (hT : OriginalGeneralPosition O T) : OriginalGeneralPosition O S := by
  intro u v q hu hv hq w hw hwS
  exact hT q (hST hu) (hST hv) hq hw (hST hwS)

/-- The maximum is defined using actual original GP sets, not rank sets. -/
noncomputable def gpNumber [Fintype V] (O : Orientation G) : ℕ := by
  classical
  exact Nat.findGreatest
    (fun k => ∃ s : Finset V, s.card = k ∧ OriginalGeneralPosition O (s : Set V))
    (Fintype.card V)

def Spectrum [Fintype V] (G : SimpleGraph V) : Set ℕ :=
  {k | ∃ O : Orientation G, gpNumber O = k}

theorem gpNumber_attained [Fintype V] (O : Orientation G) :
    ∃ s : Finset V, s.card = gpNumber O ∧ OriginalGeneralPosition O (s : Set V) := by
  classical
  unfold gpNumber
  exact Nat.findGreatest_spec
    (P := fun k => ∃ s : Finset V, s.card = k ∧ OriginalGeneralPosition O (s : Set V))
    (m := 0) (n := Fintype.card V) (Nat.zero_le _)
    ⟨∅, rfl, by intro u v q hu; simp at hu⟩

theorem card_le_gpNumber [Fintype V] (O : Orientation G) (s : Finset V)
    (hs : OriginalGeneralPosition O (s : Set V)) : s.card ≤ gpNumber O := by
  classical
  exact Nat.le_findGreatest (Finset.card_le_univ s) ⟨s, rfl, hs⟩

theorem gpNumber_le_card [Fintype V] (O : Orientation G) :
    gpNumber O ≤ Fintype.card V := by
  classical
  exact Nat.findGreatest_le _

def someEmbedding : V ↪ Option V := ⟨some, fun _ _ h => Option.some.inj h⟩

noncomputable def liftFinset (s : Finset V) : Finset (Option V) := s.map someEmbedding

noncomputable def addLeaf (s : Finset V) : Finset (Option V) := by
  classical
  exact insert none (liftFinset s)

@[simp] theorem mem_liftFinset_some (s : Finset V) (v : V) :
    some v ∈ liftFinset s ↔ v ∈ s := by
  classical
  constructor
  · intro h
    obtain ⟨a, ha, he⟩ := Finset.mem_map.mp h
    change some a = some v at he
    have hav : a = v := Option.some.inj he
    simpa only [hav] using ha
  · intro h
    exact Finset.mem_map.mpr ⟨v, h, rfl⟩

@[simp] theorem not_mem_liftFinset_none (s : Finset V) : none ∉ liftFinset s := by
  classical
  intro h
  obtain ⟨a, _, he⟩ := Finset.mem_map.mp h
  change some a = none at he
  cases he

@[simp] theorem liftFinset_card (s : Finset V) : (liftFinset s).card = s.card :=
  Finset.card_map _

@[simp] theorem addLeaf_card (s : Finset V) : (addLeaf s).card = s.card + 1 := by
  classical
  simp [addLeaf]

theorem leafSet_addLeaf (s : Finset V) :
    TreeGPLeafLabels.leafSet (s : Set V) = (addLeaf s : Set (Option V)) := by
  classical
  ext v
  cases v <;> simp [addLeaf]

noncomputable def coreFinset [Fintype V] (t : Finset (Option V)) : Finset V := by
  classical
  exact Finset.univ.filter (fun v => some v ∈ t)

@[simp] theorem mem_coreFinset [Fintype V] (t : Finset (Option V)) (v : V) :
    v ∈ coreFinset t ↔ some v ∈ t := by
  classical
  simp [coreFinset]

theorem card_coreFinset_le [Fintype V] (t : Finset (Option V)) :
    (coreFinset t).card ≤ t.card := by
  classical
  rw [← liftFinset_card (coreFinset t)]
  apply Finset.card_le_card
  intro v hv
  cases v with
  | none => exact (not_mem_liftFinset_none _ hv).elim
  | some v => exact (mem_coreFinset t v).mp ((mem_liftFinset_some _ v).mp hv)

theorem card_le_coreFinset_add_one [Fintype V] (t : Finset (Option V)) :
    t.card ≤ (coreFinset t).card + 1 := by
  classical
  rw [← addLeaf_card (coreFinset t)]
  apply Finset.card_le_card
  intro v hv
  cases v with
  | none => simp [addLeaf]
  | some v => simp [addLeaf, hv]

/-- Restriction works for every selected set, including one omitting the leaf. -/
theorem gp_restrict [Fintype V] (p : V) (hL : (leafGraph G p).IsAcyclic)
    (O : Orientation (leafGraph G p)) (t : Finset (Option V))
    (ht : OriginalGeneralPosition O (t : Set (Option V))) :
    OriginalGeneralPosition (restrictOrientation p O) (coreFinset t : Set V) := by
  classical
  obtain ⟨y, hy⟩ := (forest_original_iff_feasible hL O _).mp ht
  apply path_count_implies_original
  apply feasible_implies_path_count _ _ (fun v => y (some v))
  constructor
  · intro v
    simpa [hit] using hy.1 (some v)
  · intro v w hvw
    simpa [hit] using hy.2 (some v) (some w) hvw

theorem gpNumber_leaf_upper [Fintype V] (p : V) (hL : (leafGraph G p).IsAcyclic)
    (O : Orientation (leafGraph G p)) :
    gpNumber O ≤ gpNumber (restrictOrientation p O) + 1 := by
  classical
  obtain ⟨t, ht, hgp⟩ := gpNumber_attained O
  have hc := card_le_coreFinset_add_one t
  have hg := card_le_gpNumber _ _ (gp_restrict p hL O t hgp)
  omega

/-- An unselected leaf can always be added to any forest GP set. -/
theorem gp_lift (p : V) (hG : G.IsAcyclic)
    (O : Orientation (leafGraph G p)) (s : Finset V)
    (hs : OriginalGeneralPosition (restrictOrientation p O) (s : Set V)) :
    OriginalGeneralPosition O (liftFinset s : Set (Option V)) := by
  classical
  obtain ⟨y, hy⟩ := (forest_original_iff_feasible hG _ _).mp hs
  let z : Option V → ℕ := fun a => match a with
    | some v => y v
    | none => if O.Arc (some p) none then y p else 0
  apply path_count_implies_original
  apply feasible_implies_path_count _ _ z
  constructor
  · intro a
    cases a with
    | none =>
        change (if O.Arc (some p) none then y p else 0) ≤ 2 ∧
          hit (liftFinset s : Set (Option V)) none ≤
            (if O.Arc (some p) none then y p else 0)
        simp only [hit, Finset.mem_coe, not_mem_liftFinset_none, ite_false]
        split <;> constructor <;> try omega
        exact (hy.1 p).1
    | some v => simpa [z, hit] using hy.1 v
  · intro a b hab
    have he := O.arc_adj hab
    cases a with
    | none =>
        cases b with
        | none => exact he.elim
        | some v =>
            have hv : v = p := he
            subst v
            have hdir : ¬ O.Arc (some p) none := O.asymmetric hab
            simpa [z, hit, hdir] using (hy.1 p).2
    | some v =>
        cases b with
        | none =>
            have hv : v = p := he
            subst v
            simp [z, hit, hab]
        | some w => simpa [z, hit] using hy.2 v w hab

theorem gpNumber_core_le_leaf [Fintype V] (p : V) (hG : G.IsAcyclic)
    (O : Orientation (leafGraph G p)) :
    gpNumber (restrictOrientation p O) ≤ gpNumber O := by
  obtain ⟨s, hs, hgp⟩ := gpNumber_attained (restrictOrientation p O)
  have hc := card_le_gpNumber O (liftFinset s) (gp_lift p hG O s hgp)
  simpa only [liftFinset_card, hs] using hc

theorem gpNumber_leaf_two_values [Fintype V] (p : V) (hG : G.IsAcyclic)
    (hL : (leafGraph G p).IsAcyclic) (O : Orientation (leafGraph G p)) :
    gpNumber O = gpNumber (restrictOrientation p O) ∨
      gpNumber O = gpNumber (restrictOrientation p O) + 1 := by
  have hlo := gpNumber_core_le_leaf p hG O
  have hhi := gpNumber_leaf_upper p hL O
  omega

theorem gp_add_leaf (p : V) (hG : G.IsAcyclic) (O : Orientation G) (s : Finset V)
    (hs : OriginalGeneralPosition O (s : Set V)) :
    OriginalGeneralPosition (outOrientation O p) (addLeaf s : Set (Option V)) ∨
      OriginalGeneralPosition (inOrientation O p) (addLeaf s : Set (Option V)) := by
  classical
  obtain ⟨y, hy⟩ := (forest_original_iff_feasible hG O _).mp hs
  have hY := (feasible_adapter _ _ _).mp hy
  rcases TreeGPLeafLabels.leaf_extension_exists hY p with ⟨z, hz, _⟩ | ⟨z, hz, _⟩
  · apply Or.inl
    apply path_count_implies_original
    apply feasible_implies_path_count _ _ z
    rw [← leafSet_addLeaf]
    exact (feasible_adapter _ _ _).mpr hz
  · apply Or.inr
    apply path_count_implies_original
    apply feasible_implies_path_count _ _ z
    rw [← leafSet_addLeaf]
    exact (feasible_adapter _ _ _).mpr hz

@[simp] theorem restrict_out (O : Orientation G) (p : V) :
    restrictOrientation p (outOrientation O p) = O := by
  cases O
  rfl

@[simp] theorem restrict_in (O : Orientation G) (p : V) :
    restrictOrientation p (inOrientation O p) = O := by
  cases O
  rfl

theorem gpNumber_leaf_successor [Fintype V] (p : V) (hG : G.IsAcyclic)
    (hL : (leafGraph G p).IsAcyclic) (O : Orientation G) :
    ∃ O' : Orientation (leafGraph G p), gpNumber O' = gpNumber O + 1 := by
  obtain ⟨s, hs, hgp⟩ := gpNumber_attained O
  rcases gp_add_leaf p hG O s hgp with hout | hin
  · refine ⟨outOrientation O p, ?_⟩
    have hlo := card_le_gpNumber _ _ hout
    have hhi := gpNumber_leaf_upper p hL (outOrientation O p)
    simp only [addLeaf_card, hs] at hlo
    simp only [restrict_out] at hhi
    omega
  · refine ⟨inOrientation O p, ?_⟩
    have hlo := card_le_gpNumber _ _ hin
    have hhi := gpNumber_leaf_upper p hL (inOrientation O p)
    simp only [addLeaf_card, hs] at hlo
    simp only [restrict_in] at hhi
    omega

theorem successor_mem_spectrum [Fintype V] (p : V) (hG : G.IsAcyclic)
    (hL : (leafGraph G p).IsAcyclic) {k : ℕ} (hk : k ∈ Spectrum G) :
    k + 1 ∈ Spectrum (leafGraph G p) := by
  obtain ⟨O, rfl⟩ := hk
  exact gpNumber_leaf_successor p hG hL O

theorem spectrum_leaf_subset [Fintype V] (p : V) (hG : G.IsAcyclic)
    (hL : (leafGraph G p).IsAcyclic) {k : ℕ} (hk : k ∈ Spectrum (leafGraph G p)) :
    ∃ j ∈ Spectrum G, k = j ∨ k = j + 1 := by
  obtain ⟨O, rfl⟩ := hk
  exact ⟨_, ⟨restrictOrientation p O, rfl⟩, gpNumber_leaf_two_values p hG hL O⟩


end TreeGPLeafCardinality

namespace TreeGPSpectrumInduction

open SimpleGraph
open TreeGPRank
open TreeGPLeafCardinality

universe u
variable {V : Type u} {G : SimpleGraph V}

/-- Exactly the old vertex type after deletion of the specified leaf. -/
abbrev Core (l : V) := {v : V // v ≠ l}

/-- Actual induced deletion, not an abstract graph with a smaller cardinality. -/
def coreGraph (G : SimpleGraph V) (l : V) : SimpleGraph (Core l) :=
  G.induce {v | v ≠ l}

@[simp] theorem coreGraph_adj (G : SimpleGraph V) (l : V) (v w : Core l) :
    (coreGraph G l).Adj v w ↔ G.Adj v.val w.val := Iff.rfl

/-- Every orientation of the original tree has its actual core restriction. -/
def restrictOrientation (O : Orientation G) (l : V) : Orientation (coreGraph G l) where
  Arc v w := O.Arc v.val w.val
  arc_adj h := O.arc_adj h
  complete h := O.complete h
  asymmetric h := O.asymmetric h

/-- Mathlib's connected-deletion theorem plus inherited acyclicity. -/
theorem core_isTree [Fintype V] [DecidableRel G.Adj]
    (hG : G.IsTree) (l : V) (hl : G.degree l = 1) : (coreGraph G l).IsTree := by
  refine ⟨?_, hG.isAcyclic.induce _⟩
  change (G.induce {l}ᶜ).Connected
  exact hG.connected.induce_compl_singleton_of_degree_eq_one hl

/-- The Option construction is the original graph, with the removed vertex
as none. Every adjacency is proved, including the unique leaf neighbour. -/
noncomputable def leafCoreIso [DecidableEq V] (G : SimpleGraph V) (l : V)
    (p : Core l) (hlp : G.Adj l p.val)
    (hunique : ∀ v, G.Adj l v → v = p.val) :
    leafGraph (coreGraph G l) p ≃g G where
  toEquiv := Equiv.optionSubtypeNe l
  map_rel_iff' := by
    intro x y
    cases x with
    | none =>
        cases y with
        | none =>
            change G.Adj l l ↔ False
            simp
        | some y =>
            change G.Adj l y.val ↔ y = p
            constructor
            · intro h
              exact Subtype.ext (hunique y.val h)
            · intro h
              subst y
              exact hlp
    | some x =>
        cases y with
        | none =>
            change G.Adj x.val l ↔ x = p
            constructor
            · intro h
              exact Subtype.ext (hunique x.val h.symm)
            · intro h
              subst x
              exact hlp.symm
        | some y =>
            change G.Adj x.val y.val ↔ G.Adj x.val y.val
            rfl

theorem leaf_iso_of_degree_one [Fintype V] [DecidableEq V] [DecidableRel G.Adj]
    (l : V) (hl : G.degree l = 1) :
    ∃ p : Core l, Nonempty (leafGraph (coreGraph G l) p ≃g G) := by
  obtain ⟨p, hlp, hp⟩ := SimpleGraph.degree_eq_one_iff_existsUnique_adj.mp hl
  let p₀ : Core l := ⟨p, fun h => hlp.ne h.symm⟩
  exact ⟨p₀, ⟨leafCoreIso G l p₀ hlp (fun v hv => hp v hv)⟩⟩

theorem card_core_add_one [Fintype V] [DecidableEq V] (l : V) :
    Fintype.card (Core l) + 1 = Fintype.card V := by
  simpa only [Fintype.card_option] using Fintype.card_congr (Equiv.optionSubtypeNe l)

theorem card_core_lt [Fintype V] [DecidableEq V] (l : V) :
    Fintype.card (Core l) < Fintype.card V := by
  have h := card_core_add_one l
  omega

/-- Actual finite nontrivial tree decomposition. The final graph in this
witness is proved to be IsTree via its isomorphism to the original tree. -/
theorem finite_tree_leaf_decomposition [Fintype V] [DecidableEq V]
    [DecidableRel G.Adj] [Nontrivial V] (hG : G.IsTree) :
    ∃ l : V, G.degree l = 1 ∧ (coreGraph G l).IsTree ∧
      Fintype.card (Core l) + 1 = Fintype.card V ∧
      ∃ p : Core l, (leafGraph (coreGraph G l) p).IsTree ∧
        Nonempty (leafGraph (coreGraph G l) p ≃g G) := by
  obtain ⟨l, hl⟩ := hG.exists_vert_degree_one_of_nontrivial
  obtain ⟨p, ⟨e⟩⟩ := leaf_iso_of_degree_one l hl
  refine ⟨l, hl, core_isTree hG l hl, card_core_add_one l, p, ?_, ⟨e⟩⟩
  exact e.isTree_iff.mpr hG

/-- A genuine structural induction principle over arbitrary finite IsTree
graphs. Its property arguments are explicit and are not unproved GP axioms.
The leaf step receives both actual tree hypotheses, matching the cardinality
module's need for acyclicity of both graphs. -/
theorem finite_tree_leaf_induction
    (P : ∀ (W : Type u), [Fintype W] → SimpleGraph W → Prop)
    (base : ∀ (W : Type u) [Fintype W] [Nonempty W] [Subsingleton W]
      (H : SimpleGraph W), P W H)
    (iso : ∀ {W W' : Type u} [Fintype W] [Fintype W']
      {H : SimpleGraph W} {H' : SimpleGraph W'}, H ≃g H' → P W H → P W' H')
    (leaf : ∀ {W : Type u} [Fintype W] (H : SimpleGraph W) (p : W),
      H.IsTree → (leafGraph H p).IsTree → P W H → P (Option W) (leafGraph H p))
    [Fintype V] (hG : G.IsTree) : P V G := by
  classical
  have main : ∀ n : ℕ, ∀ (W : Type u) [Fintype W] (H : SimpleGraph W),
      Fintype.card W = n → H.IsTree → P W H := by
    intro n
    induction n using Nat.strong_induction_on with
    | h n ih =>
        intro W _ H hcard hH
        rcases subsingleton_or_nontrivial W with hs | hn
        · let : Subsingleton W := hs
          let : Nonempty W := hH.connected.nonempty
          exact base W H
        · let : Nontrivial W := hn
          obtain ⟨l, hl, hcore, hsize, p, hleaf, ⟨e⟩⟩ :=
            finite_tree_leaf_decomposition hH
          have hlt : Fintype.card (Core l) < n := by omega
          have hP : P (Core l) (coreGraph H l) :=
            ih (Fintype.card (Core l)) hlt (Core l) (coreGraph H l) rfl hcore
          exact iso e (leaf (coreGraph H l) p hcore hleaf hP)
  exact main (Fintype.card V) V G rfl hG

/-- The two possible intervals between a complete successor interval and its
one-point larger envelope. This is independent of any GP assumption. -/
theorem interval_sandwich (B : Set ℕ) (L U : ℕ)
    (inside : ∀ k, L + 1 ≤ k → k ≤ U + 1 → k ∈ B)
    (outside : ∀ k, k ∈ B → L ≤ k ∧ k ≤ U + 1) :
    B = Set.Icc L (U + 1) ∨ B = Set.Icc (L + 1) (U + 1) := by
  classical
  by_cases hL : L ∈ B
  · left
    ext k
    constructor
    · exact outside k
    · intro hk
      by_cases hkL : k = L
      · simpa only [hkL] using hL
      · exact inside k (by have := hk.1; omega) hk.2
  · right
    ext k
    constructor
    · intro hk
      have hb := outside k hk
      have hne : k ≠ L := by intro he; exact hL (he ▸ hk)
      exact ⟨by omega, hb.2⟩
    · exact fun hk => inside k hk.1 hk.2

/-- Integer-interval consequence of the leaf-step interfaces. This theorem
does not assert that an actual GP spectrum satisfies either interface. -/
theorem interval_from_leaf_steps (A B : Set ℕ) (L U : ℕ)
    (core : A = Set.Icc L U)
    (successor : ∀ j, j ∈ A → j + 1 ∈ B)
    (restriction : ∀ k, k ∈ B → ∃ j, j ∈ A ∧ (k = j ∨ k = j + 1)) :
    B = Set.Icc L (U + 1) ∨ B = Set.Icc (L + 1) (U + 1) := by
  apply interval_sandwich B L U
  · intro k hlo hhi
    have hm : k - 1 ∈ A := by
      rw [core]
      exact ⟨by omega, by omega⟩
    have hsucc := successor (k - 1) hm
    have heq : k - 1 + 1 = k := by omega
    simpa only [heq] using hsucc
  · intro k hk
    obtain ⟨j, hj, hkj⟩ := restriction k hk
    rw [core] at hj
    change L ≤ j ∧ j ≤ U at hj
    rcases hkj with h | h <;> constructor <;> omega




end TreeGPSpectrumInduction

namespace TreeGPIsoTransport

open SimpleGraph TreeGPRank TreeGPLeafCardinality

universe u v
variable {V : Type u} {W : Type v}
variable {G : SimpleGraph V} {H : SimpleGraph W}

/-- Orientation proof fields are propositions; equality of actual arcs suffices. -/
theorem orientation_ext {O P : Orientation G} (h : O.Arc = P.Arc) : O = P := by
  cases O
  cases P
  cases h
  rfl

/-- Push an orientation along a genuine simple-graph isomorphism. -/
def pushOrientation (e : G ≃g H) (O : Orientation G) : Orientation H where
  Arc x y := O.Arc (e.symm x) (e.symm y)
  arc_adj := by
    intro x y h
    have h' := e.toHom.map_adj (O.arc_adj h)
    change H.Adj (e (e.symm x)) (e (e.symm y)) at h'
    simpa only [RelIso.apply_symm_apply] using h'
  complete := by
    intro x y h
    exact O.complete (e.symm.toHom.map_adj h)
  asymmetric := by
    intro x y h
    exact O.asymmetric h

@[simp] theorem push_arc_apply (e : G ≃g H) (O : Orientation G) (x y : V) :
    (pushOrientation e O).Arc (e x) (e y) ↔ O.Arc x y := by
  change O.Arc (e.symm (e x)) (e.symm (e y)) ↔ O.Arc x y
  simp only [RelIso.symm_apply_apply]

@[simp] theorem push_symm_push (e : G ≃g H) (O : Orientation G) :
    pushOrientation e.symm (pushOrientation e O) = O := by
  apply orientation_ext
  funext x y
  simp only [pushOrientation, RelIso.symm_symm, RelIso.symm_apply_apply]

/-- In particular, all orientations are transported bijectively. -/
def orientationEquiv (e : G ≃g H) : Orientation G ≃ Orientation H where
  toFun := pushOrientation e
  invFun := pushOrientation e.symm
  left_inv := push_symm_push e
  right_inv := by
    intro O
    simpa only [RelIso.symm_symm] using push_symm_push e.symm O

/-- The mapped actual walk follows exactly the transported actual arcs. -/
theorem follows_map_iff (e : G ≃g H) (O : Orientation G)
    {a b : V} (p : G.Walk a b) :
    Follows (pushOrientation e O).Arc (p.map e.toHom) ↔ Follows O.Arc p := by
  induction p with
  | nil => rfl
  | @cons a b c h p ih =>
      change ((pushOrientation e O).Arc (e a) (e b) ∧
        Follows (pushOrientation e O).Arc (p.map e.toHom)) ↔
        (O.Arc a b ∧ Follows O.Arc p)
      simp only [push_arc_apply, ih]

/-- Map the actual walk and transport both its simplicity and direction proofs. -/
def mapPath (e : G ≃g H) (O : Orientation G) {a b : V}
    (p : DirectedSimplePath O a b) :
    DirectedSimplePath (pushOrientation e O) (e a) (e b) where
  walk := p.walk.map e.toHom
  isPath := p.isPath.map e.injective
  follows := (follows_map_iff e O p.walk).mpr p.follows

@[simp] theorem mapPath_length (e : G ≃g H) (O : Orientation G) {a b : V}
    (p : DirectedSimplePath O a b) :
    (mapPath e O p).walk.length = p.walk.length := by
  exact SimpleGraph.Walk.length_map e.toHom p.walk

@[simp] theorem mapPath_support (e : G ≃g H) (O : Orientation G) {a b : V}
    (p : DirectedSimplePath O a b) :
    (mapPath e O p).walk.support = p.walk.support.map e := by
  exact SimpleGraph.Walk.support_map e.toHom p.walk

/-- Reindex only endpoints by equality; this is the actual `Walk.copy`. -/
def copyPath {O : Orientation G} {a b a' b' : V}
    (p : DirectedSimplePath O a b) (ha : a = a') (hb : b = b') :
    DirectedSimplePath O a' b' where
  walk := p.walk.copy ha hb
  isPath := by
    cases ha
    cases hb
    exact p.isPath
  follows := by
    cases ha
    cases hb
    exact p.follows

@[simp] theorem copyPath_length {O : Orientation G} {a b a' b' : V}
    (p : DirectedSimplePath O a b) (ha : a = a') (hb : b = b') :
    (copyPath p ha hb).walk.length = p.walk.length := by
  cases ha
  cases hb
  rfl

@[simp] theorem copyPath_support {O : Orientation G} {a b a' b' : V}
    (p : DirectedSimplePath O a b) (ha : a = a') (hb : b = b') :
    (copyPath p ha hb).walk.support = p.walk.support := by
  cases ha
  cases hb
  rfl

/-- Inverse mapping has arbitrary target endpoints, not just mapped endpoints. -/
def pullPath (e : G ≃g H) (O : Orientation G) {x y : W}
    (q : DirectedSimplePath (pushOrientation e O) x y) :
    DirectedSimplePath O (e.symm x) (e.symm y) where
  walk := q.walk.map e.symm.toHom
  isPath := q.isPath.map e.symm.injective
  follows := by
    simpa only [push_symm_push] using
      (follows_map_iff e.symm (pushOrientation e O) q.walk).mpr q.follows

@[simp] theorem pullPath_length (e : G ≃g H) (O : Orientation G) {x y : W}
    (q : DirectedSimplePath (pushOrientation e O) x y) :
    (pullPath e O q).walk.length = q.walk.length := by
  exact SimpleGraph.Walk.length_map e.symm.toHom q.walk

@[simp] theorem pullPath_support (e : G ≃g H) (O : Orientation G) {x y : W}
    (q : DirectedSimplePath (pushOrientation e O) x y) :
    (pullPath e O q).walk.support = q.walk.support.map e.symm := by
  exact SimpleGraph.Walk.support_map e.symm.toHom q.walk

/-- Compare against every target path by pulling it back, preserving length. -/
theorem isShortest_map (e : G ≃g H) (O : Orientation G) {a b : V}
    (p : DirectedSimplePath O a b) (hp : IsShortest p) :
    IsShortest (mapPath e O p) := by
  intro q
  have h := hp (copyPath (pullPath e O q)
    (e.symm_apply_apply a) (e.symm_apply_apply b))
  simpa only [copyPath_length, pullPath_length, mapPath_length] using h

/-- Compare against every source path by mapping it, preserving length. -/
theorem isShortest_pull (e : G ≃g H) (O : Orientation G) {x y : W}
    (q : DirectedSimplePath (pushOrientation e O) x y) (hq : IsShortest q) :
    IsShortest (pullPath e O q) := by
  intro p
  have h := hq (copyPath (mapPath e O p)
    (e.apply_symm_apply x) (e.apply_symm_apply y))
  simpa only [copyPath_length, mapPath_length, pullPath_length] using h

theorem isShortest_map_iff (e : G ≃g H) (O : Orientation G) {a b : V}
    (p : DirectedSimplePath O a b) :
    IsShortest (mapPath e O p) ↔ IsShortest p := by
  constructor
  · intro hp q
    have h := hp (mapPath e O q)
    simpa only [mapPath_length] using h
  · exact isShortest_map e O p

theorem symm_mem_image (e : G ≃g H) (S : Set V) (x : W) :
    e.symm x ∈ S ↔ x ∈ e '' S := by
  constructor
  · intro hx
    exact ⟨e.symm x, hx, e.apply_symm_apply x⟩
  · rintro ⟨a, ha, hax⟩
    have h : e.symm x = a := by
      rw [← hax, RelIso.symm_apply_apply]
    simpa only [h] using ha

/-- The original GP predicate is transported, using all real shortest paths. -/
theorem originalGP_image_iff (e : G ≃g H) (O : Orientation G) (S : Set V) :
    OriginalGeneralPosition O S ↔
      OriginalGeneralPosition (pushOrientation e O) (e '' S) := by
  constructor
  · intro h x y q hx hy hq w hw hwS
    have hx' := (symm_mem_image e S x).mpr hx
    have hy' := (symm_mem_image e S y).mpr hy
    have hwS' := (symm_mem_image e S w).mpr hwS
    have hw' : e.symm w ∈ (pullPath e O q).walk.support := by
      rw [pullPath_support]
      exact List.mem_map.mpr ⟨w, hw, rfl⟩
    have hends := h (pullPath e O q) hx' hy' (isShortest_pull e O q hq) hw' hwS'
    rcases hends with hwu | hwv
    · left
      have h' := congrArg e hwu
      simpa only [RelIso.apply_symm_apply] using h'
    · right
      have h' := congrArg e hwv
      simpa only [RelIso.apply_symm_apply] using h'
  · intro h a b p ha hb hp w hw hwS
    have ha' : e a ∈ e '' S := ⟨a, ha, rfl⟩
    have hb' : e b ∈ e '' S := ⟨b, hb, rfl⟩
    have hwS' : e w ∈ e '' S := ⟨w, hwS, rfl⟩
    have hw' : e w ∈ (mapPath e O p).walk.support := by
      rw [mapPath_support]
      exact List.mem_map.mpr ⟨w, hw, rfl⟩
    have hends := h (mapPath e O p) ha' hb' (isShortest_map e O p hp) hw' hwS'
    exact hends.imp (fun hh => e.injective hh) (fun hh => e.injective hh)

/-- Finset transport uses its actual coerced set and an injective `Finset.map`. -/
theorem originalGP_finset_map (e : G ≃g H) (O : Orientation G) (s : Finset V)
    (hs : OriginalGeneralPosition O (s : Set V)) :
    OriginalGeneralPosition (pushOrientation e O)
      (s.map e.toEquiv.toEmbedding : Set W) := by
  rw [Finset.coe_map]
  change OriginalGeneralPosition (pushOrientation e O) (e '' (s : Set V))
  intro a b q ha hb hq w hw hwS
  exact ((originalGP_image_iff e O (s : Set V)).mp hs) q ha hb hq hw hwS

/-- An attained maximum maps to a GP set of exactly the same cardinality. -/
theorem gpNumber_le_push [Fintype V] [Fintype W]
    (e : G ≃g H) (O : Orientation G) :
    gpNumber O ≤ gpNumber (pushOrientation e O) := by
  obtain ⟨s, hs, hgp⟩ := gpNumber_attained O
  have h := card_le_gpNumber (pushOrientation e O) (s.map e.toEquiv.toEmbedding)
    (originalGP_finset_map e O s hgp)
  simpa only [Finset.card_map, hs] using h

theorem gpNumber_push [Fintype V] [Fintype W]
    (e : G ≃g H) (O : Orientation G) :
    gpNumber (pushOrientation e O) = gpNumber O := by
  apply Nat.le_antisymm
  · have h := gpNumber_le_push e.symm (pushOrientation e O)
    simpa only [push_symm_push] using h
  · exact gpNumber_le_push e O

/-- The spectrum of all actual orientations is invariant under a graph iso. -/
theorem spectrum_iso [Fintype V] [Fintype W] (e : G ≃g H) :
    Spectrum G = Spectrum H := by
  ext k
  constructor
  · rintro ⟨O, hO⟩
    refine ⟨pushOrientation e O, ?_⟩
    rw [gpNumber_push]
    exact hO
  · rintro ⟨O, hO⟩
    refine ⟨pushOrientation e.symm O, ?_⟩
    rw [gpNumber_push]
    exact hO


end TreeGPIsoTransport

namespace TreeGPSpectrumFinal

open SimpleGraph TreeGPRank TreeGPLeafCardinality

universe u
variable {V : Type u} {G : SimpleGraph V}

def trivialOrientation [Subsingleton V] (G : SimpleGraph V) : Orientation G where
  Arc _ _ := False
  arc_adj h := h.elim
  complete := by
    intro a b hab
    exact (hab.ne (Subsingleton.elim a b)).elim
  asymmetric h := h.elim

theorem gp_subsingleton [Subsingleton V] (O : Orientation G) (S : Set V) :
    OriginalGeneralPosition O S := by
  intro a b q _ _ _ w _ _
  exact Or.inl (Subsingleton.elim w a)

theorem gpNumber_subsingleton [Fintype V] [Subsingleton V] (O : Orientation G) :
    gpNumber O = Fintype.card V := by
  apply Nat.le_antisymm (gpNumber_le_card O)
  have h := card_le_gpNumber O Finset.univ (gp_subsingleton O _)
  simpa only [Finset.card_univ] using h

theorem spectrum_subsingleton [Fintype V] [Subsingleton V] (G : SimpleGraph V) :
    Spectrum G = Set.Icc (Fintype.card V) (Fintype.card V) := by
  ext k
  constructor
  · rintro ⟨O, rfl⟩
    rw [gpNumber_subsingleton]
    exact ⟨le_rfl, le_rfl⟩
  · intro hk
    have he : k = Fintype.card V := by
      have := hk.1
      have := hk.2
      omega
    exact ⟨trivialOrientation G, (gpNumber_subsingleton _).trans he.symm⟩

def IsInterval [Fintype V] (G : SimpleGraph V) : Prop :=
  ∃ L U : ℕ, L ≤ U ∧ Spectrum G = Set.Icc L U

theorem leaf_interval [Fintype V] (p : V) (hG : G.IsTree)
    (hL : (leafGraph G p).IsTree) (hI : IsInterval G) :
    IsInterval (leafGraph G p) := by
  obtain ⟨L, U, hLU, hcore⟩ := hI
  have h := TreeGPSpectrumInduction.interval_from_leaf_steps
    (Spectrum G) (Spectrum (leafGraph G p)) L U hcore
    (fun _ hj => successor_mem_spectrum p hG.isAcyclic hL.isAcyclic hj)
    (fun _ hk => spectrum_leaf_subset p hG.isAcyclic hL.isAcyclic hk)
  rcases h with h | h
  · exact ⟨L, U + 1, by omega, h⟩
  · exact ⟨L + 1, U + 1, by omega, h⟩

/-- The original directed shortest-simple-path GP spectrum of every actual
finite undirected tree is a complete integer interval. -/
theorem finite_tree_spectrum_interval [Fintype V] (hG : G.IsTree) : IsInterval G := by
  apply TreeGPSpectrumInduction.finite_tree_leaf_induction
    (P := fun W _ H => IsInterval H)
  · intro W _ _ _ H
    exact ⟨Fintype.card W, Fintype.card W, le_rfl, spectrum_subsingleton H⟩
  · intro W W' _ _ H H' e hI
    obtain ⟨L, U, hLU, hspec⟩ := hI
    refine ⟨L, U, hLU, ?_⟩
    rw [← TreeGPIsoTransport.spectrum_iso e]
    exact hspec
  · intro W _ H p hH hL hI
    exact leaf_interval p hH hL hI
  · exact hG


end TreeGPSpectrumFinal

#print axioms TreeGPRank.follows_isPath
#print axioms TreeGPRank.every_path_shortest
#print axioms TreeGPRank.prefix_selected
#print axioms TreeGPRank.original_iff_path_count
#print axioms TreeGPRank.endpointRank_feasible
#print axioms TreeGPRank.path_count_iff_feasible
#print axioms TreeGPRank.forest_original_iff_feasible
#print axioms TreeGPRank.tree_original_iff_feasible
#print axioms TreeGPLeafLabels.chosen_le_one
#print axioms TreeGPLeafLabels.out_feasible
#print axioms TreeGPLeafLabels.in_feasible
#print axioms TreeGPLeafLabels.leaf_extension_exists
#print axioms TreeGPLeafLabels.out_restrict
#print axioms TreeGPLeafLabels.in_restrict
#print axioms TreeGPLeafCardinality.feasible_adapter
#print axioms TreeGPLeafCardinality.gpNumber_attained
#print axioms TreeGPLeafCardinality.gp_restrict
#print axioms TreeGPLeafCardinality.gpNumber_leaf_upper
#print axioms TreeGPLeafCardinality.gp_lift
#print axioms TreeGPLeafCardinality.gpNumber_leaf_two_values
#print axioms TreeGPLeafCardinality.gp_add_leaf
#print axioms TreeGPLeafCardinality.gpNumber_leaf_successor
#print axioms TreeGPLeafCardinality.successor_mem_spectrum
#print axioms TreeGPLeafCardinality.spectrum_leaf_subset
#print axioms TreeGPSpectrumInduction.core_isTree
#print axioms TreeGPSpectrumInduction.leafCoreIso
#print axioms TreeGPSpectrumInduction.leaf_iso_of_degree_one
#print axioms TreeGPSpectrumInduction.card_core_add_one
#print axioms TreeGPSpectrumInduction.finite_tree_leaf_decomposition
#print axioms TreeGPSpectrumInduction.finite_tree_leaf_induction
#print axioms TreeGPSpectrumInduction.interval_sandwich
#print axioms TreeGPSpectrumInduction.interval_from_leaf_steps
#print axioms TreeGPIsoTransport.orientationEquiv
#print axioms TreeGPIsoTransport.follows_map_iff
#print axioms TreeGPIsoTransport.isShortest_map_iff
#print axioms TreeGPIsoTransport.isShortest_pull
#print axioms TreeGPIsoTransport.originalGP_image_iff
#print axioms TreeGPIsoTransport.originalGP_finset_map
#print axioms TreeGPIsoTransport.gpNumber_push
#print axioms TreeGPIsoTransport.spectrum_iso
#print axioms TreeGPSpectrumFinal.gpNumber_subsingleton
#print axioms TreeGPSpectrumFinal.spectrum_subsingleton
#print axioms TreeGPSpectrumFinal.leaf_interval
#print axioms TreeGPSpectrumFinal.finite_tree_spectrum_interval
