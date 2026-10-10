# Complete-graph edge-order constructor — exact GitHub-source replay

Agent A, 2026-10-10. This receipt is for a **new software/corollary package**, not the original frozen full Conjecture 10 proof. It is not a Lean formalization, historical novelty confirmation, or independent ROOT acceptance of the new software.

## Exact source at \`partner/dist-A\`

| Path (under workstreams/A/code/) | Exact Git blob SHA |
| --- | --- |
| \`construct_full_graph.py\` | \`b0da98d468428cb81063e31b57f02f9f290d59ab\` |
| \`verify_full_graph.py\` | \`8c712181eda1a6641c3bf8efeab7a2dc5a99ef60\` |
| \`verify_all_regular.py\` (existing frozen dependency, unchanged) | \`dfd147219f4fb016e945daabfffea9bbe419919d\` |

All three files in the portable packet were confirmed by \`git hash-object\` to exactly match these remote Git blob values. The two newly uploaded files are the actual versions rerun here; no old prototype stdout is misattributed to an untested GitHub refactor.

## Fresh-directory actual replay

Working environment: Python 3.13.5, Linux, standard library only, no network access. Extract \`agent_A_full_graph_replay.zip\` into a new temporary directory, then from the extracted root:

    python3 workstreams/A/code/verify_full_graph.py

Actual output, exit code 0:

    PASS 25204 tested graph/colouring inputs: {'valid_order': 24070, 'correct_obstruction': 1134} negative input controls: 5

These 25,204 are **tested input/colouring runs**, not distinct nonisomorphic graphs and not a universal proof. The regression reconstructs each resulting ordered incident-colour list from scratch, checking every original edge. It also independently recognizes the original problem's exceptional structures and deliberately malformed inputs. It covers *all* simple graphs on <=5 labelled vertices under two deterministic proper colourings per graph, and uses a fixed-seed bounded sample for n>=6. The genuine general theorem follows from the reviewed regular written proof plus the original authors' Theorem 5, **not** from the sample.

Exact sample:

    echo '{"n":4,"edges":[[0,1,0],[1,2,1],[2,3,0],[0,3,2]]}' | python3 workstreams/A/code/construct_full_graph.py

Actual output, exit code 0:

    {"order":[[0,1,0],[0,3,2],[1,2,1],[2,3,0]],"verified":true,"components":[{"size":4,"method":"source_distinct_palette"}]}

All results above were rerun inside the *fresh extracted* package. The ZIP was independently recreated locally, 8,588 bytes, SHA256 \`3a6a4bb64e86a13f81ca6d6d7ee2f34d95137daf640c168d659f637a1f82c284\`. It is an attachable conversation artifact; it was **not** claimed to be a signed GitHub Release.

## Mathematical scope

\`paper/FULL_GRAPH_ALGORITHM.md\` gives the exact disconnected classification and attribution. A finite simple graph with a fixed proper edge colouring has a successful **single global** edge order iff no connected component is \`K2\` or a properly **two-coloured even cycle**. Singleton isolated vertices are allowed. If all adjacent palettes agree, use A's already independently mathematically accepted regular theorem; if some adjacent palettes differ, use the ORIGINAL AUTHORS' published constructive Theorem 5. Process connected components separately, then concatenate the orders. No recolouring is allowed. The local nonregular routine uses their greedy construction, not a newly discovered source theorem.

## Review boundaries and next work

The original proof freeze \`7168f6df66ba5518cd3420c4668eab5352e4be8c\` is unaffected; the coordinator's 2026-10-10 card records a written mathematical PASS for that exact version and a separate execution HOLD. The separate v2 repaired execution packet is in \`reviews/EXECUTION_REPLAY_V2.md\`; this new complete-graph code is an **additional** file set, not a substitute for resolving that HOLD.

Independent ROOT software replay and Lean formal verification remain future steps. No unsigned GitHub API commit is represented as a signed immutable publication. No PR, merge, external author contact, submission, scheduler, or priority claim.
