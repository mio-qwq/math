import Mathlib.Combinatorics.SimpleGraph.Prod
import Mathlib.Data.Finset.Max
import Mathlib.Data.Finset.Card
import Mathlib.Data.Finset.Powerset
import Mathlib.Data.Fintype.Powerset
import Mathlib.Data.Nat.Find
import Mathlib.Data.Fin.VecNotation
import Mathlib.Tactic.FinCases
import Lean.Elab.Tactic.Omega

/-!
A fixed counterexample to the lower general-position Cartesian-product bound.
The two connected factors have 11 and 29 vertices, both lowerGP at least 6;
their actual Cartesian product has an inclusion-maximal GP set of size 5.
Original source: Welton--Khudairi--Tuite, final Conjecture 3,
arXiv 2404.19451v1 Conjecture 2.10. Verification scope is this fixed pair.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 4000000

namespace LowerGPProduct319

open SimpleGraph

universe u

section Semantics

variable {V : Type u} [DecidableEq V]

/-- Shortest among all actual simple paths with the same endpoints. -/
def IsShortest {G : SimpleGraph V} {x y : V} (p : G.Walk x y) : Prop :=
  ∀ q : G.Walk x y, q.IsPath → p.length ≤ q.length

omit [DecidableEq V] in
theorem shortest_iff_length_eq_dist {G : SimpleGraph V} {x y : V}
    (p : G.Walk x y) :
    IsShortest p ↔ p.length = G.dist x y := by
  constructor
  · intro h
    obtain ⟨q, hq, hlen⟩ := p.reachable.exists_path_of_dist
    have hl := h q hq
    have hr := SimpleGraph.dist_le p
    omega
  · intro h q _
    rw [h]
    exact SimpleGraph.dist_le q

/-- Original GP: every actual shortest simple path contains at most two selected
vertices, expressed by forbidding three strictly increasing support positions.
The endpoints of the path need not belong to S. -/
def OriginalGP (G : SimpleGraph V) (S : Finset V) : Prop :=
  ∀ {x y : V} (p : G.Walk x y), p.IsPath → IsShortest p →
    ∀ i j k : ℕ, i < j → j < k → k ≤ p.length →
      p.getVert i ∈ S → p.getVert j ∈ S → p.getVert k ∈ S → False

/-- A computable distance-table condition, checked in all ordered roles. -/
def MetricGP (d : V → V → ℕ) (S : Finset V) : Prop :=
  ∀ x ∈ S, ∀ y ∈ S, ∀ z ∈ S,
    x ≠ y → x ≠ z → y ≠ z → d x z ≠ d x y + d y z

instance metricGPDecidable [Fintype V] (d : V → V → ℕ) (S : Finset V) :
    Decidable (MetricGP d S) := by unfold MetricGP; infer_instance

omit [DecidableEq V] in
theorem shortest_dist_getVert {G : SimpleGraph V} {x y : V}
    (p : G.Walk x y) (hlen : p.length = G.dist x y)
    {i j : ℕ} (hij : i ≤ j) (hj : j ≤ p.length) :
    G.dist (p.getVert i) (p.getVert j) = j - i := by
  have hsub := ((p.take j).isSubwalk_drop i).trans (p.isSubwalk_take j)
  have hh := SimpleGraph.length_eq_dist_of_subwalk hlen hsub
  simpa only [Walk.drop_length, Walk.take_length, Walk.take_getVert,
    Nat.min_eq_left hj, Nat.min_eq_right hij] using hh.symm

omit [DecidableEq V] in
theorem metricGP_iff_original {G : SimpleGraph V} (hc : G.Connected) (S : Finset V) :
    MetricGP G.dist S ↔ OriginalGP G S := by
  constructor
  · intro h x y p hp hshort i j k hij hjk hk hi hj hs
    have hlen := (shortest_iff_length_eq_dist p).mp hshort
    have hi' : i ≤ p.length := by omega
    have hj' : j ≤ p.length := by omega
    have h_ij := shortest_dist_getVert p hlen (Nat.le_of_lt hij) hj'
    have h_jk := shortest_dist_getVert p hlen (Nat.le_of_lt hjk) hk
    have h_ik := shortest_dist_getVert p hlen (by omega : i ≤ k) hk
    have hneij : p.getVert i ≠ p.getVert j := by
      intro he
      have hh := hp.getVert_injOn hi' hj' he
      omega
    have hneik : p.getVert i ≠ p.getVert k := by
      intro he
      have hh := hp.getVert_injOn hi' hk he
      omega
    have hnejk : p.getVert j ≠ p.getVert k := by
      intro he
      have hh := hp.getVert_injOn hj' hk he
      omega
    exact h _ hi _ hj _ hs hneij hneik hnejk (by omega)
  · intro h x hx y hy z hz hxy _hxz hyz heq
    obtain ⟨p, _hp, hplen⟩ := hc.exists_path_of_dist x y
    obtain ⟨q, _hq, hqlen⟩ := hc.exists_path_of_dist y z
    let w := p.append q
    have hwlen : w.length = G.dist x z := by
      simp only [w, Walk.length_append, hplen, hqlen, ← heq]
    have hwpath : w.IsPath := w.isPath_of_length_eq_dist hwlen
    have hps : 0 < p.length := by
      rw [hplen]
      exact hc.pos_dist_of_ne hxy
    have hqs : 0 < q.length := by
      rw [hqlen]
      exact hc.pos_dist_of_ne hyz
    have hpw : p.length < w.length := by simp only [w, Walk.length_append]; omega
    apply h w hwpath ((shortest_iff_length_eq_dist w).mpr hwlen)
      0 p.length w.length hps hpw (Nat.le_refl _)
    · simpa using hx
    · simpa [w, Walk.getVert_append] using hy
    · simpa using hz

omit [DecidableEq V] in
theorem originalGP_mono {G : SimpleGraph V} {S T : Finset V}
    (h : OriginalGP G T) (hST : S ⊆ T) : OriginalGP G S := by
  intro x y p hp hs i j k hij hjk hk hi hj hh
  exact h p hp hs i j k hij hjk hk (hST hi) (hST hj) (hST hh)

omit [DecidableEq V] in
theorem metricGP_mono {d : V → V → ℕ} {S T : Finset V}
    (h : MetricGP d T) (hST : S ⊆ T) : MetricGP d S := by
  intro x hx y hy z hz hxy hxz hyz
  exact h x (hST hx) y (hST hy) z (hST hz) hxy hxz hyz

/-- One-point maximality; the next theorem proves full inclusion-maximality. -/
def MaximalGP (G : SimpleGraph V) (S : Finset V) : Prop :=
  OriginalGP G S ∧ ∀ x, x ∉ S → ¬ OriginalGP G (insert x S)

theorem maximalGP_iff_inclusion {G : SimpleGraph V} (S : Finset V) :
    MaximalGP G S ↔ OriginalGP G S ∧
      ∀ T : Finset V, S ⊆ T → OriginalGP G T → T = S := by
  constructor
  · rintro ⟨hgp, hmax⟩
    refine ⟨hgp, ?_⟩
    intro T hST hT
    apply Finset.Subset.antisymm
    · intro x hxT
      by_contra hxS
      apply hmax x hxS
      apply originalGP_mono hT
      exact Finset.insert_subset hxT hST
    · exact hST
  · rintro ⟨hgp, hmax⟩
    refine ⟨hgp, ?_⟩
    intro x hxS hnew
    have heq := hmax (insert x S) (Finset.subset_insert x S) hnew
    exact hxS (heq ▸ Finset.mem_insert_self x S)

omit [DecidableEq V] in
theorem originalGP_empty (G : SimpleGraph V) : OriginalGP G (∅ : Finset V) := by
  simp [OriginalGP]

theorem exists_maximalGP [Fintype V] (G : SimpleGraph V) :
    ∃ S : Finset V, MaximalGP G S := by
  classical
  let candidates : Finset (Finset V) := Finset.univ.filter (OriginalGP G)
  have hnonempty : candidates.Nonempty := by
    refine ⟨∅, ?_⟩
    simp [candidates, originalGP_empty]
  obtain ⟨S, hS, hmax⟩ := candidates.exists_max_image Finset.card hnonempty
  have hgp : OriginalGP G S := (Finset.mem_filter.mp hS).2
  refine ⟨S, hgp, ?_⟩
  intro x hx hnew
  have hmem : insert x S ∈ candidates := by simp [candidates, hnew]
  have hle := hmax (insert x S) hmem
  rw [Finset.card_insert_of_notMem hx] at hle
  omega

theorem exists_maximal_card [Fintype V] (G : SimpleGraph V) :
    ∃ n : ℕ, ∃ S : Finset V, MaximalGP G S ∧ S.card = n := by
  obtain ⟨S, hS⟩ := exists_maximalGP G
  exact ⟨S.card, S, hS, rfl⟩

/-- The actual minimum cardinality among inclusion-maximal original GP sets. -/
noncomputable def lowerGP [Fintype V] (G : SimpleGraph V) : ℕ := by
  classical
  exact Nat.find (exists_maximal_card G)

theorem lowerGP_spec [Fintype V] (G : SimpleGraph V) :
    ∃ S : Finset V, MaximalGP G S ∧ S.card = lowerGP G := by
  classical
  exact Nat.find_spec (exists_maximal_card G)

theorem lowerGP_le_card [Fintype V] {G : SimpleGraph V} {S : Finset V}
    (hS : MaximalGP G S) : lowerGP G ≤ S.card := by
  classical
  exact Nat.find_min' (exists_maximal_card G) ⟨S, hS, rfl⟩

theorem lowerGP_ge [Fintype V] {G : SimpleGraph V} {n : ℕ}
    (h : ∀ S : Finset V, MaximalGP G S → n ≤ S.card) : n ≤ lowerGP G := by
  obtain ⟨S, hS, hcard⟩ := lowerGP_spec G
  simpa [hcard] using h S hS

end Semantics

section TwinSaturation

variable {V : Type u} [DecidableEq V] {G : SimpleGraph V}

/-- The metric consequences of adjacent true twins. They will be checked from
the actual H adjacency and proven 0/1/2 distance formula below. -/
def DistanceTwins (G : SimpleGraph V) (x y : V) : Prop :=
  G.dist x y = 1 ∧ ∀ z, z ≠ x → z ≠ y → G.dist x z = G.dist y z

theorem metricGP_insert_distanceTwin (hc : G.Connected) {S : Finset V} {x y : V}
    (hgp : MetricGP G.dist S) (hx : x ∈ S) (hy : y ∉ S)
    (ht : DistanceTwins G x y) : MetricGP G.dist (insert y S) := by
  have hyx : G.dist y x = 1 := by rw [G.dist_comm, ht.1]
  have hleft : ∀ b ∈ S, ∀ c ∈ S, b ≠ c →
      G.dist y c ≠ G.dist y b + G.dist b c := by
    intro b hb c hcS hbc
    have hby : b ≠ y := by intro he; exact hy (he ▸ hb)
    have hcy : c ≠ y := by intro he; exact hy (he ▸ hcS)
    by_cases hbx : b = x
    · subst b
      have hcx : c ≠ x := Ne.symm hbc
      have hh := ht.2 c hcx hcy
      rw [hyx]
      omega
    · by_cases hcx : c = x
      · subst c
        have he := ht.2 b hbx hby
        have hp := hc.pos_dist_of_ne (Ne.symm hbx)
        rw [hyx, (G.dist_comm : G.dist b x = G.dist x b)]
        omega
      · rw [← ht.2 c hcx hcy, ← ht.2 b hbx hby]
        exact hgp x hx b hb c hcS (Ne.symm hbx) (Ne.symm hcx) hbc
  have hmiddle : ∀ a ∈ S, ∀ c ∈ S, a ≠ c →
      G.dist a c ≠ G.dist a y + G.dist y c := by
    intro a ha c hcS hac
    have hay : a ≠ y := by intro he; exact hy (he ▸ ha)
    have hcy : c ≠ y := by intro he; exact hy (he ▸ hcS)
    by_cases hax : a = x
    · subst a
      have hcx : c ≠ x := Ne.symm hac
      have he := ht.2 c hcx hcy
      rw [ht.1]
      omega
    · by_cases hcx : c = x
      · subst c
        have he := ht.2 a hax hay
        rw [hyx, (G.dist_comm : G.dist a y = G.dist y a), (G.dist_comm : G.dist a x = G.dist x a)]
        omega
      · rw [(G.dist_comm : G.dist a y = G.dist y a), ← ht.2 a hax hay, (G.dist_comm : G.dist x a = G.dist a x),
          ← ht.2 c hcx hcy]
        exact hgp a ha x hx c hcS hax hac (Ne.symm hcx)
  intro a ha b hb c hcS hab hac hbc
  by_cases hay : a = y
  · subst a
    have hbS : b ∈ S := (Finset.mem_insert.mp hb).resolve_left (Ne.symm hab)
    have hcS' : c ∈ S := (Finset.mem_insert.mp hcS).resolve_left (Ne.symm hac)
    exact hleft b hbS c hcS' hbc
  · have haS : a ∈ S := (Finset.mem_insert.mp ha).resolve_left hay
    by_cases hby : b = y
    · subst b
      have hcS' : c ∈ S := (Finset.mem_insert.mp hcS).resolve_left (Ne.symm hbc)
      exact hmiddle a haS c hcS' hac
    · have hbS : b ∈ S := (Finset.mem_insert.mp hb).resolve_left hby
      by_cases hcy : c = y
      · subst c
        have hh := hleft b hbS a haS (Ne.symm hab)
        intro he
        apply hh
        have h1 := (G.dist_comm : G.dist y a = G.dist a y)
        have h2 := (G.dist_comm : G.dist y b = G.dist b y)
        have h3 := (G.dist_comm : G.dist b a = G.dist a b)
        omega
      · have hcS' : c ∈ S := (Finset.mem_insert.mp hcS).resolve_left hcy
        exact hgp a haS b hbS c hcS' hab hac hbc

theorem maximalGP_saturates_distanceTwins (hc : G.Connected) {S : Finset V}
    (hS : MaximalGP G S) {x y : V} (hx : x ∈ S)
    (ht : DistanceTwins G x y) : y ∈ S := by
  by_contra hy
  apply hS.2 y hy
  apply (metricGP_iff_original hc _).mp
  exact metricGP_insert_distanceTwin hc ((metricGP_iff_original hc _).mpr hS.1) hx hy ht

end TwinSaturation

section DiameterTwo

variable {V : Type u} [DecidableEq V] (G : SimpleGraph V) [DecidableRel G.Adj]

def tableDistance (x y : V) : ℕ := if x = y then 0 else if G.Adj x y then 1 else 2

/-- A displayed common-neighbor certificate proves the entire actual distance table. -/
theorem edist_eq_tableDistance (hub : V)
    (hcommon : ∀ x y, x ≠ y → ¬ G.Adj x y → G.Adj x hub ∧ G.Adj y hub)
    (x y : V) : G.edist x y = (tableDistance G x y : ℕ∞) := by
  by_cases hxy : x = y
  · subst y
    simp [tableDistance]
  · by_cases hadj : G.Adj x y
    · simp [tableDistance, hxy, hadj, SimpleGraph.edist_eq_one_iff_adj.mpr hadj]
    · have hneigh := hcommon x y hxy hadj
      have htwo : G.edist x y = 2 := SimpleGraph.edist_eq_two_iff.mpr
        ⟨hxy, hadj, ⟨hub, hneigh⟩⟩
      simp [tableDistance, hxy, hadj, htwo]

theorem dist_eq_tableDistance (hub : V)
    (hcommon : ∀ x y, x ≠ y → ¬ G.Adj x y → G.Adj x hub ∧ G.Adj y hub)
    (x y : V) : G.dist x y = tableDistance G x y := by
  simp [SimpleGraph.dist, edist_eq_tableDistance G hub hcommon]

theorem connected_of_tableDistance [Nonempty V] (hub : V)
    (hcommon : ∀ x y, x ≠ y → ¬ G.Adj x y → G.Adj x hub ∧ G.Adj y hub) :
    G.Connected := by
  refine ⟨fun x y => SimpleGraph.reachable_of_edist_ne_top ?_⟩
  rw [edist_eq_tableDistance G hub hcommon]
  exact ENat.natCast_ne_top _

end DiameterTwo

/-! ## Actual fixed graphs -/

def gAdjacent (x y : Fin 11) : Prop :=
  x ≠ y ∧ (x = 0 ∨ y = 0 ∨ (x.val ≤ 5 ∧ y.val ≤ 5) ∨
    (6 ≤ x.val ∧ 6 ≤ y.val))

instance : DecidableRel gAdjacent := fun _ _ => by unfold gAdjacent; infer_instance

def G : SimpleGraph (Fin 11) where
  Adj := gAdjacent
  symm := ⟨by decide⟩
  loopless := ⟨by decide⟩

instance : DecidableRel G.Adj := inferInstanceAs (DecidableRel gAdjacent)

def hCoreAdjacent (x y : Fin 29) : Prop :=
  (x = 2 ∨ y = 2 ∨ (x.val < 2 ∧ 3 ≤ y.val) ∨ (y.val < 2 ∧ 3 ≤ x.val))

def hCloneNear (a q : Fin 29) : Prop :=
  a = 2 ∨ a.val = (q.val - 5) / 12 ∨ a.val = 3 + ((q.val - 5) / 6) % 2

def hAdjacent (x y : Fin 29) : Prop :=
  x ≠ y ∧
    ((x.val < 5 ∧ y.val < 5 ∧ hCoreAdjacent x y) ∨
     (5 ≤ x.val ∧ 5 ≤ y.val ∧ (x.val - 5) / 6 = (y.val - 5) / 6) ∨
     (x.val < 5 ∧ 5 ≤ y.val ∧ hCloneNear x y) ∨
     (y.val < 5 ∧ 5 ≤ x.val ∧ hCloneNear y x))

instance : DecidableRel hAdjacent := fun _ _ => by
  unfold hAdjacent hCoreAdjacent hCloneNear
  infer_instance

def H : SimpleGraph (Fin 29) where
  Adj := hAdjacent
  symm := ⟨by decide⟩
  loopless := ⟨by decide⟩

instance : DecidableRel H.Adj := inferInstanceAs (DecidableRel hAdjacent)

def dG : Fin 11 → Fin 11 → ℕ := tableDistance G
def dH : Fin 29 → Fin 29 → ℕ := tableDistance H

theorem g_common : ∀ x y : Fin 11, x ≠ y → ¬ G.Adj x y →
    G.Adj x 0 ∧ G.Adj y 0 := by decide

theorem h_common : ∀ x y : Fin 29, x ≠ y → ¬ H.Adj x y →
    H.Adj x 2 ∧ H.Adj y 2 := by decide

theorem G_connected : G.Connected := connected_of_tableDistance G 0 g_common
theorem H_connected : H.Connected := connected_of_tableDistance H 2 h_common

theorem G_dist (x y : Fin 11) : G.dist x y = dG x y :=
  dist_eq_tableDistance G 0 g_common x y

theorem H_dist (x y : Fin 29) : H.dist x y = dH x y :=
  dist_eq_tableDistance H 2 h_common x y

theorem G_edist (x y : Fin 11) : G.edist x y = (dG x y : ℕ∞) :=
  edist_eq_tableDistance G 0 g_common x y

theorem H_edist (x y : Fin 29) : H.edist x y = (dH x y : ℕ∞) :=
  edist_eq_tableDistance H 2 h_common x y

theorem G_gp_iff (S : Finset (Fin 11)) : OriginalGP G S ↔ MetricGP dG S := by
  rw [← metricGP_iff_original G_connected]
  simp only [MetricGP, G_dist]

theorem H_gp_iff (S : Finset (Fin 29)) : OriginalGP H S ↔ MetricGP dH S := by
  rw [← metricGP_iff_original H_connected]
  simp only [MetricGP, H_dist]

/-! ## Lower bounds in the factors -/



/-- All ten non-cut vertices. -/
def gStructuralOuter : Finset (Fin 11) := Finset.univ.erase 0

/-- The left K6, including the common cut vertex. -/
def gStructuralLeft : Finset (Fin 11) :=
  Finset.univ.filter (fun v => v.val ≤ 5)

/-- The right K6, including the common cut vertex. -/
def gStructuralRight : Finset (Fin 11) :=
  Finset.univ.filter (fun v => v = 0 ∨ 6 ≤ v.val)

theorem mem_gStructuralOuter (v : Fin 11) :
    v ∈ gStructuralOuter ↔ v ≠ 0 := by
  simp [gStructuralOuter]

theorem mem_gStructuralLeft (v : Fin 11) :
    v ∈ gStructuralLeft ↔ v.val ≤ 5 := by
  simp [gStructuralLeft]

theorem mem_gStructuralRight (v : Fin 11) :
    v ∈ gStructuralRight ↔ v = 0 ∨ 6 ≤ v.val := by
  simp [gStructuralRight]

theorem gStructuralOuter_card : gStructuralOuter.card = 10 := by decide
theorem gStructuralLeft_card : gStructuralLeft.card = 6 := by decide
theorem gStructuralRight_card : gStructuralRight.card = 6 := by decide

theorem gStructuralOuter_metricGP : MetricGP dG gStructuralOuter := by decide
theorem gStructuralLeft_metricGP : MetricGP dG gStructuralLeft := by decide
theorem gStructuralRight_metricGP : MetricGP dG gStructuralRight := by decide

/-- The only finite cross-side certificate: 11 x 11 ordered vertex pairs.
For a nonzero left vertex and a right vertex, the cut vertex 0 is between them.
The distinctness facts are included so later proofs need no Fin coercion work. -/
theorem gStructural_cross_through_zero : ∀ a b : Fin 11,
    a ≠ 0 → a.val ≤ 5 → 6 ≤ b.val →
    a ≠ b ∧ (0 : Fin 11) ≠ b ∧
      dG a b = dG a 0 + dG 0 b := by decide

/-- Every GP set lies in one of the three explicit GP sets of size at least 6.
This is a structural proof for an arbitrary S, not a finite subset certificate. -/
theorem gStructural_large_superset (S : Finset (Fin 11))
    (hgp : MetricGP dG S) :
    ∃ T : Finset (Fin 11), S ⊆ T ∧ MetricGP dG T ∧ 6 ≤ T.card := by
  by_cases hzero : (0 : Fin 11) ∈ S
  · by_cases hleft : ∃ a ∈ S, a ≠ (0 : Fin 11) ∧ a.val ≤ 5
    · obtain ⟨a, ha, ha0, ha5⟩ := hleft
      refine ⟨gStructuralLeft, ?_, gStructuralLeft_metricGP, ?_⟩
      · intro b hb
        apply (mem_gStructuralLeft b).mpr
        by_contra hb5
        have hb6 : 6 ≤ b.val := by omega
        have hcross := gStructural_cross_through_zero a b ha0 ha5 hb6
        exact (hgp a ha 0 hzero b hb ha0 hcross.1 hcross.2.1) hcross.2.2
      · exact le_of_eq gStructuralLeft_card.symm
    · refine ⟨gStructuralRight, ?_, gStructuralRight_metricGP, ?_⟩
      · intro b hb
        apply (mem_gStructuralRight b).mpr
        by_cases hb0 : b = (0 : Fin 11)
        · exact Or.inl hb0
        · apply Or.inr
          by_contra hb6
          have hb5 : b.val ≤ 5 := by omega
          exact hleft ⟨b, hb, hb0, hb5⟩
      · exact le_of_eq gStructuralRight_card.symm
  · refine ⟨gStructuralOuter, ?_, gStructuralOuter_metricGP, ?_⟩
    · intro b hb
      apply (mem_gStructuralOuter b).mpr
      intro hb0
      subst b
      exact hzero hb
    · rw [gStructuralOuter_card]
      decide

/-- Same signature as the frozen theorem. Extend inside the explicit larger
GP set supplied by the structural classification. -/
theorem g_small_extension : ∀ S : Finset (Fin 11), S.card < 6 → MetricGP dG S →
    ∃ x : Fin 11, x ∉ S ∧ MetricGP dG (insert x S) := by
  intro S hcard hgp
  obtain ⟨T, hST, hTgp, hTcard⟩ := gStructural_large_superset S hgp
  have hlt : S.card < T.card := lt_of_lt_of_le hcard hTcard
  obtain ⟨x, hxT, hxS⟩ := Finset.exists_mem_notMem_of_card_lt_card hlt
  refine ⟨x, hxS, ?_⟩
  exact metricGP_mono hTgp (Finset.insert_subset_iff.mpr ⟨hxT, hST⟩)



theorem G_maximal_card (S : Finset (Fin 11)) (hS : MaximalGP G S) : 6 ≤ S.card := by
  by_contra hn
  obtain ⟨x, hx, hnew⟩ := g_small_extension S (by omega) ((G_gp_iff S).mp hS.1)
  exact hS.2 x hx ((G_gp_iff _).mpr hnew)

def cloneClass (x : Fin 29) : Finset (Fin 29) :=
  Finset.univ.filter (fun y => 5 ≤ y.val ∧ (y.val - 5) / 6 = (x.val - 5) / 6)

theorem cloneClass_card : ∀ x : Fin 29, 5 ≤ x.val → (cloneClass x).card = 6 := by decide

theorem h_clone_closed_twins : ∀ x y : Fin 29, 5 ≤ x.val → y ∈ cloneClass x →
    ∀ z : Fin 29, (H.Adj x z ∨ x = z) ↔ (H.Adj y z ∨ y = z) := by decide

theorem h_clone_metric : ∀ x y : Fin 29, 5 ≤ x.val → y ∈ cloneClass x → x ≠ y →
    dH x y = 1 ∧ ∀ z : Fin 29, z ≠ x → z ≠ y → dH x z = dH y z := by decide

theorem h_saturates_clones {S : Finset (Fin 29)} (hS : MaximalGP H S)
    {x : Fin 29} (hx : x ∈ S) (hxc : 5 ≤ x.val) : cloneClass x ⊆ S := by
  intro y hy
  by_cases hxy : x = y
  · simpa [hxy] using hx
  · apply maximalGP_saturates_distanceTwins H_connected hS hx
    have ht := h_clone_metric x y hxc hy hxy
    simpa only [DistanceTwins, H_dist] using ht

def coreEmbed (i : Fin 5) : Fin 29 := ⟨i.val, by have hi := i.is_lt; omega⟩
def coreLift (T : Finset (Fin 5)) : Finset (Fin 29) := T.image coreEmbed

/-- Only 32 core subsets. No Fintype quantifier over Finset (Fin 29). -/
theorem h_core_extension : ∀ T : Finset (Fin 5), MetricGP dH (coreLift T) →
    ∃ x : Fin 29, x ∉ coreLift T ∧ MetricGP dH (insert x (coreLift T)) := by decide

theorem H_maximal_card (S : Finset (Fin 29)) (hS : MaximalGP H S) : 6 ≤ S.card := by
  classical
  by_cases hcl : ∃ x ∈ S, 5 ≤ x.val
  · obtain ⟨x, hx, hxc⟩ := hcl
    have hle := Finset.card_le_card (h_saturates_clones hS hx hxc)
    simpa only [cloneClass_card x hxc] using hle
  · have hsmall : ∀ x ∈ S, x.val < 5 := by
      intro x hx
      by_contra hn
      exact hcl ⟨x, hx, by omega⟩
    let T : Finset (Fin 5) := Finset.univ.filter (fun i => coreEmbed i ∈ S)
    have hrepr : coreLift T = S := by
      ext x
      constructor
      · intro hx
        obtain ⟨i, hi, he⟩ := Finset.mem_image.mp hx
        rw [← he]
        exact (Finset.mem_filter.mp hi).2
      · intro hx
        let i : Fin 5 := ⟨x.val, hsmall x hx⟩
        have he : coreEmbed i = x := Fin.ext rfl
        apply Finset.mem_image.mpr
        refine ⟨i, ?_, he⟩
        simpa [T, he] using hx
    obtain ⟨x, hx, hnew⟩ := h_core_extension T (by
      rw [hrepr]
      exact (H_gp_iff S).mp hS.1)
    rw [hrepr] at hx hnew
    exact False.elim (hS.2 x hx ((H_gp_iff _).mpr hnew))

theorem G_lower_at_least_six : 6 ≤ lowerGP G := lowerGP_ge G_maximal_card
theorem H_lower_at_least_six : 6 ≤ lowerGP H := lowerGP_ge H_maximal_card

/-! ## The actual Cartesian product and the five selected vertices -/

abbrev ProductVertex := Fin 11 × Fin 29
def productGraph : SimpleGraph ProductVertex := G □ H
def productDistance (x y : ProductVertex) : ℕ := dG x.1 y.1 + dH x.2 y.2

theorem fixed_orders : Fintype.card (Fin 11) = 11 ∧ Fintype.card (Fin 29) = 29 ∧
    Fintype.card ProductVertex = 319 := by decide

theorem product_connected : productGraph.Connected := G_connected.boxProd H_connected

theorem product_edist (x y : ProductVertex) :
    productGraph.edist x y = (productDistance x y : ℕ∞) := by
  change (G □ H).edist x y = _
  rw [SimpleGraph.edist_boxProd, G_edist, H_edist]
  simp [productDistance]

theorem product_dist (x y : ProductVertex) :
    productGraph.dist x y = productDistance x y := by
  simp [SimpleGraph.dist, product_edist]

theorem product_gp_iff (S : Finset ProductVertex) :
    OriginalGP productGraph S ↔ MetricGP productDistance S := by
  rw [← metricGP_iff_original product_connected]
  simp only [MetricGP, product_dist]

def chosen : Fin 5 → ProductVertex := ![(1,0),(1,1),(0,2),(6,3),(6,4)]
def selected : Finset ProductVertex := Finset.univ.image chosen

theorem chosen_injective : Function.Injective chosen := by decide
theorem chosen_mem (i : Fin 5) : chosen i ∈ selected :=
  Finset.mem_image.mpr ⟨i, Finset.mem_univ _, rfl⟩

theorem selected_card : selected.card = 5 := by decide
theorem selected_metricGP : MetricGP productDistance selected := by decide

/-- 319 candidate outside vertices, and at most 5 x 5 selected ordered pairs.
The new point is an ENDPOINT of the geodesic in this certificate. -/
theorem selected_blocks : ∀ x : ProductVertex, x ∉ selected →
    ∃ i j : Fin 5, i ≠ j ∧ x ≠ chosen i ∧ x ≠ chosen j ∧
      productDistance x (chosen j) =
        productDistance x (chosen i) + productDistance (chosen i) (chosen j) := by decide

theorem selected_originalGP : OriginalGP productGraph selected :=
  (product_gp_iff selected).mpr selected_metricGP

/-- Each outside vertex comes with an ACTUAL shortest simple path containing
two distinct selected vertices; this is stronger than a bare distance checksum. -/
theorem selected_actual_shortest_path (x : ProductVertex) (hx : x ∉ selected) :
    ∃ a ∈ selected, ∃ b ∈ selected, x ≠ a ∧ x ≠ b ∧ a ≠ b ∧
      ∃ p : productGraph.Walk x b, p.IsPath ∧ IsShortest p ∧ a ∈ p.support := by
  obtain ⟨i, j, hij, hxi, hxj, heq⟩ := selected_blocks x hx
  obtain ⟨p, _hp, hplen⟩ := product_connected.exists_path_of_dist x (chosen i)
  obtain ⟨q, _hq, hqlen⟩ := product_connected.exists_path_of_dist (chosen i) (chosen j)
  have heq' : productGraph.dist x (chosen j) =
      productGraph.dist x (chosen i) + productGraph.dist (chosen i) (chosen j) := by
    simpa only [product_dist] using heq
  let w := p.append q
  have hlen : w.length = productGraph.dist x (chosen j) := by
    simp only [w, Walk.length_append, hplen, hqlen, ← heq']
  have hw : w.IsPath := w.isPath_of_length_eq_dist hlen
  refine ⟨chosen i, chosen_mem i, chosen j, chosen_mem j, hxi, hxj,
    (fun h => hij (chosen_injective h)), w, hw,
    (shortest_iff_length_eq_dist w).mpr hlen, ?_⟩
  simp [w]

theorem selected_maximalGP : MaximalGP productGraph selected := by
  refine ⟨selected_originalGP, ?_⟩
  intro x hx hnew
  obtain ⟨i, j, hij, hxi, hxj, heq⟩ := selected_blocks x hx
  have hg := (product_gp_iff _).mp hnew
  exact hg x (Finset.mem_insert_self _ _) (chosen i)
    (Finset.mem_insert_of_mem (chosen_mem i)) (chosen j)
    (Finset.mem_insert_of_mem (chosen_mem j)) hxi hxj
    (fun h => hij (chosen_injective h)) heq

theorem product_lower_at_most_five : lowerGP productGraph ≤ 5 := by
  simpa only [selected_card] using lowerGP_le_card selected_maximalGP

theorem fixed_original_counterexample :
    G.Connected ∧ H.Connected ∧ productGraph.Connected ∧
      6 ≤ lowerGP G ∧ 6 ≤ lowerGP H ∧ lowerGP (G □ H) ≤ 5 := by
  exact ⟨G_connected, H_connected, product_connected,
    G_lower_at_least_six, H_lower_at_least_six, product_lower_at_most_five⟩

theorem original_product_bound_false :
    ¬ lowerGP (G □ H) ≥ min (lowerGP G) (lowerGP H) := by
  have hg := G_lower_at_least_six
  have hh := H_lower_at_least_six
  have hp := product_lower_at_most_five
  change lowerGP (G □ H) ≤ 5 at hp
  omega

/-- The literal universally quantified original claim already fails on the fixed
finite vertex types 11 and 29, even with connectedness explicitly required. -/
theorem not_original_conjecture :
    ¬ (∀ (A : SimpleGraph (Fin 11)) (B : SimpleGraph (Fin 29)),
      A.Connected → B.Connected → lowerGP (A □ B) ≥ min (lowerGP A) (lowerGP B)) := by
  intro h
  exact original_product_bound_false (h G H G_connected H_connected)

#print axioms metricGP_iff_original
#print axioms maximalGP_iff_inclusion
#print axioms lowerGP_spec
#print axioms metricGP_insert_distanceTwin
#print axioms G_dist
#print axioms H_dist
#print axioms product_dist
#print axioms gStructural_large_superset
#print axioms g_small_extension
#print axioms G_maximal_card
#print axioms H_maximal_card
#print axioms selected_actual_shortest_path
#print axioms selected_maximalGP
#print axioms fixed_original_counterexample
#print axioms not_original_conjecture

end LowerGPProduct319
