# B current handoff: two distinct original-conjecture proof candidates

The earlier circulant packet remains frozen at628cb3551046886c4fcb383243a090d4b664a231. The continued packing packet is described below; these are affirmative proofs, not counterexamples. Neither is claimed historically first.

## New packing packet

Target: El Zein–Mortada arXiv:2603.25113v1, §5 Conjecture1. Every finite simple subcubic graph with independent degree-three vertices, each on a triangle or square, is claimed packing4-colorable. No connectedness or minimum-degree assumption is added.

- Read packing_extension/PROOF.md, local frozen commit29d3e9b472c1b05d6cc9d8268af36053cb5508c4, SHA2562ac000076874fefed2bd3cf15e983fcbae6b8f1672952229c79957665e5dbb94.
- The proof reduces the entire class to square chains/necklaces plus caps and elementary exceptions, then uses four concatenable tiles of lengths4,5,6,7. Their scope is arbitrary connector length, not a finite search window.
- B_SELF_REVIEW.md records B's direct reasoning and actual checks; packing_review/INTERRUPTED.md records why earlier helper data do NOT constitute a finished independent verdict. This packet awaits main-Agent acceptance.
- Run python workstreams/B/packing_extension/check_tiles.py and python workstreams/B/packing_extension/self_check.py. Run verify_coloring.py on a supplied adjacency/color certificate to reconstruct every graph hypothesis and every same-color distance directly.
- SOURCE_GATE.md and packing_gate/ credit the known all-even subclass and document the bounded search for a full prior resolution.
- No Lean, human review, priority claim, merge, author contact or submission. GitHub API commits are unsigned; do not call this a signed research release. No signing credentials were requested, created or borrowed.

## Earlier frozen circulant handoff (preserved below)

# B handoff: exact circulant general-position formula

## What to review

`circulant/PROOF.md` gives a complete written proof of the unnumbered
conjecture after Theorem 3.3 of arXiv:2604.15909v1. This is an original
conjecture proof, **not a counterexample**. Do not describe it as a stronger-
version obstruction, a search result, or a result on arbitrary digraphs.

For 1<=d<n, write n=q*d+r with 2<=r<=d+1. The result is

- gp(Circ(n,{1,...,d}))=d+1 if r=d+1;
- otherwise gp=max(r,floor(d/r)+1).

The core argument forces monotone residues in any anchored general-position
set. The no-geodesic conditions on cyclic triples then force either fewer
than r units of residue span or gaps of at least r. These are matching
upper bounds for the source's two constructions. Full n,d quantifiers,
small cases, distance semantics, and both directed orientations are handled.

## Frozen review objects

- Initial local proof commit: 746a7cfc4917496a3a9636e0a34f87de3f57524a.
- Corrected local proof commit: 10c34c12b8ded555a953f75546f965cdf5a94151.
- Corrected PROOF.md SHA256: 8003f03393834d7ee763b6e182a05de06fcc85ff208f50caaae1c2d9a528e30b.

The initial review found an inaccurate inventory of six distance comparisons
in the already-known residue-one boundary case. The corrected version lists
the actual comparisons; the theorem and its main proof are unchanged.
No frozen review object was silently rewritten. Local commit IDs are not
asserted to be remotely fetchable: Git transport lacked credentials, so
publication uses a GitHub API commit with identical files instead. Match the
proof content hash and the final remote commit when accepting the handoff.

Independent internal review is recorded under `audit/`; it is not human
peer review. No nonexistent distributed-peer reply or approval is claimed.

## Reproduce

Use Python 3.12; all verification/search scripts use the standard library.
From the repository root:

    python workstreams/B/circulant/verify_lemma.py
    python workstreams/B/audit/check_independent.py

Read `audit/REPORT.md` for additional boundary and negative-test commands.
The first checker reconstructs distances by BFS and tests 6,884,676 anchored
triples on 3,346 graphs through n=90. The audit checker independently builds
full distance matrices, enumerates general-position sets, and tests the
projection identity. These finite tests validate the argument and do not
replace the all-parameter written proof.

Witness-search timeouts are explicitly inconclusive. `circulant/RESULT.md`
records 319 completed search cases, with 231 exhausted and 88 timed out.
Search was stopped after deriving the general proof. No false UNSAT or
nonexistence assertion was inferred from a timeout.

The separate `search/` directory records a paused packing-coloring route:
95,165 generated admissible graphs had checked four-colorings. No counterexample
was found. `search/STRUCTURE.md` is only a reduction sketch. This route is not
solved and need not be integrated as a mathematical theorem.

## Literature, exclusions, and remaining work

Read `literature/circulant_status_check_2026-10-10.md`. Original coauthors'
August 2026 survey still calls the exact bound conjectured optimal. A bounded
public search found no prior resolution; unindexed work and incomplete author
bibliographies remain possible. No world-first claim is justified.

No Lean formalization or compilation has been performed. Human authorship,
responsibility review, archival/publication choice, and main-branch integration
belong to the main Agent/user. No author outreach, submission, merge, or force
push is authorized by this handoff. No numbered 007/008 project was created.

The main Agent can first review the short upper-bound argument and the frozen
audit, then independently replay the checkers. Integrate into a numbered
project only after choosing the final scope and checking concurrent claims.

## Transport and provenance

Initial remote checks on 10 October 2026 exposed only main at
42a30d62d084a9dbe64c92666addd6cf28986b16. coord/distributed returned 404;
no B task card was available. B claimed its candidate on partner/dist-B
before substantial computation, then recorded the circulant route change.
This does not prove no unseen/concurrent claim exists. Changes are confined
to workstreams/B. Unknown pre-existing workspace files were preserved.

Source scripts, concise actual execution logs, outcomes, and hashes are
included. Bulky per-instance packing-search JSONL logs remain in the local
checkout; the deterministic commands regenerate them. The remote deliverable
does not claim to include those raw logs. No credentials, private prompts,
other agents' files, or shared dependency changes belong in this package.
