import TwentyDimCharacters
import Mathlib.Algebra.Algebra.Equiv

/-!
# Actual unit scaling of the dual summand

The first ten table coordinates form the base summand and the last ten
form its square-zero dual ideal. Their multiplication support is derived
from the frozen transpose-recurrence certificate, without a new table
enumeration. Scaling the latter summand by a unit gives a genuine
R-algebra automorphism for every characteristic-two specialization.

This file constructs the automorphism and its coordinate/basis actions.
It does not assert a cochain eigenvalue, an Ext action, or complete ARC.
-/

namespace ARCTwentyDimDualScale

open ARCFiniteCore ARCTermSemantics ARCFiniteTableContraction
open ARCTwentyDimAssociativity ARCTwentyDimUnit ARCTwentyDimAlgebra
open ARCTwentyDimCochainAlgebra ARCTwentyDimCharacters
open scoped BigOperators

noncomputable section

variable {R : Type*} [CommRing R] [CharP R 2]

/-- The scalar on each basis label: base letters are fixed. -/
def dualWeight (H : Rˣ) (i : Nat) : R :=
  if i < 10 then 1 else (H : R)

/-- Output support of the actual table's frozen dual recurrence. -/
theorem t_term_dual_support (a b : Fin 20) (term : Nat × Nat)
    (hterm : term ∈ tTerms a.val b.val) :
    (term.1 < 10 ↔ a.val < 10 ∧ b.val < 10) ∧
      (a.val < 10 ∨ b.val < 10) := by
  rw [t_table_matches_dual_recurrence a b] at hterm
  by_cases ha : a.val < 10
  · by_cases hb : b.val < 10
    · have hc : ∀ t ∈ cTerms a.val b.val, t.1 < 10 := by
        simpa only [List.all_eq_true, decide_eq_true_eq] using
          c_output_basis_bound ⟨a.val, ha⟩ ⟨b.val, hb⟩
      have ht : term.1 < 10 := hc term (by simpa [tByDualRecurrence, ha, hb] using hterm)
      exact ⟨by simp [ht, ha, hb], Or.inl ha⟩
    · simp only [tByDualRecurrence, ha, hb, ite_true, ite_false,
        List.mem_filterMap] at hterm
      obtain ⟨c, _, hc⟩ := hterm
      split_ifs at hc with hp
      have heq : c + 10 = term.1 := congrArg Prod.fst (Option.some.inj hc)
      have ht : ¬term.1 < 10 := by omega
      exact ⟨by simp [ht, ha, hb], Or.inl ha⟩
  · by_cases hb : b.val < 10
    · simp only [tByDualRecurrence, ha, hb, ite_true, ite_false,
        List.mem_filterMap] at hterm
      obtain ⟨c, _, hc⟩ := hterm
      split_ifs at hc with hp
      have heq : c + 10 = term.1 := congrArg Prod.fst (Option.some.inj hc)
      have ht : ¬term.1 < 10 := by omega
      exact ⟨by simp [ht, ha, hb], Or.inr hb⟩
    · simp [tByDualRecurrence, ha, hb] at hterm

omit [CharP R 2] in
/-- Every actual output scales by the product of its input weights. -/
theorem t_term_weight (H : Rˣ) (a b : Fin 20) (term : Nat × Nat)
    (hterm : term ∈ tTerms a.val b.val) :
    dualWeight H term.1 = dualWeight H a.val * dualWeight H b.val := by
  obtain ⟨hout, hab⟩ := t_term_dual_support a b term hterm
  by_cases ha : a.val < 10
  · by_cases hb : b.val < 10
    · simp [dualWeight, ha, hb, hout.mpr ⟨ha, hb⟩]
    · have ht : ¬term.1 < 10 := fun h => hb (hout.mp h).2
      simp [dualWeight, ha, hb, ht]
  · have hb : b.val < 10 := hab.resolve_left ha
    have ht : ¬term.1 < 10 := fun h => ha (hout.mp h).1
    simp [dualWeight, ha, hb, ht]

private theorem weighted_single (q : R) (H : Rˣ) (j c k : Nat) :
    dualWeight H k * specialize q (singleTerm j c k) =
      dualWeight H j * specialize q (singleTerm j c k) := by
  by_cases hk : k = j
  · simp [singleTerm, hk]
  · simp [singleTerm, hk]

private theorem weighted_sumTerms (q : R) (H : Rˣ) (terms : Terms) (m : R)
    (hweight : ∀ term ∈ terms, dualWeight H term.1 = m) (k : Nat) :
    dualWeight H k * specialize q (sumTerms terms k) =
      m * specialize q (sumTerms terms k) := by
  induction terms with
  | nil => simp
  | cons term terms ih =>
      have hm : dualWeight H term.1 = m := hweight term (List.mem_cons_self ..)
      have ht : ∀ t ∈ terms, dualWeight H t.1 = m :=
        fun t h => hweight t (List.mem_cons_of_mem _ h)
      rw [sumTerms_cons]
      simp only [Pi.add_apply, map_add, mul_add]
      rw [ih ht]
      congr 1
      rw [← hm]
      exact weighted_single q H term.1 term.2 k

/-- The specialized constants obey dual-scaling homogeneity, for arbitrary q. -/
theorem specializedConstants_weight (q : R) (H : Rˣ) (a b k : Fin 20) :
    dualWeight H k.val * specializedConstants q a b k =
      (dualWeight H a.val * dualWeight H b.val) * specializedConstants q a b k := by
  exact weighted_sumTerms q H (tTerms a.val b.val)
    (dualWeight H a.val * dualWeight H b.val) (t_term_weight H a b) k.val

/-- Coordinatewise unit scaling, with inverse given by inverse-unit scaling. -/
def dualScaleLinearEquiv (q : R) (H : Rˣ) : TableAlgebra q ≃ₗ[R] TableAlgebra q where
  toFun x := ⟨fun i => dualWeight H i.val * x.coords i⟩
  invFun x := ⟨fun i => dualWeight H⁻¹ i.val * x.coords i⟩
  left_inv x := by
    apply ARCTwentyDimAlgebra.ext q
    funext i
    change dualWeight H⁻¹ i.val * (dualWeight H i.val * x.coords i) = x.coords i
    by_cases hi : i.val < 10 <;> simp [dualWeight, hi, ← mul_assoc]
  right_inv x := by
    apply ARCTwentyDimAlgebra.ext q
    funext i
    change dualWeight H i.val * (dualWeight H⁻¹ i.val * x.coords i) = x.coords i
    by_cases hi : i.val < 10 <;> simp [dualWeight, hi, ← mul_assoc]
  map_add' x y := by
    apply ARCTwentyDimAlgebra.ext q
    funext i
    exact mul_add ..
  map_smul' r x := by
    apply ARCTwentyDimAlgebra.ext q
    funext i
    change dualWeight H i.val * (r * x.coords i) = r * (dualWeight H i.val * x.coords i)
    exact mul_left_comm ..

@[simp] theorem coords_dualScaleLinearEquiv (q : R) (H : Rˣ) (x : TableAlgebra q)
    (i : Fin 20) :
    (dualScaleLinearEquiv q H x).coords i = dualWeight H i.val * x.coords i := rfl

theorem dualScaleLinearEquiv_one (q : R) (H : Rˣ) :
    dualScaleLinearEquiv q H 1 = 1 := by
  apply ARCTwentyDimAlgebra.ext q
  funext i
  rw [coords_dualScaleLinearEquiv, coords_one, specialized_unit_coordinates]
  by_cases h0 : i = 0
  · subst i
    simp [dualWeight]
  · by_cases h8 : i = 8
    · subst i
      simp [dualWeight]
    · simp [h0, h8]

/-- Multiplicativity follows by finite bilinear contraction of the support law. -/
theorem dualScaleLinearEquiv_mul (q : R) (H : Rˣ) (x y : TableAlgebra q) :
    dualScaleLinearEquiv q H (x * y) =
      dualScaleLinearEquiv q H x * dualScaleLinearEquiv q H y := by
  apply ARCTwentyDimAlgebra.ext q
  funext k
  change dualWeight H k.val *
      (∑ a : Fin 20, ∑ b : Fin 20, x.coords a * y.coords b * specializedConstants q a b k) =
    ∑ a : Fin 20, ∑ b : Fin 20,
      (dualWeight H a.val * x.coords a) *
        (dualWeight H b.val * y.coords b) * specializedConstants q a b k
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro a ha
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro b hb
  calc
    dualWeight H k.val * (x.coords a * y.coords b * specializedConstants q a b k) =
        (x.coords a * y.coords b) *
          (dualWeight H k.val * specializedConstants q a b k) := by ring
    _ = (x.coords a * y.coords b) *
        ((dualWeight H a.val * dualWeight H b.val) * specializedConstants q a b k) := by
      rw [specializedConstants_weight]
    _ = _ := by ring

/-- Genuine R-algebra automorphism scaling only the dual summand. -/
def dualScale (q : R) (H : Rˣ) : TableAlgebra q ≃ₐ[R] TableAlgebra q :=
  AlgEquiv.ofLinearEquiv (dualScaleLinearEquiv q H)
    (dualScaleLinearEquiv_one q H) (dualScaleLinearEquiv_mul q H)

@[simp] theorem coords_dualScale_apply (q : R) (H : Rˣ) (x : TableAlgebra q)
    (i : Fin 20) :
    (dualScale q H x).coords i =
      if i.val < 10 then x.coords i else (H : R) * x.coords i := by
  change dualWeight H i.val * x.coords i = _
  by_cases hi : i.val < 10 <;> simp [dualWeight, hi]

theorem dualScale_basis (q : R) (H : Rˣ) (a : Fin 20) :
    dualScale q H (coordinateBasis q a) =
      if a.val < 10 then coordinateBasis q a else (H : R) • coordinateBasis q a := by
  apply ARCTwentyDimAlgebra.ext q
  funext i
  by_cases ha : a.val < 10
  · simp only [ha, ite_true]
    rw [coords_dualScale_apply, coordinateBasis_coords]
    by_cases hi : i = a
    · subst i
      simp [ha, ARCFiniteTrilinear.basis]
    · simp [ARCFiniteTrilinear.basis, hi]
  · simp only [ha, ite_false]
    rw [coords_dualScale_apply, coords_smul, coordinateBasis_coords]
    by_cases hi : i = a
    · subst i
      simp [ha, ARCFiniteTrilinear.basis]
    · simp [ARCFiniteTrilinear.basis, hi]

/-- Inverse automorphism agrees with scaling by the inverse unit. -/
theorem dualScale_symm (q : R) (H : Rˣ) :
    (dualScale q H).symm = dualScale q H⁻¹ := by
  ext x
  rfl

@[simp] theorem eCharacter_dualScale (q : R) (H : Rˣ) (x : TableAlgebra q) :
    eCharacter q (dualScale q H x) = eCharacter q x := by
  rw [eCharacter_apply, coords_dualScale_apply, eCharacter_apply]
  simp

@[simp] theorem fCharacter_dualScale (q : R) (H : Rˣ) (x : TableAlgebra q) :
    fCharacter q (dualScale q H x) = fCharacter q x := by
  rw [fCharacter_apply, coords_dualScale_apply, fCharacter_apply]
  simp

#print axioms t_term_dual_support
#print axioms t_term_weight
#print axioms specializedConstants_weight
#print axioms dualScaleLinearEquiv
#print axioms dualScaleLinearEquiv_one
#print axioms dualScaleLinearEquiv_mul
#print axioms dualScale
#print axioms coords_dualScale_apply
#print axioms dualScale_basis
#print axioms dualScale_symm
#print axioms eCharacter_dualScale
#print axioms fCharacter_dualScale

end
end ARCTwentyDimDualScale
