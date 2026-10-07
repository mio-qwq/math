import FiniteCoreT
import TermSemantics

/-!
# Actual polynomial-vector associativity on the table's basis labels

The frozen ten-label and twenty-label certificates are transported to
`Nat → Polynomial (ZMod 2)`. Both independent composed-coefficient bounds
are used. This introduces no new enumeration and no full algebra instance.
-/

namespace ARCTableBasisSemantics

open ARCFiniteCore ARCBytePacking ARCTermSemantics

noncomputable section

/-- A general transport lemma: packed equality plus bounds gives true vector equality. -/
theorem basis_associativity_of_packed
    (table : Nat → Nat → Terms) (a b c : Nat)
    (hl : ∀ x ∈ table a b, ∀ y ∈ table x.1 c, pMul x.2 y.2 < 256)
    (hr : ∀ x ∈ table b c, ∀ y ∈ table a x.1, pMul x.2 y.2 < 256)
    (heq : leftProduct table a b c = rightProduct table a b c) :
    leftVectorProduct table a b c = rightVectorProduct table a b c := by
  rw [← decode_leftProduct table a b c hl,
    ← decode_rightProduct table a b c hr, heq]

/-- The ten-label table is associative on all basis triples in true polynomial vectors. -/
theorem c_basis_polynomial_associativity (a b c : Fin 10) :
    leftVectorProduct cTerms a.val b.val c.val =
      rightVectorProduct cTerms a.val b.val c.val := by
  apply basis_associativity_of_packed cTerms a.val b.val c.val
  · simpa only [List.all_eq_true, decide_eq_true_eq] using
      c_composed_coefficient_bound a b c
  · simpa only [List.all_eq_true, decide_eq_true_eq] using
      c_right_composed_coefficient_bound a b c
  · exact c_basis_associativity a b c

/-- All twenty-label basis triples now have genuine F₂[X]-vector associativity. -/
theorem t_basis_polynomial_associativity (a b c : Fin 20) :
    leftVectorProduct tTerms a.val b.val c.val =
      rightVectorProduct tTerms a.val b.val c.val := by
  apply basis_associativity_of_packed tTerms a.val b.val c.val
  · simpa only [List.all_eq_true, decide_eq_true_eq] using
      t_left_composed_coefficient_bound a b c
  · simpa only [List.all_eq_true, decide_eq_true_eq] using
      t_right_composed_coefficient_bound a b c
  · exact t_basis_associativity a b c

#print axioms basis_associativity_of_packed
#print axioms c_basis_polynomial_associativity
#print axioms t_basis_polynomial_associativity

end
end ARCTableBasisSemantics
