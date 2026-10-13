# ILP1 recovery checkpoint

## Actual repository state

Primary checkout: `/workspace/scratch/6a1539b44ef3/math-ilp1`.
Branch: `partner/dist-ILP1-20261014`.
Allowed files: `workstreams/ILP1-20261014/` and `coordination/agents/ILP1-20261014.md` only.
Fetched main baseline: `bf732c32f1b8cef32ebf69cac6fb232a8a5323a3`.
Last verified remote: `310fabfae3cf7d12f64068c13b8a4111fe5aa41b`, tree `210be32f74b76ec032dfb9e51e918b084c66166c`.
Its local source6807eac9a7c5a2acdd17c3893fe0697a1e1656f6 is preserved on `partner/ilp1-local-randomized-20261014`.
The current subsequent integration includes R19–R21 and actual corridor proofs; read live git and publication receipts to determine whether it has been published. Never invent a self-referential future hash.

```sh
git fetch origin
git status --short --branch
git rev-parse HEAD origin/partner/dist-ILP1-20261014
git ls-remote origin refs/heads/partner/dist-ILP1-20261014
git log -8 --oneline
git log -1 --format=%H -- workstreams/ILP1-20261014/HANDOFF.md
```

Do not switch away from dirty work or reset it. The other researcher checkout `/workspace/scratch/b1d6bae025af/math-crypto3` was dirty at startup and remains untouched. Never edit main, shared coordination/roadmaps, paper006 or another agent's files.

## Verified conclusions to preserve

* R1 is exactly unit-time scheduling with ALL edges i->j for i+B<=j, plus true forward data edges. Actual operational bridge, optimum existence and a concrete executable exact Lean enumerator are proved. Offset-only edges are false.
* Fixed-schedule minimum window and resource caps are Lean verified. General finite Bellman interfaces are kept distinct from the concrete enumeration and Python code.
* R19 B=W+1,N=kW perfect saturation iff legal singleton/boundary-swap pair tiling. It has an O(N+E) test and short true-edge rejection certificate. Written proof plus independent reviews, not Lean verified.
* R20: for c=B-W,S=WH-N every H-completing trace has [0,max(0,tW-c-S)) subset D_t subset [0,min(N,tW+c)), and tW-S<=|D_t|<=tW. This actual-model strip/count is Lean verified. The sharp binomial candidate count and FPT(c+S) exact algorithm are separately reviewed written proofs; Python is not verified by Lean.
* R21 arbitrary-N optimum at B=W+1 has O(N min(B,N)(N+E)) time and O(N+E) space. Non-delay optimum exists by completion dominance; nonclear states have unique non-delay actions. Compress those runs between N+1 clear prefixes. General c has XP bound via at most N(2^c-1)choose(B,c) outgoing macros. Full written/independent proof and implementation audit, not yet Lean algorithm correctness.
* R15 sharp random5/4 and deterministic3/2 at B3,W2 remain proved; R18 repeated two-input family establishes the same factors with an additive constant. Actual repeated graph/separation/optimum2q is Lean verified; observation/probability argument is not. Conditional randomized scalar kernels do not close that gap.
* Resource families R11–R13 remain proved/reviewed, including the linear window needed at fixed epsilon<1/W and its exact formula. One earlier exact-saturation collapse costs only one cycle; do not imply huge IPC gain.

## Evidence and reproduction

Lean binary `/workspace/scratch/6a1539b44ef3/ilp1-tools/lean-4.34.1-linux/bin/lean`, version4.34.1, Std only. Root receipts cover161 distinct endpoints with standard axioms only. New actual-corridor review: `subagents/formal-dp/CORRIDOR_LEAN_REVIEW.md`.

```sh
python workstreams/ILP1-20261014/formal/verify_corridor.py --lean /workspace/scratch/6a1539b44ef3/ilp1-tools/lean-4.34.1-linux/bin/lean --proc-self-compat --output /tmp/ilp1-corridor-check
```

Other pinned runners in formal/ are verify.py, verify_footprint.py, verify_uniform_potential.py and verify_repeated_gadgets.py; supplementary Bellman runner is subagents/formal-dp/verify.py. Existing evidence directories are lean-root, lean-footprint-root, lean-bellman-root, lean-uniform-root, lean-repeated-root and lean-corridor-root. Check source hashes before rerunning; do not repeat unchanged exhaustive work after recovery. `admit` is a legitimate field name in ROBOperational, not an admitted proof.

From the workstream:

```sh
python -m unittest discover -s tests -v
python paper/build.py
```

Root16 test groups pass. New independent report files: `subagents/verification/corridor_results.json`, `forced_macro_results.json`, `PACKED_TILING_REVIEW.md`; source algorithm/proofs in `subagents/theory/forced_segment_dp.py`, `FORCED_SEGMENT_DP.md`, `PERFECT_SATURATION.md`; root corridor in `src/corridor.py` and CORRIDOR.md. Whole tested ranges, seeds, timing and hashes are saved. Do not add overlapping counts.

The current paper is14 pages; inspect evidence/paper-build.json and paper-qa.md hashes. PDF rendering may transiently leave a truncated PNG; load every page with PIL and rerender any failed page, never enable truncated-image acceptance. Temporary images are outside git under `/workspace/scratch/6a1539b44ef3/ilp1-paper-qa/`.

## Active roles and smallest next steps

Separate worktrees are sibling `ilp1-theory`, `ilp1-lean`, `ilp1-verification`, `ilp1-literature`, `ilp1-formal-dp`, with `partner/ilp1-<role>-20261014` branches (formal role uses formal-dp). Read actual live agent messages before duplicating work. Their commits are cherry-picked only after review.

* Theory: save arbitrary-length forced-macro family and investigate two-chain hidden-final-dependency obstruction. A candidate already works for B4,W3 with all but the last instruction's incoming dependencies known; independent review is pending. Do not claim it as a published theorem yet.
* Verification: independent prefix-potential optimality checker for R21, regenerating all macros rather than trusting a submitted subset, with tamper controls. It is polynomial graph checking, not a constant-time structural rule.
* Lean: new actual ROBReady local invariants/cardinality/forced-action/progress lemmas. At this checkpoint these are not in the161 root total; require commit, fresh root build and review. General non-delay-optimum and compressed-DP formal bridges remain open.
* Formal_dp: independent hidden-tail proof review; actual corridor Lean review79a7818 already integrated.
* Literature: last integrateda964cec, close parameter comparisons. Discrepancy precedences and frontier representations are established prior art. Recent degeneracy/time-window results do not directly imply these finer parameters, but no historical-first claim is justified.

Then pursue FPT versus XP in c=B-W, the complete Lean optimizer bridge, or larger-resource online minimax. Do not restart resolved B3 random/additive-constant questions.

## Failed routes and scope traps

Critical-path and oldest-ready priorities are not generally optimal. Height and work bounds need not be simultaneously tight. Saturation thresholds need not vary monotonically even though optimum duration does. Arbitrary true dependencies do not preserve the base interval-order class. Appending dummy instructions to reach N=kW fails (N5,B4,W3,edge0->1 vs N6). A forced macro may last Omega(N) at fixed W3. The sharp state-count example is not a complexity lower bound. XP(c) is not FPT(c). Uniform omission at B4,W3 fails4/3 (ratio37/27), and fixed biases cannot repair it; this does not refute every adaptive policy.

## Publication mechanics

Git HTTPS fetch works, but direct push lacks a username. Use the authorized GitHub connector's create_blob/create_tree/create_commit/update_ref, with the exact expected remote head and force=false. Build the tree from a pinned clean local commit and compare API tree SHA with the local tree before update_ref. Then actually fetch, query ls-remote and compare source/remote trees. Preserve local integration history on a unique branch before recreating a clean tracking branch; never force push or reset dirty files. Public receipts contain real SHAs, not automation/conversation IDs. The latest saved receipt before this integration is evidence/publication-310fabf.json.

Keep the authorized continuation enabled; no claim of continuous computation between runs. No author list, new license, submission, DOI or protected-file changes are authorized for this research.
