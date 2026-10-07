import FiniteFreeBarModules
import CharacterModule
import Mathlib.Algebra.Algebra.Basic

/-!
The first two actual finite free bar terms, with a character augmentation.
The degree-one boundary sends a basis letter b to b - algebraMap (eps b).
The augmentation is surjective and its kernel equals the boundary image.
This is only the first step of a projective presentation: no all-degree
complex, projective resolution, contracting homotopy or Ext comparison is
asserted here. The algebra remains noncommutative.
-/

namespace ARCFiniteFreeBarAugmentation

open ARCTwentyDimAlgebra ARCFiniteFreeBarModules ARCCharacterModule
open scoped BigOperators

variable {R : Type*} [CommRing R] [CharP R 2]

noncomputable section

/-- The unique word in degree zero. -/
def emptyWord : Word 0 := fun i => Fin.elim0 i

/-- A one-letter word. -/
def oneWord (i : Fin 20) : Word 1 := fun _ => i

/-- One-letter words are exactly the actual coordinate labels. -/
def oneWordEquiv : Word 1 ≃ Fin 20 where
  toFun w := w 0
  invFun := oneWord
  left_inv w := by
    funext i
    have hi : i = (0 : Fin 1) := Subsingleton.elim _ _
    simp only [oneWord, hi]
  right_inv _ := rfl

variable (q : R) (eps : TableAlgebra q →ₐ[R] R)

/-- Evaluation at the empty word identifies P0 with the actual left regular module. -/
def zeroWordEquiv : BarTerm q 0 ≃ₗ[TableAlgebra q] TableAlgebra q where
  toFun v := v emptyWord
  invFun a := fun _ => a
  left_inv v := by
    funext w
    exact congrArg v (Subsingleton.elim _ _)
  right_inv _ := rfl
  map_add' _ _ := rfl
  map_smul' _ _ := rfl

@[simp] theorem zeroWordEquiv_apply (v : BarTerm q 0) :
    zeroWordEquiv q v = v emptyWord := rfl

@[simp] theorem zeroWordEquiv_symm_apply (a : TableAlgebra q) (w : Word 0) :
    (zeroWordEquiv q).symm a w = a := rfl

/-- The character itself, as a genuine map of left A-modules. -/
def characterProjection : TableAlgebra q →ₗ[TableAlgebra q] CharacterModule eps where
  toFun a := CharacterModule.mk (eps a)
  map_add' a b := by
    apply CharacterModule.ext
    exact eps.map_add a b
  map_smul' a b := by
    apply CharacterModule.ext
    exact eps.map_mul a b

@[simp] theorem characterProjection_val (a : TableAlgebra q) :
    (characterProjection q eps a).val = eps a := rfl

/-- The actual character augmentation of P0. -/
def augmentation : BarTerm q 0 →ₗ[TableAlgebra q] CharacterModule eps :=
  (characterProjection q eps).comp (zeroWordEquiv q).toLinearMap

@[simp] theorem augmentation_val (v : BarTerm q 0) :
    (augmentation q eps v).val = eps (zeroWordEquiv q v) := rfl

/-- Scalar elements supply a preimage of every value of the character module. -/
theorem augmentation_surjective : Function.Surjective (augmentation q eps) := by
  intro x
  refine ⟨(zeroWordEquiv q).symm (algebraMap R (TableAlgebra q) x.val), ?_⟩
  apply CharacterModule.ext
  simp

/-- Subtract the scalar character value; this is R-linear, not generally A-linear. -/
def characterDefect : TableAlgebra q →ₗ[R] TableAlgebra q :=
  LinearMap.id - (Algebra.linearMap R (TableAlgebra q)).comp eps.toLinearMap

@[simp] theorem characterDefect_apply (a : TableAlgebra q) :
    characterDefect q eps a = a - algebraMap R (TableAlgebra q) (eps a) := rfl

/-- Extend the prescribed basis-letter images A-linearly. The outer scalar
of Basis.constr is R, so no commutativity of A is required. -/
def boundaryToAlgebra : BarTerm q 1 →ₗ[TableAlgebra q] TableAlgebra q :=
  (wordBasis q 1).constr R (fun w => characterDefect q eps (coordinateBasis q (w 0)))

/-- The actual degree-one boundary P1 -> P0. -/
def boundary : BarTerm q 1 →ₗ[TableAlgebra q] BarTerm q 0 :=
  (zeroWordEquiv q).symm.toLinearMap.comp (boundaryToAlgebra q eps)

@[simp] theorem boundary_basis (w : Word 1) :
    boundary q eps (wordBasis q 1 w) =
      (zeroWordEquiv q).symm
        (coordinateBasis q (w 0) - algebraMap R (TableAlgebra q)
          (eps (coordinateBasis q (w 0)))) := by
  simp [boundary, boundaryToAlgebra]

/-- The augmentation kills every genuine degree-one boundary. -/
theorem augmentation_comp_boundary :
    (augmentation q eps).comp (boundary q eps) = 0 := by
  apply (wordBasis q 1).ext
  intro w
  apply CharacterModule.ext
  change eps (zeroWordEquiv q (boundary q eps (wordBasis q 1 w))) = 0
  rw [boundary_basis, LinearEquiv.apply_symm_apply]
  simp

/-- The actual coordinate basis represents an algebra element by its stored coordinates. -/
theorem coordinateBasis_repr (a : TableAlgebra q) (i : Fin 20) :
    (coordinateBasis q).repr a i = a.coords i := by
  change (Pi.basisFun R (Fin 20)).repr a.coords i = a.coords i
  exact Pi.basisFun_repr R (Fin 20) a.coords i

/-- The genuine finite R-basis expansion used in the lifting argument. -/
theorem coordinate_expansion (a : TableAlgebra q) :
    (∑ i : Fin 20, a.coords i • coordinateBasis q i) = a := by
  simpa only [coordinateBasis_repr] using (coordinateBasis q).sum_repr a

/-- Lift all R-coordinates of an arbitrary actual algebra element into P1. -/
def coordinateLift (a : TableAlgebra q) : BarTerm q 1 :=
  fun w => algebraMap R (TableAlgebra q) (a.coords (w 0))

/-- The lifted boundary is exactly a minus its scalar character value. -/
theorem boundaryToAlgebra_coordinateLift (a : TableAlgebra q) :
    boundaryToAlgebra q eps (coordinateLift q a) = characterDefect q eps a := by
  classical
  calc
    boundaryToAlgebra q eps (coordinateLift q a) =
        ∑ w : Word 1, (algebraMap R (TableAlgebra q) (a.coords (w 0))) •
          characterDefect q eps (coordinateBasis q (w 0)) := by
      rw [boundaryToAlgebra, Module.Basis.constr_apply_fintype]
      simp only [Module.Basis.equivFun_apply, wordBasis_repr, coordinateLift]
    _ = ∑ w : Word 1, a.coords (w 0) •
          characterDefect q eps (coordinateBasis q (w 0)) := by
      simp only [_root_.algebraMap_smul]
    _ = ∑ i : Fin 20, a.coords i • characterDefect q eps (coordinateBasis q i) :=
      oneWordEquiv.sum_comp (fun i => a.coords i • characterDefect q eps (coordinateBasis q i))
    _ = characterDefect q eps (∑ i : Fin 20, a.coords i • coordinateBasis q i) := by
      rw [map_sum]
      simp only [map_smul]
    _ = characterDefect q eps a := by rw [coordinate_expansion]

theorem boundary_coordinateLift (a : TableAlgebra q) :
    boundary q eps (coordinateLift q a) =
      (zeroWordEquiv q).symm (a - algebraMap R (TableAlgebra q) (eps a)) := by
  simp only [boundary, LinearMap.comp_apply, LinearEquiv.coe_coe,
    boundaryToAlgebra_coordinateLift, characterDefect_apply]

/-- Every element of the actual augmentation kernel has an explicit boundary preimage. -/
theorem augmentation_zero_iff_exists_boundary (v : BarTerm q 0) :
    augmentation q eps v = 0 ↔ ∃ u : BarTerm q 1, boundary q eps u = v := by
  constructor
  · intro hv
    have heps : eps (zeroWordEquiv q v) = 0 := by
      have h := congrArg CharacterModule.val hv
      simpa only [augmentation_val, val_zero] using h
    refine ⟨coordinateLift q (zeroWordEquiv q v), ?_⟩
    rw [boundary_coordinateLift, heps, map_zero, sub_zero]
    exact (zeroWordEquiv q).symm_apply_apply v
  · rintro ⟨u, hu⟩
    rw [← hu]
    exact congrArg (fun f : BarTerm q 1 →ₗ[TableAlgebra q] CharacterModule eps => f u)
      (augmentation_comp_boundary q eps)

/-- Exactness of the actual projective presentation at P0. -/
theorem augmentation_ker_eq_boundary_range :
    LinearMap.ker (augmentation q eps) = LinearMap.range (boundary q eps) := by
  ext v
  exact augmentation_zero_iff_exists_boundary q eps v

#print axioms zeroWordEquiv
#print axioms characterProjection
#print axioms augmentation_surjective
#print axioms boundary_basis
#print axioms augmentation_comp_boundary
#print axioms coordinate_expansion
#print axioms boundaryToAlgebra_coordinateLift
#print axioms boundary_coordinateLift
#print axioms augmentation_zero_iff_exists_boundary
#print axioms augmentation_ker_eq_boundary_range

end
end ARCFiniteFreeBarAugmentation
