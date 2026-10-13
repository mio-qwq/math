# Independent review of the conditional randomized-potential formalization

Reviewer: formal-DP subagent, independent of the Lean and theory authors.
Review completed 2026-10-13 UTC. No author-owned file was edited.

Reviewed Lean commit: `b2da19ea36c36f77cf491f2f0ab7df6d7e98fedf`.
`UniformYoungerPotential.lean` SHA-256:
`9e5265433d856728fc3540cfd62fbd078636570f431f29b81e1b71bf776a2a28`.
The current root paper was read at root HEAD
`d0928e6f543d1cbfe59be060f3028f668ecc3902`, with paper SHA-256
`ec6ab0ba70da05553548c8e253f834add691ad2b092a5f4c6deec8ae9545ec51`.
These hashes delimit the review; later revisions require their own checks.

## Verdict

**Accepted as a nontrivial conditional scalar induction kernel and exact
local-arithmetic verification.** No blocking mathematical, integer-scaling,
or index-boundary error was found. A fresh independent Lean compilation
passed all ten printed declaration audits. The actual randomized ROB
theorem, its expectation semantics, and its global minimax interpretation
are **not** thereby Lean verified. The author documentation states that
boundary accurately.

The manuscript's arbitrary-length 5/4 written proof is consistent with the
previously independently reviewed theory proof. Its zero-based indexing,
empty-suffix boundary, and oblivious-adversary lower bound are correct in
the inspected revision. Historical novelty remains outside this review.
This is independent research-agent review, not academic peer review.

## Interface audit: what is and is not assumed

`MacroShape` supplies four forced forms and five randomized forms for each
positive remaining length up to a fixed limit. The module assumes `s > 0`
and `k(0)=0`, then proves by strong induction both

- `k(n) >= 0`;
- `n > 0` and `f(n)=f(n-1)` imply `k(n)+k(n-1) >= s`.

Neither target inequality, nor the final 5/4 bound, occurs as an interface
hypothesis. The interface is not intrinsically inconsistent: for any limit,
`f(n)=s*n` and `k(n)=0` satisfy it using the singleton constructor at every
positive index. Actual graph coverage, however, is a separate obligation.

The substantive interface assumptions are the exact successor identities
in the three difficult random cases. These encode the conclusions of the
written local graph/readiness classification:

| Local case | Additional assumptions beyond its potential identity |
| --- | --- |
| `(length 3, difference 0)` | Equal optimal tail values and `k(n-1)=s+k(n-3)` |
| `(length 4, difference 0)` | `k(n-1)=s+k(n-3)`, or `n>=6` and `2k(n-1)=k(n-3)+k(n-5)+3s` |
| `(length 4, difference 2)` | `k(n-1)=s+k(n-3)` |

These equalities are not disguised assumptions of positivity: they expose
subsequent forced or favorable random macros, and their positivity is
obtained from strictly smaller induction indices. They are nevertheless
the hardest outstanding semantic bridge, not a cosmetic precondition.
The file imports only Std, with no import or instantiation of `ROBModel`,
`ROBOperational`, a randomized policy, or a probability space.

The weaker information retained by some constructors is sound. For
example, the favorable random cases do not need an optimal-tail difference
hypothesis once their exact potential identity is supplied. Proving the
result under weaker abstract assumptions does not establish that arbitrary
ROB states satisfy those assumptions.

## Induction and boundary checks

The zero case uses `k(0)=0`; its adjacent-equality implication is guarded by
`0<n` and therefore does not assert a false inequality for two empty tails.
Every recursive use has a strictly smaller nonnegative natural index and
inherits the same limit bound. No transition cycle or unbounded process is
silently excluded by this finite-length induction.

The sole negative local increment is the `(3,0)` row. Its guard `n>=3`
makes `n-2` positive, so the adjacent-equality induction hypothesis applies
at `n-2`, with `(n-2)-1=n-3`. This yields the required tail sum before
nonnegativity at `n` is used to prove the adjacent assertion at that same
index. There is no circular invocation of the current adjacent assertion.

All other local nonnegativity arguments use nonnegative smaller tails.
The singleton case excludes the adjacent equality by
`f(n)=s+f(n-1)` and `s>0`. The non-singleton forced and favorable random
cases provide at least `s` of potential. In the remaining three random
cases, the explicit successor identities supply the needed adjacent sum.

The `n>=6` guard in the length-four/equal-tail alternative matches the
physical graph argument. In forward notation, with `e=i+4`, that argument
derives both `F_e-F_(e+1)=1` and `F_(e+1)-F_(e+2)=1`. Thus `e+1` is an
actual job, so jobs `i,...,i+5` exist. The good successor macro at `i+1`
has reverse-index tails `n-3` and `n-5`. The source never silently reads a
negative suffix through truncated natural subtraction.

Minor explanatory nuance: `n>=6` is a fact about the actual graph case,
not merely the weakest arithmetic condition for writing `n-5`; at `n=5`
that expression denotes the legitimate empty tail. The current guard is
correct and may remain stronger than the arithmetic kernel alone needs.

## Scaling and arithmetic audit

The intended instantiation is `f=sF`, `e=sE`,
`k=3f+s*n-4e=s(3F+n-4E)`, with a common positive integer `s`.
In particular, `f` is scaled too. The source does not accidentally compare
an unscaled optimum to a scaled expectation. It represents averages by
multiplying equations by two; no integer division or rounding is involved.
The five min/mean helper proofs give exactly the five rows of the written
table, and the general forced helper gives increment `(length-cost)*s`.
Natural-to-integer length subtraction is proved under `d<=n` before use.

`scaled_expected_bound` proves `4e(n)<=s*n+3f(n)` from the induction.
`scaled_five_quarters` separately assumes the width-two work lower bound
`s*n<=2f(n)` and concludes `4e(n)<=5f(n)`. Dividing by positive `s`
is mathematically legitimate, but no probability-space interpretation or
scale-existence theorem is formalized in this file.

For the actual finite policy, the missing scaling bridge is feasible in
principle: every execution finishes within N cycles because oldest issues,
so its binary random-choice tree has depth at most N; a common scale
`2^N` clears all suffix expectation denominators. This observation is a
written bridge description only, not an additional Lean verification claim.

## Paper cross-check and required reporting boundary

The inspected paper faithfully restates the macro recurrence, one-step
optimal-value differences, joint invariant, and all three difficult graph
cases. Its final difficult case forces `u=e+2`, which justifies the same
six-job boundary even though it is not written as a separate inequality.
The move/swap normalization chooses a lexicographic minimum over **all**
optimal schedules, correctly avoiding a circular assumption that the
swapped schedule must remain non-delay.

The four-job lower bound averages over two inputs fixed independently of
random choices. The same initial observation induces the same first-action
distribution, and each possible action succeeds in two cycles on at most
one input. Hence one fixed input has expectation at least 5/2. This proves
the stated strict multiplicative 5/4 lower bound, without an adaptive
adversary or an asymptotic additive-constant claim. The upper theorem
includes the empty program as an inequality; the ratio is restricted to
nonempty inputs. No missing independence between distinct suffix states is
required by the mean recurrence.

The paper currently reports 106 earlier audited declarations and explicitly
says the complete ROB/random-policy connection is not Lean verified.
That is accurate for its pre-integration snapshot. After incorporating this
new module, the total should be 116 distinct endpoints, with the ten new
ones labeled as the **conditional scalar induction and local arithmetic**.
Do not replace this distinction with a statement that the full randomized
ROB guarantee or randomized minimax equality has been Lean verified.

## Independent reproduction

The author runner was read before execution. It invokes the pinned compiler
on the actual source, builds a fresh temporary `.olean`, and records the
axiom outputs. This independent run used a fresh temporary build and wrote
only the reviewer's owned evidence directory:

```sh
python /workspace/scratch/6a1539b44ef3/ilp1-lean/workstreams/ILP1-20261014/formal/verify_uniform_potential.py \
  --lean /workspace/scratch/6a1539b44ef3/ilp1-tools/lean-4.34.1-linux/bin/lean \
  --proc-self-compat \
  --output /workspace/scratch/6a1539b44ef3/ilp1-formal-dp/workstreams/ILP1-20261014/subagents/formal-dp/evidence/uniform-potential-independent
```

Result: exit 0, PASS, ten distinct printed endpoints, each depending only
on `propext` and `Quot.sound`. Compiler: Lean 4.34.1, commit
`5045d0056413266e57c625dcd7c365b10e377c52`, bundled Std, no Mathlib.
Compilation elapsed 1.375222 seconds. Exact source/runner/shim hashes and
timestamps are in `evidence/uniform-potential-independent/receipt.json`;
the raw compiler output is `UniformYoungerPotential.log` beside it.
The source contains no `sorry`, `admit`, new axiom, unsafe implementation,
or opaque substitute for the proved declarations. No large enumeration
was rerun for this review.
