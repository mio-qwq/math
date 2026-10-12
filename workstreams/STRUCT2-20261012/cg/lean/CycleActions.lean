import CycleRigidity

/-!
Explicit rotations and reflections on cyclic indices and their actual
graph-isomorphism laws. Arithmetic is symbolic and includes every wrap.
-/

set_option Elab.async false
set_option maxHeartbeats 6000000

namespace Struct2.CycleActions

open OddCoordinates SixCycleInvariant StrongFold CycleRigidity

def rotation (m : Nat) (a t : Fin (m + m)) : Fin (m + m) :=
  if h : a.val + t.val < m + m then ⟨a.val + t.val, h⟩
  else ⟨a.val + t.val - (m + m), by have ha := a.isLt; have ht := t.isLt; omega⟩

def inverseRotation (m : Nat) (a t : Fin (m + m)) : Fin (m + m) :=
  if h : a.val ≤ t.val then ⟨t.val - a.val, by have ht := t.isLt; omega⟩
  else ⟨(m + m) + t.val - a.val, by have ha := a.isLt; omega⟩

def reflection (m : Nat) (a t : Fin (m + m)) : Fin (m + m) :=
  if h : t.val ≤ a.val then ⟨a.val - t.val, by have ha := a.isLt; omega⟩
  else ⟨(m + m) + a.val - t.val, by have ht := t.isLt; omega⟩

theorem rotation_val (m : Nat) (a t : Fin (m + m)) :
    (rotation m a t).val =
      if a.val + t.val < m + m then a.val + t.val else a.val + t.val - (m + m) := by
  unfold rotation
  split <;> rfl

theorem reflection_val (m : Nat) (a t : Fin (m + m)) :
    (reflection m a t).val =
      if t.val ≤ a.val then a.val - t.val else (m + m) + a.val - t.val := by
  unfold reflection
  split <;> rfl

theorem cycleNext_val (m : Nat) (t : Fin (m + m)) :
    (cycleNext m t).val = if t.val + 1 < m + m then t.val + 1 else 0 := by
  unfold cycleNext
  split <;> rfl

macro "cyclic_cases" : tactic => `(tactic| (
  all_goals try split at *
  all_goals try dsimp at *
  all_goals try omega
  all_goals try split at *
  all_goals try dsimp at *
  all_goals try omega
  all_goals try split at *
  all_goals try dsimp at *
  all_goals try omega
  all_goals try split at *
  all_goals try dsimp at *
  all_goals try omega
  all_goals try split at *
  all_goals try dsimp at *
  all_goals try omega
  all_goals try split at *
  all_goals try dsimp at *
  all_goals try omega
  all_goals try split at *
  all_goals try dsimp at *
  all_goals try omega
  all_goals try split at *
  all_goals try dsimp at *
  all_goals try omega
  all_goals try split at *
  all_goals try dsimp at *
  all_goals try omega
  all_goals try split at *
  all_goals try dsimp at *
  all_goals try omega
  all_goals try split at *
  all_goals try dsimp at *
  all_goals try omega
  all_goals try split at *
  all_goals try dsimp at *
  all_goals try omega
  all_goals omega))

theorem rotation_left_inv (m : Nat) (a t : Fin (m + m)) :
    inverseRotation m a (rotation m a t) = t := by
  apply Fin.ext
  have ha := a.isLt
  have ht := t.isLt
  unfold inverseRotation rotation
  cyclic_cases

theorem rotation_right_inv (m : Nat) (a t : Fin (m + m)) :
    rotation m a (inverseRotation m a t) = t := by
  apply Fin.ext
  have ha := a.isLt
  have ht := t.isLt
  unfold inverseRotation rotation
  cyclic_cases

theorem reflection_involutive (m : Nat) (a t : Fin (m + m)) :
    reflection m a (reflection m a t) = t := by
  apply Fin.ext
  have ha := a.isLt
  have ht := t.isLt
  unfold reflection
  cyclic_cases

theorem rotation_injective (m : Nat) (a t u : Fin (m + m))
    (h : rotation m a t = rotation m a u) : t = u := by
  have hi := congrArg (inverseRotation m a) h
  simpa only [rotation_left_inv] using hi

theorem reflection_injective (m : Nat) (a t u : Fin (m + m))
    (h : reflection m a t = reflection m a u) : t = u := by
  have hi := congrArg (reflection m a) h
  simpa only [reflection_involutive] using hi

theorem rotation_next (m : Nat) (a t : Fin (m + m)) :
    rotation m a (cycleNext m t) = cycleNext m (rotation m a t) := by
  apply Fin.ext
  have ha := a.isLt
  have ht := t.isLt
  simp only [rotation_val, cycleNext_val]
  cyclic_cases

theorem reflection_next (m : Nat) (a t : Fin (m + m)) :
    cycleNext m (reflection m a (cycleNext m t)) = reflection m a t := by
  apply Fin.ext
  have ha := a.isLt
  have ht := t.isLt
  simp only [reflection_val, cycleNext_val]
  by_cases hnxt : t.val + 1 < m + m <;>
    by_cases hta : t.val ≤ a.val <;>
    by_cases hnxta : t.val + 1 ≤ a.val <;>
    by_cases hanxt : a.val + 1 < m + m <;>
    simp only [hnxt, hta, hnxta, hanxt, ↓reduceIte, Nat.zero_le, Nat.sub_zero]
  all_goals first | omega | (split <;> omega)

theorem rotation_adjacency (m : Nat) (a t u : Fin (m + m)) :
    ringAdj m (rotation m a t) (rotation m a u) ↔ ringAdj m t u := by
  constructor
  · intro h
    rcases h with h | h
    · left
      rw [← rotation_next] at h
      exact rotation_injective m a _ _ h
    · right
      rw [← rotation_next] at h
      exact rotation_injective m a _ _ h
  · intro h
    rcases h with h | h
    · left
      rw [← rotation_next, h]
    · right
      rw [← rotation_next, h]

theorem reflection_preserves (m : Nat) (a t u : Fin (m + m))
    (h : ringAdj m t u) : ringAdj m (reflection m a t) (reflection m a u) := by
  rcases h with h | h
  · right
    rw [← h]
    exact reflection_next m a t
  · left
    rw [← h]
    exact reflection_next m a u

theorem reflection_adjacency (m : Nat) (a t u : Fin (m + m)) :
    ringAdj m (reflection m a t) (reflection m a u) ↔ ringAdj m t u := by
  constructor
  · intro h
    simpa only [reflection_involutive] using reflection_preserves m a _ _ h
  · exact reflection_preserves m a t u

def rotationIso (m : Nat) (a : Fin (m + m)) : CycleIso m where
  forward := rotation m a
  backward := inverseRotation m a
  left_inv := rotation_left_inv m a
  right_inv := rotation_right_inv m a
  preserves := rotation_adjacency m a

def reflectionIso (m : Nat) (a : Fin (m + m)) : CycleIso m where
  forward := reflection m a
  backward := reflection m a
  left_inv := reflection_involutive m a
  right_inv := reflection_involutive m a
  preserves := reflection_adjacency m a

theorem rotation_zero (m : Nat) (hm : 2 ≤ m) (a : Fin (m + m)) :
    rotation m a (cycleZero m hm) = a := by
  apply Fin.ext
  have ha := a.isLt
  unfold rotation cycleZero
  cyclic_cases

theorem reflection_zero (m : Nat) (hm : 2 ≤ m) (a : Fin (m + m)) :
    reflection m a (cycleZero m hm) = a := by
  apply Fin.ext
  have ha := a.isLt
  unfold reflection cycleZero
  cyclic_cases

theorem cycleNext_zero (m : Nat) (hm : 2 ≤ m) :
    cycleNext m (cycleZero m hm) = cycleOne m hm := by
  apply Fin.ext
  simp [cycleZero, cycleOne, cycleNext, show 1 < m + m by omega]

theorem rotation_direction (m : Nat) (hm : 2 ≤ m) (a : Fin (m + m)) :
    direction m hm (rotationIso m a) = true := by
  change decide (cycleNext m (rotation m a (cycleZero m hm)) =
    rotation m a (cycleOne m hm)) = true
  apply decide_eq_true
  rw [← cycleNext_zero m hm]
  exact (rotation_next m a _).symm

theorem reflection_direction (m : Nat) (hm : 2 ≤ m) (a : Fin (m + m)) :
    direction m hm (reflectionIso m a) = false := by
  change decide (cycleNext m (reflection m a (cycleZero m hm)) =
    reflection m a (cycleOne m hm)) = false
  apply decide_eq_false
  intro h
  have hb : cycleNext m (reflection m a (cycleOne m hm)) = a := by
    rw [← cycleNext_zero m hm]
    simpa only [reflection_zero] using reflection_next m a (cycleZero m hm)
  rw [reflection_zero] at h
  rw [← h] at hb
  exact cycleNext_twice_ne m hm a hb

def dihedralIso (m : Nat) (a : Fin (m + m)) (positive : Bool) : CycleIso m :=
  if positive then rotationIso m a else reflectionIso m a

theorem cycle_iso_dihedral (m : Nat) (hm : 2 ≤ m) (g : CycleIso m) :
    g = dihedralIso m (g.forward (cycleZero m hm)) (direction m hm g) := by
  apply graphIso_ext
  intro t
  apply cycle_iso_determined_by_index_direction m hm g _ _ _ t
  · cases hd : direction m hm g <;>
      simp only [dihedralIso, Bool.false_eq_true, ↓reduceIte]
    · exact (reflection_zero m hm _).symm
    · exact (rotation_zero m hm _).symm
  · cases hd : direction m hm g <;>
      simp only [dihedralIso, Bool.false_eq_true, ↓reduceIte]
    · exact (reflection_direction m hm _).symm
    · exact (rotation_direction m hm _).symm

#print axioms rotation_left_inv
#print axioms rotation_right_inv
#print axioms reflection_involutive
#print axioms rotation_next
#print axioms reflection_next
#print axioms rotation_adjacency
#print axioms reflection_adjacency
#print axioms rotationIso
#print axioms reflectionIso
#print axioms rotation_direction
#print axioms reflection_direction
#print axioms cycle_iso_dihedral

end Struct2.CycleActions
