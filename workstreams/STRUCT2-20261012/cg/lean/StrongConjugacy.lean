import StrongSwitchClassification

/-!
Conjugacy of the three strong-switch families.  The proofs use the actual
coordinate actions and the previously proved exhaustive automorphism
parametrization, not a separately assumed abstract group presentation.
-/

set_option Elab.async false
set_option maxHeartbeats 12000000
set_option maxRecDepth 20000

namespace Struct2.StrongConjugacy

open OddCoordinates StrongFold ModelStructure SixCycleInvariant RingAction CycleRigidity CycleActions
  ModelActions StrongSwitchClassification

def Conjugates (n : Nat) (g h : ModelAut n) : Prop :=
  ∃ c : ModelAut n, ∀ x, c.forward (g.forward x) = h.forward (c.forward x)

theorem parameter_forward_raw (n : Nat) (a : RingIndex n) (positive swap : Bool)
    (x : Coord n) :
    (dihedralModelIso n a positive swap).forward x =
      rawAction n (dihedralIso (3 * n) a positive).forward
        (dihedralIso n (centreResidue n a) positive).forward swap x := by
  cases positive <;> rfl

theorem rotation_halfShift_commute (m : Nat) (a t : Fin (m + m)) :
    rotation m a (halfShift m t) = halfShift m (rotation m a t) := by
  apply Fin.ext
  have ha := a.isLt
  have ht := t.isLt
  simp only [rotation_val, halfShift_val]
  cyclic_cases

theorem reflection_halfShift_commute (m : Nat) (a t : Fin (m + m)) :
    reflection m a (halfShift m t) = halfShift m (reflection m a t) := by
  apply Fin.ext
  have ha := a.isLt
  have ht := t.isLt
  simp only [reflection_val, halfShift_val]
  cyclic_cases

theorem dihedral_halfShift_commute (m : Nat) (a t : Fin (m + m)) (positive : Bool) :
    (dihedralIso m a positive).forward (halfShift m t) =
      halfShift m ((dihedralIso m a positive).forward t) := by
  cases positive
  · exact reflection_halfShift_commute m a t
  · exact rotation_halfShift_commute m a t

theorem halfTurn_commutes_parameter (n : Nat) (hn : 0 < n)
    (a : RingIndex n) (positive swap deckSwap : Bool) (x : Coord n) :
    (dihedralModelIso n a positive swap).forward
        ((rotationModelIso n (halfTurn n hn) deckSwap).forward x) =
      (rotationModelIso n (halfTurn n hn) deckSwap).forward
        ((dihedralModelIso n a positive swap).forward x) := by
  change (dihedralModelIso n a positive swap).forward
      ((dihedralModelIso n (halfTurn n hn) true deckSwap).forward x) =
    (dihedralModelIso n (halfTurn n hn) true deckSwap).forward
      ((dihedralModelIso n a positive swap).forward x)
  rw [parameter_forward_raw, parameter_forward_raw,
    parameter_forward_raw, parameter_forward_raw]
  cases x <;> cases positive <;> cases swap <;> cases deckSwap <;>
    simp only [dihedralIso, rotationIso, reflectionIso, rawAction,
      Bool.false_eq_true, ↓reduceIte, rotation_halfTurn,
      rotation_centreHalfTurn, centreResidue_halfTurn]
  all_goals first
    | congr 1; exact reflection_halfShift_commute _ _ _
    | congr 1; exact rotation_halfShift_commute _ _ _

theorem halfTurn_central (n : Nat) (hn : n % 2 = 1) (hn3 : 3 ≤ n)
    (g : ModelAut n) (deckSwap : Bool) (x : Coord n) :
    g.forward ((rotationModelIso n (halfTurn n (by omega)) deckSwap).forward x) =
      (rotationModelIso n (halfTurn n (by omega)) deckSwap).forward (g.forward x) := by
  rw [every_model_automorphism_dihedral n (by omega) g]
  exact halfTurn_commutes_parameter n (by omega) _ _ _ _ x

theorem conjugate_to_halfTurn_is_equal (n : Nat) (hn : n % 2 = 1) (hn3 : 3 ≤ n)
    (g : ModelAut n) (deckSwap : Bool)
    (h : Conjugates n (rotationModelIso n (halfTurn n (by omega)) deckSwap) g) :
    g = rotationModelIso n (halfTurn n (by omega)) deckSwap := by
  rcases h with ⟨c, hc⟩
  apply graphIso_ext
  intro x
  have he := hc (c.backward x)
  rw [c.right_inv] at he
  rw [halfTurn_central n hn hn3 c deckSwap (c.backward x), c.right_inv] at he
  exact he.symm

def oneIndex (n : Nat) (hn : 0 < n) : RingIndex n := ⟨1, by omega⟩

def oddConjugatorShift (n : Nat) (a : RingIndex n) : RingIndex n :=
  ⟨a.val / 2, by have ha := a.isLt; omega⟩

theorem odd_reflection_conjugacy_index (n : Nat) (hn : 0 < n)
    (a : RingIndex n) (ha : bit a.val = true) (t : RingIndex n) :
    rotation (3 * n) (oddConjugatorShift n a)
        (reflection (3 * n) (oneIndex n hn) t) =
      reflection (3 * n) a (rotation (3 * n) (oddConjugatorShift n a) t) := by
  apply Fin.ext
  have hal := a.isLt
  have ht := t.isLt
  have ha' : a.val % 2 = 1 := by simpa [bit] using ha
  simp only [rotation_val, reflection_val]
  unfold oddConjugatorShift oneIndex
  dsimp
  cyclic_cases

theorem odd_reflection_conjugacy_centre (n : Nat) (hn : 0 < n)
    (a : RingIndex n) (ha : bit a.val = true) (s : Fin (n + n)) :
    rotation n (centreResidue n (oddConjugatorShift n a))
        (reflection n (centreResidue n (oneIndex n hn)) s) =
      reflection n (centreResidue n a)
        (rotation n (centreResidue n (oddConjugatorShift n a)) s) := by
  have h := congrArg (centreResidue n)
    (odd_reflection_conjugacy_index n hn a ha (liftCentre n s))
  simpa only [residue_rotation, residue_reflection, centreResidue_lift] using h

theorem odd_reflection_conjugate_to_one (n : Nat) (hn : n % 2 = 1)
    (hn3 : 3 ≤ n) (a : RingIndex n) (ha : bit a.val = true) :
    Conjugates n (reflectionModelIso n (oneIndex n (by omega)) true)
      (reflectionModelIso n a true) := by
  refine ⟨rotationModelIso n (oddConjugatorShift n a) false, ?_⟩
  intro x
  change (dihedralModelIso n (oddConjugatorShift n a) true false).forward
      ((dihedralModelIso n (oneIndex n (by omega)) false true).forward x) =
    (dihedralModelIso n a false true).forward
      ((dihedralModelIso n (oddConjugatorShift n a) true false).forward x)
  rw [parameter_forward_raw, parameter_forward_raw,
    parameter_forward_raw, parameter_forward_raw]
  cases x <;>
    simp only [dihedralIso, rotationIso, reflectionIso, rawAction,
      Bool.false_eq_true, ↓reduceIte]
  all_goals first
    | congr 1; exact odd_reflection_conjugacy_index n (by omega) a ha _
    | congr 1; exact odd_reflection_conjugacy_centre n (by omega) a ha _

theorem halfTurn_parameters_ne (n : Nat) (hn3 : 3 ≤ n) :
    rotationModelIso n (halfTurn n (by omega)) false ≠
      rotationModelIso n (halfTurn n (by omega)) true := by
  intro h
  change parametersToAut n (halfTurn n (by omega), true, false) =
    parametersToAut n (halfTurn n (by omega), true, true) at h
  have hp := parametersToAut_injective n (by omega) _ _ h
  simp at hp

theorem halfTurn_reflection_ne (n : Nat) (hn3 : 3 ≤ n) (deckSwap : Bool) :
    rotationModelIso n (halfTurn n (by omega)) deckSwap ≠
      reflectionModelIso n (oneIndex n (by omega)) true := by
  intro h
  change parametersToAut n (halfTurn n (by omega), true, deckSwap) =
    parametersToAut n (oneIndex n (by omega), false, true) at h
  have hp := parametersToAut_injective n (by omega) _ _ h
  simp at hp

theorem halfTurn_classes_distinct (n : Nat) (hn : n % 2 = 1) (hn3 : 3 ≤ n) :
    ¬Conjugates n (rotationModelIso n (halfTurn n (by omega)) false)
      (rotationModelIso n (halfTurn n (by omega)) true) := by
  intro h
  exact halfTurn_parameters_ne n hn3
    (conjugate_to_halfTurn_is_equal n hn hn3 _ false h).symm

theorem halfTurn_reflection_classes_distinct (n : Nat) (hn : n % 2 = 1)
    (hn3 : 3 ≤ n) (deckSwap : Bool) :
    ¬Conjugates n (rotationModelIso n (halfTurn n (by omega)) deckSwap)
      (reflectionModelIso n (oneIndex n (by omega)) true) := by
  intro h
  exact halfTurn_reflection_ne n hn3 deckSwap
    (conjugate_to_halfTurn_is_equal n hn hn3 _ deckSwap h).symm

theorem every_strong_in_three_classes (n : Nat) (hn : n % 2 = 1) (hn3 : 3 ≤ n)
    (g : ModelAut n) (hg : IsStrong n hn g) :
    g = rotationModelIso n (halfTurn n (by omega)) false ∨
    g = rotationModelIso n (halfTurn n (by omega)) true ∨
    Conjugates n (reflectionModelIso n (oneIndex n (by omega)) true) g := by
  let p := automorphismCode n (by omega) g
  have hdecode : parametersToAut n p = g := parametersToAut_right_inv n (by omega) g
  have hc := every_strong_automorphism n hn hn3 g hg
  change (p.1 = halfTurn n (by omega) ∧ p.2.1 = true) ∨
    (bit p.1.val = true ∧ p.2.1 = false ∧ p.2.2 = true) at hc
  rcases hc with hc | hc
  · rcases hc with ⟨ha, hp⟩
    cases hs : p.2.2
    · left
      rw [← hdecode]
      rcases p with ⟨a, positive, swap⟩
      simp only at ha hp hs
      subst a
      subst positive
      subst swap
      rfl
    · right; left
      rw [← hdecode]
      rcases p with ⟨a, positive, swap⟩
      simp only at ha hp hs
      subst a
      subst positive
      subst swap
      rfl
  · right; right
    rcases hc with ⟨ha, hp, hs⟩
    rw [← hdecode]
    rcases p with ⟨a, positive, swap⟩
    simp only at ha hp hs
    subst positive
    subst swap
    exact odd_reflection_conjugate_to_one n hn hn3 a ha

structure ThreeConjugacyClasses (n : Nat) (hn : n % 2 = 1) (hn3 : 3 ≤ n) where
  first : ModelAut n
  second : ModelAut n
  third : ModelAut n
  first_strong : IsStrong n hn first
  second_strong : IsStrong n hn second
  third_strong : IsStrong n hn third
  exhaustive : ∀ g, IsStrong n hn g →
    g = first ∨ g = second ∨ Conjugates n third g
  first_second_distinct : ¬Conjugates n first second
  first_third_distinct : ¬Conjugates n first third
  second_third_distinct : ¬Conjugates n second third

def exact_three_strong_classes (n : Nat) (hn : n % 2 = 1) (hn3 : 3 ≤ n) :
    ThreeConjugacyClasses n hn hn3 where
  first := rotationModelIso n (halfTurn n (by omega)) false
  second := rotationModelIso n (halfTurn n (by omega)) true
  third := reflectionModelIso n (oneIndex n (by omega)) true
  first_strong := strong_halfTurn n hn hn3 false
  second_strong := strong_halfTurn n hn hn3 true
  third_strong := strong_odd_swapped_reflection n hn _ (by simp [oneIndex, bit])
  exhaustive := every_strong_in_three_classes n hn hn3
  first_second_distinct := halfTurn_classes_distinct n hn hn3
  first_third_distinct := halfTurn_reflection_classes_distinct n hn hn3 false
  second_third_distinct := halfTurn_reflection_classes_distinct n hn hn3 true

def firstSwitch (n : Nat) (hn : n % 2 = 1) (hn3 : 3 ≤ n) :
    Switch (modelGraph n hn) :=
  strongSwitchOf n hn (rotationModelIso n (halfTurn n (by omega)) false)
    (strong_halfTurn n hn hn3 false)

def secondSwitch (n : Nat) (hn : n % 2 = 1) (hn3 : 3 ≤ n) :
    Switch (modelGraph n hn) :=
  strongSwitchOf n hn (rotationModelIso n (halfTurn n (by omega)) true)
    (strong_halfTurn n hn hn3 true)

def thirdSwitch (n : Nat) (hn : n % 2 = 1) (hn3 : 3 ≤ n) :
    Switch (modelGraph n hn) :=
  strongSwitchOf n hn (reflectionModelIso n (oneIndex n (by omega)) true)
    (strong_odd_swapped_reflection n hn _ (by simp [oneIndex, bit]))

theorem secondSwitch_is_original (n : Nat) (hn : n % 2 = 1) (hn3 : 3 ≤ n)
    (x : Coord n) :
    (secondSwitch n hn hn3).map x = (originalStrongDeck n hn).map x := by
  change (rotationModelIso n (halfTurn n (by omega)) true).forward x = coordinateDeck n x
  cases x with
  | X t | Y t | A t =>
      change (dihedralModelIso n (halfTurn n (by omega)) true true).forward _ = _
      rw [parameter_forward]
      simp [dihedralIso, rotationIso, dataAction, coordinateDeck, rotation_halfTurn]
  | Z s =>
      simp [rotation_forward_Z, centreResidue_halfTurn, rotation_centreHalfTurn,
        coordinateDeck]

theorem fold_iso_of_conjugates (n : Nat) (hn : n % 2 = 1)
    (g h : ModelAut n) (hg : IsStrong n hn g) (hh : IsStrong n hn h)
    (hc : Conjugates n g h) :
    Nonempty (GraphIso
      (foldAdj (modelGraph n hn) (strongSwitchOf n hn g hg))
      (foldAdj (modelGraph n hn) (strongSwitchOf n hn h hh))) := by
  apply (model_folds_isomorphic_iff_conjugate n hn _ _).mpr
  exact hc

def identityModelAut (n : Nat) : ModelAut n where
  forward := id
  backward := id
  left_inv := by intro x; rfl
  right_inv := by intro x; rfl
  preserves := by intro x y; rfl

theorem conjugates_refl (n : Nat) (g : ModelAut n) : Conjugates n g g := by
  refine ⟨identityModelAut n, ?_⟩
  intro x
  rfl

theorem every_strong_fold_in_three_classes (n : Nat) (hn : n % 2 = 1)
    (hn3 : 3 ≤ n) (g : ModelAut n) (hg : IsStrong n hn g) :
    Nonempty (GraphIso (foldAdj (modelGraph n hn) (firstSwitch n hn hn3))
      (foldAdj (modelGraph n hn) (strongSwitchOf n hn g hg))) ∨
    Nonempty (GraphIso (foldAdj (modelGraph n hn) (secondSwitch n hn hn3))
      (foldAdj (modelGraph n hn) (strongSwitchOf n hn g hg))) ∨
    Nonempty (GraphIso (foldAdj (modelGraph n hn) (thirdSwitch n hn hn3))
      (foldAdj (modelGraph n hn) (strongSwitchOf n hn g hg))) := by
  rcases every_strong_in_three_classes n hn hn3 g hg with h | h | h
  · left
    subst g
    exact fold_iso_of_conjugates n hn _ _ _ _ (conjugates_refl n _)
  · right; left
    subst g
    exact fold_iso_of_conjugates n hn _ _ _ _ (conjugates_refl n _)
  · right; right
    exact fold_iso_of_conjugates n hn _ _ _ _ h

theorem first_second_folds_distinct (n : Nat) (hn : n % 2 = 1) (hn3 : 3 ≤ n) :
    ¬Nonempty (GraphIso (foldAdj (modelGraph n hn) (firstSwitch n hn hn3))
      (foldAdj (modelGraph n hn) (secondSwitch n hn hn3))) := by
  intro h
  have hc := (model_folds_isomorphic_iff_conjugate n hn _ _).mp h
  exact halfTurn_classes_distinct n hn hn3 hc

theorem first_third_folds_distinct (n : Nat) (hn : n % 2 = 1) (hn3 : 3 ≤ n) :
    ¬Nonempty (GraphIso (foldAdj (modelGraph n hn) (firstSwitch n hn hn3))
      (foldAdj (modelGraph n hn) (thirdSwitch n hn hn3))) := by
  intro h
  have hc := (model_folds_isomorphic_iff_conjugate n hn _ _).mp h
  exact halfTurn_reflection_classes_distinct n hn hn3 false hc

theorem second_third_folds_distinct (n : Nat) (hn : n % 2 = 1) (hn3 : 3 ≤ n) :
    ¬Nonempty (GraphIso (foldAdj (modelGraph n hn) (secondSwitch n hn hn3))
      (foldAdj (modelGraph n hn) (thirdSwitch n hn hn3))) := by
  intro h
  have hc := (model_folds_isomorphic_iff_conjugate n hn _ _).mp h
  exact halfTurn_reflection_classes_distinct n hn hn3 true hc

structure ExactTwoCousinCertificate (n : Nat) (hn : n % 2 = 1) (hn3 : 3 ≤ n) where
  original : Switch (modelGraph n hn)
  cousinOne : Switch (modelGraph n hn)
  cousinTwo : Switch (modelGraph n hn)
  original_is_deck : ∀ x, original.map x = (originalStrongDeck n hn).map x
  exhaustive : ∀ g hg,
    Nonempty (GraphIso (foldAdj (modelGraph n hn) cousinOne)
      (foldAdj (modelGraph n hn) (strongSwitchOf n hn g hg))) ∨
    Nonempty (GraphIso (foldAdj (modelGraph n hn) original)
      (foldAdj (modelGraph n hn) (strongSwitchOf n hn g hg))) ∨
    Nonempty (GraphIso (foldAdj (modelGraph n hn) cousinTwo)
      (foldAdj (modelGraph n hn) (strongSwitchOf n hn g hg)))
  original_ne_cousinOne : ¬Nonempty (GraphIso
    (foldAdj (modelGraph n hn) original) (foldAdj (modelGraph n hn) cousinOne))
  original_ne_cousinTwo : ¬Nonempty (GraphIso
    (foldAdj (modelGraph n hn) original) (foldAdj (modelGraph n hn) cousinTwo))
  cousins_distinct : ¬Nonempty (GraphIso
    (foldAdj (modelGraph n hn) cousinOne) (foldAdj (modelGraph n hn) cousinTwo))

def exactly_two_cousin_folds (n : Nat) (hn : n % 2 = 1) (hn3 : 3 ≤ n) :
    ExactTwoCousinCertificate n hn hn3 where
  original := secondSwitch n hn hn3
  cousinOne := firstSwitch n hn hn3
  cousinTwo := thirdSwitch n hn hn3
  original_is_deck := secondSwitch_is_original n hn hn3
  exhaustive := every_strong_fold_in_three_classes n hn hn3
  original_ne_cousinOne := by
    intro h
    rcases h with ⟨h⟩
    exact first_second_folds_distinct n hn hn3 ⟨inverseIso h⟩
  original_ne_cousinTwo := second_third_folds_distinct n hn hn3
  cousins_distinct := first_third_folds_distinct n hn hn3

#print axioms rotation_halfShift_commute
#print axioms reflection_halfShift_commute
#print axioms halfTurn_central
#print axioms conjugate_to_halfTurn_is_equal
#print axioms odd_reflection_conjugacy_index
#print axioms odd_reflection_conjugate_to_one
#print axioms halfTurn_classes_distinct
#print axioms halfTurn_reflection_classes_distinct
#print axioms every_strong_in_three_classes
#print axioms exact_three_strong_classes
#print axioms secondSwitch_is_original
#print axioms every_strong_fold_in_three_classes
#print axioms first_second_folds_distinct
#print axioms first_third_folds_distinct
#print axioms second_third_folds_distinct
#print axioms exactly_two_cousin_folds

end Struct2.StrongConjugacy
