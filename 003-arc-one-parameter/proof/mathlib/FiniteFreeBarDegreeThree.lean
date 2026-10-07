import FiniteFreeBarCochains

/-!
# The actual degree-three boundary and its full cochain compatibility

Four faces are prescribed on the actual free A-basis of P3 and extended
A-linearly to P2. Precomposition by this map corresponds exactly, under
the full Hom/cochain equivalences, to the character's full degree-two
differential on every scalar-valued bilinear cochain.

These are actual linear maps and an equality in the whole cochain module,
not tests on finitely many arrays. No degree-two composite, exactness,
all-degree resolution, or comparison with Ext is asserted here.
-/

namespace ARCFiniteFreeBarDegreeThree

open ARCTwentyDimAlgebra ARCTwentyDimCochainAlgebra ARCTwentyDimAssociativity
open ARCFiniteFreeBarModules ARCFiniteFreeBarCochains ARCCochainWordEquiv
open ARCCharacterModule ARCCharacterHochschildMaps
open scoped BigOperators

variable {R : Type*} [CommRing R] [CharP R 2]

noncomputable section

variable (q : R) (eps : TableAlgebra q →ₐ[R] R)

/-- Four actual faces of a basis word. The first coefficient acts by left
A-multiplication; the internal structure coefficients and last character
coefficient use the existing R-action on the actual free module. -/
def boundary3Basis (w : Word 3) : BarTerm q 2 :=
  coordinateBasis q (w 0) • wordBasis q 2 (word2 (w 1) (w 2)) +
    (∑ j : Fin 20, specializedConstants q (w 0) (w 1) j •
      wordBasis q 2 (word2 j (w 2))) +
    (∑ j : Fin 20, specializedConstants q (w 1) (w 2) j •
      wordBasis q 2 (word2 (w 0) j)) +
    eps (coordinateBasis q (w 2)) • wordBasis q 2 (word2 (w 0) (w 1))

/-- The prescribed faces extend to a genuine map of left A-modules. -/
def boundary3 : BarTerm q 3 →ₗ[TableAlgebra q] BarTerm q 2 :=
  (wordBasis q 3).constr R (boundary3Basis q eps)

/-- The actual free-basis action of the extended boundary. -/
theorem boundary3_basis (w : Word 3) :
    boundary3 q eps (wordBasis q 3 w) = boundary3Basis q eps w := by
  exact (wordBasis q 3).constr_basis R (boundary3Basis q eps) w

/-- Explicit four-face formula with the ordered input labels displayed. -/
theorem boundary3_word3 (a b c : Fin 20) :
    boundary3 q eps (wordBasis q 3 (word3 a b c)) =
      coordinateBasis q a • wordBasis q 2 (word2 b c) +
      (∑ j : Fin 20, specializedConstants q a b j • wordBasis q 2 (word2 j c)) +
      (∑ j : Fin 20, specializedConstants q b c j • wordBasis q 2 (word2 a j)) +
      eps (coordinateBasis q c) • wordBasis q 2 (word2 a b) :=
  boundary3_basis q eps (word3 a b c)

private theorem scalar_first_expansion (G : C2S R (TableAlgebra q))
    (x y : TableAlgebra q) :
    G x y = ∑ i : Fin 20, x.coords i • G (coordinateBasis q i) y := by
  conv_lhs => rw [basis_expansion q x]
  simp only [map_sum, map_smul, LinearMap.sum_apply, LinearMap.smul_apply]

private theorem scalar_second_expansion (G : C2S R (TableAlgebra q))
    (x y : TableAlgebra q) :
    G x y = ∑ i : Fin 20, y.coords i • G x (coordinateBasis q i) := by
  conv_lhs => rw [basis_expansion q y]
  simp only [map_sum, map_smul]

private theorem character_value_sum {I : Type*} [Fintype I]
    (v : I → CharacterModule eps) :
    (∑ i, v i).val = ∑ i, (v i).val :=
  map_sum (valueLinearEquiv eps) v Finset.univ

private theorem phi_coefficient_sum {I : Type*} [Fintype I]
    (phi : BarTerm q 2 →ₗ[TableAlgebra q] CharacterModule eps)
    (s : I → R) (v : I → BarTerm q 2) :
    (phi (∑ i, s i • v i)).val = ∑ i, s i * (phi (v i)).val := by
  rw [map_sum, character_value_sum q eps]
  simp only [phi.map_smul_of_tower, val_coefficient_smul]

/-- The precomposed Hom has the same four basis faces as the full character
coboundary of its corresponding actual bilinear cochain. -/
theorem boundary3_cochain_basis
    (phi : BarTerm q 2 →ₗ[TableAlgebra q] CharacterModule eps) (a b c : Fin 20) :
    cochain3HomEquiv q eps (phi.comp (boundary3 q eps))
      (coordinateBasis q a) (coordinateBasis q b) (coordinateBasis q c) =
    d2 eps (cochain2HomEquiv q eps phi)
      (coordinateBasis q a) (coordinateBasis q b) (coordinateBasis q c) := by
  let G := cochain2HomEquiv q eps phi
  have hfirst := scalar_first_expansion q G
    (coordinateBasis q a * coordinateBasis q b) (coordinateBasis q c)
  rw [coordinateBasis_mul_coords] at hfirst
  have hsecond := scalar_second_expansion q G
    (coordinateBasis q a) (coordinateBasis q b * coordinateBasis q c)
  rw [coordinateBasis_mul_coords] at hsecond
  rw [cochain3HomEquiv_basis, LinearMap.comp_apply, boundary3_word3, d2_apply]
  change (phi (_ + _ + _ + _)).val =
    eps (coordinateBasis q a) * G (coordinateBasis q b) (coordinateBasis q c) +
      G (coordinateBasis q a * coordinateBasis q b) (coordinateBasis q c) +
      G (coordinateBasis q a) (coordinateBasis q b * coordinateBasis q c) +
      G (coordinateBasis q a) (coordinateBasis q b) * eps (coordinateBasis q c)
  rw [hfirst, hsecond]
  simp only [map_add, val_add]
  rw [phi_coefficient_sum q eps phi, phi_coefficient_sum q eps phi]
  simp only [phi.map_smul, phi.map_smul_of_tower, val_character_smul,
    val_coefficient_smul, G, cochain2HomEquiv_basis, smul_eq_mul]
  ac_rfl

/-- Compatibility on all actual algebra inputs, as equality of full
scalar-valued trilinear cochains. No restriction to selected inputs remains. -/
theorem boundary3_cochain_compatibility
    (phi : BarTerm q 2 →ₗ[TableAlgebra q] CharacterModule eps) :
    cochain3HomEquiv q eps (phi.comp (boundary3 q eps)) =
      d2 eps (cochain2HomEquiv q eps phi) := by
  apply (cochain3BasisEquiv q).injective
  funext a b c
  exact boundary3_cochain_basis q eps phi a b c

/-- Public precomposition interface for later actual-module-Hom applications. -/
theorem cochain_precomp_boundary3
    (phi : BarTerm q 2 →ₗ[TableAlgebra q] CharacterModule eps) :
    cochain3HomEquiv q eps (phi.comp (boundary3 q eps)) =
      d2 eps (cochain2HomEquiv q eps phi) :=
  boundary3_cochain_compatibility q eps phi

/-- Conversely, every actual scalar bilinear cochain's full coboundary is
exactly the Hom precomposition by the actual degree-three boundary. -/
theorem boundary3_cochain_compatibility_inverse (G : C2S R (TableAlgebra q)) :
    ((cochain2HomEquiv q eps).symm G).comp (boundary3 q eps) =
      (cochain3HomEquiv q eps).symm (d2 eps G) := by
  apply (cochain3HomEquiv q eps).injective
  rw [boundary3_cochain_compatibility,
    (cochain2HomEquiv q eps).apply_symm_apply,
    (cochain3HomEquiv q eps).apply_symm_apply]

#print axioms boundary3
#print axioms boundary3_basis
#print axioms boundary3_word3
#print axioms boundary3_cochain_basis
#print axioms boundary3_cochain_compatibility
#print axioms cochain_precomp_boundary3
#print axioms boundary3_cochain_compatibility_inverse

end
end ARCFiniteFreeBarDegreeThree
