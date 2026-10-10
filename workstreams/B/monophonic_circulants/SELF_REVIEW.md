# B self-review and reproduction

2026-10-10 10:43UTC. Role: discovering researcher self-checking; **independent review pending**.

The claim is a universal exclusion at the single admissible order15. It does not assert that either displayed graph alone refutes the existential conjecture. All possible undirected circulants are covered because all inverse pairs of nonzero residues are represented by seven bits. This covers all circulants under any cyclic labeling, including disconnected cases; the latter simply fail diameter2.

Original premise/violation checklist:
- Parameter15 is an integer and satisfies n>=11.
- Simple undirected circulants: represented exhaustively by S=-S, 0 notinS.
- Every graph with a triangle has mp>=3, independently of diameter.
- Every triangle-free option of degree<=4 misses an explicitly listed vertex within distance2, or has at most5 vertices reachable within two steps.
- The only remaining options have the explicit independent false-twin triple{0,5,10}, giving mp>=3 even though diameter2 holds.
- Hence NO graph meets the two demanded equalities simultaneously.

The proof is elementary and finite. The programs provide separately implemented arithmetic and graph-definition regressions, not logical substitutes for the coverage argument. Neither imports `probe_interval.py`, and neither requires SciPy or a solver.

Run from repository root, ordinary Python3 (tested3.12.14; standard library only):

    python workstreams/B/monophonic_circulants/verify_elementary.py
    python workstreams/B/monophonic_circulants/verify_order15.py

Actual10:43UTC outputs are the adjacent .log files. Arithmetic:128 masks,8 forbidden patterns,19 allowed sets,10 pair-sumset rows,2 survivors,1 rejected corrupted row. Graph:128 presentations,classification109/17/2,65534 induced vertex subsets,690 paths per survivor,2 controls. No random arithmetic or floating-point decisions are used.

Discovery history: interval family passed at11–14 with separately chosen small-case generators, failed at15 and at16; `interval_probe.json`, `interval_large_probe.json` preserve those restricted-family observations. `exception15_probe.json` records the inline discovery loop over generator subsets at15; that one-off caller was not separately persisted, so use the two independent self-contained verifiers rather than treating the JSON as a reproducible source program. The original finite n<=32 general-graph existence result is prior work, not our contribution.

Checks requiring external review: exact source interpretation; standard definition of circulant and exhaustive labeling; triangle/false-twin mp obstruction; elementary forbidden-pattern completeness and ten table rows. No new axiom, Lean formalization, independent acceptance, minimum-order proof, exact survivor mp-value, or historical-firstness claim. Own branch publication does not notify or imply acceptance by ROOT.
