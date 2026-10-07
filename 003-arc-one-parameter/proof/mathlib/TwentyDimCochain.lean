import CochainSpecialization
import FiniteTrilinear
import FiniteHochschild

/-!
# The actual specialized cochain on arbitrary radical-span vectors

Generic basis-contraction lemmas connect the specified polynomial cochain
and multiplication constants to actual vector evaluation. The final scope
is a five-face vector identity on the span of the eighteen chosen radical
labels, after every characteristic-two commutative-ring specialization.

No relative Hochschild complex, balancing theorem, bar resolution, or Ext
class is constructed here.
-/

namespace ARCTwentyDimCochain

open ARCFiniteTrilinear ARCCochainBasisSemantics
open ARCCochainSpecialization ARCTwentyDimAssociativity
open scoped BigOperators

noncomputable section

section GenericContractions

variable {R I : Type*} [CommSemiring R] [Fintype I] [DecidableEq I]

/-- Multiplication with a basis vector in the first slot is one contraction. -/
theorem mul_basis_left (B : I → I → I → R) (a : I) (v : I → R) (k : I) :
    ARCFiniteBilinear.mul B (basis a) v k = ∑ j, v j * B a j k := by
  simp [ARCFiniteBilinear.mul, basis, ite_mul]

/-- Multiplication with a basis vector in the second slot is one contraction. -/
theorem mul_basis_right (B : I → I → I → R) (u : I → R) (b k : I) :
    ARCFiniteBilinear.mul B u (basis b) k = ∑ j, u j * B j b k := by
  simp [ARCFiniteBilinear.mul, basis, ite_mul, mul_ite]

/-- Two input basis vectors recover the algebra structure constants. -/
theorem mul_basis_basis (B : I → I → I → R) (a b : I) :
    ARCFiniteBilinear.mul B (basis a) (basis b) = B a b := by
  funext k
  simp [ARCFiniteBilinear.mul, basis, ite_mul, mul_ite]

/-- A first-slot vector and two basis vectors give one cochain contraction. -/
theorem eval_first_contraction (P : I → I → I → I → R)
    (u : I → R) (b c k : I) :
    eval P u (basis b) (basis c) k = ∑ j, u j * P j b c k := by
  simp [eval, basis, ite_mul, mul_ite]

/-- A second-slot vector and two basis vectors give one cochain contraction. -/
theorem eval_second_contraction (P : I → I → I → I → R)
    (a : I) (v : I → R) (c k : I) :
    eval P (basis a) v (basis c) k = ∑ j, v j * P a j c k := by
  simp [eval, basis, ite_mul, mul_ite]

/-- A third-slot vector and two basis vectors give one cochain contraction. -/
theorem eval_third_contraction (P : I → I → I → I → R)
    (a b : I) (w : I → R) (k : I) :
    eval P (basis a) (basis b) w k = ∑ j, w j * P a b j k := by
  simp [eval, basis, ite_mul, mul_ite]

/-- On four basis inputs, the actual vector formula is its five finite
structure-constant contractions. This is independent of any table. -/
theorem differential3_basis_coefficient
    (B : I → I → I → R) (P : I → I → I → I → R) (a b c d k : I) :
    ARCFiniteHochschild.differential3 B P
      (basis a) (basis b) (basis c) (basis d) k =
    (∑ j, P b c d j * B a j k) +
      ((∑ j, B a b j * P j c d k) +
        ((∑ j, B b c j * P a j d k) +
          ((∑ j, B c d j * P a b j k) + (∑ j, P a b c j * B j d k)))) := by
  unfold ARCFiniteHochschild.differential3
  rw [eval_basis P b c d, eval_basis P a b c,
    mul_basis_basis B a b, mul_basis_basis B b c, mul_basis_basis B c d]
  simp only [Pi.add_apply]
  rw [mul_basis_left, eval_first_contraction, eval_second_contraction,
    eval_third_contraction, mul_basis_right]
  ac_rfl

end GenericContractions

variable {R : Type*} [CommRing R] [CharP R 2]

/-- Actual three-vector evaluation of the cochain after specialization. -/
def specializedCochain (q : R) (u v w : Fin 20 → R) : Fin 20 → R :=
  eval (specializedCochainConstants q) u v w

/-- The evaluated cochain recovers exactly the attributed table constants. -/
theorem specializedCochain_basis (q : R) (a b c : Fin 20) :
    specializedCochain q (basis a) (basis b) (basis c) =
      specializedCochainConstants q a b c :=
  eval_basis (specializedCochainConstants q) a b c

/-- The actual specialized five-face expression on four arbitrary vectors. -/
def specializedDifferential3 (q : R) (u v w z : Fin 20 → R) : Fin 20 → R :=
  ARCFiniteHochschild.differential3
    (specializedConstants q) (specializedCochainConstants q) u v w z

/-- Its basis coefficient is exactly the already established specialized
five-term expression; multiplication and cochain constants are reused. -/
theorem specialized_differential_basis_coefficient
    (q : R) (a b c d k : Fin 20) :
    specializedDifferential3 q (basis a) (basis b) (basis c) (basis d) k =
      specializedFiveTermCoefficient q a b c d k :=
  differential3_basis_coefficient
    (specializedConstants q) (specializedCochainConstants q) a b c d k

/-- The actual vector expression vanishes on every radical-basis quadruple. -/
theorem specialized_differential_radical_basis_zero
    (q : R) (a b c d : Fin 18) :
    specializedDifferential3 q (basis (radicalBasis a)) (basis (radicalBasis b))
      (basis (radicalBasis c)) (basis (radicalBasis d)) = 0 := by
  funext k
  rw [specialized_differential_basis_coefficient]
  exact specialized_radical_basis_five_term_zero q a b c d k

/-- An arbitrary finite linear combination of the eighteen chosen labels. -/
def radicalSum (U : Fin 18 → R) : Fin 20 → R :=
  ARCFiniteHochschild.span radicalBasis U

/-- Every characteristic-two specialization has the five-face vector identity
on arbitrary vectors of the indicated radical-label span. No nilpotence,
product-closure, or relative-complex assumption is used for this raw identity. -/
theorem specialized_radical_span_closure
    (q : R) (U V W Z : Fin 18 → R) :
    specializedDifferential3 q (radicalSum U) (radicalSum V)
      (radicalSum W) (radicalSum Z) = 0 :=
  ARCFiniteHochschild.basis_span_closure
    (specializedConstants q) (specializedCochainConstants q) radicalBasis
    (specialized_differential_radical_basis_zero q) U V W Z

/-- The same conclusion with all actual multiplication and cochain faces
visible. Each input is an arbitrary vector in the chosen radical-label span. -/
theorem specialized_radical_five_faces_zero
    (q : R) (U V W Z : Fin 18 → R) :
    specializedMul q (radicalSum U)
        (specializedCochain q (radicalSum V) (radicalSum W) (radicalSum Z)) +
      specializedCochain q (specializedMul q (radicalSum U) (radicalSum V))
        (radicalSum W) (radicalSum Z) +
      specializedCochain q (radicalSum U)
        (specializedMul q (radicalSum V) (radicalSum W)) (radicalSum Z) +
      specializedCochain q (radicalSum U) (radicalSum V)
        (specializedMul q (radicalSum W) (radicalSum Z)) +
      specializedMul q
        (specializedCochain q (radicalSum U) (radicalSum V) (radicalSum W))
        (radicalSum Z) = 0 :=
  specialized_radical_span_closure q U V W Z

#print axioms mul_basis_left
#print axioms mul_basis_right
#print axioms mul_basis_basis
#print axioms eval_first_contraction
#print axioms eval_second_contraction
#print axioms eval_third_contraction
#print axioms differential3_basis_coefficient
#print axioms specializedCochain_basis
#print axioms specialized_differential_basis_coefficient
#print axioms specialized_differential_radical_basis_zero
#print axioms specialized_radical_span_closure
#print axioms specialized_radical_five_faces_zero

end
end ARCTwentyDimCochain
