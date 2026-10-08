# Actual two-polygon products and a row-ratio obstruction

For an actual complex vector v indexed by Fin(2*m), the source defines
its root polynomial as the product of the linear factors X - v(i).
Evaluation at zero equals the product of its coordinates because the
degree 2*m is even. If that actual polynomial is

```text
(X^m-a)(X^m-b),
```

Lean derives the coordinate product a*b by polynomial evaluation. The
row product is a conclusion, rather than a supplied assumption.

The product of an actual conjugate row ratio is the first row product
times the conjugate of the second. Consequently two rows and their
conjugate ratio cannot all have root polynomial

```text
(X^m-1)(X^m+1).
```

Each individual product would be -1, while the product identity forces
the ratio product to be 1. This is the elementary product obstruction
used to eliminate the binary support branch in the analytical
[all-half-order classification](../../general-patterns.md).

The source does not derive the two-polygon factorization from Newton
identities or Hadamard hypotheses, nor formalize the complete matrix
classification or phase-circle construction. Those general results
currently have written proofs. The obstruction is classically related
to even cyclic complete mappings; no novelty claim is made.

The companion verification JSON records actual compilation, independent
replay of the frozen source, four standard-axiom audits and its SHA256.
From the pinned Mathlib package directory:

```powershell
lake env lean RowProductObstruction.lean
```
