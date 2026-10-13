# Independent review: the sharp randomized three-entry ROB bound

Reviewer: ILP1 formal-DP subagent. Date: 14 October 2026, Asia/Singapore.
The theorem/proof was proposed and written by the separate theory subagent.
This reviewer did not author its joint-invariant argument.

Inspected source files from the theory worktree at HEAD
`9199c455925b65cfd609955ded7d39279b6d6011`:

- `NARROW_WINDOW_POLICY.md`, SHA-256
  `15af4461b535c14fddc98452eb20b8bbc0938006a917fb8f2ab95f54cc3bd9e5`.
- `RANDOMIZED_FIVE_QUARTERS.md`, SHA-256
  `9bc895ef7cb70165527f8b7982ee6438f9b7ca4d953434c64051e0a14625c68f`.

The second file was read as an active draft; these hashes identify the exact
proof text reviewed, regardless of when its author commits it.

## Result

**Accepted as an arbitrary-size written proof under the specified R1 model.**
No blocking proof gap or counterexample was found. Its attributes may be
recorded separately as WRITTEN_PROOF and INDEPENDENTLY_REVIEWED. This review
does not supply Lean verification, independent journal peer review, or
historical novelty clearance.

For B=3,W=2, the oldest-inclusive policy that chooses either younger ready
job with equal probability when all three are ready satisfies

`4 E[T_R] <= N + 3 T* <= 5 T*`

on every finite forward-dependency program. The matching four-job lower bound
therefore makes the **global strict randomized minimax ratio exactly 5/4**
against complete inputs fixed before the policy's random choices. An allowed
additive constant would define a different competitive notion and is not
settled by this finite lower-bound pair.

## Independently checked prerequisites

The offline normalization argument selects the lexicographically least issue-
time vector among **all** optimum continuations, not only non-delay ones.
A ready job can be moved into an unused earlier slot using the augmented-DAG
semantics. If the oldest job is omitted at B=W+1, all W other entries issue,
then the unchanged window has only the oldest job unfinished next cycle.
Swapping that oldest job with a younger first-cycle job preserves the
completed set after two cycles and makes the time vector smaller. The swapped
second cycle may idle newly visible jobs; this does not invalidate the chosen
minimum because it ranges over all optimum continuations. This correctly
establishes the normalization needed by the exact scalar recurrence.

For the fair policy, the branch issuing the first and third jobs leaves the
middle job plus at most one incomplete new entry in the next window. There
is no concealed extra random choice inside that two-cycle macro-action.
After it, the completed state is again a clear prefix. The expected-value
recurrence therefore follows from conditioning on the fair first action,
without assuming that different macro-state visits are independent events.

The auxiliary bound `0 <= F_i-F_(i+1) <= 1` is valid at boundaries as well.
Deleting the first remaining job from an augmented-DAG schedule cannot create
an edge or a width collision among surviving jobs, proving the lower bound.
Issuing the oldest job alone and then following an optimum suffix proves
the upper bound. All these values are integers. A nonempty suffix has F>=1.

## Independent derivation of the joint induction

Use the author's notation `n_i=max(0,N-i+1)` and

`K_i=3F_i+n_i-4E_i`.

The needed statements are:

1. `K_i>=0`, including empty suffixes.
2. If the suffix at i is nonempty and `F_i=F_(i+1)`, then
   `K_i+K_(i+1)>=1`.

The nonempty hypothesis in (2) must be retained: two empty suffixes violate
its conclusion. For a forced action of cycle cost a deleting ell jobs,
`K_i=ell-a+K_(i+ell)`, with increments 0,1,1,2 for the four allowed macros.

When all three jobs are ready, put p=i+2, q=i+ell, and x=F_p-F_q.
Substitution, independently carried out from
`F_i=min(1+F_p,2+F_q)` and `E_i=(3+E_p+E_q)/2`, gives

| ell | x | Additive term in `K_i=(K_p+K_q)/2 + term` |
| --- | --- | --- |
| 3 | 0 | -1/2 |
| 3 | 1 | 1 |
| 4 | 0 or 2 | 0 |
| 4 | 1 | 3/2 |

This calculation includes the exact n_i difference; it is not the earlier,
insufficient `5F-4E` potential.

At each induction index first prove (1). Its only negative term is ell=3,
x=0. There p is nonempty, q=p+1, and the already proved later instance of
(2) gives `K_p+K_q>=1`. Then prove (2) at the current index. The forced
singleton contradicts its equality antecedent. Every other forced macro,
and every random case with x=1, already gives K_i>=1. The three remaining
cases are the substantive obligation.

Write a=i,b=i+1,c=i+2,d=i+3,e=i+4. All a,b,c exist and are initially ready.
Thus the true edges a->b,a->c,b->c are absent.

- **ell=3,x=0.** Here F_c=F_d, so d exists (otherwise nonempty c would have
  F_c=0). Therefore b->d is present. At the clear-prefix state b, only the
  younger c is ready, and the forced pair {b,c} gives `K_b=1+K_d>=1`.
  Current nonnegativity has already been proved, so `K_a+K_b>=1`.

- **ell=4,x=2.** Here d exists and b->d is absent. If c->d were absent,
  the feasible pair {c,d} would give `F_c<=1+F_e`, contrary to
  `F_c-F_e=2`. Thus c->d is present. Again the b state has just c as its
  ready younger job and `K_b=1+K_d>=1`. This is valid even when e is the
  empty terminal suffix; no operation at e is assumed to exist in this case.

- **ell=4,x=0.** Here F_c=F_e. If c->d exists, the preceding b-state
  argument applies. Otherwise {c,d} is a feasible one-cycle macro from c,
  with cost `1+F_e`, strictly above the optimum F_c. The exact recurrence
  forces the alternative {c,e} to be ready and optimal. Hence e exists,
  c->e and d->e are absent, and `2+F_u=F_e` for a target
  `u in {e+1,e+2}`. The adjacent difference bound forces u=e+2 and
  `F_e-F_(e+1)=F_(e+1)-F_(e+2)=1`. In particular e+1 is nonempty.
  Monotonicity between c and e gives F_d=F_e. At state b all b,c,d are
  ready; its {b,d} branch is followed by {c,e}, because c->e is absent.
  Its two tail targets are d and e+1, whose F difference is one. This is
  its ell=4,x=1 case, so `K_b>=3/2` by later-tail nonnegativity. Together
  with the already established K_a>=0 it proves the required adjacent sum.

The reasoning never identifies values belonging to different programs or
moves an edge assumption across inconsistent states. Its induction is not
circular: all tail uses have larger indices; current K_a>=0 is completed
before current statement (2); the final b-state formula uses only later
nonnegativity rather than assuming the desired b-state equality statement.

## Consequences and exact scope

At the initial state statement (1) gives the stronger bound
`4E <= N+3F`. The work bound N<=2F gives 5/4. If M is the number of double-
issue cycles, any non-idling complete execution has T=N-M. Empty cycles can
be removed in R1, so the maximum possible M equals N-F. Consequently the
stronger theorem is equivalently `E[M_R]>=3(N-F)/4`. This is an algebraic
pairing interpretation, not a proved reduction to a separately named graph-
matching problem.

The four-job lower bound is also properly quantified: a distribution putting
half its mass on each of two fixed programs bounds the chance of a two-cycle
finish by one half. At least one fixed input therefore has expectation at
least 5/2. The fair policy realizes equality on each member. No adaptive
inspection of realized random bits or future operand oracle is used.

Longer true edges are already imposed by the three-entry ROB's artificial
precedences. The proof nonetheless quantifies over arbitrary forward DAGs;
it is not restricted to fan-in-two graphs, the lower-bound pair, or bounded
program length. The graph order remains fixed. The reasoning would need
new arguments for a different retirement/admission convention, nonunit
latency, finite retirement bandwidth, or arbitrary buffer removal.

No large enumeration was repeated for this review. Earlier finite testing
motivated the conjecture but is not a premise of the accepted proof. A
separate Lean implementation of the joint induction, and literature checks
for equivalent randomized scheduling/pairing results, remain necessary before
any stronger verification or originality label is used.
