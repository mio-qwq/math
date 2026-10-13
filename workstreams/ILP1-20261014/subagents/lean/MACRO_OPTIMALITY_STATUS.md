# Macro optimality checkpoint

Owner: ILP1 Lean subagent; branch `partner/ilp1-lean-20261014`.
Parent source checkpoint:
`f681f6a6ddc379ec683ba0e6c5d5803c1c9c4052` (first-clear decomposition).

New module `formal/ROBMacroOptimality.lean`: 20 audited declarations.
Strongest completed result: actual first-clear macros at `B=W+1` have
strictly increasing prefix endpoints and length at most `N-r`; their
mathematical minimum recurrence is equivalent to original actual
continuation optimality. A noncomputable prefixCost specification is
derived from proved actual optimum existence, with `F_N=0`, `F_0` the
original global optimum, and an attaining strictly forward macro plus
comparison with every other actual macro for each `r<N`.

Actual compilation: Lean 4.34.1, Std-only. Fresh runner
`formal/verify_macro_optimality.py`; evidence
`subagents/lean/evidence/rob-macro-optimality/`. Only standard logical
axioms. No `sorry`, `admit`, or custom axiom. Independent review of this
increment is pending and must not be inferred from prior-file reviews.

Earlier source modules are unchanged. Do not call the current
noncomputable prefixCost an executable DP. Next useful closed objectives:
prove the first-action choice classification (unique all-ready or exactly
one omitted ready job), prove macro uniqueness from that first action,
then connect a computable candidate list and simulation to these actual
macros. Runtime and schedule reconstruction remain separate obligations.

Reproduce:

```
python workstreams/ILP1-20261014/formal/verify_macro_optimality.py \
  --lean /workspace/scratch/6a1539b44ef3/ilp1-tools/lean-4.34.1-linux/bin/lean \
  --proc-self-compat --output /tmp/ilp1-macro-optimality-replay
```
