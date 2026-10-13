# Width-three counterexample and the limit of fixed rank bias

Status: **WRITTEN_PROOF** of a counterexample to one policy bound,
**NOVELTY_UNCONFIRMED**. The verification agent has independently
confirmed the optimal value and full probability tree; its saved report
is separate. This does not disprove a `4/3` guarantee for every possible
randomized online policy.

## 1. Exact nine-job counterexample

Let `B=4,W=3,N=9` and take exactly the true edges

`2->5`, `3->5`, `3->6`, `6->9`.

All indices are one-based. True indegree and outdegree are both at
most two. The offline optimum is three: the schedule

`{1,2,3}; {4,5,6}; {7,8,9}`

is legal, and the width-three work bound requires at least three cycles.

Consider the policy that always issues the oldest job and, whenever
all four entries are ready, omits each of the three younger entries
with probability one third. Otherwise it issues all ready jobs.
Every execution has exactly two random choices. The complete branches
are shown below; each row has probability `1/9`.

| First omitted job | Second omitted job | Complete issue schedule | Cycles |
| --- | --- | --- | --- |
| 2 | 6 | `{1,3,4}; {2}; {5,7,8}; {6}; {9}` | 5 |
| 2 | 7 | `{1,3,4}; {2}; {5,6,8}; {7,9}` | 4 |
| 2 | 8 | `{1,3,4}; {2}; {5,6,7}; {8,9}` | 4 |
| 3 | 6 | `{1,2,4}; {3}; {5,7,8}; {6}; {9}` | 5 |
| 3 | 7 | `{1,2,4}; {3}; {5,6,8}; {7,9}` | 4 |
| 3 | 8 | `{1,2,4}; {3}; {5,6,7}; {8,9}` | 4 |
| 4 | 5 | `{1,2,3}; {4,6,7}; {5,8}; {9}` | 4 |
| 4 | 6 | `{1,2,3}; {4,5,7}; {6,8}; {9}` | 4 |
| 4 | 7 | `{1,2,3}; {4,5,6}; {7,8,9}` | 3 |

Conditional on first omitting jobs `2,3,4`, the expected total times
are respectively `13/3,13/3,11/3`. Equivalently,

`Pr(T=3)=1/9`, `Pr(T=4)=2/3`, `Pr(T=5)=2/9`.

Thus `E[T]=37/9` and the expected competitive ratio is

`37/27 > 4/3`.

This refutes the width-three uniform-omission conjecture and the
general assertion that this policy always attains
`(3-1/W)/2` at `B=W+1`.

## 2. What minimality has actually been checked

The preceding experiment exhausts every effective gap-at-most-three
true DAG on `N<=8`, totaling 299,595 graphs, with no ratio above `4/3`.
Longer true edges are redundant with ROB precedence and never change
readiness once a job is admitted. Therefore the computational evidence
establishes minimum program length nine for a violation by this policy
over all forward-dependency graphs under the model.

The targeted nine-job search stopped at its first violation, after
262,849 graphs, and did **not** exhaust all nine-job graphs. Its mask
is 262848 in `wider_policy_search.local_graph`. The exact record is
`WIDER_NINE_JOB_SEARCH.json`; the earlier complete range remains in
`WIDER_POLICY_SEARCH.json`. The respective measured runtimes were
3.829887 and 3.874363 seconds.

Every proper subset of this example's four edges was also checked.
Removing one edge gives these exact policy values (the optimum remains
three):

| Deleted edge | Expected time | Expected ratio |
| --- | --- | --- |
| `6->9` | `34/9` | `34/27` |
| `3->6` | `4` | `4/3` |
| `3->5` | `4` | `4/3` |
| `2->5` | `4` | `4/3` |

No proper subset violates `4/3`. This is inclusion-minimality for
the displayed edge set, not a claim of globally minimum edge count
among all nine-job counterexamples. The counterexample itself has
the explicit exact probability proof above; its length-minimality is
a finite computation claim with a recorded search scope.

## 3. No fixed rank bias can repair the global 4/3 guarantee

Consider the restricted policy class that always issues the oldest
instruction, issues all ready jobs when at most three are ready, and
uses the **same conditional probability vector** `(p,q,r)` at every
four-ready window to omit the first, second, or third younger job.
Thus `p,q,r>=0` and `p+q+r=1`. The vector cannot depend on total length,
visible operands, the past history, or window position. This precise
restriction matters: the conclusion below is not about all online
randomized policies.

For the nine-job program, the branches above give

`E[T | omit 2]=E[T | omit 3]=4+p`,

`E[T | omit 4]=4-r`,

and hence

`E[T]=4-r^2+(1-r)p`.

Now add the three five-job programs with initial roots `1,2,3,4`
and last job depending on each possible pair from `2,3,4`.
Each has optimum two and a different unique two-cycle first action.
For a program whose required omitted rank has probability `s`, the
exact expected time is `2s+3(1-s)=3-s`. Their worst ratio is therefore

`(3-min(p,q,r))/2`.

If all three ratios were at most `4/3`, each of `p,q,r` would be at
least `1/3`, forcing the uniform vector. The nine-job example then
violates `4/3`. Consequently no fixed rank-bias vector in this class
can guarantee `4/3` globally. A strategy with a chance of attaining
that ratio must make a richer use of available information.

The five-job and nine-job inputs have different known lengths. Thus
the argument deliberately does **not** rule out policies that adapt
their probabilities to the known length, let alone to general history.

## 4. Exact four-input minimax within the fixed-bias class

The preceding four programs yield the sharper exact restricted-class
minimax value

`rho=(13+sqrt(73))/16`,

which is strictly above `4/3`. Put `t=min(p,q,r)`, so `0<=t<=1/3`.
The five-job family gives ratio at least `f(t)=(3-t)/2`.
Since `p>=t` and `r<=1-2t`, and
`4-r^2+(1-r)p` increases with `p` and decreases with `r` on this
domain, the nine-job example gives ratio at least

`g(t)=(3+4t-2t^2)/3`.

On `[0,1/3]`, `f` decreases and `g` increases. Their unique crossing
occurs at

`t_0=(11-sqrt(73))/8`,

the smaller root of `4t^2-11t+3=0`. Thus every fixed-bias vector has
worst ratio at least `f(t_0)=g(t_0)=rho` on these four inputs.
Choosing `p=q=t_0` and `r=1-2t_0` attains equality in both lower
bounds, proving the exact restricted-class minimax assertion.

This is a minimax equality for four particular inputs and a restricted
stationary policy class. It supplies a global lower bound for that
class, but it supplies neither a global upper bound for that class
nor a lower bound above `4/3` for fully adaptive online scheduling.
