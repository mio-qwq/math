# Repeated-gadget formalization checkpoint

Base local commit: `b2da19ea36c36f77cf491f2f0ab7df6d7e98fedf`.
The worktree was clean and `git fetch origin` completed before this increment.
Read the main agent's `REPEATED_GADGETS.md` and the independent theory review
`REPEATED_GADGET_REVIEW.md` (parent identifies review commit `91b7d2e`).

New source `formal/RepeatedGadgets.lean` proves the actual arbitrary-q family
and exact offline optimum in the existing ROB model, not a conditional
surrogate recurrence. Twenty primary declarations have real Lean 4.34.1
compilation and transitive axiom audits. Existing Lean files, runners and
earlier receipts remain unchanged.

Mathematical scope: every q>=0 and bit sequence; at most two true parents per
job; arbitrary legal idling and underissue; separation and lower bound valid
for every issue width at B=3; the explicit attaining schedule uses W=2.
The empty program has the correct optimum zero. The opposite bit convention
from another note, if any, just swaps names b and c; here true selects b.

Independent proof route: the lower bound is a repeated critical chain, one
parent-to-d edge per block plus the fully proved barrier between blocks.
This is stronger than needing to infer additivity of counted block durations.

Additional actual-state lemma: d_k is not admitted while a_k is incomplete.
Additional scheduling lemma: any two-consecutive-cycle block necessarily
starts with a_k and its hidden parent, and ends with d_k.

The probabilistic/observation-history bridge remains open. Nothing here
asserts expected duration, minimax optimality, or a general online bound.
The next valuable gap is a precise prefix-observation interface connecting
the state-level admission lemma to indistinguishability for policies with
arbitrary memory, followed by a finite probability averaging proof.

Fresh replay command:

```sh
python workstreams/ILP1-20261014/formal/verify_repeated_gadgets.py \
  --lean /workspace/scratch/6a1539b44ef3/ilp1-tools/lean-4.34.1-linux/bin/lean \
  --proc-self-compat --output /tmp/ilp1-repeated-gadgets-root-check
```

Independent parent review/recompilation is the next integration gate.
