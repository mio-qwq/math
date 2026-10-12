# Accurate failure record and scope

The exact actual-pair constraints were submitted without a restriction
on v2(D), an input XOR mask, base words or carries. All six endpoint words
and both sigma derivatives are genuine 32-bit values in the same formula.

The one Z3 `SolverFor("QF_BV")` check reached its 15000 ms resource limit
and reported UNKNOWN with reason `timeout`. The observed check duration
was 15.002334051 seconds. UNKNOWN is not UNSAT and does not establish that
a solution is absent, rare or difficult in any general sense. Solver
statistics are preserved as diagnostics; they do not certify domain
coverage. No model was extracted from UNKNOWN.

The failure mechanism established by this run is simply failure to decide
the exact unrestricted formula within the specified budget. It does not
identify an algebraic obstruction or validate any proof search branch.
The prepared independent verifier has no positive execution evidence in
this run. Its presence is reproducibility preparation, not an accepted
witness or a newly tested theorem.

The stage is frozen after this one query. Existing high-divisibility
candidate exclusions remain separate mathematical objects. This probe
neither verifies nor refutes those exclusions and never used them to
discard lower-valuation D. It leaves the entire necessary-core feasibility
question open and yields no distance-13 schedule pair or bound of 14.
