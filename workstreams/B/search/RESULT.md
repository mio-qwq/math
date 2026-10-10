# Search result and stopping record

No counterexample found. All 95,165 recorded generated graphs were exactly solved SAT; every returned coloring was checked separately by breadth-first distances (the first batch was replayed for this check). Also checked every path on 1–100 vertices, every cycle on 3–100 vertices, and K2,3. No search timed out. This is bounded computational evidence only, not a proof of Conjecture 1.

## Exact coverage

- runs.jsonl: 4,376 total tests. Every square necklace with 1–7 square blocks and each cyclic joining path of length 2–5, modulo rotation of the length sequence. Also triangle-ended chains with 1–6 joining paths from 2–5 using only rotation-minimal length tuples; those chain tuples are an intentionally recorded subset, not complete chain coverage. Maximum graph order 56; maximum search nodes 1,584.
- endpoints.jsonl: 88,350 tests. Chains with 1–6 joining paths (0–5 interior opposite-terminal squares), path lengths independently 2–6, and each endpoint independently triangle, one-terminal square, or leaf. Isomorphic endpoint-order reversal removed by choosing the six unordered endpoint-type pairs; length-tuple reversal removed only for equal endpoint types. Maximum graph order 58; maximum search nodes 14,134.
- leaves.jsonl: 2,439 additional tests. Chains with 1–5 joining paths, non-leaf-end lengths 2–6, leaf-end lengths 1–6, and at least one leaf-end path of length 1. Endpoint pairs triangle/leaf, square/leaf, leaf/leaf, with reversal normalization for equal endpoint types. Maximum graph order 41; maximum search nodes 611.

Every generated graph was checked for maximum degree ≤3, independence of degree-3 vertices, and a triangle or square through every degree-3 vertex. The solver uses complete MRV domain backtracking with distance-conflict propagation. Its timeout mode never reports UNSAT. No UNSAT candidate adjacency was written because none exists in these runs. example.json contains the adjacency and verified coloring of K2,3 as a positive sanity example.

## Reproduction

commands.log records the three actual executed Python run commands. search.py implements the solver and initial batch; endpoints.py runs endpoint variants; verify_and_leaves.py runs leaf-boundary variants, replays the initial batch with witness checks, and checks exceptional components. stdout.log, endpoints-stdout.log, and verify-stdout.log preserve run summaries. Raw per-instance records are in the three JSONL files.

## Paused route

This search is paused after the above finite complete sweeps. STRUCTURE.md gives a short structural reduction sketch to necklaces/chains plus elementary exceptions. Do not resume with more random repetitions merely because no obstruction appeared. Restore this route only if (a) a structural gap produces a genuinely new admissible graph family, (b) a literature review leaves an unresolved specific chain/necklace case with a concrete obstruction hypothesis, or (c) an arbitrary-length transfer-state proof is explicitly commissioned. A proof-oriented restart should first check existing packing-coloring results for square chains and necklaces, then target finite-state extension rules instead of increasing brute-force graph sizes.
