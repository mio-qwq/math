import Init.Data.BitVec.Lemmas
import Init.Data.BitVec.Decidable
import Lean.Elab.Tactic.Omega
import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Finset.Card

/-!
Conditional Hamming geometry supporting the written midpoint-classification proof.

Actual six-bit Hamming geometry, conditional on explicitly stated hypotheses.
For six same-parity points, antipodal closure and absence of distance-two
triangles imply that every opposite-parity vertex has at least four points
at Hamming distance at most three.

The classification of all six-point projections is not asserted here. Neither
an unconditional twelve-center obstruction nor a SimpleGraph shortest-path
equivalence is asserted. The old factor obstruction is not imported or replayed.

The three closed geometric certificates each have at most 64^2 cases and use
ordinary kernel computation. The distance-one-neighbor certificate is normalized
at zero, rather than checking all 64^3 triples of actual vertices.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 8000000

namespace Q6AntipodalCompatibility

abbrev Vertex := BitVec 6

/-- All six bits are counted in Nat, with no bit-vector overflow. -/
def pop6 (x : Vertex) : Nat := x.cpopNatRec 6 0

/-- Hamming distance on actual six-coordinate binary words. -/
def hdist (x y : Vertex) : Nat := pop6 (x ^^^ y)

/-- Binary weight parity, expressed as a Nat residue. -/
def parity (x : Vertex) : Nat := pop6 x % 2

/-- Complement all six coordinates. -/
def antipode (x : Vertex) : Vertex := ~~~x

theorem pop6_bits (x : Vertex) :
    pop6 x = (x.getLsbD 5).toNat + (x.getLsbD 4).toNat +
      (x.getLsbD 3).toNat + (x.getLsbD 2).toNat +
      (x.getLsbD 1).toNat + (x.getLsbD 0).toNat := by
  simp [pop6, BitVec.cpopNatRec]

theorem distance_bits (x y : Vertex) :
    hdist x y = ((x.getLsbD 5) ^^ (y.getLsbD 5)).toNat +
      ((x.getLsbD 4) ^^ (y.getLsbD 4)).toNat +
      ((x.getLsbD 3) ^^ (y.getLsbD 3)).toNat +
      ((x.getLsbD 2) ^^ (y.getLsbD 2)).toNat +
      ((x.getLsbD 1) ^^ (y.getLsbD 1)).toNat +
      ((x.getLsbD 0) ^^ (y.getLsbD 0)).toNat := by
  simp only [hdist, pop6_bits, BitVec.getLsbD_xor]

theorem xor_cancel (a x : Vertex) : a ^^^ (a ^^^ x) = x := by
  rw [← BitVec.xor_assoc]
  simp only [BitVec.xor_self, BitVec.zero_xor]

theorem distance_translate (a x y : Vertex) :
    hdist (a ^^^ x) (a ^^^ y) = hdist x y := by
  change pop6 ((a ^^^ x) ^^^ (a ^^^ y)) = pop6 (x ^^^ y)
  congr 1
  calc
    (a ^^^ x) ^^^ (a ^^^ y) = a ^^^ (x ^^^ (a ^^^ y)) :=
      BitVec.xor_assoc a x (a ^^^ y)
    _ = a ^^^ ((x ^^^ a) ^^^ y) := by rw [← BitVec.xor_assoc x a y]
    _ = a ^^^ ((a ^^^ x) ^^^ y) := by rw [BitVec.xor_comm x a]
    _ = a ^^^ (a ^^^ (x ^^^ y)) := by rw [BitVec.xor_assoc a x y]
    _ = x ^^^ y := xor_cancel a (x ^^^ y)

theorem antipode_involutive (x : Vertex) : antipode (antipode x) = x := by
  change ~~~(~~~x) = x
  exact BitVec.not_not

theorem antipode_injective : Function.Injective antipode := by
  intro x y hxy
  have h := congrArg antipode hxy
  simpa only [antipode_involutive] using h

/-- A 64^2 certificate for complementary distances, not a code classification. -/
theorem complement_distance_sum :
    ∀ q p : Vertex, hdist q p + hdist q (antipode p) = 6 := by
  decide

/-- A 64^2 certificate: opposite parities have precisely odd possible distances. -/
theorem opposite_parity_distances :
    ∀ q p : Vertex, parity q ≠ parity p →
      hdist q p = 1 ∨ hdist q p = 3 ∨ hdist q p = 5 := by
  decide

/-- Normalizing the common distance-one neighbor at zero avoids 64^3 cases. -/
private theorem normalized_one_neighbors :
    ∀ x y : Vertex, hdist (0#6) x = 1 → hdist (0#6) y = 1 →
      x ≠ y → hdist x y = 2 := by
  decide

/-- Distinct actual distance-one neighbors of an arbitrary vertex are distance two apart. -/
theorem distance_one_neighbors (q x y : Vertex)
    (hx : hdist q x = 1) (hy : hdist q y = 1) (hxy : x ≠ y) :
    hdist x y = 2 := by
  have hx0 : hdist (0#6) (q ^^^ x) = 1 := by
    have h := distance_translate q q x
    rw [BitVec.xor_self] at h
    exact h.trans hx
  have hy0 : hdist (0#6) (q ^^^ y) = 1 := by
    have h := distance_translate q q y
    rw [BitVec.xor_self] at h
    exact h.trans hy
  have hne : q ^^^ x ≠ q ^^^ y := by
    intro heq
    exact hxy ((BitVec.xor_right_inj q).mp heq)
  calc
    hdist x y = hdist (q ^^^ x) (q ^^^ y) :=
      (distance_translate q x y).symm
    _ = 2 := normalized_one_neighbors (q ^^^ x) (q ^^^ y) hx0 hy0 hne

def SameParity (P : Finset Vertex) (ε : Nat) : Prop :=
  ∀ p, p ∈ P → parity p = ε

def AntipodalClosed (P : Finset Vertex) : Prop :=
  ∀ p, p ∈ P → antipode p ∈ P

/-- The hypothesis concerns actual distance-two triangles among distinct words of P. -/
def DistanceTwoTriangleFree (P : Finset Vertex) : Prop :=
  ∀ a, a ∈ P → ∀ b, b ∈ P → ∀ c, c ∈ P →
    a ≠ b → a ≠ c → b ≠ c →
      ¬ (hdist a b = 2 ∧ hdist a c = 2 ∧ hdist b c = 2)

def sphere (P : Finset Vertex) (q : Vertex) (r : Nat) : Finset Vertex :=
  P.filter (fun p => hdist q p = r)

def nearThree (P : Finset Vertex) (q : Vertex) : Finset Vertex :=
  P.filter (fun p => hdist q p ≤ 3)

/-- A third distance-one neighbor would form an actual forbidden distance-two triangle. -/
theorem sphere_one_card_le_two (P : Finset Vertex)
    (htri : DistanceTwoTriangleFree P) (q : Vertex) :
    (sphere P q 1).card ≤ 2 := by
  classical
  by_contra hnot
  have hlarge : 2 < (sphere P q 1).card := by omega
  rcases Finset.two_lt_card_iff.mp hlarge with
    ⟨a, b, c, ha, hb, hc, hab, hac, hbc⟩
  rcases Finset.mem_filter.mp ha with ⟨haP, ha1⟩
  rcases Finset.mem_filter.mp hb with ⟨hbP, hb1⟩
  rcases Finset.mem_filter.mp hc with ⟨hcP, hc1⟩
  exact htri a haP b hbP c hcP hab hac hbc
    ⟨distance_one_neighbors q a b ha1 hb1 hab,
      distance_one_neighbors q a c ha1 hc1 hac,
      distance_one_neighbors q b c hb1 hc1 hbc⟩

/-- Complementation is a genuine bijection between distance-five and distance-one members. -/
theorem antipodal_sphere_five_card_eq_one (P : Finset Vertex)
    (hanti : AntipodalClosed P) (q : Vertex) :
    (sphere P q 5).card = (sphere P q 1).card := by
  classical
  refine Finset.card_bij (fun p _ => antipode p) ?_ ?_ ?_
  · intro p hp
    rcases Finset.mem_filter.mp hp with ⟨hpP, hp5⟩
    refine Finset.mem_filter.mpr ⟨hanti p hpP, ?_⟩
    have hsum := complement_distance_sum q p
    rw [hp5] at hsum
    omega
  · intro p hp p' hp' heq
    exact antipode_injective heq
  · intro p hp
    rcases Finset.mem_filter.mp hp with ⟨hpP, hp1⟩
    have hpre : antipode p ∈ sphere P q 5 := by
      refine Finset.mem_filter.mpr ⟨hanti p hpP, ?_⟩
      have hsum := complement_distance_sum q p
      rw [hp1] at hsum
      omega
    exact ⟨antipode p, hpre, antipode_involutive p⟩

theorem sphere_five_card_le_two (P : Finset Vertex)
    (hanti : AntipodalClosed P) (htri : DistanceTwoTriangleFree P)
    (q : Vertex) : (sphere P q 5).card ≤ 2 := by
  rw [antipodal_sphere_five_card_eq_one P hanti q]
  exact sphere_one_card_le_two P htri q

/-- Under the parity hypothesis, all members outside the radius-three neighborhood have distance five. -/
theorem opposite_far_card_le_two (P : Finset Vertex) (ε : Nat)
    (hpar : SameParity P ε) (hanti : AntipodalClosed P)
    (htri : DistanceTwoTriangleFree P) (q : Vertex) (hq : parity q ≠ ε) :
    (P.filter (fun p => ¬ hdist q p ≤ 3)).card ≤ 2 := by
  classical
  have hsub : P.filter (fun p => ¬ hdist q p ≤ 3) ⊆ sphere P q 5 := by
    intro p hp
    rcases Finset.mem_filter.mp hp with ⟨hpP, hfar⟩
    have hopp : parity q ≠ parity p := by
      rw [hpar p hpP]
      exact hq
    have hcases := opposite_parity_distances q p hopp
    have hp5 : hdist q p = 5 := by
      rcases hcases with h1 | h3 | h5 <;> omega
    exact Finset.mem_filter.mpr ⟨hpP, hp5⟩
  exact (Finset.card_le_card hsub).trans (sphere_five_card_le_two P hanti htri q)

/-- Conditional six-point geometry; the antipodal and triangle-free hypotheses remain explicit. -/
theorem antipodal_trianglefree_opposite_has_four_near
    (P : Finset Vertex) (hcard : P.card = 6) (ε : Nat)
    (hpar : SameParity P ε) (hanti : AntipodalClosed P)
    (htri : DistanceTwoTriangleFree P) (q : Vertex) (hq : parity q ≠ ε) :
    4 ≤ (nearThree P q).card := by
  classical
  have hfar := opposite_far_card_le_two P ε hpar hanti htri q hq
  have hpartition : (nearThree P q).card +
      (P.filter (fun p => ¬ hdist q p ≤ 3)).card = P.card := by
    exact Finset.card_filter_add_card_filter_not (s := P) (fun p => hdist q p ≤ 3)
  rw [hcard] at hpartition
  omega

#print axioms pop6_bits
#print axioms distance_bits
#print axioms xor_cancel
#print axioms distance_translate
#print axioms antipode_involutive
#print axioms antipode_injective
#print axioms complement_distance_sum
#print axioms opposite_parity_distances
#print axioms normalized_one_neighbors
#print axioms distance_one_neighbors
#print axioms sphere_one_card_le_two
#print axioms antipodal_sphere_five_card_eq_one
#print axioms sphere_five_card_le_two
#print axioms opposite_far_card_le_two
#print axioms antipodal_trianglefree_opposite_has_four_near

end Q6AntipodalCompatibility
