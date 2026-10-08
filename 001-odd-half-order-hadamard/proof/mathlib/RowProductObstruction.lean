import Mathlib.Basic.Complex.Basic
import Mathlib.Algebra.Polynomial.Eval.Defs
import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Tactic.NormNum
import Std

/-!
The product refinement of the actual two-polygons root polynomial, and the
resulting obstruction for two complex rows and their conjugate ratio.

The hypotheses are equalities of the actual products of linear factors.
Newton identities, the moment-to-root-polynomial bridge, and the matrix
support argument remain in the analytical proof in general-patterns.md.
-/

open scoped BigOperators ComplexConjugate Polynomial

namespace OddHalfOrder.RowProductObstruction

noncomputable def rowRootPolynomial (m : Nat) (v : Fin (2 * m) → ℂ) : ℂ[X] :=
  ∏ i, (Polynomial.X - Polynomial.C (v i))

/-- Evaluation of the actual root polynomial gives the product of its
`2*m` complex coordinates, since their number is even. -/
theorem rowRootPolynomial_eval_zero (m : Nat) (v : Fin (2 * m) → ℂ) :
    Polynomial.eval 0 (rowRootPolynomial m v) = ∏ i, v i := by
  classical
  have hsign : (-1 : ℂ) ^ (2 * m) = 1 := by
    rw [pow_mul]
    norm_num
  simp only [rowRootPolynomial, Polynomial.eval_prod, Polynomial.eval_sub,
    Polynomial.eval_X, Polynomial.eval_C, zero_sub]
  rw [Finset.prod_neg, Finset.card_univ, Fintype.card_fin, hsign, one_mul]

/-- The two specified polygon factors determine the actual coordinate
product. No row-product or multiplicity conclusion is assumed. -/
theorem product_of_two_polygon_factors (m : Nat) (hm : 0 < m)
    (v : Fin (2 * m) → ℂ) (a b : ℂ)
    (hpoly : rowRootPolynomial m v =
      (Polynomial.X ^ m - Polynomial.C a) * (Polynomial.X ^ m - Polynomial.C b)) :
    (∏ i, v i) = a * b := by
  have h := congrArg (Polynomial.eval (0 : ℂ)) hpoly
  rw [rowRootPolynomial_eval_zero] at h
  simpa only [Polynomial.eval_mul, Polynomial.eval_sub, Polynomial.eval_pow,
    Polynomial.eval_X, Polynomial.eval_C, zero_pow (Nat.ne_of_gt hm),
    zero_sub, neg_mul_neg] using h

/-- The product of actual conjugate row ratios is the conjugate ratio of
the row products. For unit coordinates this is the usual entrywise ratio. -/
theorem conjugate_ratio_product {n : Nat} (u v : Fin n → ℂ) :
    (∏ i, u i * conj (v i)) = (∏ i, u i) * conj (∏ i, v i) := by
  classical
  rw [Finset.prod_mul_distrib]
  congr 1
  exact (map_prod (starRingEnd ℂ) v Finset.univ).symm

/-- Two rows and their conjugate ratio cannot all have the actual root
polynomial `(X^m-1)*(X^m+1)`. This is the all-parity obstruction used to
eliminate the binary support branch in the analytical classification. -/
theorem two_rows_polygon_product_obstruction (m : Nat) (hm : 0 < m)
    (u v : Fin (2 * m) → ℂ)
    (hu : rowRootPolynomial m u =
      (Polynomial.X ^ m - Polynomial.C 1) *
        (Polynomial.X ^ m - Polynomial.C (-1)))
    (hv : rowRootPolynomial m v =
      (Polynomial.X ^ m - Polynomial.C 1) *
        (Polynomial.X ^ m - Polynomial.C (-1)))
    (hr : rowRootPolynomial m (fun i => u i * conj (v i)) =
      (Polynomial.X ^ m - Polynomial.C 1) *
        (Polynomial.X ^ m - Polynomial.C (-1))) : False := by
  have hpu := product_of_two_polygon_factors m hm u 1 (-1) hu
  have hpv := product_of_two_polygon_factors m hm v 1 (-1) hv
  have hpr := product_of_two_polygon_factors m hm (fun i => u i * conj (v i))
    1 (-1) hr
  rw [conjugate_ratio_product, hpu, hpv] at hpr
  norm_num at hpr

#print axioms rowRootPolynomial_eval_zero
#print axioms product_of_two_polygon_factors
#print axioms conjugate_ratio_product
#print axioms two_rows_polygon_product_obstruction

end OddHalfOrder.RowProductObstruction
