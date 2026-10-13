# The exact sparse window for the full two-fold group

Date: 2026-10-13 UTC. Complete written proof; definition-level regression
and the singleton-component Lean bridge have separate receipts. Independent
written acceptance and a Lean proof of the analytic limit remain pending.
All logarithms are natural. Only the full ordered-pair group is considered:

\[
T(G)=\{(\alpha,\beta)\in S_n^2:
A_{ij}=A_{\alpha(i),\beta(j)}\text{ for all }i,j\}.
\]

## 1. Result

Put \(L=\log n\), \(M=\binom n2\), and
\(B_n=(n!)^2(1-p_n)^M\). Suppose, for a fixed constant \(A\ge0\),

\[
\left|n^2p_n-(4nL-4n)\right|\le A L^2
\quad\text{for all sufficiently large }n.
\tag{1}
\]

**Theorem.** Uniformly on each such corridor,

\[
\boxed{\mathbb E|T(G(n,p_n))|=1+B_n+o(1+B_n).}
\tag{2}
\]

More precisely, the proof gives a bound of the form
\(B_n O(L^5/n)+o(1)\) for the absolute error. The constants and the
eventual threshold may depend on \(A\). Section 5 supplies an explicit
finite bound before asymptotic simplification.

In particular, for fixed real \(h,s\) and

\[
np_n=4L-4-\frac{8L^2}{n}+\frac{hL+s}{n},
\tag{3}
\]

the lower bound in `CRITICAL_BOUNDARY.md` now has a matching upper bound:

\[
\boxed{
\begin{array}{ll}
h<22:&\mathbb E|T|\sim2\pi e^{-6-s/2}n^{11-h/2},\\
h=22:&\mathbb E|T|\longrightarrow1+2\pi e^{-6-s/2},\\
h>22:&\mathbb E|T|\longrightarrow1.
\end{array}}
\tag{4}
\]

An exact centering removes the constants from the limiting function. Set

\[
p_n^*=1-(n!)^{-2/M}\quad(n\ge2).
\]

For each fixed \(x\in\mathbb R\),

\[
\boxed{p_n=p_n^*+\frac{2x}{n^2}
\quad\Longrightarrow\quad \mathbb E|T|\longrightarrow1+e^{-x}.}
\tag{5}
\]

Here

\[
p_n^*=\frac{4L-4}{n}
+\frac{-8L^2+22L+2\log(2\pi)-12}{n^2}
+O(L^3/n^3).
\tag{6}
\]

These are expectation statements. The empty graph is a vanishingly rare
event with group order \((n!)^2\); high-probability rigidity alone would
not prove (2). Neither the projection expectation nor a reduced-conditional
expectation is identified by (2).

## 2. Full components and an exact singleton classification

Use every ordered adjacency equation and the common diagonal ground, as
in `CRITICAL_BOUNDARY.md`. Write \(c_j\) for the number of ungrounded
components containing exactly \(j\) unordered edge variables. With
\(t=p/(1-p)\), the exact prescribed-pair probability is

\[
P_{\alpha,\beta}=(1-p)^M\prod_{j\ge1}(1+t^j)^{c_j}.
\tag{7}
\]

Grounded variables contribute only their zero probability. Thus the empty
assignment is factored out without assuming the system is fully grounded.

Let \(f\) be the number of vertices fixed by **both** permutations, and
\(u\) the number of transpositions which are cycles of both permutations
on the same two vertices. Then

\[
\boxed{c_1=\binom f2+u,\qquad 2u\le n-f.}
\tag{8}
\]

**Proof.** The indicator graph of an ungrounded singleton is one edge
\(\{i,j\}\). It is invariant under the full TF pair by component
invariance. Applying its adjacency relation to \((i,j)\) and \((j,i)\)
shows either that both permutations fix \(i,j\) pointwise, or that both
swap them. The mixed choices contradict injectivity. Conversely, either
of those two patterns makes the one-edge indicator TF-invariant on every
ordered pair: its endpoints are preserved, its two arcs are preserved,
and outside vertices stay outside. Consequently no equality path connects
its edge variable to another variable or the ground. This proves the iff.
Common transpositions are disjoint and avoid the common fixed vertices,
giving the second assertion. ∎

Put \(m=n-f=|\operatorname{supp}\alpha\cup\operatorname{supp}\beta|\).
The number \(N\) of grounded or nontrivial-component variables is exactly
\(M-c_1\). Thus (8) gives

\[
N\ge M-\binom{n-m}{2}-m/2
=\frac{m(2n-m-2)}2.
\tag{9}
\]

With \(q=p^2+(1-p)^2\), the component power-mean estimate therefore gives

\[
P_{\alpha,\beta}\le q^{m(2n-m-2)/4}.
\tag{10}
\]

There are at most \(\binom nm(m!)^2\) pairs of union support \(m\):
choose the union, then choose both permutations on it. This overcounts
pairs with smaller union and is a valid upper bound on the exact stratum.
A nonidentity pair cannot have \(m=1\).

## 3. A factorial tail for short cycles

For a permutation \(\alpha\), let \(s_4(\alpha)\) count its vertices in
cycles of length at most four, and \(Z\) the number of those cycles. Write
\(H=1+1/2+1/3+1/4=25/12\). For every integer \(r\ge1\), a uniform
permutation satisfies

\[
\mathbb E\binom Zr\le\frac{H^r}{r!}.
\tag{11}
\]

Indeed, specifying \(d_j\) disjoint cycles of length \(j\le4\), with
\(\sum d_j=r\) and total length \(\ell=\sum j d_j\le n\), has
expected count \(\prod_{j=1}^4(j^{d_j}d_j!)^{-1}\). This follows by
choosing the labelled cycles and permuting the remaining \(n-\ell\)
vertices, divided by \(n!\). Terms with \(\ell>n\) are zero. Sum over
the vectors and apply the multinomial identity to obtain (11).

If \(R\) is a nonnegative integer, set

\[
r=\left\lceil\frac{R+1}{4}\right\rceil,
\qquad \varepsilon_R=H^r/r!.
\]

Since \(s_4\le4Z\), Markov's inequality for \(\binom Zr\) gives

\[
\Pr[s_4(\alpha)>R]\le\varepsilon_R.
\tag{12}
\]

For \(R=\lceil L^2\rceil\), the factorial lower bound yields

\[
\log\varepsilon_R
\le-r\log r+(1+\log H)r
=-\tfrac12 L^2\log L+O(L^2).
\tag{13}
\]

No independence of cycle counts is assumed.

## 4. Pairs with few common fixed vertices

For \(0<p\le1/2\), so \(0<t\le1\), components of size at least three
give a total logarithmic correction at most \(Mt^3/3\) in (7): there
are at most \(M/3\) of them and \(\log(1+t^j)\le t^3\).

The endpoint lemma in `CRITICAL_BOUNDARY.md` implies that every endpoint
of a component of size one or two belongs to an \(\alpha\)-cycle of
length at most four. Hence, when \(s_4(\alpha)\le R\),

\[
c_1\le\binom R2,\qquad 2c_2\le\binom R2.
\]

It follows that

\[
1\le\frac{P_{\alpha,\beta}}{(1-p)^M}\le e^{\eta},
\quad
\eta=t\binom R2+\frac{t^2}{2}\binom R2+\frac{Mt^3}{3}.
\tag{14}
\]

Such a pair automatically has \(f\le R\). For the remaining pairs with
\(f\le R\) but \(s_4(\alpha)>R\), (8) and \(2c_2\le M\) give

\[
\frac{P_{\alpha,\beta}}{(1-p)^M}\le e^{\xi},
\quad
\xi=t\left(\binom R2+n/2\right)+\frac{Mt^2}{2}+\frac{Mt^3}{3}.
\tag{15}
\]

There are at most \(\varepsilon_R(n!)^2\) such pairs, by (12), allowing
an arbitrary second permutation. Thus the total contribution \(A_n\)
of all pairs with \(f\le R\) obeys

\[
B_n(1-\varepsilon_R)\le A_n
\le B_n(e^\eta+\varepsilon_R e^\xi).
\tag{16}
\]

Under (1), choose \(R=\lceil L^2\rceil<n/8\), for sufficiently large
\(n\). Uniformly on this corridor, \(t=O(L/n)\),
\(\eta=O(L^5/n)\), and \(\xi=O(L^2)\). Equations (13)--(16) prove
\(A_n=B_n(1+O(L^5/n))\); the factorial-tail term is smaller than every
fixed inverse power of \(n\).

## 5. Many common fixed vertices and an effective remainder

The identity pair contributes one. All remaining pairs with \(f>R\)
have \(2\le m\le n-R-1\), so (10) gives the explicit remainder bound

\[
\mathcal R(n,p,R)=
\sum_{m=2}^{n-R-1}\binom nm(m!)^2
q^{m(2n-m-2)/4}.
\tag{17}
\]

An empty sum is zero. For every \(n\ge2\), integer \(0\le R<n\), and
\(0<p\le1/2\), the exact finite estimate is

\[
\boxed{
1+B_n-(1-p)^M\le\mathbb E|T|
\le1+B_n(e^\eta+\varepsilon_R e^\xi)+\mathcal R(n,p,R).}
\tag{18}
\]

The lower bound retains the empty graph for every nonidentity pair and
uses probability one for the identity. The upper bound is (16) and (17).
In particular,

\[
|\mathbb E|T|-(1+B_n)|\le(1-p)^M
+B_n(e^\eta-1+\varepsilon_R e^\xi)+\mathcal R(n,p,R).
\tag{19}
\]

To show \(\mathcal R=o(1)\) under (1), put
\(F(m)=m(2n-m-3)\) and \(S(m)=(n)_m^2q^{F(m)/4}\).
The summand in (17) is at most

\[
\frac{S(m)}{\binom nm},
\tag{20}
\]

because \(q\le1\) and \(\binom nm(m!)^2=(n)_m^2/\binom nm\).
The uniform estimates (12)--(14) of `CRITICAL_BOUNDARY.md`, with
\(\delta=1/8\) and \(C=A\), apply under (1). Only the lower bound
\(p\ge(4L-4-AL^2/n)/n\) and \(p=O(L/n)\) enter those estimates.
Explicitly, for sufficiently large \(n\),

\[
S(m)\le
\begin{cases}
n^{-m/8},&2\le m\le7n/8,\\
\exp((A/2)L^2+10L),&7n/8<m\le n.
\end{cases}
\tag{21}
\]

The first part of (17) is at most
\(n^{-1/4}/(1-n^{-1/8})\). In the second part,
\(R<n-m<n/8\). Monotonicity of the binomial coefficients up to \(n/2\)
and \(\binom nR\ge(n/R)^R\) give

\[
\sum_{7n/8<m\le n-R-1}\frac{S(m)}{\binom nm}
\le \exp((A/2)L^2+11L-R\log(n/R))=o(1).
\tag{22}
\]

The logarithm has leading term \(-L^3\). Equations (19)--(22), along
with \((1-p)^M\to0\), prove (2) and its stated error form. Notice the
binomial denominator in (20). Replacing the union-support count by the
older maximum-support count loses precisely this useful entropy factor.

## 6. Identification of the window

For (3), Stirling's formula and
\(M\log(1-p)=-Mp-Mp^2/2+O(Mp^3)\) give

\[
\log B_n=(11-h/2)L+\log(2\pi)-6-s/2+O_{h,s}(L^3/n).
\tag{23}
\]

Thus (2) yields all three cases of (4), including the precise equivalent
in the divergent regime. For the exact center,
\(M\log(1-p_n^*)=-2\log(n!)\). Taylor expansion gives (6), and, for
fixed \(x\),

\[
\log B_n
=M\log\left(1-\frac{2x}{n^2(1-p_n^*)}\right)\longrightarrow-x.
\]

Equation (5) follows. This also identifies the probability-window width
as \(n^{-2}\), with the stated normalization factor two.

For fixed \(x\) in (5), the expectation conditional on a nonempty graph
also tends to one. Indeed,
\(\mathbb E[|T|;G\ne\varnothing]=\mathbb E|T|-B_n\to1\), while
\(\Pr[G\ne\varnothing]\to1\). Thus the positive excess \(e^{-x}\)
in the unconditional limit is entirely accounted for by the empty event.
This additive conclusion uses bounded \(B_n\); it is not asserted throughout
the entire corridor when \(B_n\) can grow.

## 7. Evidence, scope and next step

`check_exact_window.py` checks (8)--(10) against actual full components,
compares rational products in (7), verifies the short-cycle factorial
moments against literal permutations, and checks the union-support counts.
Small graph enumeration is used only as an independent probability oracle
at n=3,4; the prior large graph/automorphism enumerations are not repeated.
High-precision arithmetic checks (6) and (23), not the all-n proof.

`lean/SingletonComponent.lean` builds on the existing actual ordered
constraint closure, proves its singleton iff one-edge invariance bridge,
and classifies the latter by common fixed endpoints or a shared
transposition. Its compilation and axiom audit are separately recorded.
The combinatorial cardinality identity (8), probability sums, tail bound,
and analytic limit are proved in this note, not yet in Lean.

The full-group definition and the earlier fixed-p MathDB proof overlap
remain explicitly attributed in `PRIOR_ART_2026-10-13.md`. The new assertion
is the sparse expectation asymptotic and exact window; the searches recorded
there do not certify historical firstness. No new independent acceptance
is claimed. The next useful step is independent semantic review of this
proof, followed by formalizing the cardinality and expectation interfaces;
the projection's distinct sparse threshold remains open here.
