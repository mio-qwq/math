# Second Lean increment

The first increment remains frozen at
`ada228db8a794f1c0404ff591eac9fa64b024a99` for independent review.
Only the new `formal/OnlinePair.lean`, its explanatory scope note and separate
evidence were added for the second increment.

The new module compiles on Lean 4.34.1 and adds 16 audited declarations.
The strongest endpoint quantifies over all deterministic initial-window-local
first-decision policies and establishes a member of the four-job pair with
offline optimum 2 and every policy-consistent completing execution costing
at least 3 cycles. It does not assume a particular greedy rule.

The 49 combined declaration audits and exact source hashes are in
`evidence/online-pair/receipt.json`. The original 33-audit evidence remains
unchanged in `evidence/receipt.json`.

Next useful formal gap: executable bounded enumeration correctness, followed
by a bridge between that specification and the independently tested Python
solver. The current files do not claim to verify the Python implementation.
