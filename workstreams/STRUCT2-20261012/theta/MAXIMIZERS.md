# Exact facet maximizers among simple three-path graphs

## The theorem and its relation to the earlier bound

Let $\Theta(a,b,c)=\mathrm{CB}(a,b,c)$ be the graph consisting of three
internally vertex-disjoint paths with common endpoints and lengths
$a,b,c$. Throughout,

\[
 a,b,c\ge1,\qquad \#\{i:a_i=1\}\le1,\qquad a+b+c=n+1.
\tag{1}
\]

Thus the graph is simple, has $n$ vertices and $n+1$ edges, and $n\ge4$.
Let $N$ count the facets of its symmetric edge polytope.

**Theorem.** For every $n\ge4$, the maximizing unordered triple of path
lengths is unique. With the indicated integer $k$, it is

| Vertex count | Parity of $k$ | Maximizing triple |
|---|---|---|
| $n=2k-1$ | $k$ even | $(k-1,k-1,2)$ |
| $n=2k-1$ | $k$ odd | $(k,k-2,2)$ |
| $n=2k$ | $k$ even | $(k,k,1)$ |
| $n=2k$ | $k$ odd | $(k+1,k-1,1)$ |

In the odd-vertex cases $k\ge3$, and in the even-vertex cases $k\ge2$.
Every listed triple satisfies (1). This proves, and extends to all
nonempty simple theta orders, **Conjecture 33** of Braun--Bruegge,
*Journal of Integer Sequences* **26** (2023), Article 23.7.2, p. 24:
[original paper](https://cs.uwaterloo.ca/journals/JIS/VOL26/Braun/braun6.pdf).
The source asks for a maximizing triple at $n\ge10$; uniqueness and the
smaller simple orders are additional consequences of the strict proof.

The proof has three steps. First it shortens the path whose parity differs
from the other two to length 1 or 2, while adding the removed length to one
of those paths. Second it balances the two remaining lengths using an exact
rational comparison of their facet counts. Third it excludes all
same-parity triples by explicit strictly larger mixed-parity examples.
It does not infer a universal result from the source's finite enumeration.

The separate [bicyclic proof](PROOF.md) already gives the strict comparison
with $M(n)$ and the global $n$-vertex, $n+1$-edge maximum. Its final paragraph
records Conjecture 33 as outside that earlier manuscript's scope. The present
subsequent theorem closes that further question; the earlier frozen proof
and its review are preserved.

**Attribution and verification scope.** The facet-labeling theorem, the
source's Corollary 25, Vandermonde's identity, binomial unimodality, and
elementary central-binomial ratios are prior mathematics. The proposed
contribution is the complete compression, balancing, and parity-exclusion
argument for the exact maximizer. Historical priority is not certified by
the accompanying literature checks. Written review, finite execution, and
Lean scope have separate receipts; this note does not claim full Lean
formalization or human peer review.

## 1. The exact facet count, including boundary paths

Use

\[
 B_m(t)=
 \begin{cases}
 \binom m{(m+t)/2},& |t|\le m,\ m+t\equiv0\pmod2,\\
 0,&\text{otherwise},
 \end{cases}
 \quad m\ge0,
 \qquad T(a,b,c)=\sum_t B_a(t)B_b(t)B_c(t).
\tag{2}
\]

The sums are finite, and $B_0(t)=1[t=0]$. The formula does not introduce
a graph path of length zero.

The facet-labeling theorem gives $N(\Theta(a,b,c))=T(a,b,c)$ for
same-parity lengths. For mixed parity, name the same-parity lengths $x,y$
and the other length $z$. Then

\[
 N(x,y,z):=N(\Theta(x,y,z))
 =zT(x,y,z-1)+xyT(x-1,y-1,z).
\tag{3}
\]

A direct derivation and its identification with Corollary 25(ii)--(iv)
are given in Section 1 of the bicyclic proof. Briefly, normalize the first
endpoint label to zero and let the other be $t$. Each path has at most
one zero edge increment, and at least one path has none, because the
nonzero-increment edges must be spanning and connected. Equal endpoint
sums force exactly the two zero patterns counted by (3). The argument
includes $x=1$ or $z=1$, using the zero row in (2).

For same-parity nonnegative $p,q$, Vandermonde gives

\[
 \sum_t B_p(t)B_q(t)=B_{p+q}(0).
\tag{4}
\]

Consequently, for three rows of common parity,

\[
 T(a,b,c)\le \max_t B_a(t)\,B_{b+c}(0).
\tag{5}
\]

We will also retain one more shell of an even row, rather than bounding
the whole row by its central value.

## 2. Central-binomial product ratios

Put $b_j=\binom{2j}{j}$ for $j\ge0$. Its successive ratio is

\[
 \rho_j=\frac{b_{j+1}}{b_j}
 =4-\frac2{j+1}.
\tag{6}
\]

It is positive and strictly increasing in $j$. Thus, for a fixed $u\ge0$,

\[
 Q_u(v)=\frac{b_u b_v}{b_{u+v}}
\]

is nonincreasing for $v\ge0$, since

\[
 \frac{Q_u(v+1)}{Q_u(v)}
 =\frac{\rho_v}{\rho_{u+v}}\le1.
\tag{7}
\]

In particular, for $v\ge1$,

\[
 \frac{b_u b_v}{b_{u+v}}
 \le\frac{b_u b_1}{b_{u+1}}
 =\frac{u+1}{2u+1}.
\tag{8}
\]

We shall also use, for $r,s\ge1$,

\[
 b_r b_s\le2b_{r+s-1}.
\tag{9}
\]

To prove this, fix $s$. The quotient $b_r b_s/b_{r+s-1}$ equals 2 at
$r=1$, and its ratio when $r$ increases by one is
$\rho_r/\rho_{r+s-1}\le1$.

These are scalar inequalities for positive explicit integers, with no
asymptotic approximation.

## 3. Exact short-path formulas

For even $p,q\ge2$,

\[
 \boxed{N(p,q,1)=\frac{pq+2}{2}B_p(0)B_q(0).}
\tag{10}
\]

Indeed, the first term of (3) is $B_p(0)B_q(0)$. In the second term,
only $t=\pm1$ occur and
$B_{p-1}(1)=B_p(0)/2$, and similarly for $q$. This is the exact
specialization of the source's Corollary 25(iii).

For odd $x,y\ge1$ with at most one of them equal to 1,

\[
 \boxed{N(x,y,2)=\frac{xy+5}{4}B_{x+1}(0)B_{y+1}(0).}
\tag{11}
\]

For an explicit calculation, set $A_x=B_{x-1}(0)$ and
$r_x=(x-1)/(x+1)$, and define $A_y,r_y$ similarly. The relevant values are

\[
 B_x(1)=\frac{2x}{x+1}A_x,\qquad
 B_{x-1}(2)=r_xA_x,\qquad
 B_{x+1}(0)=\frac{4x}{x+1}A_x.
\]

They hold also at $x=1$, where $B_0(2)=0$. Equation (3) now gives

\[
 \begin{aligned}
 N(x,y,2)
 &=4B_x(1)B_y(1)+2xyA_xA_y(1+r_xr_y)\\
 &=\frac{4xy(xy+5)}{(x+1)(y+1)}A_xA_y,
 \end{aligned}
\]

which is exactly (11).

The two short-path counts are consequences of the already published
facet formula, not separate new counting constructions.

## 4. Compression for even vertex count

Let $x,y\ge2$ be even and $z\ge1$ odd, so $n=x+y+z-1$ is even.
The central values satisfy

\[
 \max_t B_x(t)=B_x(0),\qquad
 \max_t B_{x-1}(t)=\frac12B_x(0).
\]

Apply (5) to both terms of (3), and put $D=B_{y+z-1}(0)>0$. We obtain

\[
 N(x,y,z)\le B_x(0)D\left(z+\frac{xy}{2}\right).
\tag{12}
\]

The compressed graph has lengths

\[
 (x,\ y+z-1,\ 1),
\]

with the same total length and in the simple domain. By (10), its count is

\[
 N(x,y+z-1,1)
 =B_x(0)D\left(1+\frac{x(y+z-1)}2\right).
\tag{13}
\]

The difference of the scalar factors in (13) and (12) is

\[
 \frac{(z-1)(x-2)}2\ge0.
\]

Therefore

\[
 \boxed{N(x,y,z)\le N(x,y+z-1,1).}
\tag{14}
\]

If $z>1$ and $x>2$, the scalar comparison is strict. If $z>1$ and $x=2$,
then $z\ge3$, and the first term of (3) gives a strict instance of (5):
at $t=2$ the remaining weight

\[
 B_y(2)B_{z-1}(2)
\]

is positive, while $B_2(2)=1<B_2(0)=2$. Thus (14) is **strict whenever
$z>1$**, including $x=y=2$. At $z=1$ it is an identity.

Every even-order mixed-parity maximizer must therefore have its odd path
of length one.

## 5. Compression for odd vertex count

Let $x,y$ be odd and $z\ge2$ even. Simplicity allows us to choose
$x\ge3$, while $y\ge1$. Put

\[
 A=B_{x-1}(0),\quad
 D=B_{y+z-1}(0),\quad
 E=B_{y-1}(0)B_z(0),\quad
 r=\frac{x-1}{x+1}.
\tag{15}
\]

An even centered-binomial row is maximal at zero. Its largest value away
from zero is at $t=\pm2$. Thus, for every even $t$,

\[
 B_{x-1}(t)\le rA+(1-r)A\,1[t=0].
\tag{16}
\]

Combining (16) with (4) gives

\[
 T(x-1,y-1,z)\le rAD+(1-r)AE.
\tag{17}
\]

The odd row has peak

\[
 \max_tB_x(t)=\frac{2x}{x+1}A.
\]

Using (5) for the other term of (3), we therefore obtain the joint bound

\[
 N(x,y,z)
 \le\frac{xA}{x+1}
       \left(\bigl(2z+y(x-1)\bigr)D+2yE\right).
\tag{18}
\]

In (8), take $u=(y-1)/2\ge0$ and $v=z/2\ge1$. This yields

\[
 \frac ED
 =\frac{b_{(y-1)/2}b_{z/2}}{b_{(y+z-1)/2}}
 \le\frac{y+1}{2y}.
\tag{19}
\]

Equation (18) simplifies to

\[
 N(x,y,z)\le\frac{xAD}{x+1}(xy+2z+1).
\tag{20}
\]

Now set $y'=y+z-2$, which is positive and odd. The compressed graph
$(x,y',2)$ is simple and has the same total length. Equation (11) gives

\[
 N(x,y',2)=\frac{xAD}{x+1}(xy'+5).
\tag{21}
\]

The difference of its scalar factor and that in (20) is

\[
 xy'+5-(xy+2z+1)=(x-2)(z-2)\ge0.
\tag{22}
\]

Since $x\ge3$ and $A,D>0$, this difference is positive whenever $z>2$.
We have proved

\[
 \boxed{N(x,y,z)\le N(x,y+z-2,2),}
\tag{23}
\]

**strictly for $z>2$**. At $z=2$ it is the identity comparison. No
lower bound on $y$ beyond $y\ge1$ is needed: (19) includes $y=1$ with
$b_0=1$.

Every odd-order mixed-parity maximizer must therefore have its even path
of length two.

## 6. Strict balancing of the remaining two paths

Let $u,v\ge2$ be even and suppose $u\ge v+4$. Write

\[
 P=uv,\quad S=u+v,\quad
 d=u-v-2>0,\quad
 U=u(v+1),\quad V=(u-1)(v+2)=U+d.
\tag{24}
\]

The inward two-unit transfer gives

\[
 (u',v')=(u-2,v+2),\quad u'v'=P+2d,
\]

and direct central-binomial ratios give

\[
 \frac{B_{u-2}(0)B_{v+2}(0)}{B_u(0)B_v(0)}
 =\frac UV.
\tag{25}
\]

### 6.1 The length-one path

By (10), the nonconstant weight is $P+2$. Cross multiplication by the
positive denominators in (25) reduces the improvement to

\[
 \begin{aligned}
 U(P+2d+2)-V(P+2)
 &=d\bigl(2U-P-2\bigr)\\
 &=d(uv+2u-2)>0.
 \end{aligned}
\tag{26}
\]

Thus $N(u-2,v+2,1)>N(u,v,1)$ whenever $u\ge v+4$. Iteration leaves
exactly the even pair as close to half its total as possible.

### 6.2 The length-two path

Write the two odd path lengths as $x=u-1$, $y=v-1$. Equation (11) has
nonconstant weight

\[
 xy+5=P-S+6.
\]

The same calculation now gives

\[
 \begin{aligned}
 U(P+2d-S+6)-V(P-S+6)
 &=d\bigl(2U-P+S-6\bigr)\\
 &=d(uv+3u+v-6)>0.
 \end{aligned}
\tag{27}
\]

The last factor is positive for all $u,v\ge2$. The corresponding odd
lengths remain positive under the transfer, and the simple domain is
preserved. Thus the pair $x,y$ is again uniquely balanced up to order.

Equations (26) and (27) yield exactly the four triples in the theorem,
among mixed-parity theta graphs. Every unbalanced pair has a strictly
improving transfer, so no additional unordered length triple ties.

## 7. Same-parity triples are strictly worse

This comparison is necessary: Conjecture 33 ranges over all theta graphs.
The preceding compression alone would not exclude the same-parity class.

### 7.1 Odd vertex count and all-even lengths

Write $a+b+c=2k$, so $n=2k-1$ and $k\ge3$. In (5), let $a=2r$ and
$b+c=2s$, where $r\ge1$, $s\ge2$, and $r+s=k$. Equations (5) and (9)
give

\[
 N(\Theta(a,b,c))=T(a,b,c)\le b_r b_s\le2b_{k-1}.
\tag{28}
\]

The legal mixed-parity graph $\Theta(1,2k-3,2)$ has, by (11) and (6),

\[
 N(1,2k-3,2)=(k+1)b_{k-1}>2b_{k-1}.
\tag{29}
\]

Its two odd paths are distinct from a duplicated pair of length-one
paths because $2k-3\ge3$. Thus every all-even theta is strictly dominated.

### 7.2 Even vertex count and all-odd lengths

Write $a+b+c=2k+1$, let $c=2u+1$ and $a+b=2v$. Here $u\ge0$, $v\ge1$,
and $u+v=k$. The odd-row peak is

\[
 \max_tB_c(t)=\frac{2u+1}{u+1}b_u.
\]

Using (5) and (8),

\[
 N(\Theta(a,b,c))=T(a,b,c)
 \le\frac{2u+1}{u+1}b_u b_v\le b_k.
\tag{30}
\]

The legal mixed-parity graph $\Theta(2,2k-2,1)$ has

\[
 N(2,2k-2,1)=k b_k>b_k\qquad(k\ge2).
\tag{31}
\]

For completeness, all-odd simple theta graphs do not occur at $n=4$,
but the strictly larger comparison (31) is still legal there.

The same-parity classes are therefore always strictly worse than an
available mixed-parity triple. Together with the strict compression and
balancing arguments, this completes the theorem for every $n\ge4$.

## 8. Exact values and comparison with the global bicyclic maximum

Let $H(n)=\max_{a+b+c=n+1}N(\Theta(a,b,c))$ over the simple domain.
The proved maximizers and (10)--(11) give

\[
\begin{array}{ll}
 H(2k-1)=\dfrac{k^2-2k+6}{4}\binom{k}{k/2}^{\!2},
   &k\text{ even},\\[6pt]
 H(2k-1)=\dfrac{k(k^2-2k+5)}{k+1}
                \binom{k-1}{(k-1)/2}^{\!2},
   &k\text{ odd},\\[6pt]
 H(2k)=\dfrac{k^2+2}{2}\binom{k}{k/2}^{\!2},
   &k\text{ even},\\[6pt]
 H(2k)=\dfrac{2k(k^2+1)}{k+1}
                \binom{k-1}{(k-1)/2}^{\!2},
   &k\text{ odd}.
\end{array}
\tag{32}
\]

For $n\ge5$, divide by the original Definition 12 value $M(n)$:

\[
\begin{array}{ll}
 \dfrac{H(2k-1)}{M(2k-1)}
  =\dfrac{k^2-2k+6}{k(k+1)},& k\text{ even},\\[6pt]
 \dfrac{H(2k-1)}{M(2k-1)}
  =\dfrac{k^2-2k+5}{k(k+1)},& k\text{ odd},\\[6pt]
 \dfrac{H(2k)}{M(2k)}
  =\dfrac{k^2+2}{k(k+1)},& k\text{ even},\\[6pt]
 \dfrac{H(2k)}{M(2k)}
  =\dfrac{k^2+1}{k(k+1)},& k\text{ odd}.
\end{array}
\tag{33}
\]

All four are strictly less than one in their $n\ge5$ domains. They
therefore also recover the strict theta/global comparison proved by the
earlier, independent envelope route. All tend to one along their parity
subsequences. The odd-order two lines give exact versions of the comparison
the original paper discusses after Conjecture 33.

The even-order formulas are the corrected ratios for the original
Proposition 30; see the separate [source correction](literature/PROPOSITION30_CORRECTION.md).
That original proposition only bounds the displayed candidate graphs.
Its valid inequality and typographical corrections alone would not imply
that the candidate graphs maximize over all theta parameters.

At $n=4$, (32) yields $H(4)=12$, directly on $\Theta(2,2,1)$. As in the
earlier manuscript, this does not assign an unprovided graph meaning to
$C_1$ in the source's Definition 12.

## Reproducibility boundary

Every step above is a finite-sum or exact algebraic argument with explicit
parameter conditions. No finite cutoff is part of the universal proof.
The separate scalar checker tests the compression, short-path values,
balancing, parity exclusion, and predicted maximizers on a modest finite
window. The independently constructed graph-label checker validates the
source semantics on small graphs. Its output is not used as an assumption
in (3) or in this proof.

The final-source review receipt binds the actual bytes of this note.
Any earlier review of the global bound alone must not be read as an
automatic review of this subsequent exact-maximizer theorem.
