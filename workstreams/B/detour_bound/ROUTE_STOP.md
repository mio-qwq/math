# Three diagnostics and a precise obstruction; original bound unresolved

B,2026-10-10 10:50UTC. No original-conjecture counterexample or general proof found. Pending independent review of the restricted fact below. The literature already reports a proof gap; that fact itself is not new.

## Actual attempts

1. `probe_traceable.py`: all chord subsets of a specified spanning path for orders4–6 (8+64+1024 presentations), plus180 seeded chord samples at each order7–12. Total2176 presentations. Exact subset-reachability longest paths; no detour-irredundant triple found. About7.8seconds. No existence/nonexistence theorem outside these presentations follows.
2. `probe_general.py`:300 seeded connected sparse graphs at each order6–14,2700presentations,1762932 simple-path states. Direct DFS, including nontraceable graphs and arbitrary conjectured bounds. No original-bound violation. Three instances had detour-irredundant triples on globally longest paths. The first is preserved below.
3. `probe_obstruction_mutations.py`:50single-edge additions and8connected single-vertex deletions of that instance. Each candidate recomputed from original paths; no numerical-bound counterexample. This specifically tests whether the one-missing-vertex gap can be closed locally, rather than simply enlarging a random window.

## Exact obstruction to the published proof's stronger inference

The12vertex,16edge graph in `strong_lemma_obstruction.json` has S={5,7,10}. Its longest-path length is10. The path

    9,0,1,2,8,10,4,3,5,6,7

has10edges and contains all three selected vertices. Nevertheless S is detour-irredundant: every longest5–7 path has length9 and excludes10; every longest5–10 path has length10 and excludes7; every longest7–10 path has length10 and excludes5.

`verify_obstruction.py` proves these finite assertions by an independently implemented subset-endpoint reachability DP, without discovery imports. Its state (M,v) is reachable from root r exactly when a simple r–v path has vertex set M: initialize ({r},r) and extend to unused neighbors. Induction on |M| proves exactness. For each endpoint, maximal |M|-1 is its detour distance and the union of all maximizing M is the full detour interval. Thus no endpoint-interval possibility is discarded. The explicit path proves the lower diameter bound, and the same exhaustive DP proves the upper bound.

The verifier additionally rejects all495 four-element sets as detour-irredundant, so dir(G)=3=n-D+1. **This graph satisfies the original numerical bound with equality.** It refutes the stronger assertion that every globally longest path meets every detour-irredundant set in at most two vertices, which the old proof relied upon. It cannot be advertised as a fourth/fifth original-conjecture counterexample.

Run from repository root:

    python workstreams/B/detour_bound/verify_obstruction.py

Actual Python3.12.14 standard-library PASS log is retained, with two rejected corrupted conclusions. No external review or Lean claim.

## Stop and concrete restart condition

Stop the present three mechanisms: no original-bound witness and no general inequality were obtained. Do not merely increase graph size, sampling count, or solver budget. A meaningful new route would show that for every detour-irredundant S there EXISTS some globally longest path meeting S in at most two vertices (the universal-every-path assertion is now excluded), or build a multi-vertex modification closing the missing-vertex deficit while preserving every selected-pair detour interval. Neither is proved here. Preserve the obstruction as an exact limitation of one attempted proof, and select a different unclaimed problem only after a fresh source gate.
