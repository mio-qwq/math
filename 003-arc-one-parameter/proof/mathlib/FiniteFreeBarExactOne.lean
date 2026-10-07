import FiniteFreeBarPairLift

/-!
An explicit R-linear contraction in degree one of the actual finite free
left-module presentation. The coefficients of a vector remain elements of
the noncommutative table algebra A. The contraction transfers their twenty
R-coordinates to the two-letter word term, and the full second boundary
recovers the original vector up to the lifted first boundary.

This proves exactness at P1 for the installed boundaries P2 -> P1 -> P0.
The contraction is R-linear; A-linearity is not asserted. No higher
exactness, full projective resolution, or comparison with Ext is stated.
-/

namespace ARCFiniteFreeBarExactOne

open ARCTwentyDimAlgebra ARCTwentyDimCochainAlgebra
open ARCFiniteFreeBarModules ARCFiniteFreeBarAugmentation
open ARCFiniteFreeBarDegreeTwo ARCFiniteFreeBarPairLift ARCCochainWordEquiv
open scoped BigOperators

variable {R : Type*} [CommRing R] [CharP R 2]

noncomputable section

variable (q : R)

/-- Reindexing the genuine A-basis expansion by its one-letter labels. -/
theorem barTerm_one_expansion (v : BarTerm q 1) :
    v = ∑ j : Fin 20, v (oneWord j) • wordBasis q 1 (oneWord j) := by
  classical
  calc
    v = ∑ w : Word 1, v w • wordBasis q 1 w := by
      simpa only [wordBasis_repr] using ((wordBasis q 1).sum_repr v).symm
    _ = ∑ j : Fin 20, v (oneWord j) • wordBasis q 1 (oneWord j) :=
      (oneWordEquiv.symm.sum_comp (fun w => v w • wordBasis q 1 w)).symm

/-- Transfer all coordinates of every A-valued one-word coefficient to P2. -/
def contractingOne : BarTerm q 1 →ₗ[R] BarTerm q 2 where
  toFun v := ∑ j : Fin 20, pairLift q (v (oneWord j)) (coordinateBasis q j)
  map_add' v v' := by
    simp only [Pi.add_apply, map_add, LinearMap.add_apply, Finset.sum_add_distrib]
  map_smul' r v := by
    simp only [RingHom.id_apply, Pi.smul_apply, map_smul, LinearMap.smul_apply,
      Finset.smul_sum]

theorem contractingOne_apply (v : BarTerm q 1) :
    contractingOne q v =
      ∑ j : Fin 20, pairLift q (v (oneWord j)) (coordinateBasis q j) := rfl

private theorem word2_eq_iff (a b c d : Fin 20) :
    word2 a b = word2 c d ↔ a = c ∧ b = d := by
  constructor
  · intro h
    exact ⟨congrArg (fun w : Word 2 => w 0) h,
      congrArg (fun w : Word 2 => w 1) h⟩
  · rintro ⟨rfl, rfl⟩
    rfl

/-- The full pair lift on one basis input has exactly one second label. -/
theorem pairLift_basis_coordinate (x : TableAlgebra q) (j a b : Fin 20) :
    pairLift q x (coordinateBasis q j) (word2 a b) =
      if b = j then algebraMap R (TableAlgebra q) (x.coords a) else 0 := by
  classical
  rw [pairLift_first_expansion]
  simp only [pairLift_basis, Finset.sum_apply, Pi.smul_apply, wordBasis_apply,
    word2_eq_iff]
  by_cases h : b = j <;> simp [h, Algebra.smul_def]

/-- At word (i,j), the contraction has the central coefficient requested
by the full stored R-coordinates of the original A-valued coefficient. -/
theorem contractingOne_word2 (v : BarTerm q 1) (i j : Fin 20) :
    contractingOne q v (word2 i j) =
      algebraMap R (TableAlgebra q) ((v (oneWord j)).coords i) := by
  classical
  rw [contractingOne_apply, Finset.sum_apply]
  simp only [pairLift_basis_coordinate]
  simp

variable (eps : TableAlgebra q →ₐ[R] R)

/-- The first boundary keeps all left A-coefficients. Its scalar right
face commutes with those coefficients by the R-algebra laws. -/
theorem first_boundary_algebra_expansion (v : BarTerm q 1) :
    zeroWordEquiv q (boundary q eps v) = ∑ j : Fin 20,
      (v (oneWord j) * coordinateBasis q j +
        eps (coordinateBasis q j) • v (oneWord j)) := by
  change boundaryToAlgebra q eps v = _
  conv_lhs => rw [barTerm_one_expansion q v]
  rw [map_sum]
  apply Finset.sum_congr rfl
  intro j hj
  simp only [map_smul, boundaryToAlgebra, Module.Basis.constr_basis,
    characterDefect_apply, oneWord, smul_eq_mul, CharTwo.sub_eq_add, mul_add]
  rw [← Algebra.commutes (eps (coordinateBasis q j)) (v (oneWord j)),
    Algebra.smul_def]

/-- The full three-face boundary gives v plus the lifted first boundary. -/
theorem boundary2_contractingOne (v : BarTerm q 1) :
    boundary2 q eps (contractingOne q v) =
      v + singleLift q (zeroWordEquiv q (boundary q eps v)) := by
  classical
  rw [contractingOne_apply, map_sum]
  simp only [boundary2_pairLift, ← singleLift_apply]
  calc
    (∑ j : Fin 20,
        (v (oneWord j) • singleLift q (coordinateBasis q j) +
          singleLift q (v (oneWord j) * coordinateBasis q j) +
          eps (coordinateBasis q j) • singleLift q (v (oneWord j)))) =
        (∑ j : Fin 20, v (oneWord j) • singleLift q (coordinateBasis q j)) +
          singleLift q (∑ j : Fin 20,
            (v (oneWord j) * coordinateBasis q j +
              eps (coordinateBasis q j) • v (oneWord j))) := by
      simp only [map_sum, map_add, map_smul, Finset.sum_add_distrib]
      abel
    _ = v + singleLift q (zeroWordEquiv q (boundary q eps v)) := by
      simp only [singleLift_basis]
      rw [← barTerm_one_expansion q v, first_boundary_algebra_expansion]

/-- The explicit R-linear degree-one contraction identity in the full
actual module. No projection of A-valued coefficients is involved. -/
theorem contracting_identity (v : BarTerm q 1) :
    boundary2 q eps (contractingOne q v) +
      coordinateLift q (zeroWordEquiv q (boundary q eps v)) = v := by
  rw [boundary2_contractingOne, ← singleLift_apply, add_assoc,
    ← two_zsmul, barTerm_two_zsmul, add_zero]

/-- A closed vector has its explicit degree-two preimage. -/
theorem boundary_zero_contractingOne (v : BarTerm q 1) (hv : boundary q eps v = 0) :
    boundary2 q eps (contractingOne q v) = v := by
  rw [boundary2_contractingOne, hv, map_zero, map_zero, add_zero]

/-- Exactness at P1 for every actual character and all A-valued coefficients. -/
theorem boundary_zero_iff_exists_boundary2 (v : BarTerm q 1) :
    boundary q eps v = 0 ↔ ∃ u : BarTerm q 2, boundary2 q eps u = v := by
  constructor
  · intro hv
    exact ⟨contractingOne q v, boundary_zero_contractingOne q eps v hv⟩
  · rintro ⟨u, rfl⟩
    exact congrArg (fun F : BarTerm q 2 →ₗ[TableAlgebra q] BarTerm q 0 => F u)
      (boundary_comp_boundary2 q eps)

/-- Kernel and range equality for the installed A-linear boundaries. -/
theorem boundary_ker_eq_boundary2_range :
    LinearMap.ker (boundary q eps) = LinearMap.range (boundary2 q eps) := by
  ext v
  exact boundary_zero_iff_exists_boundary2 q eps v

#print axioms barTerm_one_expansion
#print axioms contractingOne
#print axioms contractingOne_word2
#print axioms first_boundary_algebra_expansion
#print axioms boundary2_contractingOne
#print axioms contracting_identity
#print axioms boundary_zero_contractingOne
#print axioms boundary_zero_iff_exists_boundary2
#print axioms boundary_ker_eq_boundary2_range

end
end ARCFiniteFreeBarExactOne
