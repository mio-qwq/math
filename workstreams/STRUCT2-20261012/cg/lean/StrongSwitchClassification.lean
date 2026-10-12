import ModelActions

/-!
Exact classification of the strongly switching automorphisms of the actual
odd-parameter CG canonical double-cover model.  This file works from the
proved exhaustive automorphism parametrization; it does not assume a group
presentation or a precomputed involution catalogue.
-/

set_option Elab.async false
set_option maxHeartbeats 12000000
set_option maxRecDepth 20000

namespace Struct2.StrongSwitchClassification

open OddCoordinates StrongFold ModelStructure RingAction CycleRigidity CycleActions ModelActions

def IsStrong (n : Nat) (hn : n % 2 = 1) (g : ModelAut n) : Prop :=
  (∀ x, g.forward (g.forward x) = x) ∧
  (∀ x, (modelGraph n hn).colour (g.forward x) = !(modelGraph n hn).colour x) ∧
  (∀ x, ¬ coordinateAdj n x (g.forward x))

def strongSwitchOf (n : Nat) (hn : n % 2 = 1) (g : ModelAut n)
    (h : IsStrong n hn g) : Switch (modelGraph n hn) where
  map := g.forward
  involutive := h.1
  preserves := g.preserves
  reverses := h.2.1
  nonadjacent := h.2.2

theorem bit_rotation_odd (m : Nat) (a t : Fin (m + m))
    (ha : bit a.val = true) :
    bit (rotation m a t).val = !bit t.val := by
  simp [bit] at ha
  have ht : t.val % 2 = 0 ∨ t.val % 2 = 1 := by omega
  rcases ht with ht | ht <;> simp [bit, rotation_val, ht]
  all_goals split <;> omega

theorem bit_reflection_odd (m : Nat) (a t : Fin (m + m))
    (ha : bit a.val = true) :
    bit (reflection m a t).val = !bit t.val := by
  simp [bit] at ha
  have ht : t.val % 2 = 0 ∨ t.val % 2 = 1 := by omega
  rcases ht with ht | ht <;> simp [bit, reflection_val, ht]
  all_goals split <;> omega

theorem parameter_reverses_of_odd (n : Nat) (hn : n % 2 = 1)
    (a : RingIndex n) (positive swap : Bool) (ha : bit a.val = true) (x : Coord n) :
    (modelGraph n hn).colour ((dihedralModelIso n a positive swap).forward x) =
      !(modelGraph n hn).colour x := by
  rw [parameter_forward]
  cases positive <;> cases x <;> cases swap <;>
    simp only [dihedralIso, rotationIso, reflectionIso, Bool.false_eq_true,
      ↓reduceIte, dataAction, modelGraph, toCover, centreResidue_bit]
  all_goals first
    | exact bit_reflection_odd _ a _ ha
    | exact congrArg Bool.not (bit_reflection_odd _ a _ ha)
    | simpa only [liftCentre] using bit_reflection_odd _ a _ ha
    | exact bit_rotation_odd _ a _ ha
    | exact congrArg Bool.not (bit_rotation_odd _ a _ ha)
    | simpa only [liftCentre] using bit_rotation_odd _ a _ ha

theorem parameter_reverses_only_if_odd (n : Nat) (hn : n % 2 = 1)
    (a : RingIndex n) (positive swap : Bool)
    (h : ∀ x, (modelGraph n hn).colour ((dihedralModelIso n a positive swap).forward x) =
      !(modelGraph n hn).colour x) : bit a.val = true := by
  have hx := h (.X ⟨0, by omega⟩)
  rw [parameter_forward] at hx
  cases positive <;> cases swap <;>
    simpa [dihedralIso, rotationIso, reflectionIso, dataAction, modelGraph,
      toCover, reflection, rotation, bit] using hx

theorem reflection_forward_Z (n : Nat) (a : RingIndex n) (swap : Bool)
    (s : Fin (n + n)) :
    (reflectionModelIso n a swap).forward (.Z s) =
      .Z (reflection n (centreResidue n a) s) := by
  rfl

theorem rotation_forward_Z (n : Nat) (a : RingIndex n) (swap : Bool)
    (s : Fin (n + n)) :
    (rotationModelIso n a swap).forward (.Z s) =
      .Z (rotation n (centreResidue n a) s) := by
  rfl

theorem reflection_action_involutive (n : Nat) (a : RingIndex n) (swap : Bool)
    (x : Coord n) :
    (reflectionModelIso n a swap).forward
      ((reflectionModelIso n a swap).forward x) = x := by
  cases x with
  | Z s => simp only [reflection_forward_Z, reflection_involutive]
  | X t | Y t | A t =>
  change (dihedralModelIso n a false swap).forward
      ((dihedralModelIso n a false swap).forward _) = _
  all_goals rw [parameter_forward, parameter_forward]
  all_goals cases swap <;>
    simp [dihedralIso, reflectionIso, dataAction, reflection_involutive]

def halfTurn (n : Nat) (hn : 0 < n) : RingIndex n := ⟨3 * n, by omega⟩

theorem halfTurn_eq (n : Nat) (hn : 0 < n) : (halfTurn n hn).val = 3 * n := rfl

def centreHalfTurn (n : Nat) (hn : 0 < n) : Fin (n + n) := ⟨n, by omega⟩

theorem halfShift_val (m : Nat) (t : Fin (m + m)) :
    (halfShift m t).val = if t.val < m then t.val + m else t.val - m := by
  unfold halfShift
  split <;> rfl

theorem centreResidue_halfTurn (n : Nat) (hn : 0 < n) :
    centreResidue n (halfTurn n hn) = centreHalfTurn n hn := by
  apply Fin.ext
  rw [centreResidue_val, halfTurn_eq]
  change (if 3 * n < n + n then 3 * n
    else if 3 * n < (n + n) + (n + n) then 3 * n - (n + n)
    else 3 * n - ((n + n) + (n + n))) = n
  split
  all_goals try split
  all_goals omega

theorem rotation_centreHalfTurn (n : Nat) (hn : 0 < n) (t : Fin (n + n)) :
    rotation n (centreHalfTurn n hn) t = halfShift n t := by
  apply Fin.ext
  have ht := t.isLt
  simp only [rotation_val, halfShift_val]
  by_cases h : t.val < n <;> simp [centreHalfTurn, h]
  all_goals omega

theorem rotation_halfTurn (n : Nat) (hn : 0 < n) (t : RingIndex n) :
    rotation (3 * n) (halfTurn n hn) t = halfShift (3 * n) t := by
  apply Fin.ext
  have ht := t.isLt
  simp only [rotation_val, halfTurn_eq, halfShift_val]
  by_cases h : t.val < 3 * n <;> simp [h]
  all_goals omega

theorem halfTurn_rotation_involutive (n : Nat) (hn : 0 < n) (swap : Bool) (x : Coord n) :
    (rotationModelIso n (halfTurn n hn) swap).forward
      ((rotationModelIso n (halfTurn n hn) swap).forward x) = x := by
  cases x with
  | Z s =>
      simp only [rotation_forward_Z, centreResidue_halfTurn, rotation_centreHalfTurn,
        halfShift_involutive]
  | X t | Y t | A t =>
  change (dihedralModelIso n (halfTurn n hn) true swap).forward
      ((dihedralModelIso n (halfTurn n hn) true swap).forward _) = _
  all_goals rw [parameter_forward, parameter_forward]
  all_goals cases swap <;>
    simp [dihedralIso, rotationIso, dataAction, rotation_halfTurn, halfShift_involutive]

theorem halfTurn_odd (n : Nat) (hn0 : 0 < n) (hn : n % 2 = 1) :
    bit (halfTurn n hn0).val = true := by
  simp [bit, halfTurn_eq]
  omega

theorem ringAdj_halfShift_self_false (m : Nat) (hm : 2 ≤ m) (t : Fin (m + m)) :
    ¬ ringAdj m t (halfShift m t) := by
  intro h
  rcases h with h | h
  · have hv := congrArg Fin.val h
    have ht := t.isLt
    simp only [cycleNext_val] at hv
    unfold halfShift at hv
    split at hv <;> split at hv <;> dsimp at * <;> omega
  · have hv := congrArg Fin.val h
    have ht := t.isLt
    simp only [cycleNext_val] at hv
    unfold halfShift at hv
    split at hv <;> split at hv <;> dsimp at * <;> omega

theorem halfTurn_nonadjacent (n : Nat) (hn3 : 3 ≤ n) (swap : Bool) (x : Coord n) :
    ¬ coordinateAdj n x ((rotationModelIso n (halfTurn n (by omega)) swap).forward x) := by
  change ¬ coordinateAdj n x
    ((dihedralModelIso n (halfTurn n (by omega)) true swap).forward x)
  rw [parameter_forward]
  cases x <;> cases swap <;>
    simp only [dihedralIso, rotationIso, dataAction, Bool.false_eq_true, ↓reduceIte,
      coordinateAdj, rotation_halfTurn]
  all_goals try simp
  all_goals exact ringAdj_halfShift_self_false (3 * n) (by omega) _

theorem swapped_reflection_nonadjacent (n : Nat) (a : RingIndex n) (x : Coord n) :
    ¬ coordinateAdj n x ((reflectionModelIso n a true).forward x) := by
  change ¬ coordinateAdj n x ((dihedralModelIso n a false true).forward x)
  rw [parameter_forward]
  cases x <;> simp [dataAction, coordinateAdj]

theorem strong_halfTurn (n : Nat) (hn : n % 2 = 1) (hn3 : 3 ≤ n) (swap : Bool) :
    IsStrong n hn (rotationModelIso n (halfTurn n (by omega)) swap) := by
  refine ⟨halfTurn_rotation_involutive n (by omega) swap, ?_,
    halfTurn_nonadjacent n hn3 swap⟩
  exact parameter_reverses_of_odd n hn (halfTurn n (by omega)) true swap
    (halfTurn_odd n (by omega) hn)

theorem strong_odd_swapped_reflection (n : Nat) (hn : n % 2 = 1)
    (a : RingIndex n) (ha : bit a.val = true) :
    IsStrong n hn (reflectionModelIso n a true) := by
  refine ⟨reflection_action_involutive n a true, ?_, swapped_reflection_nonadjacent n a⟩
  exact parameter_reverses_of_odd n hn a false true ha

def ringZero' (n : Nat) (hn : 0 < n) : RingIndex n := ⟨0, by omega⟩

theorem odd_rotation_involution_half (n : Nat) (hn : 0 < n) (a : RingIndex n)
    (ha : bit a.val = true)
    (hi : rotation (3 * n) a (rotation (3 * n) a (ringZero' n hn)) = ringZero' n hn) :
    a = halfTurn n hn := by
  apply Fin.ext
  have hal := a.isLt
  have ha' : a.val % 2 = 1 := by simpa [bit] using ha
  have hv := congrArg Fin.val hi
  simp only [rotation_val] at hv
  unfold ringZero' at hv
  dsimp at hv
  split at hv
  all_goals try split at hv
  all_goals simp only [halfTurn_eq]
  all_goals omega

theorem rotation_involution_forces_half (n : Nat) (hn : n % 2 = 1) (hn3 : 3 ≤ n)
    (a : RingIndex n) (swap : Bool) (ha : bit a.val = true)
    (hi : ∀ x, (rotationModelIso n a swap).forward
      ((rotationModelIso n a swap).forward x) = x) :
    a = halfTurn n (by omega) := by
  have hx := hi (.X (ringZero' n (by omega)))
  change (dihedralModelIso n a true swap).forward
    ((dihedralModelIso n a true swap).forward (.X (ringZero' n (by omega)))) =
      .X (ringZero' n (by omega)) at hx
  rw [parameter_forward, parameter_forward] at hx
  cases swap <;>
    simp only [dihedralIso, rotationIso, dataAction, Bool.false_eq_true, ↓reduceIte] at hx
  all_goals exact odd_rotation_involution_half n (by omega) a ha (Coord.X.inj hx)

def reflectionWitness (n : Nat) (a : RingIndex n) : RingIndex n :=
  ⟨a.val / 2, by have ha := a.isLt; omega⟩

theorem reflection_witness_next (n : Nat) (a : RingIndex n)
    (ha : bit a.val = true) :
    cycleNext (3 * n) (reflectionWitness n a) =
      reflection (3 * n) a (reflectionWitness n a) := by
  apply Fin.ext
  have hal := a.isLt
  have ha' : a.val % 2 = 1 := by simpa [bit] using ha
  simp only [cycleNext_val, reflection_val]
  unfold reflectionWitness
  dsimp
  split <;> split <;> omega

theorem unswapped_odd_reflection_not_nonadjacent (n : Nat) (a : RingIndex n)
    (ha : bit a.val = true) :
    ¬(∀ x, ¬coordinateAdj n x ((reflectionModelIso n a false).forward x)) := by
  intro h
  let t := reflectionWitness n a
  have hadj : ringAdj (3 * n) t (reflection (3 * n) a t) :=
    Or.inl (reflection_witness_next n a ha)
  have hx := h (.X t)
  change ¬coordinateAdj n (.X t)
    ((dihedralModelIso n a false false).forward (.X t)) at hx
  rw [parameter_forward] at hx
  exact hx (by simpa [dihedralIso, reflectionIso, dataAction, coordinateAdj] using hadj)

theorem parameter_isStrong_iff (n : Nat) (hn : n % 2 = 1) (hn3 : 3 ≤ n)
    (a : RingIndex n) (positive swap : Bool) :
    IsStrong n hn (dihedralModelIso n a positive swap) ↔
      (a = halfTurn n (by omega) ∧ positive = true) ∨
      (bit a.val = true ∧ positive = false ∧ swap = true) := by
  constructor
  · intro h
    have ha := parameter_reverses_only_if_odd n hn a positive swap h.2.1
    cases hp : positive with
    | false =>
        right
        refine ⟨ha, rfl, ?_⟩
        cases hs : swap with
        | false =>
            exfalso
            apply unswapped_odd_reflection_not_nonadjacent n a ha
            intro x
            have hx := h.2.2 x
            simpa [dihedralModelIso, hp, hs] using hx
        | true => rfl
    | true =>
        left
        refine ⟨?_, rfl⟩
        apply rotation_involution_forces_half n hn hn3 a swap ha
        intro x
        have hx := h.1 x
        simpa [dihedralModelIso, hp] using hx
  · intro h
    rcases h with h | h
    · rcases h with ⟨rfl, rfl⟩
      simpa [dihedralModelIso] using strong_halfTurn n hn hn3 swap
    · rcases h with ⟨ha, rfl, rfl⟩
      simpa [dihedralModelIso] using strong_odd_swapped_reflection n hn a ha

theorem every_strong_automorphism (n : Nat) (hn : n % 2 = 1) (hn3 : 3 ≤ n)
    (g : ModelAut n) (h : IsStrong n hn g) :
    let a := (automorphismCode n (by omega) g).1
    let positive := (automorphismCode n (by omega) g).2.1
    let swap := (automorphismCode n (by omega) g).2.2
    (a = halfTurn n (by omega) ∧ positive = true) ∨
      (bit a.val = true ∧ positive = false ∧ swap = true) := by
  dsimp
  have hg := parametersToAut_right_inv n (by omega) g
  rw [← hg] at h
  exact (parameter_isStrong_iff n hn hn3 _ _ _).mp h

#print axioms parameter_reverses_of_odd
#print axioms reflection_action_involutive
#print axioms halfTurn_rotation_involutive
#print axioms halfTurn_nonadjacent
#print axioms strong_halfTurn
#print axioms strong_odd_swapped_reflection
#print axioms odd_rotation_involution_half
#print axioms reflection_witness_next
#print axioms unswapped_odd_reflection_not_nonadjacent
#print axioms parameter_isStrong_iff
#print axioms every_strong_automorphism

end Struct2.StrongSwitchClassification
