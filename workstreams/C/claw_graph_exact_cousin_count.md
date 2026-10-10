# Exact number of TF-cousins of the claw graph CG(n) for odd n

**Agent C | 2026-10-10 | universal affirmative proof candidate, NOT yet independently accepted.**

## Exact public open problem, status and attribution

Russell Mizzi, *Lifting and Folding: A Framework for Unstable Graphs and TF-Cousins*, arXiv:2603.27559v3 (10 September 2026), **Definition 6.1** and **Section 7**, explicitly asks for the number of nonisomorphic TF-cousin graphs of the claw graph CG(n) for *general odd n*. It establishes that CG(1) (Petersen graph) has exactly one, and that CG(n) for every odd n>=3 has **at least two**. The lower bound includes a companion CG'(n) and an extra folded graph containing triangles (credited in the source to V. Rozhoň and R. Šámal, obtained via Bolzano). These known examples are **not our new constructions**.

Primary source: https://arxiv.org/html/2603.27559v3#S6 ; https://arxiv.org/html/2603.27559v3#S7 (especially last three paragraphs), retrieved 2026-10-10. The classification-by-conjugacy theorem used at the end is **the source's existing Theorem 4.6 and Remark 4.7**, ultimately based on Pacco–Scapellato. We do **not** claim that correspondence as new. Bounded title/author/follow-up checks through 2026-10-10 did not disclose a subsequent exact all-odd-n result; historical firstness is unestablished, and a missed or unindexed prior result remains possible.

**Proposed new theorem (complete mathematical argument given below).** For every ODD integer n>=3, the connected cubic claw graph CG(n) has **exactly TWO** nonisomorphic TF-cousins, i.e. exactly THREE isomorphism classes of simple graph bases of its canonical double cover including CG(n) itself.

More sharply, for K=CDC(CG(n)),

    Aut(K) ≅ D_(6n) × C_2,                    of size 24n;
    # strongly switching involutions = 3n+2;
    their conjugacy class sizes = 1, 3n, 1;
    # nonisomorphic graph bases = 3;
    # nonisomorphic TF-cousins other than CG(n) = 2.

Here D_(6n) means the dihedral automorphism group of a circuit on **6n points**, of order **12n**. The n=1 exception is NOT covered: its CDC has 240 automorphisms and TWO guide classes, as already published.

**Outcome type:** a **complete written exact positive classification/proof candidate of an original open counting question**, not a counterexample. It is not a Lean theorem, signed main release, independent acceptance, or priority certification. Existing C result packets are left frozen.

## 1. Exact source-defined graph and its canonical double cover

Fix odd n>=3, let N=6n. The simple undirected graph CG(n) has vertices

    u_t,                         t ∈ Z/NZ,              [N circuit vertices]
    c_i,                         i ∈ Z/nZ,              [n claw centres]
    ell_(i,j),                   i ∈ Z/nZ,  j=0,1,2,    [3n leaves].

Its edges are exactly

    u_t -- u_(t+1);
    c_i -- ell_(i,j);
    ell_(i,j) -- u_(i+jn);
    ell_(i,j) -- u_(i+jn+3n).

Indices on circuit vertices are modulo N. This is literally the author's Definition 6.1, rather than an independently modified claw family. Hence |V(CG(n))|=10n and |E(CG(n))|=15n.

K=CDC(CG(n)) is the standard simple undirected canonical double cover: its vertices are (x,s), s∈{0,1}, and its edges join (x,s) to (y,1-s) exactly when xy∈E(CG(n)).

For each t∈Z/NZ define the following three **distinct vertex types of K**:

    U_t = (u_t, t mod 2);
    V_t = (u_(t+3n), t mod 2);
    L_t = (ell_(i,j), 1-(t mod 2)),

where r=t mod(3n) is represented by 0<=r<3n, i=r mod n, and j=floor(r/n). For each a∈Z/(2n)Z set

    W_a = (c_(a mod n), a mod 2).

Because n is odd, CRT gives a unique a mod2n for every pair (i∈Z/n, s∈Z/2), and a unique L label for each of the two copies of each ell_(i,j). Because 3n is odd, the U,V labels cover both layers of all u_t exactly once. Hence this is an **explicit bijection** from four tagged vertex sets of sizes N,N,N,2n onto all 20n cover vertices.

**Lemma 1 (synchronized-cylinder model).** Under this bijection the cover K has *exactly* these edges, and no others:

    U_t -- U_(t+1),            V_t -- V_(t+1),
    U_t -- L_t,                V_t -- L_t,
    L_t -- W_(t mod 2n).

The three leaves of W_a are L_a, L_(a+2n), L_(a+4n).

**Proof.** A circuit edge switches the layer when t is incremented, giving U and V circuits. The two antipodal circuit vertices for the chosen leaf have indices differing by 3n, an odd number; their equal layer 1-(leaf layer) corresponds precisely to U_t and V_t. The associated claw centre has the same layer t mod2 as both circuit endpoints. Its index i equals t mod n, so, because n is odd, (i,t mod2) is indexed uniquely by t mod2n. Every original edge is of one of the displayed three types. The bijection and degree-3 counts exclude further edges. QED.

## 2. Intrinsic identification of all four vertex types by C8 counts

The next step is a genuine **all-n structural proof**, not a computational graph-label heuristic.

**Lemma 2.** In K for odd n>=3, the number of distinct **simple 8-cycles** containing any fixed vertex is:

    3 for each U_t and each V_t;
    2 for each L_t;
    0 for each W_a.

**Proof (exhaustive by graph structure).** First suppose a simple C8 passes through W_a. The two neighbours of W_a on that cycle must be two **different** leaves L_t,L_s among {L_a,L_(a+2n),L_(a+4n)}. Upon removing W_a from that purported 8-cycle we would have a path of length 6 connecting these two leaves inside K−W_a.

No such path of length ≤6 can visit *another* W_b. Indeed, from either L_t or L_s, reaching W_b for b≠a requires at least four edges: L_t is adjacent to U_t,V_t,W_a only, and to reach a leaf of a different centre one must travel at least one edge along a U or V circuit. Both endpoints need at least four edges to reach W_b, giving path length at least eight. Therefore a path of length≤6 from L_t to L_s avoiding W_a must lie entirely in the graph of U,V,L vertices.

In that centre-deleted graph, moving between U and V via L keeps the index t unchanged, and only a ring edge U_t--U_(t±1) or V_t--V_(t±1) changes t by one. The least circular distance between t and s is **2n**. An L_t-to-L_s path must first enter a circuit and last leave it, using at least two non-ring edges, and so has length at least 2n+2>=8. This contradicts the required length 6. Hence **no C8 contains W**.

Now delete the W vertices altogether. We have two disjoint N-circuits U and V, with a *subdivided rung* U_t--L_t--V_t for every t. A simple C8 with no L lies within a single N-circuit, impossible since N=6n>=18. Each used L traverses a rung, and a closed path traverses an even number of rungs. Four rungs cost eight edges already; between different rung indices a simple cycle needs additional circuit edges, hence ≥12 total edges. Thus exactly **two** rungs are used.

If those rungs have indices t and s, their four rung edges leave precisely four circuit edges for the U and V paths connecting them. Since N>=18, both paths must have length two, hence s=t±2. Every such two-rung pair gives exactly one C8:

    U_t -- U_(t+1) -- U_(t+2) -- L_(t+2) --
    V_(t+2) -- V_(t+1) -- V_t -- L_t -- U_t.

There are exactly N such distinct cycles, indexed by t modN. Each U_t or V_t lies in the three starting windows t-2,t-1,t. Each L_t appears as either endpoint of a length-two window, giving two occurrences. Centres appear in none. QED.

The integers 3,2,0 are pairwise distinct, so **EVERY automorphism of K MUST PRESERVE the disjoint intrinsic sets** {all U,V}, {all L}, {all W}. No exceptional graph automorphism may covertly exchange a claw centre with a circuit vertex when n>=3.

## 3. Complete automorphism group

**Lemma 3.** Aut(K)=D_N×C2, of order 4N=24n.

**Proof.** Removing the intrinsically recognized L and W vertices leaves exactly **two disconnected N-circuits**, U and V. An automorphism of K either preserves these two circuits individually or swaps them. Its restrictions act as dihedral permutations of the circuit positions t: the U circuit index map is t↦eps_U t+b_U and the V circuit map is t↦eps_V t+b_V.

Crucially, L_t has as its **only circuit neighbours** the *matched* pair {U_t,V_t}. The image of L_t has circuit neighbours {U_s,V_s} for **one common index s**, so the two dihedral maps must satisfy eps_U t+b_U ≡ eps_V t+b_V (mod N) for **every** t. Hence the maps agree pointwise: both equal a single dihedral map

    f(t) = eps*t+b  mod N,   eps∈{+1,-1}, b∈Z/NZ.

It follows that L_t maps to L_(f(t)). Since W_a is uniquely adjacent to the triple of leaves whose indices are congruent to a modulo 2n, it must map to W_(eps*a+b mod2n). This is consistent for every dihedral map because congruence mod2n is preserved by both rotations and reflections.

Conversely, *every* common f as above and either independent choice of swapping or not swapping the U/V circuits preserves all five kinds of edges in Lemma 1. These are **all** automorphisms, with no hidden extras. The common dihedral map group has order 2N and swapping the two circuits is a central C2, yielding group D_N×C2 with order 4N=24n. QED.

We write an arbitrary automorphism as (eps,b,sigma), where sigma∈{0,1} swaps U and V when 1, maps L_t↦L_(eps*t+b), and maps W_a↦W_(eps*a+b mod2n).

## 4. Exhaustive classification of strongly switching involutions

**Lemma 4.** K has exactly **3n+2** strongly switching involutions, in exactly three Aut(K)-conjugacy classes of sizes **1,3n,1**.

**Proof.** K's connected bipartition in the explicit model assigns colour t mod2 to both U_t and V_t, colour 1-(t mod2) to L_t, and colour a mod2 to W_a. Consequently (eps,b,sigma) switches the two bipartition classes iff b is ODD. The choice of eps or sigma does not affect this parity.

**Case eps=+1 (rotations).** The dihedral map t↦t+b is involutive iff 2b=0 modN, hence b∈{0,N/2}={0,3n}. Since n is odd, the switching condition b odd selects **only b=3n**. Either sigma=0 or sigma=1 is allowed: both give an involution and are strongly switching. Indeed the circuit image has index distance 3n if the circuits are not swapped, which is never one; if they are swapped there are no U-V edges at all; and images of L and W stay within their own independent vertex types. These are exactly TWO strong guide elements.

**Case eps=−1 (reflections).** Every map t↦b-t is an involution, and switching again requires b odd, giving N/2=3n possible values of b. When sigma=0, one has for some t the congruence b−2t≡1 (modN) (since b−1 is even and N is even), so U_t is mapped to its adjacent U_(t+1). This is **not** strongly switching. When sigma=1, U-vertices map to V-vertices and vice versa, and all L- and W-vertices map within their own independent sets; therefore **none of the vertices is adjacent to its image**. Thus there are exactly **3n** strong guides of the form (-1,b,1) with odd b.

The two rotation-halfturn guide elements (1,3n,0) and (1,3n,1) are central in D_N×C2 because N is even; each forms a singleton conjugacy class. Conjugation of a reflection by a dihedral rotation t↦t+a replaces its parameter b by b+2a. As a ranges over Z/N, this sweeps **all odd values** of b, so the 3n reflection/swap guides form ONE conjugacy class. There can be no additional classes. QED.

## 5. Count all bases, not just the displayed examples

By the already-published **Mizzi Theorem 4.6 / Remark 4.7** (conjugacy-class correspondence, originating in Pacco–Scapellato and refined by Bychawski), the isomorphism classes of **LOOPLESS** base graphs whose canonical double cover is K are in bijection with the conjugacy classes of **STRONGLY switching involutions** of Aut(K). The strong condition specifically forbids folding an edge into a loop. Because CG(n) is a finite connected nonbipartite vertex-determining simple graph for odd n, its CDC is connected; all source hypotheses for that theorem are met.

By Lemma 4 there are exactly THREE such classes. One is the original CG(n), arising from its canonical layer-flip involution. The other TWO, and no further ones, are precisely its TF-cousins up to graph isomorphism. We have proved:

    For every ODD n>=3, # TF-cousins(CG(n)) = 3−1 = 2.

This sharpens the source's known lower bound at least two to an exact answer for **all odd n>=3**. Source already states the n=1 exception has one, so the complete odd-n answer is 1 when n=1, 2 when odd n>=3.

Neither the previously published lower-bound examples nor the conjugacy-base bijection are claimed as new. The **new element proposed for review** is the explicit synchronized-cylinder model, its C8-identifiable vertex types, the exhaustive D_N×C2 group computation, and the strong-guide class count.

## 6. Independently runnable exact checks

Two semantically different finite verifiers supplement (but do **NOT** replace) the universal proof.

**A. Source-definition-first, independent stdlib check.** File `check_claw_universal_structure.py` rebuilds CG(n) directly from Definition 6.1, rebuilds its CDC without a graph library, independently rebuilds the four-type model, checks the explicit vertex map on **every adjacency list**, directly enumerates all C8 and their incidence counts, checks **all 24n purported automorphisms** on every actual model edge and nonedge, enumerates the full proposed strong guide family, and computes conjugacy under those transformations. Includes **three deliberate damaged-input / invalid-guide tests**, which are required to fail.

Run:

    python3 check_claw_universal_structure.py

Actual CPython 3.13.5/Linux run **PASS** at n=3,5,7,9 with negative tests=3/3 rejected:

| n | CG vertices | CDC vertices | C8 | 24n automorphisms | strong guides | class sizes | companions |
|---:|---:|---:|---:|---:|---:|---|---:|
| 3 | 30 | 60 | 18 | 72 | 11 | 1,9,1 | 2 |
| 5 | 50 | 100 | 30 | 120 | 17 | 1,15,1 | 2 |
| 7 | 70 | 140 | 42 | 168 | 23 | 1,21,1 | 2 |
| 9 | 90 | 180 | 54 | 216 | 29 | 1,27,1 | 2 |

**B. Independent exhaustive automorphism search.** `claw_guides_conjugacy_probe.py` uses NetworkX **vf2pp_all_isomorphisms** to enumerate *ALL*, rather than the proposed 24n transformations, of the actual canonical double cover's automorphisms at n=1,3,5,7,9. The iterator ran to completion at each size (no timeout; the `complete` flag is true only on natural exhaustion). It then filters all strongly switching involutions under the original adjacency and complete conjugacy action. Results:

| n | Complete Aut count | strong guides | conjugacy sizes |
|---:|---:|---:|---|
| 1 | 240 | 11 | 10,1 (published Petersen benchmark) |
| 3 | 72 | 11 | 1,9,1 |
| 5 | 120 | 17 | 1,15,1 |
| 7 | 168 | 23 | 1,21,1 |
| 9 | 216 | 29 | 1,27,1 |

Run:

    python3 claw_guides_conjugacy_probe.py 1 3 5 7 9

NetworkX 3.6.1; CPython 3.13.5. Last n=9 exhaustive run took approximately 7.5 seconds. All **finite** automorphism iterators were exhausted, but that empirical fact is **not** the mathematical proof for arbitrary n.

The independent source `claw_n1_fold_sanity.py` additionally folds *all eleven* strongly switching involutions of the n=1 CDC, finds exactly two nonisomorphic base graphs, including the original, and reproduces the known Petersen/Desargues datum; it is a regression check, **not** a new theorem.

Neither script imports the other's automorphism derivation. Check exact remote file SHA256 and Git blob identifiers against the STATUS/HANDOFF receipt; no source or compilation hash should be invented. No Lean build or axiom audit has been performed.

## 7. Review attack points, limitations, follow-on directions

1. Check every vertex in the explicit **source CG(n) -> model K** map, especially that n odd is needed for the claw centre CRT identification and for bipartition parity.
2. Scrutinize the *only delicate geometric step*, the **no-W C8** claim: any purported C8 through W_a yields a length-six path between two L leaves differing by ±2n, which cannot visit another centre or bridge the circular index distance 2n. Check n=3 boundary and whether special short cycles can arise from two centre hops.
3. Check that C8 enumeration includes **ALL simple** 8-cycles and correctly handles N=18; the U/V/L/W incidence statistics 3/2/0 must be intrinsic.
4. Check the argument that matching neighbours of L_t force a **COMMON** dihedral action on U and V; consider both preservation and swap of the two circuits.
5. Check the layer colouring of U,V,L,W and the 2b=0 (mod6n) classification, especially n odd makes 3n an odd half-turn.
6. For reflected maps without U/V swap, explicitly solve 2t=b−1 (mod6n) to exhibit an adjacent image. For reflected maps WITH swap, explicitly check there are no U-V graph edges.
7. Check dihedral conjugacy parity classes and that half-turn+swap is central.
8. Confirm **the exact scope of Mizzi Theorem 4.6 and Remark 4.7**, especially the distinction between all involutions, switching involutions, and **strongly** switching involutions; verify the bijection is with isomorphism classes of **loopless** bases, excluding CG itself from the cousin count.
9. Verify no known later all-odd-n CG family classification (publisher revisions, author notes, follow-ups) was omitted; the bounded source check is not a proof of historical originality.
10. Do not claim that a networkx PASS or the finite 3/5/7/9 window establishes the all-n theorem: its *written* proof is Sections 1–5, and genuinely independent ROOT review remains pending.

**STOP/continuation:** This specific open counting problem has a complete all-odd-n written answer candidate; it is not useful to expand the same automorphism enumeration arbitrarily. Freeze manuscript/checkers for ROOT review, preserve earlier C results and their frozen SHAs, and move to a genuinely distinct original open question only after a fresh source/collision gate. No main edits, no merge, no peer review, no email/author contact, no submission, no numbered 007/008 project, no historical firstness claim.
