import CycleActions

/-!
Construct the actual dihedral model automorphism family and prove that it
exhausts all actual automorphisms. The lower-bound construction verifies
centre-residue compatibility; it is not inferred from the upper bound.
-/

set_option Elab.async false
set_option maxHeartbeats 12000000
set_option maxRecDepth 20000

namespace Struct2.ModelActions

open OddCoordinates ModelStructure SixCycleInvariant StrongFold RingAction CycleRigidity CycleActions

theorem centreResidue_val (n : Nat) (t : RingIndex n) :
    (centreResidue n t).val =
      if t.val < n + n then t.val
      else if t.val < (n + n) + (n + n) then t.val - (n + n)
      else t.val - ((n + n) + (n + n)) := by
  unfold centreResidue
  split
  · rfl
  · split <;> rfl

theorem residue_rotation (n : Nat) (a t : RingIndex n) :
    centreResidue n (rotation (3 * n) a t) =
      rotation n (centreResidue n a) (centreResidue n t) := by
  apply Fin.ext
  have ha := a.isLt
  have ht := t.isLt
  simp only [centreResidue_val, rotation_val]
  cyclic_cases

theorem residue_reflection (n : Nat) (a t : RingIndex n) :
    centreResidue n (reflection (3 * n) a t) =
      reflection n (centreResidue n a) (centreResidue n t) := by
  apply Fin.ext
  have ha := a.isLt
  have ht := t.isLt
  simp only [centreResidue_val, reflection_val]
  cyclic_cases

theorem iso_forward_eq_iff {V W : Type} {A : V → V → Prop} {B : W → W → Prop}
    (g : GraphIso A B) (t u : V) : g.forward t = g.forward u ↔ t = u := by
  exact ⟨iso_forward_injective g t u, congrArg g.forward⟩

def rawAction (n : Nat) (p : RingIndex n → RingIndex n)
    (c : Fin (n + n) → Fin (n + n)) (swap : Bool) : Coord n → Coord n
  | .X t => if swap then .Y (p t) else .X (p t)
  | .Y t => if swap then .X (p t) else .Y (p t)
  | .A t => .A (p t)
  | .Z s => .Z (c s)

def compatibleModelIso (n : Nat) (p : CycleIso (3 * n)) (c : CycleIso n)
    (hf : ∀ t, centreResidue n (p.forward t) = c.forward (centreResidue n t))
    (swap : Bool) : ModelAut n where
  forward := rawAction n p.forward c.forward swap
  backward := rawAction n p.backward c.backward swap
  left_inv := by
    intro v
    cases v <;> cases swap <;> simp only [rawAction, Bool.false_eq_true, ↓reduceIte,
      p.left_inv, c.left_inv]
  right_inv := by
    intro v
    cases v <;> cases swap <;> simp only [rawAction, Bool.false_eq_true, ↓reduceIte,
      p.right_inv, c.right_inv]
  preserves := by
    intro v w
    cases v <;> cases w <;> cases swap <;>
      simp only [rawAction, Bool.false_eq_true, ↓reduceIte, coordinateAdj,
        p.preserves, hf, iso_forward_eq_iff p, iso_forward_eq_iff c]

theorem compatible_forward_data (n : Nat) (p : CycleIso (3 * n)) (c : CycleIso n)
    (hf : ∀ t, centreResidue n (p.forward t) = c.forward (centreResidue n t))
    (swap : Bool) (v : Coord n) :
    (compatibleModelIso n p c hf swap).forward v = dataAction n p.forward swap v := by
  cases v with
  | X t => rfl
  | Y t => rfl
  | A t => rfl
  | Z s =>
    have he := hf (liftCentre n s)
    rw [centreResidue_lift] at he
    exact congrArg Coord.Z he.symm

def rotationModelIso (n : Nat) (a : RingIndex n) (swap : Bool) : ModelAut n :=
  compatibleModelIso n (rotationIso (3 * n) a)
    (rotationIso n (centreResidue n a)) (residue_rotation n a) swap

def reflectionModelIso (n : Nat) (a : RingIndex n) (swap : Bool) : ModelAut n :=
  compatibleModelIso n (reflectionIso (3 * n) a)
    (reflectionIso n (centreResidue n a)) (residue_reflection n a) swap

def dihedralModelIso (n : Nat) (a : RingIndex n) (positive swap : Bool) : ModelAut n :=
  if positive then rotationModelIso n a swap else reflectionModelIso n a swap

theorem parameter_forward (n : Nat) (a : RingIndex n) (positive swap : Bool) (v : Coord n) :
    (dihedralModelIso n a positive swap).forward v =
      dataAction n (dihedralIso (3 * n) a positive).forward swap v := by
  cases positive <;> simp only [dihedralModelIso, dihedralIso, Bool.false_eq_true, ↓reduceIte]
  · exact compatible_forward_data n _ _ _ swap v
  · exact compatible_forward_data n _ _ _ swap v

theorem every_model_automorphism_dihedral (n : Nat) (hn : 2 ≤ n) (g : ModelAut n) :
    g = dihedralModelIso n
      ((inducedRingIso n hn g).forward (ringZero n hn))
      (direction (3 * n) (by omega) (inducedRingIso n hn g))
      (ringSwap n g (ringZero n hn)) := by
  apply graphIso_ext
  intro v
  rw [every_automorphism_synchronized n hn g v]
  have hp := cycle_iso_dihedral (3 * n) (by omega) (inducedRingIso n hn g)
  have he := congrArg (fun p : CycleIso (3 * n) =>
    dataAction n p.forward (ringSwap n g (ringZero n hn)) v) hp
  exact he.trans (parameter_forward n _ _ _ v).symm

theorem parameter_leafImage (n : Nat) (a : RingIndex n) (positive swap : Bool) (t : RingIndex n) :
    leafImage n (dihedralModelIso n a positive swap) t =
      (dihedralIso (3 * n) a positive).forward t := by
  unfold leafImage
  rw [parameter_forward]
  rfl

theorem parameter_inducedRingIso (n : Nat) (hn : 2 ≤ n) (a : RingIndex n) (positive swap : Bool) :
    inducedRingIso n hn (dihedralModelIso n a positive swap) =
      dihedralIso (3 * n) a positive := by
  apply graphIso_ext
  exact parameter_leafImage n a positive swap

theorem parameter_ringSwap (n : Nat) (a : RingIndex n) (positive swap : Bool) (t : RingIndex n) :
    ringSwap n (dihedralModelIso n a positive swap) t = swap := by
  unfold ringSwap
  rw [parameter_forward]
  cases swap <;> rfl

theorem parameter_code (n : Nat) (hn : 2 ≤ n) (a : RingIndex n) (positive swap : Bool) :
    automorphismCode n hn (dihedralModelIso n a positive swap) = (a, positive, swap) := by
  unfold automorphismCode
  rw [parameter_inducedRingIso, parameter_ringSwap]
  cases positive <;> simp only [dihedralIso, Bool.false_eq_true, ↓reduceIte]
  · rw [reflection_direction]
    change (reflection (3 * n) a (cycleZero (3 * n) (by omega)), false, swap) = (a, false, swap)
    rw [reflection_zero]
  · rw [rotation_direction]
    change (rotation (3 * n) a (cycleZero (3 * n) (by omega)), true, swap) = (a, true, swap)
    rw [rotation_zero]

abbrev Parameters (n : Nat) := RingIndex n × Bool × Bool

def parametersToAut (n : Nat) (p : Parameters n) : ModelAut n :=
  dihedralModelIso n p.1 p.2.1 p.2.2

theorem parametersToAut_left_inv (n : Nat) (hn : 2 ≤ n) (p : Parameters n) :
    automorphismCode n hn (parametersToAut n p) = p := by
  exact parameter_code n hn p.1 p.2.1 p.2.2

theorem parametersToAut_right_inv (n : Nat) (hn : 2 ≤ n) (g : ModelAut n) :
    parametersToAut n (automorphismCode n hn g) = g :=
  (every_model_automorphism_dihedral n hn g).symm

theorem parametersToAut_injective (n : Nat) (hn : 2 ≤ n) (p q : Parameters n)
    (he : parametersToAut n p = parametersToAut n q) : p = q := by
  have hi := congrArg (automorphismCode n hn) he
  simpa only [parametersToAut_left_inv] using hi

def modelAutToOriginal (n : Nat) (hn : n % 2 = 1) (g : ModelAut n) :
    GraphIso (coverAdj n) (coverAdj n) where
  forward := fun v => toCover n (g.forward (fromCover n v))
  backward := fun v => toCover n (g.backward (fromCover n v))
  left_inv := by
    intro v
    simp only [fromCover_toCover n hn, g.left_inv, toCover_fromCover n hn]
  right_inv := by
    intro v
    simp only [fromCover_toCover n hn, g.right_inv, toCover_fromCover n hn]
  preserves := by
    intro v w
    have hi := toCover_adjacency n hn (fromCover n v) (fromCover n w)
    simp only [toCover_fromCover n hn] at hi
    exact (toCover_adjacency n hn _ _).trans ((g.preserves _ _).trans hi.symm)

theorem modelAutToOriginal_left_inv (n : Nat) (hn : n % 2 = 1) (g : ModelAut n) :
    originalAutToModel n hn (modelAutToOriginal n hn g) = g := by
  apply graphIso_ext
  intro v
  dsimp [originalAutToModel, modelAutToOriginal]
  simp only [fromCover_toCover n hn]

theorem modelAutToOriginal_right_inv (n : Nat) (hn : n % 2 = 1)
    (g : GraphIso (coverAdj n) (coverAdj n)) :
    modelAutToOriginal n hn (originalAutToModel n hn g) = g := by
  apply graphIso_ext
  intro v
  dsimp [originalAutToModel, modelAutToOriginal]
  simp only [toCover_fromCover n hn]

def originalParametersToAut (n : Nat) (hn : n % 2 = 1) (p : Parameters n) :
    GraphIso (coverAdj n) (coverAdj n) :=
  modelAutToOriginal n hn (parametersToAut n p)

def originalAutParameters (n : Nat) (hn : n % 2 = 1) (hlarge : 3 ≤ n)
    (g : GraphIso (coverAdj n) (coverAdj n)) : Parameters n :=
  automorphismCode n (by omega) (originalAutToModel n hn g)

theorem originalParametersToAut_left_inv (n : Nat) (hn : n % 2 = 1) (hlarge : 3 ≤ n)
    (p : Parameters n) :
    originalAutParameters n hn hlarge (originalParametersToAut n hn p) = p := by
  unfold originalAutParameters originalParametersToAut
  rw [modelAutToOriginal_left_inv, parametersToAut_left_inv]

theorem originalParametersToAut_right_inv (n : Nat) (hn : n % 2 = 1) (hlarge : 3 ≤ n)
    (g : GraphIso (coverAdj n) (coverAdj n)) :
    originalParametersToAut n hn (originalAutParameters n hn hlarge g) = g := by
  unfold originalAutParameters originalParametersToAut
  rw [parametersToAut_right_inv, modelAutToOriginal_right_inv]

def unpackCode (N : Nat) (c : Fin (4 * N)) : Fin N × Bool × Bool :=
  (⟨c.val / 4, by have hc := c.isLt; omega⟩,
    decide (2 ≤ c.val % 4), decide (c.val % 2 = 1))

theorem pack_unpackCode (N : Nat) (c : Fin (4 * N)) : packCode N (unpackCode N c) = c := by
  apply Fin.ext
  by_cases hd : 2 ≤ c.val % 4 <;> by_cases hs : c.val % 2 = 1 <;>
    simp only [packCode, unpackCode, hd, hs, decide_true, decide_false,
      Bool.false_eq_true, ↓reduceIte]
  all_goals omega

theorem unpack_packCode (N : Nat) (p : Fin N × Bool × Bool) :
    unpackCode N (packCode N p) = p := by
  apply packCode_injective N
  exact pack_unpackCode N (packCode N p)

def modelNumericToAut (n : Nat) (c : Fin (24 * n)) : ModelAut n :=
  let c' : Fin (4 * ((3 * n) + (3 * n))) := ⟨c.val, by have hc := c.isLt; omega⟩
  parametersToAut n (unpackCode ((3 * n) + (3 * n)) c')

theorem model_numeric_code_left_inv (n : Nat) (hn : 2 ≤ n) (c : Fin (24 * n)) :
    finiteAutCode n hn (modelNumericToAut n c) = c := by
  apply Fin.ext
  change (packCode ((3 * n) + (3 * n))
    (automorphismCode n hn (parametersToAut n (unpackCode ((3 * n) + (3 * n)) _)))).val = c.val
  rw [parametersToAut_left_inv, pack_unpackCode]

theorem model_numeric_code_right_inv (n : Nat) (hn : 2 ≤ n) (g : ModelAut n) :
    modelNumericToAut n (finiteAutCode n hn g) = g := by
  apply actual_automorphism_embeds_in_24n n hn
  exact model_numeric_code_left_inv n hn _

def originalNumericToAut (n : Nat) (hn : n % 2 = 1) (c : Fin (24 * n)) :
    GraphIso (coverAdj n) (coverAdj n) :=
  modelAutToOriginal n hn (modelNumericToAut n c)

theorem original_numeric_code_left_inv (n : Nat) (hn : n % 2 = 1) (hlarge : 3 ≤ n)
    (c : Fin (24 * n)) :
    originalFiniteAutCode n hn hlarge (originalNumericToAut n hn c) = c := by
  change finiteAutCode n (by omega)
    (originalAutToModel n hn (modelAutToOriginal n hn (modelNumericToAut n c))) = c
  rw [modelAutToOriginal_left_inv, model_numeric_code_left_inv]

theorem original_numeric_code_right_inv (n : Nat) (hn : n % 2 = 1) (hlarge : 3 ≤ n)
    (g : GraphIso (coverAdj n) (coverAdj n)) :
    originalNumericToAut n hn (originalFiniteAutCode n hn hlarge g) = g := by
  apply originalCDC_automorphism_embeds_in_24n n hn hlarge
  exact original_numeric_code_left_inv n hn hlarge _

structure FiniteParametrization (V : Type) (N : Nat) where
  encode : V → Fin N
  decode : Fin N → V
  encode_decode : ∀ c, encode (decode c) = c
  decode_encode : ∀ v, decode (encode v) = v

def originalCDC_exact_24n (n : Nat) (hn : n % 2 = 1) (hlarge : 3 ≤ n) :
    FiniteParametrization (GraphIso (coverAdj n) (coverAdj n)) (24 * n) where
  encode := originalFiniteAutCode n hn hlarge
  decode := originalNumericToAut n hn
  encode_decode := original_numeric_code_left_inv n hn hlarge
  decode_encode := original_numeric_code_right_inv n hn hlarge

#print axioms residue_rotation
#print axioms residue_reflection
#print axioms compatibleModelIso
#print axioms rotationModelIso
#print axioms reflectionModelIso
#print axioms parameter_forward
#print axioms every_model_automorphism_dihedral
#print axioms parameter_inducedRingIso
#print axioms parameter_code
#print axioms parametersToAut_left_inv
#print axioms parametersToAut_right_inv
#print axioms parametersToAut_injective
#print axioms modelAutToOriginal
#print axioms modelAutToOriginal_left_inv
#print axioms modelAutToOriginal_right_inv
#print axioms originalParametersToAut_left_inv
#print axioms originalParametersToAut_right_inv
#print axioms pack_unpackCode
#print axioms unpack_packCode
#print axioms model_numeric_code_left_inv
#print axioms model_numeric_code_right_inv
#print axioms original_numeric_code_left_inv
#print axioms original_numeric_code_right_inv
#print axioms originalCDC_exact_24n

end Struct2.ModelActions
