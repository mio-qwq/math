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

`PERFECT_SATURATION_REVIEW.md` independently accepts theory commit
`69dc6527d69918972f8f5576410fde7d409a5ecc`: the arbitrary-width two-macro
characterization for B=W+1 and W dividing N, the path-component criterion,
the weaker odd-interval negative certificate, and O(N+|E|) edge accounting.
The final nondivisible aside has the necessary full-first-action guard;
the earlier unguarded wording is not a counterexample to the final theorem.
`perfect_negative_certificate_check.py` independently checks actual edge
witnesses without trusting producer flags. All 29 targeted parser/tampering
checks passed; evidence is in `evidence/perfect-negative-checks.json`.
No CSP enumeration was repeated, and no Lean verification is claimed here.

`CORRIDOR_LEAN_REVIEW.md` independently accepts Lean commit
`bf7b46cf258d357fdf2ba85d59b0299f68cf4d2c`: actual lane-injection work
bounds and the closed ROBTrace corridor/count bounds for every completing
horizon H and cut 0<=t<=H. Fresh compilation passed 16+9=25 new endpoints
and both imports. All audits use standard axioms only; empty/final-layer
and natural-subtraction semantics passed review. Evidence is saved in
`evidence/corridor-independent/`. The binomial candidate-state bound,
tightness, exact reachability algorithm, and Python remain unformalized
by these modules; do not promote those statuses with the strip theorem.

`LOOKAHEAD_BOUNDARY_REVIEW.md` independently accepts theory commit
`f9c74fc56e96a69772f7106519b3373df49c4ac6`: even all-but-last incoming
information cannot ensure an optimal first action at B=4,W=3, with every
N>=7 and every fixed extra-lookahead L covered by the stated length bound.
The two optimum values, first-action sets, padding/admission endpoints,
and exact promised-pair minimax ratios passed independent proof review.
This gives no additive-constant lower bound or global upper algorithm.
Small independent time-CSP evidence covers 12 programs, 216 decisions,
60 operational replays, and 33 observation pairs; all passed. Script and
`evidence/lookahead-pair-checks.json` are saved. No Lean/novelty claim is made.

`READY_CONTINUATION_LEAN_REVIEW.md` independently accepts author commits
`4b7334a571f2ee24ee84297774a243affa7b3814` and
`0ddd4ba34ad7554ea32e487c18aea92bc28e9cf9`. Separate fresh runner invocations
rebuilt all imports and passed 25+12=37 new audited endpoints. Actual ROB
coherence, ready/hole counting, forced non-delay actions, non-delay trace
termination, and completion dominance for finite chains of actual ROBStep
transitions passed semantic review. Source hashes and complete receipts are in
`evidence/ready-independent/`, `evidence/continuation-independent/`, and
`evidence/ready-continuation-provenance.json`. All audits use only standard
axioms; source is byte-identical to the pinned commits. No infinite-trace
splicing, non-delay optimum existence, macro DP, or Python verification is
claimed. A later untracked ROBNonDelay module was outside this review.

That later module now has its own review: `NONDELAY_LEAN_REVIEW.md` accepts
author commit `daa73300afcbeb724be39077f42e97c746464895`. Fresh independent
compilation rebuilt five imports and passed 11 new audited endpoints with only
standard axioms. Actual action extension, exact-horizon finite normalization,
bounded non-delay completion, and an optimal non-delay finite continuation from
every coherent forward-program state with positive B,W are now proved and
independently reviewed. Evidence is in `evidence/nondelay-independent/` and
`evidence/nondelay-provenance.json`. The complete time-assignment representation
bridge and macro-DP/Python verification still remain open; arbitrary non-delay
policies are not claimed optimal. No foreign file was changed.

The standard-initial-state representation gap is now closed by a later increment:
`REPRESENTATION_LEAN_REVIEW.md` independently accepts author commit
`0b4e56b3fe5e9dbf2d7e3132d991886a0b88a4f7`. Fresh compilation rebuilt six
imports and passed 16 new audits with only standard axioms. Actual finite
profiles produce exact issue times/lanes; initial finite finishing chains are
equivalent to original Feasible, their optima to original Optimal, and a global
optimal non-delay profile has an exactly matching legal time assignment.
Evidence is in `evidence/representation-independent/` and its provenance JSON.
Arbitrary-state residual realization does not assert global legality of already
completed jobs' dummy times. Infinite canonical-state identification, prefix
macro decomposition, and executable DP remain outside this proof.
`FIRST_CLEAR_PREFIX_INTERFACE.md` records only a proposed next formal interface,
with no additional Lean-verified theorem claim.

`FORCED_PREFIX_LEAN_REVIEW.md` accepts author commit
`f681f6a6ddc379ec683ba0e6c5d5803c1c9c4052`. Independent fresh compilation
passed 18 new audits plus all seven imports with only standard axioms. Actual
successor uniqueness, nonclear all-ready forcing at B=W+1, bounded first-clear
tail existence/uniqueness, and decomposition retaining the original non-delay
action list and suffix are now verified and reviewed. Evidence and pinned hashes
are in `evidence/forced-prefix-independent/` and its provenance JSON.
PrefixMacro permits terminal idle macros; positive list length is not yet
strict endpoint advance. Macro N-r bounds, optimal cost recurrence, action
enumeration and executable DP are not claimed by this module. The author's
untracked ROBMacroOptimality file was outside this review.
