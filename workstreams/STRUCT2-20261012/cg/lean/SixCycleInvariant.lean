import ModelStructure

/-!
Structural six-cycle lemmas for the actual synchronized CG cover model.
The universal proof uses symbolic adjacency and index arithmetic, not an
enumeration of fixed graph orders. The n=1 centre exception is retained.
-/

set_option Elab.async false
set_option maxHeartbeats 6000000
set_option maxRecDepth 20000

namespace Struct2.SixCycleInvariant

open OddCoordinates ModelStructure StrongFold

theorem cycleNext_injective (m : Nat) (a b : Fin (m + m))
    (h : cycleNext m a = cycleNext m b) : a = b := by
  apply Fin.ext
  have hv := congrArg Fin.val h
  unfold cycleNext at hv
  split at hv <;> split at hv <;> dsimp at * <;> omega

theorem cycleNext_twice_ne (m : Nat) (hm : 2 ≤ m) (a : Fin (m + m)) :
    cycleNext m (cycleNext m a) ≠ a := by
  intro h
  have hv := congrArg Fin.val h
  unfold cycleNext at hv
  all_goals try split at hv
  all_goals try dsimp at *
  all_goals try split at hv
  all_goals try dsimp at *
  all_goals try split at hv
  all_goals try dsimp at *
  all_goals omega

theorem centreResidue_cycleNext (n : Nat) (t : Fin ((3 * n) + (3 * n))) :
    centreResidue n (cycleNext (3 * n) t) = cycleNext n (centreResidue n t) := by
  apply Fin.ext
  have ht := t.isLt
  unfold centreResidue cycleNext
  all_goals try split
  all_goals try dsimp at *
  all_goals try split
  all_goals try dsimp at *
  all_goals try split
  all_goals try dsimp at *
  all_goals try split
  all_goals try dsimp at *
  all_goals try split
  all_goals try dsimp at *
  all_goals try split
  all_goals try dsimp at *
  all_goals try split
  all_goals try dsimp at *
  all_goals omega

theorem ring_two_steps (m : Nat) (p r q : Fin (m + m))
    (hpr : ringAdj m p r) (hrq : ringAdj m r q) :
    p = q ∨ cycleNext m (cycleNext m p) = q ∨ cycleNext m (cycleNext m q) = p := by
  rcases hpr with hpr | hpr <;> rcases hrq with hrq | hrq
  · exact Or.inr (Or.inl (by rw [hpr, hrq]))
  · exact Or.inl (cycleNext_injective m p q (hpr.trans hrq.symm))
  · exact Or.inl (hpr.symm.trans hrq)
  · exact Or.inr (Or.inr (by rw [hrq, hpr]))

theorem no_two_steps_same_centre (n : Nat) (hn : 2 ≤ n)
    (p r q : Fin ((3 * n) + (3 * n)))
    (hpq : p ≠ q) (hc : centreResidue n p = centreResidue n q)
    (hpr : ringAdj (3 * n) p r) (hrq : ringAdj (3 * n) r q) : False := by
  rcases ring_two_steps (3 * n) p r q hpr hrq with h | h | h
  · exact hpq h
  · have hi := congrArg (centreResidue n) h
    rw [centreResidue_cycleNext, centreResidue_cycleNext, ← hc] at hi
    exact cycleNext_twice_ne n hn (centreResidue n p) hi
  · have hi := congrArg (centreResidue n) h
    rw [centreResidue_cycleNext, centreResidue_cycleNext, hc] at hi
    exact cycleNext_twice_ne n hn (centreResidue n q) hi

def SixCycle {n : Nat} (v₀ v₁ v₂ v₃ v₄ v₅ : Coord n) : Prop :=
  [v₀, v₁, v₂, v₃, v₄, v₅].Nodup ∧
  coordinateAdj n v₀ v₁ ∧ coordinateAdj n v₁ v₂ ∧
  coordinateAdj n v₂ v₃ ∧ coordinateAdj n v₃ v₄ ∧
  coordinateAdj n v₄ v₅ ∧ coordinateAdj n v₅ v₀

def HasSixCycle {n : Nat} (v : Coord n) : Prop :=
  ∃ v₁ v₂ v₃ v₄ v₅ : Coord n, SixCycle v v₁ v₂ v₃ v₄ v₅

def IsCentre {n : Nat} : Coord n → Prop
  | .Z _ => True
  | _ => False

theorem coordinateAdj_symmetric (n : Nat) (x y : Coord n) :
    coordinateAdj n x y → coordinateAdj n y x := by
  cases x <;> cases y <;> simp [coordinateAdj, ringAdj, or_comm, eq_comm]

theorem centre_neighbour (n : Nat) (s : Fin (n + n)) (v : Coord n)
    (h : coordinateAdj n (.Z s) v) :
    ∃ p, v = .A p ∧ s = centreResidue n p := by
  cases v with
  | X p => exact False.elim h
  | Y p => exact False.elim h
  | A p => exact ⟨p, rfl, h⟩
  | Z p => exact False.elim h

theorem leaf_neighbour (n : Nat) (p : Fin ((3 * n) + (3 * n))) (v : Coord n)
    (h : coordinateAdj n (.A p) v) :
    v = .X p ∨ v = .Y p ∨ v = .Z (centreResidue n p) := by
  cases v with
  | X q => exact Or.inl (congrArg Coord.X h.symm)
  | Y q => exact Or.inr (Or.inl (congrArg Coord.Y h.symm))
  | A q => exact False.elim h
  | Z s => exact Or.inr (Or.inr (congrArg Coord.Z h.symm))

theorem no_six_cycle_at_centre (n : Nat) (hn : 2 ≤ n)
    (s : Fin (n + n)) (v₁ v₂ v₃ v₄ v₅ : Coord n) :
    ¬ SixCycle (.Z s) v₁ v₂ v₃ v₄ v₅ := by
  rintro ⟨hd, h01, h12, h23, h34, h45, h50⟩
  rcases centre_neighbour n s v₁ h01 with ⟨p, rfl, hp⟩
  rcases centre_neighbour n s v₅ (coordinateAdj_symmetric n _ _ h50) with ⟨q, rfl, hq⟩
  have hpq : p ≠ q := by
    intro he
    subst q
    simp at hd
  have hc : centreResidue n p = centreResidue n q := hp.symm.trans hq
  have hn₂ : v₂ ≠ .Z s := by
    intro he
    rw [he] at hd
    simp at hd
  have hn₄ : v₄ ≠ .Z s := by
    intro he
    rw [he] at hd
    simp at hd
  have hv₂ : v₂ = .X p ∨ v₂ = .Y p := by
    rcases leaf_neighbour n p v₂ h12 with h | h | h
    · exact Or.inl h
    · exact Or.inr h
    · exact False.elim (hn₂ (by simpa only [← hp] using h))
  have hv₄ : v₄ = .X q ∨ v₄ = .Y q := by
    rcases leaf_neighbour n q v₄ (coordinateAdj_symmetric n _ _ h45) with h | h | h
    · exact Or.inl h
    · exact Or.inr h
    · exact False.elim (hn₄ (by simpa only [← hq] using h))
  rcases hv₂ with h₂ | h₂ <;> rcases hv₄ with h₄ | h₄ <;> cases v₃ <;>
    simp only [h₂, h₄, coordinateAdj] at h23 h34
  all_goals first
    | exact hpq (h23.trans h34)
    | exact no_two_steps_same_centre n hn p _ q hpq hc h23 h34

theorem six_cycle_X (n : Nat) (t : Fin ((3 * n) + (3 * n))) :
    SixCycle (.X t) (.X (cycleNext (3 * n) t)) (.A (cycleNext (3 * n) t))
      (.Y (cycleNext (3 * n) t)) (.Y t) (.A t) := by
  have ht := cycleNext_ne (3 * n) t
  constructor
  · simp [ht, Ne.symm ht]
  · exact ⟨Or.inl rfl, rfl, rfl, Or.inr rfl, rfl, rfl⟩

theorem six_cycle_Y (n : Nat) (t : Fin ((3 * n) + (3 * n))) :
    SixCycle (.Y t) (.Y (cycleNext (3 * n) t)) (.A (cycleNext (3 * n) t))
      (.X (cycleNext (3 * n) t)) (.X t) (.A t) := by
  have ht := cycleNext_ne (3 * n) t
  constructor
  · simp [ht, Ne.symm ht]
  · exact ⟨Or.inl rfl, rfl, rfl, Or.inr rfl, rfl, rfl⟩

theorem six_cycle_A (n : Nat) (t : Fin ((3 * n) + (3 * n))) :
    SixCycle (.A t) (.X t) (.X (cycleNext (3 * n) t)) (.A (cycleNext (3 * n) t))
      (.Y (cycleNext (3 * n) t)) (.Y t) := by
  have ht := cycleNext_ne (3 * n) t
  constructor
  · simp [ht, Ne.symm ht]
  · exact ⟨rfl, Or.inl rfl, rfl, rfl, Or.inr rfl, rfl⟩

theorem has_six_cycle_iff_not_centre (n : Nat) (hn : 2 ≤ n) (v : Coord n) :
    HasSixCycle v ↔ ¬ IsCentre v := by
  cases v with
  | X t =>
    constructor
    · intro _
      simp [IsCentre]
    · intro _
      exact ⟨_, _, _, _, _, six_cycle_X n t⟩
  | Y t =>
    constructor
    · intro _
      simp [IsCentre]
    · intro _
      exact ⟨_, _, _, _, _, six_cycle_Y n t⟩
  | A t =>
    constructor
    · intro _
      simp [IsCentre]
    · intro _
      exact ⟨_, _, _, _, _, six_cycle_A n t⟩
  | Z s =>
    constructor
    · rintro ⟨v₁, v₂, v₃, v₄, v₅, h⟩
      exact False.elim (no_six_cycle_at_centre n hn s _ _ _ _ _ h)
    · intro h
      exact False.elim (h True.intro)

theorem nodup_map_of_injective {V W : Type} (f : V → W)
    (hf : ∀ x y, f x = f y → x = y) (l : List V) (h : l.Nodup) :
    (l.map f).Nodup := by
  induction l with
  | nil => simp
  | cons a l ih =>
    rcases List.nodup_cons.mp h with ⟨ha, hl⟩
    apply List.nodup_cons.mpr
    constructor
    · intro hm
      rcases List.mem_map.mp hm with ⟨b, hb, he⟩
      exact ha (by simpa only [hf b a he] using hb)
    · exact ih hl

theorem iso_forward_injective {V W : Type} {A : V → V → Prop} {B : W → W → Prop}
    (iso : GraphIso A B) (x y : V) (h : iso.forward x = iso.forward y) : x = y := by
  have hi := congrArg iso.backward h
  simpa only [iso.left_inv] using hi

def inverseIso {V W : Type} {A : V → V → Prop} {B : W → W → Prop}
    (iso : GraphIso A B) : GraphIso B A where
  forward := iso.backward
  backward := iso.forward
  left_inv := iso.right_inv
  right_inv := iso.left_inv
  preserves := by
    intro x y
    simpa only [iso.right_inv] using (iso.preserves (iso.backward x) (iso.backward y)).symm

theorem map_six_cycle (n : Nat) (iso : GraphIso (coordinateAdj n) (coordinateAdj n))
    (v₀ v₁ v₂ v₃ v₄ v₅ : Coord n) (h : SixCycle v₀ v₁ v₂ v₃ v₄ v₅) :
    SixCycle (iso.forward v₀) (iso.forward v₁) (iso.forward v₂)
      (iso.forward v₃) (iso.forward v₄) (iso.forward v₅) := by
  rcases h with ⟨hd, h01, h12, h23, h34, h45, h50⟩
  constructor
  · exact nodup_map_of_injective iso.forward (iso_forward_injective iso) _ hd
  · exact ⟨(iso.preserves _ _).mpr h01, (iso.preserves _ _).mpr h12,
      (iso.preserves _ _).mpr h23, (iso.preserves _ _).mpr h34,
      (iso.preserves _ _).mpr h45, (iso.preserves _ _).mpr h50⟩

theorem automorphism_preserves_six_cycle (n : Nat)
    (iso : GraphIso (coordinateAdj n) (coordinateAdj n)) (v : Coord n) :
    HasSixCycle (iso.forward v) ↔ HasSixCycle v := by
  constructor
  · rintro ⟨v₁, v₂, v₃, v₄, v₅, h⟩
    have hi := map_six_cycle n (inverseIso iso) _ _ _ _ _ _ h
    exact ⟨_, _, _, _, _, by simpa only [inverseIso, iso.left_inv] using hi⟩
  · rintro ⟨v₁, v₂, v₃, v₄, v₅, h⟩
    exact ⟨_, _, _, _, _, map_six_cycle n iso _ _ _ _ _ _ h⟩

theorem automorphism_preserves_centres (n : Nat) (hn : 2 ≤ n)
    (iso : GraphIso (coordinateAdj n) (coordinateAdj n)) (v : Coord n) :
    IsCentre (iso.forward v) ↔ IsCentre v := by
  have h := automorphism_preserves_six_cycle n iso v
  rw [has_six_cycle_iff_not_centre n hn, has_six_cycle_iff_not_centre n hn] at h
  have hd : ∀ w : Coord n, Decidable (IsCentre w) := by
    intro w
    cases w <;> dsimp [IsCentre] <;> infer_instance
  constructor <;> intro hc
  · by_cases hv : IsCentre v
    · exact hv
    · exact False.elim ((h.mpr hv) hc)
  · by_cases hv : IsCentre (iso.forward v)
    · exact hv
    · exact False.elim ((h.mp hv) hc)

def IsLeaf {n : Nat} : Coord n → Prop
  | .A _ => True
  | _ => False

def IsRing {n : Nat} : Coord n → Prop
  | .X _ => True
  | .Y _ => True
  | _ => False

theorem leaf_iff_adjacent_centre (n : Nat) (v : Coord n) :
    IsLeaf v ↔ ∃ z : Coord n, IsCentre z ∧ coordinateAdj n v z := by
  cases v with
  | X t =>
    constructor
    · intro h
      exact False.elim h
    · rintro ⟨z, hz, he⟩
      cases z <;> simp_all only [IsCentre, coordinateAdj]
  | Y t =>
    constructor
    · intro h
      exact False.elim h
    · rintro ⟨z, hz, he⟩
      cases z <;> simp_all only [IsCentre, coordinateAdj]
  | A t =>
    constructor
    · intro _
      exact ⟨.Z (centreResidue n t), True.intro, rfl⟩
    · intro _
      exact True.intro
  | Z s =>
    constructor
    · intro h
      exact False.elim h
    · rintro ⟨z, hz, he⟩
      cases z <;> simp_all only [IsCentre, coordinateAdj]

theorem map_leaf (n : Nat) (hn : 2 ≤ n)
    (iso : GraphIso (coordinateAdj n) (coordinateAdj n)) (v : Coord n)
    (h : IsLeaf v) : IsLeaf (iso.forward v) := by
  rcases (leaf_iff_adjacent_centre n v).mp h with ⟨z, hz, he⟩
  apply (leaf_iff_adjacent_centre n _).mpr
  exact ⟨iso.forward z, (automorphism_preserves_centres n hn iso z).mpr hz,
    (iso.preserves _ _).mpr he⟩

theorem automorphism_preserves_leaves (n : Nat) (hn : 2 ≤ n)
    (iso : GraphIso (coordinateAdj n) (coordinateAdj n)) (v : Coord n) :
    IsLeaf (iso.forward v) ↔ IsLeaf v := by
  constructor
  · intro h
    have hi := map_leaf n hn (inverseIso iso) (iso.forward v) h
    simpa only [inverseIso, iso.left_inv] using hi
  · exact map_leaf n hn iso v

theorem ring_iff_not_centre_not_leaf (n : Nat) (v : Coord n) :
    IsRing v ↔ ¬ IsCentre v ∧ ¬ IsLeaf v := by
  cases v <;> simp [IsRing, IsCentre, IsLeaf]

theorem automorphism_preserves_rings (n : Nat) (hn : 2 ≤ n)
    (iso : GraphIso (coordinateAdj n) (coordinateAdj n)) (v : Coord n) :
    IsRing (iso.forward v) ↔ IsRing v := by
  rw [ring_iff_not_centre_not_leaf n (iso.forward v),
    ring_iff_not_centre_not_leaf n v,
    automorphism_preserves_centres n hn iso v,
    automorphism_preserves_leaves n hn iso v]

def ActualSixCycle {n : Nat} (v₀ v₁ v₂ v₃ v₄ v₅ : Cover n) : Prop :=
  [v₀, v₁, v₂, v₃, v₄, v₅].Nodup ∧
  coverAdj n v₀ v₁ ∧ coverAdj n v₁ v₂ ∧ coverAdj n v₂ v₃ ∧
  coverAdj n v₃ v₄ ∧ coverAdj n v₄ v₅ ∧ coverAdj n v₅ v₀

def ActualHasSixCycle {n : Nat} (v : Cover n) : Prop :=
  ∃ v₁ v₂ v₃ v₄ v₅ : Cover n, ActualSixCycle v v₁ v₂ v₃ v₄ v₅

def IsOriginalCentre {n : Nat} : OddCoordinates.Base n → Prop
  | .centre _ => True
  | _ => False

theorem map_six_cycle_to_original (n : Nat) (hn : n % 2 = 1)
    (v₀ v₁ v₂ v₃ v₄ v₅ : Coord n) (h : SixCycle v₀ v₁ v₂ v₃ v₄ v₅) :
    ActualSixCycle (toCover n v₀) (toCover n v₁) (toCover n v₂)
      (toCover n v₃) (toCover n v₄) (toCover n v₅) := by
  rcases h with ⟨hd, h01, h12, h23, h34, h45, h50⟩
  constructor
  · exact nodup_map_of_injective (toCover n) (toCover_injective n hn) _ hd
  · exact ⟨(toCover_adjacency n hn _ _).mpr h01,
      (toCover_adjacency n hn _ _).mpr h12,
      (toCover_adjacency n hn _ _).mpr h23,
      (toCover_adjacency n hn _ _).mpr h34,
      (toCover_adjacency n hn _ _).mpr h45,
      (toCover_adjacency n hn _ _).mpr h50⟩

theorem actual_has_six_cycle_iff_model (n : Nat) (hn : n % 2 = 1) (v : Cover n) :
    ActualHasSixCycle v ↔ HasSixCycle (fromCover n v) := by
  let iso := inverseIso (OddCoverIso.originalCDCModelIso n hn)
  constructor
  · rintro ⟨v₁, v₂, v₃, v₄, v₅, hd, h01, h12, h23, h34, h45, h50⟩
    refine ⟨fromCover n v₁, fromCover n v₂, fromCover n v₃,
      fromCover n v₄, fromCover n v₅, ?_, ?_⟩
    · exact nodup_map_of_injective iso.forward (iso_forward_injective iso) _ hd
    · exact ⟨(iso.preserves _ _).mpr h01, (iso.preserves _ _).mpr h12,
        (iso.preserves _ _).mpr h23, (iso.preserves _ _).mpr h34,
        (iso.preserves _ _).mpr h45, (iso.preserves _ _).mpr h50⟩
  · rintro ⟨v₁, v₂, v₃, v₄, v₅, h⟩
    refine ⟨toCover n v₁, toCover n v₂, toCover n v₃,
      toCover n v₄, toCover n v₅, ?_⟩
    simpa only [toCover_fromCover n hn] using
      map_six_cycle_to_original n hn _ _ _ _ _ _ h

theorem fromCover_is_centre (n : Nat) (v : Cover n) :
    IsCentre (fromCover n v) ↔ IsOriginalCentre v.1 := by
  rcases v with ⟨v, b⟩
  cases v with
  | ring t =>
    change IsCentre (if b = bit t.val then .X t else .Y (halfShift (3 * n) t)) ↔ False
    split <;> rfl
  | leaf a => rfl
  | centre c => rfl

theorem actualCDC_six_cycle_characterization (n : Nat) (hn : n % 2 = 1)
    (hlarge : 3 ≤ n) (v : Cover n) :
    ActualHasSixCycle v ↔ ¬ IsOriginalCentre v.1 := by
  rw [actual_has_six_cycle_iff_model n hn,
    has_six_cycle_iff_not_centre n (by omega), fromCover_is_centre]

theorem n_one_centre_exception :
    SixCycle (n := 1) (.Z ⟨0, by decide⟩) (.A ⟨0, by decide⟩)
      (.X ⟨0, by decide⟩) (.X ⟨1, by decide⟩)
      (.X ⟨2, by decide⟩) (.A ⟨2, by decide⟩) := by
  unfold SixCycle coordinateAdj ringAdj
  decide +kernel

#print axioms cycleNext_injective
#print axioms cycleNext_twice_ne
#print axioms centreResidue_cycleNext
#print axioms no_two_steps_same_centre
#print axioms no_six_cycle_at_centre
#print axioms six_cycle_X
#print axioms six_cycle_Y
#print axioms six_cycle_A
#print axioms has_six_cycle_iff_not_centre
#print axioms nodup_map_of_injective
#print axioms map_six_cycle
#print axioms automorphism_preserves_six_cycle
#print axioms automorphism_preserves_centres
#print axioms leaf_iff_adjacent_centre
#print axioms automorphism_preserves_leaves
#print axioms automorphism_preserves_rings
#print axioms map_six_cycle_to_original
#print axioms actual_has_six_cycle_iff_model
#print axioms fromCover_is_centre
#print axioms actualCDC_six_cycle_characterization
#print axioms n_one_centre_exception

end Struct2.SixCycleInvariant
