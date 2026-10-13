# Finite execution representation checkpoint

Owner: ILP1 Lean subagent; branch `partner/ilp1-lean-20261014`.
Parent source checkpoint before this increment:
`daa73300afcbeb724be39077f42e97c746464895` (ROBNonDelay).

Completed new file: `formal/ROBRepresentation.lean`, 16 audited declarations.
The actual finite ROBStep model now has a proved equivalence with the
original global `Feasible` and `Optimal` predicates from its initial state.
For arbitrary finite forward programs and positive resources, there is a
global optimal non-delay actual profile and a legal time assignment with
exactly the same issue decisions, horizon at most `n`.

Core proof: labelled Profile induction, residual time/lane extraction,
strict dependency and window edges, unique issue of each initially pending
job. Empty programs and padded completion horizons are covered.

Actual verification: Lean 4.34.1, Std-only, fresh runner
`formal/verify_representation.py`; evidence under
`subagents/lean/evidence/rob-representation/`. No custom axiom, `sorry`,
or `admit`; only standard logical axioms appear in audits.
Independent review of this increment is pending until a separate reviewer
reports acceptance; prior NonDelay review is separate and already accepted.

Old reviewed source files are unchanged. The next mathematical bridge is
first-clear-prefix macro decomposition of actual non-delay profiles, and
then soundness/completeness of the prefix dynamic program. The current
result does not assert that all non-delay choices are optimal.

Next reproduction command from the worktree root:

```
python workstreams/ILP1-20261014/formal/verify_representation.py \
  --lean /workspace/scratch/6a1539b44ef3/ilp1-tools/lean-4.34.1-linux/bin/lean \
  --proc-self-compat --output /tmp/ilp1-representation-replay
```
