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

At the original checkpoint, parent review and cherry-pick were pending;
the later root manuscript includes these 20 endpoints in its 106-endpoint
audit. This status file does not itself assert remote publication. The Python exact solver is not a Lean-verified
implementation, and the generic enumeration interface is deliberately
uninstantiated for concrete ROB states.

The operational/generic first checkpoint is local commit
`238e5f63fd8d11705397c10890dd10dec6ede6ef`; the Bellman-equality follow-up
is recorded by the enclosing commit. The separate Lean task owns concrete
bounded time/lane enumeration; do not reimplement it here. Remaining useful
interface work is a concrete certificate-table export/checker whose coverage
of ROB transitions is itself proved, which is not supplied by these files.

## Later independent reviews

`PAPER_REVIEW.md` records the original manuscript review and its corrected
minimum-window boundary. `RANDOMIZED_POTENTIAL_REVIEW.md` independently
accepts the arbitrary-length written 5/4 proof at B=3, W=2.

`UNIFORM_POTENTIAL_REVIEW.md` reviews Lean author commit
`b2da19ea36c36f77cf491f2f0ab7df6d7e98fedf` and the corresponding new paper
section. An independent fresh compilation passed all ten new endpoints,
with only standard `propext` and `Quot.sound`; source hashes and logs are
saved in `evidence/uniform-potential-independent/`. This establishes the
conditional scalar induction and local arithmetic only. Derivation of
`MacroShape` from arbitrary ROB programs and probability semantics remains
unformalized. No blocking error was found in the inspected written proof.

Current useful next step: prove one actual ROB-to-macro semantic interface,
starting with oldest-inclusive normalization or the two-action clear-prefix
recurrence, without relabeling the conditional kernel as the full theorem.
The wider B=4, W=3 uniform-omission 4/3 candidate has been reported refuted
by the theory agent; do not spend further proof effort assuming that bound.

`REPEATED_GADGETS_LEAN_REVIEW.md` independently accepts final Lean commit
`0caf016f817478ad3521a841e12513669c98b55f`: the exact arbitrary-q graph
family, all-schedule block barrier, hidden admission primitive, forced
two-cycle actions, actual legal witness, and global offline optimum 2q.
Fresh independent compilation rebuilt both imports and passed all 20 new
audited endpoints. Evidence is in `evidence/repeated-gadgets-independent/`.
This is an actual-model theorem, but the online observation and probability
bridge and additive-constant lower bounds remain written proofs.
