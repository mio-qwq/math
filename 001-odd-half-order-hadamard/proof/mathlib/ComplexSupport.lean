import Support
import Mathlib.Basic.Complex.Basic
import Mathlib.Algebra.Ring.Commute
import Std

/-!
The scalar support-intersection argument for actual nonzero complex values.
We instantiate the abstract cancellation laws only on the nonzero subtype.
The Hadamard/Newton arguments yielding the multiplicities and the at-most-two
hypothesis remain separate from this file.
-/

namespace OddHalfOrder.ComplexSupport

open OddHalfOrder.Support

abbrev NonzeroComplex := {z : ℂ // z ≠ 0}

/-- Complex cancellation is valid on the nonzero subtype, including products. -/
def complexPhaseCancellation : PhaseCancellation NonzeroComplex where
  one := ⟨1, one_ne_zero⟩
  mul x y := ⟨x.val * y.val, mul_ne_zero x.property y.property⟩
  right_identity x := by
    apply Subtype.ext
    exact mul_one x.val
  left_cancel x y z h := by
    apply Subtype.ext
    exact mul_left_cancel₀ x.property (congrArg Subtype.val h)

/-- An injective map transports the at-most-two property back to its source. -/
theorem atMostTwo_of_injective {α β : Type} (f : α → β)
    (hf : Function.Injective f) (values : List α)
    (hsmall : AtMostTwo (values.map f)) : AtMostTwo values := by
  intro a b c ha hb hc
  have h := hsmall (f a) (f b) (f c)
    (List.mem_map_of_mem ha) (List.mem_map_of_mem hb) (List.mem_map_of_mem hc)
  rcases h with h | h | h
  · exact Or.inl (hf h)
  · exact Or.inr (Or.inl (hf h))
  · exact Or.inr (Or.inr (hf h))

/-- Four actual complex phases with at most two values collapse to `1,-1`. -/
theorem complex_four_phase_collapse (x y : ℂ)
    (hx0 : x ≠ 0) (hy0 : y ≠ 0) (hx1 : x ≠ 1) (hy1 : y ≠ 1)
    (hsmall : AtMostTwo [(1 : ℂ), x, y, x * y]) :
    x = -1 ∧ y = -1 ∧ x * y = 1 := by
  let X : NonzeroComplex := ⟨x, hx0⟩
  let Y : NonzeroComplex := ⟨y, hy0⟩
  let g := complexPhaseCancellation
  have hX : X ≠ g.one := by
    intro h
    exact hx1 (congrArg Subtype.val h)
  have hY : Y ≠ g.one := by
    intro h
    exact hy1 (congrArg Subtype.val h)
  have hsmall' : AtMostTwo [g.one, X, Y, g.mul X Y] := by
    apply atMostTwo_of_injective Subtype.val Subtype.val_injective
    change AtMostTwo [(1 : ℂ), x, y, x * y]
    exact hsmall
  obtain ⟨hYX, hproduct⟩ := four_phase_collapse g X Y hX hY hsmall'
  have hyx : y = x := congrArg Subtype.val hYX
  have hxy : x * y = 1 := congrArg Subtype.val hproduct
  have hxx : x * x = 1 := by simpa only [hyx] using hxy
  have hminus : x = -1 := by
    rcases mul_self_eq_one_iff.mp hxx with h | h
    · exact False.elim (hx1 h)
    · exact h
  exact ⟨hminus, hyx.trans hminus, hxy⟩

/-- The four classes of a support intersection contain exactly `2*t`
copies of the actual complex value `1`. -/
theorem complex_four_phase_one_count (x y : ℂ)
    (hx0 : x ≠ 0) (hy0 : y ≠ 0) (hx1 : x ≠ 1) (hy1 : y ≠ 1)
    (hsmall : AtMostTwo [(1 : ℂ), x, y, x * y]) (m t : Nat) :
    weightedCount (1 : ℂ)
      [(1, t), (x, m - t), (y, m - t), (x * y, t)] = 2 * t := by
  classical
  have hproduct := (complex_four_phase_collapse x y hx0 hy0 hx1 hy1 hsmall).2.2
  simp [weightedCount, hx1, hy1, hproduct, Nat.mul_comm, Nat.mul_two]

/-- An odd support size cannot equal this actual complex phase multiplicity. -/
theorem complex_mismatched_support_obstruction (x y : ℂ) (m t : Nat)
    (hx0 : x ≠ 0) (hy0 : y ≠ 0) (hx1 : x ≠ 1) (hy1 : y ≠ 1)
    (hodd : ∃ s : Nat, m = 2 * s + 1)
    (hsmall : AtMostTwo [(1 : ℂ), x, y, x * y]) :
    weightedCount (1 : ℂ)
      [(1, t), (x, m - t), (y, m - t), (x * y, t)] ≠ m := by
  classical
  rw [complex_four_phase_one_count x y hx0 hy0 hx1 hy1 hsmall m t]
  obtain ⟨s, hs⟩ := hodd
  omega

/-- In the row-ratio notation, the two nonconstant phases themselves are `-1`. -/
theorem complex_ratio_four_phase_collapse (phi psi : ℂ)
    (hphi0 : phi ≠ 0) (hpsi0 : psi ≠ 0) (hphi1 : phi ≠ 1) (hpsi1 : psi ≠ 1)
    (hsmall : AtMostTwo [(1 : ℂ), phi, psi⁻¹, phi * psi⁻¹]) :
    phi = -1 ∧ psi = -1 := by
  have hpsiinv1 : psi⁻¹ ≠ 1 := by
    intro h
    apply hpsi1
    have hi := congrArg Inv.inv h
    simpa using hi
  obtain ⟨hphi, hpsiinv, _⟩ := complex_four_phase_collapse phi psi⁻¹
    hphi0 (inv_ne_zero hpsi0) hphi1 hpsiinv1 hsmall
  refine ⟨hphi, ?_⟩
  have hi := congrArg Inv.inv hpsiinv
  simpa using hi

#print axioms complex_four_phase_collapse
#print axioms complex_four_phase_one_count
#print axioms complex_mismatched_support_obstruction
#print axioms complex_ratio_four_phase_collapse

end OddHalfOrder.ComplexSupport
