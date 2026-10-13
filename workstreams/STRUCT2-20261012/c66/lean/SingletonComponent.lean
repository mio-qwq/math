import ComponentSupport

/-!
The actual ungrounded singleton components used by EXACT_WINDOW.md.
No probability, finite-cardinality or asymptotic theorem is assumed or
claimed here. The closure includes every ordered equation and the ground.
-/

set_option Elab.async false

namespace Struct2.C66.SingletonComponent

open ComponentSupport

def OneEdge {V : Type} (i j x y : V) : Prop :=
  (x = i ∧ y = j) ∨ (x = j ∧ y = i)

def SharedEdgeAction {V : Type} (a b : Perm V) (i j : V) : Prop :=
  (a.forward i = i ∧ a.forward j = j ∧
    b.forward i = i ∧ b.forward j = j) ∨
  (a.forward i = j ∧ a.forward j = i ∧
    b.forward i = j ∧ b.forward j = i)

theorem perm_injective {V : Type} (a : Perm V) {x y : V}
    (h : a.forward x = a.forward y) : x = y := by
  have hh := congrArg a.backward h
  simpa only [a.left_inv] using hh

theorem one_edge_invariant_iff {V : Type} (a b : Perm V) (i j : V)
    (hne : i ≠ j) :
    TFInvariant (OneEdge i j) a b ↔ SharedEdgeAction a b i j := by
  constructor
  · intro h
    have hij := (h i j).mpr (Or.inl ⟨rfl, rfl⟩)
    have hji := (h j i).mpr (Or.inr ⟨rfl, rfl⟩)
    rcases hij with ⟨ai, bj⟩ | ⟨ai, bj⟩
    · rcases hji with ⟨aj, bi⟩ | ⟨aj, bi⟩
      · exact False.elim (hne (perm_injective a (ai.trans aj.symm)))
      · exact Or.inl ⟨ai, aj, bi, bj⟩
    · rcases hji with ⟨aj, bi⟩ | ⟨aj, bi⟩
      · exact Or.inr ⟨ai, aj, bi, bj⟩
      · exact False.elim (hne (perm_injective a (ai.trans aj.symm)))
  · rintro (⟨ai, aj, bi, bj⟩ | ⟨ai, aj, bi, bj⟩) x y
    · constructor
      · rintro (⟨hx, hy⟩ | ⟨hx, hy⟩)
        · exact Or.inl ⟨perm_injective a (hx.trans ai.symm),
            perm_injective b (hy.trans bj.symm)⟩
        · exact Or.inr ⟨perm_injective a (hx.trans aj.symm),
            perm_injective b (hy.trans bi.symm)⟩
      · rintro (⟨rfl, rfl⟩ | ⟨rfl, rfl⟩)
        · exact Or.inl ⟨ai, bj⟩
        · exact Or.inr ⟨aj, bi⟩
    · constructor
      · rintro (⟨hx, hy⟩ | ⟨hx, hy⟩)
        · exact Or.inr ⟨perm_injective a (hx.trans aj.symm),
            perm_injective b (hy.trans bi.symm)⟩
        · exact Or.inl ⟨perm_injective a (hx.trans ai.symm),
            perm_injective b (hy.trans bj.symm)⟩
      · rintro (⟨rfl, rfl⟩ | ⟨rfl, rfl⟩)
        · exact Or.inr ⟨ai, bj⟩
        · exact Or.inl ⟨aj, bi⟩

theorem edge_variable_nonzero {n : Nat} (i j : Fin n) (hne : i ≠ j) :
    edgeVariable i j ≠ none := by
  by_cases hl : i.val < j.val <;> simp [edgeVariable, hne, hl]

theorem edge_variable_fiber {n : Nat} (i j x y : Fin n) (hne : i ≠ j) :
    edgeVariable x y = edgeVariable i j ↔ OneEdge i j x y := by
  classical
  by_cases hxy : x = y <;> by_cases hlxy : x.val < y.val <;>
    by_cases hlij : i.val < j.val <;> simp_all [edgeVariable, OneEdge]
  all_goals grind [Fin.ext_iff]

def FreeSingleton {n : Nat} (a b : Perm (Fin n)) (i j : Fin n) : Prop :=
  edgeVariable i j ≠ none ∧
  ∀ v, FullConnected a b (edgeVariable i j) v → v = edgeVariable i j

theorem singleton_adjacency {n : Nat} (a b : Perm (Fin n))
    (i j : Fin n) (hne : i ≠ j) (hs : FreeSingleton a b i j)
    (x y : Fin n) :
    componentAdj a b (edgeVariable i j) x y ↔ OneEdge i j x y := by
  constructor
  · intro hc
    exact (edge_variable_fiber i j x y hne).mp (hs.2 _ hc)
  · intro he
    change FullConnected a b (edgeVariable i j) (edgeVariable x y)
    rw [(edge_variable_fiber i j x y hne).mpr he]
    exact .refl _

theorem singleton_implies_invariant {n : Nat} (a b : Perm (Fin n))
    (i j : Fin n) (hne : i ≠ j) (hs : FreeSingleton a b i j) :
    TFInvariant (OneEdge i j) a b := by
  intro x y
  exact (singleton_adjacency a b i j hne hs _ _).symm.trans
    ((full_component_invariant a b (edgeVariable i j) x y).trans
      (singleton_adjacency a b i j hne hs x y))

theorem invariant_fiber_transport {n : Nat} (a b : Perm (Fin n))
    (i j : Fin n) (hne : i ≠ j) (hi : TFInvariant (OneEdge i j) a b)
    {v w : Option (Fin n × Fin n)} (hc : FullConnected a b v w) :
    (v = edgeVariable i j ↔ w = edgeVariable i j) := by
  induction hc with
  | refl => exact Iff.rfl
  | equation x y =>
    exact (edge_variable_fiber i j x y hne).trans
      ((hi x y).symm.trans (edge_variable_fiber i j _ _ hne).symm)
  | symm _ ih => exact ih.symm
  | trans _ _ ih1 ih2 => exact ih1.trans ih2

theorem invariant_implies_singleton {n : Nat} (a b : Perm (Fin n))
    (i j : Fin n) (hne : i ≠ j) (hi : TFInvariant (OneEdge i j) a b) :
    FreeSingleton a b i j := by
  refine ⟨edge_variable_nonzero i j hne, ?_⟩
  intro v hc
  exact (invariant_fiber_transport a b i j hne hi hc).mp rfl

theorem actual_singleton_classification {n : Nat} (a b : Perm (Fin n))
    (i j : Fin n) (hne : i ≠ j) :
    FreeSingleton a b i j ↔ SharedEdgeAction a b i j := by
  constructor
  · intro hs
    exact (one_edge_invariant_iff a b i j hne).mp
      (singleton_implies_invariant a b i j hne hs)
  · intro ha
    exact invariant_implies_singleton a b i j hne
      ((one_edge_invariant_iff a b i j hne).mpr ha)

theorem singleton_is_ungrounded {n : Nat} (a b : Perm (Fin n))
    (i j : Fin n) (hs : FreeSingleton a b i j) :
    ¬FullConnected a b (edgeVariable i j) none := by
  intro hc
  exact hs.1 (hs.2 none hc).symm

#print axioms one_edge_invariant_iff
#print axioms edge_variable_nonzero
#print axioms edge_variable_fiber
#print axioms singleton_adjacency
#print axioms singleton_implies_invariant
#print axioms invariant_fiber_transport
#print axioms invariant_implies_singleton
#print axioms actual_singleton_classification
#print axioms singleton_is_ungrounded

end Struct2.C66.SingletonComponent
