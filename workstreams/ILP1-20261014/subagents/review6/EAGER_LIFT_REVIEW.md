# Independent review: causal non-delay policy lift

Decision: ACCEPTED as a written theorem for the stated ideal ROB and prefix
incoming-dependency observation interface. Reviewed theory commit
`2fc0fdeb4739dc6cfa7bc3bdd71bf0ae7ee71313`, especially `EAGER_POLICY_LIFT.md`
and the unchanged callback prototype. No Lean or historical novelty claim.

## Proof review

Completion inclusion implies monotonic retired prefix. After deleting already
real-completed jobs from a legal virtual batch, each remaining parent is real
completed and its index is below the enlarged real admission frontier. Its
unfinished status puts it above the real retirement frontier. Hence the retained
batch is actually ready, including in states with completed unretired holes.
Visibility also grows monotonically; virtual metadata queries are legal at the
real state. Extra filler observations are withheld from the virtual controller,
so its fixed random tape generates its original execution and distribution.

The induction is over virtual actions, not a synchronization of the two clocks.
An action with empty residual causes zero real cycles; a nonempty residual is
filled using pre-cycle readiness and causes one real cycle. Completion inclusion
is maintained in either case. No same-cycle chain bypass occurs. The finite
virtual-termination assumption excludes an endless sequence of skipped virtual
idles before a next meaningful action. If real completion happens first, aborting
virtual work is legal and improves the comparison. At N=0 no callback is needed.
Thus the time bound holds separately for every fixed completing random tape.
The expectation argument uses that same input-independent tape coupling; it
makes no claim against an adversary choosing the input after seeing real fillers.

The non-delay reduction is about policies permitted to remember and simulate
arbitrary histories with uncharged scheduling computation. It does not establish
finite-state or hardware-efficient optimal scheduling. The two-chain family
corollary follows because its reachable ready set has at most two elements,
and both paired chain jobs are admitted at distance B-1. This proves optimality
on that family only. It supplies no improvement of the universal coefficient.

## Independent implementation evidence

`eager_independent_audit.py` uses its own set-valued completion state, incoming
parent sets, first-missing retirement index, admission and ready-set checks.
Callbacks reject queries beyond the current real frontier, invalid or delayed
issue batches, and callbacks after actual completion. A second independent
implementation transforms the captured *unmodified* chunk plan into an expected
lift using sets and explicit before-cycle readiness. It compares every issued
batch, skipped-cycle count and makespan. It does not call the author's test.

The run covered all 76 forward labelled DAGs through N=4 at L=0,2,7;
240 seeded graphs of N=5,...,34 with up to four incoming edges; and 20 two-chain
family/lookahead cases. In total: 488 instances, 3,926 fixed offsets, 488
controlled-random-wrapper calls, 25,268 real cycles and 49,763 metadata queries.
All passed, including 1,795 skipped virtual cycles, 575 early virtual aborts and
1,433 strict improvements over the original chunk controller. All 160 tested
family offsets attain the chain optimum. The random wrapper was verified to
make exactly one draw from the documented offset range. Results, seed, Python
version, elapsed time and source hashes are in `evidence/eager-independent.json`.
These are finite implementation checks, not the arbitrary-policy proof.

Reproduce from the repository root:

```
python workstreams/ILP1-20261014/subagents/review6/eager_independent_audit.py
python workstreams/ILP1-20261014/subagents/review6/eager_counterexample.py
```

## Root-proposed negative control, independently reproduced

For N=5, B=4, W=3, L=0, and the sole true edge 3→4, offsets 1,2,3 yield
`[0,1,2]; [3]; [4]`, whereas offset 4 yields `[1,2,3]; [0]; [4]`.
All cost three cycles. The independent operational checker accepts
`[0,1,3]; [2,4]`, and the work lower bound ceil(5/3)=2 proves its optimum.
Thus the fixed prototype's expected ratio is 3/2 even with fan-in/out at most
one. The tempting claim that every offset starts with [0,1,2] is false.

This rules out pure multiplicative 4/3 or exact optimality for this specified
implementation. It is not a lower bound against all non-delay/lookahead policies,
and a single finite input gives no claim with an unrestricted additive constant.
Detailed traces are in `evidence/eager-five-job-counterexample.json`.
