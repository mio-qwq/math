# Genuine polynomial five-term cochain identities

`CochainBasisSemantics.lean` transports the frozen packed closure certificate into genuine finite contractions over F₂[X]. It defines the actual cochain coefficients P(a,b,c,k), alongside the already established algebra constants B(a,b,k).

For every four labels a,b,c,d in the specified 18-element radical basis and every output coordinate k, Lean proves that the following sum is zero:

```
sum_j P(b,c,d,j) B(a,j,k)
+ sum_j B(a,b,j) P(j,c,d,k)
+ sum_j B(b,c,j) P(a,j,d,k)
+ sum_j B(c,d,j) P(a,b,j,k)
+ sum_j P(a,b,c,j) B(j,d,k).
```

Each of the five faces is separately interpreted. A generic sparse-contraction lemma combines faithful byte decoding, the certified product bound and finite output labels. Duplicate labels are allowed; the resulting polynomial arithmetic is untruncated. The 104,976 frozen identities are reused without another enumeration.

All nine audits compiled without warnings and use only standard axioms. The exact conclusion is a radical-basis identity. This source does not prove all-vector extension, corner balancing, a relative Hochschild complex or identification of an Ext class.

Replay requires the previously compiled `CochainClosure.olean` and `FiniteTableContraction.olean`, then `lake env lean CochainBasisSemantics.lean`. Rebuild the large closure prerequisites only when needed using `../verify.ps1`.
