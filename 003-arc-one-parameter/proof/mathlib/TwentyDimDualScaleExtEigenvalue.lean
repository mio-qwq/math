import ExtMkCanonicalFunctor
import FiniteFreeBarDualScaleCocycle
import TwentyDimDualScaleExtTransport

/-!
# The canonical inverse-dual-scaling weight of the fixed actual Ext cubed class

The general exact-functor/extMk naturality theorem identifies the class on
the mapped specified resolution with the canonical functor image. The
whole resolution and cocycle comparison then calculates the canonical
transport on the fixed actual class and every scalar multiple of it.

This computes one class and its generated scalar submodule. No dimension
or whole-Ext scalar action, parameter group-law coherence, all-degree
self-Ext profile, tensor-square realization or complete ARC is asserted.
-/

namespace ARCTwentyDimDualScaleExtEigenvalue

open CategoryTheory CategoryTheory.Abelian
open ARCTwentyDimAlgebra ARCTwentyDimCharacters ARCCharacterModule
open ARCFiniteFreeBarProjectiveResolution ARCFiniteFreeBarExtThree
open ARCTwentyDimDualScaleModule ARCFiniteFreeBarDualScaleComparison
open ARCFiniteFreeBarDualScaleCocycle ARCTwentyDimDualScaleExtTransport
open ARCExtMkCanonicalFunctor
open scoped ModuleCat.Algebra

universe u
variable {R : Type u} [CommRing R] [CharP R 2]

noncomputable section

set_option backward.isDefEq.respectTransparency false in
/-- The represented mapped-resolution class is the actual canonical
exact-functor image, with the specified input resolution retained. -/
theorem twisted_fExtThree_eq_mapExactFunctor (q : R) (H : Rˣ) :
    twisted_fExtThree q H = (fExtThree q).mapExactFunctor (dualScaleFunctor q H) := by
  symm
  simpa only [fExtThree, twisted_fExtThree, twistedResolution] using
    mapExactFunctor_extMk (dualScaleFunctor q H)
      (projectiveResolution q (fCharacter q)) (fCocycle q) 4 rfl (fCocycle_closed q)

/-- The genuine canonical transported action has inverse-unit weight on
the fixed actual f-character Ext cubed class. -/
theorem dualScaleExtTransport_fExtThree (q : R) (H : Rˣ) :
    dualScaleExtTransportMap q H 3 (fExtThree q) = (↑(H⁻¹) : R) • fExtThree q := by
  rw [dualScaleExtTransportMap_apply, ← twisted_fExtThree_eq_mapExactFunctor]
  exact twisted_fExtThree_endpoints q H

/-- The canonical action is explicitly computed on all scalar multiples
of the fixed class, without a whole-Ext dimension assumption. -/
theorem dualScaleExtTransport_fExtThree_smul (q : R) (H : Rˣ) (r : R) :
    dualScaleExtTransportMap q H 3 (r • fExtThree q) =
      (r * (↑(H⁻¹) : R)) • fExtThree q := by
  rw [dualScaleExtTransportMap_smul, dualScaleExtTransport_fExtThree, smul_smul]

/-- The computed canonical image is nonzero whenever q cubed is nonzero. -/
theorem dualScaleExtTransport_fExtThree_ne_zero (q : R) (H : Rˣ) (hq : q ^ 3 ≠ 0) :
    dualScaleExtTransportMap q H 3 (fExtThree q) ≠ 0 :=
  (dualScaleExtTransportMap_ne_zero_iff q H 3 (fExtThree q)).2
    (fExtThree_ne_zero q hq)

#print axioms twisted_fExtThree_eq_mapExactFunctor
#print axioms dualScaleExtTransport_fExtThree
#print axioms dualScaleExtTransport_fExtThree_smul
#print axioms dualScaleExtTransport_fExtThree_ne_zero

end
end ARCTwentyDimDualScaleExtEigenvalue
