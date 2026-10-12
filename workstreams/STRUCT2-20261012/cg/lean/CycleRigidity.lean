import RingAction

/-!
An arbitrary adjacency automorphism of a cycle is determined by the images
of two consecutive vertices. The data reduce to one cyclic index and a
Boolean direction. Together with synchronized ring actions this yields an
injective encoding of every actual CG model automorphism into 24n codes.
Existence of every code and the strong-switch classification are separate.
-/

set_option Elab.async false
set_option maxHeartbeats 6000000

namespace Struct2.CycleRigidity

open OddCoordinates SixCycleInvariant StrongFold RingAction

abbrev CycleIso (m : Nat) := GraphIso (ringAdj m) (ringAdj m)

def cycleZero (m : Nat) (hm : 2 ≤ m) : Fin (m + m) := ⟨0, by omega⟩
def cycleOne (m : Nat) (hm : 2 ≤ m) : Fin (m + m) := ⟨1, by omega⟩

theorem cycle_zero_one_adjacent (m : Nat) (hm : 2 ≤ m) :
    ringAdj m (cycleZero m hm) (cycleOne m hm) := by
  left
  apply Fin.ext
  simp [cycleZero, cycleOne, cycleNext, show 1 < m + m by omega]

theorem other_neighbour_unique (m : Nat) (a b c d : Fin (m + m))
    (hba : ringAdj m b a) (hbc : ringAdj m b c) (hbd : ringAdj m b d)
    (hac : a ≠ c) (had : a ≠ d) : c = d := by
  rcases hba with hba | hba <;> rcases hbc with hbc | hbc <;> rcases hbd with hbd | hbd
  all_goals first
    | exact hbc.symm.trans hbd
    | exact cycleNext_injective m c d (hbc.trans hbd.symm)
    | exact False.elim (hac (hba.symm.trans hbc))
    | exact False.elim (had (hba.symm.trans hbd))
    | exact False.elim (hac (cycleNext_injective m a c (hba.trans hbc.symm)))
    | exact False.elim (had (cycleNext_injective m a d (hba.trans hbd.symm)))

theorem cycle_iso_determined_by_zero_one (m : Nat) (hm : 2 ≤ m)
    (g h : CycleIso m)
    (hz : g.forward (cycleZero m hm) = h.forward (cycleZero m hm))
    (ho : g.forward (cycleOne m hm) = h.forward (cycleOne m hm))
    (t : Fin (m + m)) : g.forward t = h.forward t := by
  have all : ∀ a (ha : a < m + m),
      g.forward ⟨a, ha⟩ = h.forward ⟨a, ha⟩ := by
    intro a
    induction a using Nat.strongRecOn with
    | ind a ih =>
      intro ha
      match a with
      | 0 => exact hz
      | 1 => exact ho
      | b + 2 =>
        have hb : b < m + m := by omega
        have hb1 : b + 1 < m + m := by omega
        let prev : Fin (m + m) := ⟨b, hb⟩
        let mid : Fin (m + m) := ⟨b + 1, hb1⟩
        let curr : Fin (m + m) := ⟨b + 2, ha⟩
        have hi0 : g.forward prev = h.forward prev := ih b (by omega) hb
        have hi1 : g.forward mid = h.forward mid := ih (b + 1) (by omega) hb1
        have e0 : cycleNext m prev = mid := by
          apply Fin.ext
          simp [cycleNext, prev, mid, hb1]
        have e1 : cycleNext m mid = curr := by
          apply Fin.ext
          simp [cycleNext, mid, curr, ha]
        have hba : ringAdj m (h.forward mid) (h.forward prev) :=
          (h.preserves _ _).mpr (Or.inr e0)
        have hbc : ringAdj m (h.forward mid) (g.forward curr) := by
          rw [← hi1]
          exact (g.preserves _ _).mpr (Or.inl e1)
        have hbd : ringAdj m (h.forward mid) (h.forward curr) :=
          (h.preserves _ _).mpr (Or.inl e1)
        have hac : h.forward prev ≠ g.forward curr := by
          intro he
          rw [← hi0] at he
          have hv := congrArg Fin.val (iso_forward_injective g _ _ he)
          dsimp [prev, curr] at hv
          omega
        have had : h.forward prev ≠ h.forward curr := by
          intro he
          have hv := congrArg Fin.val (iso_forward_injective h _ _ he)
          dsimp [prev, curr] at hv
          omega
        exact other_neighbour_unique m _ _ _ _ hba hbc hbd hac had
  exact all t.val t.isLt

def direction (m : Nat) (hm : 2 ≤ m) (g : CycleIso m) : Bool :=
  decide (cycleNext m (g.forward (cycleZero m hm)) = g.forward (cycleOne m hm))

theorem direction_true (m : Nat) (hm : 2 ≤ m) (g : CycleIso m)
    (hd : direction m hm g = true) :
    cycleNext m (g.forward (cycleZero m hm)) = g.forward (cycleOne m hm) := by
  simpa only [direction, decide_eq_true_eq] using hd

theorem direction_false (m : Nat) (hm : 2 ≤ m) (g : CycleIso m)
    (hd : direction m hm g = false) :
    cycleNext m (g.forward (cycleOne m hm)) = g.forward (cycleZero m hm) := by
  have he := (g.preserves _ _).mpr (cycle_zero_one_adjacent m hm)
  rcases he with h | h
  · have ht : direction m hm g = true := by simp [direction, h]
    rw [ht] at hd
    cases hd
  · exact h

theorem cycle_iso_determined_by_index_direction (m : Nat) (hm : 2 ≤ m)
    (g h : CycleIso m)
    (hz : g.forward (cycleZero m hm) = h.forward (cycleZero m hm))
    (hd : direction m hm g = direction m hm h)
    (t : Fin (m + m)) : g.forward t = h.forward t := by
  apply cycle_iso_determined_by_zero_one m hm g h hz _ t
  cases hg : direction m hm g with
  | false =>
    have hh : direction m hm h = false := hd.symm.trans hg
    apply cycleNext_injective m
    rw [direction_false m hm g hg, direction_false m hm h hh, hz]
  | true =>
    have hh : direction m hm h = true := hd.symm.trans hg
    rw [← direction_true m hm g hg, ← direction_true m hm h hh, hz]

def automorphismCode (n : Nat) (hn : 2 ≤ n) (iso : ModelAut n) :
    RingIndex n × Bool × Bool :=
  ((inducedRingIso n hn iso).forward (ringZero n hn),
    direction (3 * n) (by omega) (inducedRingIso n hn iso),
    ringSwap n iso (ringZero n hn))

theorem graphIso_ext {V W : Type} {A : V → V → Prop} {B : W → W → Prop}
    (g h : GraphIso A B) (he : ∀ v, g.forward v = h.forward v) : g = h := by
  have hf : g.forward = h.forward := funext he
  have hb : g.backward = h.backward := by
    funext w
    have hi := g.left_inv (h.backward w)
    rw [hf, h.right_inv] at hi
    exact hi
  cases g
  cases h
  dsimp at hf hb
  cases hf
  cases hb
  rfl

theorem actual_automorphism_code_injective (n : Nat) (hn : 2 ≤ n)
    (g h : ModelAut n) (he : automorphismCode n hn g = automorphismCode n hn h) : g = h := by
  have hz := congrArg Prod.fst he
  have hd := congrArg (fun p : RingIndex n × Bool × Bool => p.2.1) he
  have hs := congrArg (fun p : RingIndex n × Bool × Bool => p.2.2) he
  apply graphIso_ext g h
  apply automorphism_determined_by_ring_data n hn g h
  · intro t
    apply cycle_iso_determined_by_index_direction (3 * n) (by omega)
      (inducedRingIso n hn g) (inducedRingIso n hn h) _ hd t
    exact hz
  · exact hs

def packCode (N : Nat) (p : Fin N × Bool × Bool) : Fin (4 * N) :=
  ⟨4 * p.1.val + 2 * (if p.2.1 then 1 else 0) + (if p.2.2 then 1 else 0), by
    have hp := p.1.isLt
    cases p.2.1 <;> cases p.2.2 <;> dsimp <;> omega⟩

theorem packCode_injective (N : Nat) (p q : Fin N × Bool × Bool)
    (he : packCode N p = packCode N q) : p = q := by
  rcases p with ⟨⟨a, ha⟩, d, s⟩
  rcases q with ⟨⟨b, hb⟩, e, t⟩
  have hv := congrArg Fin.val he
  cases d <;> cases s <;> cases e <;> cases t <;> dsimp [packCode] at hv
  all_goals have hab : a = b := by omega
  all_goals subst b
  all_goals first | rfl | omega

def finiteAutCode (n : Nat) (hn : 2 ≤ n) (g : ModelAut n) : Fin (24 * n) :=
  let p := packCode ((3 * n) + (3 * n)) (automorphismCode n hn g)
  ⟨p.val, by have hp := p.isLt; omega⟩

theorem actual_automorphism_embeds_in_24n (n : Nat) (hn : 2 ≤ n)
    (g h : ModelAut n) (he : finiteAutCode n hn g = finiteAutCode n hn h) : g = h := by
  apply actual_automorphism_code_injective n hn g h
  apply packCode_injective ((3 * n) + (3 * n))
  apply Fin.ext
  have hv := congrArg (fun x : Fin (24 * n) => x.val) he
  exact hv

def originalAutToModel (n : Nat) (hn : n % 2 = 1)
    (g : GraphIso (coverAdj n) (coverAdj n)) : ModelAut n where
  forward := fun v => fromCover n (g.forward (toCover n v))
  backward := fun v => fromCover n (g.backward (toCover n v))
  left_inv := by
    intro v
    simp only [toCover_fromCover n hn, g.left_inv, fromCover_toCover n hn]
  right_inv := by
    intro v
    simp only [toCover_fromCover n hn, g.right_inv, fromCover_toCover n hn]
  preserves := by
    intro v w
    have hi := toCover_adjacency n hn
      (fromCover n (g.forward (toCover n v))) (fromCover n (g.forward (toCover n w)))
    simp only [toCover_fromCover n hn] at hi
    exact hi.symm.trans ((g.preserves _ _).trans (toCover_adjacency n hn v w))

def originalFiniteAutCode (n : Nat) (hn : n % 2 = 1) (hlarge : 3 ≤ n)
    (g : GraphIso (coverAdj n) (coverAdj n)) : Fin (24 * n) :=
  finiteAutCode n (by omega) (originalAutToModel n hn g)

theorem originalCDC_automorphism_embeds_in_24n (n : Nat) (hn : n % 2 = 1)
    (hlarge : 3 ≤ n) (g h : GraphIso (coverAdj n) (coverAdj n))
    (he : originalFiniteAutCode n hn hlarge g = originalFiniteAutCode n hn hlarge h) :
    g = h := by
  have hi := actual_automorphism_embeds_in_24n n (by omega)
    (originalAutToModel n hn g) (originalAutToModel n hn h) he
  apply graphIso_ext g h
  intro v
  have hm := congrArg (fun p : ModelAut n => p.forward (fromCover n v)) hi
  dsimp [originalAutToModel] at hm
  simp only [toCover_fromCover n hn] at hm
  have hc := congrArg (toCover n) hm
  simpa only [toCover_fromCover n hn] using hc

#print axioms other_neighbour_unique
#print axioms cycle_iso_determined_by_zero_one
#print axioms direction_true
#print axioms direction_false
#print axioms cycle_iso_determined_by_index_direction
#print axioms graphIso_ext
#print axioms actual_automorphism_code_injective
#print axioms packCode_injective
#print axioms actual_automorphism_embeds_in_24n
#print axioms originalAutToModel
#print axioms originalCDC_automorphism_embeds_in_24n

end Struct2.CycleRigidity
