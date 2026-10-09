import Q6PackingDomination
import Lean.Elab.Tactic.Omega

/-! Actual six-bit geometry for an explicit finite graph construction.
The closed certificates are normalized at zero. They certify geometry,
not the graph or the original conjecture; the path bridge is separate. -/

set_option maxRecDepth 100000
set_option maxHeartbeats 16000000

namespace Q6PackingComplexGeometry

open Q6PackingDomination

theorem hdist_symm (a b : Vertex) : hdist a b = hdist b a := by
  simp only [hdist, BitVec.xor_comm]

theorem hdist_self (a : Vertex) : hdist a a = 0 := by
  simp [hdist, pop6, BitVec.cpopNatRec]

private theorem normalized_triangle :
    ∀ u v : Vertex, hdist u v ≤ hdist (0#6) u + hdist (0#6) v := by decide

theorem hdist_triangle (a b c : Vertex) :
    hdist a c ≤ hdist a b + hdist b c := by
  have h := normalized_triangle (b ^^^ a) (b ^^^ c)
  have ha := distance_translate b b a
  have hc := distance_translate b b c
  rw [BitVec.xor_self] at ha hc
  rw [ha, hc, distance_translate, hdist_symm b a] at h
  exact h

private theorem normalized_zero : ∀ z : Vertex, hdist (0#6) z = 0 → z = 0#6 := by decide

theorem hdist_zero_eq (a b : Vertex) (h : hdist a b = 0) : a = b := by
  have ht := distance_translate a a b
  rw [BitVec.xor_self] at ht
  have hz : a ^^^ b = 0#6 := normalized_zero (a ^^^ b) (ht.trans h)
  apply (BitVec.xor_right_inj a).mp
  exact (show a ^^^ a = 0#6 from BitVec.xor_self).trans hz.symm

private def lowest (z : Vertex) : Vertex := z &&& (-z)

/-- Change one genuinely differing coordinate towards b. -/
def nextVertex (a b : Vertex) : Vertex := a ^^^ lowest (a ^^^ b)

private theorem normalized_next : ∀ z : Vertex, z ≠ 0#6 →
    hdist (0#6) (lowest z) = 1 ∧ hdist (lowest z) z + 1 = hdist (0#6) z := by decide

theorem nextVertex_spec (a b : Vertex) (hne : a ≠ b) :
    hdist a (nextVertex a b) = 1 ∧
      hdist (nextVertex a b) b + 1 = hdist a b := by
  have hz : a ^^^ b ≠ 0#6 := by
    intro hz
    have heq : a = b := by
      apply (BitVec.xor_right_inj a).mp
      exact (show a ^^^ a = 0#6 from BitVec.xor_self).trans hz.symm
    exact hne heq
  have hn := normalized_next (a ^^^ b) hz
  have hfirst := distance_translate a a (nextVertex a b)
  have hlast := distance_translate a (nextVertex a b) b
  have hbase := distance_translate a a b
  simp only [nextVertex, xor_cancel, BitVec.xor_self] at hfirst hlast hbase
  constructor
  · change hdist a (a ^^^ lowest (a ^^^ b)) = 1
    exact hfirst.symm.trans hn.1
  · change hdist (a ^^^ lowest (a ^^^ b)) b + 1 = hdist a b
    rw [← hlast, ← hbase]
    exact hn.2

private theorem normalized_single_cover : ∀ x : Vertex,
    ∃ c : Vertex, (c = 0#6 ∨ hdist (0#6) c = 4) ∧ hdist x c ≤ 2 := by decide

/-- Zero plus all weight-four words, translated to a, covers all targets. -/
theorem single_cover (a x : Vertex) :
    ∃ c : Vertex, (c = a ∨ hdist a c = 4) ∧ hdist x c ≤ 2 := by
  rcases normalized_single_cover (a ^^^ x) with ⟨c, hc, hx⟩
  refine ⟨a ^^^ c, ?_, ?_⟩
  · rcases hc with hc | hc
    · left
      simp only [hc, BitVec.xor_zero]
    · right
      have ht := distance_translate a a (a ^^^ c)
      simp only [BitVec.xor_self, xor_cancel] at ht
      rw [← ht]
      exact hc
  · have ht := distance_translate a x (a ^^^ c)
    simp only [xor_cancel] at ht
    rw [← ht]
    exact hx

private theorem normalized_pair_cover : ∀ b x : Vertex, hdist (0#6) b = 4 →
    ∃ c : Vertex, (c = 0#6 ∨ c = b ∨ (4 ≤ hdist (0#6) c ∧ 4 ≤ hdist b c)) ∧
      hdist x c ≤ 2 := by decide

/-- A distance-four pair plus all its common far neighbors covers every target. -/
theorem pair_cover (a b x : Vertex) (hab : hdist a b = 4) :
    ∃ c : Vertex, (c = a ∨ c = b ∨ (4 ≤ hdist a c ∧ 4 ≤ hdist b c)) ∧
      hdist x c ≤ 2 := by
  have hb := distance_translate a a b
  rw [BitVec.xor_self] at hb
  rcases normalized_pair_cover (a ^^^ b) (a ^^^ x) (hb.trans hab) with ⟨c, hc, hx⟩
  refine ⟨a ^^^ c, ?_, ?_⟩
  · rcases hc with hc | hc | hc
    · left
      simp only [hc, BitVec.xor_zero]
    · right; left
      simp only [hc, xor_cancel]
    · right; right
      have hta := distance_translate a a (a ^^^ c)
      have htb := distance_translate a b (a ^^^ c)
      simp only [BitVec.xor_self, xor_cancel] at hta htb
      rw [← hta, ← htb]
      exact hc
  · have ht := distance_translate a x (a ^^^ c)
    simp only [xor_cancel] at ht
    rw [← ht]
    exact hx

#print axioms hdist_symm
#print axioms hdist_self
#print axioms normalized_triangle
#print axioms hdist_triangle
#print axioms normalized_zero
#print axioms hdist_zero_eq
#print axioms normalized_next
#print axioms nextVertex_spec
#print axioms normalized_single_cover
#print axioms single_cover
#print axioms normalized_pair_cover
#print axioms pair_cover

end Q6PackingComplexGeometry
