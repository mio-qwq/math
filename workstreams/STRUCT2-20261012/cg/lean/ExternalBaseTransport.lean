import StrongConjugacy

/-!
Transport the deck of an arbitrary finite/simple-style canonical double cover
back to a connected bipartite graph, and recover the external base as the
resulting strong fold.  Finiteness is not needed for the construction.
-/

set_option Elab.async false
set_option maxHeartbeats 12000000
set_option maxRecDepth 20000

namespace Struct2.ExternalBaseTransport

open StrongFold SixCycleInvariant
open ModelStructure RingAction ModelActions StrongSwitchClassification StrongConjugacy

structure SimpleGraph (V : Type) where
  adj : V → V → Prop
  symmetric : ∀ x y, adj x y → adj y x
  loopless : ∀ x, ¬adj x x

def coverAdj {V : Type} (H : SimpleGraph V) (x y : V × Bool) : Prop :=
  x.2 ≠ y.2 ∧ H.adj x.1 y.1

def coverGraph {V : Type} (H : SimpleGraph V) : BipGraph (V × Bool) where
  adj := coverAdj H
  symmetric := by
    intro x y h
    exact ⟨Ne.symm h.1, H.symmetric _ _ h.2⟩
  loopless := by
    intro x h
    exact h.1 rfl
  colour := Prod.snd
  opposite := by
    intro x y h
    exact h.1

def coverDeck {V : Type} (x : V × Bool) : V × Bool := (x.1, !x.2)

theorem coverDeck_involutive {V : Type} (x : V × Bool) :
    coverDeck (coverDeck x) = x := by
  rcases x with ⟨v, b⟩
  cases b <;> rfl

theorem coverDeck_preserves {V : Type} (H : SimpleGraph V) (x y : V × Bool) :
    coverAdj H (coverDeck x) (coverDeck y) ↔ coverAdj H x y := by
  rcases x with ⟨x, b⟩
  rcases y with ⟨y, c⟩
  cases b <;> cases c <;> simp [coverAdj, coverDeck]

variable {W V : Type} (G : BipGraph W) (H : SimpleGraph V)

theorem iso_colour_agreement_edge
    (q : GraphIso G.adj (coverAdj H)) {x y : W} (h : G.adj x y) :
    ((coverGraph H).colour (q.forward x) = G.colour x) ↔
      ((coverGraph H).colour (q.forward y) = G.colour y) := by
  have hxy := G.opposite x y h
  have hqxqy := (coverGraph H).opposite _ _ ((q.preserves x y).mpr h)
  cases hx : G.colour x <;> cases hy : G.colour y <;>
    cases hqx : (coverGraph H).colour (q.forward x) <;>
    cases hqy : (coverGraph H).colour (q.forward y) <;> simp_all

theorem iso_colour_agreement_walk
    (q : GraphIso G.adj (coverAdj H)) {x y : W} (h : Walk G x y) :
    ((coverGraph H).colour (q.forward x) = G.colour x) ↔
      ((coverGraph H).colour (q.forward y) = G.colour y) := by
  induction h with
  | refl => exact Iff.rfl
  | step hedge _ ih => exact (iso_colour_agreement_edge G H q hedge).trans ih

def deckAfterIso (q : GraphIso G.adj (coverAdj H)) :
    GraphIso G.adj (coverAdj H) where
  forward := fun x => coverDeck (q.forward x)
  backward := fun y => q.backward (coverDeck y)
  left_inv := by
    intro x
    rw [coverDeck_involutive, q.left_inv]
  right_inv := by
    intro y
    rw [q.right_inv, coverDeck_involutive]
  preserves := by
    intro x y
    exact (coverDeck_preserves H _ _).trans (q.preserves x y)

theorem colour_preserving_cover_iso (root : W)
    (connected : ∀ x y, Walk G x y)
    (q : GraphIso G.adj (coverAdj H)) :
    ∃ p : GraphIso G.adj (coverAdj H),
      ∀ x, (coverGraph H).colour (p.forward x) = G.colour x := by
  by_cases hr : (coverGraph H).colour (q.forward root) = G.colour root
  · refine ⟨q, ?_⟩
    intro x
    exact (iso_colour_agreement_walk G H q (connected root x)).mp hr
  · refine ⟨deckAfterIso G H q, ?_⟩
    intro x
    have hx : (coverGraph H).colour (q.forward x) ≠ G.colour x := by
      intro he
      exact hr ((iso_colour_agreement_walk G H q (connected root x)).mpr he)
    change (q.forward x).2 ≠ G.colour x at hx
    change (!(q.forward x).2) = G.colour x
    cases hcx : G.colour x <;> cases hcq : (q.forward x).2 <;> simp_all

def transportedSwitch (q : GraphIso G.adj (coverAdj H))
    (hc : ∀ x, (coverGraph H).colour (q.forward x) = G.colour x) : Switch G where
  map := fun x => q.backward (coverDeck (q.forward x))
  involutive := by
    intro x
    rw [q.right_inv, coverDeck_involutive, q.left_inv]
  preserves := by
    intro x y
    calc
      G.adj (q.backward (coverDeck (q.forward x)))
          (q.backward (coverDeck (q.forward y))) ↔
          coverAdj H
            (q.forward (q.backward (coverDeck (q.forward x))))
            (q.forward (q.backward (coverDeck (q.forward y)))) :=
        (q.preserves _ _).symm
      _ ↔ coverAdj H (coverDeck (q.forward x)) (coverDeck (q.forward y)) := by
        rw [q.right_inv, q.right_inv]
      _ ↔ coverAdj H (q.forward x) (q.forward y) := coverDeck_preserves H _ _
      _ ↔ G.adj x y := q.preserves x y
  reverses := by
    intro x
    have h := hc (q.backward (coverDeck (q.forward x)))
    rw [q.right_inv] at h
    calc
      G.colour (q.backward (coverDeck (q.forward x))) =
          (coverDeck (q.forward x)).2 := h.symm
      _ = (!(q.forward x).2) := rfl
      _ = (!G.colour x) := congrArg Bool.not (hc x)
  nonadjacent := by
    intro x h
    have hq := (q.preserves x _).mpr h
    rw [q.right_inv] at hq
    exact H.loopless (q.forward x).1 hq.2

def externalBaseIso (q : GraphIso G.adj (coverAdj H))
    (hc : ∀ x, (coverGraph H).colour (q.forward x) = G.colour x) :
    GraphIso H.adj (foldAdj G (transportedSwitch G H q hc)) where
  forward := fun v => ⟨q.backward (v, false), by
    have h := hc (q.backward (v, false))
    rw [q.right_inv] at h
    exact h.symm⟩
  backward := fun x => (q.forward x.val).1
  left_inv := by
    intro v
    simp only [q.right_inv]
  right_inv := by
    intro x
    apply Subtype.ext
    change q.backward ((q.forward x.val).1, false) = x.val
    have hq : q.forward x.val = ((q.forward x.val).1, false) := by
      apply Prod.ext
      · rfl
      · have h := hc x.val
        rw [x.property] at h
        exact h
    rw [← hq, q.left_inv]
  preserves := by
    intro x y
    change G.adj (q.backward (x, false))
      (q.backward (coverDeck (q.forward (q.backward (y, false))))) ↔ H.adj x y
    rw [q.right_inv]
    calc
      G.adj (q.backward (x, false)) (q.backward (coverDeck (y, false))) ↔
          coverAdj H
            (q.forward (q.backward (x, false)))
            (q.forward (q.backward (coverDeck (y, false)))) :=
        (q.preserves _ _).symm
      _ ↔ coverAdj H (x, false) (coverDeck (y, false)) := by
        rw [q.right_inv, q.right_inv]
      _ ↔ H.adj x y := by simp [coverAdj, coverDeck]

theorem arbitrary_cover_recovers_base (root : W)
    (connected : ∀ x y, Walk G x y)
    (q : GraphIso G.adj (coverAdj H)) :
    ∃ s : Switch G, Nonempty (GraphIso H.adj (foldAdj G s)) := by
  rcases colour_preserving_cover_iso G H root connected q with ⟨p, hp⟩
  exact ⟨transportedSwitch G H p hp, ⟨externalBaseIso G H p hp⟩⟩

def composeIso {A B C : Type} {R : A → A → Prop} {S : B → B → Prop}
    {T : C → C → Prop} (f : GraphIso R S) (g : GraphIso S T) : GraphIso R T where
  forward := fun x => g.forward (f.forward x)
  backward := fun z => f.backward (g.backward z)
  left_inv := by intro x; rw [g.left_inv, f.left_inv]
  right_inv := by intro z; rw [f.right_inv, g.right_inv]
  preserves := by
    intro x y
    exact (g.preserves _ _).trans (f.preserves x y)

def switchModelAut (n : Nat) (hn : n % 2 = 1)
    (s : Switch (modelGraph n hn)) : ModelAut n where
  forward := s.map
  backward := s.map
  left_inv := s.involutive
  right_inv := s.involutive
  preserves := s.preserves

theorem switchModelAut_strong (n : Nat) (hn : n % 2 = 1)
    (s : Switch (modelGraph n hn)) : IsStrong n hn (switchModelAut n hn s) := by
  exact ⟨s.involutive, s.reverses, s.nonadjacent⟩

/- This closes the converse omitted by the earlier internal switch
classification: an entirely external simple graph whose canonical double
cover is the CG model is one of the three already classified folds. -/
theorem external_base_in_three_fold_classes (n : Nat) (hn : n % 2 = 1)
    (hn3 : 3 ≤ n) {V : Type} (H : SimpleGraph V)
    (q : GraphIso (modelGraph n hn).adj (coverAdj H)) :
    Nonempty (GraphIso H.adj
      (foldAdj (modelGraph n hn) (firstSwitch n hn hn3))) ∨
    Nonempty (GraphIso H.adj
      (foldAdj (modelGraph n hn) (secondSwitch n hn hn3))) ∨
    Nonempty (GraphIso H.adj
      (foldAdj (modelGraph n hn) (thirdSwitch n hn hn3))) := by
  rcases colour_preserving_cover_iso (modelGraph n hn) H (modelRoot n hn)
      (model_connected n hn) q with ⟨p, hp⟩
  let s := transportedSwitch (modelGraph n hn) H p hp
  let g := switchModelAut n hn s
  have hg : IsStrong n hn g := switchModelAut_strong n hn s
  have hext : GraphIso H.adj (foldAdj (modelGraph n hn) s) :=
    externalBaseIso (modelGraph n hn) H p hp
  rcases every_strong_fold_in_three_classes n hn hn3 g hg with hi | hi | hi
  · left
    rcases hi with ⟨hi⟩
    change GraphIso (foldAdj (modelGraph n hn) (firstSwitch n hn hn3))
      (foldAdj (modelGraph n hn) s) at hi
    exact ⟨composeIso hext (inverseIso hi)⟩
  · right; left
    rcases hi with ⟨hi⟩
    change GraphIso (foldAdj (modelGraph n hn) (secondSwitch n hn hn3))
      (foldAdj (modelGraph n hn) s) at hi
    exact ⟨composeIso hext (inverseIso hi)⟩
  · right; right
    rcases hi with ⟨hi⟩
    change GraphIso (foldAdj (modelGraph n hn) (thirdSwitch n hn hn3))
      (foldAdj (modelGraph n hn) s) at hi
    exact ⟨composeIso hext (inverseIso hi)⟩

#print axioms iso_colour_agreement_walk
#print axioms colour_preserving_cover_iso
#print axioms transportedSwitch
#print axioms externalBaseIso
#print axioms arbitrary_cover_recovers_base
#print axioms switchModelAut_strong
#print axioms external_base_in_three_fold_classes

end Struct2.ExternalBaseTransport
