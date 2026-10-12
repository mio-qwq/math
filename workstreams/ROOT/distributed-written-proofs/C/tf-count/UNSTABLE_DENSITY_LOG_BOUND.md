# A second-order logarithmic counting bound for nontrivially unstable graphs

Exact coarse-counting consequence of a prior construction.

## Source and original question

Ademir Hujdurović and Đorđe Mitrović, *Some conditions implying stability of graphs*, **Journal of Graph Theory** 105 (2024), 98–109, DOI [10.1002/jgt.23018](https://doi.org/10.1002/jgt.23018), **Problem 5.3** (original journal full text [here](https://onlinelibrary.wiley.com/doi/full/10.1002/jgt.23018)), asks for an **approximation formula** for the number of nontrivially unstable graphs of order n. Source definitions: finite simple connected, **nonbipartite**, **twin-free** graph G with an automorphism of its canonical double cover CDC(G) not arising from Aut(G)×C2. The source gives raw counts through order 10 and its *Construction 5.1 / Proposition 5.2*, which adds four vertices to **any** connected, nonbipartite, twin-free base graph to obtain a nontrivially unstable graph. That construction and its instability proof are **existing results by the authors**, not a new graph construction here. Search 2026-10-10 screened the original journal, recent TF graph literature, and general graph-counting sources; it did not certify a complete subsequent solution, so priority/open-status remains uncertain.

Let U_N be the number of ordinary graph-isomorphism classes of nontrivially unstable simple undirected graphs on N vertices. We do **not** claim a full asymptotic equivalent U_N ∼ f(N) or the exact exponential rarity rate relative to all graphs.

## Partial result — explicit rigorous lower bound

**Proposition (coarse-counting corollary).** For every integer **N≥16**,

\[
\boxed{U_N\ \ge\ \frac{114}{5}\ \frac{2^{\binom{N-4}{2}}}{N!}.}
\]

Moreover, using the classical graph-enumeration theorem \(G_N\sim2^{\binom N2}/N!\) for the number of **all** unlabeled N-vertex simple graphs,

\[
\boxed{\log_2 U_N=\binom N2-\log_2 N!+O(N)
       =\frac{N^2}{2}-N\log_2 N+O(N).}
\]

Hence the **quadratic and N log N terms** of the logarithmic count are identified, but the whole **linear-in-N uncertainty** remains. In particular this bound does NOT prove the conjecturally small *fraction* of nontrivially unstable graphs, nor an approximation U_N∼f(N), nor the sharp exponential exponent for that fraction. This is a transparent **existing-method implication**, not a claimed world-first solution.

### Proof of the source-base abundance estimate

Fix \(m=N-4\ge12\) and choose a uniformly random **labelled** m-vertex simple graph X. The independent \(\binom m2\) edges are equiprobable. We upper-bound the three disallowed events from the original definition.

**Disconnected.** Any disconnected graph admits a nonempty vertex subset S of size \(1\le s\le\lfloor m/2\rfloor\) with no cross edges, so

\[
P_{\rm disc}\le
\sum_{s=1}^{\lfloor m/2\rfloor}\binom ms2^{-s(m-s)}
\le m\,2^{-(m-1)}+2^{4-m}.
\]

For \(2\le s\le m/2\), the exponent \(s(m-s)\ge2(m-2)\), while \(\sum_s\binom ms\le2^m\), giving the final term.

**Bipartite.** Summing over all \(2^m\) labelled bipartitions, each permitting at most \(\lfloor m^2/4\rfloor\) independent edges, gives

\[
P_{\rm bip}\le
2^{\,m+\lfloor m^2/4\rfloor-\binom m2}.
\]

This counts each bipartite graph multiple times, harmless for an upper bound.

**Twins.** For distinct vertices u,v to have the **same open neighbourhood**, uv must be a nonedge and for every other vertex w, uw and vw must agree. These are \(m-1\) independent Bernoulli constraints, so one fixed pair has probability \(2^{-(m-1)}\). The union bound gives

\[
P_{\rm twins}\le\binom m2\,2^{-(m-1)}.
\]

The sum B(m) of the three explicit upper bounds is a **strictly decreasing** function of all integers \(m\ge12\): the \(m/2^{m-1}\), \(2^{4-m}\) and \(\binom m2/2^{m-1}\) terms decrease; for the bipartite term, its base-two exponent \(e(m)=m+\lfloor m^2/4\rfloor-\binom m2\) has \(e(m+1)-e(m)\le-4\) for m≥12, by the even/odd floor calculation. At m=12 its **exact** value is

\[
B(12)=\frac{11009}{262144}<\frac1{20}.
\]

Thus **at least 19/20 of all** \(2^{\binom m2}\) labelled m-vertex simple graphs are **simultaneously connected, nonbipartite and twin-free** for every m≥12. There are therefore at least

\[
T_m\ge\frac{19}{20}\frac{2^{\binom m2}}{m!}
\]

distinct **unlabelled** m-vertex good base graphs, since an isomorphism class has at most m! labelled realizations.

### Transfer to the actual nontrivially unstable graphs and bound the loss

For every one of these good base isomorphism classes choose one representative X. Apply **exactly the authors' Construction 5.1**, with the nonempty singleton subsets \(A=\{x_1\}, B=\{x_2\}\) (distinct vertices), to form Y=X(A,B). Its four new vertices a1,a2,b1,b2 have edges a1b1,a2b2, both a_i joined to x1, and both b_i joined to x2; no other edges are introduced. By the source's **published Proposition 5.2**, Y is nontrivially unstable on \(N=m+4\) vertices.

Even if two different base graphs X give **isomorphic** outputs Y, every possible base-class preimage corresponds to deleting **some four-vertex subset** of a fixed representative of Y. There are only \(\binom N4\) subsets; therefore **at most** \(\binom N4\) different base isomorphism classes can map to one output isomorphism class. This argument does NOT incorrectly assume the four added vertices are intrinsically identifiable.

Therefore

\[
U_N\ge\frac{T_m}{\binom N4}
\ge\frac{19}{20}\,\frac{2^{\binom{N-4}{2}}}
 {(N-4)!\binom N4}
=\frac{24\cdot19}{20}\,\frac{2^{\binom{N-4}{2}}}{N!}
=\frac{114}{5}\,\frac{2^{\binom{N-4}{2}}}{N!},
\]

as claimed. The classical general-graph enumeration \(G_N\sim2^{\binom N2}/N!\) provides the upper bound on U_N. Since \(\binom N2-\binom{N-4}2=4N-10\), the displayed **logarithmic-scale statement** follows. This completes the exact argument.
