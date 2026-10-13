# Independent review: sharp non-delay loss at one excess ROB slot

Decision: ACCEPTED as a written theorem for all W>=2, B=W+1.
Reviewed ratio6 commits `ff328a8` and `6cb8b76`; exact source hashes accompany
this report. The result is a sharp restriction/embedding of the classical
Graham bound. No historical novelty or Lean verification is endorsed here.

## Mathematical review

For one empty-dependency program of length W², the youngest-ready policy
consumes each of W-1 consecutive groups of W+1 jobs in two cycles: the W
newer jobs, then the oldest one. One last job remains. Thus its exact makespan
is 2W-1 while the increasing consecutive W-job batches attain the work bound W.
This alone proves the strict multiplicative lower bound.

For the repeated construction, the proof needs genuine barriers: simply
concatenating independent blocks would lose the ratio asymptotically. The
proposed construction supplies them without additional instructions. With s
the next block start, the ROB supplies all predecessors through s-W-1 to its
first W+1 jobs. Their true parents are s-W+1,...,s-1. The only omitted previous
job, s-W, is a true predecessor of s-1 through the local special edge. These
three facts account for **every** job in the previous W²-job block. Later
new-block jobs have s as a window predecessor. Consequently all adjacent blocks
are strictly separated, under every legal schedule, not merely the witnesses.

The proposed W-cycle optimum swaps the two jobs straddling the final nominal
W-job batch boundary. Before the penultimate cycle its prefix is W²-2W;
job W²-W is the final admitted position in that W+1 window. Before the final
cycle its prefix is W²-W-1, whose window includes W²-1. The special parent
therefore precedes its target by one full cycle. The width is W in every cycle,
and cross-block parents completed earlier. This proves T*=qW by work equality.
The W=2 endpoint has zero ordinary prefix batches and satisfies the same proof.

For the poor schedule, every nonfinal pair of actions leaves the oldest job
unexecuted while completing all W newer jobs, making the next ready set a
singleton. The special target W²-1 is last, and its parent W²-W lies inside the
last W-job action. The barrier prevents any future-block job from entering a
ready set. Therefore the schedule is exactly the named causal youngest-ready
policy, not just some non-delay schedule. Its makespan is q(2W-1).

For fixed W and any rho<2-1/W, q(2W-1-rho W) is unbounded as q grows. This
excludes a fixed input-independent additive constant, even if that constant
may depend on W. At W=3 the maximum true fan-in is two; generally it is W-1.
The construction does not bound fan-out by two and does not prove fan-in-two
sharpness for arbitrary W.

The upper bound transfers the classical list-scheduling theorem to the exact
augmented DAG. An unfinished job outside the ROB has the oldest unfinished job
as an augmented predecessor; inside the ROB every window predecessor is already
completed. Hence the ready sets are identical. The usual work/chain argument
gives T<=N/W+(1-1/W)h and therefore T<=(2-1/W)T*, where h is augmented-DAG
height. This establishes the matching bound for every non-delay schedule.

## Independent checks and provenance

The reviewer did not call author search, family generator or operational replay.
`ratio_independent_audit.py` independently reconstructs dependencies and converts
them into a static augmented DAG. It validates the optimal time assignment
against every true/window edge and cycle width, computes ancestor closure to
verify every pair in adjacent-block separation, and runs youngest-ready by
searching the entire augmented graph. It then compares all actions against the
claimed arithmetic traces. This differs from the author's explicit window and
retirement replay.

The actual run checked 52 cases: W=2,...,14 and q in {1,2,3,5}, up to N=980.
It validated 893,802 cross-block ancestor pairs and 2,145 youngest-policy cycles.
Every optimum meets the work bound. The result is in
`evidence/ratio-independent.json` with script hash and duration. Reproduce with:

```
python workstreams/ILP1-20261014/subagents/review6/ratio_independent_audit.py
```

The claim that N=9 is the first violation of 3/2 at B4,W3 depends on the author's
299,595-graph exhaustive run through N=8. I inspected `search.py` and the saved
output. The effective-edge restriction is justified because every omitted
long edge is already an R1 window edge; the min/max recurrences use all legal
nonempty batches / all maximal-cardinality batches, respectively. I did not
repeat that enumeration and do not label its minimality claim independently
recomputed. The arbitrary-size tightness proof does not rely on minimality.

## Consequences and limits

The earlier universal conjecture that **every** non-delay B4,W3 schedule stays
within 3/2 is refuted, including its additive-constant version. The exact worst
non-delay factor is 5/3, and generally 2-1/W even when c=B-W=1. This describes
worst choices inside the policy class. It neither proves a lower bound against
all online policies nor changes the best-policy minimax question. In particular,
this construction does not establish that the specific eager lifted chunk
controller executes the bad schedule; that requires a separate policy replay.

## Addendum: oldest-inclusive tightness, ea93b64

ACCEPTED: at B4,W3 the worst-case factor remains 5/3 even for non-delay
schedules that include the oldest unfinished job at every cycle. The reviewed
`OLDEST_INCLUSIVE_TIGHTNESS.md` uses the R17 block with true edges
1→4, 2→4, 2→5, 5→8, and adds previous job8 as the sole cross-block parent
of the next four roots. Maximum true fan-in remains two.

The fixed policy chooses oldest then the two largest other ready indices.
Its five-cycle sequence is 023;1;467;5;8. Each singleton results from the
other admitted unfinished job being blocked (4 by1; 8 by5); in the last
cycle, the admitted next-block roots wait for8. Thus this specific execution
clears the block before repeating, giving5q. Separately, 012;345;678 per block
is legal, full-width and oldest-inclusive, proving optimum3q by the work bound.
The same unbounded-q inequality excludes every factor below5/3 with a fixed
additive constant. Neither offline lower bound nor policy induction requires
every possible schedule to respect a complete inter-block barrier.

This absence of a universal barrier is real. On two blocks the partial legal
trace 012;345;8;9 executes new-block job9 while old-block jobs6 and7 remain
unfinished. `oldest_independent_audit.py` independently verifies this negative
control, then runs its own augmented-DAG readiness policy for q=1,...,20 and50,
and independently checks the optimal traces. All42 full traces passed, with
1,300 poor-policy cycles and N up to450. No author simulation was imported.
Receipt and reproducible source are saved in this directory. The stronger
claim that oldest inclusion suffices for a ratio below5/3 is therefore refuted;
no claim against the best oldest-inclusive policy follows.
