# The concrete two-sided unit

`TwentyDimUnit.lean` proves that the vector `e + f`, with coordinates one at labels 0 and 8 and zero elsewhere, is a left and right identity for the actual twenty-coordinate multiplication.

Both basis identities are obtained from the frozen `t_unit_actions` certificate through faithful byte decoding and the certified table coefficient bounds. The generic finite-contraction theorem then extends the actions to every polynomial vector. Applying the polynomial specialization map gives the same two-sided unit in every commutative characteristic-two ring, for every parameter q.

All nine printed audits use only the standard three axioms. The source compiles without warnings, new enumeration, `sorry`, added axioms or `native_decide`. Associativity is supplied by `TwentyDimAssociativity.lean`; this file does not install a library algebra instance or establish the homological realization.

For replay, first build the semantic modules, `FiniteBilinearUnit.lean`, `ScalarEvaluation.lean` and the frozen `../CochainData.lean`, then run `lake env lean TwentyDimUnit.lean` with this directory and its parent in `LEAN_PATH`.
