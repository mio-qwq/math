import CochainSpecialization
import CochainCycleSemantics

/-!
The fixed vector-valued cochain is separated from the full four-face
two-cochain boundary, already on the two radical triples of the cycle.
Both outer faces are genuine multiplications in the actual table; their
f coordinates vanish. Polynomial and characteristic-two specializations
are covered. This is not an identification with Ext or a complete
Hochschild/relative complex.
-/

namespace ARCCochainFullBoundary

open ARCFiniteCore ARCTermSemantics ARCFiniteTableContraction
open ARCTwentyDimAssociativity ARCCochainBasisSemantics ARCCochainSpecialization
open ARCCochainCycleSemantics
open scoped BigOperators

noncomputable section

set_option maxHeartbeats 1000000

/-- A sparse sum vanishes at a coordinate absent from every list term. -/
theorem sumTerms_absent (terms : Terms) (k : Nat)
    (h : ∀ term ∈ terms, term.1 ≠ k) : sumTerms terms k = 0 := by
  induction terms with
  | nil => rfl
  | cons term terms ih =>
      have hhead := h term (List.mem_cons_self ..)
      have htail : ∀ t ∈ terms, t.1 ≠ k := fun t ht => h t (List.mem_cons_of_mem _ ht)
      simp [sumTerms_cons, singleTerm, Ne.symm hhead, ih htail]

/-- Twenty kernel-checked sparse rows suffice to bound the first outer face.
This is a small output-label check, not a repeated closure enumeration. -/
private theorem t_left_cycle_outputs :
    ∀ j : Fin 20, (tTerms 6 j.val).all (fun term => term.1 ≠ 8) = true := by decide

/-- The analogous twenty rows for the right outer face. -/
private theorem t_right_cycle_outputs :
    ∀ j : Fin 20, (tTerms j.val 17).all (fun term => term.1 ≠ 8) = true := by decide

theorem t_left_cycle_f_coordinate_zero (j : Fin 20) : tConstants 6 j 8 = 0 := by
  change sumTerms (tTerms 6 j.val) 8 = 0
  apply sumTerms_absent
  simpa only [List.all_eq_true, decide_eq_true_eq] using t_left_cycle_outputs j

theorem t_right_cycle_f_coordinate_zero (j : Fin 20) : tConstants j 17 8 = 0 := by
  change sumTerms (tTerms j.val 17) 8 = 0
  apply sumTerms_absent
  simpa only [List.all_eq_true, decide_eq_true_eq] using t_right_cycle_outputs j

abbrev VectorTwoCoChain (R : Type*) := Fin 20 → Fin 20 → (Fin 20 → R)
abbrev VectorThreeCoChain (R : Type*) := Fin 20 → Fin 20 → Fin 20 → (Fin 20 → R)

def basisVector {R : Type*} [CommSemiring R] (a : Fin 20) : Fin 20 → R :=
  fun k => if k = a then 1 else 0

theorem mul_basis_left {R : Type*} [CommSemiring R]
    (B : Fin 20 → Fin 20 → Fin 20 → R) (a k : Fin 20) (v : Fin 20 → R) :
    ARCFiniteBilinear.mul B (basisVector a) v k = ∑ j : Fin 20, B a j k * v j := by
  classical
  simp [ARCFiniteBilinear.mul, basisVector, mul_comm]

theorem mul_basis_right {R : Type*} [CommSemiring R]
    (B : Fin 20 → Fin 20 → Fin 20 → R) (c k : Fin 20) (u : Fin 20 → R) :
    ARCFiniteBilinear.mul B u (basisVector c) k = ∑ j : Fin 20, u j * B j c k := by
  classical
  simp [ARCFiniteBilinear.mul, basisVector]

/-- The full four-face boundary on basis inputs in characteristic two.
The two outer faces use the actual finite structure-constant multiplication. -/
def fullBasisD2 {R : Type*} [CommSemiring R]
    (B : Fin 20 → Fin 20 → Fin 20 → R) (G : VectorTwoCoChain R) : VectorThreeCoChain R :=
  fun a b c =>
    ARCFiniteBilinear.mul B (basisVector a) (G b c) +
      (fun k => ∑ j : Fin 20, B a b j * G j c k) +
      (fun k => ∑ j : Fin 20, B b c j * G a j k) +
      ARCFiniteBilinear.mul B (G a b) (basisVector c)

def fProjection {R : Type*} (G : VectorTwoCoChain R) : ScalarTwoCoChain R :=
  fun a b => G a b 8

/-- The full boundary's two outer faces vanish in coordinate f on the cycle inputs. -/
theorem fullBasisD2_f_projection {R : Type*} [CommSemiring R]
    (B : Fin 20 → Fin 20 → Fin 20 → R) (G : VectorTwoCoChain R)
    (hl : ∀ j, B 6 j 8 = 0) (hr : ∀ j, B j 17 8 = 0) (b : Fin 20) :
    fullBasisD2 B G 6 b 17 8 = scalarInternalD2 B (fProjection G) 6 b 17 := by
  simp only [fullBasisD2, Pi.add_apply, mul_basis_left, mul_basis_right, hl, hr,
    zero_mul, mul_zero, Finset.sum_const_zero, zero_add, add_zero,
    scalarInternalD2, fProjection]

/-- The actual fixed polynomial-valued vector cochain. -/
def polynomialP : VectorThreeCoChain Poly := fun a b c k => pConstants a b c k

theorem polynomial_fullBasisD2_f_projection (G : VectorTwoCoChain Poly) (b : Fin 20) :
    fullBasisD2 tConstants G 6 b 17 8 = scalarInternalD2 tConstants (fProjection G) 6 b 17 :=
  fullBasisD2_f_projection tConstants G t_left_cycle_f_coordinate_zero
    t_right_cycle_f_coordinate_zero b

/-- No full vector-valued boundary agrees with P even on the cycle's two triples. -/
theorem polynomialP_no_full_boundary_interpolation :
    ¬ ∃ G : VectorTwoCoChain Poly,
      fullBasisD2 tConstants G 6 1 17 = polynomialP 6 1 17 ∧
      fullBasisD2 tConstants G 6 2 17 = polynomialP 6 2 17 := by
  rintro ⟨G, hx, hy⟩
  have hx8 := congrArg (fun v : Fin 20 → Poly => v 8) hx
  have hy8 := congrArg (fun v : Fin 20 → Poly => v 8) hy
  rw [polynomial_fullBasisD2_f_projection] at hx8 hy8
  exact polynomial_fCoordinate_no_cycle_interpolation ⟨fProjection G, hx8, hy8⟩

/-- In particular, the polynomial-valued P is not a full two-cochain boundary. -/
theorem polynomialP_not_full_boundary :
    ¬ ∃ G : VectorTwoCoChain Poly, fullBasisD2 tConstants G = polynomialP := by
  rintro ⟨G, hG⟩
  apply polynomialP_no_full_boundary_interpolation
  exact ⟨G, congrFun (congrFun (congrFun hG 6) 1) 17,
    congrFun (congrFun (congrFun hG 6) 2) 17⟩

variable {R : Type*} [CommRing R] [CharP R 2]

theorem specialized_left_cycle_f_coordinate_zero (q : R) (j : Fin 20) :
    specializedConstants q 6 j 8 = 0 := by
  unfold specializedConstants
  rw [t_left_cycle_f_coordinate_zero, map_zero]

theorem specialized_right_cycle_f_coordinate_zero (q : R) (j : Fin 20) :
    specializedConstants q j 17 8 = 0 := by
  unfold specializedConstants
  rw [t_right_cycle_f_coordinate_zero, map_zero]

def specializedP (q : R) : VectorThreeCoChain R :=
  fun a b c k => specializedCochainConstants q a b c k

theorem specialized_fullBasisD2_f_projection (q : R) (G : VectorTwoCoChain R) (b : Fin 20) :
    fullBasisD2 (specializedConstants q) G 6 b 17 8 =
      scalarInternalD2 (specializedConstants q) (fProjection G) 6 b 17 :=
  fullBasisD2_f_projection (specializedConstants q) G
    (specialized_left_cycle_f_coordinate_zero q) (specialized_right_cycle_f_coordinate_zero q) b

/-- Nonzero q³ rules out every full vector-valued boundary on just two radical triples. -/
theorem specializedP_no_full_boundary_interpolation (q : R) (hq : q ^ 3 ≠ 0) :
    ¬ ∃ G : VectorTwoCoChain R,
      fullBasisD2 (specializedConstants q) G 6 1 17 = specializedP q 6 1 17 ∧
      fullBasisD2 (specializedConstants q) G 6 2 17 = specializedP q 6 2 17 := by
  rintro ⟨G, hx, hy⟩
  have hx8 := congrArg (fun v : Fin 20 → R => v 8) hx
  have hy8 := congrArg (fun v : Fin 20 → R => v 8) hy
  rw [specialized_fullBasisD2_f_projection] at hx8 hy8
  exact specialized_fCoordinate_no_cycle_interpolation q hq ⟨fProjection G, hx8, hy8⟩

theorem specializedP_not_full_boundary (q : R) (hq : q ^ 3 ≠ 0) :
    ¬ ∃ G : VectorTwoCoChain R, fullBasisD2 (specializedConstants q) G = specializedP q := by
  rintro ⟨G, hG⟩
  apply specializedP_no_full_boundary_interpolation q hq
  exact ⟨G, congrFun (congrFun (congrFun hG 6) 1) 17,
    congrFun (congrFun (congrFun hG 6) 2) 17⟩

theorem specializedP_not_full_boundary_of_nonzero [NoZeroDivisors R] (q : R) (hq : q ≠ 0) :
    ¬ ∃ G : VectorTwoCoChain R, fullBasisD2 (specializedConstants q) G = specializedP q :=
  specializedP_not_full_boundary q (pow_ne_zero 3 hq)

#print axioms t_left_cycle_f_coordinate_zero
#print axioms t_right_cycle_f_coordinate_zero
#print axioms fullBasisD2_f_projection
#print axioms polynomialP_no_full_boundary_interpolation
#print axioms polynomialP_not_full_boundary
#print axioms specializedP_no_full_boundary_interpolation
#print axioms specializedP_not_full_boundary
#print axioms specializedP_not_full_boundary_of_nonzero

end
end ARCCochainFullBoundary
