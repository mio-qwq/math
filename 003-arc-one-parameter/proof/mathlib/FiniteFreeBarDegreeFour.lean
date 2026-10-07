import FiniteFreeBarCochains

/-!
The actual five-face boundary from the fourth finite free term to the third.
It is extended A-linearly from the entire word basis, with A the installed
noncommutative table algebra. Precomposition by any actual character-module
Hom agrees on basis inputs with the full scalar degree-three differential.
The specified f-character Hom therefore kills this actual boundary.

No adjacent-boundary composition, exactness, all-degree resolution, or
identification with Ext is asserted in this file.
-/

namespace ARCFiniteFreeBarDegreeFour

open ARCTwentyDimAlgebra ARCTwentyDimCochainAlgebra ARCTwentyDimAssociativity
open ARCFiniteFreeBarModules ARCFiniteFreeBarCochains ARCCochainWordEquiv
open ARCCharacterModule ARCCharacterHochschildMaps ARCTwentyDimCharacters
open scoped BigOperators

/-- An ordered four-letter word in the actual coordinate labels. -/
def word4 (a b c d : Fin 20) : Word 4 := Fin.cons a (word3 b c d)

theorem word4_eta (w : Word 4) : word4 (w 0) (w 1) (w 2) (w 3) = w := by
  change Fin.cons (w 0)
    (word3 ((Fin.tail w) 0) ((Fin.tail w) 1) ((Fin.tail w) 2)) = w
  rw [word3_eta, Fin.cons_self_tail]

variable {R : Type*} [CommRing R] [CharP R 2]

noncomputable section

variable (q : R) (eps : TableAlgebra q →ₐ[R] R)

/-- Five actual faces. The first uses genuine left A-multiplication;
the other coefficients use the central R-action on the actual free term. -/
def boundary4Basis (w : Word 4) : BarTerm q 3 :=
  coordinateBasis q (w 0) • wordBasis q 3 (word3 (w 1) (w 2) (w 3)) +
    (∑ j : Fin 20, specializedConstants q (w 0) (w 1) j •
      wordBasis q 3 (word3 j (w 2) (w 3))) +
    (∑ j : Fin 20, specializedConstants q (w 1) (w 2) j •
      wordBasis q 3 (word3 (w 0) j (w 3))) +
    (∑ j : Fin 20, specializedConstants q (w 2) (w 3) j •
      wordBasis q 3 (word3 (w 0) (w 1) j)) +
    eps (coordinateBasis q (w 3)) • wordBasis q 3 (word3 (w 0) (w 1) (w 2))

/-- Extension from all fourth-degree basis words to a genuine left A-linear map. -/
def boundary4 : BarTerm q 4 →ₗ[TableAlgebra q] BarTerm q 3 :=
  (wordBasis q 4).constr R (boundary4Basis q eps)

theorem boundary4_basis (w : Word 4) :
    boundary4 q eps (wordBasis q 4 w) = boundary4Basis q eps w :=
  (wordBasis q 4).constr_basis R (boundary4Basis q eps) w

theorem boundary4_word4 (a b c d : Fin 20) :
    boundary4 q eps (wordBasis q 4 (word4 a b c d)) =
      coordinateBasis q a • wordBasis q 3 (word3 b c d) +
        (∑ j : Fin 20, specializedConstants q a b j • wordBasis q 3 (word3 j c d)) +
        (∑ j : Fin 20, specializedConstants q b c j • wordBasis q 3 (word3 a j d)) +
        (∑ j : Fin 20, specializedConstants q c d j • wordBasis q 3 (word3 a b j)) +
        eps (coordinateBasis q d) • wordBasis q 3 (word3 a b c) :=
  boundary4_basis q eps (word4 a b c d)

private theorem scalar_first_expansion (F : C3S R (TableAlgebra q))
    (x y z : TableAlgebra q) :
    F x y z = ∑ i : Fin 20, x.coords i • F (coordinateBasis q i) y z := by
  conv_lhs => rw [basis_expansion q x]
  simp only [map_sum, map_smul, LinearMap.sum_apply, LinearMap.smul_apply]

private theorem scalar_second_expansion (F : C3S R (TableAlgebra q))
    (x y z : TableAlgebra q) :
    F x y z = ∑ i : Fin 20, y.coords i • F x (coordinateBasis q i) z := by
  conv_lhs => rw [basis_expansion q y]
  simp only [map_sum, map_smul, LinearMap.sum_apply, LinearMap.smul_apply]

private theorem scalar_third_expansion (F : C3S R (TableAlgebra q))
    (x y z : TableAlgebra q) :
    F x y z = ∑ i : Fin 20, z.coords i • F x y (coordinateBasis q i) := by
  conv_lhs => rw [basis_expansion q z]
  simp only [map_sum, map_smul]

private theorem character_value_sum {I : Type*} [Fintype I]
    (v : I → CharacterModule eps) :
    (∑ i, v i).val = ∑ i, (v i).val :=
  map_sum (valueLinearEquiv eps) v Finset.univ

private theorem phi_coefficient_sum {I : Type*} [Fintype I]
    (phi : BarTerm q 3 →ₗ[TableAlgebra q] CharacterModule eps)
    (s : I → R) (v : I → BarTerm q 3) :
    (phi (∑ i, s i • v i)).val = ∑ i, s i * (phi (v i)).val := by
  rw [map_sum, character_value_sum q eps]
  simp only [phi.map_smul_of_tower, val_coefficient_smul]

/-- An arbitrary actual Hom precomposed with the actual boundary gives
all five full character faces of its corresponding trilinear cochain. -/
theorem boundary4_cochain_basis
    (phi : BarTerm q 3 →ₗ[TableAlgebra q] CharacterModule eps) (a b c d : Fin 20) :
    ((phi.comp (boundary4 q eps)) (wordBasis q 4 (word4 a b c d))).val =
      differential3 eps (fun x y z => cochain3HomEquiv q eps phi x y z)
        (coordinateBasis q a) (coordinateBasis q b)
        (coordinateBasis q c) (coordinateBasis q d) := by
  let F := cochain3HomEquiv q eps phi
  have hfirst := scalar_first_expansion q F
    (coordinateBasis q a * coordinateBasis q b) (coordinateBasis q c) (coordinateBasis q d)
  rw [coordinateBasis_mul_coords] at hfirst
  have hsecond := scalar_second_expansion q F
    (coordinateBasis q a) (coordinateBasis q b * coordinateBasis q c) (coordinateBasis q d)
  rw [coordinateBasis_mul_coords] at hsecond
  have hthird := scalar_third_expansion q F
    (coordinateBasis q a) (coordinateBasis q b) (coordinateBasis q c * coordinateBasis q d)
  rw [coordinateBasis_mul_coords] at hthird
  rw [LinearMap.comp_apply, boundary4_word4]
  change (phi (_ + _ + _ + _ + _)).val =
    eps (coordinateBasis q a) * F (coordinateBasis q b) (coordinateBasis q c) (coordinateBasis q d) +
      F (coordinateBasis q a * coordinateBasis q b) (coordinateBasis q c) (coordinateBasis q d) +
      F (coordinateBasis q a) (coordinateBasis q b * coordinateBasis q c) (coordinateBasis q d) +
      F (coordinateBasis q a) (coordinateBasis q b) (coordinateBasis q c * coordinateBasis q d) +
      F (coordinateBasis q a) (coordinateBasis q b) (coordinateBasis q c) * eps (coordinateBasis q d)
  rw [hfirst, hsecond, hthird]
  simp only [map_add, val_add]
  rw [phi_coefficient_sum q eps phi, phi_coefficient_sum q eps phi,
    phi_coefficient_sum q eps phi]
  simp only [phi.map_smul, phi.map_smul_of_tower, val_character_smul,
    val_coefficient_smul, F, cochain3HomEquiv_basis, smul_eq_mul]
  ac_rfl

/-- The published f-cochain Hom is closed for this actual degree-four
boundary on the entire free module, not only on selected radical words. -/
theorem fCochainHom_closed :
    (fCochainHom q).comp (boundary4 q (fCharacter q)) = 0 := by
  apply (wordBasis q 4).ext
  intro w
  apply CharacterModule.ext
  have h := boundary4_cochain_basis q (fCharacter q) (fCochainHom q)
    (w 0) (w 1) (w 2) (w 3)
  rw [word4_eta] at h
  change ((fCochainHom q).comp (boundary4 q (fCharacter q)) (wordBasis q 4 w)).val = 0
  rw [h]
  have hf : cochain3HomEquiv q (fCharacter q) (fCochainHom q) = actualfSimpleP q :=
    (cochain3HomEquiv q (fCharacter q)).apply_symm_apply (actualfSimpleP q)
  rw [hf]
  exact actualfSimpleP_character_closed q (coordinateBasis q (w 0))
    (coordinateBasis q (w 1)) (coordinateBasis q (w 2)) (coordinateBasis q (w 3))

#print axioms word4_eta
#print axioms boundary4
#print axioms boundary4_basis
#print axioms boundary4_word4
#print axioms boundary4_cochain_basis
#print axioms fCochainHom_closed

end
end ARCFiniteFreeBarDegreeFour
