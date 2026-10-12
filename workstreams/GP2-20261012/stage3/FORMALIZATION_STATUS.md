# Formalization boundary

The reciprocal trace bound has a complete all-parameter written proof,
exact rational semantic checks, and an independently reviewed certificate
chain. Those checks are not an all-parameter Lean theorem.

The recovered local runtime
`/workspace/scratch/668a9b2a5e45/gp2-private-deps/lean-4.34.1-linux/bin/lean`
was actually invoked with `--version`. It exited 1 with
`error: failed to locate application`. An explicit `LEAN_SYSROOT` and an
isolated copied launcher with the original public library directory gave
the same error. No Lean source compilation or axiom audit is claimed in
this stage. The failure is not evidence against the mathematical theorem.
Pinned intended versions remain Lean 4.34.1 and Mathlib
`d13f23b723b8a846827a245b89c10fc7d3f11612`.

The smallest useful formalization boundary is the Frobenius Gram/trace
lemma and the six-variable tangent-polynomial inequality, followed by the
weighted reciprocal event decomposition. The inherited repair theorem
also remains written rather than fully formalized. Compile and audit each
universal step before advertising full Ka4 Lean verification.
