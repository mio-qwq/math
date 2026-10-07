# The recursive A-linear differential family

`FiniteFreeBarRecursive.lean` defines actual A-linear maps
`D(n) : P(n+1) →ₗ[A] Pn` for every n. D(0) is the existing character
boundary. The next map is prescribed on the entire A-basis by

`D(n+1)(e_(i::w)) = cb_i • e_w + Hn(D(n)(cb_i • e_w))`.

Basis extension uses the central coefficient ring R as its outer
scalar and the true noncommutative A-module action. All A-valued
word coefficients occur in the proved full evaluation formula.
The recursion decreases its natural-number index without negative
indices or degree-changing assumptions.

Compilation and independent replay passed without warnings, with eight
standard-axiom audits. Exact hashes and toolchain are recorded in the
verification JSON. The definitions and basis formulas by themselves
do not assert chain laws or exactness; those are proved separately.
