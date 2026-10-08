import TwentyDimNilpotence
import NilIdealJacobson
import Mathlib.RingTheory.Jacobson.Semiprimary

/-!
# The whole actual table radical through the two-coordinate augmentation

The published sixth-power vanishing proves that the complete augmentation
kernel is a nil ideal, hence lies in the actual ring Jacobson radical.
The whole radical is the augmentation preimage of the coefficient-product
radical. For semisimple coefficient rings, including fields, it is exactly
the eighteen-coordinate augmentation kernel, at every parameter.
The published grading and finite certificates are reused unchanged.
-/

namespace ARCTwentyDimAugmentationJacobson

open ARCTwentyDimAlgebra ARCTwentyDimAugmentation ARCTwentyDimNilpotence

noncomputable section

variable {R : Type*} [CommRing R] [CharP R 2]

def augmentationIdeal (q : R) : Ideal (TableAlgebra q) :=
  RingHom.ker (augmentation q)

instance augmentationIdeal_twoSided (q : R) : (augmentationIdeal q).IsTwoSided :=
  inferInstanceAs (RingHom.ker (augmentation q)).IsTwoSided

theorem mem_augmentationIdeal (q : R) (x : TableAlgebra q) :
    x ∈ augmentationIdeal q ↔ x.coords 0 = 0 ∧ x.coords 8 = 0 :=
  augmentation_kernel_iff q x

theorem augmentationIdeal_element_nilpotent (q : R) (x : TableAlgebra q)
    (hx : x ∈ augmentationIdeal q) : IsNilpotent x :=
  ⟨6, augmentation_kernel_pow_six_zero q x hx⟩

theorem augmentationIdeal_le_jacobson (q : R) :
    augmentationIdeal q ≤ Ring.jacobson (TableAlgebra q) :=
  ARCNilIdealJacobson.nilIdeal_le_jacobson (augmentationIdeal q)
    (augmentationIdeal_element_nilpotent q)

theorem jacobson_eq_augmentation_comap (q : R) :
    Ring.jacobson (TableAlgebra q) =
      Ideal.comap (augmentation q) (Ring.jacobson (R × R)) :=
  ARCNilIdealJacobson.radical_comap_of_nil_ker (augmentation q)
    (augmentation_surjective q) (augmentationIdeal_element_nilpotent q)

theorem jacobson_eq_augmentationIdeal [IsSemisimpleRing R] (q : R) :
    Ring.jacobson (TableAlgebra q) = augmentationIdeal q :=
  ARCNilIdealJacobson.radical_eq_ker_of_nil_ker (augmentation q)
    (augmentation_surjective q) (augmentationIdeal_element_nilpotent q)
    (IsSemisimpleRing.jacobson_eq_bot (R × R))

theorem mem_jacobson_iff [IsSemisimpleRing R] (q : R) (x : TableAlgebra q) :
    x ∈ Ring.jacobson (TableAlgebra q) ↔ x.coords 0 = 0 ∧ x.coords 8 = 0 := by
  rw [jacobson_eq_augmentationIdeal, mem_augmentationIdeal]

theorem mem_jacobson_iff_radicalSum [IsSemisimpleRing R] (q : R) (x : TableAlgebra q) :
    x ∈ Ring.jacobson (TableAlgebra q) ↔
      ∃ U : Fin 18 → R, ARCTwentyDimCochain.radicalSum U = x.coords := by
  rw [jacobson_eq_augmentationIdeal]
  exact augmentation_kernel_iff_radicalSum q x

theorem jacobson_word_zero [IsSemisimpleRing R] (q : R) (xs : List (TableAlgebra q))
    (hx : ∀ x ∈ xs, x ∈ Ring.jacobson (TableAlgebra q)) (hlen : 6 ≤ xs.length) :
    xs.prod = 0 := by
  apply augmentation_kernel_word_zero q xs _ hlen
  intro x hxs
  change x ∈ augmentationIdeal q
  rw [← jacobson_eq_augmentationIdeal q]
  exact hx x hxs

#print axioms mem_augmentationIdeal
#print axioms augmentationIdeal_element_nilpotent
#print axioms augmentationIdeal_le_jacobson
#print axioms jacobson_eq_augmentation_comap
#print axioms jacobson_eq_augmentationIdeal
#print axioms mem_jacobson_iff
#print axioms mem_jacobson_iff_radicalSum
#print axioms jacobson_word_zero

end
end ARCTwentyDimAugmentationJacobson
