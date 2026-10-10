import Mathlib.Combinatorics.SimpleGraph.Diam
import Mathlib.Combinatorics.SimpleGraph.Paths
import Mathlib.Combinatorics.SimpleGraph.Walk.Chord
import Mathlib.Data.Fin.VecNotation
import Mathlib.Data.Nat.Find
import Mathlib.Tactic.FinCases
import Lean.Elab.Tactic.Omega

/-!
A complete order-15 exclusion refutes the original Conjecture 4.5.
Actual compilation and original-definition review are recorded with this file.

The original monophonic condition below quantifies over every actual mathlib
simple chordless walk.  No shortest-path replacement or bound on its length
is made.  The only finite classification concerns the 128 inverse-pair
connection choices on the cyclic group of order 15.
-/

namespace MonophonicCirculant15

open SimpleGraph

variable {V : Type*} {G : SimpleGraph V}

/-- The original condition: no induced simple path has three selected vertices.
Indices are ordered to count distinct vertices of the simple path. -/
def MonophonicPosition (G : SimpleGraph V) (S : Set V) : Prop :=
  ∀ ⦃u v : V⦄ (p : G.Walk u v), p.IsPath → p.IsChordless →
    ∀ i j k : ℕ, i < j → j < k → k ≤ p.length →
      p.getVert i ∈ S → p.getVert j ∈ S → p.getVert k ∈ S → False

/-- The same original definition stated literally using distinct vertices
contained in the support of an arbitrary induced simple path. -/
def OriginalMonophonicPosition (G : SimpleGraph V) (S : Set V) : Prop :=
  ∀ ⦃u v : V⦄ (p : G.Walk u v), p.IsPath → p.IsChordless →
    ∀ a b c, a ≠ b → a ≠ c → b ≠ c → a ∈ S → b ∈ S → c ∈ S →
      a ∈ p.support → b ∈ p.support → c ∈ p.support → False

theorem monophonicPosition_iff_original (S : Set V) :
    MonophonicPosition G S ↔ OriginalMonophonicPosition G S := by
  constructor
  · intro h u v p hp hc a b c hab hac hbc ha hb hcS haP hbP hcP
    obtain ⟨i, rfl, hi⟩ := SimpleGraph.Walk.mem_support_iff_exists_getVert.mp haP
    obtain ⟨j, rfl, hj⟩ := SimpleGraph.Walk.mem_support_iff_exists_getVert.mp hbP
    obtain ⟨k, rfl, hk⟩ := SimpleGraph.Walk.mem_support_iff_exists_getVert.mp hcP
    have hijne : i ≠ j := fun he => hab (congrArg p.getVert he)
    have hikne : i ≠ k := fun he => hac (congrArg p.getVert he)
    have hjkne : j ≠ k := fun he => hbc (congrArg p.getVert he)
    by_cases hij : i < j <;> by_cases hjk : j < k <;> by_cases hik : i < k
    · exact h p hp hc i j k hij hjk hk ha hb hcS
    · omega
    · exact h p hp hc i k j hik (by omega) hj ha hcS hb
    · exact h p hp hc k i j (by omega) hij hj hcS ha hb
    · exact h p hp hc j i k (by omega) hik hk hb ha hcS
    · exact h p hp hc j k i hjk (by omega) hi hb hcS ha
    · omega
    · exact h p hp hc k j i (by omega) (by omega) hi hcS hb ha
  · intro h u v p hp hc i j k hij hjk hk ha hb hcS
    have hi : i ≤ p.length := by omega
    have hj : j ≤ p.length := by omega
    have hab : p.getVert i ≠ p.getVert j := by
      intro he
      have := hp.getVert_injOn hi hj he
      omega
    have hac : p.getVert i ≠ p.getVert k := by
      intro he
      have := hp.getVert_injOn hi hk he
      omega
    have hbc : p.getVert j ≠ p.getVert k := by
      intro he
      have := hp.getVert_injOn hj hk he
      omega
    exact h p hp hc _ _ _ hab hac hbc ha hb hcS
      (p.getVert_mem_support i) (p.getVert_mem_support j) (p.getVert_mem_support k)

/-- Maximum cardinality of an actual monophonic position set. -/
noncomputable def mpNumber [Fintype V] (G : SimpleGraph V) : ℕ := by
  classical
  exact Nat.findGreatest
    (fun k => ∃ S : Finset V, S.card = k ∧ MonophonicPosition G (S : Set V))
    (Fintype.card V)

theorem card_le_mpNumber [Fintype V] (S : Finset V)
    (hS : MonophonicPosition G (S : Set V)) : S.card ≤ mpNumber G := by
  classical
  exact Nat.le_findGreatest (Finset.card_le_univ S) ⟨S, rfl, hS⟩

theorem mpNumber_attained [Fintype V] (G : SimpleGraph V) :
    ∃ S : Finset V, S.card = mpNumber G ∧
      OriginalMonophonicPosition G (S : Set V) := by
  classical
  have hzero : ∃ S : Finset V, S.card = 0 ∧ MonophonicPosition G (S : Set V) := by
    exact ⟨∅, rfl, by simp [MonophonicPosition]⟩
  obtain ⟨S, hcard, hS⟩ := Nat.findGreatest_spec
    (P := fun k => ∃ S : Finset V, S.card = k ∧ MonophonicPosition G (S : Set V))
    (m := 0) (n := Fintype.card V) (Nat.zero_le _) hzero
  exact ⟨S, hcard, (monophonicPosition_iff_original _).mp hS⟩

/-- In a simple chordless walk, adjacent vertices occur at consecutive indices. -/
theorem chordless_adj_indices {u v : V} (p : G.Walk u v)
    (hp : p.IsPath) (hc : p.IsChordless) {i j : ℕ}
    (hi : i ≤ p.length) (hj : j ≤ p.length)
    (hadj : G.Adj (p.getVert i) (p.getVert j)) :
    i + 1 = j ∨ j + 1 = i := by
  have he := hc.mem_edges (p.getVert_mem_support i) (p.getVert_mem_support j) hadj
  obtain ⟨t, ht, heq⟩ := (p.mk_mem_edges_iff_exists).mp he
  rcases Sym2.eq_iff.mp heq with ⟨hti, htj⟩ | ⟨htj, hti⟩
  · have hti' : t = i := hp.getVert_injOn (show t ≤ p.length by omega) hi hti
    have htj' : t + 1 = j := hp.getVert_injOn (show t + 1 ≤ p.length by omega) hj htj
    omega
  · have htj' : t = j := hp.getVert_injOn (show t ≤ p.length by omega) hj htj
    have hti' : t + 1 = i := hp.getVert_injOn (show t + 1 ≤ p.length by omega) hi hti
    omega

theorem monophonic_of_pairwise_adj (S : Set V)
    (hS : ∀ x ∈ S, ∀ y ∈ S, x ≠ y → G.Adj x y) :
    MonophonicPosition G S := by
  intro u v p hp hc i j k hij hjk hk hiS _hjS hkS
  have hi : i ≤ p.length := by omega
  have hj : j ≤ p.length := by omega
  have hik : p.getVert i ≠ p.getVert k := by
    intro he
    have := hp.getVert_injOn hi hk he
    omega
  have h := chordless_adj_indices p hp hc hi hk
    (hS _ hiS _ hkS hik)
  omega

/-- An entire open-twin class is monophonic.  The proof uses the predecessor
of the middle selected vertex, so it applies to induced paths of every length. -/
theorem monophonic_of_open_twins (S : Set V)
    (hS : ∀ x ∈ S, ∀ y ∈ S, ∀ w, G.Adj x w ↔ G.Adj y w) :
    MonophonicPosition G S := by
  intro u v p hp hc i j k hij hjk hk _hiS hjS hkS
  have hprev : j - 1 < p.length := by omega
  have hstep : j - 1 + 1 = j := by omega
  have he : G.Adj (p.getVert j) (p.getVert (j - 1)) := by
    simpa only [hstep] using (p.adj_getVert_succ hprev).symm
  have he' := (hS _ hjS _ hkS (p.getVert (j - 1))).mp he
  have h := chordless_adj_indices p hp hc (by omega) hk he'.symm
  omega

theorem triangle_monophonic {a b c : V}
    (hab : G.Adj a b) (hbc : G.Adj b c) (hca : G.Adj c a) :
    MonophonicPosition G ({a, b, c} : Set V) := by
  apply monophonic_of_pairwise_adj
  intro x hx y hy hxy
  simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hx hy
  rcases hx with rfl | rfl | rfl <;>
    rcases hy with rfl | rfl | rfl <;>
    first | exact hab | exact hab.symm | exact hbc | exact hbc.symm |
      exact hca | exact hca.symm | exact False.elim (hxy rfl)

theorem twins_monophonic {a b c : V}
    (hab : ∀ w, G.Adj a w ↔ G.Adj b w)
    (hac : ∀ w, G.Adj a w ↔ G.Adj c w) :
    MonophonicPosition G ({a, b, c} : Set V) := by
  apply monophonic_of_open_twins
  intro x hx y hy w
  simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hx hy
  rcases hx with rfl | rfl | rfl <;>
    rcases hy with rfl | rfl | rfl <;>
    first | exact Iff.rfl | exact hab w | exact (hab w).symm |
      exact hac w | exact (hac w).symm |
      exact (hab w).symm.trans (hac w) |
      exact (hac w).symm.trans (hab w)

theorem three_le_mpNumber_of_triple [Fintype V] {a b c : V}
    (hab : a ≠ b) (hac : a ≠ c) (hbc : b ≠ c)
    (hS : MonophonicPosition G ({a, b, c} : Set V)) : 3 ≤ mpNumber G := by
  classical
  have hs : ({a, b, c} : Finset V).card = 3 := by simp [hab, hac, hbc]
  have h := card_le_mpNumber (G := G) ({a, b, c} : Finset V) (by simpa using hS)
  simpa only [hs] using h

/-- Seven independent bits choose the inverse pairs ±1,...,±7. -/
abbrev Choices := Fin 7 → Bool

/-- A symmetric, loopless Cayley adjacency, using representatives 0,...,14. -/
def cyclicAdj (P : Choices) (u v : Fin 15) : Prop :=
  u ≠ v ∧ ∃ k : Fin 7, P k = true ∧
    ((u.val + k.val + 1) % 15 = v.val ∨
      (v.val + k.val + 1) % 15 = u.val)

instance (P : Choices) : DecidableRel (cyclicAdj P) := fun _ _ => by
  unfold cyclicAdj
  infer_instance

def circulant (P : Choices) : SimpleGraph (Fin 15) where
  Adj := cyclicAdj P
  symm := by
    constructor
    intro u v h
    rcases h with ⟨hne, k, hk, h⟩
    exact ⟨hne.symm, k, hk, h.symm⟩
  loopless := by constructor; intro u h; exact h.1 rfl

instance (P : Choices) : DecidableRel (circulant P).Adj :=
  inferInstanceAs (DecidableRel (cyclicAdj P))

def ReachTwo (G : SimpleGraph V) (u v : V) : Prop :=
  u = v ∨ G.Adj u v ∨ ∃ w, G.Adj u w ∧ G.Adj w v

def FiniteObstruction (P : Choices) : Prop :=
  (∃ a b : Fin 15, (circulant P).Adj 0 a ∧
      (circulant P).Adj a b ∧ (circulant P).Adj b 0) ∨
  (∃ v : Fin 15, ¬ ReachTwo (circulant P) 0 v) ∨
  ((∀ w : Fin 15, (circulant P).Adj 0 w ↔ (circulant P).Adj 5 w) ∧
    (∀ w : Fin 15, (circulant P).Adj 0 w ↔ (circulant P).Adj 10 w))

instance (P : Choices) : Decidable (FiniteObstruction P) := by
  unfold FiniteObstruction ReachTwo
  infer_instance

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
/-- Exactly 2^7 choices.  Kernel reduction only: no compiled/native oracle.
This deliberately checks only local structural certificates, never paths. -/
theorem finite_classification :
    ∀ b0 b1 b2 b3 b4 b5 b6 : Bool,
      FiniteObstruction ![b0, b1, b2, b3, b4, b5, b6] := by
  decide

theorem all_choices_classified (P : Choices) : FiniteObstruction P := by
  have hP : P = ![P 0, P 1, P 2, P 3, P 4, P 5, P 6] := by
    funext k
    fin_cases k <;> rfl
  rw [hP]
  exact finite_classification _ _ _ _ _ _ _

/-- The bridge uses genuine extended graph distance, and includes unreachable pairs. -/
theorem reachTwo_of_edist_le_two {u v : V} (h : G.edist u v ≤ 2) :
    ReachTwo G u v := by
  classical
  by_cases huv : u = v
  · exact Or.inl huv
  by_cases hadj : G.Adj u v
  · exact Or.inr (Or.inl hadj)
  have hn : (G.commonNeighbors u v).Nonempty := by
    by_contra hnon
    have hemp : G.commonNeighbors u v = ∅ := Set.not_nonempty_iff_eq_empty.mp hnon
    have hlt := (SimpleGraph.two_lt_edist_iff (G := G)).mpr ⟨huv, hadj, hemp⟩
    exact (not_lt_of_ge h) hlt
  obtain ⟨w, hw⟩ := hn
  rw [G.mem_commonNeighbors] at hw
  exact Or.inr (Or.inr ⟨w, hw.1, hw.2.symm⟩)

theorem three_le_mpNumber_of_diameter (P : Choices)
    (hdiam : (circulant P).ediam ≤ 2) : 3 ≤ mpNumber (circulant P) := by
  rcases all_choices_classified P with htri | hfar | htw
  · obtain ⟨a, b, h0a, hab, hb0⟩ := htri
    exact three_le_mpNumber_of_triple h0a.ne hb0.ne.symm hab.ne
      (triangle_monophonic h0a hab hb0)
  · obtain ⟨v, hv⟩ := hfar
    exact False.elim (hv (reachTwo_of_edist_le_two
      ((SimpleGraph.edist_le_ediam (G := circulant P)).trans hdiam)))
  · exact three_le_mpNumber_of_triple (by decide : (0 : Fin 15) ≠ 5)
      (by decide : (0 : Fin 15) ≠ 10) (by decide : (5 : Fin 15) ≠ 10)
      (twins_monophonic htw.1 htw.2)

theorem no_labeled_counterexample (P : Choices) :
    ¬ ((circulant P).ediam = 2 ∧ mpNumber (circulant P) = 2) := by
  rintro ⟨hd, hm⟩
  have := three_le_mpNumber_of_diameter P hd.le
  omega

/-- Standard circulant presentation, permitting arbitrary original vertex labels.
Inverse-closed nonzero connections are encoded by their seven inverse pairs. -/
def IsCirculant15 (G : SimpleGraph V) : Prop :=
  ∃ P : Choices, Nonempty ((circulant P) ≃g G)

theorem iso_reachTwo {W : Type*} {H : SimpleGraph W} (e : G ≃g H)
    {u v : V} (h : ReachTwo H (e u) (e v)) : ReachTwo G u v := by
  rcases h with h | h | ⟨w, huw, hwv⟩
  · exact Or.inl (e.injective h)
  · exact Or.inr (Or.inl (e.map_adj_iff.mp h))
  · exact Or.inr (Or.inr ⟨e.symm w,
      e.map_adj_iff.mp (by simpa using huw),
      e.map_adj_iff.mp (by simpa using hwv)⟩)

theorem three_le_mpNumber_of_circulant15 [Fintype V]
    (hG : IsCirculant15 G) (hd : G.ediam ≤ 2) : 3 ≤ mpNumber G := by
  obtain ⟨P, ⟨e⟩⟩ := hG
  rcases all_choices_classified P with htri | hfar | htw
  · obtain ⟨a, b, h0a, hab, hb0⟩ := htri
    have h0a' := e.map_adj_iff.mpr h0a
    have hab' := e.map_adj_iff.mpr hab
    have hb0' := e.map_adj_iff.mpr hb0
    exact three_le_mpNumber_of_triple h0a'.ne hb0'.ne.symm hab'.ne
      (triangle_monophonic h0a' hab' hb0')
  · obtain ⟨v, hv⟩ := hfar
    have hr : ReachTwo G (e 0) (e v) := reachTwo_of_edist_le_two
      ((SimpleGraph.edist_le_ediam (G := G)).trans hd)
    exact False.elim (hv (iso_reachTwo e hr))
  · have h05 : ∀ w, G.Adj (e 0) w ↔ G.Adj (e 5) w := by
      intro w
      obtain ⟨z, rfl⟩ := e.surjective w
      exact e.map_adj_iff.trans ((htw.1 z).trans e.map_adj_iff.symm)
    have h010 : ∀ w, G.Adj (e 0) w ↔ G.Adj (e 10) w := by
      intro w
      obtain ⟨z, rfl⟩ := e.surjective w
      exact e.map_adj_iff.trans ((htw.2 z).trans e.map_adj_iff.symm)
    exact three_le_mpNumber_of_triple
      (fun h => (by decide : (0 : Fin 15) ≠ 5) (e.injective h))
      (fun h => (by decide : (0 : Fin 15) ≠ 10) (e.injective h))
      (fun h => (by decide : (5 : Fin 15) ≠ 10) (e.injective h))
      (twins_monophonic h05 h010)

theorem no_circulant15 [Fintype V] (hG : IsCirculant15 G) :
    ¬ (G.ediam = 2 ∧ mpNumber G = 2) := by
  rintro ⟨hd, hm⟩
  have := three_le_mpNumber_of_circulant15 hG hd.le
  omega

/-- Difference `v-u` in the actual cyclic group of order 15. -/
def difference (u v : Fin 15) : Fin 15 :=
  ⟨(v.val + 15 - u.val) % 15, Nat.mod_lt _ (by decide)⟩

def positiveGenerator (k : Fin 7) : Fin 15 := ⟨k.val + 1, by omega⟩

theorem difference_zero : ∀ v : Fin 15, difference 0 v = v := by decide

theorem inverse_pair_cover : ∀ u v : Fin 15, u ≠ v →
    ∃ k : Fin 7, difference u v = positiveGenerator k ∨
      difference v u = positiveGenerator k := by decide

theorem difference_step : ∀ u v : Fin 15, ∀ k : Fin 7,
    ((u.val + k.val + 1) % 15 = v.val ∨
      (v.val + k.val + 1) % 15 = u.val) ↔
    (difference u v = positiveGenerator k ∨
      difference v u = positiveGenerator k) := by decide

/-- An unrestricted cyclic Cayley presentation.  Simplicity and symmetry of
`G` force zero exclusion and inverse closure of `S`; they are not extra
unproved assumptions.  `e` allows completely arbitrary original labels. -/
def HasCayleyPresentation15 (G : SimpleGraph V) : Prop :=
  ∃ e : Fin 15 ≃ V, ∃ S : Set (Fin 15),
    ∀ u v, G.Adj (e u) (e v) ↔ difference u v ∈ S

theorem cayleyPresentation_card [Fintype V] (hG : HasCayleyPresentation15 G) :
    Fintype.card V = 15 := by
  obtain ⟨e, _, _⟩ := hG
  simpa using Fintype.card_congr e.symm

/-- Every raw connection set is encoded by the seven inverse-pair bits.
This proves the coverage bridge, rather than assuming a finite classification
of all abstract circulants. -/
theorem cayleyPresentation_isCirculant15
    (hG : HasCayleyPresentation15 G) : IsCirculant15 G := by
  classical
  obtain ⟨e, S, he⟩ := hG
  have hnormalize : ∀ u v, G.Adj (e u) (e v) ↔
      G.Adj (e 0) (e (difference u v)) := by
    intro u v
    rw [he u v, he 0 (difference u v), difference_zero]
  let P : Choices := fun k => decide (G.Adj (e 0) (e (positiveGenerator k)))
  have hP (k : Fin 7) : P k = true ↔ G.Adj (e 0) (e (positiveGenerator k)) := by
    simp [P]
  refine ⟨P, ⟨{ toEquiv := e, map_rel_iff' := ?_ }⟩⟩
  intro u v
  change G.Adj (e u) (e v) ↔ cyclicAdj P u v
  constructor
  · intro hadj
    have hne : u ≠ v := fun h => hadj.ne (congrArg e h)
    obtain ⟨k, hk⟩ := inverse_pair_cover u v hne
    refine ⟨hne, k, ?_, (difference_step u v k).mpr hk⟩
    apply (hP k).mpr
    rcases hk with hk | hk
    · simpa only [hk] using (hnormalize u v).mp hadj
    · simpa only [hk] using (hnormalize v u).mp hadj.symm
  · rintro ⟨_, k, hk, hstep⟩
    have hgen := (hP k).mp hk
    rcases (difference_step u v k).mp hstep with hdiff | hdiff
    · apply (hnormalize u v).mpr
      simpa only [hdiff] using hgen
    · apply SimpleGraph.Adj.symm
      apply (hnormalize v u).mpr
      simpa only [hdiff] using hgen

/-- Original circulant order-15 exclusion, without prespecified vertex labels
or a presumed reduced connection-set list. -/
theorem no_cayley15 [Fintype V] (hG : HasCayleyPresentation15 G) :
    ¬ (G.ediam = 2 ∧ mpNumber G = 2) :=
  no_circulant15 (cayleyPresentation_isCirculant15 hG)

/-- The natural-valued diameter formulation, also excluding disconnected graphs
because mathlib's diameter is zero in that case. -/
theorem no_cayley15_nat_diameter [Fintype V] (hG : HasCayleyPresentation15 G) :
    ¬ (G.diam = 2 ∧ mpNumber G = 2) := by
  rintro ⟨hd, hm⟩
  have hn : G.ediam ≠ ⊤ := G.ediam_ne_top_of_diam_ne_zero (by omega)
  have he : G.ediam = 2 := by
    have hc := G.natCast_diam_eq_ediam_iff.mpr hn
    rw [hd] at hc
    exact hc.symm
  exact no_cayley15 hG ⟨he, hm⟩

/-- Usual circulant connection-set presentation on cyclic labels of any
positive order.  It is deliberately independent of the 15-vertex classifier. -/
def CyclicConnectionPresentation (n : ℕ) (hn : 0 < n)
    (G : SimpleGraph (Fin n)) : Prop :=
  ∃ S : Set (Fin n), ∀ u v,
    G.Adj u v ↔ (⟨(v.val + n - u.val) % n, Nat.mod_lt _ hn⟩ : Fin n) ∈ S

/-- Conjecture 4.5, using cyclic labels for its existential circulant graph.
The maximum is over all original induced simple paths, through the proved
`monophonicPosition_iff_original` bridge. -/
def OriginalConjecture45 : Prop :=
  ∀ n : ℕ, ∀ hn : 11 ≤ n, ∃ G : SimpleGraph (Fin n),
    CyclicConnectionPresentation n (by omega) G ∧ G.diam = 2 ∧ mpNumber G = 2

theorem not_originalConjecture45 : ¬ OriginalConjecture45 := by
  intro h
  obtain ⟨G, ⟨S, hS⟩, hd, hm⟩ := h 15 (by decide)
  have hG : HasCayleyPresentation15 G := by
    refine ⟨Equiv.refl _, S, ?_⟩
    intro u v
    exact hS u v
  exact no_cayley15_nat_diameter hG ⟨hd, hm⟩

end MonophonicCirculant15

#print axioms MonophonicCirculant15.monophonicPosition_iff_original
#print axioms MonophonicCirculant15.mpNumber_attained
#print axioms MonophonicCirculant15.monophonic_of_open_twins
#print axioms MonophonicCirculant15.finite_classification
#print axioms MonophonicCirculant15.cayleyPresentation_isCirculant15
#print axioms MonophonicCirculant15.no_cayley15_nat_diameter
#print axioms MonophonicCirculant15.not_originalConjecture45
