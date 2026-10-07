import TwentyDimCochain
import TwentyDimFrobenius
import CochainFullBoundary
import HochschildLowDegrees

/-!
The actual cochain as three nested linear maps on the installed algebra.
Its actual five-face formula vanishes on arbitrary radical-span elements.
This does not identify a relative cohomology or Ext object.
-/

namespace ARCTwentyDimCochainAlgebra

open ARCTwentyDimAlgebra ARCTwentyDimFrobenius ARCTwentyDimCochain
open ARCTwentyDimAssociativity ARCCochainSpecialization ARCFiniteTrilinear
open scoped BigOperators

variable {R : Type*} [CommRing R] [CharP R 2]

noncomputable section

variable (q : R)

/-- The attributed cochain on the actual table algebra. -/
def algebraCochain : TableAlgebra q →ₗ[R] TableAlgebra q →ₗ[R]
    TableAlgebra q →ₗ[R] TableAlgebra q where
  toFun x :=
    { toFun y :=
        { toFun z := ⟨specializedCochain q x.coords y.coords z.coords⟩
          map_add' z z' := by
            apply ARCTwentyDimAlgebra.ext q
            exact eval_add_third (specializedCochainConstants q) x.coords y.coords z.coords z'.coords
          map_smul' r z := by
            apply ARCTwentyDimAlgebra.ext q
            exact eval_smul_third (specializedCochainConstants q) r x.coords y.coords z.coords }
      map_add' y y' := by
        apply LinearMap.ext
        intro z
        apply ARCTwentyDimAlgebra.ext q
        exact eval_add_second (specializedCochainConstants q) x.coords y.coords y'.coords z.coords
      map_smul' r y := by
        apply LinearMap.ext
        intro z
        apply ARCTwentyDimAlgebra.ext q
        exact eval_smul_second (specializedCochainConstants q) r x.coords y.coords z.coords }
  map_add' x x' := by
    apply LinearMap.ext
    intro y
    apply LinearMap.ext
    intro z
    apply ARCTwentyDimAlgebra.ext q
    exact eval_add_first (specializedCochainConstants q) x.coords x'.coords y.coords z.coords
  map_smul' r x := by
    apply LinearMap.ext
    intro y
    apply LinearMap.ext
    intro z
    apply ARCTwentyDimAlgebra.ext q
    exact eval_smul_first (specializedCochainConstants q) r x.coords y.coords z.coords

@[simp] theorem algebraCochain_coords (x y z : TableAlgebra q) :
    (algebraCochain q x y z).coords = specializedCochain q x.coords y.coords z.coords := rfl

theorem coordinateBasis_coords (a : Fin 20) :
    (coordinateBasis q a).coords = basis a := by
  funext b
  simpa only [basis, eq_comm] using coords_coordinateBasis q a b

/-- The installed-algebra cochain has exactly the original basis coefficients. -/
theorem algebraCochain_basis (a b c : Fin 20) :
    (algebraCochain q (coordinateBasis q a) (coordinateBasis q b)
      (coordinateBasis q c)).coords = specializedCochainConstants q a b c := by
  rw [algebraCochain_coords, coordinateBasis_coords, coordinateBasis_coords,
    coordinateBasis_coords, specializedCochain_basis]

/-- The chosen radical-label span as elements of the actual algebra. -/
def radicalElement (U : Fin 18 → R) : TableAlgebra q := ⟨radicalSum U⟩

/-- The actual algebra differential agrees with the proved coordinate formula. -/
theorem algebra_differential3_coords (x y z w : TableAlgebra q) :
    (ARCHochschildLowDegrees.differential3 (fun a b c => algebraCochain q a b c)
      x y z w).coords = specializedDifferential3 q x.coords y.coords z.coords w.coords := rfl

/-- Actual five-face closure for all four radical-span algebra elements. -/
theorem algebraCochain_radical_closed (U V W Z : Fin 18 → R) :
    ARCHochschildLowDegrees.differential3 (fun a b c => algebraCochain q a b c)
      (radicalElement q U) (radicalElement q V) (radicalElement q W)
      (radicalElement q Z) = 0 := by
  apply ARCTwentyDimAlgebra.ext q
  exact specialized_radical_span_closure q U V W Z

/-- Every algebra element is the finite sum of its actual coordinate basis. -/
theorem basis_expansion (x : TableAlgebra q) :
    x = ∑ i : Fin 20, x.coords i • coordinateBasis q i := by
  apply (coordsLinearEquiv q).injective
  rw [map_sum]
  simp only [map_smul]
  change x.coords = ∑ i : Fin 20, x.coords i • (coordinateBasis q i).coords
  funext k
  simp [Finset.sum_apply, coords_coordinateBasis]

/-- Coordinates of an arbitrary actual bilinear cochain on the basis. -/
def bilinearBasisValues (G : TableAlgebra q →ₗ[R] TableAlgebra q →ₗ[R] TableAlgebra q) :
    ARCCochainFullBoundary.VectorTwoCoChain R :=
  fun a b => (G (coordinateBasis q a) (coordinateBasis q b)).coords

theorem bilinear_first_expansion
    (G : TableAlgebra q →ₗ[R] TableAlgebra q →ₗ[R] TableAlgebra q)
    (x y : TableAlgebra q) :
    G x y = ∑ i : Fin 20, x.coords i • G (coordinateBasis q i) y := by
  conv_lhs => rw [basis_expansion q x]
  simp only [map_sum, map_smul, LinearMap.sum_apply, LinearMap.smul_apply]

theorem bilinear_second_expansion
    (G : TableAlgebra q →ₗ[R] TableAlgebra q →ₗ[R] TableAlgebra q)
    (x y : TableAlgebra q) :
    G x y = ∑ i : Fin 20, y.coords i • G x (coordinateBasis q i) := by
  conv_lhs => rw [basis_expansion q y]
  simp only [map_sum, map_smul]

theorem coords_sum {I : Type*} [Fintype I] (f : I → TableAlgebra q) :
    (∑ i, f i).coords = ∑ i, (f i).coords :=
  map_sum (coordsLinearEquiv q) f Finset.univ

theorem coordinateBasis_mul_coords (a b : Fin 20) :
    (coordinateBasis q a * coordinateBasis q b).coords = specializedConstants q a b := by
  rw [coords_mul, coordinateBasis_coords, coordinateBasis_coords]
  exact ARCTwentyDimCochain.mul_basis_basis (specializedConstants q) a b

/-- Full actual-algebra coboundaries on basis inputs are exactly the previously
proved four-face coordinate boundary, for every genuine bilinear cochain. -/
theorem algebra_differential2_basis_coords
    (G : TableAlgebra q →ₗ[R] TableAlgebra q →ₗ[R] TableAlgebra q)
    (a b c : Fin 20) :
    (ARCHochschildLowDegrees.differential2 (fun x y => G x y)
      (coordinateBasis q a) (coordinateBasis q b) (coordinateBasis q c)).coords =
    ARCCochainFullBoundary.fullBasisD2 (specializedConstants q)
      (bilinearBasisValues q G) a b c := by
  have hfirst := congrArg (fun x : TableAlgebra q => x.coords)
    (bilinear_first_expansion q G (coordinateBasis q a * coordinateBasis q b)
      (coordinateBasis q c))
  rw [coords_sum] at hfirst
  simp_rw [coords_smul, coordinateBasis_mul_coords] at hfirst
  have hsecond := congrArg (fun x : TableAlgebra q => x.coords)
    (bilinear_second_expansion q G (coordinateBasis q a)
      (coordinateBasis q b * coordinateBasis q c))
  rw [coords_sum] at hsecond
  simp_rw [coords_smul, coordinateBasis_mul_coords] at hsecond
  simp only [ARCHochschildLowDegrees.differential2, coords_add, coords_mul,
    coordinateBasis_coords, hfirst, hsecond]
  funext k
  simp only [ARCCochainFullBoundary.fullBasisD2, Pi.add_apply, Finset.sum_apply,
    Pi.smul_apply, smul_eq_mul, bilinearBasisValues]
  rfl

/-- No actual bilinear cochain has coboundary agreeing with the fixed cochain
on even the two basis triples of the separating cycle. -/
theorem algebraCochain_no_boundary_interpolation (hq : q ^ 3 ≠ 0) :
    ¬ ∃ G : TableAlgebra q →ₗ[R] TableAlgebra q →ₗ[R] TableAlgebra q,
      ARCHochschildLowDegrees.differential2 (fun x y => G x y)
        (coordinateBasis q 6) (coordinateBasis q 1) (coordinateBasis q 17) =
        algebraCochain q (coordinateBasis q 6) (coordinateBasis q 1) (coordinateBasis q 17) ∧
      ARCHochschildLowDegrees.differential2 (fun x y => G x y)
        (coordinateBasis q 6) (coordinateBasis q 2) (coordinateBasis q 17) =
        algebraCochain q (coordinateBasis q 6) (coordinateBasis q 2) (coordinateBasis q 17) := by
  rintro ⟨G, hx, hy⟩
  have hx' := congrArg (fun x : TableAlgebra q => x.coords) hx
  have hy' := congrArg (fun x : TableAlgebra q => x.coords) hy
  rw [algebra_differential2_basis_coords, algebraCochain_basis] at hx' hy'
  exact ARCCochainFullBoundary.specializedP_no_full_boundary_interpolation q hq
    ⟨bilinearBasisValues q G, hx', hy'⟩

/-- The fixed trilinear map is not the full coboundary of any bilinear map. -/
theorem algebraCochain_not_coboundary (hq : q ^ 3 ≠ 0) :
    ¬ ∃ G : TableAlgebra q →ₗ[R] TableAlgebra q →ₗ[R] TableAlgebra q,
      ARCHochschildLowDegrees.differential2Linear G = algebraCochain q := by
  rintro ⟨G, hG⟩
  apply algebraCochain_no_boundary_interpolation q hq
  refine ⟨G, ?_, ?_⟩
  · exact congrArg (fun F => F (coordinateBasis q 6) (coordinateBasis q 1)
      (coordinateBasis q 17)) hG
  · exact congrArg (fun F => F (coordinateBasis q 6) (coordinateBasis q 2)
      (coordinateBasis q 17)) hG

theorem algebraCochain_not_coboundary_of_nonzero [NoZeroDivisors R]
    (hq : q ≠ 0) :
    ¬ ∃ G : TableAlgebra q →ₗ[R] TableAlgebra q →ₗ[R] TableAlgebra q,
      ARCHochschildLowDegrees.differential2Linear G = algebraCochain q :=
  algebraCochain_not_coboundary q (pow_ne_zero 3 hq)

#print axioms algebraCochain
#print axioms algebraCochain_basis
#print axioms algebraCochain_radical_closed
#print axioms basis_expansion
#print axioms algebra_differential2_basis_coords
#print axioms algebraCochain_no_boundary_interpolation
#print axioms algebraCochain_not_coboundary
#print axioms algebraCochain_not_coboundary_of_nonzero

end
end ARCTwentyDimCochainAlgebra
