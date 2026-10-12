import OddCoverIso

/-!
The synchronized all-odd model is an actual connected bipartite graph.
Its original deck is an actual strong switch. The classical fold/conjugacy
theorem is instantiated on this original-defined model, not an assumed
group or finite catalogue. No complete automorphism classification is made.
-/

set_option Elab.async false
set_option maxHeartbeats 4000000

namespace Struct2.ModelStructure

open OddCoordinates StrongFold

theorem cycleNext_ne (m : Nat) (a : Fin (m + m)) : cycleNext m a ≠ a := by
  intro h
  have hv := congrArg Fin.val h
  unfold cycleNext at hv
  split at hv <;> dsimp at * <;> omega

theorem baseAdj_symmetric (n : Nat) (x y : Base n) :
    baseAdj n x y ↔ baseAdj n y x := by
  cases x <;> cases y <;> simp [baseAdj, ringAdj, or_comm, eq_comm]

theorem baseAdj_loopless (n : Nat) (x : Base n) : ¬ baseAdj n x x := by
  cases x with
  | ring t =>
    intro h
    rcases h with h | h <;> exact cycleNext_ne (3 * n) t h
  | leaf a => simp [baseAdj]
  | centre c => simp [baseAdj]

theorem coverAdj_symmetric (n : Nat) (x y : Cover n) :
    coverAdj n x y → coverAdj n y x := by
  intro h
  exact ⟨Ne.symm h.1, (baseAdj_symmetric n x.1 y.1).mp h.2⟩

def modelGraph (n : Nat) (hn : n % 2 = 1) : BipGraph (Coord n) where
  adj := coordinateAdj n
  symmetric := by
    intro x y h
    exact (toCover_adjacency n hn y x).mp
      (coverAdj_symmetric n _ _ ((toCover_adjacency n hn x y).mpr h))
  loopless := by
    intro x h
    exact ((toCover_adjacency n hn x x).mpr h).1 rfl
  colour := fun x => (toCover n x).2
  opposite := by
    intro x y h
    exact ((toCover_adjacency n hn x y).mpr h).1

def actualCoverGraph (n : Nat) : BipGraph (Cover n) where
  adj := coverAdj n
  symmetric := coverAdj_symmetric n
  loopless := by
    intro x h
    exact h.1 rfl
  colour := Prod.snd
  opposite := by
    intro x y h
    exact h.1

def originalLayerDeck (n : Nat) : Switch (actualCoverGraph n) where
  map := OddCoordinates.deck n
  involutive := by
    intro x
    rcases x with ⟨v, b⟩
    cases b <;> rfl
  preserves := by
    intro x y
    change coverAdj n (OddCoordinates.deck n x) (OddCoordinates.deck n y) ↔ coverAdj n x y
    unfold coverAdj OddCoordinates.deck
    cases x.2 <;> cases y.2 <;> simp
  reverses := by
    intro x
    rfl
  nonadjacent := by
    intro x h
    exact baseAdj_loopless n x.1 h.2

def originalFoldRecoversCG (n : Nat) :
    GraphIso (baseAdj n) (foldAdj (actualCoverGraph n) (originalLayerDeck n)) where
  forward := fun v => ⟨(v, false), rfl⟩
  backward := fun v => v.val.1
  left_inv := by
    intro v
    rfl
  right_inv := by
    rintro ⟨⟨v, b⟩, hb⟩
    apply Subtype.ext
    change b = false at hb
    subst b
    rfl
  preserves := by
    intro x y
    change (false ≠ true ∧ baseAdj n x y) ↔ baseAdj n x y
    simp

theorem coordinateDeck_involutive (n : Nat) (x : Coord n) :
    coordinateDeck n (coordinateDeck n x) = x := by
  cases x <;> simp [coordinateDeck, halfShift_involutive]

def originalStrongDeck (n : Nat) (hn : n % 2 = 1) : Switch (modelGraph n hn) where
  map := coordinateDeck n
  involutive := coordinateDeck_involutive n
  preserves := coordinateDeck_preserves n hn
  reverses := by
    intro x
    exact congrArg Prod.snd (coordinateDeck_intertwines n hn x)
  nonadjacent := by
    intro x h
    have hc := (toCover_adjacency n hn x (coordinateDeck n x)).mpr h
    rw [coordinateDeck_intertwines n hn x] at hc
    exact baseAdj_loopless n (toCover n x).1 hc.2

theorem walk_trans {V : Type} (G : BipGraph V) {x y z : V}
    (h : Walk G x y) (k : Walk G y z) : Walk G x z := by
  induction h with
  | refl => exact k
  | step he _ ih => exact .step he (ih k)

theorem walk_reverse {V : Type} (G : BipGraph V) {x y : V}
    (h : Walk G x y) : Walk G y x := by
  induction h with
  | refl => exact .refl _
  | step he _ ih =>
    exact walk_trans G ih (.step (G.symmetric _ _ he) (.refl _))

theorem transport_walk {V W : Type} (G : BipGraph V) (H : BipGraph W)
    (iso : GraphIso G.adj H.adj) {x y : V} (h : Walk G x y) :
    Walk H (iso.forward x) (iso.forward y) := by
  induction h with
  | refl => exact .refl _
  | step he _ ih => exact .step ((iso.preserves _ _).mpr he) ih

def modelRoot (n : Nat) (hn : n % 2 = 1) : Coord n :=
  .X ⟨0, by omega⟩

theorem ring_walk_to_root (n : Nat) (hn : n % 2 = 1)
    (t : Fin ((3 * n) + (3 * n))) :
    Walk (modelGraph n hn) (.X t) (modelRoot n hn) := by
  have paths : ∀ a (ha : a < (3 * n) + (3 * n)),
      Walk (modelGraph n hn) (.X ⟨a, ha⟩) (modelRoot n hn) := by
    intro a
    induction a with
    | zero =>
      intro ha
      exact .refl _
    | succ a ih =>
      intro ha
      have hp : a < (3 * n) + (3 * n) := by omega
      refine .step ?_ (ih hp)
      change ringAdj (3 * n) ⟨a + 1, ha⟩ ⟨a, hp⟩
      right
      apply Fin.ext
      simp [cycleNext, ha]
  exact paths t.val t.isLt

theorem model_walk_to_root (n : Nat) (hn : n % 2 = 1) (x : Coord n) :
    Walk (modelGraph n hn) x (modelRoot n hn) := by
  cases x with
  | X t => exact ring_walk_to_root n hn t
  | A t =>
    refine .step ?_ (ring_walk_to_root n hn t)
    exact rfl
  | Y t =>
    refine .step (y := .A t) ?_ (.step ?_ (ring_walk_to_root n hn t))
    · exact rfl
    · exact rfl
  | Z s =>
    let t : Fin ((3 * n) + (3 * n)) := ⟨s.val, by omega⟩
    have hs : centreResidue n t = s := by
      apply Fin.ext
      simp [centreResidue, t, s.isLt]
    refine .step (y := .A t) ?_ (.step ?_ (ring_walk_to_root n hn t))
    · exact hs.symm
    · exact rfl

theorem model_connected (n : Nat) (hn : n % 2 = 1) :
    ∀ x y : Coord n, Walk (modelGraph n hn) x y := by
  intro x y
  exact walk_trans (modelGraph n hn) (model_walk_to_root n hn x)
    (walk_reverse (modelGraph n hn) (model_walk_to_root n hn y))

theorem actualCDC_connected (n : Nat) (hn : n % 2 = 1) :
    ∀ x y : Cover n, Walk (actualCoverGraph n) x y := by
  intro x y
  have h := transport_walk (modelGraph n hn) (actualCoverGraph n)
    (OddCoverIso.originalCDCModelIso n hn)
    (model_connected n hn (fromCover n x) (fromCover n y))
  simpa only [OddCoverIso.originalCDCModelIso, toCover_fromCover n hn] using h

theorem model_folds_isomorphic_iff_conjugate (n : Nat) (hn : n % 2 = 1)
    (s t : Switch (modelGraph n hn)) :
    Nonempty (GraphIso (foldAdj (modelGraph n hn) s) (foldAdj (modelGraph n hn) t)) ↔
      ∃ a : GraphIso (modelGraph n hn).adj (modelGraph n hn).adj,
        ∀ x, a.forward (s.map x) = t.map (a.forward x) :=
  folds_isomorphic_iff_conjugate (modelGraph n hn) s t
    (modelRoot n hn) (model_connected n hn)

#print axioms baseAdj_symmetric
#print axioms baseAdj_loopless
#print axioms modelGraph
#print axioms actualCoverGraph
#print axioms originalLayerDeck
#print axioms originalFoldRecoversCG
#print axioms originalStrongDeck
#print axioms ring_walk_to_root
#print axioms model_walk_to_root
#print axioms model_connected
#print axioms transport_walk
#print axioms actualCDC_connected
#print axioms model_folds_isomorphic_iff_conjugate

end Struct2.ModelStructure
