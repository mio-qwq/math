# Local pair-cost bounds on all binary coordinate systems

Research note, 8 October 2026.

We prove the constant-one cover and pruning bounds for arbitrary independent
nonnegative costs on the complete two-by-two original families when both
relations are four-vertex paths. The only assumptions on the costs are the
nine local product inequalities. This removes the proportional and symmetric
exchange restrictions of [reflexive-cost-families.md](reflexive-cost-families.md)
on this fixed pair of nonblock relations. Together with the previously
proved block-relation theorem, it settles every relation and every partial
original family when each of the four coordinate sets has size at most two.

The proof is analytic, includes zero costs, and gives an exact formula for the
minimum augmented cover. It is not a Lean formalization. Sufficiency of the
local condition for arbitrary pairs of relations remains open. Historical
priority and equivalence to the full existing weighted-graph literature have
not been established.

## 1. Graph, notation and theorem

Take \(P=I=S=J=\{0,1\}\), \(R=P\times J\), \(C=I\times S\), and
\[
E=F=\{(0,0),(0,1),(1,1)\}.
\]
Keep the \(R\) and \(C\) graph tags separate. An original pair
\(r=(p,j),c=(i,s)\) conflicts when \(E(p,i)\) and \(F(s,j)\).
Its cross-corners are \(H=(p,s)\), \(Z=(i,j)\).
All four corners occur in each family.

Write the original costs, in order \(00,01,10,11\), as
\[
x=(a,b,c,d),\qquad y=(A,B,C,D),
\]
and the corner costs as
\[
h=(\alpha,\beta,\gamma,\delta),\qquad z=(u,v,w,t).
\]
The italic cost \(C=y_{10}\) is distinguished from the original family \(C\)
by context. All sixteen costs are independent nonnegative real numbers.
The complete list of conflicts and hypotheses is

| Conflict | Cross-corners \(H,Z\) | Local inequality |
| --- | --- | --- |
| \(r_{00}c_{00}\) | \(00,00\) | \(aA\le\alpha u\) |
| \(r_{00}c_{10}\) | \(00,10\) | \(aC\le\alpha w\) |
| \(r_{01}c_{00}\) | \(00,01\) | \(bA\le\alpha v\) |
| \(r_{01}c_{01}\) | \(01,01\) | \(bB\le\beta v\) |
| \(r_{01}c_{10}\) | \(00,11\) | \(bC\le\alpha t\) |
| \(r_{01}c_{11}\) | \(01,11\) | \(bD\le\beta t\) |
| \(r_{10}c_{10}\) | \(10,10\) | \(cC\le\gamma w\) |
| \(r_{11}c_{10}\) | \(10,11\) | \(dC\le\gamma t\) |
| \(r_{11}c_{11}\) | \(11,11\) | \(dD\le\delta t\) |

The augmented bipartite graph \(\Gamma\) has left side \(R\sqcup Z_L\)
and right side \(C\sqcup Z_R\). Its edges are the nine conflicts above,
together with
\[
a-u_R,\ a-w_R,\ b-v_R,\ b-t_R,\ c-w_R,\ d-t_R,
\]
\[
u_L-A,\ v_L-A,\ v_L-B,\ w_L-C,\ t_L-C,\ t_L-D.
\]
Here vertex letters also denote their corresponding original costs.
Both copies of a \(Z\) corner have that corner's cost. There are no
edges between the two \(Z\) copies. Thus \(\Gamma\) has sixteen vertices
and twenty-one edges.

**Theorem.** Under the nine displayed local inequalities, \(\Gamma\) has
a vertex cover of cost at most
\[
\alpha+\beta+\gamma+\delta+u+v+w+t. \tag{1}
\]
There are conflict-free original survivors whose deletion cost \(D_{\rm del}\)
satisfies
\[
D_{\rm del}\le\alpha+\beta+\gamma+\delta+
              \sum_{z\in U}z, \tag{2}
\]
where \(U\) is the actual set of corners covered by neither survivor family.
The coefficient one is sharp in both bounds. An optimal cover and an
optimal value of \(D_{\rm del}-\sum_U z\) can be obtained by at most
fifteen explicit candidate deletions, with no division by a cost.

## 2. Exact reduction to three branches

For any deletion \(Q\) covering the original conflicts, let \(U(Q)\) be
its actual uncovered corner set. A corner cannot be covered by survivors
on both sides: those two survivors would form an original conflict.
If one side covers it, the opposite tagged corner vertex must be selected
in an augmented cover; if neither side covers it, neither copy is needed.
Consequently the cheapest completion of \(Q\) has cost
\[
u+v+w+t+D_{\rm del}(Q)-\sum_{z\in U(Q)}z. \tag{3}
\]
Every augmented cover restricts to such a \(Q\), and nonnegative corner
costs allow redundant selected corner copies to be removed. This proves
equality between the augmented optimum and the minimum of (3).

Put \(X=a+b+c+d\), \(Y=A+B+C+D\), \(s_+=\max(s,0)\), and
\[
a_* = a-(w-c)_+,\qquad A_* = A-(v-B)_+,\qquad
\phi(p,q,r)=\min(p,q,p+q-r).
\]
The arguments \(p,q\) of \(\phi\) may be negative when they are \(a_*,A_*\).
There is an exact identity, valid for all nonnegative costs without any
local inequalities,
\[
\operatorname{OPT}_\Gamma-(u+v+w+t)
=\min(f_b,f_C,f_0), \tag{4}
\]
where
\[
\begin{aligned}
f_b&=Y+\min(0,a-u,a+c-u-w),\\
f_C&=X+\min(0,A-u,A+B-u-v),\\
f_0&=b+C+\phi(a_*,A_*,u)+\phi(d,D,t).
\end{aligned} \tag{5}
\]

To prove this, partition conflict-free survivors into three exhaustive
classes. The universal originals \(b=r_{01}\), \(C=c_{10}\) conflict,
so they cannot both survive.

If \(b\) survives, all \(C\)-family originals are deleted. Keep \(d\):
it saves a nonnegative cost and does not change the uncovered set.
The corners \(v,t\) stay covered by \(b\). For \(a,c\), deleting only
\(c\) pays \(c\) with no uncovered gain and is weakly worse than keeping
both. The other choices give \(0,a-u,a+c-u-w\), proving \(f_b\).
If \(C\) survives, all \(R\)-family originals are deleted, \(D\) may
be kept, and the analogous choices for \(A,B\) prove \(f_C\).

If \(b,C\) are both deleted, the remaining conflicts are exactly
\(a-A\) and \(d-D\). The original \(c\) can unlock gain \(w\) only when
\(a\) is deleted, and is then best deleted exactly when \(w>c\).
Similarly \(B\) can unlock \(v\) only when \(A\) is deleted, and is then
best deleted exactly when \(v>B\). The three cover choices for \(a-A\)
therefore give \(a_*,A_*,a_*+A_*-u\).
The three choices for \(d-D\) give \(d,D,d+D-t\).
These two parts share no remaining corner or original, proving \(f_0\).
Ties may always be resolved by keeping the optional leaf.

The first two branches use three candidates each; the last uses the
three left choices times the three right choices, with optional leaves
chosen as just described. These fifteen candidates prove (4) and supply
the claimed exact algorithm, including all zero-cost inputs.

## 3. A one-conflict inequality

For nonnegative \(p,q,r,k\) satisfying \(pq\le kr\),
\[
\phi(p,q,r)\le k. \tag{6}
\]
Indeed, if \(p\le k\) or \(q\le k\), this is immediate. Otherwise
\(p,q>k\), so \(k>0\), and
\[
(p-k)(q-k)>0
\quad\Longrightarrow\quad
p+q-\frac{pq}{k}<k.
\]
Using \(r\ge pq/k\) proves (6). This also treats zero costs without
division by zero.

## 4. Proof for strictly positive costs

Write \(H=\alpha+\beta+\gamma+\delta\). We prove the minimum in (4)
is at most \(H\). All costs in this section are strictly positive.

### 4.1. The middle region

Suppose \(b\le\alpha+\beta\) and \(C\le\alpha+\gamma\). Define
\[
\xi=(b-\beta)_+,\qquad \eta=(C-\gamma)_+.
\]
Then \(0\le\xi,\eta\le\alpha\).
The local inequalities \(cC\le\gamma w\), \(aC\le\alpha w\) give
\[
(w-c)_+\ge \frac{w\eta}{C}\ge\frac{a\eta}{\alpha},
\qquad a_*\le a(1-\eta/\alpha).
\]
This holds also when \(\eta=0\), directly from \(a_*\le a\).
Similarly \(bB\le\beta v\), \(bA\le\alpha v\) imply
\[
A_*\le A(1-\xi/\alpha).
\]
Put
\[
K=\alpha(1-\eta/\alpha)(1-\xi/\alpha)
 =\alpha-\xi-\eta+\xi\eta/\alpha\ge0.
\]
If either \(a_*,A_*\) is negative, then \(\phi(a_*,A_*,u)\le0\le K\).
Otherwise \(a_*A_*\le K u\) follows from \(aA\le\alpha u\);
(6) gives in either case
\[
\phi(a_*,A_*,u)\le K. \tag{7}
\]

When \(\xi\eta=0\), (6) and \(dD\le\delta t\) give
\(\phi(d,D,t)\le\delta=\delta-\xi\eta/\alpha\).
When \(\xi\eta>0\), we have \(b>\beta\), \(C>\gamma\), and
\[
d\le\gamma t/C<t,\qquad D\le\beta t/b<t.
\]
Thus \(\phi(d,D,t)=d+D-t\), and
\[
\begin{aligned}
\delta-\phi(d,D,t)
&\ge dD/t-d-D+t\\
&=(t-d)(t-D)/t\\
&\ge t\,\xi\eta/(bC)\\
&\ge \xi\eta/\alpha,
\end{aligned} \tag{8}
\]
where the last step uses \(bC\le\alpha t\).
Combining (7) and (8) proves
\[
f_0\le b+C+\alpha-\xi-\eta+\delta
     \le\alpha+\beta+\gamma+\delta=H. \tag{9}
\]
The endpoint cases \(\xi=\alpha\) or \(\eta=\alpha\) are included:
then \(K=0\), and (6) remains applicable.

### 4.2. The region \(b>\alpha+\beta\)

Put \(P=\alpha+\beta\), \(Q=\gamma+\delta\), and
\[
\lambda=P/b<1,\qquad \mu=\min(1,Q/d).
\]
Delete all \(C\)-family originals, keep \(a,c\), and choose whether to
delete \(b,d\). Use the following four probabilities for their deletion
indicators \(I_b,I_d\):

| \((I_b,I_d)\) | Probability |
| --- | --- |
| \((1,1)\) | \(\min(\lambda,\mu)\) |
| \((1,0)\) | \((\lambda-\mu)_+\) |
| \((0,1)\) | \((\mu-\lambda)_+\) |
| \((0,0)\) | \(1-\max(\lambda,\mu)\) |

They are nonnegative and sum to one; their marginal probabilities are
\(\lambda,\mu\). Every choice is an actual original conflict cover.
Its actual uncovered set has \(v\) exactly when \(I_b=1\), and \(t\)
exactly when \(I_bI_d=1\); \(u,w\) stay covered by \(a,c\).
The deletion cost minus uncovered gain is therefore
\[
Y+bI_b+dI_d-vI_b-tI_bI_d. \tag{10}
\]
The local inequalities give
\[
A+B\le\lambda v,\qquad
C+D\le\lambda t,\qquad C+D\le(Q/d)t.
\]
Since \(\lambda<1\), the last two imply
\[
C+D\le\min(\lambda,\mu)t. \tag{11}
\]
The expected value of (10) is consequently at most
\[
b\lambda+d\mu\le P+Q=H.
\]
One of the four finite choices has value at most \(H\).
By (4), its minimizing fifteen-candidate algorithm also has value at most
\(H\). No randomized output or integration is needed.

### 4.3. The region \(C>\alpha+\gamma\)

The symmetry is explicit. Swap the original families and transpose
their coordinates, using the new arrays
\[
(a',b',c',d')=(A,C,B,D),\quad
(A',B',C',D')=(a,c,b,d),
\]
\[
(\alpha',\beta',\gamma',\delta')=(\alpha,\gamma,\beta,\delta),
\quad (u',v',w',t')=(u,w,v,t).
\]
The nine inequalities and twenty-one edges become exactly the same
lists in the new labels. Section 4.2 applies because
\(b'=C>\alpha'+\beta'=\alpha+\gamma\).
In old labels its choices delete all \(R\)-family originals, keep
\(A,B\), and possibly delete \(C,D\). The actual uncovered gain is
\(wI_C+tI_CI_D\).
The relevant summed inequalities are
\[
C(a+c)\le(\alpha+\gamma)w,\quad
C(b+d)\le(\alpha+\gamma)t,\quad
D(b+d)\le(\beta+\delta)t.
\]
Thus this case also proves a value at most \(H\).
Together the middle region and these two outer regions exhaust all
strictly positive costs.

## 5. All zero-cost boundaries

For a finite graph the minimum cover cost is the minimum of finitely
many linear functions of its vertex costs, hence is continuous.
We show that every locally feasible nonnegative input is a limit of
strictly positive locally feasible inputs on this same graph.

For \(\varepsilon>0\), replace each original cost by
\(x_r^\varepsilon=x_r+\varepsilon^2\),
\(y_c^\varepsilon=y_c+\varepsilon^2\), and each corner cost by
\(z_z^\varepsilon=z_z+\varepsilon\). For each \(H\) corner set
\[
h_h^\varepsilon=
\max\left(h_h+\varepsilon,\
 \max_{\substack{\text{actual conflicts }e\\H(e)=h}}
 \frac{(x_{r(e)}+\varepsilon^2)(y_{c(e)}+\varepsilon^2)}
      {z_{Z(e)}+\varepsilon}\right). \tag{12}
\]
All entries are positive and satisfy the same nine local conditions.
If \(z_{Z(e)}>0\), the displayed ratio tends to
\(x_{r(e)}y_{c(e)}/z_{Z(e)}\le h_h\).
If \(z_{Z(e)}=0\), local feasibility gives \(x_{r(e)}y_{c(e)}=0\),
and the ratio equals
\(\varepsilon(x_{r(e)}+y_{c(e)})+\varepsilon^3\), tending to zero.
Each finite maximum in (12) therefore tends to \(h_h\).

Apply the strictly positive result and take the limit in the continuous
minimum cover cost and its bound. This proves (1) for the original input.
Equation (3) gives (2). For exact construction at zero costs, simply
use the fifteen candidates of Section 2 on the original input: that
formula already holds on the closed nonnegative domain and uses no
division or limiting search. Initially isolated originals need not be
protected here: every original has a diagonal conflict.

## 6. Every binary relation and partial original family

**Corollary.** Let \(P,I,S,J\) be arbitrary finite sets, each of size at
most two. For arbitrary relations \(E\subseteq P\times I\),
\(F\subseteq S\times J\) and arbitrary partial families
\(R\subseteq P\times J\), \(C\subseteq I\times S\), assign nonnegative
pair costs as in [compatible-pair-costs.md](compatible-pair-costs.md).
Assume \(x_{pj}y_{is}\le h_{ps}z_{ij}\) for every actual conflict.
Then the actual augmented graph has a cover of cost at most
\(\sum_Hh+\sum_Zz\), and there is a pruning with
\[
D_{\rm del}\le\sum_Hh+\sum_{z\in U}z
\]
retaining every original that initially has no conflict. Both conclusions
use the actual cross-corner sets of these partial families.

**Proof.** If either relation is a disjoint union of complete bipartite
blocks, the theorem of
[compatible-pair-costs.md](compatible-pair-costs.md) applies, including
empty sets and isolated coordinates.
Otherwise each relation must have two vertices on each side and exactly
three edges. Indeed, every bipartite graph on at most two vertices per
side with zero, one or two edges has complete nonisolated components,
as does the four-edge graph; the only nonblock case is the three-edge
path. Independently relabel the four coordinate sets so that both
relations are the paths of Section 1.

Complete \(R,C\) to the full two-by-two families. Give each missing
original cost zero, and give each corner outside the actual \(H,Z\)
cost zero. Retain all costs on actual originals and actual corners.
For a full-grid conflict whose originals are both present, its two
corners are in the actual \(H,Z\), so its inequality is the assumed one.
For every other new conflict the product of original costs is zero,
so the completed local inequality holds automatically.
The theorem above supplies a full-grid augmented cover with cost at
most the unchanged budget \(\sum_Hh+\sum_Zz\).

The actual augmented graph is the induced subgraph on its original
vertices and its two actual \(Z\) copies. Restrict the full-grid cover
to these vertices; it covers every actual edge and cannot increase
cost. An original with no original conflict has no augmented edge
either: if \(r=(p,j)\) covered an actual corner \((i,j)\), that corner's
conflict witness would supply a present \(c=(i,s)\) with \(F(s,j)\);
together with \(E(p,i)\) this would be a conflict with \(r\).
The argument for a \(C\) original is symmetric. Remove such isolated
originals from the cover without increasing cost.

Take the unselected originals as survivors, and replace the corner
part of the cover by the cheapest completion described in Section 2.
The same argument for (3) applies to partial families: a corner is
covered by at most one survivor side, and its necessary corner-copy
cost is zero or \(z\) as specified there. Its cost is
\(\sum_Zz+D_{\rm del}-\sum_Uz\), no greater than that of the cover.
This proves the pruning bound and the required retention. All padding
uses zero costs, so the zero-cost proof is essential here. \(\square\)

The result covers the whole binary coordinate domain, rather than
only the complete reflexive grid. For rational inputs the block case
uses the existing exact threshold algorithm. In the path case, pad
with zeros, use the fifteen candidates, then restrict and remove
isolated originals as in the proof.

## 7. Sharpness, provenance and remaining scope

The sharp example of Section 3 of
[reflexive-cost-families.md](reflexive-cost-families.md) is included:
\[
x=h=\begin{pmatrix}2&1\\1&2\end{pmatrix},\qquad
y=z=3x.
\]
There \(H=6\), \(\sum z=18\). The eight disjoint diagonal coverage
edges carry total capacity twenty-four, forcing every augmented cover
to cost at least twenty-four. The same diagonal original conflicts
give \(D_{\rm del}\ge6+\sum_U z\). Deleting all \(R\) realizes equality
in both bounds. The determinant of \(x\) is three, so this is not a
rank-one original-cost table.

The upstream [pruning proof](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/A-proof-of-Seymours-second-neighborhood-conjecture-September-23-2026/build/source/02-pruning.tex)
supplies the conflict/coverage framework and its rank-based unweighted
bound. The product-weighted lifting in [paper.md](paper.md), the block
threshold construction in [compatible-pair-costs.md](compatible-pair-costs.md),
and the two restricted cost families are separately documented antecedents
within this repository. Here the entire independent-cost domain for
the specified two paths is proved, rather than inferred from numerical
examples. The outer-region proof uses a finite common-threshold coupling;
the middle-region proof uses two coupled single-conflict deficits.

Classical related methods include Ahlswede and Daykin,
*An inequality for the weights of two families of sets, their unions and
intersections*, Z. Wahrscheinlichkeitstheorie verw. Gebiete 43 (1978),
183–185 ([author-hosted original](https://www.math.uni-bielefeld.de/ahlswede/homepage/public/30.pdf)),
and *Inequalities for a pair of maps \(S\times S\to S\) with \(S\) a
finite set*, Math. Z. 165 (1979), 267–289
([author-hosted original](https://www.math.uni-bielefeld.de/ahlswede/homepage/public/33.pdf)).
The standard Boolean-lattice four-functions theorem assumes inequalities
for all ordered input pairs. Our nine inequalities concern only the
oriented conflicts, out of sixteen possible ordered original pairs;
the missing seven hypotheses prevent a direct invocation of that theorem.
This comparison does not exclude a further reduction to a classical result.

The general independent-cost theorem for larger coordinate sets and
arbitrary \(E,F\), larger path relations, equality classification for independent costs, and a
complete Lean proof remain open. The written theorem above does not
resolve the upstream second-neighborhood conjecture or establish
historical priority.
