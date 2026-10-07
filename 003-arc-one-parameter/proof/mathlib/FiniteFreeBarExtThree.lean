import FiniteFreeBarProjectiveResolution
import FiniteFreeBarRecursiveLowDegrees
import FiniteFreeBarNonboundary
import Mathlib.Algebra.Category.ModuleCat.Ext.HasExt
import Mathlib.CategoryTheory.Abelian.Projective.Ext

/-!
The fixed full f-character module cochain defines an actual Mathlib Ext^3
class, using the specified all-degree finite free projective resolution.
The low-degree comparison identifies its adjacent maps with the previously
proved actual boundaries. The Ext zero criterion quantifies over every
actual A-linear degree-two map; the full nonboundary theorem excludes them
all whenever q^3 is nonzero.

This file proves actual Ext^3 nonvanishing. It does not assert the other
degree vanishing, coefficient-module vanishing, or complete ARC realization.
-/

namespace ARCFiniteFreeBarExtThree

open CategoryTheory CategoryTheory.Category
open ARCTwentyDimAlgebra ARCTwentyDimCharacters ARCCharacterModule
open ARCFiniteFreeBarModules ARCFiniteFreeBarCochains
open ARCFiniteFreeBarDegreeThree ARCFiniteFreeBarDegreeFour
open ARCFiniteFreeBarRecursiveLowDegrees ARCFiniteFreeBarProjectiveResolution
open ARCFiniteFreeBarNonboundary

universe u
variable {R : Type u} [CommRing R] [CharP R 2]

noncomputable section

variable (q : R)

/-- The actual module-Hom cocycle on the specified resolution term. -/
def fCocycle : (projectiveResolution q (fCharacter q)).complex.X 3 ⟶
    characterObject q (fCharacter q) :=
  ModuleCat.ofHom (fCochainHom q)

/-- Its categorical cocycle condition uses equality of the full actual
recursive and installed degree-four maps. -/
theorem fCocycle_closed :
    (projectiveResolution q (fCharacter q)).complex.d 4 3 ≫ fCocycle q = 0 := by
  rw [projectiveResolution_d q (fCharacter q) 3, recursiveBoundary_three]
  exact ModuleCat.hom_ext (fCochainHom_closed q)

/-- The fixed cocycle, interpreted in actual Mathlib Ext of the actual
left character module with itself. -/
def fExtThree : CategoryTheory.Abelian.Ext
    (characterObject q (fCharacter q)) (characterObject q (fCharacter q)) 3 :=
  (projectiveResolution q (fCharacter q)).extMk (fCocycle q) 4 rfl (fCocycle_closed q)

/-- The actual Ext zero criterion is precisely the existence of an arbitrary
degree-two A-linear precomposition boundary for the installed map. -/
theorem fExtThree_eq_zero_iff : fExtThree q = 0 ↔
    ∃ phi : BarTerm q 2 →ₗ[TableAlgebra q] CharacterModule (fCharacter q),
      phi.comp (boundary3 q (fCharacter q)) = fCochainHom q := by
  rw [fExtThree, (projectiveResolution q (fCharacter q)).extMk_eq_zero_iff
    (fCocycle q) 4 rfl (fCocycle_closed q) 2 rfl]
  constructor
  · rintro ⟨g, hg⟩
    refine ⟨g.hom, ?_⟩
    rw [projectiveResolution_d q (fCharacter q) 2, recursiveBoundary_two] at hg
    exact congrArg (fun h => h.hom) hg
  · rintro ⟨phi, hphi⟩
    refine ⟨ModuleCat.ofHom phi, ?_⟩
    rw [projectiveResolution_d q (fCharacter q) 2, recursiveBoundary_two]
    exact ModuleCat.hom_ext hphi

/-- Nonzero q^3 gives a nonzero element of actual Ext^3. -/
theorem fExtThree_ne_zero (hq : q ^ 3 ≠ 0) : fExtThree q ≠ 0 := by
  intro h
  exact fCochainHom_not_boundary q hq ((fExtThree_eq_zero_iff q).mp h)

/-- In a ring without zero divisors, the simpler q != 0 hypothesis suffices. -/
theorem fExtThree_ne_zero_of_nonzero [NoZeroDivisors R] (hq : q ≠ 0) :
    fExtThree q ≠ 0 :=
  fExtThree_ne_zero q (pow_ne_zero 3 hq)

/-- Explicit actual Ext^3 nonvanishing, without choosing a different resolution. -/
theorem exists_nonzero_ext_three (hq : q ^ 3 ≠ 0) :
    ∃ xi : CategoryTheory.Abelian.Ext
      (characterObject q (fCharacter q)) (characterObject q (fCharacter q)) 3,
      xi ≠ 0 :=
  ⟨fExtThree q, fExtThree_ne_zero q hq⟩

#print axioms fCocycle
#print axioms fCocycle_closed
#print axioms fExtThree
#print axioms fExtThree_eq_zero_iff
#print axioms fExtThree_ne_zero
#print axioms fExtThree_ne_zero_of_nonzero
#print axioms exists_nonzero_ext_three

end
end ARCFiniteFreeBarExtThree
