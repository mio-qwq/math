import SixCycleInvariant

/-!
Restrict arbitrary actual model automorphisms to synchronized ring actions.
No type preservation, chosen dihedral group or completeness premise is assumed.
The six-cycle invariant supplies the type preservation used below.
-/

set_option Elab.async false
set_option maxHeartbeats 6000000

namespace Struct2.RingAction

open OddCoordinates ModelStructure SixCycleInvariant StrongFold

abbrev RingIndex (n : Nat) := Fin ((3 * n) + (3 * n))
abbrev ModelAut (n : Nat) := GraphIso (coordinateAdj n) (coordinateAdj n)

def leafImage (n : Nat) (iso : ModelAut n) (t : RingIndex n) : RingIndex n :=
  match iso.forward (.A t) with
  | .A u => u
  | _ => t

theorem leaf_forward (n : Nat) (hn : 2 ≤ n) (iso : ModelAut n) (t : RingIndex n) :
    iso.forward (.A t) = .A (leafImage n iso t) := by
  have h := (automorphism_preserves_leaves n hn iso (.A t)).mpr True.intro
  cases hv : iso.forward (.A t) with
  | X u => simp only [hv, IsLeaf] at h
  | Y u => simp only [hv, IsLeaf] at h
  | A u => simp only [leafImage, hv]
  | Z u => simp only [hv, IsLeaf] at h

theorem leafImage_injective (n : Nat) (hn : 2 ≤ n) (iso : ModelAut n)
    (t u : RingIndex n) (h : leafImage n iso t = leafImage n iso u) : t = u := by
  have hi : iso.forward (.A t) = iso.forward (.A u) := by
    rw [leaf_forward n hn iso t, leaf_forward n hn iso u, h]
  exact Coord.A.inj (iso_forward_injective iso _ _ hi)

theorem leafImage_left_inv (n : Nat) (hn : 2 ≤ n) (iso : ModelAut n) (t : RingIndex n) :
    leafImage n (inverseIso iso) (leafImage n iso t) = t := by
  have h := congrArg iso.backward (leaf_forward n hn iso t)
  rw [iso.left_inv] at h
  have hi := leaf_forward n hn (inverseIso iso) (leafImage n iso t)
  change iso.backward (.A (leafImage n iso t)) = _ at hi
  exact Coord.A.inj (hi.symm.trans h.symm)

theorem leafImage_right_inv (n : Nat) (hn : 2 ≤ n) (iso : ModelAut n) (t : RingIndex n) :
    leafImage n iso (leafImage n (inverseIso iso) t) = t := by
  have h := congrArg iso.forward (leaf_forward n hn (inverseIso iso) t)
  change iso.forward (iso.backward (.A t)) = _ at h
  rw [iso.right_inv] at h
  have hi := leaf_forward n hn iso (leafImage n (inverseIso iso) t)
  exact Coord.A.inj (hi.symm.trans h.symm)

theorem ring_neighbour_of_leaf (n : Nat) (p : RingIndex n) (v : Coord n)
    (hr : IsRing v) (he : coordinateAdj n v (.A p)) :
    v = .X p ∨ v = .Y p := by
  cases v with
  | X u => exact Or.inl (congrArg Coord.X he)
  | Y u => exact Or.inr (congrArg Coord.Y he)
  | A u => exact False.elim hr
  | Z u => exact False.elim hr

theorem image_X_shape (n : Nat) (hn : 2 ≤ n) (iso : ModelAut n) (t : RingIndex n) :
    iso.forward (.X t) = .X (leafImage n iso t) ∨
      iso.forward (.X t) = .Y (leafImage n iso t) := by
  have he := (iso.preserves (.X t) (.A t)).mpr rfl
  rw [leaf_forward n hn iso t] at he
  exact ring_neighbour_of_leaf n _ _
    ((automorphism_preserves_rings n hn iso (.X t)).mpr True.intro) he

theorem image_Y_shape (n : Nat) (hn : 2 ≤ n) (iso : ModelAut n) (t : RingIndex n) :
    iso.forward (.Y t) = .X (leafImage n iso t) ∨
      iso.forward (.Y t) = .Y (leafImage n iso t) := by
  have he := (iso.preserves (.Y t) (.A t)).mpr rfl
  rw [leaf_forward n hn iso t] at he
  exact ring_neighbour_of_leaf n _ _
    ((automorphism_preserves_rings n hn iso (.Y t)).mpr True.intro) he

def ringSwap (n : Nat) (iso : ModelAut n) (t : RingIndex n) : Bool :=
  match iso.forward (.X t) with
  | .Y _ => true
  | _ => false

theorem ring_X_forward (n : Nat) (hn : 2 ≤ n) (iso : ModelAut n) (t : RingIndex n) :
    iso.forward (.X t) =
      if ringSwap n iso t then .Y (leafImage n iso t) else .X (leafImage n iso t) := by
  rcases image_X_shape n hn iso t with h | h <;> simp only [ringSwap, h] <;> rfl

theorem ring_Y_forward (n : Nat) (hn : 2 ≤ n) (iso : ModelAut n) (t : RingIndex n) :
    iso.forward (.Y t) =
      if ringSwap n iso t then .X (leafImage n iso t) else .Y (leafImage n iso t) := by
  have hne : iso.forward (.X t) ≠ iso.forward (.Y t) := by
    intro h
    have hi := iso_forward_injective iso _ _ h
    cases hi
  rcases image_X_shape n hn iso t with hx | hx <;>
    rcases image_Y_shape n hn iso t with hy | hy
  · exact False.elim (hne (hx.trans hy.symm))
  · simp only [ringSwap, hx]
    exact hy
  · simp only [ringSwap, hx]
    exact hy
  · exact False.elim (hne (hx.trans hy.symm))

theorem ringSwap_successor (n : Nat) (hn : 2 ≤ n) (iso : ModelAut n) (t : RingIndex n) :
    ringSwap n iso (cycleNext (3 * n) t) = ringSwap n iso t := by
  have he := (iso.preserves (.X t) (.X (cycleNext (3 * n) t))).mpr (Or.inl rfl)
  rw [ring_X_forward n hn iso t, ring_X_forward n hn iso (cycleNext (3 * n) t)] at he
  cases hs : ringSwap n iso t <;> cases ht : ringSwap n iso (cycleNext (3 * n) t) <;>
    simp only [hs, ht, Bool.false_eq_true, ↓reduceIte, coordinateAdj] at he ⊢

def ringZero (n : Nat) (hn : 2 ≤ n) : RingIndex n := ⟨0, by omega⟩

theorem ringSwap_constant (n : Nat) (hn : 2 ≤ n) (iso : ModelAut n) (t : RingIndex n) :
    ringSwap n iso t = ringSwap n iso (ringZero n hn) := by
  have h : ∀ a (ha : a < (3 * n) + (3 * n)),
      ringSwap n iso ⟨a, ha⟩ = ringSwap n iso (ringZero n hn) := by
    intro a
    induction a with
    | zero =>
      intro ha
      rfl
    | succ a ih =>
      intro ha
      have hp : a < (3 * n) + (3 * n) := by omega
      have he : cycleNext (3 * n) ⟨a, hp⟩ = (⟨a + 1, ha⟩ : RingIndex n) := by
        apply Fin.ext
        simp [cycleNext, ha]
      rw [← he]
      exact (ringSwap_successor n hn iso _).trans (ih hp)
  exact h t.val t.isLt

def inducedRingIso (n : Nat) (hn : 2 ≤ n) (iso : ModelAut n) :
    GraphIso (ringAdj (3 * n)) (ringAdj (3 * n)) where
  forward := leafImage n iso
  backward := leafImage n (inverseIso iso)
  left_inv := leafImage_left_inv n hn iso
  right_inv := leafImage_right_inv n hn iso
  preserves := by
    intro t u
    have he := iso.preserves (.X t) (.X u)
    rw [ring_X_forward n hn iso t, ring_X_forward n hn iso u,
      ringSwap_constant n hn iso t, ringSwap_constant n hn iso u] at he
    cases hs : ringSwap n iso (ringZero n hn) <;>
      simpa only [hs, Bool.false_eq_true, ↓reduceIte, coordinateAdj] using he

def liftCentre (n : Nat) (s : Fin (n + n)) : RingIndex n :=
  ⟨s.val, by have hs := s.isLt; omega⟩

theorem centreResidue_lift (n : Nat) (s : Fin (n + n)) :
    centreResidue n (liftCentre n s) = s := by
  apply Fin.ext
  simp [centreResidue, liftCentre, s.isLt]

theorem centre_forward (n : Nat) (hn : 2 ≤ n) (iso : ModelAut n) (s : Fin (n + n)) :
    iso.forward (.Z s) = .Z (centreResidue n (leafImage n iso (liftCentre n s))) := by
  have hr := (automorphism_preserves_centres n hn iso (.Z s)).mpr True.intro
  cases hv : iso.forward (.Z s) with
  | X u => simp only [hv, IsCentre] at hr
  | Y u => simp only [hv, IsCentre] at hr
  | A u => simp only [hv, IsCentre] at hr
  | Z c =>
    have hs : coordinateAdj n (.A (liftCentre n s)) (.Z s) := centreResidue_lift n s
    have he := (iso.preserves _ _).mpr hs
    rw [leaf_forward n hn iso (liftCentre n s), hv] at he
    change centreResidue n (leafImage n iso (liftCentre n s)) = c at he
    exact congrArg Coord.Z he.symm

def dataAction (n : Nat) (p : RingIndex n → RingIndex n) (swap : Bool) : Coord n → Coord n
  | .X t => if swap then .Y (p t) else .X (p t)
  | .Y t => if swap then .X (p t) else .Y (p t)
  | .A t => .A (p t)
  | .Z s => .Z (centreResidue n (p (liftCentre n s)))

theorem every_automorphism_synchronized (n : Nat) (hn : 2 ≤ n) (iso : ModelAut n)
    (v : Coord n) :
    iso.forward v = dataAction n (inducedRingIso n hn iso).forward
      (ringSwap n iso (ringZero n hn)) v := by
  cases v with
  | X t =>
    rw [ring_X_forward n hn iso t, ringSwap_constant n hn iso t]
    rfl
  | Y t =>
    rw [ring_Y_forward n hn iso t, ringSwap_constant n hn iso t]
    rfl
  | A t => exact leaf_forward n hn iso t
  | Z s => exact centre_forward n hn iso s

theorem automorphism_determined_by_ring_data (n : Nat) (hn : 2 ≤ n)
    (iso other : ModelAut n)
    (hp : ∀ t, (inducedRingIso n hn iso).forward t = (inducedRingIso n hn other).forward t)
    (hs : ringSwap n iso (ringZero n hn) = ringSwap n other (ringZero n hn))
    (v : Coord n) : iso.forward v = other.forward v := by
  rw [every_automorphism_synchronized n hn iso v,
    every_automorphism_synchronized n hn other v, hs]
  cases v <;> simp only [dataAction, hp]

#print axioms leaf_forward
#print axioms leafImage_injective
#print axioms leafImage_left_inv
#print axioms leafImage_right_inv
#print axioms ring_X_forward
#print axioms ring_Y_forward
#print axioms ringSwap_successor
#print axioms ringSwap_constant
#print axioms inducedRingIso
#print axioms centre_forward
#print axioms every_automorphism_synchronized
#print axioms automorphism_determined_by_ring_data

end Struct2.RingAction
