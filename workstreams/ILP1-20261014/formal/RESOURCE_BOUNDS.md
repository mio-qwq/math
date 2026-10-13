# Exact resource caps for this ROB model

`ResourceBounds.lean` adds seven compiled general theorems, with standard
axiom audits. They apply to arbitrary finite programs and time assignments.

For each job `i`, assign a lane equal to
`i - retirementCount(t_i)`. Canonical ROB visibility places that lane in
`{0,...,B-1}`. Jobs issuing in the same cycle use the same retirement frontier,
so equal lanes imply equal job indices. Thus every ROB-legal time assignment
already satisfies width `B`.

Consequently, for every program and horizon:

`Legal(P,B,W,t) <-> Legal(P,B,min(B,W),t)`.

The corresponding feasibility and optimal-horizon predicates are equivalent.
In particular increasing width beyond the ROB capacity cannot improve the
optimum under these specific retirement, admission, and latency rules.

The module also proves that when `B>=N`, every time assignment satisfies the
ROB visibility condition. Legal scheduling then consists exactly of true
dependency order plus the width constraint. This identifies the full-window
baseline with ordinary unit-time precedence scheduling.

These are basic model/resource identities, with no historical novelty claim.
They do not determine the potentially smaller program-dependent saturation
values `B_sat` or `W_sat`, and they do not transfer automatically to processors
with different window-release or same-cycle bypass semantics.

The full author-run 68-declaration receipt is preserved in
`subagents/lean/evidence/resource-bounds/`; earlier receipts remain unchanged.
