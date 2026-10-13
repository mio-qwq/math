# ILP1 recovery checkpoint

Use the live branch head, not an assumed future SHA:

```sh
git fetch origin
git switch partner/dist-ILP1-20261014
git status --short
git log -5 --oneline
git rev-parse HEAD
```

Baseline actually fetched: `bf732c32f1b8cef32ebf69cac6fb232a8a5323a3`. This file is first created in the initial ILP1 commit; its containing commit is obtained using `git log -1 --format=%H -- workstreams/ILP1-20261014/HANDOFF.md`.

Primary checkout: `/workspace/scratch/6a1539b44ef3/math-ilp1`. Independent worktrees: `ilp1-theory`, `ilp1-lean`, `ilp1-verification`, `ilp1-literature` under the same scratch parent. Their branches are `partner/ilp1-<role>-20261014` and their commits are integrated only after review. Preserve unfinished files and check live tasks before resuming.

Strongest current written base: eager ROB feasibility exactly equals unit-job precedence scheduling after adding every edge i->j with i+B<=j. Proof in THEOREMS.md. Completed jobs blocked behind an earlier index retain slots. Do not replace full prefix edges with only offset edges.

Verified counterexamples: oldest-ready suboptimal at N4,B3,W2,E={(2,3)}; online indistinguishable pair uses parent1 vs parent2 of job3. Saturation thresholds both nonmonotone at N4,E={(1,3),(2,3)}. Source tests reproduce them.

Next commands from workstream:

```sh
python -m unittest discover -s tests -v
python tests/exhaustive.py --max-n 5 --random 100 --seed 20261014 --output evidence/exhaustive.json
```

Do not rerun the exhaustive audit merely because a new session starts; compare hashes and reuse evidence if unchanged.

Next meaningful work: independently integrate/review the time-assignment solver and formal model; verify the general online dichotomy (a universally optimal deterministic policy exists iff W=1 or W>=B), then the binomial-family randomized lower bound. Current core challenge is a structural optimum/certificate or saturation algorithm beyond the full-state DP. Literature has already located important prior ROB-edge models, so the reduction alone must not be labeled a new discovery.

Runtime notes: Python3.12.14 available. No Lean was on PATH at startup; Lean subagent installed pinned4.34.1 under sibling `ilp1-tools/` and is documenting a current-process executable-location compatibility wrapper. Before accepting formal status, read its exact source, run actual compilation and audit axioms.
