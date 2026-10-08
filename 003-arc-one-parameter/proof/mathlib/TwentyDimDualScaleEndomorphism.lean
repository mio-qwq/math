import TwentyDimDualScale
import Mathlib.Algebra.Algebra.Subalgebra.Basic
import Mathlib.RingTheory.Ideal.Maps
import Mathlib.LinearAlgebra.Projection

/-!
# Scalar endomorphisms and the actual split square-zero summand

Every scalar, including zero and nonunits, scales the upper ten coordinates
of the actual table algebra while fixing the lower ten. Multiplicativity on
all vectors follows from the previously proved dual support law. No new
table enumeration is used.

The zero-scalar member is an idempotent algebra projection. Its image
is the lower-coordinate subalgebra and its two-sided kernel consists
exactly of upper-coordinate vectors, whose pairwise products are zero.
The actual range and kernel give a complementary R-module decomposition.
This does not identify the kernel with the dual bimodule or prove a full
self-Ext profile or the ARC realization.
-/

namespace ARCTwentyDimDualScaleEndomorphism

open ARCFiniteCore ARCTermSemantics ARCFiniteTableContraction
open ARCTwentyDimAssociativity ARCTwentyDimUnit ARCTwentyDimAlgebra
open ARCTwentyDimDualScale
open scoped BigOperators

noncomputable section

variable {R : Type*} [CommRing R] [CharP R 2]

/-- Lower labels have weight one; upper labels have any chosen scalar. -/
def scalarDualWeight (r : R) (i : Nat) : R := if i < 10 then 1 else r

omit [CharP R 2] in
/-- The support law is homogeneous even when the scalar is not a unit. -/
theorem t_term_scalar_weight (r : R) (a b : Fin 20) (term : Nat × Nat)
    (hterm : term ∈ tTerms a.val b.val) :
    scalarDualWeight r term.1 = scalarDualWeight r a.val * scalarDualWeight r b.val := by
  obtain ⟨hout, hab⟩ := t_term_dual_support a b term hterm
  by_cases ha : a.val < 10
  · by_cases hb : b.val < 10
    · simp [scalarDualWeight, ha, hb, hout.mpr ⟨ha, hb⟩]
    · have ht : ¬term.1 < 10 := fun h => hb (hout.mp h).2
      simp [scalarDualWeight, ha, hb, ht]
  · have hb : b.val < 10 := hab.resolve_left ha
    have ht : ¬term.1 < 10 := fun h => ha (hout.mp h).1
    simp [scalarDualWeight, ha, hb, ht]

private theorem weighted_single (q r : R) (j c k : Nat) :
    scalarDualWeight r k * specialize q (singleTerm j c k) =
      scalarDualWeight r j * specialize q (singleTerm j c k) := by
  by_cases hk : k = j <;> simp [singleTerm, hk]

private theorem weighted_sumTerms (q r : R) (terms : Terms) (m : R)
    (hweight : ∀ term ∈ terms, scalarDualWeight r term.1 = m) (k : Nat) :
    scalarDualWeight r k * specialize q (sumTerms terms k) =
      m * specialize q (sumTerms terms k) := by
  induction terms with
  | nil => simp
  | cons term terms ih =>
      have hm : scalarDualWeight r term.1 = m := hweight term (List.mem_cons_self ..)
      have ht : ∀ t ∈ terms, scalarDualWeight r t.1 = m :=
        fun t h => hweight t (List.mem_cons_of_mem _ h)
      rw [sumTerms_cons]
      simp only [Pi.add_apply, map_add, mul_add]
      rw [ih ht]
      congr 1
      rw [← hm]
      exact weighted_single q r term.1 term.2 k

/-- The actual specialized constants are homogeneous for every scalar. -/
theorem specializedConstants_scalar_weight (q r : R) (a b k : Fin 20) :
    scalarDualWeight r k.val * specializedConstants q a b k =
      (scalarDualWeight r a.val * scalarDualWeight r b.val) *
        specializedConstants q a b k := by
  exact weighted_sumTerms q r (tTerms a.val b.val)
    (scalarDualWeight r a.val * scalarDualWeight r b.val)
    (t_term_scalar_weight r a b) k.val

/-- Actual coordinate scaling as an R-linear map. -/
def scalarDualLinearMap (q r : R) : TableAlgebra q →ₗ[R] TableAlgebra q where
  toFun x := ⟨fun i => scalarDualWeight r i.val * x.coords i⟩
  map_add' x y := by
    apply ARCTwentyDimAlgebra.ext q
    funext i
    exact mul_add ..
  map_smul' s x := by
    apply ARCTwentyDimAlgebra.ext q
    funext i
    change scalarDualWeight r i.val * (s * x.coords i) =
      s * (scalarDualWeight r i.val * x.coords i)
    exact mul_left_comm ..

private theorem scalarDualLinearMap_one (q r : R) : scalarDualLinearMap q r 1 = 1 := by
  apply ARCTwentyDimAlgebra.ext q
  funext i
  change scalarDualWeight r i.val * (1 : TableAlgebra q).coords i = _
  rw [coords_one, specialized_unit_coordinates]
  by_cases h0 : i = 0
  · subst i
    simp [scalarDualWeight]
  · by_cases h8 : i = 8
    · subst i
      simp [scalarDualWeight]
    · simp [h0, h8]

private theorem scalarDualLinearMap_mul (q r : R) (x y : TableAlgebra q) :
    scalarDualLinearMap q r (x * y) =
      scalarDualLinearMap q r x * scalarDualLinearMap q r y := by
  apply ARCTwentyDimAlgebra.ext q
  funext k
  change scalarDualWeight r k.val *
      (∑ a : Fin 20, ∑ b : Fin 20,
        x.coords a * y.coords b * specializedConstants q a b k) =
    ∑ a : Fin 20, ∑ b : Fin 20,
      (scalarDualWeight r a.val * x.coords a) *
        (scalarDualWeight r b.val * y.coords b) * specializedConstants q a b k
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro a ha
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro b hb
  calc
    scalarDualWeight r k.val * (x.coords a * y.coords b * specializedConstants q a b k) =
        (x.coords a * y.coords b) *
          (scalarDualWeight r k.val * specializedConstants q a b k) := by ring
    _ = (x.coords a * y.coords b) *
        ((scalarDualWeight r a.val * scalarDualWeight r b.val) *
          specializedConstants q a b k) := by rw [specializedConstants_scalar_weight]
    _ = _ := by ring

/-- The actual R-algebra endomorphism for arbitrary scalar r. -/
def rho (q r : R) : TableAlgebra q →ₐ[R] TableAlgebra q :=
  AlgHom.ofLinearMap (scalarDualLinearMap q r)
    (scalarDualLinearMap_one q r) (scalarDualLinearMap_mul q r)

@[simp] theorem coords_rho (q r : R) (x : TableAlgebra q) (i : Fin 20) :
    (rho q r x).coords i = if i.val < 10 then x.coords i else r * x.coords i := by
  change scalarDualWeight r i.val * x.coords i = _
  by_cases hi : i.val < 10 <;> simp [scalarDualWeight, hi]

/-- Composition multiplies the scalars, as actual algebra homomorphisms. -/
theorem rho_comp (q r s : R) : (rho q s).comp (rho q r) = rho q (s * r) := by
  apply AlgHom.ext
  intro x
  apply ARCTwentyDimAlgebra.ext q
  funext i
  change (rho q s (rho q r x)).coords i = (rho q (s * r) x).coords i
  by_cases hi : i.val < 10 <;> simp [coords_rho, hi, mul_assoc]

theorem rho_one (q : R) : rho q 1 = AlgHom.id R (TableAlgebra q) := by
  apply AlgHom.ext
  intro x
  apply ARCTwentyDimAlgebra.ext q
  funext i
  change (rho q 1 x).coords i = x.coords i
  by_cases hi : i.val < 10 <;> simp [coords_rho, hi]

/-- On units this is the previously constructed genuine automorphism. -/
theorem rho_unit (q : R) (H : Rˣ) : rho q (H : R) = (dualScale q H).toAlgHom := by
  apply AlgHom.ext
  intro x
  apply ARCTwentyDimAlgebra.ext q
  funext i
  exact (coords_rho q (H : R) x i).trans (coords_dualScale_apply q H x i).symm

/-- The zero scalar gives the actual idempotent lower projection. -/
theorem rho_zero_idempotent (q : R) (x : TableAlgebra q) :
    rho q 0 (rho q 0 x) = rho q 0 x := by
  have h := congrArg (fun f : TableAlgebra q →ₐ[R] TableAlgebra q => f x)
    (rho_comp q 0 0)
  simpa only [AlgHom.comp_apply, mul_zero] using h

/-- The projected image is an actual subalgebra of the noncommutative table algebra. -/
def lowerSubalgebra (q : R) : Subalgebra R (TableAlgebra q) := (rho q 0).range

/-- The kernel is an actual ideal, with a two-sided instance even over this noncommutative ring. -/
def upperIdeal (q : R) : Ideal (TableAlgebra q) := RingHom.ker (rho q 0).toRingHom

instance upperIdealIsTwoSided (q : R) : (upperIdeal q).IsTwoSided :=
  inferInstanceAs (RingHom.ker (rho q 0).toRingHom).IsTwoSided

/-- Kernel membership is exactly vanishing of every lower coordinate. -/
theorem mem_upperIdeal (q : R) (x : TableAlgebra q) :
    x ∈ upperIdeal q ↔ ∀ i : Fin 20, i.val < 10 → x.coords i = 0 := by
  change rho q 0 x = 0 ↔ _
  constructor
  · intro h i hi
    have hc := congrArg (fun a : TableAlgebra q => a.coords i) h
    simpa [coords_rho, hi] using hc
  · intro h
    apply ARCTwentyDimAlgebra.ext q
    funext i
    by_cases hi : i.val < 10 <;> simp [coords_rho, hi, h]

/-- Image membership is exactly vanishing of every upper coordinate. -/
theorem mem_lowerSubalgebra (q : R) (x : TableAlgebra q) :
    x ∈ lowerSubalgebra q ↔ ∀ i : Fin 20, ¬ i.val < 10 → x.coords i = 0 := by
  change (∃ y : TableAlgebra q, rho q 0 y = x) ↔ _
  constructor
  · rintro ⟨y, rfl⟩ i hi
    simp [coords_rho, hi]
  · intro h
    refine ⟨x, ?_⟩
    apply ARCTwentyDimAlgebra.ext q
    funext i
    by_cases hi : i.val < 10 <;> simp [coords_rho, hi, h]

private theorem upper_constants_eq_zero (q : R) (a b k : Fin 20)
    (ha : ¬a.val < 10) (hb : ¬b.val < 10) : specializedConstants q a b k = 0 := by
  have hterms : tTerms a.val b.val = [] := by
    apply List.eq_nil_iff_forall_not_mem.mpr
    intro term hterm
    exact (t_term_dual_support a b term hterm).2.elim ha hb
  change specialize q (sumTerms (tTerms a.val b.val) k.val) = 0
  rw [hterms]
  simp

/-- Whole-vector square-zero multiplication in the actual two-sided kernel. -/
theorem upperIdeal_mul_eq_zero (q : R) (x y : TableAlgebra q)
    (hx : x ∈ upperIdeal q) (hy : y ∈ upperIdeal q) : x * y = 0 := by
  have hxc := (mem_upperIdeal q x).mp hx
  have hyc := (mem_upperIdeal q y).mp hy
  apply ARCTwentyDimAlgebra.ext q
  funext k
  change (∑ a : Fin 20, ∑ b : Fin 20,
    x.coords a * y.coords b * specializedConstants q a b k) = 0
  apply Finset.sum_eq_zero
  intro a ha
  apply Finset.sum_eq_zero
  intro b hb
  by_cases hlowA : a.val < 10
  · simp [hxc a hlowA]
  · by_cases hlowB : b.val < 10
    · simp [hyc b hlowB]
    · rw [upper_constants_eq_zero q a b k hlowA hlowB, mul_zero]

/-- The actual lower image as an R-submodule. -/
def lowerSubmodule (q : R) : Submodule R (TableAlgebra q) := (rho q 0).toLinearMap.range

/-- The actual upper kernel as an R-submodule. -/
def upperSubmodule (q : R) : Submodule R (TableAlgebra q) := (rho q 0).toLinearMap.ker

theorem lowerSubalgebra_toSubmodule (q : R) :
    (lowerSubalgebra q).toSubmodule = lowerSubmodule q := by
  ext x
  rfl

theorem upperIdeal_restrictScalars (q : R) :
    (upperIdeal q).restrictScalars R = upperSubmodule q := by
  ext x
  rfl

private theorem rho_zero_linear_idempotent (q : R) :
    IsIdempotentElem (rho q 0).toLinearMap := by
  apply LinearMap.ext
  intro x
  exact rho_zero_idempotent q x

/-- These are complementary actual R-submodules, not merely matching dimensions. -/
theorem lower_upper_isCompl (q : R) : IsCompl (lowerSubmodule q) (upperSubmodule q) :=
  LinearMap.IsIdempotentElem.isCompl (rho_zero_linear_idempotent q)

/-- Genuine R-module splitting of the algebra into its lower image and upper kernel. -/
def lowerUpperLinearEquiv (q : R) :
    TableAlgebra q ≃ₗ[R] (lowerSubmodule q) × (upperSubmodule q) :=
  ((lowerSubmodule q).prodEquivOfIsCompl (upperSubmodule q) (lower_upper_isCompl q)).symm

/-- Multiplication on the split summands has no upper-upper term. -/
theorem lowerUpper_mul (q : R) (c d : lowerSubalgebra q) (x y : upperIdeal q) :
    ((c : TableAlgebra q) + x) * ((d : TableAlgebra q) + y) =
      (c : TableAlgebra q) * d + (c : TableAlgebra q) * y + (x : TableAlgebra q) * d := by
  rw [add_mul, mul_add, mul_add, upperIdeal_mul_eq_zero q x y x.property y.property,
    add_zero, add_assoc]

#print axioms scalarDualWeight
#print axioms t_term_scalar_weight
#print axioms specializedConstants_scalar_weight
#print axioms scalarDualLinearMap
#print axioms rho
#print axioms coords_rho
#print axioms rho_comp
#print axioms rho_one
#print axioms rho_unit
#print axioms rho_zero_idempotent
#print axioms lowerSubalgebra
#print axioms upperIdeal
#print axioms upperIdealIsTwoSided
#print axioms mem_upperIdeal
#print axioms mem_lowerSubalgebra
#print axioms upperIdeal_mul_eq_zero
#print axioms lowerSubmodule
#print axioms upperSubmodule
#print axioms lowerSubalgebra_toSubmodule
#print axioms upperIdeal_restrictScalars
#print axioms lower_upper_isCompl
#print axioms lowerUpperLinearEquiv
#print axioms lowerUpper_mul

end
end ARCTwentyDimDualScaleEndomorphism
