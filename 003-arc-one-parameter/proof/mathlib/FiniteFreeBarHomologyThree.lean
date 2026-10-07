import FiniteFreeBarComposition34
import FiniteFreeBarNonboundary
import LowDegreeCohomology

/-!
The actual Hom(P2,S) -> Hom(P3,S) -> Hom(P4,S) maps come from the
actual A-linear boundaries. Their composite is zero by the full
A-coefficient chain law. The fixed f-character module map defines a
nonzero class in this actual Hom cycles-modulo-boundaries quotient
when q^3 is nonzero. No exact resolution or Ext comparison is asserted.
-/

namespace ARCFiniteFreeBarHomologyThree

open ARCTwentyDimAlgebra ARCFiniteFreeBarModules ARCCharacterModule
open ARCFiniteFreeBarDegreeThree ARCFiniteFreeBarDegreeFour
open ARCFiniteFreeBarComposition34 ARCFiniteFreeBarNonboundary
open ARCFiniteFreeBarCochains ARCTwentyDimCharacters

variable {R : Type*} [CommRing R] [CharP R 2]

noncomputable section

variable (q : R) (eps : TableAlgebra q →ₐ[R] R)

local instance characterSmulCommReverse :
    SMulCommClass (TableAlgebra q) R (CharacterModule eps) :=
  SMulCommClass.symm R (TableAlgebra q) (CharacterModule eps)

/-- All genuine A-linear maps from the degree-n free term. -/
abbrev HomTerm (n : Nat) := BarTerm q n →ₗ[TableAlgebra q] CharacterModule eps

/-- Precomposition with the actual third boundary, R-linearly packaged. -/
def delta2 : HomTerm q eps 2 →ₗ[R] HomTerm q eps 3 where
  toFun phi := phi.comp (boundary3 q eps)
  map_add' phi psi := by
    apply LinearMap.ext
    intro v
    rfl
  map_smul' r phi := by
    apply LinearMap.ext
    intro v
    rfl

/-- Precomposition with the actual fourth boundary, R-linearly packaged. -/
def delta3 : HomTerm q eps 3 →ₗ[R] HomTerm q eps 4 where
  toFun phi := phi.comp (boundary4 q eps)
  map_add' phi psi := by
    apply LinearMap.ext
    intro v
    rfl
  map_smul' r phi := by
    apply LinearMap.ext
    intro v
    rfl

/-- The Hom differentials compose to zero, using the actual full chain law. -/
theorem delta3_comp_delta2 : (delta3 q eps).comp (delta2 q eps) = 0 := by
  apply LinearMap.ext
  intro phi
  apply LinearMap.ext
  intro v
  change phi (boundary3 q eps (boundary4 q eps v)) = 0
  have h : boundary3 q eps (boundary4 q eps v) = 0 :=
    LinearMap.congr_fun (boundary3_comp_boundary4 q eps) v
  rw [h, map_zero]

/-- The actual Hom complex quotient at degree three. -/
abbrev H3 := ARCLowDegreeCohomology.Cohomology
  (delta2 q eps) (delta3 q eps) (delta3_comp_delta2 q eps)

/-- A class of an actual closed A-linear map. -/
def classOf (phi : HomTerm q eps 3) (hphi : delta3 q eps phi = 0) : H3 q eps :=
  ARCLowDegreeCohomology.classOf (delta2 q eps) (delta3 q eps)
    (delta3_comp_delta2 q eps) phi hphi

/-- Vanishing excludes no possible degree-two A-linear map from consideration. -/
theorem classOf_eq_zero_iff (phi : HomTerm q eps 3) (hphi : delta3 q eps phi = 0) :
    classOf q eps phi hphi = 0 ↔
      ∃ psi : HomTerm q eps 2, psi.comp (boundary3 q eps) = phi :=
  ARCLowDegreeCohomology.classOf_eq_zero_iff (delta2 q eps) (delta3 q eps)
    (delta3_comp_delta2 q eps) phi hphi

/-- The fixed actual f-character module map is a Hom cocycle. -/
theorem fCochainHom_cycle : delta3 q (fCharacter q) (fCochainHom q) = 0 :=
  fCochainHom_closed q

/-- Its class in the actual Hom quotient. -/
def fHomClass : H3 q (fCharacter q) :=
  classOf q (fCharacter q) (fCochainHom q) (fCochainHom_cycle q)

/-- The actual module-Hom class is nonzero under the precise coefficient condition. -/
theorem fHomClass_ne_zero (hq : q ^ 3 ≠ 0) : fHomClass q ≠ 0 := by
  intro h
  exact fCochainHom_not_boundary q hq
    ((classOf_eq_zero_iff q (fCharacter q) (fCochainHom q)
      (fCochainHom_cycle q)).mp h)

theorem fHomClass_ne_zero_of_nonzero [NoZeroDivisors R] (hq : q ≠ 0) :
    fHomClass q ≠ 0 := fHomClass_ne_zero q (pow_ne_zero 3 hq)

#print axioms delta2
#print axioms delta3
#print axioms delta3_comp_delta2
#print axioms classOf_eq_zero_iff
#print axioms fCochainHom_cycle
#print axioms fHomClass
#print axioms fHomClass_ne_zero
#print axioms fHomClass_ne_zero_of_nonzero

end
end ARCFiniteFreeBarHomologyThree
