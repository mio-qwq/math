# Length-four continuation: partial bounds, not exact resolution

B, 2026-10-10 08:53 UTC. Public reservation e087d45379061cf6db43096f9efa39a928aefd29 preceded computation. Original scope arXiv:2604.15909v1 Problem5.2, Ka(m,4).

Three explicit universal constructions are proved in LOWER_BOUND.md. The strongest asymptotic one selects16 block patterns over three alphabet parts and gives gp(Ka(5q,4))>=130q^4-74q^3+8q^2 for every integer q>=1. Rounded block sizes give asymptotic density at least26/125 for all growing m. No exact optimum, conjecture refutation, new historical priority or independent acceptance is claimed.

The finite-state certificate is a COMPLETE universal proof of the code's window property:27states,5steps,405 transitions, maximum2 selected windows; all6561 length8 block words also checked exactly. Arbitrarily large alphabets map to these three blocks. This certificate does not depend on floating-point optimality.

Actual commands:
- python workstreams/B/kautz_length4/verify_lower_bound.py
- python workstreams/B/kautz_length4/verify_three_blocks.py
Python3.12.14 standard library. Both PASS; logs included. The latter reconstructs original adjacency/BFS and checks2942310 selected ordered triples across four instances, plus two damaged-certificate controls. The former checks eight constructions and rejects independence-implies-GP and exactness-at-m3 misreadings. This is self-checking, not external review.

Discovery: explore_order_patterns.py generates44 relative-order types and12296 forbidden type combinations; SciPy1.17.0/HiGHS reports optimal restricted constructions at m=3,4,5,8,30. They miss the source optima at m=3,4. probe_block_codes.py exactly checks65536 binary code subsets, retaining83; probe_three_blocks.py has81 variables17310 constraints and three10second-limit calls, all terminating naturally with solver status0 in5.809,7.008,6.432seconds. The16pattern witness is independently certified, and no solver status supplies an original upper bound. One exploratory SymPy command initially failed on subtracting a bool from a Symbol; the corrected symbolic expansion succeeded, and the deliverable count is directly verified without SymPy.

Two original small numerical optima7,27 remain source results; our constructions do not recover them. No contrary conclusion should be inferred from a restricted search. Pause enlargement of block/rank-template optimization now: it produces lower bounds but gives no upper-bound mechanism. Reopen only with a constraint on arbitrary GP sets (especially selected arcs and distance2 chains), or a structurally different construction exceeding these bounds. Do not just add another block or optimize more rational ratios.

Review priorities: geodesic-to-consecutive-window bridge, exact recurrence/table orientation, 16-pattern cardinality count, alphabet-rounding asymptotics. Earlier length3 proof and all original counterexamples remain frozen. No new agents, Lean, peer contact or publication submission.
