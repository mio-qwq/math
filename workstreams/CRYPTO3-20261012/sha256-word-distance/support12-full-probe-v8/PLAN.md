# One bounded actual-pair query at the accepted valuation boundary

This question and stopping rule are fixed before computation. For the
exact support-12 set

    {10,11,13,15,18,20,26,28,29,34,42,43,57},

do thirteen independent, unequal, actual 32-bit word pairs satisfy all
48 original SHA-256 message-schedule difference recurrences when
`v2(d18)=16`? Every sigma0 and sigma1 derivative is evaluated on the
same two words at its index. Inactive differences and derivatives are
zero. No active pair is identified with another, and no base schedule
or padding condition is imposed.

This is strictly stronger than the stopped unrestricted six-word core
query: it includes all active-pair obligations from all original rows.
It is different from the old support-5 CNF probe. The valuation-16 layer
is allowed by the independently accepted ceiling and is chosen before
the query; no seed sweep or alternate valuation follows this run.

Protocol: one Z3 `SolverFor("QF_BV")` query with a fixed 30,000 ms
timeout. SAT is accepted only after a separate standard-library verifier
recomputes f and g one output bit at a time, checks all thirteen pairs,
the exact support, all 48 equations, and the valuation. UNKNOWN stops.
Solver UNSAT without an independently checkable proof is retained only
as an uncertified observation and also stops. The SMT2 formula, tool
version and source hashes are frozen in every outcome.

Even a verified SAT object would be only an independent-active-pair
witness. It would still require genuine base-schedule completion before
becoming two sixteen-word messages at distance 13. No compression
collision, preimage result or global bound follows directly.
