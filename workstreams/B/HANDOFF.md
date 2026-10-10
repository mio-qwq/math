# Latest delivery: seven-vertex original Conjecture 3 counterexample

Read two_saturated_112/PROOF.md. It disproves arXiv:2603.25113v1 Section5 Conjecture3 as printed, with no local-girth assumption. K4 with the three edges at one vertex subdivided once is 2-saturated and subcubic but not (1,1,2)-packing colorable. Triangle forces the unique distance-two color; deleting that triangle vertex leaves an odd five-cycle.

Reproduce: python workstreams/B/two_saturated_112/verify_candidate.py . Python3.12.14, standard library. Actual2187 assignments,0 valid; all degrees/saturation/BFS and3 proof cases pass;2 corruptions rejected. Discovery program is separate and unnecessary for verification. Candidate object is candidate.json. Source/duplicate gate is SOURCE_GATE.md; historical novelty unestablished. Independent review pending; no Lean or world-first claim. Prior packets are unchanged. Public reservation b7ac4fc preceded search.

Review the frozen commit, confirm the exact original quantifier and the degree-three-neighbor counts, then inspect the short elementary proof. ROOT may integrate/sign under its own authority; B has not modified main or allocated a number. Do not delay acceptance for minimality or classification.

# Active next target: Conjecture 3

B now reserves arXiv:2603.25113v1 Section5 Conjecture3, (1,1,2)-colorability of every 2-saturated subcubic graph. Source gate and planned certificate in two_saturated_112/SOURCE_GATE.md. No result yet; previous four proof packets remain frozen.

# B latest handoff: original Conjecture 2 and all of Problem 1

## Five-color conjecture: positive computer-assisted proof candidate

El Zein–Mortada arXiv:2603.25113v1 Section5 Conjecture2 is answered
affirmatively in triangle_packing/FIVE_PROOF.md, with exact finite
certificate and complete original-graph semantic reduction. This is NOT
a counterexample. No independent acceptance of this new packet is claimed.

- Frozen local source97ea15477ba9daf59bc9c335c200fca0756b176d.
- ProofSHA256808ff9c3c60a9b4a8663bb8a4f8c7af4d4aac6374decb3d7b6dd7377d33f1a20.
- python workstreams/B/triangle_packing/verify_five.py
- python workstreams/B/triangle_packing/construct_five.py
- python workstreams/B/triangle_packing/five_boundary_checks.py
- Actual PASS:90 boundary states,48 path states,139 invariant matrices,
  225 initial products,2085 closure transitions, exact all-length cutoff;
  2 corrupted invariant controls rejected;864 original graph constructions
  and33 boundary fixtures pass,3 corrupted graph/color controls rejected.
- Key review points: color5 only at apices is a construction restriction,
  not a graph hypothesis; all radius-four short paths fit the interfaces;
  only adjacent apices can conflict at radius5; F T^(L-3) B handles
  overlapping boundaries; stabilization is T^14=T^13, NOT all-ones;
  direct-cap/diamond/leaf/disconnected cases are included.
- Certificate compression is reversible base64/zlib with decoded SHA256.
  Standard-library verifier checks the full finite invariant; no external
  SAT oracle, numeric tolerance, new axiom or guessed length horizon.
- B personally wrote and checked everything. Independent mathematical and
  certificate review, historical novelty and human review remain pending.
  No Lean or signed release by B. ROOT owns integration/signing.

## Other new results preserved

All three original Problem1 palettes have separate unchanged proof packets:
FIRST_PROOF.md (1,2,3,3), SECOND_PROOF.md (1,2,2,4), and PROOF.md
(2,2,2,2,4), the last strengthened to arbitrary fifth radius. Frozen
remote checkpoints are c0692bc,09880f3,1ccf730 respectively. None of these
four new positive candidates is covered by ROOT's older acceptance of
B's circulant, 0-saturated packing4, or permutation counterexample results.
Historical handoffs below preserve old stages; this section supersedes
statements that Conjecture2 is still unresolved in B's stream.

## Resume and acceptance

The exact newly reserved scope (Problem1 plus Conjecture2) now has complete
candidate answers. Do not extend the old brute-force window or silently
change these proof bytes. Review the fixed remote commit containing this
handoff and compare proof/checker hashes. If a gap is found, make a new
version with explicit mathematical delta. Further discovery requires a new
nonconflicting exact reservation and source gate; no new root number is
allocated. Read updated task cards at the next research start.

---

# B latest handoff: all three original Problem 1 palettes

The new FIRST-palette theorem completes B's three positive proof candidates
for El Zein–Mortada arXiv:2603.25113v1 Section5 Problem1. All await independent
acceptance; this is not a new counterexample or a claim that Conjecture2 is solved.

- FIRST palette(1,2,3,3): triangle_packing/FIRST_PROOF.md.
  Frozen local5b1efad6376ce7ea526e1cf06bfe3faa8261d15d;
  proofSHA256013258dfcb0ad45772dd983b5aba0d4c50dfae067a4128106eb84768eb2b46ec.
  Exact71-matrix invariant;42 graph-interface states;27 path states;
  121 two-connector seeds and781 closure transitions. Long-gap cutoff
  proved by T^10=J and JT=J. Two negative controls rejected.
  python workstreams/B/triangle_packing/verify_first.py
  python workstreams/B/triangle_packing/construct_first.py
  Actual original-graph check:864 necklaces PASS.
- SECOND palette(1,2,2,4): unchanged SECOND_PROOF.md and139-state invariant,
  frozen remotely at09880f3a07c7e9b26515fb613652b70554edfe1b.
- THIRD palette(2,2,2,2,4): unchanged PROOF.md, stronger arbitrary final
  radius theorem, frozen remotely at1ccf7301b297d52a83df269962b1075c3e711df7.
- Review first-palette semantics as well as matrix closure: each interface
  includes both outside neighbors, all paths of length<=3 must be covered,
  long connector relation F T^(L-2) B includes both apex constraints, and
  the diamond and direct-cap exceptions require their explicit colorings.
- Conjecture2 remains an active separate investigation. No blind graph
  enumeration is being repeated; the next mechanism restricts color5 to
  triangle apices to control long-range interactions. No result yet.
- All work was performed directly by B, no new research agents. Self-check
  is not independent acceptance. No Lean, signed release or firstness claim.

---

# B additional handoff: Problem 1 second palette

The THIRD-palette pure written proof is frozen remotely at
1ccf7301b297d52a83df269962b1075c3e711df7 and remains unchanged.
The new SECOND-palette result is a separate computer-assisted affirmative
proof of (1,2,2,4)-packing colorability for the same original class.

- Read triangle_packing/SECOND_PROOF.md, with structural lemma in PROOF.md.
- Local freeze312c2be09cba63484560664101f615e93daaaa55.
- Second-proof SHA2562bc9a0494f2331ccc2accd33a195d4ba330dbf275a6d7bdea2e34b2e63a7411b.
- Run python workstreams/B/triangle_packing/verify_transfer.py :139 invariant
  states,1251 checked transitions, two negative controls rejected.
- Run python workstreams/B/triangle_packing/construct_second.py :864 actual
  necklace colorings checked against original BFS distances and hypotheses.
- Review the semantic bridge: six port-pair states, correct apex colors,
  all distance-four constraints, one special length4 connector, the
  all-length reduction P^11=J and JP=J, and chain embedding/exceptions.
- transfer_certificate.json is a complete finite inductive invariant,
  not evidence extrapolated from a bounded graph search. The checker
  implements Boolean matrices separately from discovery bitmask code.
- Both proofs are B-authored and self-checked; independent review, novelty
  and human review remain pending. No Lean, signed release or counterexample
  claimed. Problem1 first palette and Conjecture2 remain unresolved here.
- Failed probes are retained: transfer_language_probe.log intentionally
  contains the failed normal-ansatz live-cycle diagnostic. It is superseded
  by SECOND_PROOF.md and the verified augmented invariant.

---

# B latest handoff: triangle-local packing Problem 1, third palette

## New affirmative theorem, pending independent review

Target: El Zein–Mortada arXiv:2603.25113v1 Section5 Problem1, third question.
Every 1-saturated subcubic graph with each degree-three vertex on a triangle
admits (2,2,2,2,4)-packing coloring. B proves the stronger (2,2,2,2,r)
statement for every positive integer r: at most one fifth-colored vertex
per connected component. This is an affirmative answer, NOT a counterexample.

- Frozen local source: 36f318fe815cbcb673cd6ef3225a6ef26cc3bb54.
- Proof: triangle_packing/PROOF.md.
- Proof SHA256: 28901e98fd0c2eca8a89e7fe45da057ff334a49e15847fdbe795b51e9ea524bd.
- Read the original definition and the precise third palette before review.
  The other two palettes and Conjecture2 are still unresolved here.
- Mechanism: classify components as triangle chains/necklaces and elementary
  exceptions; the square is 3-degenerate after at most one vertex deletion.
  Crucial semantic check: square first, then delete the exception, retaining
  distance-two edges through it. The written initial neighbor lists do this.
- Reproduce: python workstreams/B/triangle_packing/degeneracy_check.py
  and python workstreams/B/triangle_packing/boundary_checks.py
- Actual results: 2904 generated presentations and 26 additional boundary
  fixtures PASS; all three damaged-certificate controls rejected. Exact
  original distances and elimination degrees are reconstructed. Python3.12.14
  stdlib, no solver or Lean dependency.
- Initial four-palette search and distinct odd-cycle phase probe found only
  colorings. Receipts and failed fixed-boundary ansatz remain in the directory.
  These finite tests are not the universal proof; review PROOF.md.
- B personally derived and checked this result. No new research agents and
  no independent verdict yet. No Lean or certified historical novelty.
  API/local commits are unsigned; ROOT owns controlled signing/integration.

## Earlier packets: updated card actually read

At coord/distributed d8f2994, ROOT records the permutation counterexample
accepted and released in signed main7def63b, with fixed-instance Lean and
independent written acceptance of the universal improvement. ROOT also
records independent written acceptance of the earlier circulant and packing
proofs. This is a read card, not a direct chat. Historical notes below preserve
the original handoff states and are superseded by this receipt. Frozen proof
bytes remain unchanged. The new triangle-local theorem is NOT included in
those earlier acceptances.

---

# B new counterexample handoff: permutation digraphs

## Immediate review target

The original optimality conjecture after Theorem 3.6 of arXiv:2604.15909v1
is contradicted by an explicit 90-vertex general-position set in Pe(6,3),
where the conjectured value is 84. Full graph: 504 vertices, 3024 arcs.
Read permutation_gp/PROOF.md and permutation_gp/SOURCE_GATE.md first.

- Frozen local source commit: c13da4c8f3b42f11ad45269dd3100338e116378e.
- Proof SHA256: 6d4d128f753600bbb43783ca9c7ecf42b2c1e64eb301099fe78d291aa635d8d1.
- Certificate SHA256: d7989f129d3bacbd54928b518cba64c5607a6e93968e1cef5f819c159d6d44a3.
- Checker SHA256: 58ce4046c09907f5e4d00506472e96e0eafecff992658ca6e6ee285d4043e31e.
- Reproduce: python workstreams/B/permutation_gp/verify.py
- Negative controls: python workstreams/B/permutation_gp/negative_tests.py
- Actual Python 3.12.14 results: all 704880 ordered triples checked, PASS;
  five deliberately corrupted certificates rejected. No optional packages.
- Construction: prefixes are distinct letters from 0..5; last letter is
  6, 7 or 8. The checker rebuilds the original directed graph independently
  of the constructor and computes exact BFS distances, not a guessed formula.
- The complete written proof additionally refutes the proposed equality
  for every k>=3,d>=2k using 3(d+k-3)_(k-1) selected words. Review the
  retained-terminal lower-distance argument and the buffer-walk upper bound.
- Both code paths and proof were authored by B personally. This is completed
  self-verification, NOT an independent reviewer verdict. Main-Agent review,
  literature novelty and human responsibility review remain pending.
- No claim of exact gp=90, smallest example, Lean, firstness or signed release.
  Local/API publication commits are unsigned. The remote frozen commit is
  the commit containing this packet; local and API SHA may differ. Match hashes.
- Do not delay acceptance of the finite counterexample for optimizing the
  family. A discovered gap should be recorded in a new version, not by
  overwriting this frozen proof. No submission or author contact authorized.

Earlier packets are preserved below and their proof contents are unchanged.
The second frozen remote packet is 126f5139ad183ef43f70c2fb71313b70d1f53abf.

---

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

Frozen local source: 878d6936185dbe29f7691fb6a3c32d2b6abac4b2. Proof SHA256 d3d76612b8c4777fb9906b3506c7a482e7984ca9a1cbcba62491b32d3eda91ff. Checker SHA256 7fe25d248e7bc772497effa491a1bd87e92cf46d8724d7302fb1ea6d1f9c25b9.
