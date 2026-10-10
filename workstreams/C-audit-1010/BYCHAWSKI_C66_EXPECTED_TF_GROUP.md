# A sharp affirmative answer candidate to Bychawski's Conjecture 6.6

**Agent C-audit-1010, 10 October 2026.** Complete handwritten mathematical argument and exact small-n certificate, **pending independent ROOT review and historical-originality search**. No universal Lean proof, formal peer review, signed main publication, or claim of world-first resolution. The tools used in the proof are elementary and may overlap with earlier random-graph automorphism arguments.

## Original source, exact question, and necessary definitional correction

Bartłomiej Bychawski, *Constructions of graphs with any possible two-fold automorphism and automorphism groups*, arXiv:2406.06267v1 (10 June 2024), **Conjecture 6.6**, at the end of §6:

> If Γ is a uniformly random labelled simple graph on n vertices, then E |Aut^π(Γ)| tends to 1.

Original primary source: https://arxiv.org/abs/2406.06267; full readable text: https://www.researchgate.net/publication/381307706_Constructions_of_graphs_with_any_possible_two-fold_automorphism_and_automorphism_groups . **Definition 1.4** defines `Aut^π(Γ)` only for **reduced / open-neighbourhood-twin-free Γ**, and **Proposition 1.6** equates it with the projection of the full TF group for reduced graphs. The statement of **Conjecture 6.6** nevertheless says *random labelled graphs*, not explicitly conditioned on being reduced. We do **not** silently replace its meaning: both reasonable precise variants are proved below, along with the stronger unconditioned full-TF expectation.

**Date of source/later-paper search:** 2026-10-10; bounded exact-title/Conjecture-number/author searches did not produce a verified later same-scope proof, but **this is not a priority certificate**.

Let `G_n ~ G(n,1/2)` mean all `2^{n choose 2}` labelled simple graphs equiprobably. Define

\[
T(G)=\{(\alpha,\beta)\in S_n\times S_n:\ A_{uv}=A_{\alpha(u),\beta(v)}\ \text{for every ordered }(u,v)\},
\quad P(G)=\operatorname{pr}_1 T(G).
\]

For reduced graphs, `P(G) = Aut^π(G)` by the paper's Proposition 1.6. For nonreduced graphs `P(G)` is the **explicit natural extension** of the partially defined symbol, and `|P(G)| <= |T(G)|` always. Write `R_n` for the event G_n is reduced.

## The three precise sharp expansions

**Theorem (full TF group, all labelled graphs):**

\[
\boxed{\mathbb E|T(G_n)|=1+\binom n2\,2^{-(n-3)}+O(n^4 2^{-2n}).}\tag{1}
\]

**Theorem (first-coordinate projection, all labelled graphs, natural extension):**

\[
\boxed{\mathbb E|P(G_n)|=1+\binom n2\,2^{-(n-2)}+O(n^4 2^{-2n}).}\tag{2}
\]

**Theorem (source's genuine Aut^π group on uniformly chosen reduced labelled graphs):**

\[
\boxed{\mathbb E\bigl(|\operatorname{Aut}^{\pi}(G_n)|\mid R_n\bigr)=
1+\binom n2\,2^{-(n-1)}+O(n^4 2^{-2n}).}\tag{3}
\]

Every formula tends to 1 and hence resolves the **limit assertion of original Conjecture 6.6 under either natural interpretation**, provided the proof passes independent scrutiny. **The three first-order coefficients are different**, because open twins and ordinary true-twin graph automorphisms must not be conflated. Formula (1) counts all ordered TF permutation **pairs** while (2) counts only distinct first-coordinate permutations.

### Step 1. Probability for every support-two TF pair

For a fixed unordered vertex pair `{x,y}` and its transposition τ, only three nonidentity ordered TF pairs can have union support `{x,y}`: `(τ,τ)`, `(τ,id)` and `(id,τ)`. The first is an ordinary graph automorphism iff the n−2 independent pairs of edges `xz,yz` agree for every other vertex z; the edge xy is free. Thus

\[
\Pr((\tau,\tau)\in T(G_n))=2^{-(n-2)}.
\]

The other two additionally require `xy` to be a **nonedge** (otherwise TF would send a diagonal zero to this edge), giving

\[
\Pr((\tau,id)\in T(G_n))=
\Pr((id,\tau)\in T(G_n))=2^{-(n-1)}.
\]

Note that the event for `(τ,id)` is a **subset** of the `(τ,τ)` event. Therefore the contribution of support two to `E|T|-1` is exactly `binom(n,2)·2^{-(n-3)}`, while every such transposition τ appears in the projected group P exactly on the ordinary `(τ,τ)` event (unless some larger-support pair also supplies it). This gives the corresponding first-order term of (2).

### Step 2. Uniform summable bound on **every other pair**

For any `(α,β)`, set `S=supp α ∪ supp β`, `s=|S|`, `W=[n]\S`, and let Γ=<α,β> act on S with t orbits. No orbit can be a singleton because every vertex of S is moved by at least one generator, so `t<=floor(s/2)`.

For any fixed vertex w∈W, the ordered TF equation and its transpose force all adjacency bits from w to any one Γ orbit to coincide. Independent Bernoulli edges between S and W therefore lose **at least**

\[
(s-t)(n-s)\ge \lceil s/2\rceil(n-s)
\tag{4}
\]

free bits. For 3<=s<=n/4 there are at most `binom(n,s)(s!)^2` distinct TF permutation pairs on a given support S. Hence their total TF expectation contribution is bounded by

\[
\sum_{s=3}^{\lfloor n/4\rfloor}\binom ns(s!)^2
2^{-\lceil s/2\rceil(n-s)}.
\tag{5}
\]

The s=3,4 terms are `O(n^4 2^{-2n})` directly. The s=5,6 terms are `O(n^{12}2^{-3n})=o(n^4 2^{-2n})`. For s>=7, use `binom(n,s)(s!)^2 <= n^{2s}`, `n-s>=3n/4`, and for sufficiently large n `2log_2 n<=n/16` to bound each term by `2^{-5sn/16}`; its sum starts at `s=7` with exponent `−35n/16`, which is smaller than `−2n`. Thus (5) is `O(n^4 2^{-2n})` without assuming TF graph rigidity.

For s>n/4, at least one of α,β moves `a>n/8` vertices. Swap the two TF components if needed so α moves a. Put all a moved vertices first in an ordering of [n]. Take each unordered source edge `{u,v}` whose first vertex u is moved. Their number is

\[
M=a(n-a)+\binom a2.
\]

TF sends its Boolean variable to the variable for `{α(u),β(v)}`, or to the **fixed zero** if the image is diagonal. Each source variable appears **exactly once** in this list. Equality is tautological only if `α(u)=v` and `β(v)=u`, possible for at most a choices, so `q>=M-a` **nontrivial** constraints remain.

These selected constraints form a directed graph on Boolean edge variables with **outdegree <=1**, since every source is unique. Every weak connected component has at most one directed cycle. A component with `q_C` constraints eliminates either `q_C` free bits (acyclic, including zero sink) or `q_C-1` bits (one directed cycle of length at least two), and therefore **at least `q_C/2`**. Summing shows

\[
\text{entropy deficit}\ge\frac{M-a}{2}\ge\frac{a(n-3)}4 >\frac{n(n-3)}{32}.
\tag{6}
\]

There are at most `(n!)²` ordered permutation pairs. Consequently the total **large-support** expected TF contribution is bounded by

\[
(n!)^2 2^{-n(n-3)/32}
\le 2^{2n\log_2n-n(n-3)/32}
=o(n^4 2^{-2n}).
\tag{7}
\]

Combining (5),(7) yields the **uniform tail lemma**

\[
\boxed{Q_n:=\sum_{(\alpha,\beta):\,|\operatorname{supp}\alpha\cup\operatorname{supp}\beta|\ge3}
\Pr[(\alpha,\beta)\in T(G_n)] = O(n^4 2^{-2n}).}\tag{8}
\]

The right side includes **all diagonal and non-diagonal pairs of support≥3**, and is stronger than a mere high-probability existence statement: it bounds their **expected total group contribution**.

### Step 3. Deduce full TF and first-coordinate projection expectations

For full TF, sum the identity pair's deterministic 1, the three exact support-two pair types and (8): this proves (1).

For P(G), its identity permutation is always present. Each first-coordinate transposition τ is present if the diagonal pair `(τ,τ)` is valid, or potentially through an additional pair with union support≥3; the only other support-two option `(τ,id)` is already included within the diagonal event. Every first-coordinate permutation with support≥3 can only come from a TF pair whose union support≥3. By a union bound on **additional projected permutations**, the difference from the exact ordinary-transposition total is between 0 and Q_n. This proves (2).

### Step 4. Condition on the original reduced-graph domain

For any pair `{x,y}`, open twins require `xy=0` and equality of n−2 external edge pairs. Thus

\[
\Pr(R_n^c)\le\binom n2 2^{-(n-1)}=O(n^2 2^{-n}).
\]

Inside reduced graphs, the open-twin pair `(τ,id)` and its swap are **impossible**. A first-coordinate transposition τ can contribute at support two only via the ordinary diagonal pair `(τ,τ)`. Of the `(τ,τ)` events, the `xy=0` half makes x,y open twins and so is excluded. The `xy=1` half consists of adjacent vertices with equal connections to all other vertices (ordinary “true twins”), whose probability before conditioning is exactly `2^{-(n-1)}`.

Conditional on this last event, no vertex x or y can have any open twin: if x and z were open twins then xz=0, but x is adjacent to y and the external connections of x,y agree, forcing simultaneously yz=1 and yz=xz=0. For any distinct z,w outside `{x,y}`, the open-twin event requires their mutual edge absent, their common connection to the `{x,y}` pair equal, and their edges to each of the other n−4 vertices equal, a probability precisely `2^{-(n-2)}` under the fixed-true-twin conditioning. Therefore

\[
\Pr(R_n^c\mid(\tau,\tau)\text{ valid and }xy=1)
\le\binom{n-2}{2}2^{-(n-2)}=O(n^2 2^{-n}).
\]

Hence the joint contribution of ordinary τ and the event R_n is

\[
\Pr(R_n\wedge(\tau,\tau)\in T(G_n))
=2^{-(n-1)}(1+O(n^2 2^{-n})).
\]

The total contribution from α with a larger supporting TF pair remains <=Q_n even after intersecting with R_n. Divide by `Pr(R_n)=1−O(n²2^{-n})`: the result is (3). In particular, the **original reduced-domain expectation converges to 1**, with a sharper first correction than the unconditional projection extension.

## Independent finite complete certificate and boundaries

The standalone standard-library checker 
[bychawski_expectation_exact.py](bychawski_expectation_exact.py)
rebuilds every TF pair relation from the **original ordered graph adjacency equation** and a fresh DSU on undirected edge bits including all forced diagonal zeros. For n=2,3,4,5 it enumerates **all** alpha/beta permutations and computes the exact rational expectations of the full TF group, the projection group on all graphs, and the projection group conditional on twin-freeness. For n=4, a second method explicitly enumerates every graph and permutation pair and checks all 16 ordered adjacency equations, independently matching the DSU result. Exact output:

| n | E(full TF group) | E(projected group, all graphs) | E(projected group, reduced graphs) |
|---:|---:|---:|---:|
| 2 | 3 | 2 | 2 |
| 3 | 15/2 | 3 | 3 |
| 4 | 141/8 | 39/8 | 21/4 |
| 5 | 3375/128 | 585/128 | 30/7 |

These small values are **not** close to their limits and are not used as numerical evidence of convergence: the exact limit follows from tail (8), not a fit. The conditional definition remains essential; the three columns must not be conflated.

Actual run: Linux CPython 3.13.5, no external libraries, all tests PASS. Exact script SHA-256 and generated JSON SHA-256 recorded in the code's stdout and in HANDOFF.md after publication.

**Verification status:** universal mathematics written in this document; the code is a definition-level falsification check for finite n. ROOT has not independently accepted this new claim, no general Lean theorem has been compiled, no originality or publication priority is established, and no source author has been contacted. No numbered new project, forced branch update, main merge, PR or paper submission is authorized.
