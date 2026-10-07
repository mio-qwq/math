import TwentyDimFrobenius
import Mathlib.Algebra.Module.Injective
import Mathlib.LinearAlgebra.Basis.VectorSpace
import Mathlib.Algebra.Algebra.RestrictScalars

/-!
Self-injectivity of the actual twenty-dimensional algebra over a field.
An arbitrary A-linear map from a submodule is extended by first extending
its scalar trace, and then recovering an A-valued map through the perfect
trace duality. All modules in the extension argument are arbitrary: no
finite-dimensional hypothesis on them is used. The parameter q is arbitrary.

The proof respects the noncommutative order: testing the extension on a
left coefficient a uses the scalar functional on a acting on the input.
Only the symmetrizing trace rotates the product, never commutativity of A.
Restriction of scalars is installed explicitly when constructing the
Module.Injective witness. No injectivity claim over general commutative
coefficient rings or Ext/stable-category comparison is asserted here.
-/

namespace ARCTwentyDimSelfInjective

open ARCTwentyDimAlgebra ARCTwentyDimFrobenius

universe u v w
variable {k : Type u} [Field k] [CharP k 2]

noncomputable section

variable (q : k)

section TraceLift

variable {M : Type v} [AddCommGroup M]
  [Module k M] [Module (TableAlgebra q) M] [IsScalarTower k (TableAlgebra q) M]

/-- A scalar functional tested on the actual left A-action is k-linear
in the testing coefficient. The scalar tower supplies this compatibility. -/
def orbitFunctional (ell : M →ₗ[k] k) (m : M) : TableAlgebra q →ₗ[k] k where
  toFun a := ell (a • m)
  map_add' a b := by rw [add_smul, map_add]
  map_smul' r a := by
    change ell ((r • a) • m) = r • ell (a • m)
    rw [smul_assoc, map_smul]

/-- Recover the full actual A-valued element from all scalar action tests. -/
def traceLift (ell : M →ₗ[k] k) (m : M) : TableAlgebra q :=
  (traceDualEquiv q).symm (orbitFunctional q ell m)

/-- This equality characterizes every recovered element by the perfect trace. -/
theorem traceLift_pairing (ell : M →ₗ[k] k) (m : M) (a : TableAlgebra q) :
    tracePairing q (traceLift q ell m) a = ell (a • m) := by
  have h := LinearMap.congr_fun
    ((traceDualEquiv q).apply_symm_apply (orbitFunctional q ell m)) a
  change tracePairing q (traceLift q ell m) a = ell (a • m) at h
  exact h

theorem traceLift_add (ell : M →ₗ[k] k) (m m' : M) :
    traceLift q ell (m + m') = traceLift q ell m + traceLift q ell m' := by
  apply (traceDualEquiv q).injective
  apply LinearMap.ext
  intro a
  change tracePairing q (traceLift q ell (m + m')) a =
    tracePairing q (traceLift q ell m + traceLift q ell m') a
  rw [traceLift_pairing, map_add, LinearMap.add_apply, traceLift_pairing,
    traceLift_pairing, smul_add, map_add]

/-- Left A-linearity follows by testing in order a*b, then rotating the
trace pairing. No pair of A-elements is assumed to commute. -/
theorem traceLift_algebra_smul (ell : M →ₗ[k] k) (b : TableAlgebra q) (m : M) :
    traceLift q ell (b • m) = b * traceLift q ell m := by
  apply (traceDualEquiv q).injective
  apply LinearMap.ext
  intro a
  change tracePairing q (traceLift q ell (b • m)) a =
    tracePairing q (b * traceLift q ell m) a
  calc
    _ = ell (a • (b • m)) := traceLift_pairing q ell (b • m) a
    _ = ell ((a * b) • m) := by rw [smul_smul]
    _ = tracePairing q (traceLift q ell m) (a * b) :=
      (traceLift_pairing q ell m (a * b)).symm
    _ = tracePairing q (a * b) (traceLift q ell m) :=
      tracePairing_symmetric q (traceLift q ell m) (a * b)
    _ = tracePairing q a (b * traceLift q ell m) :=
      tracePairing_invariant q a b (traceLift q ell m)
    _ = _ := tracePairing_symmetric q a (b * traceLift q ell m)

/-- The recovered extension is a genuine left A-linear map. -/
def traceLiftLinear (ell : M →ₗ[k] k) : M →ₗ[TableAlgebra q] TableAlgebra q where
  toFun := traceLift q ell
  map_add' := traceLift_add q ell
  map_smul' b m := by
    change traceLift q ell (b • m) = b * traceLift q ell m
    exact traceLift_algebra_smul q ell b m

@[simp] theorem traceLiftLinear_apply (ell : M →ₗ[k] k) (m : M) :
    traceLiftLinear q ell m = traceLift q ell m := rfl

end TraceLift

section Extension

variable {M : Type v} {N : Type w} [AddCommGroup M] [AddCommGroup N]
  [Module k M] [Module k N]
  [Module (TableAlgebra q) M] [Module (TableAlgebra q) N]
  [IsScalarTower k (TableAlgebra q) M] [IsScalarTower k (TableAlgebra q) N]

/-- Every A-linear map extends across every injective A-linear map, once
the compatible field scalar structures have been specified. The field is
used only for the k-linear left inverse, not to invert q. -/
theorem linearMap_extension (j : M →ₗ[TableAlgebra q] N)
    (hj : Function.Injective j) (f : M →ₗ[TableAlgebra q] TableAlgebra q) :
    ∃ g : N →ₗ[TableAlgebra q] TableAlgebra q, g.comp j = f := by
  obtain ⟨r, hr⟩ := (j.restrictScalars k).exists_leftInverse_of_injective
    (LinearMap.ker_eq_bot.mpr hj)
  let ell : N →ₗ[k] k := (traceLinear q).comp ((f.restrictScalars k).comp r)
  refine ⟨traceLiftLinear q ell, ?_⟩
  apply LinearMap.ext
  intro m
  change traceLift q ell (j m) = f m
  apply (traceDualEquiv q).injective
  apply LinearMap.ext
  intro a
  change tracePairing q (traceLift q ell (j m)) a = tracePairing q (f m) a
  rw [traceLift_pairing]
  change traceLinear q (f (r (a • j m))) = tracePairing q (f m) a
  have hr_apply (t : M) : r (j t) = t := LinearMap.congr_fun hr t
  rw [← j.map_smul, hr_apply, f.map_smul]
  change tracePairing q a (f m) = tracePairing q (f m) a
  exact tracePairing_symmetric q a (f m)

end Extension

/-- The actual left regular module is injective, for every field parameter.
The witness installs the inherited k-action on arbitrary A-modules and
uses the preceding full extension theorem. No injectivity premise is used. -/
theorem tableAlgebra_injective :
    Module.Injective (TableAlgebra q) (TableAlgebra q) where
  out M N _ _ _ _ j hj f := by
    let : Module k M := Module.restrictScalars k (TableAlgebra q) M
    let : Module k N := Module.restrictScalars k (TableAlgebra q) N
    let : IsScalarTower k (TableAlgebra q) M :=
      IsScalarTower.restrictScalars k (TableAlgebra q) M
    let : IsScalarTower k (TableAlgebra q) N :=
      IsScalarTower.restrictScalars k (TableAlgebra q) N
    obtain ⟨g, hg⟩ := linearMap_extension q j hj f
    exact ⟨g, fun m => LinearMap.congr_fun hg m⟩

instance tableAlgebraModuleInjective :
    Module.Injective (TableAlgebra q) (TableAlgebra q) := tableAlgebra_injective q

#print axioms orbitFunctional
#print axioms traceLift
#print axioms traceLift_pairing
#print axioms traceLift_algebra_smul
#print axioms traceLiftLinear
#print axioms linearMap_extension
#print axioms tableAlgebra_injective

end
end ARCTwentyDimSelfInjective
