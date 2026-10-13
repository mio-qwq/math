# R5 window-footprint review and formalization checkpoint

Base local commit: `3fbc203a21b23d5ac42203ae4bdb6af5b2df9c79`.
`git fetch origin` completed before this increment; the worktree was clean.
The current root worktree's `THEOREMS.md` R5 and the theory subagent's
`STRUCTURAL_RESULTS.md` Theorem 2 were read before deriving the proof.

## Independent check of the written window claim

The written formula is correct under its stated nonempty-program and positive
resource convention. The all-pairs ROB constraint is equivalent to
`t(j)<=t(i) -> j<i+B`. For i<j, this is exactly `j-i+1<=B`.
When i>=j it follows automatically from B>0. The diagonal forces B>0 when
the program is nonempty. Thus the seed 1 is necessary for the strict-pair
presentation and makes the upper-bound predicate exact.

The maximum exists because every demand is bounded by `max(1,N)`.
The formal proof additionally proves attainment, rather than silently treating
an arbitrary upper bound as the actual maximum. The central iff works for
every natural-number time assignment; no extra horizon hypothesis is needed.

## Actual Lean coverage

New file: `formal/ResourceFootprint.lean`.
New audited declarations: 18, all actually compiled against Lean 4.34.1.
The strongest endpoint `fixed_schedule_minimum_window` proves the exact
minimum capacity for the given legal time assignment and fixed issue width.
All prior Lean files and prior run receipts remain unchanged.

Source-specific logs, compiler version, hashes and axiom dependencies are in
`evidence/resource-footprint/`. The new standalone runner is
`formal/verify_footprint.py`; it compiles imports from scratch.

The result's originality remains unconfirmed. This is a precise fixed-schedule
resource characterization, not a claimed efficient optimizer over schedules.
The width-cardinality formula and global saturation minimizations in R5 remain
outside this module. Independent parent review/recompilation is the next gate.
