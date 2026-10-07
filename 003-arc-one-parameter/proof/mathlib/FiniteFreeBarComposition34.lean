import FiniteFreeBarTripleLift
import FiniteFreeBarDegreeFour

/-!
The actual third and fourth finite free boundaries compose to zero.
Full trilinear lifts turn each interior table contraction into genuine
algebra multiplication. The twenty terms cancel in ten pairs in the
entire A-valued second free module. No character projection or basis-word
enumeration is used, and A is not assumed commutative.

Only this adjacent-boundary composition is proved. Exactness, an
all-degree resolution and a comparison with Ext remain separate tasks.
-/

namespace ARCFiniteFreeBarComposition34

open ARCTwentyDimAlgebra ARCTwentyDimCochainAlgebra ARCTwentyDimAssociativity
open ARCFiniteFreeBarModules ARCFiniteFreeBarDegreeThree ARCFiniteFreeBarDegreeFour
open ARCFiniteFreeBarPairLift ARCFiniteFreeBarTripleLift ARCCochainWordEquiv
open scoped BigOperators

variable {R : Type*} [CommRing R] [CharP R 2]

noncomputable section

variable (q : R) (eps : TableAlgebra q →ₐ[R] R)

private theorem tripleLift_first_expansion (x y z : TableAlgebra q) :
    tripleLift q x y z =
      ∑ a : Fin 20, x.coords a • tripleLift q (coordinateBasis q a) y z := by
  conv_lhs => rw [basis_expansion q x]
  simp only [map_sum, map_smul, LinearMap.sum_apply, LinearMap.smul_apply]

private theorem tripleLift_second_expansion (x y z : TableAlgebra q) :
    tripleLift q x y z =
      ∑ b : Fin 20, y.coords b • tripleLift q x (coordinateBasis q b) z := by
  conv_lhs => rw [basis_expansion q y]
  simp only [map_sum, map_smul, LinearMap.sum_apply, LinearMap.smul_apply]

private theorem tripleLift_third_expansion (x y z : TableAlgebra q) :
    tripleLift q x y z =
      ∑ c : Fin 20, z.coords c • tripleLift q x y (coordinateBasis q c) := by
  conv_lhs => rw [basis_expansion q z]
  simp only [map_sum, map_smul]

private theorem tripleLift_product_first_basis (a b c d : Fin 20) :
    tripleLift q (coordinateBasis q a * coordinateBasis q b)
      (coordinateBasis q c) (coordinateBasis q d) =
      ∑ j : Fin 20, specializedConstants q a b j • wordBasis q 3 (word3 j c d) := by
  rw [tripleLift_first_expansion, coordinateBasis_mul_coords]
  simp only [tripleLift_basis]

private theorem tripleLift_product_second_basis (a b c d : Fin 20) :
    tripleLift q (coordinateBasis q a) (coordinateBasis q b * coordinateBasis q c)
      (coordinateBasis q d) =
      ∑ j : Fin 20, specializedConstants q b c j • wordBasis q 3 (word3 a j d) := by
  rw [tripleLift_second_expansion, coordinateBasis_mul_coords]
  simp only [tripleLift_basis]

private theorem tripleLift_product_third_basis (a b c d : Fin 20) :
    tripleLift q (coordinateBasis q a) (coordinateBasis q b)
      (coordinateBasis q c * coordinateBasis q d) =
      ∑ j : Fin 20, specializedConstants q c d j • wordBasis q 3 (word3 a b j) := by
  rw [tripleLift_third_expansion, coordinateBasis_mul_coords]
  simp only [tripleLift_basis]

/-- Five actual lift faces, retaining the genuine left A-action. -/
def fiveTripleFaces (x y z w : TableAlgebra q) : BarTerm q 3 :=
  x • tripleLift q y z w + tripleLift q (x * y) z w +
    tripleLift q x (y * z) w + tripleLift q x y (z * w) + eps w • tripleLift q x y z

/-- The actual fourth boundary on every ordered basis word has full-lift semantics. -/
theorem boundary4_tripleLift_basis (a b c d : Fin 20) :
    boundary4 q eps (wordBasis q 4 (word4 a b c d)) =
      fiveTripleFaces q eps (coordinateBasis q a) (coordinateBasis q b)
        (coordinateBasis q c) (coordinateBasis q d) := by
  rw [boundary4_word4]
  simp only [fiveTripleFaces, tripleLift_product_first_basis,
    tripleLift_product_second_basis, tripleLift_product_third_basis, tripleLift_basis]

/-- Twenty full-coefficient terms cancel in ten pairs for arbitrary actual
algebra inputs. Character values occur only in the prescribed last face. -/
theorem boundary3_fiveTripleFaces_zero (x y z w : TableAlgebra q) :
    boundary3 q eps (fiveTripleFaces q eps x y z w) = 0 := by
  simp only [fiveTripleFaces, map_add, (boundary3 q eps).map_smul,
    (boundary3 q eps).map_smul_of_tower, boundary3_tripleLift,
    smul_add, smul_smul, map_mul, mul_assoc]
  rw [smul_algebra_smul_comm (eps w) x (pairLift q y z), mul_comm (eps w) (eps z)]
  abel_nf
  simp only [barTerm_two_zsmul, zero_add]

/-- Adjacent actual A-linear boundaries compose to zero on the whole P4.
No selected-word or character-value restriction remains. -/
theorem boundary3_comp_boundary4 :
    (boundary3 q eps).comp (boundary4 q eps) = 0 := by
  apply (wordBasis q 4).ext
  intro w
  have h := boundary4_tripleLift_basis q eps (w 0) (w 1) (w 2) (w 3)
  rw [word4_eta] at h
  change boundary3 q eps (boundary4 q eps (wordBasis q 4 w)) = 0
  rw [h]
  exact boundary3_fiveTripleFaces_zero q eps (coordinateBasis q (w 0))
    (coordinateBasis q (w 1)) (coordinateBasis q (w 2)) (coordinateBasis q (w 3))

#print axioms tripleLift_product_first_basis
#print axioms tripleLift_product_second_basis
#print axioms tripleLift_product_third_basis
#print axioms boundary4_tripleLift_basis
#print axioms boundary3_fiveTripleFaces_zero
#print axioms boundary3_comp_boundary4

end
end ARCFiniteFreeBarComposition34
