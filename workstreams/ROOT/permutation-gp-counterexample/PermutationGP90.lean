import Mathlib.Data.Fintype.Prod
import Mathlib.Data.Fintype.Card
import Mathlib.Data.Fintype.Fin
import Lean.Elab.Tactic.Omega

/- Actual Pe(6,3) digraph and a 90-point counterexample.
   Vertices are injective words of length three over nine letters.
   Walks use only the actual shift-and-fresh-letter arc relation.
   The 90-point construction was supplied by the independent B discoverer;
   this file develops its actual-graph proof, rather than asserting gp = 90.
   Source: arXiv:2604.15909v1, Definition 2.1 and Section 3.3. -/
namespace PermutationGP90

abbrev Letter := Fin 9
abbrev Triple := Letter × Letter × Letter

def Distinct (x : Triple) : Prop :=
  x.1 ≠ x.2.1 ∧ x.1 ≠ x.2.2 ∧ x.2.1 ≠ x.2.2

instance (x : Triple) : Decidable (Distinct x) := by
  unfold Distinct
  infer_instance

abbrev Vertex := {x : Triple // Distinct x}

def first (u : Vertex) : Letter := u.1.1
def second (u : Vertex) : Letter := u.1.2.1
def third (u : Vertex) : Letter := u.1.2.2

def Edge (u v : Vertex) : Prop :=
  first v = second u ∧ second v = third u ∧
  third v ≠ first u ∧ third v ≠ second u ∧ third v ≠ third u

inductive Walk : ℕ → Vertex → Vertex → Prop
  | nil (u : Vertex) : Walk 0 u u
  | cons {n : ℕ} {u v w : Vertex} :
      Edge u v → Walk n v w → Walk (n + 1) u w

def Selected (u : Vertex) : Prop :=
  3 ≤ (first u).val ∧ 3 ≤ (second u).val ∧ (third u).val < 3

instance (u : Vertex) : Decidable (Selected u) := by
  unfold Selected
  infer_instance

def selected : Finset Vertex := Finset.univ.filter Selected

theorem mem_selected (u : Vertex) : u ∈ selected ↔ Selected u := by
  simp [selected]

theorem selected_card : selected.card = 90 := by decide

theorem first_ne_second (u : Vertex) : first u ≠ second u := u.2.1

theorem first_ne_third (u : Vertex) : first u ≠ third u := u.2.2.1

theorem second_ne_third (u : Vertex) : second u ≠ third u := u.2.2.2

def make (a b c : Letter) (hab : a ≠ b) (hac : a ≠ c) (hbc : b ≠ c) : Vertex :=
  ⟨(a, b, c), hab, hac, hbc⟩

def back : Finset Letter := Finset.univ.filter (fun a => 3 ≤ a.val)

theorem back_card : back.card = 6 := by decide

def Fresh (u v : Vertex) (a : Letter) : Prop :=
  a ≠ first u ∧ a ≠ second u ∧ a ≠ first v ∧ a ≠ second v

/-- Six back letters minus at most four forbidden letters contain two distinct choices. -/
theorem two_fresh (u v : Vertex) :
    ∃ p q : Letter, 3 ≤ p.val ∧ 3 ≤ q.val ∧
      Fresh u v p ∧ Fresh u v q ∧ p ≠ q := by
  let forbidden : Finset Letter := {first u, second u, first v, second v}
  have hf : forbidden.card ≤ 4 := Finset.card_le_four
  have hfb : forbidden.card < back.card := by
    rw [back_card]
    omega
  obtain ⟨p, hp, hpf⟩ := Finset.exists_mem_notMem_of_card_lt_card hfb
  let forbiddenP : Finset Letter := insert p forbidden
  have hfp : forbiddenP.card ≤ 5 := by
    have h := Finset.card_insert_le p forbidden
    dsimp [forbiddenP]
    omega
  have hfpb : forbiddenP.card < back.card := by
    rw [back_card]
    omega
  obtain ⟨q, hq, hqf⟩ := Finset.exists_mem_notMem_of_card_lt_card hfpb
  have hpback : 3 ≤ p.val := by simpa [back] using hp
  have hqback : 3 ≤ q.val := by simpa [back] using hq
  have hpfresh : Fresh u v p := by simpa [forbidden, Fresh] using hpf
  have hqfresh : q ≠ p ∧ Fresh u v q := by
    simpa [forbiddenP, forbidden, Fresh] using hqf
  exact ⟨p, q, hpback, hqback, hpfresh, hqfresh.2, hqfresh.1.symm⟩

theorem no_edge_selected {u v : Vertex} (hu : Selected u) (hv : Selected v) :
    ¬ Edge u v := by
  intro he
  have h := congrArg Fin.val he.2.1
  have huTail := hu.2.2
  have hvSecond := hv.2.1
  omega

theorem no_two_edges_selected {u v w : Vertex}
    (hu : Selected u) (hv : Selected v) :
    ¬ (Edge u w ∧ Edge w v) := by
  rintro ⟨he₁, he₂⟩
  have h₁ := congrArg Fin.val he₁.2.1
  have h₂ := congrArg Fin.val he₂.1
  have huTail := hu.2.2
  have hvFirst := hv.1
  omega

/-- Every walk between two different selected vertices has length at least three. -/
theorem walk_length_at_least_three {n : ℕ} {u v : Vertex}
    (hu : Selected u) (hv : Selected v) (hne : u ≠ v)
    (h : Walk n u v) : 3 ≤ n := by
  cases n with
  | zero =>
      cases h
      exact (hne rfl).elim
  | succ n =>
      cases n with
      | zero =>
          cases h with
          | cons he hrest =>
              cases hrest
              exact (no_edge_selected hu hv he).elim
      | succ n =>
          cases n with
          | zero =>
              cases h with
              | cons he₁ hrest =>
                  cases hrest with
                  | cons he₂ hlast =>
                      cases hlast
                      exact (no_two_edges_selected hu hv ⟨he₁, he₂⟩).elim
          | succ n => omega

/-- Append the two fresh letters and then the target word: a,b,t,p,q,c,e,s. -/
theorem five_walk {u v : Vertex} (hu : Selected u) (hv : Selected v) :
    Walk 5 u v := by
  obtain ⟨p, q, hpback, hqback, hpf, hqf, hpq⟩ := two_fresh u v
  have huTail := hu.2.2
  have hvTail := hv.2.2
  have hvFirst := hv.1
  have hpt : p ≠ third u := by
    intro h
    have he := congrArg Fin.val h
    omega
  have hqt : q ≠ third u := by
    intro h
    have he := congrArg Fin.val h
    omega
  have hct : first v ≠ third u := by
    intro h
    have he := congrArg Fin.val h
    omega
  have hsq : third v ≠ q := by
    intro h
    have he := congrArg Fin.val h
    omega
  let w₁ : Vertex := make (second u) (third u) p
    (second_ne_third u) hpf.2.1.symm hpt.symm
  let w₂ : Vertex := make (third u) p q hpt.symm hqt.symm hpq
  let w₃ : Vertex := make p q (first v) hpq hpf.2.2.1 hqf.2.2.1
  let w₄ : Vertex := make q (first v) (second v)
    hqf.2.2.1 hqf.2.2.2 (first_ne_second v)
  have he₁ : Edge u w₁ := by
    exact ⟨rfl, rfl, hpf.1, hpf.2.1, hpt⟩
  have he₂ : Edge w₁ w₂ := by
    exact ⟨rfl, rfl, hqf.2.1, hqt, hpq.symm⟩
  have he₃ : Edge w₂ w₃ := by
    exact ⟨rfl, rfl, hct, hpf.2.2.1.symm, hqf.2.2.1.symm⟩
  have he₄ : Edge w₃ w₄ := by
    exact ⟨rfl, rfl, hpf.2.2.2.symm, hqf.2.2.2.symm, (first_ne_second v).symm⟩
  have he₅ : Edge w₄ v := by
    exact ⟨rfl, rfl, hsq, (first_ne_third v).symm, (second_ne_third v).symm⟩
  exact Walk.cons he₁ (Walk.cons he₂ (Walk.cons he₃
    (Walk.cons he₄ (Walk.cons he₅ (Walk.nil v)))))

/-- Actual-arc formulation: every walk through a different third selected
vertex admits a shorter walk between its endpoints. Shortest walks are paths,
since deleting any repeated-vertex segment strictly shortens a walk. -/
def GeneralPosition (S : Finset Vertex) : Prop :=
  ∀ {u v w : Vertex}, u ∈ S → v ∈ S → w ∈ S → w ≠ u → w ≠ v →
    ∀ {m n : ℕ}, Walk m u w → Walk n w v →
      ∃ k : ℕ, Walk k u v ∧ k < m + n

theorem selected_general_position : GeneralPosition selected := by
  intro u v w hu hv hw hwu hwv m n huw hwvWalk
  have huS : Selected u := (mem_selected u).mp hu
  have hvS : Selected v := (mem_selected v).mp hv
  have hwS : Selected w := (mem_selected w).mp hw
  have hm : 3 ≤ m := walk_length_at_least_three huS hwS hwu.symm huw
  have hn : 3 ≤ n := walk_length_at_least_three hwS hvS hwv hwvWalk
  exact ⟨5, five_walk huS hvS, by omega⟩

/-- Equivalent exclusion of a shortest walk passing through the third point.
The split walks are quantified over the actual arc relation, with no assumption
that their concatenation was originally chosen as shortest. -/
def NoShortestThrough (S : Finset Vertex) : Prop :=
  ∀ {u v w : Vertex}, u ∈ S → v ∈ S → w ∈ S → w ≠ u → w ≠ v →
    ∀ {m n : ℕ}, Walk m u w → Walk n w v →
      ¬ (∀ k : ℕ, Walk k u v → m + n ≤ k)

theorem general_position_iff_no_shortest_through (S : Finset Vertex) :
    GeneralPosition S ↔ NoShortestThrough S := by
  classical
  constructor
  · intro h u v w hu hv hw hwu hwv m n huw hwvWalk hmin
    obtain ⟨k, hk, hlt⟩ := h hu hv hw hwu hwv huw hwvWalk
    have hle := hmin k hk
    omega
  · intro h u v w hu hv hw hwu hwv m n huw hwvWalk
    by_contra hshort
    apply h hu hv hw hwu hwv huw hwvWalk
    intro k hk
    by_contra hle
    have hlt : k < m + n := by omega
    exact hshort ⟨k, hk, hlt⟩

theorem selected_no_shortest_through : NoShortestThrough selected :=
  (general_position_iff_no_shortest_through selected).mp selected_general_position

/-- The proposed exact value at d = 6, k = 3 is 2 * 6 * 7 = 84. -/
theorem permutation_counterexample :
    GeneralPosition selected ∧ selected.card = 90 ∧ 2 * 6 * (6 + 1) < selected.card := by
  refine ⟨selected_general_position, selected_card, ?_⟩
  rw [selected_card]
  decide

theorem not_conjectured_upper_bound :
    ¬ (∀ S : Finset Vertex, GeneralPosition S → S.card ≤ 2 * 6 * (6 + 1)) := by
  intro h
  have hbound := h selected selected_general_position
  rw [selected_card] at hbound
  omega

#print axioms selected_card
#print axioms two_fresh
#print axioms walk_length_at_least_three
#print axioms five_walk
#print axioms selected_general_position
#print axioms general_position_iff_no_shortest_through
#print axioms selected_no_shortest_through
#print axioms permutation_counterexample
#print axioms not_conjectured_upper_bound


inductive SimplePath : ℕ → Vertex → Vertex → List Vertex → Prop
  | nil (u : Vertex) : SimplePath 0 u u [u]
  | cons {n : ℕ} {u v w : Vertex} {l : List Vertex} :
      Edge u v → SimplePath n v w l → u ∉ l →
        SimplePath (n + 1) u w (u :: l)

theorem SimplePath.toWalk {n : ℕ} {u v : Vertex} {l : List Vertex}
    (h : SimplePath n u v l) : Walk n u v := by
  induction h with
  | nil u => exact Walk.nil u
  | cons he hp hnot ih => exact Walk.cons he ih

theorem SimplePath.supportNodup {n : ℕ} {u v : Vertex} {l : List Vertex}
    (h : SimplePath n u v l) : l.Nodup := by
  induction h with
  | nil u => simp
  | cons he hp hnot ih => exact List.nodup_cons.mpr ⟨hnot, ih⟩

/-- If a vertex lies on a simple path, retain its suffix to the same endpoint. -/
theorem SimplePath.suffix {n : ℕ} {v w : Vertex} {l : List Vertex}
    (h : SimplePath n v w l) {u : Vertex} (hu : u ∈ l) :
    ∃ k : ℕ, ∃ l' : List Vertex, SimplePath k u w l' ∧ k ≤ n := by
  induction h generalizing u with
  | nil v =>
      have heq : u = v := by simpa using hu
      subst u
      exact ⟨0, [v], SimplePath.nil v, Nat.le_refl 0⟩
  | @cons n v z w l he hp hnot ih =>
      rcases List.mem_cons.mp hu with heq | hmem
      · subst u
        exact ⟨n + 1, v :: l, SimplePath.cons he hp hnot, Nat.le_refl (n + 1)⟩
      · obtain ⟨k, l', hk, hkn⟩ := ih hmem
        exact ⟨k, l', hk, by omega⟩

/-- Delete loops constructively: every actual walk has a no-longer simple path
with the same ordered endpoints. No graph-distance or reachability assumptions. -/
theorem walk_to_simple_path {n : ℕ} {u v : Vertex} (h : Walk n u v) :
    ∃ k : ℕ, ∃ l : List Vertex, SimplePath k u v l ∧ k ≤ n := by
  induction h with
  | nil u => exact ⟨0, [u], SimplePath.nil u, Nat.le_refl 0⟩
  | @cons n u v w he hw ih =>
      obtain ⟨k, l, hp, hkn⟩ := ih
      by_cases hu : u ∈ l
      · obtain ⟨j, l', hj, hjk⟩ := hp.suffix hu
        exact ⟨j, l', hj, by omega⟩
      · exact ⟨k + 1, u :: l, SimplePath.cons he hp hu, by omega⟩

/-- Path-segment formulation: no pair of path segments through a
different third selected vertex can have a total length minimal among all
simple paths between the ordered endpoints. A geodesic through the third
vertex would give exactly such a pair by splitting its vertex sequence. -/
def PathGeneralPosition (S : Finset Vertex) : Prop :=
  ∀ {u v w : Vertex}, u ∈ S → v ∈ S → w ∈ S → w ≠ u → w ≠ v →
    ∀ {m n : ℕ} {l₁ l₂ : List Vertex},
      SimplePath m u w l₁ → SimplePath n w v l₂ →
        ¬ (∀ k : ℕ, ∀ l : List Vertex, SimplePath k u v l → m + n ≤ k)

theorem selected_path_general_position : PathGeneralPosition selected := by
  intro u v w hu hv hw hwu hwv m n l₁ l₂ hp₁ hp₂ hmin
  apply selected_no_shortest_through hu hv hw hwu hwv hp₁.toWalk hp₂.toWalk
  intro k hk
  obtain ⟨j, l, hj, hjk⟩ := walk_to_simple_path hk
  exact Nat.le_trans (hmin j l hj) hjk

/-- A 90-point path-segment GP set exceeds the conjectured 84 at (d,k)=(6,3).
This is a witness lower bound, not an assertion of the exact GP number. -/
theorem permutation_path_counterexample :
    PathGeneralPosition selected ∧ selected.card = 90 ∧
      2 * 6 * (6 + 1) < selected.card := by
  refine ⟨selected_path_general_position, selected_card, ?_⟩
  rw [selected_card]
  decide

/-- Split an actual simple path at any support vertex, preserving the exact
total length. The two pieces need only be walks for the length lower bound. -/
theorem SimplePath.split_walk {n : ℕ} {u v : Vertex} {l : List Vertex}
    (hp : SimplePath n u v l) {w : Vertex} (hw : w ∈ l) :
    ∃ m k : ℕ, Walk m u w ∧ Walk k w v ∧ m + k = n := by
  induction hp generalizing w with
  | nil u =>
      have heq : w = u := by simpa using hw
      subst w
      exact ⟨0, 0, Walk.nil u, Walk.nil u, rfl⟩
  | @cons n u z v l he hp hnot ih =>
      rcases List.mem_cons.mp hw with heq | hmem
      · subst w
        exact ⟨0, n + 1, Walk.nil u, Walk.cons he hp.toWalk, by omega⟩
      · obtain ⟨m, k, hm, hk, hmk⟩ := ih hmem
        exact ⟨m + 1, k, Walk.cons he hm, hk, by omega⟩

/-- Definition 2.1 in single-path form: on every shortest actual directed
simple path between two selected vertices, every selected support vertex is
one of the ordered endpoints. No unformalized splitting or loop deletion is
used to connect this statement to the 90-point construction. -/
def OriginalGeneralPosition (S : Finset Vertex) : Prop :=
  ∀ {n : ℕ} {u v : Vertex} {l : List Vertex},
    SimplePath n u v l → u ∈ S → v ∈ S →
      (∀ k : ℕ, ∀ l' : List Vertex, SimplePath k u v l' → n ≤ k) →
        ∀ {w : Vertex}, w ∈ l → w ∈ S → w = u ∨ w = v

theorem selected_original_general_position : OriginalGeneralPosition selected := by
  intro n u v l hp hu hv hmin w hw hwS
  by_cases hwu : w = u
  · exact Or.inl hwu
  by_cases hwv : w = v
  · exact Or.inr hwv
  obtain ⟨m, k, hm, hk, hmk⟩ := hp.split_walk hw
  have huSelected : Selected u := (mem_selected u).mp hu
  have hvSelected : Selected v := (mem_selected v).mp hv
  have hwSelected : Selected w := (mem_selected w).mp hwS
  have hmLower : 3 ≤ m :=
    walk_length_at_least_three huSelected hwSelected (fun h => hwu h.symm) hm
  have hkLower : 3 ≤ k :=
    walk_length_at_least_three hwSelected hvSelected hwv hk
  obtain ⟨j, l', hj, hj5⟩ := walk_to_simple_path (five_walk huSelected hvSelected)
  have hnj : n ≤ j := hmin j l' hj
  omega

/-- The original single-shortest-path property, the exact witness size, and
the strict comparison with the conjectured value 84. -/
theorem permutation_original_counterexample :
    OriginalGeneralPosition selected ∧ selected.card = 90 ∧
      2 * 6 * (6 + 1) < selected.card := by
  refine ⟨selected_original_general_position, selected_card, ?_⟩
  rw [selected_card]
  decide

theorem not_original_conjectured_upper_bound :
    ¬ (∀ S : Finset Vertex, OriginalGeneralPosition S → S.card ≤ 2 * 6 * (6 + 1)) := by
  intro h
  have hbound := h selected selected_original_general_position
  rw [selected_card] at hbound
  omega

#print axioms SimplePath.toWalk
#print axioms SimplePath.supportNodup
#print axioms walk_to_simple_path
#print axioms selected_path_general_position
#print axioms permutation_path_counterexample
#print axioms SimplePath.split_walk
#print axioms selected_original_general_position
#print axioms permutation_original_counterexample
#print axioms not_original_conjectured_upper_bound

end PermutationGP90
