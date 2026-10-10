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
