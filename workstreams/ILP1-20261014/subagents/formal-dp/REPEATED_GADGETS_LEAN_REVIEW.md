# Independent review of the actual repeated-gadget ROB formalization

Reviewer: formal-DP subagent, independent of the Lean author and of the
root's construction. Review date: 2026-10-13 UTC. Only this reviewer's
owned directory was modified.

Final reviewed Lean commit: `0caf016f817478ad3521a841e12513669c98b55f`.
`RepeatedGadgets.lean` SHA-256:
`d031ef0e025e25bd54821c2df7c8da8d7d3eddea30ee5be47ab461827786a612`.
The source was initially inspected while in progress, then checked against
this clean final commit before the fresh independent compilation.

Reference root note `REPEATED_GADGETS.md` SHA-256:
`b74592fdaca121692da281063cd1cc5e3f93547e7f320d26c77612df9f404925`.
Root HEAD at inspection: `c48909b3bf2254c8cf409830dc6a022025c89fa2`.
The root note and paper were active uncommitted files. The inspected
paper's SHA-256 was
`08d210307846c7bf748c33588d57465735b17651e02fa0d353a60a4bf019b02b`.
Later edits are not automatically covered by these hashes.

## Verdict

**Accepted.** This module proves the stated finite graph family's
separation, explicit schedule, exact offline optimum, and admission
primitive in the already defined actual ROB model. It is not merely a
generic theorem with uninstantiated scheduling assumptions. No blocking
graph-mapping, quantifier, horizon, or empty-program error was found.

A fresh independent build compiled `ROBModel`, `ROBOperational`, and the
new module, with 22, 11, and 20 audited declarations respectively. All
axiom dependencies are among `propext`, `Classical.choice`, and `Quot.sound`.
Only the last 20 endpoints are new; the 33 recompiled imports must not be
counted again. The documented absence of probability and observation-history
formalization is accurate and essential.

## Exact graph mapping

Writing an index uniquely as `4k+r`, with `0<=r<4`, expands `dep` into
exactly these two disjoint edge classes:

1. `4k+p -> 4k+3`, where `p=1` for bit true and `p=2` for bit false.
2. `4k+r -> 4(k+1)+s`, where `r` is 2 or 3 and `s` is 0, 1, or 2.

Conversely every edge in either displayed class satisfies `dep`. Thus
there is one within-block edge per block and six true edges per adjacent
block pair, with no extra true edges. The window-generated edges enter the
proof through `windowEdges_iff_canonicalROB`, not through a strengthened
definition of the true DAG. The graph is exactly the zero-based family in
the root note, with the harmless convention true=b and false=c.

For a target at offset 3, only the selected same-block parent is possible.
For a target at offsets 0, 1, or 2, only the two indicated previous-block
vertices are possible; initial-block roots have none. This independently
explains the correct `indegree_at_most_two` statement: every triple of
incoming predecessors contains a duplicate. It is a graph indegree result,
not a separate formalization of instruction-expression semantics.

Every target has `j/4<q`, so values of `bits` outside `[0,q)` are irrelevant.
The quantifier `bits : Nat -> Bool` therefore represents all finite hidden
bit strings without restricting which strings are allowed. No uniformity,
periodicity, or probability assumption is imposed.

## Separation and actual state semantics

`adjacent_root_separation` considers **every** legal time assignment at
B=3 and arbitrary width, not only the displayed witness. If a previous
block job is at least three indices behind the next root, the ROB window
edge gives strict precedence. Otherwise division/remainder arithmetic
places the previous job at offset 2 or 3, exactly where the true edge
supplies the missing precedence. The next block's hidden job follows one
of its own roots, so it cannot evade the barrier.

Nonadjacent blocks are separated by the all-pairs window constraints.
The proof needs neither non-delay execution nor a specific priority rule;
idle cycles and underfilled issue batches remain allowed. The operational
corollary states that at the actual issue-cycle state of any later-block
job, every earlier-block job is already completed. This is precisely the
strict next-cycle availability convention, without an uncounted separator.

`hidden_not_admitted` has the premise `c<=t(a_k)`. At the start of such a
cycle, `a_k` is incomplete, retirement cannot pass its index, and eager
admission is at most `4k+3`, the index of `d_k`. Since admitted indices are
**strictly below** the admitted frontier, the non-strict frontier inequality
really does exclude `d_k`. The boundary `c=t(a_k)` is correct: a job issued
in that cycle only completes at its end. The lemma does not assert that
`d_k` remains hidden in the following cycle.

This admission theorem is a single-trace state fact. It does not prove that
two different hidden-bit programs induce identical observation histories,
nor a conditional distribution statement about a policy's random state.

## Schedule, global optimum, and boundary audit

The explicit schedule uses cycles `2k` and `2k+1` for block k. The oldest
job and selected parent use the first cycle; the other root and hidden job
use the second. The phase/lane table assigns at most two jobs to each
cycle. Its `decide` proof is a four-entry local fact, not finite testing of
the arbitrary-block theorem.

The proofs separately establish true-dependency legality, the canonical
ROB condition, and the width-two bound. In a single block the only pair
with index gap at least three is oldest-to-hidden, and it has strictly
increasing phase. Different blocks have strictly increasing base cycles.
The resulting witness has all issue times strictly below `2q`.

The lower bound is genuinely global. For any legal schedule, the hidden
parent-to-last edge and the proved inter-block barrier form a two-job chain
per block. Induction proves `t(d_k)>=2k+1`, regardless of issue width.
Applying the horizon's strict upper bound to the final block gives
`2q<=horizon`. This is not an assumption that a schedule executes the
blocks in the proposed way, nor an enumeration over a bounded horizon.

`optimal_two_per_block` combines a real feasible witness with this lower
bound against **every** feasible horizon in the existing definition of
`Optimal`. `operational_two_per_block` constructs an actual trace whose
retired frontier is `4q` at boundary `2q`. Conversely,
`trace_finished_lower_bound` transfers the lower bound to arbitrary
completed actual traces.

All main endpoints quantify over `q : Nat`, including q=0. At zero the
vertex type is empty, the schedule's legality and horizon conditions are
vacuous, the witness trace is initially finished, and the optimum is zero.
The lower-bound proof explicitly branches on q=0 before selecting the last
block. Block-local lemmas require `k<q`, so no nonexistent block is selected.

`two_cycle_block_forced` correctly assumes all four issue times lie in
`[start,start+2)`. The oldest-to-hidden window edge and parent-to-hidden
true edge force both predecessors to issue at `start`, and the hidden job
at `start+1`. It states these times, not an unconditional two-element batch
for arbitrary width. At width two those two distinct predecessors fill the
first batch, as the accompanying documentation correctly explains.

## Coverage of the paper's new lower-bound argument

The inspected paper's repeated-gadget section uses the same true edge
family and the same strict block separation. Its explicit two-cycle
witness and the value `T*=2q` are now supported by this actual-model Lean
module. The graph fan-in bound, hidden-job admission primitive, and forced
first-cycle jobs are also formalized for arbitrary q.

Still not formalized are a policy/observation process, coupling of histories
under unseen-bit changes, independent input bits, conditional expectations,
the fixed-input averaging step, expected duration `5q/2`, deterministic
adversarial completion, or the argument excluding a smaller competitive
factor with any fixed additive constant. Those remain independently reviewed
written mathematics. The new module must not be described as a complete
Lean verification of the randomized or deterministic online lower bounds.

The current pre-integration paper reports 116 earlier endpoints and says
the old four-job obstruction alone does not formalize the composition.
After integration, add 20 new endpoints for a total of 136, retaining the
distinction between the verified repeated-program structure/offline optimum
and the unformalized observation/probability argument. Historical priority
is not assessed in this review.

## Reproduction

The runner was read before use and rebuilds both local imports in a fresh
temporary directory. The independent command was:

```sh
python /workspace/scratch/6a1539b44ef3/ilp1-lean/workstreams/ILP1-20261014/formal/verify_repeated_gadgets.py \
  --lean /workspace/scratch/6a1539b44ef3/ilp1-tools/lean-4.34.1-linux/bin/lean \
  --proc-self-compat \
  --output /workspace/scratch/6a1539b44ef3/ilp1-formal-dp/workstreams/ILP1-20261014/subagents/formal-dp/evidence/repeated-gadgets-independent
```

All three compiler calls exited zero. The new module compiled in 1.179197
seconds; the two imports took 0.534562 and 0.496061 seconds. Compiler:
Lean 4.34.1, commit `5045d0056413266e57c625dcd7c365b10e377c52`, bundled Std,
no Mathlib. Exact hashes and timestamps are in the independent receipt;
all three raw compiler logs are saved alongside it. The new source contains
no `sorry`, `admit`, new axiom, unsafe definition, or native proof shortcut.
No large enumeration was rerun. This is research-agent verification, not
academic peer review.
