# Independent review: finite-horizon completion corridor

Reviewer: independent verification subagent C. Scope: a written proof, a separately
written time-variable CSP, direct operational replay, and source inspection of
the primary `src/corridor.py`. Status: WRITTEN_PROOF and INDEPENDENTLY_REVIEWED;
this review does not claim Lean verification or confirmed originality.

## Statement and independent proof

Use zero-based instruction indices and a boundary after exactly `t` cycles.
Let `1<=W<=B`, `c=B-W`, and a proposed horizon `H` satisfy `S=WH-N>=0`.
A schedule completing in at most `H` cycles is padded by terminal empty actions.
Write `D_t` for its completed set, `r_t` for its completed-prefix length,
`d_t=tW-|D_t|` for used idle issue slots, and `h_t=|D_t|-r_t` for completed
instructions retained behind the first unfinished instruction. Then

\[
 [0,\max(0,tW-c-S))\subseteq D_t
 \subseteq[0,\min(N,tW+c)),\qquad
 tW-S\le |D_t|\le tW.
\]

First, `0<=d_t<=S`, since the schedule uses exactly `S` idle slots over its
entire padded horizon. For `t<H`, let the next action contain `W-delta` jobs.
The window contains at most `B-h_t` unfinished jobs. Therefore
`h_t<=c+delta`, while `d_t+delta=d_(t+1)<=S`, and hence
`r_t=tW-d_t-h_t>=tW-c-S`. At `t=H`, instead use completion directly:
`r_H=N=HW-S>=HW-c-S`. This avoids applying a nonexistent next-cycle bound
at the terminal boundary.

If job `j` completes during cycle `s<=t`, its admission required
`j<r_(s-1)+B`. Since `r_(s-1)<=|D_(s-1)|<=(s-1)W`, we obtain
`j<sW+c<=tW+c`. This proves the upper side of the corridor; cardinality
bounds are the definition of `d_t`. No non-delay assumption was used.

The variable strip has length at most `2c+S`, so there are at most
`2^(2c+S)` candidates per layer. The sharper uniform bound is

\[
 M(c,S)=\sum_{j=c}^{c+S}\binom{2c+S}{j}.
\]

To check boundary truncation, embed the actual strip into the untruncated
integer interval `[a,b)=[tW-c-S,tW+c)`. Positions below zero are fixed
completed and positions at least `N` are fixed unfinished. The number of
selected positions in this virtual interval is `|D_t|-a=c+S-d_t`, between
`c` and `c+S`. This injectively embeds actual candidates into the subsets
counted by `M`, including empty or truncated strips.

Enumerate candidate pairs in successive layers and retain exactly the actual
ROB transitions: the completed set grows, at most `W` new jobs are added,
each new job lies in the window determined by the old retired prefix, and
each true predecessor belongs to the old completed set. Empty additions are
allowed. The corridor bounds prove completeness; transition tests prove
soundness. The completed set is a sufficient state, so retaining one parent
per reached candidate loses no future solution. There are at most `M^2`
pairs per layer, giving `2^{O(c+S)} poly(N+E)` feasibility after the
`H>=N` serial shortcut. This is a parameterized finite-horizon result,
not an unrestricted polynomial-time optimal scheduling claim.

## Primary source inspection

Reviewed SHA-256 of `src/corridor.py`:

`98b28cbae3cff040a5f3ce3cc76fe4e8cf226de07c0c2977a6bc0e9308f0302a`.

The source computes precisely the fixed-prefix/variable-strip candidates,
then tests true ROB transitions using predecessor masks and the actual oldest
unfinished index. It does not enumerate every ready subset. The backtracking
parents preserve legal transitions, and removal of terminal empty actions is
safe. The candidate-count report agrees with a separately written subset
generator at each reported layer.

For a nonempty program, replacing `B` by `min(B,N)` and `W` by
`min(W,B,N)` preserves the operational model. The code recomputes `c,S`
after this normalization. Thus `W>B` and `B>N` do not introduce a negative
window excess. The empty program, zero horizon, insufficient total capacity,
and horizons at least `N` are explicitly handled. Forward-edge validation
precedes the serial shortcut. No correctness defect was found at the fixed
source hash.

## Actual independent verification

Run from this directory:

```sh
python corridor_audit.py --primary-module ../../src/corridor.py
```

The independent corridor implementation and time-assignment CSP share no
primary-solver calls. The former deliberately omits the `H>=N` shortcut,
so its small complete range also tests the strip construction with substantial
slack. A separate enumeration constructs every time map in the listed small
range, filters solely by direct ROB replay, and checks each boundary inequality.

- All forward DAGs with `0<=N<=4`, `1<=W<=4`, `0<=c<=2`, and `0<=H<=N`:
  4,332 independent CSP/corridor comparisons.
- All direct ROB legal time assignments for forward DAGs with `1<=N<=3`,
  `1<=W<=3`, `0<=c<=2`, and `1<=H<=4` with nonnegative slack: 2,050 legal
  assignments and 9,384 boundary checks. These include deliberate idle cycles;
  the checked inequalities include `h_t<=c+delta` before every actual next cycle.
- Seed `2026101409`: 298 valid indegree-at-most-two random instances from
  300 draws, with `1<=W<=8`, `0<=c<=3`, `0<=S<=3`, `1<=H<=6`, and `N=WH-S`.
- 99 additional empty-DAG positive cases with `2<=W<=12`, `0<=c,S<=2`, `H=4`.
- 68 resource-boundary cases covering `N=0`, `H=0`, `W>B`, `B>N`, `W=1`,
  `c=0`, serial shortcuts, and the dummy-padding counterexample below.
- Total primary/CSP comparisons: 4,797. Direct replay of all returned feasible
  primary traces: 1,921. All passed. The primary source hash was unchanged before
  and after the run. Actual elapsed time: 0.4095278849999886 seconds; exact
  finish time and source hashes are recorded in `corridor_results.json`.

The explicit padding counterexample has `B=4,W=3,N=5`, true edge `0->1`.
It finishes in two cycles as `{0,2,3}`, `{1,4}`. Appending a single independent
job changes `N` to six; two cycles become impossible. Therefore reduction to
the divisible-`N` full-throughput theorem by adding dummy jobs is invalid.

The finite tests support implementation correctness and independently exercise
the fragile boundary arguments. The arbitrary-size guarantee rests on the
written proof above, and is not inferred from the tested ranges.
