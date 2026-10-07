# Actual five-face closure on arbitrary radical-span vectors

`TwentyDimCochain.lean` evaluates the actual cochain constants by genuine trilinear finite sums. It proves that basis inputs recover the specified table, and that all five vector faces on basis inputs have exactly the already verified structure-constant contractions.

For arbitrary functions U,V,W,Z from `Fin 18` to any commutative characteristic-two ring R, let u,v,w,z be their linear combinations of the eighteen specified radical labels. At every parameter q, Lean proves the actual vector identity

`u*P(v,w,z) + P(u*v,w,z) + P(u,v*w,z) + P(u,v,w*z) + P(u,v,w)*z = 0`.

Every multiplication and cochain evaluation here is the previously defined actual table operation. The proof extends the verified basis contractions by four-linearity. It requires no new enumeration and no nonzero-parameter hypothesis.

All twelve audits compile without warnings and use standard axioms. The statement concerns the explicitly defined radical-label span; this file does not identify it with the Jacobson radical or construct a relative complex, resolution or Ext class.
