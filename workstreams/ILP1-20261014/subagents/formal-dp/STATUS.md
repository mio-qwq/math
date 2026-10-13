# Formal-DP checkpoint

Base: `d7e2e6eeae34479f9ecd123fcf4471c1c57575d7`.
Branch: `partner/ilp1-formal-dp-20261014`.
Owned path: `workstreams/ILP1-20261014/subagents/formal-dp/` only.

Completed and actually compiled: operational Bellman potential lower bounds
for all traces, witness global optimality, and a separate generic executable
finite-list search with soundness, completeness, and bounded exclusion. A further generic Bellman attainment proof constructs an exact finishing
witness by potential induction and proves value uniqueness. There are 20
new audited theorem endpoints. All precise interfaces and exclusions
are in README.md. The first clean reproduction receipt is in evidence/.

Parent review and cherry-pick are pending. No remote publication claim is
made by this checkpoint. The Python exact solver is not a Lean-verified
implementation, and the generic enumeration interface is deliberately
uninstantiated for concrete ROB states.

The operational/generic first checkpoint is local commit
`238e5f63fd8d11705397c10890dd10dec6ede6ef`; the Bellman-equality follow-up
is recorded by the enclosing commit. The separate Lean task owns concrete
bounded time/lane enumeration; do not reimplement it here. Remaining useful
interface work is a concrete certificate-table export/checker whose coverage
of ROB transitions is itself proved, which is not supplied by these files.
