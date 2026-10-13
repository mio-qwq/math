# Independent refutation of uniform younger omission at B=4,W=3

Verification subagent C, 2026-10-13 UTC. The nine-job witness was discovered by
the theory agent. This reviewer independently verifies its optimum with the
time-variable CSP and its expected policy cost by a full direct ROB probability
tree. This refutes the proposed bound for **this particular policy**; it does
not refute the existence of a different `4/3`-competitive online policy.

## The exact counterexample

Use zero-based jobs `0,...,8`, `B=4`, `W=3`, and true edges

`(1,4), (2,4), (2,5), (5,8)`.

All other true edges are absent. The maximum indegree and outdegree are both
two. The offline optimum is exactly three: the work bound is `9/3=3`, and
the legal schedule is

`{0,1,2}; {3,4,5}; {6,7,8}`.

The policy always includes the oldest job. At a full ready window of four
jobs it omits each of the three younger jobs with probability `1/3`; elsewhere
it issues every ready job. Its complete execution tree has exactly nine
equiprobable leaves, each of probability `1/9`:

| First action | Possible total durations, conditional probabilities 1/3 each | Conditional expected duration |
| --- | --- | --- |
| `{0,2,3}` | `5,4,4` | `13/3` |
| `{0,1,3}` | `5,4,4` | `13/3` |
| `{0,1,2}` | `4,4,3` | `11/3` |

Consequently

`P(T=3)=1/9`, `P(T=4)=2/3`, `P(T=5)=2/9`,

and `E[T]=37/9`, with ratio `37/27 > 4/3`.

Every leaf schedule passes the independent operational replay. The complete
schedules, cycle-start completed sets, visible windows, ready sets, and visible
predecessor sets are saved in `wider_policy_independent_results.json`.

The initial ready window is `{0,1,2,3}`. After either of the first two actions,
only the omitted root is ready in cycle two. Both histories then reach the
same clear-prefix state with completed prefix `{0,1,2,3}`; the next full ready
window is `{4,5,6,7}`. Choosing to omit job `5` there delays hidden successor
`8`, yielding the five-cycle leaves. After the third first action, the second
full ready window is `{3,4,5,6}`; omitting job `6` yields the three-cycle leaf.
Each random choice uses only the observed ready window. The future program is
fixed in advance throughout; there is no adaptive alteration of dependencies.

Oldest-ready ordering happens to execute the displayed three-cycle optimum.
Thus this witness exposes a failure of independent uniform decisions across
connected stages, not an impossibility theorem for all online schedulers.

## Minimality scope

The theory agent's `WIDER_POLICY_SEARCH.json` records all 299,595 effective
graphs of gaps one through three on `1<=N<=8`. Its recorded source hash is
`49126292496e3f8d3174e2f8b36ada45e8b38c8c526fbb08fa1e86bd2d478ba8`.
It found no violation of `4/3`. Longer true edges are redundant with the ROB
precedences at `B=4`, so this is a finite minimum-job-count result for the
specific policy under the model. This reviewer read that report and its source
but did not rerun that exhaustive enumeration.

At `N=9`, the theory search stopped at mask `262848` after examining 262,849
graphs. It did **not** exhaust all nine-job graphs. This reviewer separately
checked all 15 proper edge deletions of this witness and all nine single-vertex
deletions (compacting indices and removing incident edges). None retains the
violation. This establishes deletion minimality of the displayed witness,
not the absence of a different nine-job counterexample with fewer edges.

## Earlier finite support and a failed potential

Before receiving the counterexample, this reviewer sampled 10,000 graphs for
each `W=3,4,5`, with `B=W+1`. The single sequential RNG seed was `2026101407`.
Each sample chose `N` uniformly from `W+2,...,40`, a local-edge inclusion
probability from `{0.1,0.2,0.3,0.4,0.5,0.6,0.8}`, and candidate incoming edges
from the preceding `W` jobs. If more than two parents were selected, it retained
two uniformly sampled parents. Thus every sampled graph has indegree at most
two. Exact completed-set recursions supplied the optimum and rational policy
expectation; the retained extremal witnesses were subsequently checked by CSP.

None of these 30,000 samples exceeded `(3-1/W)/2`. The maxima were:

| W | N | Edges | F | E | E/F |
| --- | --- | --- | --- | --- | --- |
| 3 | 5 | `(2,4),(3,4)` | 2 | 8/3 | 4/3 |
| 4 | 7 | `(4,5),(3,5)` | 2 | 11/4 | 11/8 |
| 5 | 9 | `(3,7),(5,7),(5,8)` | 2 | 14/5 | 7/5 |

These observations were only finite support, and the nine-job width-three
counterexample supersedes the general policy conjecture. The experiment is
preserved to prevent its positive finite result from being mistaken for a
proof or silently disappearing after refutation.

The natural-looking extension of the width-two potential,

`K=N+(2W-1)F-2W E`,

already fails on the first row: at `W=3,N=5,F=2,E=8/3`, it equals `-1`.
Thus that particular induction proposal was invalid even before the eventual
policy-bound counterexample. The valid width-two theorem remains unaffected.

Reproduction: `python wider_policy_independent.py`. The script reproduces the
fixed-seed sample, checks the extremal witnesses, enumerates the full probability
tree, and performs the deletion checks. Its source hash, Python version, actual
runtime, and exact rational outputs are in `wider_policy_independent_results.json`.

Status: the wider uniform-policy conjecture is **REFUTED**; this counterexample
is **INDEPENDENTLY_REVIEWED**. No Lean or originality claim is made here.

## Independent review of a fixed-rank-bias repair

The theory agent additionally considered policies using the same conditional
probabilities `(p,q,r)` at every full ready window to omit the first, second,
or third younger job. The vector is fixed across lengths, visible operand
patterns, and histories; otherwise all ready jobs issue. I independently
accept the following four-input restricted-class calculation.

In the nine-job example, the first two omission branches have expected total
time `4+p`, because only the next first-rank omission takes five rather than
four cycles. The third first branch has expected total time `4-r`, because
its next third-rank omission is the only three-cycle leaf. Hence

`E_9=(1-r)(4+p)+r(4-r)=4-r^2+(1-r)p`.

For each of the three five-job programs with four roots and a final job
depending on a pair of younger roots, two-cycle success corresponds to one
omitted rank. Their expected costs are `3-p`, `3-q`, and `3-r`, with optimum
two. In particular, keeping all three ratios at most `4/3` forces
`p=q=r=1/3`, which the nine-job example disproves. No fixed vector in this
restricted class can globally guarantee `4/3`.

More precisely let `t=min(p,q,r)`. The three short inputs give worst ratio
`f(t)=(3-t)/2`. Since `p>=t` and `r<=1-2t`, and `E_9` is nondecreasing
in `p` and nonincreasing in `r` on the probability simplex, the fourth ratio
is at least `g(t)=(3+4t-2t^2)/3`. Here `0<=t<=1/3`; `f` decreases and
`g` increases. Their unique crossing is

`t_0=(11-sqrt(73))/8`, from `4t^2-11t+3=0`.

Thus the exact minimax value on these **four inputs within this restricted
policy class** is `(13+sqrt(73))/16`. The choice `p=q=t_0,r=1-2t_0`
attains both bounds. This is not a global upper bound over every program,
and it is not a lower bound above `4/3` for arbitrary online policies.
In particular, the five-job and nine-job inputs have different lengths,
so a policy permitted to choose different biases at different known lengths
is not covered by this argument.

`fixed_bias_audit.py` reweights the independently generated full ROB execution
trees for all 91 probability triples on the denominator-12 simplex. The 364
exact rational program checks confirm the displayed formulas and inequalities.
Their scope, source hashes, and actual runtime are in `fixed_bias_results.json`.
The algebra above supplies the continuous-parameter proof; the finite grid
is not being used as a proof for arbitrary probabilities.
