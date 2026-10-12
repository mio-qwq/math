# Precommit: screen all frozen twin representatives

Input is exactly the 21 directly checked twin fixtures in `CERTIFICATE.json`
with SHA-256
`f74dd80590b0e6b9c3f2ccb4841e9c39b94dd03a53c065dd16f3e48252854bd5`.
For every fixture run two QF_BV queries, in certificate order: the required
third forward-D joint member `(-A,-T)`, and the reciprocal sigma0 edge
`F_A(u)=D`.  Each query has a 30-second timeout, no changed seed, no retry,
and no use of another twin word beyond the frozen list.

A fixture advances only when both queries are SAT and both returned words
pass direct standard-library evaluation.  UNSAT is an uncertified solver
observation, not an exclusion; UNKNOWN stops that query.  The fixed maximum
is 42 queries.  A positive result is only a selected four-pair local
witness and does not fulfill the other support rows or base completion.

