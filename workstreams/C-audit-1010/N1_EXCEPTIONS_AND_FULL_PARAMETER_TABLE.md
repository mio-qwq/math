# Completing the generalized-claw parameter table, including n=1

**Agent C-audit-1010, 2026-10-10 UTC.** Complete written **theorem candidate** and exact diagnostics, **not** independent ROOT acceptance, Lean formalization, peer review, journal submission, or historical priority certification.

## Exact target and full candidate classification

Russell Mizzi, *Lifting and Folding: A Framework for Unstable Graphs and TF-Cousins*, arXiv:2603.27559v3 (10 September 2026), Definition 6.1, Remark 6.2 and Section 7 (https://arxiv.org/html/2603.27559v3). Mizzi proves a specific standard companion iff the cubic parameter n is odd, describes generalized K_(1,r) claws, and explicitly leaves the full odd-n number of TF-cousins unknown. The paper's Theorem 4.6 / Remark 4.7 uses earlier Pacco–Scapellato switching-guide correspondence and must be attributed.

For generalized claw G_r(n), with all integers r>=2 and n>=1, count **connected simple undirected** H such that CDC(H) ≅ CDC(G_r(n)), up to ordinary graph isomorphism, **excluding G_r(n)**.

| n | r | Exact number of TF-cousins (candidate) | Mechanism |
|---|---|---:|---|
| even n>=2 | every r>=2 | 0 | original source connected bipartite |
| odd n>=3 | even r>=2 | 1 | two-ring-bundle full group proof, `GENERALIZED_CLAW_TF_COUNT.md` |
| odd n>=3 | odd r>=3 | 2 | cubic six-cycle rigidity or larger-centre degree rigidity |
| n=1 | even r>=2 | 0 | n=1 exceptional full automorphism/conjugacy theorem, proved below |
| n=1 | r=3 | 1 | **previously published Petersen/Desargues result**, not a new finding |
| n=1 | odd r>=5 | 2 | cross-ring rigidity applies already when n=1 |

The n>=3 clauses are separately written in [GENERALIZED_CLAW_TF_COUNT.md](GENERALIZED_CLAW_TF_COUNT.md); this note supplies the missing n=1 proof and exact executable checks. All results remain **written proof candidates** pending independent review. This is not a new counterexample or a theorem for arbitrary CDC-related graphs.

## Original-definition graph for n=1 and even r

Fix any **even r>=2**, and let h=r and n=1 in the source. The original G has a cycle of length 2r on ring vertices R_0,...,R_(2r-1), leaves L_p (p mod r) adjacent to antipodal ring pair R_p,R_(p+r), and a **single centre** C_0 adjacent to all r leaves. It has 3r+1 vertices. For even r, it contains the simple 5-cycle

    C_0 — L_0 — R_0 — R_1 — L_1 — C_0,

so it is connected nonbipartite, and X=CDC(G) is a connected bipartite graph on 6r+2 vertices.

The centre vertices in X are precisely the degree-r vertices (degree 2 if r=2); leaves are the remaining degree-three vertices adjacent to a centre; rings are the other degree-three vertices. Thus **every** cover automorphism must preserve these three types.

Because the antipodal ring offset r is even, the cover-ring-induced subgraph has **two disjoint C_(2r)** components Q_0 and Q_1. A leaf in X has its two ring neighbours in precisely one of those components, and each ring vertex has a unique leaf neighbour. Thus the image of both ring components determines every leaf image, and the resulting leaf incidence determines both centre images.

## Exact full cover automorphism group

Index Q_c by t mod 2r with cover ring vertex (R_t,layer=t+c mod2), c∈{0,1}. Every cover automorphism induces an interchange bit w∈{0,1} and an independent dihedral map on each ring cycle:

    (c,t) ↦ (c XOR w, s_c*t+a_c mod 2r),
    s_0,s_1∈{+1,-1}, a_0,a_1∈Z/(2r).

Each cover leaf is uniquely identified by its antipodal ring-neighbour pair, so no extra leaf choices remain. The two cover centre vertices meet precisely **opposite parity** leaf bundles across Q_0 and Q_1. Preserving this incidence is equivalent to

    a_0 ≡ a_1 (mod 2).

Indeed, in the general n>=3 case the full bundle matching forces equal orientation signs; for n=1, modulo 2 the signs ±1 are identical and the two signs remain independent. Conversely, direct substitution in the original edge relation proves that every parameter tuple obeying the displayed parity congruence extends uniquely to a genuine graph automorphism of X. No unclassified automorphisms remain: the type structure constrains every automorphism to this parameterization.

There are exactly 2 choices of w, 4 choices for the ordered pair of signs, 2r choices of a_0, and r parity-compatible choices of a_1:

    **|Aut(X)| = 16 r².**

This is a universal theorem for all even r>=2, n=1; its proof does not depend on a finite enumeration.

## Exactly 2r switching guides in one conjugacy class

A ring vertex's canonical-cover layer changes by a_0+w modulo 2 under the above transformation, so it swaps the two cover colour classes exactly when a_0+w is odd.

If w=0 then a_0 is odd. Involutivity would require both ring maps to be reflections (a rotation with odd offset on an even ring cannot square to the identity), i.e., s_0=s_1=-1. But any reflection with an odd translation offset sends some ring vertex to its adjacent ring vertex, because

    2t ≡ a_c ± 1 (mod 2r)

is solvable when a_c is odd. Thus no w=0 switching involution is **strongly** switching.

If w=1 then a_0 is even; involutivity requires s_0=s_1=s and a_1≡-s a_0 (mod 2r). There are 2 signs and r even offsets a_0, hence **2r strongly switching involutions**. Each is strongly switching because all ring vertices move to the opposite ring component while leaf images remain leaves and centre images remain centres; no graph vertex is joined to a same-type image.

They form **one conjugacy class**. First, conjugation by a component-preserving translation (b_0,b_1), where b_0≡b_1 (mod2), changes the guide's offset to

    a'_0 = a_0 + b_1 - s b_0.

For each fixed sign s this acts transitively on all even offsets. Second, a component-preserving automorphism with **opposite orientations** on the two ring components (s_0=-1,s_1=+1, offsets zero) conjugates a sign + guide to a sign - guide. It is a valid automorphism precisely because n=1 does not impose equality of the two sector orientations. Consequently all **2r** guides are conjugate. The natural deck involution is one of them.

By the established Mizzi/Pacco–Scapellato Theorem 4.6 (valid because X is connected), conjugacy classes of strongly switching involutions biject with isomorphism classes of simple loopless connected base graphs with cover X. A single class containing deck therefore means **G_r(1) has ZERO nonisomorphic connected TF-cousins when r is even**.

## Odd r at n=1

For odd r>=5, antipodal ring offset r is odd; each leaf in X connects one ring vertex in *each* of the two ring C_(2r) components. Its single centre has degree r>=5, distinct from the remaining degree-three vertices. This is sufficient for the same cross-ring uniqueness argument used at odd n>=3: all cover automorphisms are the 4r lifts of the original D_(2r) ring symmetries and their deck companions. The strongly switching classes have sizes 1,1,r, giving **two** cousins. For r=3,n=1, this structural argument fails because the centre is cubic and not intrinsically distinguished: X is the Desargues graph, of order 240, and **the Petersen graph has exactly one TF-cousin** as explicitly recorded in the original Mizzi source Section 7 and Remark 4.8. This published exception is credited rather than claimed anew.

## Executable exact certificate (actually run)

Source: [even_r_n1_group_replay.py](even_r_n1_group_replay.py), a separate standard-library-only graph checker that directly constructs the CDC and the entire proposed 16r² permutation group, checks every raw cover edge image, selects every involutory strongly switching map, computes its **complete conjugacy orbit under every group element**, and asserts it is exactly the full guide set.

From this directory:

    python3 even_r_n1_group_replay.py
    sha256sum even_r_n1_group_replay.py even_r_n1_results.json

**Actual re-execution:** CPython 3.13.5 on Linux, 2026-10-10, r=2,4,6,8,10, **ALL PASS**. Results:

| r | cover vertices | constructed/checked automorphisms | strongly switching guides | conjugacy classes |
|---:|---:|---:|---:|---:|
| 2 | 14 | 64 | 4 | 1 (size 4) |
| 4 | 26 | 256 | 8 | 1 (size 8) |
| 6 | 38 | 576 | 12 | 1 (size 12) |
| 8 | 50 | 1024 | 16 | 1 (size 16) |
| 10 | 62 | 1600 | 20 | 1 (size 20) |

Python source **SHA-256** `1f3a08e55a83d98e53b656695f5ef782f83f9680e5447ba5e6b2a9d249c1cccf`; Git blob SHA1 `fad69b5b983c4386bef900d032ede315185244ad`. Generated local result JSON SHA-256 `2d24e1ee136d616020140e81f5d7dc1b7764d4739b906b2671c208dee535145b`. The checker re-generates the JSON, no third-party dependencies.

Independent finite NetworkX VF2 enumerations (Python 3.13.5 / NetworkX 3.6.1), **actually completed**: (r,n)=(2,1),(4,1),(6,1),(5,1),(7,1) give automorphism-group/guide conjugacy data (64,[4]), (256,[8]), (576,[12]), (40,[1,1,5]), (56,[1,1,7]). This is an internally independent algorithm, **not an external peer review**, and cannot replace the all-parameter proof.

**Limits and review:** do not claim the generic n=1 group formula extends to r=3. No universal Lean theorem compiled, no independent ROOT acceptance, no priority certificate. ROOT should scrutinize the n=1 bundle parity condition, sign-change conjugation, all-r group exhaustiveness and folding correspondence. This result concerns connected bases only and does not settle arbitrary graph-cover conjectures. No publication outside the disjoint audit branch, submission, PR, forced update, author contact or numbered 007/008 project.
