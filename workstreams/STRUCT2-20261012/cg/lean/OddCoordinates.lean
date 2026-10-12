import Std

/-!
Universal odd-parameter vertex coordinates for Mizzi's claw graph CDC.
The synchronized ring has size 6*n, written (3*n)+(3*n) to expose its
two halves. These are actual mutually inverse functions, not cardinality
comparisons. Every original adjacency and the deck map are preserved.
The original leaf naming (i,j) is connected by an explicit bijection.
-/

set_option Elab.async false
set_option maxHeartbeats 4000000

namespace Struct2.OddCoordinates

def bit (a : Nat) : Bool := a % 2 == 1

theorem bit_add_odd (a m : Nat) (hm : m % 2 = 1) :
    bit (a + m) = !bit a := by
  have ha : a % 2 = 0 ∨ a % 2 = 1 := by omega
  rcases ha with ha | ha
  · have hsum : (a + m) % 2 = 1 := by omega
    simp [bit, ha, hsum]
  · have hsum : (a + m) % 2 = 0 := by omega
    simp [bit, ha, hsum]

def halfShift (m : Nat) (a : Fin (m + m)) : Fin (m + m) :=
  if h : a.val < m then ⟨a.val + m, by omega⟩
  else ⟨a.val - m, by omega⟩

def reduceHalf (m : Nat) (a : Fin (m + m)) : Fin m :=
  if h : a.val < m then ⟨a.val, h⟩
  else ⟨a.val - m, by omega⟩

def joinHalf (m : Nat) (a : Fin m) (b : Bool) : Fin (m + m) :=
  if bit a.val = b then ⟨a.val, by omega⟩
  else ⟨a.val + m, by omega⟩

theorem halfShift_involutive (m : Nat) (a : Fin (m + m)) :
    halfShift m (halfShift m a) = a := by
  apply Fin.ext
  unfold halfShift
  split <;> split <;> dsimp at * <;> simp_all <;> omega

theorem reduceHalf_shift (m : Nat) (a : Fin (m + m)) :
    reduceHalf m (halfShift m a) = reduceHalf m a := by
  apply Fin.ext
  unfold halfShift reduceHalf
  split <;> split <;> dsimp at * <;> simp_all <;> omega

theorem reduceHalf_is_mod (m : Nat) (a : Fin (m + m)) :
    (reduceHalf m a).val = a.val % m := by
  unfold reduceHalf
  split
  · simp_all [Nat.mod_eq_of_lt]
  · rename_i h
    have hm : m ≤ a.val := by omega
    have hlt : a.val - m < m := by omega
    simp [Nat.mod_eq_sub_mod hm, Nat.mod_eq_of_lt hlt]

theorem halfShift_bit (m : Nat) (hm : m % 2 = 1) (a : Fin (m + m)) :
    bit (halfShift m a).val = !bit a.val := by
  unfold halfShift
  split
  · exact bit_add_odd a.val m hm
  · rename_i h
    have hle : m ≤ a.val := by omega
    have hp := bit_add_odd (a.val - m) m hm
    rw [Nat.sub_add_cancel hle] at hp
    have hn := congrArg Bool.not hp
    simpa using hn.symm

theorem reduceHalf_join (m : Nat) (a : Fin m) (b : Bool) :
    reduceHalf m (joinHalf m a b) = a := by
  apply Fin.ext
  unfold reduceHalf joinHalf
  split <;> split <;> dsimp at * <;> simp_all <;> omega

theorem joinHalf_bit (m : Nat) (hm : m % 2 = 1) (a : Fin m) (b : Bool) :
    bit (joinHalf m a b).val = b := by
  unfold joinHalf
  split
  · assumption
  · rename_i h
    rw [bit_add_odd a.val m hm]
    cases hb : bit a.val <;> cases b <;> simp_all

theorem joinHalf_reduce (m : Nat) (hm : m % 2 = 1) (a : Fin (m + m)) :
    joinHalf m (reduceHalf m a) (bit a.val) = a := by
  apply Fin.ext
  unfold reduceHalf
  split
  · simp [joinHalf]
  · rename_i h
    have hle : m ≤ a.val := by omega
    have hp := bit_add_odd (a.val - m) m hm
    rw [Nat.sub_add_cancel hle] at hp
    have hneq : bit (a.val - m) ≠ bit a.val := by
      rw [hp]
      cases bit (a.val - m) <;> decide
    simp [joinHalf, hneq]
    omega

inductive Base (n : Nat) where
  | ring : Fin ((3 * n) + (3 * n)) → Base n
  | leaf : Fin (3 * n) → Base n
  | centre : Fin n → Base n
  deriving DecidableEq

inductive Coord (n : Nat) where
  | X : Fin ((3 * n) + (3 * n)) → Coord n
  | Y : Fin ((3 * n) + (3 * n)) → Coord n
  | A : Fin ((3 * n) + (3 * n)) → Coord n
  | Z : Fin (n + n) → Coord n
  deriving DecidableEq

abbrev Cover (n : Nat) := Base n × Bool

def toCover (n : Nat) : Coord n → Cover n
  | .X t => (.ring t, bit t.val)
  | .Y t => (.ring (halfShift (3 * n) t), bit t.val)
  | .A t => (.leaf (reduceHalf (3 * n) t), !bit t.val)
  | .Z s => (.centre (reduceHalf n s), bit s.val)

def fromCover (n : Nat) : Cover n → Coord n
  | (.ring t, b) => if b = bit t.val then .X t else .Y (halfShift (3 * n) t)
  | (.leaf a, b) => .A (joinHalf (3 * n) a (!b))
  | (.centre c, b) => .Z (joinHalf n c b)

theorem triple_odd (n : Nat) (hn : n % 2 = 1) : (3 * n) % 2 = 1 := by
  omega

theorem fromCover_toCover (n : Nat) (hn : n % 2 = 1) (x : Coord n) :
    fromCover n (toCover n x) = x := by
  have hk := triple_odd n hn
  cases x with
  | X t => simp [toCover, fromCover]
  | Y t =>
    simp only [toCover, fromCover, halfShift_bit _ hk]
    cases bit t.val <;> simp [halfShift_involutive]
  | A t => simp [toCover, fromCover, joinHalf_reduce _ hk]
  | Z s => simp [toCover, fromCover, joinHalf_reduce _ hn]

theorem toCover_fromCover (n : Nat) (hn : n % 2 = 1) (x : Cover n) :
    toCover n (fromCover n x) = x := by
  have hk := triple_odd n hn
  rcases x with ⟨v, b⟩
  cases v with
  | ring t =>
    by_cases h : b = bit t.val
    · simp [fromCover, toCover, h]
    · simp only [fromCover, h, ↓reduceIte, toCover,
        halfShift_involutive, halfShift_bit _ hk]
      cases hb : bit t.val <;> cases b <;> simp_all
  | leaf a => simp [fromCover, toCover, reduceHalf_join, joinHalf_bit _ hk]
  | centre c => simp [fromCover, toCover, reduceHalf_join, joinHalf_bit _ hn]

theorem toCover_injective (n : Nat) (hn : n % 2 = 1) :
    ∀ x y : Coord n, toCover n x = toCover n y → x = y := by
  intro x y h
  have hi := congrArg (fromCover n) h
  simpa only [fromCover_toCover n hn] using hi

theorem toCover_surjective (n : Nat) (hn : n % 2 = 1) :
    ∀ x : Cover n, ∃ y : Coord n, toCover n y = x := by
  intro x
  exact ⟨fromCover n x, toCover_fromCover n hn x⟩

def deck (n : Nat) (x : Cover n) : Cover n := (x.1, !x.2)

def coordinateDeck (n : Nat) : Coord n → Coord n
  | .X t => .Y (halfShift (3 * n) t)
  | .Y t => .X (halfShift (3 * n) t)
  | .A t => .A (halfShift (3 * n) t)
  | .Z s => .Z (halfShift n s)

theorem coordinateDeck_intertwines (n : Nat) (hn : n % 2 = 1) (x : Coord n) :
    toCover n (coordinateDeck n x) = deck n (toCover n x) := by
  have hk := triple_odd n hn
  cases x <;>
    simp [coordinateDeck, toCover, deck, halfShift_involutive,
      halfShift_bit _ hk, halfShift_bit _ hn, reduceHalf_shift]

/- Original edge semantics and the synchronized cover edge list. -/

def cycleNext (m : Nat) (a : Fin (m + m)) : Fin (m + m) :=
  if h : a.val + 1 < m + m then ⟨a.val + 1, h⟩
  else ⟨0, by omega⟩

def ringAdj (m : Nat) (a b : Fin (m + m)) : Prop :=
  cycleNext m a = b ∨ cycleNext m b = a

theorem cycleNext_bit (m : Nat) (a : Fin (m + m)) :
    bit (cycleNext m a).val = !bit a.val := by
  unfold cycleNext
  split
  · exact bit_add_odd a.val 1 (by decide)
  · rename_i h
    have ha : a.val % 2 = 1 := by omega
    simp [bit, ha]

theorem halfShift_cycleNext (m : Nat) (a : Fin (m + m)) :
    halfShift m (cycleNext m a) = cycleNext m (halfShift m a) := by
  apply Fin.ext
  unfold halfShift cycleNext
  have ha := a.isLt
  split <;> split <;> dsimp at *
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

theorem halfShift_injective (m : Nat) (a b : Fin (m + m))
    (h : halfShift m a = halfShift m b) : a = b := by
  have hi := congrArg (halfShift m) h
  simpa only [halfShift_involutive] using hi

theorem ringAdj_halfShift (m : Nat) (a b : Fin (m + m)) :
    ringAdj m (halfShift m a) (halfShift m b) ↔ ringAdj m a b := by
  unfold ringAdj
  rw [← halfShift_cycleNext, ← halfShift_cycleNext]
  constructor
  · intro h
    rcases h with h | h
    · exact Or.inl (halfShift_injective m _ _ h)
    · exact Or.inr (halfShift_injective m _ _ h)
  · intro h
    rcases h with h | h
    · exact Or.inl (congrArg (halfShift m) h)
    · exact Or.inr (congrArg (halfShift m) h)

theorem ringAdj_bits (m : Nat) (a b : Fin (m + m)) (h : ringAdj m a b) :
    bit a.val ≠ bit b.val := by
  rcases h with h | h
  · have hb : bit b.val = !bit a.val := by rw [← h]; exact cycleNext_bit m a
    rw [hb]
    cases bit a.val <;> decide
  · have ha : bit a.val = !bit b.val := by rw [← h]; exact cycleNext_bit m b
    rw [ha]
    cases bit b.val <;> decide

theorem bit_reduce_eq_iff (m : Nat) (hm : m % 2 = 1)
    (a b : Fin (m + m)) :
    (bit a.val = bit b.val ∧ reduceHalf m a = reduceHalf m b) ↔ a = b := by
  constructor
  · rintro ⟨hb, hr⟩
    calc
      a = joinHalf m (reduceHalf m a) (bit a.val) := (joinHalf_reduce m hm a).symm
      _ = joinHalf m (reduceHalf m b) (bit b.val) := by rw [hb, hr]
      _ = b := joinHalf_reduce m hm b
  · intro h
    subst b
    exact ⟨rfl, rfl⟩

def centreOfLeaf (n : Nat) (a : Fin (3 * n)) : Fin n :=
  if h : a.val < n then ⟨a.val, h⟩
  else if h : a.val < n + n then ⟨a.val - n, by omega⟩
  else ⟨a.val - (n + n), by omega⟩

def centreResidue (n : Nat) (a : Fin ((3 * n) + (3 * n))) : Fin (n + n) :=
  if h : a.val < n + n then ⟨a.val, h⟩
  else if h : a.val < (n + n) + (n + n) then ⟨a.val - (n + n), by omega⟩
  else ⟨a.val - ((n + n) + (n + n)), by omega⟩

theorem centreOfLeaf_is_mod (n : Nat) (a : Fin (3 * n)) :
    (centreOfLeaf n a).val = a.val % n := by
  unfold centreOfLeaf
  split
  · simp_all [Nat.mod_eq_of_lt]
  · rename_i h
    have hle : n ≤ a.val := by omega
    rw [Nat.mod_eq_sub_mod hle]
    split
    · rename_i hsmall
      have hlt : a.val - n < n := by omega
      simp [Nat.mod_eq_of_lt hlt]
    · rename_i hlarge
      have hle2 : n ≤ a.val - n := by omega
      have hlt : a.val - n - n < n := by omega
      rw [Nat.mod_eq_sub_mod hle2, Nat.mod_eq_of_lt hlt]
      dsimp
      omega

theorem centreResidue_bit (n : Nat) (a : Fin ((3 * n) + (3 * n))) :
    bit (centreResidue n a).val = bit a.val := by
  unfold centreResidue
  split
  · rfl
  · split
    · have hmod : (a.val - (n + n)) % 2 = a.val % 2 := by omega
      simp [bit, hmod]
    · have hmod : (a.val - ((n + n) + (n + n))) % 2 = a.val % 2 := by omega
      simp [bit, hmod]

theorem centreOfLeaf_coordinate (n : Nat) (a : Fin ((3 * n) + (3 * n))) :
    centreOfLeaf n (reduceHalf (3 * n) a) = reduceHalf n (centreResidue n a) := by
  apply Fin.ext
  have ha := a.isLt
  unfold centreOfLeaf reduceHalf centreResidue
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

def baseAdj (n : Nat) : Base n → Base n → Prop
  | .ring t, .ring u => ringAdj (3 * n) t u
  | .ring t, .leaf a => reduceHalf (3 * n) t = a
  | .leaf a, .ring t => a = reduceHalf (3 * n) t
  | .leaf a, .centre c => centreOfLeaf n a = c
  | .centre c, .leaf a => c = centreOfLeaf n a
  | _, _ => False

def coverAdj (n : Nat) (x y : Cover n) : Prop :=
  x.2 ≠ y.2 ∧ baseAdj n x.1 y.1

def coordinateAdj (n : Nat) : Coord n → Coord n → Prop
  | .X t, .X u => ringAdj (3 * n) t u
  | .Y t, .Y u => ringAdj (3 * n) t u
  | .X t, .A u => t = u
  | .Y t, .A u => t = u
  | .A t, .X u => t = u
  | .A t, .Y u => t = u
  | .A t, .Z s => centreResidue n t = s
  | .Z s, .A t => s = centreResidue n t
  | _, _ => False

theorem cycleNext_is_mod (m : Nat) (a : Fin (m + m)) :
    (cycleNext m a).val = (a.val + 1) % (m + m) := by
  unfold cycleNext
  split
  · simp_all [Nat.mod_eq_of_lt]
  · rename_i h
    have he : a.val + 1 = m + m := by omega
    simp [he]

theorem centreResidue_is_mod (n : Nat) (a : Fin ((3 * n) + (3 * n))) :
    (centreResidue n a).val = a.val % (n + n) := by
  unfold centreResidue
  split
  · simp_all [Nat.mod_eq_of_lt]
  · rename_i h
    have hle : n + n ≤ a.val := by omega
    rw [Nat.mod_eq_sub_mod hle]
    split
    · have hlt : a.val - (n + n) < n + n := by omega
      simp [Nat.mod_eq_of_lt hlt]
    · have hle2 : n + n ≤ a.val - (n + n) := by omega
      have hlt : a.val - (n + n) - (n + n) < n + n := by omega
      rw [Nat.mod_eq_sub_mod hle2, Nat.mod_eq_of_lt hlt]
      dsimp
      omega

def leafIndex (n : Nat) (i : Fin n) (j : Fin 3) : Fin (3 * n) :=
  ⟨i.val + n * j.val, by
    have hj : j.val = 0 ∨ j.val = 1 ∨ j.val = 2 := by omega
    rcases hj with hj | hj | hj <;> rw [hj] <;> simp <;> omega⟩

def leafName (n : Nat) (hn : 0 < n) (a : Fin (3 * n)) : Fin n × Fin 3 :=
  (⟨a.val % n, Nat.mod_lt _ hn⟩,
    ⟨a.val / n, (Nat.div_lt_iff_lt_mul hn).mpr a.isLt⟩)

theorem leafName_index (n : Nat) (hn : 0 < n) (i : Fin n) (j : Fin 3) :
    leafName n hn (leafIndex n i j) = (i, j) := by
  apply Prod.ext
  · apply Fin.ext
    change (i.val + n * j.val) % n = i.val
    simp [Nat.add_mod, Nat.mod_eq_of_lt i.isLt]
  · apply Fin.ext
    change (i.val + n * j.val) / n = j.val
    rw [Nat.add_mul_div_left _ _ hn, Nat.div_eq_of_lt i.isLt]
    simp

theorem leafIndex_name (n : Nat) (hn : 0 < n) (a : Fin (3 * n)) :
    leafIndex n (leafName n hn a).1 (leafName n hn a).2 = a := by
  apply Fin.ext
  exact Nat.mod_add_div a.val n

theorem centre_named_leaf (n : Nat) (i : Fin n) (j : Fin 3) :
    centreOfLeaf n (leafIndex n i j) = i := by
  apply Fin.ext
  rw [centreOfLeaf_is_mod]
  change (i.val + n * j.val) % n = i.val
  simp [Nat.add_mod, Nat.mod_eq_of_lt i.isLt]

theorem reduceHalf_eq_iff (m : Nat) (t : Fin (m + m)) (a : Fin m) :
    reduceHalf m t = a ↔ t.val = a.val ∨ t.val = a.val + m := by
  constructor
  · intro h
    have hv := congrArg Fin.val h
    unfold reduceHalf at hv
    split at hv <;> dsimp at * <;> omega
  · intro h
    apply Fin.ext
    unfold reduceHalf
    split <;> dsimp at * <;> omega

/- This is exactly the two ring attachments in Definition 6.1. -/
theorem original_ring_leaf_incidence (n : Nat)
    (t : Fin ((3 * n) + (3 * n))) (a : Fin (3 * n)) :
    baseAdj n (.ring t) (.leaf a) ↔
      t.val = a.val ∨ t.val = a.val + 3 * n :=
  reduceHalf_eq_iff (3 * n) t a

theorem bool_ne_not (a b : Bool) : (a ≠ !b) ↔ a = b := by
  cases a <;> cases b <;> decide

theorem not_bool_ne (a b : Bool) : ((!a) ≠ b) ↔ a = b := by
  cases a <;> cases b <;> decide

theorem ring_cdc_same (m : Nat) (a b : Fin (m + m)) :
    (bit a.val ≠ bit b.val ∧ ringAdj m a b) ↔ ringAdj m a b := by
  constructor
  · exact And.right
  · intro h
    exact ⟨ringAdj_bits m a b h, h⟩

theorem ring_cdc_cross (m : Nat) (hm : m % 2 = 1) (a b : Fin (m + m)) :
    (bit a.val ≠ bit b.val ∧ ringAdj m a (halfShift m b)) ↔ False := by
  constructor
  · intro h
    have hc := ringAdj_bits m a (halfShift m b) h.2
    rw [halfShift_bit m hm b] at hc
    cases ha : bit a.val <;> cases hb : bit b.val <;> simp_all
  · exact False.elim

theorem ring_cdc_cross_rev (m : Nat) (hm : m % 2 = 1) (a b : Fin (m + m)) :
    (bit a.val ≠ bit b.val ∧ ringAdj m (halfShift m a) b) ↔ False := by
  constructor
  · intro h
    have hc := ringAdj_bits m (halfShift m a) b h.2
    rw [halfShift_bit m hm a] at hc
    cases ha : bit a.val <;> cases hb : bit b.val <;> simp_all
  · exact False.elim

/- Every edge is checked against the original CG type/incidence definition.
   The synchronized adjacency is not assumed as a graph-isomorphism premise. -/
theorem toCover_adjacency (n : Nat) (hn : n % 2 = 1) (x y : Coord n) :
    coverAdj n (toCover n x) (toCover n y) ↔ coordinateAdj n x y := by
  have hk := triple_odd n hn
  cases x with
  | X t =>
    cases y with
    | X u => exact ring_cdc_same (3 * n) t u
    | Y u => exact ring_cdc_cross (3 * n) hk t u
    | A u =>
      simpa only [toCover, coverAdj, baseAdj, coordinateAdj, bool_ne_not] using
        bit_reduce_eq_iff (3 * n) hk t u
    | Z s => simp [toCover, coverAdj, baseAdj, coordinateAdj]
  | Y t =>
    cases y with
    | X u => exact ring_cdc_cross_rev (3 * n) hk t u
    | Y u =>
      simpa only [toCover, coverAdj, baseAdj, coordinateAdj, ringAdj_halfShift] using
        ring_cdc_same (3 * n) t u
    | A u =>
      simpa only [toCover, coverAdj, baseAdj, coordinateAdj,
        reduceHalf_shift, bool_ne_not] using bit_reduce_eq_iff (3 * n) hk t u
    | Z s => simp [toCover, coverAdj, baseAdj, coordinateAdj]
  | A t =>
    cases y with
    | X u =>
      simpa only [toCover, coverAdj, baseAdj, coordinateAdj, not_bool_ne] using
        bit_reduce_eq_iff (3 * n) hk t u
    | Y u =>
      simpa only [toCover, coverAdj, baseAdj, coordinateAdj,
        reduceHalf_shift, not_bool_ne] using bit_reduce_eq_iff (3 * n) hk t u
    | A u => simp [toCover, coverAdj, baseAdj, coordinateAdj]
    | Z s =>
      change ((!bit t.val) ≠ bit s.val ∧
        centreOfLeaf n (reduceHalf (3 * n) t) = reduceHalf n s) ↔
        centreResidue n t = s
      rw [not_bool_ne, centreOfLeaf_coordinate, ← centreResidue_bit n t]
      exact bit_reduce_eq_iff n hn (centreResidue n t) s
  | Z s =>
    cases y with
    | X u => simp [toCover, coverAdj, baseAdj, coordinateAdj]
    | Y u => simp [toCover, coverAdj, baseAdj, coordinateAdj]
    | A t =>
      change (bit s.val ≠ !bit t.val ∧
        reduceHalf n s = centreOfLeaf n (reduceHalf (3 * n) t)) ↔
        s = centreResidue n t
      rw [bool_ne_not, centreOfLeaf_coordinate, ← centreResidue_bit n t]
      exact bit_reduce_eq_iff n hn s (centreResidue n t)
    | Z u => simp [toCover, coverAdj, baseAdj, coordinateAdj]

theorem coordinateDeck_preserves (n : Nat) (hn : n % 2 = 1) (x y : Coord n) :
    coordinateAdj n (coordinateDeck n x) (coordinateDeck n y) ↔ coordinateAdj n x y := by
  rw [← toCover_adjacency n hn, ← toCover_adjacency n hn]
  rw [coordinateDeck_intertwines n hn, coordinateDeck_intertwines n hn]
  unfold coverAdj deck
  cases (toCover n x).2 <;> cases (toCover n y).2 <;> simp

#print axioms bit_add_odd
#print axioms halfShift_involutive
#print axioms reduceHalf_is_mod
#print axioms halfShift_bit
#print axioms joinHalf_reduce
#print axioms fromCover_toCover
#print axioms toCover_fromCover
#print axioms toCover_injective
#print axioms toCover_surjective
#print axioms coordinateDeck_intertwines
#print axioms halfShift_cycleNext
#print axioms ringAdj_halfShift
#print axioms ringAdj_bits
#print axioms centreOfLeaf_is_mod
#print axioms centreResidue_bit
#print axioms centreOfLeaf_coordinate
#print axioms cycleNext_is_mod
#print axioms centreResidue_is_mod
#print axioms leafName_index
#print axioms leafIndex_name
#print axioms centre_named_leaf
#print axioms original_ring_leaf_incidence
#print axioms toCover_adjacency
#print axioms coordinateDeck_preserves

end Struct2.OddCoordinates
