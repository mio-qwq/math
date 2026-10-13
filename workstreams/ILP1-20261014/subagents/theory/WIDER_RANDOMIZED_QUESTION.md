# Next randomized question: B=4, W=3

Current status: **REFUTED** for the uniform-omission policy.
`WIDER_POLICY_COUNTEREXAMPLE.md` gives a nine-job two-input graph
with optimum three and exact policy expectation `37/9`, hence ratio
`37/27>4/3`. The earlier search below remains a truthful record of
the computational support before that counterexample was found.
The width-two result in `RANDOMIZED_FIVE_QUARTERS.md` is proved; none
of its upper bounds are silently extended here.

## Candidate and evidence

For `B=W+1`, define the uniform-younger-omission policy to issue the
oldest unfinished job every cycle. If all `W+1` entries are ready,
omit one of the `W` younger entries uniformly. In every other state,
issue all ready jobs. The generalized oldest-inclusive normalization
theorem guarantees that an offline optimum can use actions of this
form, but choosing among them without future information can lose time.

At `B=4,W=3`, the hidden-cover family proves a global randomized lower
bound `4/3`, even with at most two true inputs per instruction. The
initial question was whether this particular uniform policy had the
matching global upper bound `E[T]<=4T*/3`. It does not.

`wider_policy_search.py` evaluates exact optimal values and exact
policy expectations with completed-set recursions. It searches all
effective true edges of gaps one through three: longer edges are
already imposed by the ROB. `WIDER_POLICY_SEARCH.json` records all
299,595 effective graphs with one through eight instructions, with
no ratio above `4/3`. Sizes five and six attain `4/3`. The run used
Python 3.12.14 and took 3.874363 seconds; the JSON records the exact
source hash. Fractions are computed exactly by scaled integer
recursion, not estimated by random schedule samples.

The current search is not an independent cross-check of every value;
it is a new proof-development instrument. Its completed-set optimal
routine permits every maximal ready action, while the policy's
expectation averages only oldest-inclusive actions. It stops and
cross-checks the optimum with the earlier generic solver if it finds
a counterexample. No counterexample was found in the declared range.

## A failed amortization shortcut

One tempting stronger assertion is

`E[T] <= T* + ((W-1)/W) floor(T*/2)`.

It is false already at width two: a six-job effective graph with
local mask 136 in `wider_policy_search.local_graph` has `T*=3` and
expected time `15/4`, exceeding the proposed `7/2`. At width three,
an eight-job graph with mask 32960 has `T*=3` and expected time `34/9`,
exceeding `11/3`. These are exact recursions, not statistical failures.
Thus regret cannot simply be charged to at most `floor(T*/2)`
independent bad decision epochs. The proven width-two joint potential
did not require that false assertion.

## Four-state structural reduction for a future proof

Under an oldest-inclusive non-delay policy at `B=4,W=3`, a state with
oldest unfinished job `i` can have completed jobs beyond the retired
prefix only at offsets one and two. Indeed, the previous oldest job
issued, so retirement advances by at least one; every job completed
in that cycle belonged to the previous four-entry window. No completed
job can remain at offset three in the refilled window.

There are therefore four state types: no completed later job; only
`i+1` completed; only `i+2` completed; or both completed. Only the
first type can have four ready unfinished jobs and make a random
choice. The other types have at most three unfinished window entries,
so non-delay uniquely determines their actions. This is a useful
specialization of the existing fixed-window exact state bound, not
a new general algorithmic complexity claim.

Unlike the width-two case, a two-cycle macro-action need not return
to a clear-prefix state. For example, if only `i+1` is completed and
the sole ready younger unfinished job is `i+3`, issuing `i,i+3`
produces the same state type at oldest `i+2`. A proof must account
for such repeated states; copying the earlier two-macro scalar
recurrence would be unsound.

The next useful step is a different policy that adapts to visible
information, or a lower-bound family excluding every `4/3` policy.
The counterexample rules out the uniform policy; the same note proves
that no fixed rank bias repairs a global `4/3` guarantee. The global
minimax ratio for fully adaptive policies remains unresolved here.
