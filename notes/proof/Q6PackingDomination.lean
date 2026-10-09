import Init.Data.BitVec.Lemmas
import Init.Data.BitVec.Decidable
import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Fin.VecNotation

/-!
Complete finite Hamming-space factor obstruction for radius two and separation four.

An obstruction for every subset of the binary Hamming space of length six,
without a linearity hypothesis. All closed finite certificates use `decide`,
not native computation or an added axiom. The two-positive-center certificate
has only 22^3 index cases; no powerset of the 64 vertices is enumerated.

The graph interpretation is Q6 because its graph distance is Hamming distance.
That shortest-path equivalence is written mathematics here, not a theorem
about Mathlib's SimpleGraph.dist. No strong-product feasibility is asserted.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 8000000

namespace Q6PackingDomination

abbrev Vertex := BitVec 6

/-- The Nat-valued count of all six bits; no BitVec wraparound in the result. -/
def pop6 (x : Vertex) : Nat := x.cpopNatRec 6 0

/-- The Hamming distance between actual six-bit vertices. -/
def hdist (x y : Vertex) : Nat := pop6 (x ^^^ y)

theorem pop6_bits (x : Vertex) :
    pop6 x = (x.getLsbD 5).toNat + (x.getLsbD 4).toNat +
      (x.getLsbD 3).toNat + (x.getLsbD 2).toNat +
      (x.getLsbD 1).toNat + (x.getLsbD 0).toNat := by
  simp [pop6, BitVec.cpopNatRec]

/-- This exposes the six coordinate differences counted by the metric. -/
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

/-- Simultaneous XOR translation preserves the metric. -/
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

/-- Separation required by p=3, including arbitrary nonlinear center sets. -/
def Packing (S : Set Vertex) : Prop :=
  ∀ x, x ∈ S → ∀ y, y ∈ S → x ≠ y → 4 ≤ hdist x y

/-- Closed radius-two covering of every actual vertex. -/
def Covers2 (S : Set Vertex) : Prop :=
  ∀ x, ∃ c, c ∈ S ∧ hdist x c ≤ 2

/- The fifteen weight-four words (complements of unordered coordinate pairs),
the six weight-five words, and the weight-six word. -/
private def center : Fin 22 → Vertex :=
  ![60, 58, 54, 46, 30, 57, 53, 45, 29, 51, 43,
    27, 39, 23, 15, 62, 61, 59, 55, 47, 31, 63]

/-- This checks just 64 vertices and their membership in the 22-word list. -/
private theorem candidate_complete :
    ∀ x : Vertex, 4 ≤ hdist 0 x → ∃ i : Fin 22, center i = x := by
  decide

/-- Standard two's-complement isolation of the lowest set bit. -/
private def lowest (x : Vertex) : Vertex := x &&& (-x)

private def singleWitness (i : Fin 22) : Vertex :=
  let p := center i
  if p = 63 then 7
  else lowest (~~~p) ||| lowest p ||| lowest (p ^^^ lowest p)

/-- For a compatible pair, select one bit in each of its three zero-pair blocks. -/
private def pairWitness (i j : Fin 22) : Vertex :=
  lowest (~~~center i) ||| lowest (~~~center j) ||| lowest (center i &&& center j)

private theorem single_far :
    ∀ i : Fin 22, 2 < hdist (singleWitness i) 0 ∧
      2 < hdist (singleWitness i) (center i) := by
  decide

/-- Closed 22^2 certificate, including all heavy-word incompatibilities. -/
private theorem pair_far :
    ∀ i j : Fin 22, 4 ≤ hdist (center i) (center j) →
      2 < hdist (pairWitness i j) 0 ∧
      2 < hdist (pairWitness i j) (center i) ∧
      2 < hdist (pairWitness i j) (center j) := by
  decide

/-- Closed 22^3 certificate, used for every additional center in an arbitrary set. -/
private theorem third_far :
    ∀ i j k : Fin 22, 4 ≤ hdist (center i) (center j) →
      4 ≤ hdist (center i) (center k) →
      4 ≤ hdist (center j) (center k) →
      2 < hdist (pairWitness i j) (center k) := by
  decide

private theorem zero_far : 2 < hdist (7 : Vertex) 0 := by
  decide

/-- Every normalized packing has a genuine vertex omitted by all radius-two balls. -/
theorem normalized_has_uncovered (S : Set Vertex) (h0 : (0 : Vertex) ∈ S)
    (hp : Packing S) : ∃ x, ∀ c, c ∈ S → 2 < hdist x c := by
  classical
  have hindex : ∀ x, x ∈ S → x ≠ 0 → ∃ i : Fin 22, center i = x := by
    intro x hx hx0
    exact candidate_complete x (hp 0 h0 x hx (Ne.symm hx0))
  by_cases hone : ∃ i : Fin 22, center i ∈ S
  · rcases hone with ⟨i, hi⟩
    by_cases htwo : ∃ j : Fin 22, center j ∈ S ∧ center j ≠ center i
    · rcases htwo with ⟨j, hj, hji⟩
      have hsep := hp (center i) hi (center j) hj (Ne.symm hji)
      have hbase := pair_far i j hsep
      refine ⟨pairWitness i j, ?_⟩
      intro x hx
      by_cases hx0 : x = 0
      · simpa only [hx0] using hbase.1
      · rcases hindex x hx hx0 with ⟨k, hk⟩
        rw [← hk] at hx ⊢
        by_cases hki : center k = center i
        · simpa only [hki] using hbase.2.1
        · by_cases hkj : center k = center j
          · simpa only [hkj] using hbase.2.2
          · exact third_far i j k hsep
              (hp (center i) hi (center k) hx (Ne.symm hki))
              (hp (center j) hj (center k) hx (Ne.symm hkj))
    · refine ⟨singleWitness i, ?_⟩
      intro x hx
      by_cases hx0 : x = 0
      · simpa only [hx0] using (single_far i).1
      · have hxi : x = center i := by
          by_contra hxi
          rcases hindex x hx hx0 with ⟨j, hj⟩
          apply htwo
          refine ⟨j, ?_, ?_⟩
          · simpa only [hj] using hx
          · simpa only [hj] using hxi
        simpa only [hxi] using (single_far i).2
  · refine ⟨(7 : Vertex), ?_⟩
    intro x hx
    by_cases hx0 : x = 0
    · rw [hx0]
      exact zero_far
    · rcases hindex x hx hx0 with ⟨i, hi⟩
      exact False.elim (hone ⟨i, by simpa only [hi] using hx⟩)

/-- All subsets, with no normalization or linearity assumption, have an omitted vertex. -/
theorem packing_has_uncovered (S : Set Vertex) (hp : Packing S) :
    ∃ x, ∀ c, c ∈ S → 2 < hdist x c := by
  classical
  by_cases hnonempty : S.Nonempty
  · rcases hnonempty with ⟨a, ha⟩
    let T : Set Vertex := {x | a ^^^ x ∈ S}
    have h0 : (0 : Vertex) ∈ T := by
      change a ^^^ (0 : Vertex) ∈ S
      simpa only [BitVec.ofNat_eq_ofNat, BitVec.xor_zero] using ha
    have hpT : Packing T := by
      intro x hx y hy hxy
      change a ^^^ x ∈ S at hx
      change a ^^^ y ∈ S at hy
      have hne : a ^^^ x ≠ a ^^^ y := by
        intro heq
        exact hxy ((BitVec.xor_right_inj a).mp heq)
      have hsep := hp (a ^^^ x) hx (a ^^^ y) hy hne
      simpa only [distance_translate] using hsep
    rcases normalized_has_uncovered T h0 hpT with ⟨w, hw⟩
    refine ⟨a ^^^ w, ?_⟩
    intro c hc
    have hTc : a ^^^ c ∈ T := by
      change a ^^^ (a ^^^ c) ∈ S
      simpa only [xor_cancel] using hc
    have htrans : hdist (a ^^^ w) c = hdist w (a ^^^ c) := by
      simpa only [xor_cancel] using distance_translate a w (a ^^^ c)
    rw [htrans]
    exact hw (a ^^^ c) hTc
  · refine ⟨0, ?_⟩
    intro c hc
    exact False.elim (hnonempty ⟨c, hc⟩)

/-- The complete finite-code obstruction corresponding to gamma_2^3(Q6)=infinity. -/
theorem no_packing_cover (S : Set Vertex) (hp : Packing S) : ¬ Covers2 S := by
  intro hc
  rcases packing_has_uncovered S hp with ⟨x, hx⟩
  rcases hc x with ⟨c, hmem, hnear⟩
  exact (Nat.not_lt_of_ge hnear) (hx c hmem)

#print axioms pop6_bits
#print axioms distance_bits
#print axioms xor_cancel
#print axioms distance_translate
#print axioms candidate_complete
#print axioms single_far
#print axioms pair_far
#print axioms third_far
#print axioms zero_far
#print axioms normalized_has_uncovered
#print axioms packing_has_uncovered
#print axioms no_packing_cover

end Q6PackingDomination
