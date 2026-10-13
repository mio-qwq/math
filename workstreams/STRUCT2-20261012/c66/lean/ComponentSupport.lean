import Std

/-!
Actual ordered TF equality closure and the component-endpoint transport used
by CRITICAL_BOUNDARY.md.  The probability estimates, excess sum and global
permutation count remain written results outside this formalization.
-/

set_option Elab.async false

namespace Struct2.C66.ComponentSupport

structure Perm (V : Type) where
  forward : V → V
  backward : V → V
  left_inv : ∀ x, backward (forward x) = x
  right_inv : ∀ x, forward (backward x) = x

def Endpoint {V : Type} (R : V → V → Prop) (x : V) : Prop := ∃ y, R x y

def TFInvariant {V : Type} (R : V → V → Prop) (a b : Perm V) : Prop :=
  ∀ x y, R (a.forward x) (b.forward y) ↔ R x y

theorem endpoint_transport {V : Type} (R : V → V → Prop) (a b : Perm V)
    (h : TFInvariant R a b) (x : V) :
    Endpoint R (a.forward x) ↔ Endpoint R x := by
  constructor
  · rintro ⟨y, hy⟩
    refine ⟨b.backward y, ?_⟩
    apply (h x (b.backward y)).mp
    simpa only [b.right_inv] using hy
  · rintro ⟨y, hy⟩
    exact ⟨b.forward y, (h x y).mpr hy⟩

theorem swapped_invariant {V : Type} (R : V → V → Prop) (a b : Perm V)
    (hs : ∀ x y, R x y ↔ R y x) (h : TFInvariant R a b) :
    TFInvariant R b a := by
  intro x y
  exact (hs _ _).trans ((h y x).trans (hs y x))

theorem second_endpoint_transport {V : Type} (R : V → V → Prop) (a b : Perm V)
    (hs : ∀ x y, R x y ↔ R y x) (h : TFInvariant R a b) (x : V) :
    Endpoint R (b.forward x) ↔ Endpoint R x :=
  endpoint_transport R b a (swapped_invariant R a b hs h) x

def iterate {V : Type} (a : Perm V) : Nat → V → V
  | 0, x => x
  | k + 1, x => a.forward (iterate a k x)

theorem iterates_in_endpoint {V : Type} (R : V → V → Prop) (a b : Perm V)
    (h : TFInvariant R a b) {x : V} (hx : Endpoint R x) (k : Nat) :
    Endpoint R (iterate a k x) := by
  induction k with
  | zero => exact hx
  | succ k ih => exact (endpoint_transport R a b h _).mpr ih

def edgeAdj {V : Type} (es : List (V × V)) (x y : V) : Prop :=
  (x, y) ∈ es ∨ (y, x) ∈ es

def endpoints {V : Type} (es : List (V × V)) : List V :=
  es.flatMap fun e => [e.1, e.2]

theorem endpoints_length {V : Type} (es : List (V × V)) :
    (endpoints es).length = 2 * es.length := by
  induction es with
  | nil => rfl
  | cons e es ih =>
    simp only [endpoints, List.flatMap_cons, List.length_append,
      List.length_cons, List.length_nil]
    change 2 + (endpoints es).length = 2 * (es.length + 1)
    rw [ih]
    omega

theorem edge_endpoint_mem {V : Type} (es : List (V × V)) {x : V}
    (h : Endpoint (edgeAdj es) x) : x ∈ endpoints es := by
  rcases h with ⟨y, h | h⟩
  · exact List.mem_flatMap.mpr ⟨(x, y), h, by simp⟩
  · exact List.mem_flatMap.mpr ⟨(y, x), h, by simp⟩

def orbitPrefix {V : Type} (a : Perm V) (x : V) (m : Nat) : List V :=
  (List.range m).map fun k => iterate a k x

theorem invariant_prefix_length_le_twice_edges {V : Type}
    (es : List (V × V)) (a b : Perm V)
    (h : TFInvariant (edgeAdj es) a b) {x : V}
    (hx : Endpoint (edgeAdj es) x) (m : Nat)
    (hd : (orbitPrefix a x m).Nodup) : m ≤ 2 * es.length := by
  have hsub : orbitPrefix a x m ⊆ endpoints es := by
    intro y hy
    rcases List.mem_map.mp hy with ⟨k, _, rfl⟩
    exact edge_endpoint_mem es (iterates_in_endpoint (edgeAdj es) a b h hx k)
  have hlen := hd.length_le_of_subset hsub
  simpa only [orbitPrefix, List.length_map, List.length_range, endpoints_length] using hlen

/- Each diagonal is the same ground.  Each off-diagonal variable is the
unordered pair of its two endpoints, represented by the increasing pair. -/
def edgeVariable {n : Nat} (i j : Fin n) : Option (Fin n × Fin n) :=
  if i = j then none else if i.val < j.val then some (i, j) else some (j, i)

theorem edgeVariable_diagonal {n : Nat} (i : Fin n) :
    edgeVariable i i = none := by simp [edgeVariable]

theorem edgeVariable_symmetric {n : Nat} (i j : Fin n) :
    edgeVariable i j = edgeVariable j i := by
  by_cases he : i = j
  · subst j; rfl
  · have hev : i.val ≠ j.val := by
      intro h
      exact he (Fin.ext h)
    have he' : j ≠ i := Ne.symm he
    by_cases hl : i.val < j.val
    · have hn : ¬j.val < i.val := by omega
      simp [edgeVariable, he, he', hl, hn]
    · have hr : j.val < i.val := by omega
      simp [edgeVariable, he, he', hl, hr]

inductive FullConnected {n : Nat} (a b : Perm (Fin n)) :
    Option (Fin n × Fin n) → Option (Fin n × Fin n) → Prop where
  | refl (v) : FullConnected a b v v
  | equation (i j : Fin n) :
      FullConnected a b (edgeVariable i j)
        (edgeVariable (a.forward i) (b.forward j))
  | symm {u v} : FullConnected a b u v → FullConnected a b v u
  | trans {u v w} : FullConnected a b u v → FullConnected a b v w →
      FullConnected a b u w

def componentAdj {n : Nat} (a b : Perm (Fin n))
    (c : Option (Fin n × Fin n)) (x y : Fin n) : Prop :=
  FullConnected a b c (edgeVariable x y)

theorem component_symmetric {n : Nat} (a b : Perm (Fin n))
    (c : Option (Fin n × Fin n)) (x y : Fin n) :
    componentAdj a b c x y ↔ componentAdj a b c y x := by
  unfold componentAdj
  rw [edgeVariable_symmetric x y]

theorem ungrounded_component_loopless {n : Nat} (a b : Perm (Fin n))
    (c : Option (Fin n × Fin n)) (hg : ¬FullConnected a b c none) (x : Fin n) :
    ¬componentAdj a b c x x := by
  simpa only [componentAdj, edgeVariable_diagonal] using hg

theorem full_component_invariant {n : Nat} (a b : Perm (Fin n))
    (c : Option (Fin n × Fin n)) : TFInvariant (componentAdj a b c) a b := by
  intro x y
  constructor
  · intro h
    exact .trans h (.symm (.equation x y))
  · intro h
    exact .trans h (.equation x y)

theorem full_component_endpoint_transport {n : Nat} (a b : Perm (Fin n))
    (c : Option (Fin n × Fin n)) (x : Fin n) :
    (Endpoint (componentAdj a b c) (a.forward x) ↔
      Endpoint (componentAdj a b c) x) ∧
    (Endpoint (componentAdj a b c) (b.forward x) ↔
      Endpoint (componentAdj a b c) x) := by
  exact ⟨endpoint_transport _ a b (full_component_invariant a b c) x,
    second_endpoint_transport _ a b (component_symmetric a b c)
      (full_component_invariant a b c) x⟩

/- The edge list is a complete enumeration of the actual component, supplied
as an adjacency equivalence, rather than a premise of support invariance.
A genuine m-cycle gives the Nodup orbitPrefix premise immediately. -/
theorem actual_component_cycle_prefix_bound {n : Nat} (a b : Perm (Fin n))
    (c : Option (Fin n × Fin n)) (es : List (Fin n × Fin n))
    (he : ∀ x y, componentAdj a b c x y ↔ edgeAdj es x y)
    {x : Fin n} (hx : Endpoint (componentAdj a b c) x) (m : Nat)
    (hd : (orbitPrefix a x m).Nodup) : m ≤ 2 * es.length := by
  have hi : TFInvariant (edgeAdj es) a b := by
    intro u v
    exact (he _ _).symm.trans ((full_component_invariant a b c u v).trans (he u v))
  have hx' : Endpoint (edgeAdj es) x := by
    rcases hx with ⟨y, hy⟩
    exact ⟨y, (he x y).mp hy⟩
  exact invariant_prefix_length_le_twice_edges es a b hi hx' m hd

noncomputable def componentEdges {n : Nat} (a b : Perm (Fin n))
    (c : Option (Fin n × Fin n)) : List (Fin n × Fin n) := by
  classical
  exact ((List.finRange n).flatMap fun i => (List.finRange n).map fun j => (i, j)).filter
    fun e => decide (e.1.val < e.2.val ∧ componentAdj a b c e.1 e.2)

theorem mem_componentEdges {n : Nat} (a b : Perm (Fin n))
    (c : Option (Fin n × Fin n)) (x y : Fin n) :
    (x, y) ∈ componentEdges a b c ↔ x.val < y.val ∧ componentAdj a b c x y := by
  classical
  simp [componentEdges, List.mem_flatMap, List.mem_map, List.mem_finRange]

theorem componentEdges_adjacency {n : Nat} (a b : Perm (Fin n))
    (c : Option (Fin n × Fin n)) (hg : ¬FullConnected a b c none)
    (x y : Fin n) : edgeAdj (componentEdges a b c) x y ↔ componentAdj a b c x y := by
  change ((x, y) ∈ componentEdges a b c ∨ (y, x) ∈ componentEdges a b c) ↔ _
  rw [mem_componentEdges, mem_componentEdges]
  constructor
  · rintro (⟨_, h⟩ | ⟨_, h⟩)
    · exact h
    · exact (component_symmetric a b c x y).mpr h
  · intro h
    by_cases hl : x.val < y.val
    · exact Or.inl ⟨hl, h⟩
    · have hne : x.val ≠ y.val := by
        intro he
        have he' : x = y := Fin.ext he
        subst y
        exact ungrounded_component_loopless a b c hg x h
      exact Or.inr ⟨by omega, (component_symmetric a b c x y).mp h⟩

theorem canonical_component_cycle_prefix_bound {n : Nat} (a b : Perm (Fin n))
    (c : Option (Fin n × Fin n)) (hg : ¬FullConnected a b c none)
    {x : Fin n} (hx : Endpoint (componentAdj a b c) x) (m : Nat)
    (hd : (orbitPrefix a x m).Nodup) : m ≤ 2 * (componentEdges a b c).length := by
  exact actual_component_cycle_prefix_bound a b c (componentEdges a b c)
    (fun u v => (componentEdges_adjacency a b c hg u v).symm) hx m hd

#print axioms endpoint_transport
#print axioms second_endpoint_transport
#print axioms iterates_in_endpoint
#print axioms invariant_prefix_length_le_twice_edges
#print axioms edgeVariable_symmetric
#print axioms ungrounded_component_loopless
#print axioms full_component_invariant
#print axioms full_component_endpoint_transport
#print axioms actual_component_cycle_prefix_bound
#print axioms mem_componentEdges
#print axioms componentEdges_adjacency
#print axioms canonical_component_cycle_prefix_bound

end Struct2.C66.ComponentSupport
