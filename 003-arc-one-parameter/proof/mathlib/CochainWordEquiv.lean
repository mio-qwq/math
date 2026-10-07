import FiniteFreeBarModules
import TwentyDimCochainAlgebra
import CharacterHochschildMaps
import Mathlib.LinearAlgebra.Pi
import Mathlib.Data.Fin.Tuple.Basic

/-!
# All scalar cochains as word coefficients

The actual table algebra's coordinate basis constructs mutually inverse
R-linear equivalences between all scalar bilinear/trilinear cochains and
arbitrary scalar functions on words of length two/three. Evaluation on
basis inputs and inverse finite-sum formulas are explicit.

These are degreewise coordinate equivalences only. No compatibility with
a bar differential, exact resolution, or comparison with Ext is asserted.
-/

namespace ARCCochainWordEquiv

open ARCTwentyDimAlgebra ARCTwentyDimCochainAlgebra ARCFiniteFreeBarModules
open ARCCharacterHochschildMaps
open scoped BigOperators

/-- A two-letter word with its prescribed ordered entries. -/
def word2 (a b : Fin 20) : Word 2 := Fin.cons a (Fin.cons b Fin.elim0)

/-- A three-letter word, retaining its ordered entries. -/
def word3 (a b c : Fin 20) : Word 3 := Fin.cons a (word2 b c)

theorem word2_eta (w : Word 2) : word2 (w 0) (w 1) = w := by
  have hnil : (Fin.elim0 : Fin 0 → Fin 20) = Fin.tail (Fin.tail w) :=
    Subsingleton.elim _ _
  change Fin.cons (w 0) (Fin.cons ((Fin.tail w) 0) Fin.elim0) = w
  rw [hnil, Fin.cons_self_tail, Fin.cons_self_tail]

theorem word3_eta (w : Word 3) : word3 (w 0) (w 1) (w 2) = w := by
  change Fin.cons (w 0) (word2 ((Fin.tail w) 0) ((Fin.tail w) 1)) = w
  rw [word2_eta, Fin.cons_self_tail]

section ScalarFunctions

variable {R : Type*} [CommRing R]

/-- Ordered pairs of input labels and length-two words carry the same
arbitrary scalar functions, as a genuine R-linear equivalence. -/
def curried2WordEquiv : (Fin 20 → Fin 20 → R) ≃ₗ[R] (Word 2 → R) where
  toFun f w := f (w 0) (w 1)
  invFun h a b := h (word2 a b)
  left_inv f := by funext a b; rfl
  right_inv h := by funext w; change h (word2 (w 0) (w 1)) = h w; rw [word2_eta]
  map_add' _ _ := rfl
  map_smul' _ _ := rfl

/-- The analogous ordered-triple equivalence, with no selected subspace. -/
def curried3WordEquiv : (Fin 20 → Fin 20 → Fin 20 → R) ≃ₗ[R] (Word 3 → R) where
  toFun f w := f (w 0) (w 1) (w 2)
  invFun h a b c := h (word3 a b c)
  left_inv f := by funext a b c; rfl
  right_inv h := by
    funext w
    change h (word3 (w 0) (w 1) (w 2)) = h w
    rw [word3_eta]
  map_add' _ _ := rfl
  map_smul' _ _ := rfl

end ScalarFunctions

variable {R : Type*} [CommRing R] [CharP R 2]

noncomputable section

variable (q : R)

omit [CharP R 2] in
private theorem reverse_three_sums (f : Fin 20 → Fin 20 → Fin 20 → R) :
    (∑ c, ∑ b, ∑ a, f a b c) = ∑ a, ∑ b, ∑ c, f a b c := by
  calc
    _ = ∑ b, ∑ c, ∑ a, f a b c := Finset.sum_comm
    _ = ∑ b, ∑ a, ∑ c, f a b c := by
      apply Finset.sum_congr rfl
      intro b hb
      exact Finset.sum_comm
    _ = ∑ a, ∑ b, ∑ c, f a b c := Finset.sum_comm

/-- All scalar linear maps are determined by unrestricted coordinate-basis values. -/
def cochain1BasisEquiv : (TableAlgebra q →ₗ[R] R) ≃ₗ[R] (Fin 20 → R) :=
  ((coordinateBasis q).constr (M' := R) R).symm

/-- Nested basis construction gives the full scalar bilinear cochain space. -/
def cochain2BasisEquiv : C2S R (TableAlgebra q) ≃ₗ[R] (Fin 20 → Fin 20 → R) :=
  ((coordinateBasis q).constr (M' := TableAlgebra q →ₗ[R] R) R).symm.trans
    (LinearEquiv.piCongrRight (fun _ : Fin 20 => cochain1BasisEquiv q))

/-- Three nested basis constructions give all scalar trilinear cochains. -/
def cochain3BasisEquiv : C3S R (TableAlgebra q) ≃ₗ[R]
    (Fin 20 → Fin 20 → Fin 20 → R) :=
  ((coordinateBasis q).constr (M' := C2S R (TableAlgebra q)) R).symm.trans
    (LinearEquiv.piCongrRight (fun _ : Fin 20 => cochain2BasisEquiv q))

@[simp] theorem cochain2BasisEquiv_apply (G : C2S R (TableAlgebra q)) (a b : Fin 20) :
    cochain2BasisEquiv q G a b = G (coordinateBasis q a) (coordinateBasis q b) := rfl

@[simp] theorem cochain3BasisEquiv_apply (F : C3S R (TableAlgebra q)) (a b c : Fin 20) :
    cochain3BasisEquiv q F a b c =
      F (coordinateBasis q a) (coordinateBasis q b) (coordinateBasis q c) := rfl

/-- Reconstruction recovers every arbitrarily specified pair coefficient. -/
theorem cochain2BasisEquiv_symm_basis (h : Fin 20 → Fin 20 → R) (a b : Fin 20) :
    (cochain2BasisEquiv q).symm h (coordinateBasis q a) (coordinateBasis q b) = h a b :=
  congrFun (congrFun ((cochain2BasisEquiv q).apply_symm_apply h) a) b

/-- Reconstruction recovers every arbitrarily specified triple coefficient. -/
theorem cochain3BasisEquiv_symm_basis (h : Fin 20 → Fin 20 → Fin 20 → R)
    (a b c : Fin 20) :
    (cochain3BasisEquiv q).symm h (coordinateBasis q a) (coordinateBasis q b)
      (coordinateBasis q c) = h a b c :=
  congrFun (congrFun (congrFun ((cochain3BasisEquiv q).apply_symm_apply h) a) b) c

/-- The actual inverse bilinear map is the finite contraction of the two
input coordinate vectors with its arbitrary basis coefficients. -/
theorem cochain2BasisEquiv_symm_apply (h : Fin 20 → Fin 20 → R)
    (x y : TableAlgebra q) :
    (cochain2BasisEquiv q).symm h x y =
      ∑ a : Fin 20, ∑ b : Fin 20, x.coords a * y.coords b * h a b := by
  conv_lhs => rw [basis_expansion q x, basis_expansion q y]
  simp only [map_sum, map_smul, LinearMap.sum_apply, LinearMap.smul_apply,
    smul_eq_mul, cochain2BasisEquiv_symm_basis, Finset.mul_sum]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro a ha
  apply Finset.sum_congr rfl
  intro b hb
  ac_rfl

/-- The actual inverse trilinear map has the full finite threefold contraction. -/
theorem cochain3BasisEquiv_symm_apply (h : Fin 20 → Fin 20 → Fin 20 → R)
    (x y z : TableAlgebra q) :
    (cochain3BasisEquiv q).symm h x y z =
      ∑ a : Fin 20, ∑ b : Fin 20, ∑ c : Fin 20,
        x.coords a * y.coords b * z.coords c * h a b c := by
  conv_lhs => rw [basis_expansion q x, basis_expansion q y, basis_expansion q z]
  simp only [map_sum, map_smul, LinearMap.sum_apply, LinearMap.smul_apply,
    smul_eq_mul, cochain3BasisEquiv_symm_basis, Finset.mul_sum]
  rw [reverse_three_sums]
  apply Finset.sum_congr rfl
  intro a ha
  apply Finset.sum_congr rfl
  intro b hb
  apply Finset.sum_congr rfl
  intro c hc
  ac_rfl

/-- All scalar bilinear cochains are equivalent to arbitrary length-two
word coefficients, not merely injected into a coefficient function space. -/
def cochain2WordEquiv : C2S R (TableAlgebra q) ≃ₗ[R] (Word 2 → R) :=
  (cochain2BasisEquiv q).trans curried2WordEquiv

/-- The full trilinear cochain/length-three-word coefficient equivalence. -/
def cochain3WordEquiv : C3S R (TableAlgebra q) ≃ₗ[R] (Word 3 → R) :=
  (cochain3BasisEquiv q).trans curried3WordEquiv

@[simp] theorem cochain2WordEquiv_apply (G : C2S R (TableAlgebra q)) (w : Word 2) :
    cochain2WordEquiv q G w = G (coordinateBasis q (w 0)) (coordinateBasis q (w 1)) := rfl

@[simp] theorem cochain3WordEquiv_apply (F : C3S R (TableAlgebra q)) (w : Word 3) :
    cochain3WordEquiv q F w = F (coordinateBasis q (w 0)) (coordinateBasis q (w 1))
      (coordinateBasis q (w 2)) := rfl

/-- The inverse word-coefficient map on arbitrary actual algebra inputs. -/
theorem cochain2WordEquiv_symm_apply (h : Word 2 → R) (x y : TableAlgebra q) :
    (cochain2WordEquiv q).symm h x y =
      ∑ a : Fin 20, ∑ b : Fin 20, x.coords a * y.coords b * h (word2 a b) :=
  cochain2BasisEquiv_symm_apply q (fun a b => h (word2 a b)) x y

theorem cochain3WordEquiv_symm_apply (h : Word 3 → R) (x y z : TableAlgebra q) :
    (cochain3WordEquiv q).symm h x y z =
      ∑ a : Fin 20, ∑ b : Fin 20, ∑ c : Fin 20,
        x.coords a * y.coords b * z.coords c * h (word3 a b c) :=
  cochain3BasisEquiv_symm_apply q (fun a b c => h (word3 a b c)) x y z

#print axioms curried2WordEquiv
#print axioms curried3WordEquiv
#print axioms cochain2BasisEquiv
#print axioms cochain3BasisEquiv
#print axioms cochain2BasisEquiv_symm_apply
#print axioms cochain3BasisEquiv_symm_apply
#print axioms cochain2WordEquiv
#print axioms cochain3WordEquiv
#print axioms cochain2WordEquiv_symm_apply
#print axioms cochain3WordEquiv_symm_apply

end
end ARCCochainWordEquiv
