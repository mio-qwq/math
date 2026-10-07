import TwentyDimSelfInjective
import Mathlib.Algebra.Category.ModuleCat.Abelian
import Mathlib.Algebra.Category.ModuleCat.Injective
import Mathlib.Algebra.Category.ModuleCat.Ext.HasExt
import Mathlib.Algebra.Homology.DerivedCategory.Ext.EnoughInjectives

/-!
For every parameter over a characteristic-two field, the actual regular
left module of the twenty-coordinate table algebra is an injective object
of its actual module category. Consequently actual Mathlib Ext into this
regular module vanishes in every positive degree, for every source module.

The injectivity used here is proved for this algebra in
TwentyDimSelfInjective; it is not an additional hypothesis. The target is
the table algebra itself, not a tensor-square algebra or another algebra
in the eventual ARC construction. This file does not establish the
remaining self-Ext profile or the complete ARC realization.
-/

namespace ARCTwentyDimExtIntoAlgebra

open CategoryTheory
open ARCTwentyDimAlgebra ARCTwentyDimSelfInjective

universe u
variable {k : Type u} [Field k] [CharP k 2]

noncomputable section

variable (q : k)

/-- The actual regular left module, with multiplication as its left action. -/
def regularAlgebraObject : ModuleCat.{u} (TableAlgebra q) :=
  ModuleCat.of (TableAlgebra q) (TableAlgebra q)

/-- The proved algebraic injectivity gives actual categorical injectivity. -/
instance regularAlgebraObject_injective : Injective (regularAlgebraObject q) := by
  let : Module.Injective (TableAlgebra q) (TableAlgebra q) := tableAlgebra_injective q
  exact Module.injective_object_of_injective_module (TableAlgebra q) (TableAlgebra q)

/-- Every actual Ext element into the regular algebra in a successor degree is zero. -/
theorem ext_succ_eq_zero (M : ModuleCat.{u} (TableAlgebra q)) (n : Nat)
    (e : Abelian.Ext M (regularAlgebraObject q) (n + 1)) : e = 0 :=
  Abelian.Ext.eq_zero_of_injective e

/-- Ext into the actual regular algebra vanishes in every positive degree,
without any restriction on the source module. -/
theorem ext_positive_eq_zero (M : ModuleCat.{u} (TableAlgebra q)) (n : Nat)
    (hn : 0 < n) (e : Abelian.Ext M (regularAlgebraObject q) n) : e = 0 := by
  cases n with
  | zero => simp at hn
  | succ n => exact ext_succ_eq_zero q M n e

/-- Each positive-degree actual Ext group into the regular algebra has one element. -/
theorem ext_positive_subsingleton (M : ModuleCat.{u} (TableAlgebra q)) (n : Nat)
    (hn : 0 < n) : Subsingleton (Abelian.Ext M (regularAlgebraObject q) n) :=
  subsingleton_of_forall_eq 0 (ext_positive_eq_zero q M n hn)

/-- The successor-degree vanishing as an actual Ext-group statement. -/
theorem ext_succ_subsingleton (M : ModuleCat.{u} (TableAlgebra q)) (n : Nat) :
    Subsingleton (Abelian.Ext M (regularAlgebraObject q) (n + 1)) :=
  Abelian.Ext.subsingleton_of_injective M (regularAlgebraObject q) n

#print axioms regularAlgebraObject
#print axioms regularAlgebraObject_injective
#print axioms ext_succ_eq_zero
#print axioms ext_positive_eq_zero
#print axioms ext_positive_subsingleton
#print axioms ext_succ_subsingleton

end
end ARCTwentyDimExtIntoAlgebra
