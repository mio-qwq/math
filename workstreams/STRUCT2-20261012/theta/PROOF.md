# Facet maxima for simple bicyclic graphs

## Statement, source, and scope

Let $G$ be a finite connected **simple** graph, and let

\[
 P_G=\operatorname{conv}\{\pm(e_u-e_v):uv\in E(G)\}.
\]

Write $N(G)$ for its number of facets. For odd $s\ge3$, put

\[
 h(s)=s\binom{s-1}{(s-1)/2}.
\]

For $k\ge3$, define

\[
 W(k)=
 \begin{cases}
 h(k-1)h(k+1),&k\text{ even},\\
 h(k)^2,&k\text{ odd},
 \end{cases}
 \qquad
 M(2k-1)=W(k),\quad M(2k)=2W(k).
\tag{1}
\]

These are precisely the facet counts in Definition 12 of Benjamin Braun and
Kaitlin Bruegge, *Facets of Symmetric Edge Polytopes for Graphs with Few Edges*,
Journal of Integer Sequences **26** (2023), Article 23.7.2:
[journal original](https://cs.uwaterloo.ca/journals/JIS/VOL26/Braun/braun6.pdf),
[arXiv v4](https://arxiv.org/abs/2201.13303v4).
Their wedge means identification at one vertex, not the complete graph join.

**Theorem.** For every integer $n\ge5$,

\[
 \max\{N(G):G\text{ connected and simple},\ |V(G)|=n,
 |E(G)|=n+1\}=M(n).
\tag{2}
\]

Every simple three-path graph

\[
 \Theta(a,b,c)=\mathrm{CB}(a,b,c),\qquad
 a,b,c\ge1,\quad a+b+c=n+1,
\]

on $n\ge5$ vertices satisfies the **strict** bound

\[
 N(\Theta(a,b,c))<M(n).
\tag{3}
\]

The parameter domain includes at most one length equal to 1. Two purported
length-one paths would represent the same edge in a simple graph and are
excluded. In particular, (3) proves the mixed-parity inequality in the
journal's Conjecture 32. Together with the graph reduction below, it proves
Conjecture 13 on its well-defined range $n\ge5$. It does not prove the
finer theta-maximizer assertion of Conjecture 33.

The only connected simple graph with four vertices and five edges is

\[
 K_4-e=\Theta(1,2,2),\qquad N(K_4-e)=12.
\tag{4}
\]

The numerical binomial expression in the original proof of Theorem 18
extends to $M(4)=12$, consistent with (4). The graph description in
Definition 12 instead contains an undefined $C_1$ at $n=3,4$. We do not
invent a one-cycle convention: (2) uses $n\ge5$, and (4) is a separate
exact small case. At $n=3$ no simple graph with $n+1=4$ edges exists.

**Contribution boundary.** The original facet-labeling characterization,
cycle formula, and multiplicativity are prior results, reproduced below
to make the counting argument explicit. The original paper already proved
the same-parity bound (Theorem 27) and the edge-disjoint-cycle bound
(Theorem 14). The new mechanism here is a direct central-binomial envelope
for the **two length-weighted terms together** in the mixed-parity count.
The short same-parity argument below is included only to make the proof of
(2) self-contained; it is not counted as another solved conjecture.
Historical priority is not certified; the dated literature report records
what was checked. This is a written mathematical proof, not a full Lean
formalization or a claim of human peer review.

## 1. Exact counting from facet labels

We use the characterization cited as Theorem 5 in Braun--Bruegge, due to
Higashitani, Jochemko and Michalek. After fixing one vertex label to zero,
facets are in bijection with integer functions $f:V(G)\to\mathbb Z$ such that

1. $|f(u)-f(v)|\le1$ on every edge;
2. the edges with $|f(u)-f(v)|=1$ form a connected spanning subgraph.

The normalization removes translations. Opposite functions are not
identified: they give opposite facets.

For a cycle, connectedness permits at most one edge with equal endpoint
labels. On an even cycle, parity of the sum of edge increments forces zero
such edges; on an odd cycle, it forces exactly one. Thus

\[
 N(C_s)=\begin{cases}
 \binom{s}{s/2},&s\text{ even},\\
 s\binom{s-1}{(s-1)/2}=h(s),&s\text{ odd}.
 \end{cases}
\tag{5}
\]

Also $N(K_2)=2$. For a wedge $G_1\vee G_2$, normalize at the shared
vertex. The restrictions to the two graphs satisfy the facet criterion
independently, and conversely any two such restrictions combine. Therefore

\[
 N(G_1\vee G_2)=N(G_1)N(G_2).
\tag{6}
\]

In particular, attaching a leaf multiplies $N$ by 2. These facts are
Lemma 7 and Proposition 9 in the source.

Define the centered binomial rows, including the zero row, by

\[
 B_m(t)=\begin{cases}
 \binom m{(m+t)/2},& |t|\le m,\quad m+t\equiv0\pmod2,\\
 0,&\text{otherwise},
 \end{cases}
 \quad m\ge0,\qquad
 T(a,b,c)=\sum_{t\in\mathbb Z}B_a(t)B_b(t)B_c(t).
\tag{7}
\]

Every sum is finite, and $B_0(t)=1$ exactly at $t=0$. The sum $T$ is
the symmetric form of the source's $F$ when its three arguments have
the same parity.

Orient all three paths of a theta from its first endpoint, labeled zero,
to the other endpoint, labeled $t$. The increments are in

\[
 \{-1,0,1\},\qquad\text{with the same sum }t\text{ on every path}.
\]

A path has at most one zero increment: two zero edges isolate the vertices
between them in the saturated-edge subgraph, since internal path vertices
have no other neighbors. At least one path has no zero, because otherwise
the two common endpoints are in different saturated components. Conversely,
if at most one zero occurs on each path and one path has no zero, then all
internal segments attach to the endpoints and the saturated graph is
connected.

If $a,b,c$ have a common parity, equality of endpoint sums forces every
path to have the same number of zero edges modulo 2. The preceding
connectedness condition therefore forces no zero edges at all, and

\[
 N(\Theta(a,b,c))=T(a,b,c).
\tag{8}
\]

For mixed parity, name the two equal-parity lengths $x,y$ and the other
length $z$. Equality of endpoint sums leaves precisely two possibilities:

- just the $z$-path has a zero edge;
- just the $x$- and $y$-paths have one zero edge each.

There are respectively $z$ and $xy$ choices for their positions. After
deleting the zero positions, the sign words have lengths

\[
 (x,y,z-1)\quad\text{or}\quad(x-1,y-1,z).
\]

Consequently, throughout the simple parameter domain,

\[
 \boxed{N(\Theta(x,y,z))
   =zT(x,y,z-1)+xyT(x-1,y-1,z).}
\tag{9}
\]

This independently recovers Corollary 25(ii). It also justifies the boundary
terms directly, rather than extending a positive-row theorem without proof.
When $z=1$, the first term is $B_x(0)B_y(0)$, as in Corollary 25(iii).
When, for example, $x=1$, the second term is

\[
 yB_{y-1}(0)B_z(0),
\]

as in Corollary 25(iv). Here the sole odd path other than $x$ has

\[
 y\ge3.
\]

The source's duplicated-length-one expression in part (v) is unnecessary
and outside the present simple three-path domain.

## 2. A central-binomial envelope

For nonnegative $p,q$ of the same parity, Vandermonde's identity gives

\[
 \sum_t B_p(t)B_q(t)=\binom{p+q}{(p+q)/2}=B_{p+q}(0).
\tag{10}
\]

Indeed, set $j=(p+t)/2$, reflect the second binomial lower index, and apply
the usual convolution. Zero-row cases are included. Hence

\[
 T(a,b,c)\le \bigl(\max_t B_a(t)\bigr)B_{b+c}(0)
\tag{11}
\]

whenever $a,b,c\ge0$ have common parity. This bound retains the exact
combined length $b+c$, which is the useful feature here.

Binomial unimodality gives the following exact peak values:

\[
 \begin{aligned}
 \max_t B_x(t)&=\frac{2x}{x+1}B_{x-1}(0)
                  &&(x\text{ odd}),\\
 \max_t B_x(t)&=\frac{4(x-1)}xB_{x-2}(0)
                  &&(x\ge2\text{ even}),\\
 \max_t B_{x-1}(t)&=\frac{2(x-1)}xB_{x-2}(0)
                  &&(x\ge2\text{ even}).
 \end{aligned}
\tag{12}
\]

For completeness, the peak is at $t=0$ in an even row and at $t=\pm1$
in an odd row. The three ratios follow immediately by cancellation of
factorials. Unimodality follows from

\[
 \binom m{j+1}/\binom mj=(m-j)/(j+1).
\]

## 3. Odd-cycle products and $M$

For odd $s\ge3$,

\[
 \frac{h(s+2)}{h(s)}=4\frac{s+2}{s+1}.
\tag{13}
\]

Thus if $p,q\ge3$ are odd and $q\ge p+4$,

\[
 \frac{h(p+2)h(q-2)}{h(p)h(q)}
 =\frac{(p+2)(q-1)}{(p+1)q}>1.
\tag{14}
\]

At fixed $p+q=2k$, the largest product is therefore $W(k)$ in (1),
uniquely in the pair of lengths up to order. Equivalently,

\[
 h(p)h(q)\le M(p+q-1).
\tag{15}
\]

This is the elementary odd-cycle balancing comparison already present
in the source's Lemma 17.

We also need

\[
 2M(n)\le M(n+1)\qquad(n\ge5).
\tag{16}
\]

For odd $n$, this is equality by (1). For even $n\ge6$, choose a
maximizing pair of odd lengths whose sum is $n$, and increase one of them
by two. By (13), the new odd-cycle product is more than four times the old
one. Since $M(n)$ is twice that old product, this proves (16), strictly.
For the separately defined value $M(4)=12$, the transition to $M(5)=36$
also satisfies (16), strictly.

## 4. Mixed parity: the full weighted bound

### 4.1 Odd vertex count

Here $x,y$ are odd and $z$ is even. Simplicity allows us to name one
of the odd lengths $x\ge3$; the other has $y\ge1$, and $z\ge2$.
Put

\[
 A=B_{x-1}(0),\qquad D=B_{y+z-1}(0).
\]

Applying (11) separately to the two terms of (9), with their coefficients
still present, gives

\[
 \begin{aligned}
 N(\Theta(x,y,z))
 &\le z\frac{2x}{x+1}AD+xyAD\\
 &=x\left(y+\frac{2z}{x+1}\right)AD\\
 &<x(y+z)AD\\
 &=h(x)h(y+z)\le M(n).
 \end{aligned}
\tag{17}
\]

The strict step uses $x\ge3$, $z>0$, and $A,D>0$. Both cycle lengths

\[
 x\ge3,\qquad y+z\ge3
\]

are odd and sum to $n+1$. Thus the comparison graph is a genuine simple
wedge on $n$ vertices and $n+1$ edges.

### 4.2 Even vertex count, an even path of length at least four

Here $x,y\ge2$ are even and $z\ge1$ is odd. If either even path has
length at least four, name it $x\ge4$. Put

\[
 A=B_{x-2}(0),\qquad D=B_{y+z-1}(0).
\]

The same argument, now using the last two ratios in (12), gives

\[
 \begin{aligned}
 N(\Theta(x,y,z))
 &\le z\frac{4(x-1)}xAD
       +xy\frac{2(x-1)}xAD\\
 &=2(x-1)\left(y+\frac{2z}{x}\right)AD\\
 &<2(x-1)(y+z)AD\\
 &=2h(x-1)h(y+z)\le2M(n-1)=M(n).
 \end{aligned}
\tag{18}
\]

Both odd cycle lengths $x-1,y+z$ are at least three and sum to $n$.
The comparison consists of their wedge and one pendant edge; it has
exactly $n$ vertices and $n+1$ edges.

### 4.3 Both even paths have length two

It remains to consider $\Theta(2,2,z)$, $z=2c+1$, $c\ge0$. Let

\[
 A=\binom{2c}c.
\]

Only $t=0,\pm2$ occur in the first term of (9), and only $t=\pm1$
in the second. Using

\[
 B_{2c}(2)=\frac c{c+1}A,
 \qquad B_{2c+1}(1)=\frac{2c+1}{c+1}A,
\]

including $c=0$ with the out-of-range value zero, we obtain

\[
 \begin{aligned}
 N(\Theta(2,2,z))
 &=z\bigl(4A+2B_{2c}(2)\bigr)+8B_{2c+1}(1)\\
 &=6z\frac{c+2}{c+1}A.
 \end{aligned}
\tag{19}
\]

If $c\ge1$, then $z\ge3$, $n=z+3\ge6$, and

\[
 N(\Theta(2,2,z))<12zA=2h(3)h(z)\le M(n).
\tag{20}
\]

These comparison cycles are again genuine odd cycles, with one extra
edge. If $c=0$, (19) gives precisely (4).

Equations (17)--(20) exhaust all mixed-parity simple theta parameters.
No assertion about the relative sizes of their separate $F$-maximizers
has been used.

## 5. Same parity, included for a self-contained global proof

The source already proves this case in Theorem 27. A short version of the
same envelope suffices in the simple domain.

If all lengths are even, choose $a\ge2$, put $m=b+c\ge4$, and write

\[
 A=B_a(0),\quad D=B_m(0).
\]

Then $N=T(a,b,c)\le AD$, whereas

\[
 h(a+1)h(m-1)=\frac{(a+1)m}{4}AD>AD.
\tag{21}
\]

The two odd lengths $a+1,m-1\ge3$ sum to $n+1$, proving (3).

If all lengths are odd, simplicity permits a choice $a\ge3$ and ensures

\[
 m=b+c\ge4.
\]

Put $A=B_{a-1}(0)$, $D=B_m(0)$. Now

\[
 N=T(a,b,c)\le\frac{2a}{a+1}AD
   <\frac{am}{2}AD
   =2h(a)h(m-1)\le M(n).
\tag{22}
\]

The strict inequality follows from $m(a+1)>4$. Both odd cycle lengths
are at least three and sum to $n$, so again one extra edge supplies the
correct graph size. This proves (3) for all legal theta graphs on $n\ge5$.

## 6. All connected simple graphs with $n+1$ edges

Such a graph has cycle rank two. Prune leaves until its connected 2-core
remains. If the core has $v$ vertices, it has $v+1$ edges and minimum
degree at least two, so

\[
 \sum_{u\in V}(\deg(u)-2)=2.
\tag{23}
\]

Consequently it has either one degree-four vertex, or two degree-three
vertices, with all other degrees two. Following maximal degree-two paths
gives precisely the following possibilities: two cycles sharing a vertex;
two vertex-disjoint cycles joined by a path; or three internally disjoint
paths between the two degree-three vertices. One may express this step
by suppressing degree-two vertices to a small multigraph, but the original
graph throughout remains simple. This auxiliary suppression never treats
parallel edges as different edges of a simple input graph.

### 6.1 The theta core

If the core is a theta on $v\ge5$ vertices and $t=n-v$ leaves were
pruned, (6), (3), and (16) imply

\[
 N(G)=2^tN(\Theta)<2^tM(v)\le M(n).
\tag{24}
\]

If the core has $v=4$, it is $K_4-e$. For $n\ge5$,

\[
 N(G)=12\,2^{n-4}<36\,2^{n-5}
       =M(5)2^{n-5}\le M(n).
\tag{25}
\]

Thus no graph with a theta core is a maximizer when $n\ge5$.

### 6.2 Two edge-disjoint cycles

Let their lengths be $p,q\ge3$, and let $t\ge0$ be the number of
remaining edges, all bridges. Then

\[
 n=p+q+t-1,
 \qquad N(G)=2^tN(C_p)N(C_q)
\tag{26}
\]

by the blockwise version of (6). The exact arrangement of bridges does not
affect this count.

If one cycle length, say $p$, is even, it is at least four. Shortening
that cycle by one and adding a bridge preserves both the vertex and edge
counts and changes its contribution by the factor

\[
 \frac{2h(p-1)}{\binom p{p/2}}=\frac p2>1.
\tag{27}
\]

Therefore a maximizing graph has both cycle lengths odd. If then $t\ge2$,
replace two bridges by an increase of two in one odd cycle length. By (13),
the new count divided by the old is

\[
 \frac{h(p+2)}{4h(p)}=\frac{p+2}{p+1}>1.
\tag{28}
\]

A maximizing graph consequently has $t=0$ for odd $n$, and $t=1$
for even $n$. Applying (14) then forces the two odd cycle lengths to be
as equal as parity permits. Its value is exactly (1). Each comparison is
realized by a connected simple wedge of the chosen cycles with the required
number of tree edges, so it stays inside the permitted class.

Conversely, those balanced odd-cycle graphs exist for every $n\ge5$
and attain (1). Together with (24)--(28), this proves (2).

The proof also identifies the maximizers by their block data: two odd
cycle blocks of the balanced lengths in (1), and no bridge for odd $n$,
or exactly one bridge for even $n$. For even $n$, this includes either
two disjoint cycles joined by a single bridge, or two cycles sharing one
vertex with one pendant edge; different attachment positions may give
different ordinary graph isomorphism types. No uniqueness of the whole
graph is claimed in that case.

## Verification and remaining question

The infinite proof is Sections 1--6. Exact small-graph checks are provided
separately by a checker that constructs the input graph, enumerates integer
labels along a spanning tree, checks every original edge and the connectivity
of the saturated subgraph, and never calls a binomial formula to count the
facets. Those finite checks test the semantic correspondence, not the
universal inequality.

Conjecture 33 asks which theta maximizes $N$ **within the theta class**.
The strict comparison with $M(n)$ leaves that question open. In particular,
the envelope here is deliberately not asserted to be attained by a theta.

Independent written review, actual checker runs, exact source hashes, and
any supporting Lean compilation have separate receipts. No historical
compilation is being reported as a new execution, and no universal
graph/polytope Lean proof is claimed by this manuscript.
