# Independent verification — ILP1-20261014

Baseline: `bf732c32f1b8cef32ebf69cac6fb232a8a5323a3`.
Branch: `partner/ilp1-verification-20261014`.
Owned path: this directory only. The main research branch integrates these files.

## Independent algorithm

`constraint_solver.py` solves a finite-horizon constraint problem whose variables
are execution times. For zero-based jobs, it adds every precedence `i -> j` with
`j - i >= B`, then tries horizons in increasing order. Job times are assigned in
program order with predecessor lower bounds, successor-depth upper bounds, and
per-cycle capacity counters. This implementation does not import or invoke the
primary completed-set dynamic program.

For a fixed horizon the search is complete: every predecessor of job `j` has an
earlier program index, every feasible time lies in the searched interval, and
branching only excludes full cycles. A successor-depth upper bound excludes only
times from which a required chain cannot finish. Trying all horizons from a valid
lower bound through `N` therefore returns an optimum, conditional on the reviewed
ROB/precedence equivalence. Direct ROB replay independently checks every returned
schedule. This is a classical exact-search baseline, not a novelty claim.

API: `solve(n, edges, B, W) -> (optimum, schedule)`. Jobs and cycles are zero-based.
The empty program has duration zero. `B` and `W` must be positive integers.

## Reproduction

Python 3, standard library only. From this directory:

```sh
python run_audit.py --output verification_results.json
python extended_audit.py --primary-directory ../../src --output extended_results.json
python online_audit.py --output online_results.json
python sharpened_chain_audit.py
python followup_audit.py --primary-directory ../../src
python saturation_drop_audit.py
python approximate_saturation_audit.py
python one_slot_oldest_audit.py
python randomized_bound_audit.py
python window_plus_one_family_audit.py
python hidden_subset_audit.py
python wider_policy_independent.py
python repeated_pair_audit.py
```

The optional `--primary-directory` cross-check imports the separately written
primary solver/checker in the audit driver only. It never changes the independent
solver implementation. The report records the exact primary source hashes used.

## Evidence

- `verification_results.json`: exhaustive ROB/assignment equivalence checks for
  every forward DAG with `1 <= N <= 4`, all `1 <= B,W <= N`, and every time map
  into `0..N-1`; 264,121 comparisons, 1,105 exact-optimum cross-checks. Also 660
  boundary cases; all 683 indegree-at-most-two DAGs with `N <= 5` and 16,377 resource
  combinations for greedy checks; 3,000 fixed-seed random instances.
- `extended_results.json`: 17,378 independent-primary optimum comparisons and
  Bellman-certificate replays, saturation-threshold counterexamples, augmented
  critical-path failure, online prefix families, and block lower-bound examples.
- `online_results.json`: 98 binomial-family programs with 36,426 full-first-action
  checks, plus 112 chain-family programs with 11,036 first-action checks including
  empty and underfull actions.
- `sharpened_chain_results.json`: 240 shortened-chain programs for every
  `3<=B<=10, 2<=W<B`; 75,352 first-action checks, explicit witness replay, and
  60,506 adverse actions excluded at the claimed optimum.
- `REVIEW.md`: written independent proof audit, exact witnesses, and scope limits.
- `FOLLOWUP_REVIEW.md` and `followup_results.json`: exact chain-family randomized
  minimax/advice verification (40,830 policy and 440 advice replays), 350 independent
  saturation checks, 24 rejected certificate tampers, and source-level review of
  the Lean operational bridge. The latter is semantic inspection, not an extra
  compilation run.
- `SATURATION_REVIEW.md` and `saturation_drop_results.json`: independently
  accepted written proofs and exact checks of the fixed-width window drop
  `B_sat(2)=2K` versus `B_sat(3)=3`, plus the depth-two family with an exact
  issue-width saturation curve. Nine layered and 25 depth-two programs were
  checked, with 216 and 5,720 resource decisions respectively.
- `APPROXIMATE_SATURATION_REVIEW.md` and `approximate_saturation_results.json`:
  the serial-prefix/independent-suffix exact makespan and general-width
  approximation threshold, with complete independent proofs, 2,020 exact
  optimum/replay checks, and 1,185 approximation-threshold checks.
- `ONE_SLOT_OLDEST_REVIEW.md` and `one_slot_oldest_results.json`: the fixed-positive-
  tolerance one-slot width corollary (420 rational boundary checks), plus the
  lexicographic proof of oldest-inclusive optimal schedules at `B=W+1`
  (225 exhaustive small cases, 200 seeded cases, and an outside-domain negative
  control).
- `RANDOMIZED_BOUND_REVIEW.md` and `randomized_bound_results.json`: independent
  arbitrary-size review of the sharp `5/4` randomized online bound at `B=3,W=2`,
  using a joint potential invariant. The new invariants and fragile local
  implications were also checked on 684 effective graphs including the empty
  graph, using time-variable CSP optima and direct ROB policy expectations.
- `WINDOW_PLUS_ONE_FAMILY_REVIEW.md` and `window_plus_one_family_results.json`:
  exact hidden-omission family ratio at `B=W+1`, including matching graphs with
  randomized lower bounds approaching `3/2`; 77 programs, 10,675 first-action
  checks, and 419 direct policy replays.
- The same review's hidden-subset extension and `hidden_subset_results.json`:
  selected new `B>W+1` cases, with 51 programs, 1,927 first-action checks,
  and 761 policy replays.
- `WIDER_POLICY_COUNTEREXAMPLE_REVIEW.md` and `wider_policy_independent_results.json`:
  a nine-job `B=4,W=3` counterexample with exact expected ratio `37/27>4/3`,
  independently checked by CSP and its complete nine-leaf ROB probability tree.
  The report also preserves the earlier finite random support and failed potential.
- `REPEATED_PAIR_REVIEW.md` and `repeated_pair_results.json`: independent proof
  review of the barrier-separated family that makes the `5/4` randomized and
  `3/2` deterministic lower bounds robust to additive constants; 127 bit-string
  programs and an exact six-block probability tree.

All finite checks passed. These reports do not constitute arbitrary-size Lean
proofs. This subagent has not run Lean or made originality claims.
