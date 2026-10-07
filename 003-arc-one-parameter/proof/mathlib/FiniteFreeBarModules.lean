import TwentyDimAlgebra
import Mathlib.Algebra.Module.Projective
import Mathlib.Algebra.Category.ModuleCat.Projective
import Mathlib.LinearAlgebra.FreeModule.Finite.Basic
import Mathlib.Data.Fintype.BigOperators

/-!
# Finite free candidate bar terms over the actual noncommutative algebra

In degree n the index set consists of n-letter words in the twenty basis
labels, and the term is the left A-module of A-valued functions on that
finite set. Its standard coordinate basis proves freeness, finite
generation, module-theoretic projectivity and categorical projectivity.

The coefficient action is multiplication in the installed table algebra,
which need not be commutative. These are only candidate terms: this file
defines no differential, augmentation, exact complex, resolution, or Ext
comparison. A basis cardinal is stated without asserting an invariant
module-rank formula for arbitrary coefficient rings.
-/

namespace ARCFiniteFreeBarModules

open ARCTwentyDimAlgebra

/-- n-letter words in the actual twenty-coordinate basis labels. -/
abbrev Word (n : Nat) := Fin n → Fin 20

variable {R : Type*} [CommRing R] [CharP R 2]

/-- The finite function module over the actual table algebra in degree n. -/
abbrev BarTerm (q : R) (n : Nat) := Word n → TableAlgebra q

noncomputable section

/-- The action is actual left table multiplication at every word coordinate. -/
theorem barTerm_smul_apply (q : R) (n : Nat) (a : TableAlgebra q)
    (v : BarTerm q n) (w : Word n) :
    (a • v) w = a * v w := rfl

/-- A completely explicit A-basis indexed by the finite word set. -/
def wordBasis (q : R) (n : Nat) :
    Module.Basis (Word n) (TableAlgebra q) (BarTerm q n) :=
  Pi.basisFun (TableAlgebra q) (Word n)

/-- Each basis vector has coefficient one at its word and zero elsewhere. -/
theorem wordBasis_apply (q : R) (n : Nat) (w w' : Word n) :
    wordBasis q n w w' = if w' = w then 1 else 0 := by
  classical
  simp [wordBasis, Pi.basisFun_apply, Pi.single_apply]

/-- The basis representation is exactly the input's actual A-valued coordinate. -/
theorem wordBasis_repr (q : R) (n : Nat) (v : BarTerm q n) (w : Word n) :
    (wordBasis q n).repr v w = v w :=
  Pi.basisFun_repr (TableAlgebra q) (Word n) v w

/-- Every candidate term is a genuinely free left module over A. -/
instance barTermFree (q : R) (n : Nat) : Module.Free (TableAlgebra q) (BarTerm q n) :=
  Module.Free.of_basis (wordBasis q n)

/-- Every candidate term is finitely generated as a left A-module. -/
instance barTermFinite (q : R) (n : Nat) : Module.Finite (TableAlgebra q) (BarTerm q n) :=
  Module.Finite.of_basis (wordBasis q n)

/-- Module-theoretic projectivity is established by the actual basis. -/
instance barTermProjective (q : R) (n : Nat) :
    Module.Projective (TableAlgebra q) (BarTerm q n) :=
  Module.Projective.of_basis (wordBasis q n)

/-- The same actual term as an object of the category of left A-modules. -/
def barModule (q : R) (n : Nat) : ModuleCat (TableAlgebra q) :=
  ModuleCat.of (TableAlgebra q) (BarTerm q n)

/-- Every such module-category object is projective in the categorical sense. -/
theorem barModule_projective (q : R) (n : Nat) :
    CategoryTheory.Projective (barModule q n) :=
  ModuleCat.projective_of_free (wordBasis q n)

/-- This is the cardinal of the exhibited A-basis in every degree, including
degree zero. It does not require nontriviality of the coefficient ring. -/
theorem word_card (n : Nat) : Fintype.card (Word n) = 20 ^ n := by
  classical
  simp [Word]

#print axioms wordBasis
#print axioms wordBasis_apply
#print axioms wordBasis_repr
#print axioms barTermFree
#print axioms barTermFinite
#print axioms barTermProjective
#print axioms barModule_projective
#print axioms word_card

end
end ARCFiniteFreeBarModules
