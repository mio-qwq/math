import FiniteFreeBarInsertion

/-!
A recursive family of genuine A-linear maps on the finite free terms.
The first map is the installed character boundary. Each successor is
extended from the entire A-basis, using the preceding boundary and the
R-linear coefficient insertion. The index convention is D(n):P(n+1)->Pn,
so every recursive reference has a strictly smaller natural-number index.

These definitions and basis formulas alone assert no chain law, contraction
identity, exactness, projective resolution, standard bar identification or
Ext comparison. Such properties require separate proofs. A remains the
actual noncommutative table algebra, and insertion is only R-linear.
-/

namespace ARCFiniteFreeBarRecursive

open ARCTwentyDimAlgebra ARCFiniteFreeBarModules ARCFiniteFreeBarAugmentation
open ARCFiniteFreeBarInsertion
open scoped BigOperators

variable {R : Type*} [CommRing R] [CharP R 2]

noncomputable section

variable (q : R)

/-- Construct the next genuine left A-linear map from an arbitrary preceding
one. The outer scalar for Basis.constr is R, without commutativity of A. -/
def nextBoundary (n : Nat)
    (d : BarTerm q (n + 1) →ₗ[TableAlgebra q] BarTerm q n) :
    BarTerm q (n + 2) →ₗ[TableAlgebra q] BarTerm q (n + 1) :=
  (wordBasis q (n + 2)).constr R (fun w =>
    coordinateBasis q (w 0) • wordBasis q (n + 1) (Fin.tail w) +
      coefficientInsertion q n
        (d (coordinateBasis q (w 0) • wordBasis q (n + 1) (Fin.tail w))))

/-- The successor definition on every word, retaining the full left coefficient. -/
theorem nextBoundary_basis (n : Nat)
    (d : BarTerm q (n + 1) →ₗ[TableAlgebra q] BarTerm q n) (w : Word (n + 2)) :
    nextBoundary q n d (wordBasis q (n + 2) w) =
      coordinateBasis q (w 0) • wordBasis q (n + 1) (Fin.tail w) +
        coefficientInsertion q n
          (d (coordinateBasis q (w 0) • wordBasis q (n + 1) (Fin.tail w))) := by
  exact (wordBasis q (n + 2)).constr_basis R _ w

/-- The same basis formula with its first letter and tail explicit. -/
theorem nextBoundary_cons_basis (n : Nat)
    (d : BarTerm q (n + 1) →ₗ[TableAlgebra q] BarTerm q n)
    (i : Fin 20) (w : Word (n + 1)) :
    nextBoundary q n d (wordBasis q (n + 2) (Fin.cons i w)) =
      coordinateBasis q i • wordBasis q (n + 1) w +
        coefficientInsertion q n (d (coordinateBasis q i • wordBasis q (n + 1) w)) := by
  simpa only [Fin.cons_zero, Fin.tail_cons] using
    nextBoundary_basis q n d (Fin.cons i w)

/-- The A-linear extension evaluates every vector through all its actual
A-valued word coefficients, rather than through their character values. -/
theorem nextBoundary_apply (n : Nat)
    (d : BarTerm q (n + 1) →ₗ[TableAlgebra q] BarTerm q n)
    (v : BarTerm q (n + 2)) :
    nextBoundary q n d v = ∑ w : Word (n + 2), v w •
      (coordinateBasis q (w 0) • wordBasis q (n + 1) (Fin.tail w) +
        coefficientInsertion q n
          (d (coordinateBasis q (w 0) • wordBasis q (n + 1) (Fin.tail w)))) := by
  rw [nextBoundary, Module.Basis.constr_apply_fintype]
  simp only [Module.Basis.equivFun_apply, wordBasis_repr]

/-- A structurally recursive family, with D(n) mapping P(n+1) to Pn.
No properties of a chain complex are built into this definition. -/
def recursiveBoundary (eps : TableAlgebra q →ₐ[R] R) :
    (n : Nat) → BarTerm q (n + 1) →ₗ[TableAlgebra q] BarTerm q n
  | 0 => boundary q eps
  | n + 1 => nextBoundary q n (recursiveBoundary eps n)

@[simp] theorem recursiveBoundary_zero (eps : TableAlgebra q →ₐ[R] R) :
    recursiveBoundary q eps 0 = boundary q eps := rfl

theorem recursiveBoundary_succ (eps : TableAlgebra q →ₐ[R] R) (n : Nat) :
    recursiveBoundary q eps (n + 1) = nextBoundary q n (recursiveBoundary q eps n) := rfl

/-- The actual recursive defining equation on every complete basis word. -/
theorem recursiveBoundary_succ_basis (eps : TableAlgebra q →ₐ[R] R) (n : Nat)
    (i : Fin 20) (w : Word (n + 1)) :
    recursiveBoundary q eps (n + 1) (wordBasis q (n + 2) (Fin.cons i w)) =
      coordinateBasis q i • wordBasis q (n + 1) w +
        coefficientInsertion q n
          (recursiveBoundary q eps n (coordinateBasis q i • wordBasis q (n + 1) w)) := by
  rw [recursiveBoundary_succ]
  exact nextBoundary_cons_basis q n (recursiveBoundary q eps n) i w

#print axioms nextBoundary
#print axioms nextBoundary_basis
#print axioms nextBoundary_cons_basis
#print axioms nextBoundary_apply
#print axioms recursiveBoundary
#print axioms recursiveBoundary_zero
#print axioms recursiveBoundary_succ
#print axioms recursiveBoundary_succ_basis

end
end ARCFiniteFreeBarRecursive
