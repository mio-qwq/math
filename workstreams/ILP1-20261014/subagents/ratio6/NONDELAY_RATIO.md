# A sharp 5/3 non-delay bound at B=4, W=3

Authoring role: ratio6, independent counterexample search. Base commit
`6b36144046a7a5325706b54673d38b24bf4046fa` was inspected and `git fetch origin`
actually completed before editing. Only this subdirectory is owned here.

## Status and exact claim

The proposed universal inequality `T_ND <= (3/2) T*` is **REFUTED**.
The stronger assertion allowing any fixed additive constant is also false.
For R1 with B=4 and W=3, the supremum over finite programs and non-delay
schedules of `T_ND/T*` is exactly **5/3**. The lower bound already holds
for the single deterministic, causal policy that always issues the three
largest ready indices (or all ready indices if fewer than three).
Programs in the repeated lower-bound family have at most two true input
parents per operation.

The lower bound has a complete written proof below and independent finite
set-based replay evidence. No Lean proof has been produced here. The upper
bound is the already attributed classical Graham list-scheduling theorem,
transferred through R1 augmented precedence equivalence. **No originality
claim:** this is a sharp restriction/embedding of a classical bound; its exact
prior appearance under the occupied ROB window still requires literature audit.
Independent mathematical review by another role is pending at this commit.

This is a worst-case statement about all non-delay policies and a particular
poor policy. It does **not** prove a 5/3 lower bound for every online policy or
identify the optimal online minimax ratio.

## Smallest strict counterexample

Take N=9 and E empty. The three-cycle schedule

    {0,1,2}; {3,4,5}; {6,7,8}

is legal, and the work bound N/W=3 proves optimality. The five-cycle schedule

    {1,2,3}; {0}; {5,6,7}; {4}; {8}

is non-delay: its ready sets are respectively `{0,1,2,3}`, `{0}`,
`{4,5,6,7}`, `{4}`, `{8}`. Completed instructions remain in the ROB until
the omitted oldest one retires. Thus the ratio is 5/3.

All effective graphs on N<=8 were exhaustively checked by `search.py`:
299,595 graphs, with graph counts 1,2,8,64,512,4096,32768,262144.
There was no strict counterexample before N=9. This makes the example minimal
in N within R1, and its zero true edges are automatically minimal as well.
This minimality statement relies on finite exhaustive computation, not Lean.

Why these graphs cover all forward true dependencies: every true edge i->j
with j-i>=4 is already forced by the ROB rule. It cannot change any legal
schedule or any reachable ready set. Hence only the edges with 1<=j-i<=3
need enumeration. The min DP permits every nonempty legal action; the max DP
permits exactly actions of size min(3, number of ready jobs). Idle actions
cannot help an optimum and are never non-delay in a nonterminal R1 state.
Both recurrences increase the completed set and thus terminate.

## A repeated two-input family: the additive constant cannot help

For any q>=1, partition N=9q jobs into blocks of nine. In block b (starting
at s=9b), add the local edge `(s+6)->(s+8)`. For b>=1, each of its first
four jobs s,s+1,s+2,s+3 has the two parents `s-2` and `s-1`, the previous
block's local jobs 7 and 8. There are no other true edges.

**Separation lemma.** Every job of a block must execute strictly after all
jobs in the preceding block. For a first-four job j in a new block, its
window predecessors contain every previous job through s-4 (local 5), since
j>=s and B=4. Its true parents include local 7 and 8. The previous local 6
precedes local 8. Thus all nine previous jobs precede j. Any later job of the
new block has its first job s as a window predecessor, so the assertion
extends to the entire new block. This uses strict unit-cycle precedence.

A three-cycle schedule for each block, offset by s, is

    {0,1,2}; {3,4,6}; {5,7,8}.

The second action lies in the window [3,7); the last action lies in [5,9),
and job 8's parent 6 completed in the previous cycle. At later blocks the
extra parents completed before the block starts. Concatenating gives a legal
3q-cycle schedule; N/W=3q proves `T*=3q` without an exponential search.

The largest-ready-index policy instead executes each block as

    {1,2,3}; {0}; {5,6,7}; {4}; {8}.

The separation lemma prevents a future block from contributing a ready job
before the current one finishes. The only local true edge 6->8 is satisfied
by the displayed trace. Each action is precisely the three largest ready
indices, or all of them when fewer than three exist. Consequently this one
policy takes exactly `5q` cycles. The claimed 3/2 bound with additive constant
alpha would require `5q <= (9/2)q + alpha`, impossible for q>2alpha.
Indeed no factor rho<5/3 can hold with a fixed input-independent alpha.

All jobs have true fan-in at most two. The outgoing degree is not limited to
two: the preceding block's final jobs each feed four new roots. This family
does not claim simultaneous fan-in/fan-out-two tightness.

## Matching upper bound and scope

For every completed state, an unexecuted job beyond the ROB is blocked in the
augmented DAG by the oldest uncompleted job. Inside the ROB, all augmented
window predecessors are already complete, so readiness matches true-parent
readiness. Thus R1 non-delay schedules are ordinary non-delay/list schedules
of the augmented DAG on three identical unit-time machines.

Graham's bound is `T <= (2-1/3)T* = (5/3)T*`; see the already audited
`../../LITERATURE.md` and R9 in `../../THEOREMS.md` (the numbered section may
be found by searching for Graham). The repeated family proves this constant
cannot improve even under B=4 and true fan-in two. This tightness has no
implication that selecting the *best* non-delay schedule is difficult: the
existing B=W+1 polynomial optimization result remains valid.

## Reproducibility and next question

Python 3.12.14, standard library only. Run from this directory:

    python search.py --max-n 8
    python random_audit.py
    python replay.py

`search8-results.txt` records the exhaustive range and elapsed 16.0267 seconds.
The first run through N=7 is retained separately, not added to the total.
`random-results.json` records seed 2026101406 and discovery at zero-based
case 252; it stopped immediately upon refutation, rather than completing the
planned 10,000 samples. `replay-results.json` contains independent explicit
ROB admission/retirement checks for q=1..100, 200 family schedules, and source
hashes. The family work lower bound certifies each displayed optimum. Its
worst trace is checked for the specific largest-index policy, not merely
maximum action cardinality. Finite q checks supplement the arbitrary-q proof.

The useful replacement question concerns *which* causal non-delay policies
achieve factors below 5/3. Non-delay normalization alone cannot establish
3/2. Any improved guarantee must exploit the choice at a full-ready clear
prefix. A separate question is simultaneous fan-in/out-two repeated tightness.
