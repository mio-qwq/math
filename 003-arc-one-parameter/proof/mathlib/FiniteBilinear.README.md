# Associativity from finite structure constants

`FiniteBilinear.lean` is an independent general theorem over every commutative semiring R and finite index type I. For constants B(a,b,k), it defines

`mul B u v k = sum_a sum_b u(a) * v(b) * B(a,b,k)`.

If the finite basis contraction identities `sum_j B(a,b,j) * B(j,c,k) = sum_j B(b,c,j) * B(a,j,k)` hold, the file proves associativity for **every** vector u,v,w. Expanding and reordering four finite sums gives the two sides; the hypothesis identifies each contracted summand. No finite computation or added axiom is used.

The theorem compiled without warnings and its audit lists only the standard three axioms. Its source hash is recorded in `FiniteBilinear.verification.json`.

The sparse-table-to-finite-contraction bridge is a separate step. This generic theorem does not claim that the ARC table already meets its hypothesis, install a twenty-dimensional algebra instance, or prove its homological realization.

From this directory:

```sh
lake exe cache get Mathlib/Algebra/BigOperators/Ring/Finset.lean Mathlib/Algebra/BigOperators/Group/Finset/Sigma.lean
lake env lean FiniteBilinear.lean
```
