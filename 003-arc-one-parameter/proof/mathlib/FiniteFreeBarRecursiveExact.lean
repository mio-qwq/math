import FiniteFreeBarRecursiveContraction

/-!
The recursively defined finite free A-linear maps obey all adjacent chain
laws and are exact in every degree. The proof uses actual R-linear
coefficient insertion and induction; no finite bound on the degree or
enumeration of words is assumed. All A-valued coefficients are retained.

This is all-degree exactness of the specified module maps. A categorical
projective-resolution object, its low-degree comparison to the previously
installed boundaries, and the Ext application require separate work.
-/

namespace ARCFiniteFreeBarRecursiveExact

open ARCTwentyDimAlgebra ARCFiniteFreeBarModules ARCFiniteFreeBarAugmentation
open ARCFiniteFreeBarInsertion ARCFiniteFreeBarRecursive
open ARCFiniteFreeBarRecursiveContraction ARCCharacterModule

variable {R : Type*} [CommRing R] [CharP R 2]

noncomputable section

variable (q : R) (eps : TableAlgebra q →ₐ[R] R)

private theorem barTerm_add_self (n : Nat) (v : BarTerm q n) : v + v = 0 := by
  funext w
  change v w + v w = 0
  exact CharTwo.add_self_eq_zero (v w)

/-- The augmentation kills the first map of the actual recursive family. -/
theorem augmentation_comp_recursiveBoundary_zero :
    (augmentation q eps).comp (recursiveBoundary q eps 0) = 0 :=
  augmentation_comp_boundary q eps

/-- Every adjacent pair of actual recursive A-linear maps composes to zero. -/
theorem recursiveBoundary_comp (n : Nat) :
    (recursiveBoundary q eps n).comp (recursiveBoundary q eps (n + 1)) = 0 := by
  induction n with
  | zero =>
    apply (wordBasis q 2).ext
    intro w
    have h := recursiveBoundary_succ_basis q eps 0 (w 0) (Fin.tail w)
    rw [Fin.cons_self_tail] at h
    change recursiveBoundary q eps 0
      (recursiveBoundary q eps 1 (wordBasis q 2 w)) = 0
    rw [h, map_add, recursiveBoundary_zero_insertion]
    have haug : augmentation q eps
        (recursiveBoundary q eps 0
          (coordinateBasis q (w 0) • wordBasis q 1 (Fin.tail w))) = 0 :=
      LinearMap.congr_fun (augmentation_comp_recursiveBoundary_zero q eps) _
    rw [haug, map_zero, add_zero, barTerm_add_self]
  | succ n ih =>
    apply (wordBasis q (n + 3)).ext
    intro w
    have h := recursiveBoundary_succ_basis q eps (n + 1) (w 0) (Fin.tail w)
    rw [Fin.cons_self_tail] at h
    change recursiveBoundary q eps (n + 1)
      (recursiveBoundary q eps (n + 2) (wordBasis q (n + 3) w)) = 0
    rw [h, map_add, recursiveBoundary_succ_insertion]
    have hprev : recursiveBoundary q eps n
        (recursiveBoundary q eps (n + 1)
          (coordinateBasis q (w 0) • wordBasis q (n + 2) (Fin.tail w))) = 0 :=
      LinearMap.congr_fun ih _
    rw [hprev, map_zero, add_zero, barTerm_add_self]

/-- A closed vector in any positive degree has its explicit inserted preimage. -/
theorem recursiveBoundary_zero_preimage (n : Nat) (v : BarTerm q (n + 1))
    (hv : recursiveBoundary q eps n v = 0) :
    recursiveBoundary q eps (n + 1) (coefficientInsertion q (n + 1) v) = v := by
  rw [recursiveBoundary_succ_insertion, hv, map_zero, add_zero]

/-- Exactness in every positive degree, with no restriction on the A coefficients. -/
theorem recursiveBoundary_zero_iff_exists (n : Nat) (v : BarTerm q (n + 1)) :
    recursiveBoundary q eps n v = 0 ↔
      ∃ u : BarTerm q (n + 2), recursiveBoundary q eps (n + 1) u = v := by
  constructor
  · intro hv
    exact ⟨coefficientInsertion q (n + 1) v,
      recursiveBoundary_zero_preimage q eps n v hv⟩
  · rintro ⟨u, rfl⟩
    exact LinearMap.congr_fun (recursiveBoundary_comp q eps n) u

/-- Every kernel is the actual range of the following A-linear differential. -/
theorem recursiveBoundary_ker_eq_range (n : Nat) :
    LinearMap.ker (recursiveBoundary q eps n) =
      LinearMap.range (recursiveBoundary q eps (n + 1)) := by
  ext v
  exact recursiveBoundary_zero_iff_exists q eps n v

/-- The recursive family is also exact at the augmentation term P0. -/
theorem augmentation_ker_eq_recursiveBoundary_zero_range :
    LinearMap.ker (augmentation q eps) =
      LinearMap.range (recursiveBoundary q eps 0) :=
  augmentation_ker_eq_boundary_range q eps

#print axioms augmentation_comp_recursiveBoundary_zero
#print axioms recursiveBoundary_comp
#print axioms recursiveBoundary_zero_preimage
#print axioms recursiveBoundary_zero_iff_exists
#print axioms recursiveBoundary_ker_eq_range
#print axioms augmentation_ker_eq_recursiveBoundary_zero_range

end
end ARCFiniteFreeBarRecursiveExact
