import Q6PackingDomination
import Q6PackingComplexGeometry
import Mathlib.Combinatorics.SimpleGraph.Walk.Basic
import Mathlib.Data.Fintype.Card
import Mathlib.Data.Fintype.Prod
import Mathlib.Data.Fintype.Sum
import Lean.Elab.Tactic.Omega

/-!
Explicit finite simple undirected graphs and standard Mathlib Walks.
No distance matrix, native decision procedure, proof oracle, or linearity
hypothesis is used. The imported Q6 geometry has source-specific compilation and axiom records.

The main statement is the existence version of the original strong-product
conjecture at d=2,p=3, expressed using standard at-most-length Walks. A numeric
gamma function and SimpleGraph.dist are not introduced.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 16000000

namespace Q6PackingComplexCounterexample

open Q6PackingDomination
open Q6PackingComplexGeometry

/-! General actual-graph reachability and the Walk bridge. -/

def Step {α : Type*} (K : SimpleGraph α) (u v : α) : Prop := u = v ∨ K.Adj u v

def Reach {α : Type*} (K : SimpleGraph α) : Nat → α → α → Prop
  | 0, u, v => u = v
  | n + 1, u, v => ∃ w, Step K u w ∧ Reach K n w v

theorem reach_refl {α : Type*} (K : SimpleGraph α) (n : Nat) (u : α) :
    Reach K n u u := by
  induction n with
  | zero => rfl
  | succ n ih => exact ⟨u, Or.inl rfl, ih⟩

theorem reach_to_walk {α : Type*} (K : SimpleGraph α) (n : Nat) (u v : α)
    (h : Reach K n u v) : ∃ p : K.Walk u v, p.length ≤ n := by
  induction n generalizing u v with
  | zero =>
      change u = v at h
      subst v
      exact ⟨.nil, Nat.le_refl 0⟩
  | succ n ih =>
      rcases h with ⟨w, hstep, htail⟩
      rcases ih w v htail with ⟨p, hp⟩
      rcases hstep with heq | hadj
      · subst w
        exact ⟨p, Nat.le_trans hp (Nat.le_succ n)⟩
      · refine ⟨.cons hadj p, ?_⟩
        simpa only [SimpleGraph.Walk.length_cons] using (Nat.succ_le_succ hp)

theorem walk_to_reach {α : Type*} (K : SimpleGraph α) {u v : α}
    (p : K.Walk u v) : ∀ n, p.length ≤ n → Reach K n u v := by
  induction p with
  | nil =>
      intro n _
      exact reach_refl K n _
  | @cons u w v hadj p ih =>
      intro n hn
      cases n with
      | zero => simp only [SimpleGraph.Walk.length_cons] at hn; omega
      | succ n =>
          refine ⟨w, Or.inr hadj, ih n ?_⟩
          simp only [SimpleGraph.Walk.length_cons] at hn
          omega

/-- Lazy padding is exactly a standard walk with length at most the bound. -/
theorem reach_iff_walk {α : Type*} (K : SimpleGraph α) (n : Nat) (u v : α) :
    Reach K n u v ↔ ∃ p : K.Walk u v, p.length ≤ n := by
  constructor
  · exact reach_to_walk K n u v
  · rintro ⟨p, hp⟩
    exact walk_to_reach K p n hp

def strong {α β : Type*} (K : SimpleGraph α) (L : SimpleGraph β) :
    SimpleGraph (α × β) where
  Adj u v := u ≠ v ∧ Step K u.1 v.1 ∧ Step L u.2 v.2
  symm.symm u v h := by
    refine ⟨Ne.symm h.1, ?_, ?_⟩
    · exact h.2.1.elim (fun heq => Or.inl heq.symm) (fun ha => Or.inr ha.symm)
    · exact h.2.2.elim (fun heq => Or.inl heq.symm) (fun ha => Or.inr ha.symm)
  loopless.irrefl u h := h.1 rfl

/-- The exact ordinary strong-product edge definition, with no loops. -/
theorem strong_adj_standard {α β : Type*} (K : SimpleGraph α) (L : SimpleGraph β)
    (u v : α × β) :
    (strong K L).Adj u v ↔
      (K.Adj u.1 v.1 ∧ u.2 = v.2) ∨
      (u.1 = v.1 ∧ L.Adj u.2 v.2) ∨
      (K.Adj u.1 v.1 ∧ L.Adj u.2 v.2) := by
  constructor
  · rintro ⟨hne, hk, hl⟩
    rcases hk with heqk | hak <;> rcases hl with heql | hal
    · exact False.elim (hne (Prod.ext heqk heql))
    · exact Or.inr (Or.inl ⟨heqk, hal⟩)
    · exact Or.inl ⟨hak, heql⟩
    · exact Or.inr (Or.inr ⟨hak, hal⟩)
  · rintro (⟨hak, heql⟩ | ⟨heqk, hal⟩ | ⟨hak, hal⟩)
    · exact ⟨fun heq => hak.ne (congrArg Prod.fst heq), Or.inr hak, Or.inl heql⟩
    · exact ⟨fun heq => hal.ne (congrArg Prod.snd heq), Or.inl heqk, Or.inr hal⟩
    · exact ⟨fun heq => hak.ne (congrArg Prod.fst heq), Or.inr hak, Or.inr hal⟩

theorem strong_step {α β : Type*} (K : SimpleGraph α) (L : SimpleGraph β)
    (u v : α × β) :
    Step (strong K L) u v ↔ Step K u.1 v.1 ∧ Step L u.2 v.2 := by
  classical
  constructor
  · rintro (heq | hadj)
    · subst v; exact ⟨Or.inl rfl, Or.inl rfl⟩
    · exact hadj.2
  · intro h
    by_cases heq : u = v
    · exact Or.inl heq
    · exact Or.inr ⟨heq, h⟩

/-- Both coordinates reach the SAME product vertex within the SAME bound. -/
theorem strong_reach {α β : Type*} (K : SimpleGraph α) (L : SimpleGraph β)
    (n : Nat) (u v : α × β) :
    Reach (strong K L) n u v ↔ Reach K n u.1 v.1 ∧ Reach L n u.2 v.2 := by
  induction n generalizing u v with
  | zero =>
      change u = v ↔ u.1 = v.1 ∧ u.2 = v.2
      exact ⟨fun h => ⟨congrArg Prod.fst h, congrArg Prod.snd h⟩,
        fun h => Prod.ext h.1 h.2⟩
  | succ n ih =>
      constructor
      · rintro ⟨w, hstep, htail⟩
        have hs := (strong_step K L u w).mp hstep
        have ht := (ih w v).mp htail
        exact ⟨⟨w.1, hs.1, ht.1⟩, ⟨w.2, hs.2, ht.2⟩⟩
      · rintro ⟨⟨a, hsa, hta⟩, ⟨b, hsb, htb⟩⟩
        refine ⟨(a, b), (strong_step K L u (a, b)).mpr ⟨hsa, hsb⟩, ?_⟩
        exact (ih (a, b) v).mpr ⟨hta, htb⟩

def WalkPacking {α : Type*} (K : SimpleGraph α) (S : Set α) : Prop :=
  ∀ u, u ∈ S → ∀ v, v ∈ S → u ≠ v →
    ¬ ∃ p : K.Walk u v, p.length ≤ 3

def WalkCovers2 {α : Type*} (K : SimpleGraph α) (S : Set α) : Prop :=
  ∀ u, ∃ c, c ∈ S ∧ ∃ p : K.Walk u c, p.length ≤ 2

/-! Q6 is the actual graph with one-bit-flip edges. -/

def G : SimpleGraph Vertex where
  Adj a b := hdist a b = 1
  symm.symm a b h := (hdist_symm b a).trans h
  loopless.irrefl a h := by rw [hdist_self] at h; cases h

theorem G_reach_bound (n : Nat) (a b : Vertex) (h : Reach G n a b) :
    hdist a b ≤ n := by
  induction n generalizing a b with
  | zero => change a = b at h; subst b; rw [hdist_self]
  | succ n ih =>
      rcases h with ⟨w, hstep, htail⟩
      have ht := ih w b htail
      have hs : hdist a w ≤ 1 := by
        rcases hstep with heq | hadj
        · subst w; rw [hdist_self]; exact Nat.zero_le 1
        · exact Nat.le_of_eq hadj
      have htri := hdist_triangle a w b
      omega

theorem G_reach_of_bound (n : Nat) (a b : Vertex) (h : hdist a b ≤ n) :
    Reach G n a b := by
  induction n generalizing a b with
  | zero =>
      change a = b
      exact hdist_zero_eq a b (Nat.eq_zero_of_le_zero h)
  | succ n ih =>
      by_cases heq : a = b
      · subst b; exact reach_refl G (n + 1) a
      · have hn := nextVertex_spec a b heq
        refine ⟨nextVertex a b, Or.inr hn.1, ih (nextVertex a b) b ?_⟩
        omega

theorem G_reach_iff_hamming (n : Nat) (a b : Vertex) :
    Reach G n a b ↔ hdist a b ≤ n :=
  ⟨G_reach_bound n a b, G_reach_of_bound n a b⟩

/-- This now imports the all-nonlinear obstruction into genuine Q6 Walk semantics. -/
theorem factor_no_walk_cover :
    ¬ ∃ S : Set Vertex, WalkPacking G S ∧ WalkCovers2 G S := by
  rintro ⟨S, hp, hc⟩
  have hpCode : Packing S := by
    intro a ha b hb hab
    by_contra hnot
    have hsmall : hdist a b ≤ 3 := by omega
    exact hp a ha b hb hab ((reach_iff_walk G 3 a b).mp
      (G_reach_of_bound 3 a b hsmall))
  have hcCode : Covers2 S := by
    intro a
    rcases hc a with ⟨c, hcS, p, hp⟩
    exact ⟨c, hcS, G_reach_bound 2 a c (walk_to_reach G p 2 hp)⟩
  exact no_packing_cover S hpCode hcCode

/-! Canonical unordered pairs: 64+64+480 actual nodes, not doubled labels. -/

abbrev PairLabel := {p : Vertex × Vertex // p.1.toNat < p.2.toNat ∧ hdist p.1 p.2 = 4}
abbrev Steiner := Sum Vertex PairLabel
abbrev HNode := Sum Vertex Steiner

private def vertexEquivFin : Vertex ≃ Fin 64 where
  toFun x := x.toFin
  invFun x := BitVec.ofFin x
  left_inv _ := rfl
  right_inv _ := rfl

local instance vertexFintype : Fintype Vertex :=
  Fintype.ofEquiv (Fin 64) vertexEquivFin.symm

local instance pairFintype : Fintype PairLabel := inferInstance
local instance steinerFintype : Fintype Steiner := inferInstance
local instance nodeFintype : Fintype HNode := inferInstance

theorem pair_card : Fintype.card PairLabel = 480 := by decide
theorem node_card : Fintype.card HNode = 608 := by
  have hv : Fintype.card Vertex = 64 := by decide
  simp only [HNode, Steiner, Fintype.card_sum, hv, pair_card]

def A (a : Vertex) : HNode := Sum.inl a
def T (s : Steiner) : HNode := Sum.inr s
def singleton (a : Vertex) : Steiner := Sum.inl a
def pair (p : PairLabel) : Steiner := Sum.inr p

def Support : Steiner → Vertex → Prop
  | Sum.inl a, b => b = a
  | Sum.inr p, b => b = p.val.1 ∨ b = p.val.2

def Compatible (s t : Steiner) : Prop :=
  ∀ a b, (Support s a ∨ Support t a) → (Support s b ∨ Support t b) →
    a ≠ b → 4 ≤ hdist a b

theorem support_separated (s : Steiner) (a b : Vertex)
    (ha : Support s a) (hb : Support s b) (hab : a ≠ b) : 4 ≤ hdist a b := by
  cases s with
  | inl c =>
      change a = c at ha
      change b = c at hb
      exact False.elim (hab (ha.trans hb.symm))
  | inr p =>
      rcases ha with rfl | rfl <;> rcases hb with rfl | rfl
      · exact False.elim (hab rfl)
      · exact Nat.le_of_eq p.property.2.symm
      · rw [hdist_symm]
        exact Nat.le_of_eq p.property.2.symm
      · exact False.elim (hab rfl)

theorem compatible_symm {s t : Steiner} (h : Compatible s t) : Compatible t s := by
  intro a b ha hb hab
  exact h a b (ha.elim Or.inr Or.inl) (hb.elim Or.inr Or.inl) hab

def HAdj : HNode → HNode → Prop
  | Sum.inl _, Sum.inl _ => False
  | Sum.inl a, Sum.inr s => Support s a
  | Sum.inr s, Sum.inl a => Support s a
  | Sum.inr s, Sum.inr t => s ≠ t ∧ Compatible s t

def H : SimpleGraph HNode where
  Adj := HAdj
  symm.symm u v h := by
    cases u with
    | inl a => cases v with
      | inl b => exact h
      | inr s => exact h
    | inr s => cases v with
      | inl a => exact h
      | inr t => exact ⟨Ne.symm h.1, compatible_symm h.2⟩
  loopless.irrefl u h := by
    cases u with
    | inl a => exact h
    | inr s => exact h.1 rfl

theorem H_two_step_centers (a b : Vertex) (u : HNode)
    (ha : Step H (A a) u) (hb : Step H u (A b)) :
    a = b ∨ 4 ≤ hdist a b := by
  cases u with
  | inl c =>
      have hac : a = c := by
        rcases ha with heq | hfalse
        · exact Sum.inl.inj heq
        · exact False.elim hfalse
      have hcb : c = b := by
        rcases hb with heq | hfalse
        · exact Sum.inl.inj heq
        · exact False.elim hfalse
      exact Or.inl (hac.trans hcb)
  | inr s =>
      have hasa : Support s a := by
        rcases ha with heq | hadj
        · cases heq
        · exact hadj
      have hasb : Support s b := by
        rcases hb with heq | hadj
        · cases heq
        · exact hadj
      by_cases hab : a = b
      · exact Or.inl hab
      · exact Or.inr (support_separated s a b hasa hasb hab)

/-- An actual H-walk of length at most three cannot connect incompatible A labels. -/
theorem H_short_centers (a b : Vertex) (hr : Reach H 3 (A a) (A b)) :
    a = b ∨ 4 ≤ hdist a b := by
  rcases hr with ⟨u, hau, v, huv, w, hvw, hwb⟩
  change w = A b at hwb
  subst w
  rcases hau with heq | hau
  · subst u
    exact H_two_step_centers a b v huv hvw
  · rcases hvw with heq | hvb
    · subst v
      exact H_two_step_centers a b u (Or.inr hau) huv
    · cases u with
      | inl c => exact False.elim hau
      | inr s => cases v with
        | inl c => exact False.elim hvb
        | inr t =>
            have ha : Support s a := hau
            have hb : Support t b := hvb
            by_cases hab : a = b
            · exact Or.inl hab
            · apply Or.inr
              rcases huv with heq | hadj
              · have hst : s = t := Sum.inr.inj heq
                subst t
                exact support_separated s a b ha hb hab
              · exact hadj.2 a b (Or.inl ha) (Or.inr hb) hab

theorem compatible_singleton (s : Steiner) (c : Vertex)
    (hfar : ∀ a, Support s a → 4 ≤ hdist a c) : Compatible s (singleton c) := by
  intro a b ha hb hab
  rcases ha with ha | ha <;> rcases hb with hb | hb
  · exact support_separated s a b ha hb hab
  · change b = c at hb
    subst b
    exact hfar a ha
  · change a = c at ha
    subst a
    rw [hdist_symm]
    exact hfar b hb
  · change a = c at ha
    change b = c at hb
    exact False.elim (hab (ha.trans hb.symm))

theorem H_to_singleton_edge (s : Steiner) (c : Vertex)
    (hfar : ∀ a, Support s a → 4 ≤ hdist a c) : H.Adj (T s) (T (singleton c)) := by
  refine ⟨?_, compatible_singleton s c hfar⟩
  intro heq
  have hm : Support s c := by rw [heq]; rfl
  have hc := hfar c hm
  rw [hdist_self] at hc
  omega

theorem canonical_pair (a b : Vertex) (hab : hdist a b = 4) :
    ∃ p : PairLabel, Support (pair p) a ∧ Support (pair p) b := by
  have hne : a ≠ b := by intro heq; subst b; rw [hdist_self] at hab; cases hab
  by_cases hlt : a.toNat < b.toNat
  · exact ⟨⟨(a, b), hlt, hab⟩, Or.inl rfl, Or.inr rfl⟩
  · have hlt' : b.toNat < a.toNat := by
      have hnat : a.toNat ≠ b.toNat := by
        intro heq
        exact hne (BitVec.eq_of_toNat_eq heq)
      omega
    exact ⟨⟨(b, a), hlt', (hdist_symm b a).trans hab⟩,
      Or.inr rfl, Or.inl rfl⟩

theorem reach_two_edges {α : Type*} (K : SimpleGraph α) {u v w : α}
    (huv : K.Adj u v) (hvw : K.Adj v w) : Reach K 2 u w :=
  ⟨v, Or.inr huv, w, Or.inr hvw, rfl⟩

theorem reach_one_padded {α : Type*} (K : SimpleGraph α) {u v : α}
    (huv : K.Adj u v) : Reach K 2 u v :=
  ⟨v, Or.inr huv, v, Or.inl rfl, rfl⟩

/-- The label is selected once and covers both coordinates simultaneously. -/
theorem H_same_center_cover (x : Vertex) (h : HNode) :
    ∃ c : Vertex, hdist x c ≤ 2 ∧ Reach H 2 h (A c) := by
  cases h with
  | inl a =>
      rcases single_cover a x with ⟨c, hc, hx⟩
      refine ⟨c, hx, ?_⟩
      rcases hc with hca | hac
      · subst c; exact reach_refl H 2 (A a)
      · rcases canonical_pair a c hac with ⟨p, hpa, hpc⟩
        exact reach_two_edges H (u := A a) (v := T (pair p)) (w := A c) hpa hpc
  | inr s => cases s with
    | inl a =>
        rcases single_cover a x with ⟨c, hc, hx⟩
        refine ⟨c, hx, ?_⟩
        rcases hc with hca | hac
        · subst c
          exact reach_one_padded H (u := T (singleton a)) (v := A a) rfl
        · have hfar : ∀ b, Support (singleton a) b → 4 ≤ hdist b c := by
            intro b hb; change b = a at hb; subst b; exact Nat.le_of_eq hac.symm
          exact reach_two_edges H (H_to_singleton_edge (singleton a) c hfar)
            (show H.Adj (T (singleton c)) (A c) from rfl)
    | inr p =>
        rcases pair_cover p.val.1 p.val.2 x p.property.2 with ⟨c, hc, hx⟩
        refine ⟨c, hx, ?_⟩
        rcases hc with hca | hcb | hcommon
        · subst c
          exact reach_one_padded H (u := T (pair p)) (v := A p.val.1) (Or.inl rfl)
        · subst c
          exact reach_one_padded H (u := T (pair p)) (v := A p.val.2) (Or.inr rfl)
        · have hfar : ∀ b, Support (pair p) b → 4 ≤ hdist b c := by
            intro b hb
            rcases hb with rfl | rfl
            · exact hcommon.1
            · exact hcommon.2
          exact reach_two_edges H (H_to_singleton_edge (pair p) c hfar)
            (show H.Adj (T (singleton c)) (A c) from rfl)

def ProductGraph : SimpleGraph (Vertex × HNode) := strong G H
def centerSet : Set (Vertex × HNode) := {z | ∃ a : Vertex, z = (a, A a)}

theorem product_walk_packing : WalkPacking ProductGraph centerSet := by
  rintro u ⟨a, rfl⟩ v ⟨b, rfl⟩ hne ⟨p, hp⟩
  have hr := walk_to_reach ProductGraph p 3 hp
  have hcoords := (strong_reach G H 3 (a, A a) (b, A b)).mp hr
  have hsmall := G_reach_bound 3 a b hcoords.1
  rcases H_short_centers a b hcoords.2 with heq | hlarge
  · subst b; exact hne rfl
  · omega

theorem product_walk_cover : WalkCovers2 ProductGraph centerSet := by
  rintro ⟨x, h⟩
  rcases H_same_center_cover x h with ⟨c, hxc, hhc⟩
  refine ⟨(c, A c), ⟨c, rfl⟩, ?_⟩
  apply (reach_iff_walk ProductGraph 2 (x, h) (c, A c)).mp
  exact (strong_reach G H 2 (x, h) (c, A c)).mpr
    ⟨G_reach_of_bound 2 x c hxc, hhc⟩

/-- Exact existence-level counterexample, on actual finite simple graphs and actual Walks. -/
theorem original_existence_counterexample :
    (¬ ∃ S : Set Vertex, WalkPacking G S ∧ WalkCovers2 G S) ∧
    (∃ S : Set (Vertex × HNode),
      WalkPacking ProductGraph S ∧ WalkCovers2 ProductGraph S) :=
  ⟨factor_no_walk_cover, centerSet, product_walk_packing, product_walk_cover⟩

#print axioms reach_refl
#print axioms reach_to_walk
#print axioms walk_to_reach
#print axioms reach_iff_walk
#print axioms strong_adj_standard
#print axioms strong_step
#print axioms strong_reach
#print axioms G_reach_bound
#print axioms G_reach_of_bound
#print axioms G_reach_iff_hamming
#print axioms factor_no_walk_cover
#print axioms pair_card
#print axioms node_card
#print axioms support_separated
#print axioms compatible_symm
#print axioms H_two_step_centers
#print axioms H_short_centers
#print axioms compatible_singleton
#print axioms H_to_singleton_edge
#print axioms canonical_pair
#print axioms reach_two_edges
#print axioms reach_one_padded
#print axioms H_same_center_cover
#print axioms product_walk_packing
#print axioms product_walk_cover
#print axioms original_existence_counterexample

end Q6PackingComplexCounterexample
