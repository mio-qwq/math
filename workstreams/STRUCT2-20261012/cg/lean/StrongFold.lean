import Std

/-!
The classical strong-fold construction for an arbitrary bipartite graph.
This is a semantic prerequisite for the CG classification, not a formal
proof of the all-parameter CG automorphism group. No finiteness assumption,
graph catalogue, precomputed involution list, or new axiom is used.
-/

set_option Elab.async false

namespace Struct2.StrongFold

structure BipGraph (V : Type) where
  adj : V → V → Prop
  symmetric : ∀ x y, adj x y → adj y x
  loopless : ∀ x, ¬ adj x x
  colour : V → Bool
  opposite : ∀ x y, adj x y → colour x ≠ colour y

structure Switch {V : Type} (G : BipGraph V) where
  map : V → V
  involutive : ∀ x, map (map x) = x
  preserves : ∀ x y, G.adj (map x) (map y) ↔ G.adj x y
  reverses : ∀ x, G.colour (map x) = !G.colour x
  nonadjacent : ∀ x, ¬ G.adj x (map x)

structure GraphIso {V W : Type} (A : V → V → Prop) (B : W → W → Prop) where
  forward : V → W
  backward : W → V
  left_inv : ∀ x, backward (forward x) = x
  right_inv : ∀ y, forward (backward y) = y
  preserves : ∀ x y, B (forward x) (forward y) ↔ A x y

variable {V : Type} (G : BipGraph V) (s : Switch G)

abbrev Base := {v : V // G.colour v = false}

def representative (x : V) : Base G :=
  if h : G.colour x = false then ⟨x, h⟩
  else ⟨s.map x, by
    rw [s.reverses]
    cases hc : G.colour x <;> simp_all⟩

def decode (x : Base G × Bool) : V :=
  if x.2 then s.map x.1.val else x.1.val

def encode (x : V) : Base G × Bool :=
  (representative G s x, G.colour x)

theorem representative_base (x : Base G) :
    representative G s x.val = x := by
  apply Subtype.ext
  simp [representative, x.property]

theorem representative_switch (x : V) :
    representative G s (s.map x) = representative G s x := by
  apply Subtype.ext
  cases h : G.colour x <;>
    simp [representative, h, s.reverses, s.involutive]

theorem colour_decode (x : Base G × Bool) :
    G.colour (decode G s x) = x.2 := by
  rcases x with ⟨x, b⟩
  cases b <;> simp [decode, s.reverses, x.property]

theorem decode_encode (x : V) : decode G s (encode G s x) = x := by
  cases h : G.colour x <;>
    simp [encode, decode, representative, h, s.involutive]

theorem encode_decode (x : Base G × Bool) : encode G s (decode G s x) = x := by
  rcases x with ⟨x, b⟩
  apply Prod.ext
  · cases b <;>
      simp [encode, decode, representative_switch, representative_base]
  · exact colour_decode G s (x, b)

def foldAdj (x y : Base G) : Prop := G.adj x.val (s.map y.val)

theorem switch_adj (x y : V) :
    G.adj (s.map x) y ↔ G.adj x (s.map y) := by
  simpa only [s.involutive] using s.preserves x (s.map y)

theorem fold_symmetric (x y : Base G) : foldAdj G s x y → foldAdj G s y x := by
  intro h
  exact (switch_adj G s y.val x.val).mp (G.symmetric _ _ h)

theorem fold_loopless (x : Base G) : ¬ foldAdj G s x x :=
  s.nonadjacent x.val

def cdcAdj (x y : Base G × Bool) : Prop :=
  x.2 ≠ y.2 ∧ foldAdj G s x.1 y.1

theorem decode_adjacency (x y : Base G × Bool) :
    G.adj (decode G s x) (decode G s y) ↔ cdcAdj G s x y := by
  rcases x with ⟨x, b⟩
  rcases y with ⟨y, c⟩
  cases b <;> cases c
  · simp only [decode, Bool.false_eq_true, ↓reduceIte, cdcAdj,
      ne_eq, not_true_eq_false, false_and, iff_false]
    intro h
    exact G.opposite _ _ h (x.property.trans y.property.symm)
  · simp [decode, cdcAdj, foldAdj]
  · simpa [decode, cdcAdj, foldAdj] using switch_adj G s x.val y.val
  · simp only [decode, ↓reduceIte, cdcAdj, ne_eq, not_true_eq_false,
      false_and, iff_false]
    intro h
    exact G.opposite _ _ h (by simp [s.reverses, x.property, y.property])

def foldDoubleCoverIso : GraphIso G.adj (cdcAdj G s) where
  forward := encode G s
  backward := decode G s
  left_inv := decode_encode G s
  right_inv := encode_decode G s
  preserves := by
    intro x y
    simpa only [decode_encode] using
      (decode_adjacency G s (encode G s x) (encode G s y)).symm

def deck (x : Base G × Bool) : Base G × Bool := (x.1, !x.2)

theorem encode_switch (x : V) :
    encode G s (s.map x) = deck G (encode G s x) := by
  apply Prod.ext
  · exact representative_switch G s x
  · exact s.reverses x

theorem decode_deck (x : Base G × Bool) :
    decode G s (deck G x) = s.map (decode G s x) := by
  rcases x with ⟨x, b⟩
  cases b <;> simp [deck, decode, s.involutive]

variable (t : Switch G)

def liftForward (h : GraphIso (foldAdj G s) (foldAdj G t)) (x : V) : V :=
  decode G t (h.forward (representative G s x), G.colour x)

def liftBackward (h : GraphIso (foldAdj G s) (foldAdj G t)) (x : V) : V :=
  decode G s (h.backward (representative G t x), G.colour x)

theorem lift_forward_colour (h : GraphIso (foldAdj G s) (foldAdj G t)) (x : V) :
    G.colour (liftForward G s t h x) = G.colour x :=
  colour_decode G t _

theorem lift_conjugates (h : GraphIso (foldAdj G s) (foldAdj G t)) (x : V) :
    liftForward G s t h (s.map x) = t.map (liftForward G s t h x) := by
  unfold liftForward
  rw [representative_switch, s.reverses]
  exact decode_deck G t (h.forward (representative G s x), G.colour x)

theorem representative_decode (x : Base G × Bool) :
    representative G s (decode G s x) = x.1 := by
  exact congrArg Prod.fst (encode_decode G s x)

def liftFoldIso (h : GraphIso (foldAdj G s) (foldAdj G t)) :
    GraphIso G.adj G.adj where
  forward := liftForward G s t h
  backward := liftBackward G s t h
  left_inv := by
    intro x
    simp only [liftForward, liftBackward, representative_decode,
      colour_decode, h.left_inv]
    exact decode_encode G s x
  right_inv := by
    intro x
    simp only [liftForward, liftBackward, representative_decode,
      colour_decode, h.right_inv]
    exact decode_encode G t x
  preserves := by
    intro x y
    rw [liftForward, liftForward, decode_adjacency]
    change (G.colour x ≠ G.colour y ∧
      foldAdj G t (h.forward (representative G s x))
        (h.forward (representative G s y))) ↔ G.adj x y
    rw [h.preserves]
    exact (foldDoubleCoverIso G s).preserves x y

/- Every isomorphism between the actual folds has now been lifted to an
   actual original-graph automorphism conjugating the two guides. -/
theorem fold_iso_has_conjugating_automorphism
    (h : GraphIso (foldAdj G s) (foldAdj G t)) :
    ∃ a : GraphIso G.adj G.adj,
      (∀ x, G.colour (a.forward x) = G.colour x) ∧
      (∀ x, a.forward (s.map x) = t.map (a.forward x)) :=
  ⟨liftFoldIso G s t h, lift_forward_colour G s t h, lift_conjugates G s t h⟩

def restrictConjugator (a : GraphIso G.adj G.adj)
    (hc : ∀ x, G.colour (a.forward x) = G.colour x)
    (hg : ∀ x, a.forward (s.map x) = t.map (a.forward x)) :
    GraphIso (foldAdj G s) (foldAdj G t) where
  forward := fun x => ⟨a.forward x.val, (hc x.val).trans x.property⟩
  backward := fun x => ⟨a.backward x.val, by
    have h := hc (a.backward x.val)
    rw [a.right_inv] at h
    exact h.symm.trans x.property⟩
  left_inv := by
    intro x
    apply Subtype.ext
    exact a.left_inv x.val
  right_inv := by
    intro x
    apply Subtype.ext
    exact a.right_inv x.val
  preserves := by
    intro x y
    change G.adj (a.forward x.val) (t.map (a.forward y.val)) ↔
      G.adj x.val (s.map y.val)
    rw [← hg]
    exact a.preserves x.val (s.map y.val)

inductive Walk : V → V → Prop where
  | refl (x : V) : Walk x x
  | step {x y z : V} : G.adj x y → Walk y z → Walk x z

theorem colour_agreement_edge (a : GraphIso G.adj G.adj)
    {x y : V} (h : G.adj x y) :
    (G.colour (a.forward x) = G.colour x) ↔
      (G.colour (a.forward y) = G.colour y) := by
  have hxy := G.opposite x y h
  have haxay := G.opposite _ _ ((a.preserves x y).mpr h)
  cases hx : G.colour x <;> cases hy : G.colour y <;>
    cases hax : G.colour (a.forward x) <;> cases hay : G.colour (a.forward y) <;>
    simp_all

theorem colour_agreement_walk (a : GraphIso G.adj G.adj)
    {x y : V} (h : Walk G x y) :
    (G.colour (a.forward x) = G.colour x) ↔
      (G.colour (a.forward y) = G.colour y) := by
  induction h with
  | refl => exact Iff.rfl
  | step hedge _ ih => exact (colour_agreement_edge G a hedge).trans ih

theorem automorphism_colour_uniform (root : V)
    (connected : ∀ x y, Walk G x y) (a : GraphIso G.adj G.adj) :
    (∀ x, G.colour (a.forward x) = G.colour x) ∨
      (∀ x, G.colour (a.forward x) = !G.colour x) := by
  by_cases h : G.colour (a.forward root) = G.colour root
  · left
    intro x
    exact (colour_agreement_walk G a (connected root x)).mp h
  · right
    intro x
    have hx : G.colour (a.forward x) ≠ G.colour x := by
      intro hx
      exact h ((colour_agreement_walk G a (connected root x)).mpr hx)
    cases hcx : G.colour x <;> cases hcax : G.colour (a.forward x) <;> simp_all

def switchAfter (a : GraphIso G.adj G.adj) : GraphIso G.adj G.adj where
  forward := fun x => t.map (a.forward x)
  backward := fun x => a.backward (t.map x)
  left_inv := by
    intro x
    rw [t.involutive, a.left_inv]
  right_inv := by
    intro x
    rw [a.right_inv, t.involutive]
  preserves := by
    intro x y
    exact (t.preserves _ _).trans (a.preserves x y)

/- The connected bipartition is derived through walks. A part-reversing
   conjugator is composed with the target guide to obtain a preserving one.
   Thus this final equivalence uses the entire automorphism group. -/
theorem folds_isomorphic_iff_conjugate (root : V)
    (connected : ∀ x y, Walk G x y) :
    Nonempty (GraphIso (foldAdj G s) (foldAdj G t)) ↔
      ∃ a : GraphIso G.adj G.adj,
        ∀ x, a.forward (s.map x) = t.map (a.forward x) := by
  constructor
  · rintro ⟨h⟩
    exact ⟨liftFoldIso G s t h, lift_conjugates G s t h⟩
  · rintro ⟨a, ha⟩
    rcases automorphism_colour_uniform G root connected a with hc | hc
    · exact ⟨restrictConjugator G s t a hc ha⟩
    · refine ⟨restrictConjugator G s t (switchAfter G t a) ?_ ?_⟩
      · intro x
        change G.colour (t.map (a.forward x)) = G.colour x
        rw [t.reverses, hc]
        cases G.colour x <;> rfl
      · intro x
        change t.map (a.forward (s.map x)) = t.map (t.map (a.forward x))
        rw [ha]

#print axioms fold_symmetric
#print axioms fold_loopless
#print axioms decode_adjacency
#print axioms foldDoubleCoverIso
#print axioms encode_switch
#print axioms decode_deck
#print axioms liftFoldIso
#print axioms fold_iso_has_conjugating_automorphism
#print axioms restrictConjugator
#print axioms automorphism_colour_uniform
#print axioms folds_isomorphic_iff_conjugate

end Struct2.StrongFold
