# ILP1 recovery checkpoint

## Branch and baseline

Primary checkout: `/workspace/scratch/6a1539b44ef3/math-ilp1`.
Exclusive branch: `partner/dist-ILP1-20261014`.
Exclusive files: this workstream and `coordination/agents/ILP1-20261014.md`.
Actually fetched baseline: `bf732c32f1b8cef32ebf69cac6fb232a8a5323a3`.
Last remote SHA verified before this integration: `4379581865cb3c7cf81ccd6397ade07faa9bbff4`.
Live current SHA and file-containing commit must be read with git; never invent a future publication hash.

```sh
git fetch origin
git status --short
git log -6 --oneline
git rev-parse HEAD
git ls-remote origin refs/heads/partner/dist-ILP1-20261014
git log -1 --format=%H -- workstreams/ILP1-20261014/HANDOFF.md
```

Do not switch away from dirty work or reset it. Other researcher checkout `/workspace/scratch/b1d6bae025af/math-crypto3` had uncommitted changes at startup and was not touched. Never modify main/shared roadmaps/publication006/other agent states.

Independent worktrees are sibling `ilp1-theory`, `ilp1-lean`, `ilp1-verification`, `ilp1-literature`, `ilp1-formal-dp`. Their branches are `partner/ilp1-<role>-20261014` (formal role uses formal-dp). Check actual subagent status before repeating work. They own disjoint role paths; Lean owns formal/. Cherry-pick reviewed commits only.

## Strongest verified state

* R1 eager ROB is exactly precedence scheduling with ALL prefix edges i->j for i+B<=j. General operational equivalence and optimum existence are Lean verified. Offset-only edges are false.
* A separate executable Lean time/lane enumeration returns an actual globally optimal legal schedule for arbitrary forward Boolean DAGs and positive resources, including empty programs. Python is not formally verified.
* Fixed-schedule footprint beta=max({1} union {j-i+1:i<j,t_i>=t_j}) is Lean verified, including maximum attainment and minimum-window interpretation.
* Positive resource cap min(B,W), full-window identities, general Bellman lower certificates and attaining-potential principles are formally checked. Generic finite-search interfaces are explicitly distinguished from the concrete enumerator.
* Written and independently reviewed online classification: universal optimum iff W1 or W>=B. General randomized/advice formulas are not fully Lean verified. Global strict deterministic ratio at B3,W2 is3/2; randomized global ratio remains in[5/4,3/2].
* Layered two-input family has B_sat(width2)=N, B_sat(width3)=3; small-window width2 penalty is only one cycle. Do not imply huge IPC benefit.
* Chain-prefix plus independent suffix: T=K+ceil(max(0,K-B+1)/min(B,W)) for W>=2; B_epsilon=max(ceil((K+1)/(q+1)),K+1-qW),q=floor(epsilonK). Fixed epsilon<1/W can require Omega(N) window. True indegree/outdegree<=1. New family results are reviewed written proofs, not Lean proofs or novelty claims.

## Evidence and exact commands

Lean installed at `/workspace/scratch/6a1539b44ef3/ilp1-tools/lean-4.34.1-linux/bin/lean`, version4.34.1 (Std only). Runners compile fresh objects and audit actual declarations; the included C shim only resolves this host's current-process executable-path restriction. Root logs cover106 distinct endpoints with standard axioms only.

From repository root:

```sh
python workstreams/ILP1-20261014/formal/verify.py --lean /workspace/scratch/6a1539b44ef3/ilp1-tools/lean-4.34.1-linux/bin/lean --proc-self-compat --output /tmp/ilp1-lean-check
python workstreams/ILP1-20261014/formal/verify_footprint.py --lean /workspace/scratch/6a1539b44ef3/ilp1-tools/lean-4.34.1-linux/bin/lean --proc-self-compat --output /tmp/ilp1-footprint-check
python workstreams/ILP1-20261014/subagents/formal-dp/verify.py --lean /workspace/scratch/6a1539b44ef3/ilp1-tools/lean-4.34.1-linux/bin/lean --proc-self-compat --output /tmp/ilp1-bellman-check
```

From workstream:

```sh
python -m unittest discover -s tests -v
python paper/build.py
```

Do not rerun unchanged exhaustive audits after session recovery. Source hashes/timings/seeds are in evidence and each verification JSON. Root12 unit groups, independent17378 solver cases, layered216, depth-two5720, chain-prefix2020+1185 checks already passed.

## Failed routes and caveats

Oldest-ready and both original/augmented critical-path priorities are not universally optimal; minimal witnesses are saved. Height and work lower bounds need not be jointly attainable. Both resource saturation thresholds can decrease with unchanged target duration. Arbitrary true edges do not preserve a window-only interval-order graph class. An ASAP true-dependency schedule need not minimize its optimal window. Finite online gadgets do not imply lower bounds allowing an additive constant. Resource statements depend on the fixed topological program order, not only an unlabeled DAG.

## Publication and recovery mechanics

Git HTTPS transport fetch succeeds but push reports missing username. The authorized GitHub connector successfully created/published the first checkpoint. Subsequent publication uses create_tree/create_commit/update_ref with expected current SHA and force=false, followed by actual git fetch/ls-remote and tree equality. Local integration commits may have different hashes from connector commits; preserve them on a unique local branch before recreating the clean tracking branch. Never force push or discard dirty changes. The first local-only baseline is preserved under partner/ilp1-local-baseline-20261014.

The enabled2h automation belongs to this conversation; do not alter other automations. It must perform recovery/research, not claim uninterrupted background execution.

Oldest-inclusion normalization for B=W+1 is now proved and independently reviewed (THEOREMS R14); the B3,W2 scalar recurrence is in NARROW_WINDOW_POLICY.md. Next substantive target: the global randomized B3,W2 gap, using the uniform younger-choice candidate. Theory agent is saving a targeted finite exhaustive experiment; do not call its general5/4 bound proved. In parallel, formalize robust saturation families and deepen prior-art equivalence searches. Read live subagent messages/commits and STATUS before deciding which smallest unfinished step remains. Manuscript authorship, new licensing, submissions and DOI are not authorized.
