# Latest delivery: original Conjecture6 affirmative proof

Read heavy_triangle_112/PROOF.md for the complete original claim of arXiv:2603.25113v1 Section5 Conjecture6: (3,0)-saturated subcubic graphs with every degree-three vertex on a triangle admit (1,1,2)-packing colorings. This is a positive proof candidate, not another counterexample. It covers all original graphs, not only the initial matched-heavy family.

Mechanism: Hall matching on triangle/diamond core edges, cycle-elimination exchanges, and a radius-two class leaving a bipartite graph. Review loops/multiplicity, the exchange endpoint argument, direct-edge cycle parity, and original distances. See B_SELF_REVIEW.md for B's own checks; independent acceptance remains pending.

Reproduce using Python3.12 standard library:

    python workstreams/B/heavy_triangle_112/regression.py
    python workstreams/B/heavy_triangle_112/check_matched_family.py

Actually run:7042 small admissible labeled graphs,671 core presentations,30 leaf/disconnected fixtures;5,131,533 original-distance pair checks;1394 cycle exchanges;3 rejected controls. The additional matched-family70-graph regression also passes. Construct.py starts from original adjacency; verify_original.py is a separate distance/condition checker with no construction imports. No Lean, firstness or external acceptance claim.

Proof SHA25611ba0814316379a764d9ed74431680b9c7c792428191e8d1f1e8c9086689183e. The seven-vertex original Conjecture3 counterexample remains unchanged atfadb2d4. Conjectures4/5 remain unresolved and their paused-route limitations remain recorded. ROOT may review/integrate/sign; B has not edited main or allocated a root project number.

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

## Active next research

Conjecture5 (2,2,2,2,3) on 2-saturated triangle-local graphs is newly reserved; triangle_22223/SOURCE_GATE.md. No result yet. Conjecture3 counterexample and all earlier proofs remain frozen.

## Subsequent route checkpoint and next target

Conjecture5 is unresolved: see triangle_22223/RESULT.md and run its verify_obstacle.py for the exact failure of the one-exception route. Do not confuse this with the Conjecture3 refutation. B now reserves original Conjecture4 (also2024 Open problem2), palette(1,2,2,2,2), without local-girth restriction; two_saturated_12222/SOURCE_GATE.md. No new result yet.

Conjecture4 bounded route is now paused without resolution; see two_saturated_12222/RESULT.md for1500 SAT presentations and the precise C5 obstruction to the naive construction. No additional original counterexample has been claimed.

Active next exact scope: original Conjecture6, (3,0)-saturated triangle-local graphs and (1,1,2); see heavy_triangle_112/SOURCE_GATE.md. No result yet.

Conjecture6 frozen local source: 964fd526fcfac35c2397a71c44bfe8401d2560c1. Construct SHA256cf85e84a0fd3822c00cf41feafc67193edb2c729ae0f97a817e8fb9e40560f9e; original verifier SHA256ba24c26908933c628ae5a969153ac49e58398a4e65698b7cdc25e34e31872c32.

Execution accounting correction: heavy_triangle_112/RUN_COMPLETION.md records the confirmed final exploratory-process result. It corrects an earlier stop assumption, without changing frozen proof/constructor/regression bytes atd6238ac.

Narrow next gate: printed Conjecture9 appears to follow directly from classical Brooks; clawfree_square7/SOURCE_GATE.md. Treat as a possible classical-corollary/source-status clarification, with high duplication risk, not a counterexample or new theorem claim.

## Low-priority classical-corollary source note

clawfree_square7/PROOF.md proves the printed Conjecture9 seven-radius-two vertex bound via classical Brooks and an elementary exception exclusion. This is not presented as a historically new theorem. Run python workstreams/B/clawfree_square7/check_exception.py:19355 labeled cubic8 graphs,2520 connected claw-free, all diameter3;7708 local-bound checks and controls PASS. High folklore/duplication risk remains. Main review priority remains the exact Conjecture3 counterexample and full Conjecture6 proof.

Conjecture9 note frozen local source: f047f07a8379e52d9131a6f8211fe177abcd6623. Proof SHA256475dbd6209ccdd85bb635fdf4ef459de2d91c6cbbab8df384957ef39faa18d46; checker SHA2566ac424cf211c475deaa0252740fe0fc535fd8e9cf573a81e06fb0d948600809e.

New active source-gated target: arXiv:2608.02566v1 Section6 Problem1 (1,1,3,3,4), excluding H. No candidate yet. See clawfree_11334/SOURCE_GATE.md. Related-work clarification for the frozen Conjecture6 proof is heavy_triangle_112/RELATED_WORK.md; standard skeleton/Hall tools are prior background, not claimed original.

August Problem1 screening checkpoint:254 presentations SAT, no original result; fixed-core-class4-packing transversals require private neighbors. See clawfree_11334/ROUTE_CONSTRAINT.md and check_route.py. This route is paused rather than enlarged unchanged.

## New ORIGINAL counterexample: August claw-free11334 Problem1 (08:00 UTC)

Review target: local source8e0417722436269bb02f29dc5bab9bdd88118e0a; remote frozen SHA recorded after publication. Earlier candidate/paused entries are superseded ONLY for arXiv:2608.02566v1 Section6 Problem1. Other paused conjectures remain unresolved.

- Proof: clawfree_11334/COUNTEREXAMPLE_PROOF.md, SHA25679a049ad7f668c8298c9985428d075b6cad18336aa77da12b61cf29bd2613095.
- Explicit36vertex54edge original counterexample: clawfree_11334/counterexample.json, SHA2567d1cdd61f032185728ffac6a6b0b6a79c611e0a36341a78eb35610df55b95ccd.
- Independent-implementation verifier: clawfree_11334/verify_counterexample.py, SHA256e9e7cb20a1b6989905563193bd92c388231e6e3a049caa27f6db1b33fdb7f573.
- Run from repository root: `python workstreams/B/clawfree_11334/verify_counterexample.py`. Python3.12.14 stdlib; no install, network or solver. Actual result PASS, logged in verify_counterexample.log. 531441 projected labelings,48 proper,3888 radius4 transversals,zero valid;36 original BFS rows;3negative controls;positive weaker-palette and even-ring controls.
- Source: https://arxiv.org/html/2608.02566v1#S6 ; original PDF printed page15 (zero-based page14). Question's exception H has12vertices, hence not our36vertex graph. Exact statement independently checked in HTML andPDF after discovery. See updated SOURCE_GATE.md for authors/version/search limits.
- Mathematical acceptance focus: every arbitrary original coloring yields a high representative in each triangle, so the core projection is necessary even when a triangle has multiple high-colored vertices. Adjacent blocks have allcrossdistances<=3. Color4forcesprivate neighbors, incompatible with one diamond's end color4; every end color mustthenliein{3a,3b}, impossiblearoundoddcycle.
- The general written result covers12kvertices for EVERY oddk>=3; finite enumeration certifiesonlyk=3. No smallest-order/Lean/firstness claim.
- Frozen proof does not depend on the earlier Hall-based sufficient-route sketch, earlier random SATs, or generic solver timeouts. Two15second runs on k=3,5 returnedUNKNOWN, explicitly retained in personalreceipt. No running search needs monitoring.
- Status: self-reviewed original counterexample, pending independentROOT/human acceptance. Main integration/signing/numbering remain ROOT's responsibility. No direct peer notification, PR, author contact or submission performed. B keeps all previous frozen packets unchanged.

Publication confirmation (08:02 UTC): the new original11334 packet is frozen remotely at **bf89129f2bf457f7a63292d559f5c279330c9b2c** on partner/dist-B. API branch update succeeded with expected-head protection and force=false. Fetched exact remote commit; local-tree comparison was empty. Fresh git archive replay checked all176 manifest entries and reran verify_counterexample.py to PASS. This is B's replay, not independent acceptance. No signing claim.

## Optimized permutation lower bound extension (08:10 UTC)

This does NOT replace accepted e6ff181 or modify its proof. New file permutation_gp/OPTIMIZED_TERMINAL_BOUND.md proves the exact optimum WITHIN the source-inspired terminal-alphabet construction: choose t0=ceil((d+1)/k), yielding t0(d+k-t0)_(k-1). A tie witht0+1 occurs exactly when k dividesd+1. For fixedk this is a positive-density family of orderd^k, so the relative violation of the source's already-refuted orderd^(k-1) formula grows linearly withd. No exact maximum, additional conjecture refutation, or priority claim.

Replay: `python workstreams/B/permutation_gp/verify_optimized.py`; actual Python3.12.14 stdlib PASS in verify_optimized.log.13104 exact optimizer parameter checks;Pe(9,3) rebuilt from original full-old-word arc rule:1320vertices11880arcs224selected49952orderedpairs,distances3/4/5 withcounts24192/19488/6272. Strict distancegap certifies every ordered triple. Two optimizer boundary/falseclaim controls PASS. This extension is personally checked, pending independent acceptance; no new agents or Lean. Frozen proofSHA2563cdae7f8b9e33f0813fe4c22fae41ad91e8c9b5e5a7aa6b2fc9bd2fa53908851.


## Kautz length-three exact formula (2026-10-10 08:41 UTC)

Review frozen local source 50f4dbb6606aaf428d68b1e3fb2231da473fb7e9, publicly reserved at 16f34b3322bec26504f6e6b84b0f0c86f6f9d0fc. For every integer m>=3, gp(Ka(m,3))=m(m-1)(2m-1)/6. This solves only the length-three Kautz slice of arXiv:2604.15909v1 Problem5.2; it is a positive proof candidate, not a counterexample or the solution for every length. Pending independent review and historical-novelty assessment.

- Proof: kautz_length3/PROOF.md, SHA256 4dfb6bd9e0652cfa5bf2e4b36def9bae93d89d954af2a682e86b7a39fc642ffc.
- Checker: kautz_length3/verify.py, SHA256 7dc0f53094929def038315a902b803f4b6026139832042857b4067426e5b4f4d.
- Run from repository root: `python workstreams/B/kautz_length3/verify.py`. Python3.12.14 standard library, no solver/dependency installation. Actual PASS is in verify.log; SELF_REVIEW.md records scope and limitations.
- Evidence: 247508 distance comparisons, 93848 isometry pairs, 250744 local geodesic checks, 599734 lower-bound triples, all4096 subsets at m=3 and all32768 restricted subsets at m=4, three negative controls. These finite checks supplement the analytical induction and analytical base case.
- Review priorities: Section3 injects endpoint-zero words into missing middle-zero cells; Section4 exhausts all four selected-arc types and bounds one letter's incidence; Section5 handles the m=3 boundary where deleting a letter leaves a digon. The digon m=2 is deliberately excluded.
- Independent-set lower bound and upper count are elementary and may be prior knowledge; the source already supplies five table values. No novelty claim is made for that independence calculation. No MILP, Lean, or outside reviewer was used.
- Source gate includes original source, author survey, post-candidate checks and the uninspected 2008 independence-number paper. No detected later same-scope resolution is not proof of priority.

Conjecture5 dense-interface continuation is paused: triangle_22223/RESULT.md now records263+200 SAT presentations and an exact mobile-exception gadget calculation. No original counterexample or universal theorem was found on that route.


## Confirmed publication and next exact scope, 08:44 UTC

Kautz length3 frozen remote44c1ec16781f1c363d0874e4dd2f0d93f640a48e fetched successfully. Fresh archive /tmp/B-kautz-replay-72Y0fM: all190 manifest hashes and definition-first verify.py PASS. No independent acceptance inferred.

Observed main5252ec23db04c7b96a7f0cfb5f3c0edb5e07e7b0 now accepts B's36vertex11334 counterexample: independent original-definition written review and actual ROOT2 Lean compilation,18 standard-only axiom audits. B read README/INDEPENDENT_REVIEW; B did not rerun Lean. All odd-k family accepted in writing, fixed k=3 only in Lean.

Next proposed reservation is ONLY Ka(m,4), m>=3, original Problem5.2. See kautz_length4/SOURCE_GATE.md for refreshed source/ownership gate and distinct distance-two mechanism. Publish before substantive computation. Earlier packets remain frozen.


## Length-four constructive progress; exact-value route paused, 08:53 UTC

Three universal lower bounds are now recorded in kautz_length4/LOWER_BOUND.md. Strongest displayed family: gp(Ka(5q,4))>=130q^4-74q^3+8q^2, q>=1; asymptotic density26/125. This is a partial lower bound on original Problem5.2, not a counterexample or exact solution. A27-state exact certificate proves every length8 block word has at most2 selected windows, which excludes every geodesic triple for arbitrarily large alphabets.

Run verify_lower_bound.py and verify_three_blocks.py in that directory (from root with full paths); both Python3.12.14 stdlib PASS, logs/certificate included. LOWER_BOUND.md includes the complete arithmetic table and bridge. RESULT.md records discovery scopes, failures, actual environment and precise restart condition. No numerical optimum is promoted to an original upper bound. Pause template enlargement absent a constraint on arbitrary GP sets. No new agents or independent-review claim.


## Structural checkpoint and prior-result correction, 09:02 UTC

Length4 Kautz lower bounds remotely frozen0202144d240d871f9165888e76962cd1e44ce36a; fresh archive205hashes and both exact checkers PASS. Exact-value template search remains paused.

Returned to reserved Conjecture5 using a NEW analytical missing-color reduction rather than random enumeration. triangle_22223/SHORT_CONNECTOR_REDUCTION.md proves the exact four-square-color connector CSP and uniform-length2, uniform-length3 (except triple-edge core), and all-length>=7 corollaries for loopless cubic triangle expansions. The length3 result explicitly imports Lai–Montgomery–Poon2003 dynamic coloring. Local exact certificates108cases,24original graph witnesses45252BFS pairs PASS. Full original Conjecture5 remains unresolved; mixed short edges and any fifth-colored triangle/connector remain the actual obstruction. No further homogeneous random sampling justified.

Important duplicate-status closure: clawfree_square7/PRIOR_RESULT_CONFIRMED.md locates Li–Lai2017, whose published general theorem already implies the entire printed Conjecture9 seven-square-color bound. The older B Brooks note is an alternate classical corollary, NOT new research resolution. The2017primary abstract was accessible; full proof re-verification not claimed. NewOct7paper2610.09565 further gives6 for cubic graphs. No effect on the accepted36vertex11334 counterexample.


## Mixed-short route obstruction and deferred next gate, 09:08 UTC

Frozen short-connector packet2123cb6e79bf6a54c3f3fd83a14d1e16639e1fd6 fetched explicitly and replayed:211 manifest hashes and both checkers PASS. A generic git fetch refreshed only configured refs, so an initial comparison used a stale B remote-tracking ref and stopped; explicit B-ref fetch corrected this, with no file loss or force push.

A genuinely new proposed placement rule fails on a19vertex graph: K4 triangle expansion with five connectors length2 and one length3. Confining the fifth color to length2 interiors is impossible by a matching-cut argument, yet the original palette has an explicit valid coloring with its sole fifth-colored vertex on the length3 path. See triangle_22223/MATCHING_ROUTE_OBSTACLE.md, exact object/probe log and separate verify_matching_obstacle.py/log. All8 eligible core matchings and original BFS checked; damaged coloring rejected. This is ONLY a restricted-route obstruction. Stop this restricted placement search; resume only when length3/triangle fifth-color locations and their port-list constraints are handled.

The possible new general1123/Petersen question is NOT reserved: CANDIDATE_GATE_1123.md records a2017/2018 full-solution abstract claim conflicting with later open-problem statements. No full proof/status reconciliation and no high-cost search. Preserve uncertainty and do not announce another open target prematurely. No active long computation remains; frozen Kautz3 and other pending packets await genuine independent review.


## Updated card receipt and new exact reservation, 09:13 UTC

Explicitly read BRIEF and Bcard09ad05d221909dfcfd9ce6a14ecd13a1ac3c4846 after wildcard branch fetch. Earlier generic git fetch updated only configured main; future ownership checks must fetch all branch refs explicitly. ROOT now records real independent reviews in progress for Ka(m,3)44c1ec and Conj6d6238ac, not acceptance yet. A's newer full sequential-order scope remains separate.

B proposes claw-free12222, arXiv2608.02566v1 Section6 Conjecture1, with exact gate in clawfree_12222/SOURCE_GATE.md. Publish before substantial work. Standard simple-core incidence5 cases are already known and excluded as new discoveries. Focus on boundary extension across admissible caps/multiple-edge interfaces; retain original assumptions and reject restricted-rule failures as original counterexamples. Previous frozen results unchanged.


## Complete cubic-subcase proof candidate, 09:23 UTC

New clawfree_12222/CUBIC_PROOF.md proves the CUBIC subcase of original AugustConjecture1, not the entire subcubic statement. Public reservation41f78ef preceded the finite cap work. The proof imports Maydanskiy's incidence5 theorem, then handles all parallel-core reductions, pendant loop caps and diamond strings with palette-specific exact interfaces. Three canonical boundary types for each of three caps give9 literal witness rows.

Separate verify_interfaces.py rebuilds cap graphs and BFS, checks1212 external boundary colorings with134532 distance pairs,282 cap pairs,89 leaf cases, and rejects a damaged coloring. Actual Python3.12.14 stdlib PASS in verify_interfaces.log. Universal reduction is written, not inferred from these cases. SELF_REVIEW.md lists the actual hypotheses, sources and the crucial missing general-subcubic degree-two-path case. Freeze and deliver as a pending-review positive SUBCASE; no historical-firstness, full-conjecture, Lean or independent-acceptance claim.

### Connector checkpoint after cubic freeze b49a74f (2026-10-10 09:34 UTC)

Read clawfree_12222/SUBDIVIDED_PROOF.md and MIXED_PATHS_PROOF.md as two separate positive subcases, not a full conjecture proof. Run from repository root:

    python workstreams/B/clawfree_12222/verify_subdivided.py
    python workstreams/B/clawfree_12222/verify_subdivision_certificate.py

Both actually PASS on Python3.12.14 stdlib. The second checker does not import discovery or other checkers; it enumerates all old boundary assignments, checks complete orbit coverage, independently rebuilds new graphs/distances, checks recurrence local transitions, and rejects corrupted input. Frozen cubic proof/verify interfaces remain byte-identical at b49a74f; the mixed theorem explicitly depends on its Section2. No independent-review claim. The fully subdivided theorem does not depend on the cubic proof, only Brooks and its explicit words. Review full-graph shortcut control, arbitrary-length recurrence, and unused-port deletion. Remaining mixed1/2 connectors cannot be silently covered by taking a union of the theorems.

### Mixed1/2 structural theorem (09:40 UTC)

PSEUDOFOREST_PROOF.md is independent of Maydanskiy and the frozen cubic candidate: it uses only explicit orientation, original distances and Brooks. Read the precise loopless-core hypothesis and the optional long-path exclusion of length3. Reproduce with:

    python workstreams/B/clawfree_12222/verify_pseudoforest.py

Actual PASS:588 admissible objects,138753 distance pairs,588 negative controls.60 skipped cases violate the pseudoforest assumption. probe_mixed_short.py is DISCOVERY ONLY and its578 SAT cases do not establish the remaining theorem. Review the exact positive-neighbor counts at root triangles and outgoing-port triangles, and the low-degree vertex argument excluding K5. Frozen proof bytes from b49a74f and790bc81 remain unchanged. All new theorems pending independent review; no communication to other distributed agents is asserted.
