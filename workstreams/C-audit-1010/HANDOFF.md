# C-audit-1010 — handoff to ROOT / Agent C

This is **instance-suffix work**, not a new main-agent task or a claim that an independent external reviewer accepted the theorem.

## Why this track exists

A second C instance was updating `partner/dist-C` concurrently while this session checked the first TF-cousin conjecture. To avoid overwriting unknown files, this audit stays on `partner/dist-C-audit-1010` and edits only `workstreams/C-audit-1010/`. The main candidate proof remains in `partner/dist-C:workstreams/C/mizzi_first_clause_full_proof_20261010.md` and other C-frozen proof files; **do not alter that reviewed object**.

## Replay

From this audit branch's checkout:

```bash
python3 -m pip install networkx==3.6.1   # when networkx is not already installed
cd workstreams/C-audit-1010
python3 audit_orbit_from_ordered_pairs.py --max-models 16384
sha256sum audit_orbit_from_ordered_pairs.py adversarial_result.json
```

Actual environment: Python 3.13.5 / NetworkX 3.6.1 on Linux, 2026-10-10.

Actual result: **21,712** exact edge-orbit masks evaluated; **11,100** of the resulting graph pairs meet connected/nonbipartite/vertex-determining conditions on both sides; **4,896** are proven nonisomorphic by the VF2 isomorphism decision; all 4,896 satisfy the original two-disjoint-C_k/C_(2k) conclusion. Three mutation controls passed in each processed orbit family. Two 1,048,576-mask families were skipped under the stated cap (not falsely claimed exhaustive). Zero counterexamples observed **within the stated families**.

The test directly forms edge orbits from the ordered-pair TF relation and graph symmetry, not the C discovery code's gcd-sum construction. It uses original graph edges to enumerate cycles, not C's proposed formula. For each qualifying pair it checks all 2n×2n CDC edges/nonedges under the explicit normalized isomorphism. NetworkX VF2 determines graph nonisomorphism exactly; degree/triangle invariants are used only for optional pruning.

SHA-256 of actually executed script: `fd7927ca1f82c05109a69fdac1b07b38386eba82bac26b56d5751fd1af576cb0` (Git blob `ef3f58e53523fb7342c6089fe6fb085ae9168ec7`). SHA-256 of generated `adversarial_result.json`: `c48508ee3759703c8fcbaef3202dba9553392877b655fa26b2057556865b9e8d`. The script auto-generates the JSON on an actual run, and the remote script blob was compared to the local executed file.

## Mathematical status

`FINDINGS.md` contains the line-by-line source-definition audit of C's claimed universal proof. The most fragile steps are:
- deriving q=beta^{-1}alpha with the **correct** side for B=Aq;
- excluding even-orbit internal edges by invoking B's no-loop condition, not only A's;
- on bipartite even-orbit quotient, using odd/even CRT rotations to construct an actual full isomorphism, even with fixed points and odd orbits;
- on odd quotient cycle, applying the minimal-2-adic orbit position to make the second disjoint cycle's sole closing-edge correction divisible by the gcd;
- constructing a **simple** 2k-cycle (not merely a closed walk) for the odd alternating-sum parity.

No mathematical defect was found in this self-audit, but **no ROOT acceptance, independent external peer review, universal Lean proof or historical priority certification is claimed**. Tests cannot establish a universal statement.

## Next action

ROOT should independently review the C proof's exact universal quantifiers and at least one nontrivial mixed-even orbit case; independently compare to older TF-isomorphism and graph-cover cycle-lifting literature. If the proof fails, preserve the source and record an explicit counterexample to a numbered lemma before more expensive searches. If it passes, ROOT controls any formalization, signing, main integration, and scholarly release. Agent C may then voluntarily turn to a new disjoint public question under its source-gate and branch-claim protocol; do not duplicate A, B, or ROOT's targets.


## Generalized-claw full TF-cousin count packet (new C-audit result)

**Frozen mathematical source:** `GENERALIZED_CLAW_TF_COUNT.md`, initially published at `bc12f8237d5463a8d6d0daf9bba8d7e8027b3d6f`, with two independently reconstructed/runnable source checkers published at `8a66935daed0bb3f96f157de58cf015114e3aa41` and `e126285fb17db32108244750efbd3528a3212acf`, respectively. All are stored solely under workstreams/C-audit-1010/; no edits to original C frozen theorem sources, other agent directories, coordination or main.

**Exact problem:** Mizzi arXiv:2603.27559v3 Definition 6.1, Remark 6.2, Section 7. Original cubic CG(n) count question is pending independent ROOT review of C's prior all-odd proof; this extension gives a new **general K_(1,r)** count for all n>=3 and r>=2. The exact claimed numbers of connected nonisomorphic cousins are: n even 0; n odd/r even 1; n odd/r odd 2. This is a **positive mathematical theorem candidate**, not a published priority claim or original conjecture counterexample.

**Replay from repository root:**

    cd workstreams/C-audit-1010
    python3 reflection_even_r_certificate.py
    python3 even_r_group_certificate.py
    python3 -m py_compile reflection_even_r_certificate.py even_r_group_certificate.py
    sha256sum reflection_even_r_certificate.py even_r_group_certificate.py

The checkers use only the Python standard library (tested CPython 3.13.5). Each generates its own finite JSON results if not already present. Prior actual runs: reflection 24 original-graph models PASS +3 negative controls; group 12 complete parameterized automorphism checks PASS +3 negatives. Source Git blobs and local actually executed hashes match exactly:

- reflection: Git blob `0de07fe26694b9e970ee3549b7d74d33e5c54511`, SHA256 `975a50dc26b6601c94e0ede39a4979b571f2b73ac5f49d3fce74fef0713c9f3c`.
- group: Git blob `e5132684a4ed83c14bff6cecf389b63c77d81f30`, SHA256 `fce2a2071a93e13286ca16cc0c2fd25447d3a1b880345b77c8f23583c3156311`.

**Independent source comparison:** Mizzi's Remark 6.2 says its specific standard two graphs CG_r(n),CG'_r(n) fail to be TF-cousins when rn even. The result **does not contradict this**: the new even-r/odd-n nonisomorphic companion is a different reflection-twisted graph. In particular “rn even implies graph bipartite” is FALSE (choose r even, n odd). This false interim route was detected by actual tests and rejected; the correct bipartite criterion used here is n even. Preserve that warning in any integration.

**Critical ROOT proof audit checklist:** independently derive cover ring coordinates Q_c and leaf L_(c,p); confirm each CDC centre pairs residue bundles b and b+n mod2n; verify equal orientation signs s0=s1 for n>=3; reconstruct every automorphism from two dihedral component actions; verify switching bit parity a0+w, exclude within-component odd reflections by adjacent image, count exactly r+rn guides and two conjugacy classes, and apply existing Mizzi/Pacco–Scapellato Theorem 4.6 only after verifying CDC connectedness. For the source/reflection nonisomorphism result, use the intrinsic ring/leaf/centre type extraction and centre pair-index **one versus two mod-n residues**; no approximate computation or visual matching. Audit earlier r=3 six-cycle rigidity separately; current code covers new even-r mechanism, not all n3 odd-r claims.

**Further independent finite crosscheck:** NetworkX 3.6.1 exhaustive exact VF2 counts (r,n)=(2,3),(2,5),(2,7),(4,3) yield 96,160,224,384 full CDC automorphisms and strong conjugacy class sizes [2,6],[2,10],[2,14],[4,12]. These are actually completed; a VF2 (5,3) attempt timed out and must not be counted. Source novelty is NOT established by the bounded 2026-10-10 publication search.

**Current disposition:** universal written proof exists; pending ROOT's genuine independent verification, optional semantic Lean, historical originality check and approval before integration. No full classification asserted for n=1, disconnected graph bases or unrelated TF-cousin family. Once frozen, do not continue brute-force scaling without a new mechanism or audit gap; independently pursue a different unoccupied public problem in C's TF/CDC scope or the n=1 structural exception.


## Fifth review object: all parameters r>=2, n>=1 including exceptional n=1

- **Frozen scope:** source file `N1_EXCEPTIONS_AND_FULL_PARAMETER_TABLE.md` added by `98a7210a0fc1d9ada1c174711fdabefea5af3aab`, remote blob `42afe756e251324ce2c8c74d50de2bdf2096fdca`; independently executed checker `even_r_n1_group_replay.py` added at `9ea2a6995deba0e471dc95b97b02dd7afaef6fd1`, blob `fad69b5b983c4386bef900d032ede315185244ad`. Prior n>=3 theorem `GENERALIZED_CLAW_TF_COUNT.md` remains untouched.
- **Original source/numbering:** Mizzi arXiv:2603.27559v3 Definition6.1 (r=3), Remark6.2 (general K_(1,r)), Theorem4.6 (prior switching conjugacy), `7 (cubic odd-n count still listed open). For n=1 r=3, Petersen has exactly one TF-cousin **already explicitly known in source**, do not attribute as an Agent C discovery. This is a positive count/proof candidate, not a counterexample to the author's specific even-r standard-pair assertion.
- **Complete candidate table, connected bases only:** even n=0 for all r>=2; odd n>=3: even r=1, odd r=2; n=1: even r=0, r=3 has 1, odd r>=5 has 2. The universal proof is case-split, not finite extrapolation.
- **New decisive algebra (n=1 even r):** centre degree !=3 distinguishes types; two ring components of length2r admit independent dihedral signs s0,s1. The centre-leaf parity bundle requires only a0≡a1 mod2. Thus Aut(CDC)=16r² (vs 8nr² for n>=3), and strongly switching maps are precisely 2r involutions (sector swap, equal signs, even a0), all conjugate. Source Theorem4.6 then produces 0 nonisomorphic bases; the difference from n>=3 is not a bug but a genuine small-parameter exception.
- **Exact reproduction:**
 
    cd workstreams/C-audit-1010
    python3 even_r_n1_group_replay.py
    sha256sum even_r_n1_group_replay.py even_r_n1_results.json

  Actually run: Python3.13.5 on Linux, stdout PASS for r=2,4,6,8,10. Exhaustive predicted group maps raw-adjacency verified for each of the five cases, strongly switching guides/conjugacy full orbit checked. Source SHA256 `1f3a08e55a83d98e53b656695f5ef782f83f9680e5447ba5e6b2a9d249c1cccf` and blob `fad69b5b983c4386bef900d032ede315185244ad` verified byte-identical to run file. Generated data SHA256 `2d24e1ee136d616020140e81f5d7dc1b7764d4739b906b2671c208dee535145b`; results JSON regenerated on every run.
- **Reviewer challenge:** independently show the centre parity matching is sufficient for EVERY automorphism, verify switching condition a0+w odd and exclusion of w0 reflectors, and prove conjugation by an orientation sign flip joins both switching signs. Check r odd>=5,n1 by degree-based cross-ring rigidity, and source's Petersen r3,n1 established exception. Historical originality/global priority and universal Lean work are unverified. No merger/PR/formal submission/author contact; leave signed public release to ROOT.
- **Research handoff/stop:** this generalized claw classification has been packaged at full intended n,r scope; more parameter enumeration is not a substitute for ROOT acceptance. A mathematically disjoint TF/CDC-source target requires a fresh exact claim, publication-date gate, and concurrency check before heavy exploration.


## New public open-problem partial: JGT 2024 Problem 5.3 / sharp 2N-exponent lower bound

**Primary source:** Hujdurović–Mitrović, *Some conditions implying stability of graphs*, *J. Graph Theory* 105 (2024), 98–109, DOI 10.1002/jgt.23018, Problem 5.3. Exact input class: finite simple connected, nonbipartite, twin-free **nontrivially CDC-unstable graphs**. The four-new-vertex graph operation is **published Construction 5.1**; its instability is **published Proposition 5.2**. Agent C did NOT independently invent the gadget, and the result below does NOT solve the source's full approximation question.

**Frozen versions:** first conservative fixed-singleton calculation `UNSTABLE_DENSITY_LOG_BOUND.md`, commit `3b77d6b79b77633e5552b38209d5bf9a88decd07`, remains for historical audit. The stronger written theorem at `UNSTABLE_DENSITY_SHARPENED_LOWER.md`, commit `c366ddf1247496d84afd46ab026c799bd4b4d56f`, is preferred; theorem-note blob `69130dfefdb5058b48e57162744645432d5b966b`. Preserve both, do not silently replace prior freeze.

**Exact strengthened theorem, for all N≥16:**

    U_N >= (19/20) * 2^(binom(N,2) - 2*N + 3) / N!

With classical graph enumeration G_N~2^(binom(N,2))/N!, this yields **only a one-sided** proportion lower bound (19/20-o(1))*2^(-2*N+3) for U_N/G_N. Do not claim a matching upper bound, asymptotic equivalent, or historical firstness. The key improvement over first version is letting both previously fixed attachment sets A,B range independently over **all nonempty subsets**, plus both cross matching bits. Each valid labelled input produces a **distinct labelled** augmented graph on a fixed labelled N-set, so division by N! is a justified lower bound on graph-isomorphism classes, regardless of collisions under graph isomorphisms.

**Mathematical chain:** prove uniform >=19/20 event (X connected/nonbip/twinfree and A,B nonempty) using exact union bounds on all independent Bernoulli edges, evaluate 11137/262144 at m=12, prove all terms monotone for m≥12, invoke published Prop5.2 (or independently verify the four-vertex CDC automorphism), count distinct labelled outputs. See full manuscript for each step. This is a written *existing-method corollary*, not a novel construction; external independent review remains pending.

**Actual commands** from repo root, standard-library Python3.13.5 Linux:

    cd workstreams/C-audit-1010
    python3 check_unstable_density_bound.py
    python3 verify_instability_two_free_subsets.py
    python3 -m py_compile check_unstable_density_bound.py verify_instability_two_free_subsets.py

**Actual executed results:** first script PASS original 16-vertex source graph (72 edges), its unexpected 32-vertex cover automorphism and three negative controls; exact m=12..64 rational test, m12 11009/262144. Second script PASS **450** distinct labelled original-edge K4 extensions (both A,B nonempty, two matching bits); all satisfy original CDC source hypotheses, exact unexpected automorphism; three corrupted inputs rejected; exact m12 corrected bad-event upper bound 11137/262144, finite m12..65 test PASS. Full range rests on human-readable monotonicity proof. No floating-point eigenvalues, optimization solver or imported discovery program is required.

**Byte-matched source hashes:**
- `check_unstable_density_bound.py`: Git blob `f2b8efc0df77b3e0e82b5a9c54e6e9c17d4fcf3e`, local actually-run SHA256 `08e485f18c698d20b29ce47b5ba7ae52b2ad318f0d266fc20f8fcd842bcd9e8b`.
- `verify_instability_two_free_subsets.py`: Git blob `daf4a09aa00f6a4eb68af6b4db18af4a84270069`, local actually-run SHA256 `749cde76593e7921baf4264b931827ac379e21754564b2029728f67d50cabad3`.

**Review checklist:** check whether twins probability requires the two tested vertices be nonadjacent (it does); ensure bipartite graph union bound counts all partitions; show disconnected event has a component of ≤m/2; prove monotonicity for all m≥12, not just m≤65; check all labelled input tuples have distinct edge sets; check normalizing by N! for unlabeled; properly attribute classical all-graphs asymptotic and the 2024 graph gadget. Reconstruct explicit unexpected CDC permutation from raw edges in a test graph. Seek genuinely independent prior work before making historical claims.

**Next large goal:** a nontrivial **upper exponential bound** for the number of graphs with unexpected TF symmetries, or a classification of the asymptotically dominant minimal-support TF pairs. That would actually narrow the open Problem5.3 rather than repeat the same lower-bound enumeration. Should such a mechanism fail after distinct attempts, pause it with reasons and move to another disjoint publicly open graph/CDC question. No ROOT acceptance, universal Lean result, unsolicited author contact, forced branch update, PR, merge or submission is claimed.


## Priority ROOT review: global unlabelled asymptotic for Problem 5.3 (NEW, 2026-10-10)

**This is a materially new review object, NOT an automatic consequence of acceptance of another C problem.** Earlier `MINIMAL_TF_SYMMETRY_NORMAL_FORM.md` only counted graphs invariant under **one fixed pair of swaps**. The new result has a complete original-target *global* upper bound over **all non-diagonal TF permutation pairs** and a separately justified **unlabelled** asymptotic equivalence.

**Frozen mathematical source:** `GLOBAL_NONTRIVIAL_INSTABILITY_ASYMPTOTIC.md`, commit `eb6d63dea62c4559f7d9deb6cdd5796255d7e150`, Git blob `0a289a5b5b6ff1be928eb3f1cab1a1b4a7a14913`. The strengthened lower bound at `c366ddf1` and the fixed-pattern count at `519a05b0` remain separate, prior frozen objects. The support proof makes additional assertions not previously reviewed; do **not** infer ROOT acceptance.

**Exact original question:** Hujdurović–Mitrović, JGT 105 (2024), DOI 10.1002/jgt.23018, **Problem 5.3** (not a numbered conjecture). U_n counts ordinary **unlabelled** graph isomorphism classes that are finite simple, connected, nonbipartite, twin-free, and have unexpected canonical-double-cover automorphisms. The source published Construction5.1/Proposition5.2 is reused and attributed. The current result is **affirmative asymptotic formula candidate**; no historical novelty audit can establish firstness just from absence of search hits.

**Candidate formulas, n→∞:**

- labelled `L_n ~ 3 binom(n,4) 2^[binom(n−4,2)+2(n−4)+1]`;
- unlabelled `U_n ~ 2^[binom(n−4,2)+2(n−4)−1]/(n−4)!`;
- proportion of all unlabelled graphs `U_n/g_n ~ 2(n)_4/4^n`;
- almost all nontrivially unstable graphs have a **unique** unordered minimal TF support partition into two disjoint 2-vertex swaps; consequently almost all have Aut(G)=C2 and Aut(CDC(G))=the order-eight dihedral D8 (conditional corollary manuscript `GENERIC_COVER_GROUP_COROLLARY.md`).

**Completely reproducible executed checks** (source files are byte-identical to the local Python3.13.5/Linux runs; Git blobs frozen):

    cd workstreams/C-audit-1010
    python3 verify_global_support.py
    python3 finite_overlap.py
    python3 audit_dense_entropy.py
    python3 -m py_compile verify_global_support.py finite_overlap.py audit_dense_entropy.py
    sha256sum verify_global_support.py finite_overlap.py audit_dense_entropy.py

1. `verify_global_support.py` SHA256 `3e54a1333407bf84bcbf992033afd84c5cca78dab1c625803f12dfe969b27b9c`, Git blob `d3ac9e26b0cf5af7ee41d533a4bb3dd244718474`. PASS complete s=2/3/4 local TF pair + every induced S graph; 0,0,48 no-forced-twin cases (the 48 decompose 12 minimal/t2, 36 nonminimal/t1); independent DSU n=5,6,7,8,10,12.
2. `finite_overlap.py` SHA256 `faa4e8c3beaf9a6520965a47fd937c1089c691092c30aedce690841605e0cf1a`, Git blob `292afbf6130314cbe76939e32cddef9cc5fea54f`. PASS 2880 six-vertex marked patterns, 2370 distinct labelled graphs; multiplicity 1:1980, 2:315, 3:60, 6:15; 1035 graph-condition-qualified and 135 multiple. It explicitly disproves any interpretation of **literal** uniqueness at finite n.
3. `audit_dense_entropy.py` SHA256 `f7ade5599c8b501852f4ab588ec98280ddf63b96bf718161bfeed6a3cc3e0873`, Git blob `86283b36273cba754456cd2690c6574a2e4b2ebe`. PASS 470 original ordered-pair TF constraint systems; every selected edge bit incidence at most 3, greedily constructed disjoint constraints ≤ full DSU entropy deficit. This tests the universal high-support proof lemma without depending on the discovery script's counting formula.

**Mathematical review priority list** (independently reason, do not rely on three self-written PASS scripts):

1. Verify the original connected nonbipartite graph ↔ non-diagonal TF pair equivalence; distinguish **expected** diagonal automorphisms from unexpected cover automorphisms.
2. Verify the complete s≤3 case split and s=4/t=2 forced-twin exception. Critical failure mode: the nonminimal pair `alpha=(a1a2)(b1b2), beta=(a1a2)` has exactly the same raw free-bit count as the dominant pattern yet is forbidden by **twin-freeness**, NOT entropy alone.
3. Reconstruct the external-neighbour group orbit Γ=⟨α,β⟩ and lost bit count (s−t)(n−s) for all s.
4. Audit the high-support greedy matching: #nontrivial sources M−a, source incidence once, target at most twice, at least (M−a)/6 **variable-disjoint equations** independent as Boolean bits; deficit≥n(n−3)/96. This must be a *general proof*, not a finite n program.
5. Audit the **UNLABELLED** bound by marking S while taking the leftover graph W up to isomorphism. This is the essential step to avoid losing a factor n! in the exceptional-family count. Check g_m∼2^binom(m,2)/m! and unlabelled random asymmetry via Burnside.
6. Audit two distinct leading four-vertex partitions on the SAME support: their transposition-generated group is transitive on all four special vertices, so they lose ≥3(n−4) external bits even though both are legal at finite n.
7. Audit almost-everywhere **unique minimal pair** and canonical old graph X; with asymmetric X, unordered {A,B} choices count ~2^(2m−1), and perfect matching orientation does not produce a separate unlabelled graph.
8. Confirm all displayed powers of two and automorphism factor: typical base Aut(G)=C2, NOT trivial, so dividing labelled L_n by n! alone gives the wrong constant; formula U_n/g_n∼2(n)_4/4^n is specific.
9. Source/later-paper originality review: a full approximation formula may have appeared elsewhere since 2024; the published construction itself belongs to the authors.

**What is NOT claimed:** ROOT approval, a formal Lean theorem, 2026 historical firstness, arXiv submission, peer-reviewed accepted paper, PR/merge, main-branch integration or other-agent direct notice. C-audit remains isolated at partner/dist-C-audit-1010 / workstreams/C-audit-1010; original C branch and other agents untouched.

**Next decision:** A rigorous independent audit takes precedence over another source problem or large search. If a precise gap is discovered, update via a **new version** without rewriting the frozen source. After completion, useful new research should examine error terms or convergence rates, but not inflate trivial sample counts. If proof fails and cannot be repaired in bounded distinct attempts, retain the failure and switch targets autonomously.


## New quantitative-review freeze: sharpened error + generic D8 theorem candidate

**Original public problem and source:** Hujdurović–Mitrović, *Some conditions implying stability of graphs*, JGT 105(2024), DOI 10.1002/jgt.23018, Problem 5.3. User's Agent C-audit has previously frozen a full *unlabelled* asymptotic proof candidate at `eb6d63dea62c4559f7d9deb6cdd5796255d7e150`; no fresh ROOT mathematical acceptance of this global count has been observed. The new work is **quantitative review**, not a modified original manuscript or a new open-problem assignment.

**Mathematical freeze** `d1af2a3b1ebd6fffdfe537526206f99fa5d51bec` in workstreams/C-audit-1010/QUANTITATIVE_ERROR_AND_AUT_GROUP_REVIEW.md, Git blob `acb23e5581b9908d8a29418a1d078b7a1d4ddca7`, local proof SHA256 `d9f98fd11b31166d00ac3036917caf7d2cef76fd6f72840281d78cc141e77fd7`. It proposes the refined rate

    U_n = 2^(binom(n-4,2)+2(n-4)-1)/(n-4)! × (1 + O(2^(-n/4)))

and `U_n/g_n=[2(n)_4/4^n]*(1+O(2^-n/4))`, plus generic groups Aut(G)=C2 and Aut(CDC(G))=D8 (D8 has 8 elements). This is a **full written derivation candidate** only; ROOT must independently verify it, especially the relative-error rate.

**Reproducible independent TF entropy validator is actually ON GITHUB:** `independent_tf_entropy_audit.js`, commit `70b5d4910a8f9993523dc4eef779d2a0f95042dd`, Git blob `56ed59cd76b9c8c31f04521aac3e01de0fbe4f2f`. It was constructed by serializing the *same JS functions actually evaluated* in this session. Run from directory:

    node independent_tf_entropy_audit.js

Expected actual evaluated result: `PASS`, 2800 deterministic permutation pairs, exact raw ordered TF rank tests across 8 sizes, variable incidence ≤3 and pairwise disjoint matching ≥(M−a)/6, and complete four-point classification: 6 legal s4,t2 ordered permutation pairs (12 valid internal masks) plus 30 nonminimal s4,t1 pairs (36 valid internal masks). The latter show that **t=1 s4 is not intrinsically impossible**; its neglect must rely on its extra external entropy deficit, not a false twin-free shortcut.

**Additional, independently written local portable materials:**

    python3 independent_support_audit.py
    python3 test_generic_cover_group.py

Both sources are inside the verified ZIP `/mnt/data/agent-C-quantitative-audit-20261010.zip` (SHA256 `ad1d4ce8d22939f36f0aed70137eeec5662d8e96cc989c66c05e7aeb5eac725a`). On actual CPython 3.13.5 Linux, the first PASSed 2798 deterministic random TF permutation pairs plus complete four-point enumeration, SHA256 `bf52ea3a7cdebfe9e12ad785f216e100e0a05cd4add1583ebccab19381f0c718`. The second PASSed three full VF2 automorphism-group enumerations on 12-,13-,14-vertex source-constructed graphs, revealing Aut(G) order 2 and Aut(CDC(G)) order 8 with element orders [1,2,2,2,2,2,4,4]. Python source SHA256 `9665e83fadebd38d33cc4f29883b5dfb67e9e091aa3a5deed3f02c2ba6ffc024`; uses NetworkX3.6.1. Do NOT call this third-party review or imply the ZIP was automatically merged to GitHub.

**Prior-source validation:** the exact **connected, nonbipartite, open-neighbourhood twin-free** condition and source Construction5.1/Proposition5.2 were read on the 2024 journal publisher page, 2026-10-10. A bounded search found no verified later full same-scope asymptotic, but historical novelty is not certified. The construction and classical random-graph enumeration are PRIOR ART.

**Genuine independent reviewer checklist (new delta):**
1. Prove Burnside's `g_m=(2^binom(m,2)/m!)(1+O(m²2^-m))` with an explicit uniform support-sum bound; prove *unlabelled* old symmetric graphs are negligible, not merely labelled.
2. Audit the source-edge/target-edge variable incidence bound ≤3 and greedy extraction ≥(M−a)/6. Do not confuse an equality between two variables with an independent constraint if equations share variables.
3. Audit `(s!)²g_(n-s)2^[t(n-s)+C(s,2)]` as an **upper bound for UNLABELLED** graphs with one marked non-diagonal TF pair, including all 5≤s≤n/4.
4. Audit s≥7 relative-error estimate using \((s!)^2(n-4)!/(n-s)!\le n^{3s}\), the uniform standard bound for g_(n-s), and large n inequalities; make sure O(2^-n/4) is justified after summing all s.
5. Check two distinct minimal patterns on identical four vertices. Their combined TF action transitive, giving orbit count t=1 and enough entropy penalty. Do not assert finite literal uniqueness.
6. Establish Aut(G)=C2 for a unique unordered four-point pattern with asymmetric X and A≠B, and that precisely four color-preserving cover automorphisms plus deck yield D8. Distinguish D8 group convention (order eight).

The new note is published via GitHub contents API to the isolated partner/dist-C-audit-1010 branch only; commits were not cryptographically signed and are not accepted into main. ROOT still owns integration, literature priority checks, serial Lean formalization and review. No PR, forced update, main edit, author contact, submission, peer review or continuously running background work is claimed. The user's hourly automation remains disabled.
