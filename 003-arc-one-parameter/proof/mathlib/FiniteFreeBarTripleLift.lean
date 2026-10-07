import FiniteFreeBarPairLift

/-!
The full three-word lift is an actual R-trilinear map into the third
finite free A-module. The actual third boundary on this lift has its four
faces as an equality in the entire second free module. All coefficients
remain in the noncommutative algebra A; no character projection is used.

This file proves only the lift and boundary semantics. It does not assert
the third/fourth boundary composition, exactness, a resolution, or Ext.
-/

namespace ARCFiniteFreeBarTripleLift

open ARCTwentyDimAlgebra ARCTwentyDimCochainAlgebra ARCTwentyDimAssociativity
open ARCFiniteFreeBarModules ARCFiniteFreeBarDegreeThree ARCFiniteFreeBarPairLift
open ARCCochainWordEquiv
open scoped BigOperators

variable {R : Type*} [CommRing R] [CharP R 2]

noncomputable section

variable (q : R)

/-- Three nested basis extensions give a genuine R-trilinear full-word lift. -/
def tripleLift : TableAlgebra q →ₗ[R] TableAlgebra q →ₗ[R]
    TableAlgebra q →ₗ[R] BarTerm q 3 :=
  (coordinateBasis q).constr R (fun a =>
    (coordinateBasis q).constr R (fun b =>
      (coordinateBasis q).constr R (fun c => wordBasis q 3 (word3 a b c))))

@[simp] theorem tripleLift_basis (a b c : Fin 20) :
    tripleLift q (coordinateBasis q a) (coordinateBasis q b) (coordinateBasis q c) =
      wordBasis q 3 (word3 a b c) := by
  simp [tripleLift]

private theorem reverse_three_sums {M : Type*} [AddCommMonoid M]
    (f : Fin 20 → Fin 20 → Fin 20 → M) :
    (∑ c, ∑ b, ∑ a, f a b c) = ∑ a, ∑ b, ∑ c, f a b c := by
  calc
    _ = ∑ b, ∑ c, ∑ a, f a b c := Finset.sum_comm
    _ = ∑ b, ∑ a, ∑ c, f a b c := by
      apply Finset.sum_congr rfl
      intro b _
      exact Finset.sum_comm
    _ = ∑ a, ∑ b, ∑ c, f a b c := Finset.sum_comm

/-- The trilinear lift has the full finite three-coordinate contraction. -/
theorem tripleLift_apply (x y z : TableAlgebra q) :
    tripleLift q x y z = ∑ a : Fin 20, ∑ b : Fin 20, ∑ c : Fin 20,
      (x.coords a * y.coords b * z.coords c) • wordBasis q 3 (word3 a b c) := by
  conv_lhs => rw [basis_expansion q x, basis_expansion q y, basis_expansion q z]
  simp only [map_sum, map_smul, LinearMap.sum_apply, LinearMap.smul_apply,
    tripleLift_basis, Finset.smul_sum, smul_smul]
  rw [reverse_three_sums]
  apply Finset.sum_congr rfl
  intro a _
  apply Finset.sum_congr rfl
  intro b _
  apply Finset.sum_congr rfl
  intro c _
  congr 1
  ac_rfl

variable (eps : TableAlgebra q →ₐ[R] R)

/-- The four actual faces, packaged as a true R-trilinear map. -/
def tripleFaces : TableAlgebra q →ₗ[R] TableAlgebra q →ₗ[R]
    TableAlgebra q →ₗ[R] BarTerm q 2 where
  toFun x :=
    { toFun y :=
        { toFun z := x • pairLift q y z + pairLift q (x * y) z +
            pairLift q x (y * z) + eps z • pairLift q x y
          map_add' z z' := by
            simp only [map_add, mul_add, smul_add, add_smul]
            abel
          map_smul' r z := by
            simp only [RingHom.id_apply, map_smul, Algebra.mul_smul_comm,
              smul_add, smul_smul, smul_eq_mul]
            rw [smul_algebra_smul_comm r x (pairLift q y z)] }
      map_add' y y' := by
        apply LinearMap.ext
        intro z
        change x • pairLift q (y + y') z + pairLift q (x * (y + y')) z +
          pairLift q x ((y + y') * z) + eps z • pairLift q x (y + y') =
            (x • pairLift q y z + pairLift q (x * y) z +
              pairLift q x (y * z) + eps z • pairLift q x y) +
            (x • pairLift q y' z + pairLift q (x * y') z +
              pairLift q x (y' * z) + eps z • pairLift q x y')
        simp only [map_add, mul_add, add_mul, LinearMap.add_apply, smul_add]
        abel
      map_smul' r y := by
        apply LinearMap.ext
        intro z
        change x • pairLift q (r • y) z + pairLift q (x * (r • y)) z +
          pairLift q x ((r • y) * z) + eps z • pairLift q x (r • y) =
            r • (x • pairLift q y z + pairLift q (x * y) z +
              pairLift q x (y * z) + eps z • pairLift q x y)
        simp only [map_smul, Algebra.mul_smul_comm, Algebra.smul_mul_assoc,
          LinearMap.smul_apply, smul_add, smul_smul]
        rw [smul_algebra_smul_comm r x (pairLift q y z), mul_comm (eps z) r] }
  map_add' x x' := by
    apply LinearMap.ext
    intro y
    apply LinearMap.ext
    intro z
    change (x + x') • pairLift q y z + pairLift q ((x + x') * y) z +
      pairLift q (x + x') (y * z) + eps z • pairLift q (x + x') y =
        (x • pairLift q y z + pairLift q (x * y) z +
          pairLift q x (y * z) + eps z • pairLift q x y) +
        (x' • pairLift q y z + pairLift q (x' * y) z +
          pairLift q x' (y * z) + eps z • pairLift q x' y)
    simp only [map_add, add_mul, LinearMap.add_apply, smul_add, add_smul]
    abel
  map_smul' r x := by
    apply LinearMap.ext
    intro y
    apply LinearMap.ext
    intro z
    change (r • x) • pairLift q y z + pairLift q ((r • x) * y) z +
      pairLift q (r • x) (y * z) + eps z • pairLift q (r • x) y =
        r • (x • pairLift q y z + pairLift q (x * y) z +
          pairLift q x (y * z) + eps z • pairLift q x y)
    have hs (a : TableAlgebra q) (v : BarTerm q 2) : (r • a) • v = r • (a • v) :=
      smul_assoc r a v
    simp only [map_smul, Algebra.smul_mul_assoc, LinearMap.smul_apply, smul_add, hs,
      smul_smul]
    rw [mul_comm (eps z) r]

/-- The actual third boundary postcomposed with the trilinear lift. -/
def boundary3TripleLift : TableAlgebra q →ₗ[R] TableAlgebra q →ₗ[R]
    TableAlgebra q →ₗ[R] BarTerm q 2 where
  toFun x :=
    { toFun y := ((boundary3 q eps).restrictScalars R).comp (tripleLift q x y)
      map_add' y y' := by
        apply LinearMap.ext
        intro z
        simp only [LinearMap.comp_apply, map_add, LinearMap.add_apply]
      map_smul' r y := by
        apply LinearMap.ext
        intro z
        simp only [RingHom.id_apply, LinearMap.comp_apply, map_smul, LinearMap.smul_apply] }
  map_add' x x' := by
    apply LinearMap.ext
    intro y
    apply LinearMap.ext
    intro z
    change boundary3 q eps (tripleLift q (x + x') y z) =
      boundary3 q eps (tripleLift q x y z) + boundary3 q eps (tripleLift q x' y z)
    simp only [map_add, LinearMap.add_apply]
  map_smul' r x := by
    apply LinearMap.ext
    intro y
    apply LinearMap.ext
    intro z
    change boundary3 q eps (tripleLift q (r • x) y z) =
      r • boundary3 q eps (tripleLift q x y z)
    simp only [map_smul, LinearMap.smul_apply, (boundary3 q eps).map_smul_of_tower]

/-- All three actual input slots agree, by their complete coordinate basis.
This is equality of full trilinear maps into the second free module. -/
theorem boundary3TripleLift_eq_tripleFaces :
    boundary3TripleLift q eps = tripleFaces q eps := by
  apply (coordinateBasis q).ext
  intro a
  apply (coordinateBasis q).ext
  intro b
  apply (coordinateBasis q).ext
  intro c
  change boundary3 q eps (tripleLift q (coordinateBasis q a)
    (coordinateBasis q b) (coordinateBasis q c)) = _
  rw [tripleLift_basis, boundary3_pairLift_basis]
  rfl

/-- Exact four-face semantics of the actual third boundary, on arbitrary
actual algebra triples, retaining all A-valued free-module coefficients. -/
theorem boundary3_tripleLift (x y z : TableAlgebra q) :
    boundary3 q eps (tripleLift q x y z) =
      x • pairLift q y z + pairLift q (x * y) z +
        pairLift q x (y * z) + eps z • pairLift q x y := by
  have h := congrArg (fun F : TableAlgebra q →ₗ[R] TableAlgebra q →ₗ[R]
    TableAlgebra q →ₗ[R] BarTerm q 2 => F x y z)
    (boundary3TripleLift_eq_tripleFaces q eps)
  change boundary3 q eps (tripleLift q x y z) =
    x • pairLift q y z + pairLift q (x * y) z +
      pairLift q x (y * z) + eps z • pairLift q x y at h
  exact h

#print axioms tripleLift
#print axioms tripleLift_basis
#print axioms tripleLift_apply
#print axioms tripleFaces
#print axioms boundary3TripleLift_eq_tripleFaces
#print axioms boundary3_tripleLift

end
end ARCFiniteFreeBarTripleLift
