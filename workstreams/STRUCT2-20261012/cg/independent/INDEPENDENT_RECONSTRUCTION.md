# Odd claw graphs: an independent reconstruction from the original definition

## Scope and source

Let \(n\geq 3\) be odd. The object is the claw graph in Russell Mizzi,
*Lifting and Folding: A Framework for Unstable Graphs and TF-Cousins*,
arXiv:2603.27559v3 (10 September 2026), Definition 6.1. The question in
Section 7 is the number of ordinary isomorphism classes of finite simple
graphs whose canonical double cover is isomorphic to that of this claw graph.

Primary source: <https://arxiv.org/html/2603.27559v3>.

The argument below was reconstructed from that definition before consulting
the earlier project candidate. It proves that there are exactly three bases,
including the original graph, hence exactly two TF-cousins. The known
existence of the companion and of a reflection fold is not claimed as new:
Mizzi's Section 7 attributes the latter to V. Rozhoň and R. Šámal using
Bolzano. Originality of the full classification requires a separate
comparison with that literature.

## 1. Original graph and a coordinate model for its cover

Put

\[
h=2n,\qquad k=3n,\qquad N=6n=3h=2k.
\]

Thus \(h\geq6\) is even and \(k\) is odd. Write the original leaves as
\(\ell_a\), \(a\in\mathbb Z_k\), where
\(\ell_a=\ell_{a\bmod n,\lfloor a/n\rfloor}\) using the representative
\(0\leq a<k\). Definition 6.1 gives exactly these edges:

\[
u_tu_{t+1},\qquad u_t\ell_{t\bmod k},\qquad
\ell_a c_{a\bmod n}.
\]

The ring indices are in \(\mathbb Z_N\), and the centre indices in
\(\mathbb Z_n\). In the canonical double cover each original edge joins
the two opposite layers.

The cover has the following alternate coordinates:

\[
\begin{aligned}
X_t&=(u_t,t\bmod2),\\
Y_t&=(u_{t+k},t\bmod2),\\
A_t&=(\ell_{t\bmod k},1-(t\bmod2)),\\
Z_s&=(c_{s\bmod n},s\bmod2),
\end{aligned}
\qquad t\in\mathbb Z_N,\quad s\in\mathbb Z_h.
\]

Oddness of \(n\) and \(k\) shows that these are bijective coordinates:
the two lifts of each original vertex receive distinct labels. Directly
substituting the original edges gives exactly

\[
X_tX_{t+1},\quad Y_tY_{t+1},\quad
X_tA_t,\quad Y_tA_t,\quad A_tZ_{t\bmod h}. \tag{1}
\]

Denote this graph by \(B_n\). It consists of two \(N\)-cycles, a subdivided
matching between corresponding positions, and one centre for each residue
modulo \(h\), joined to the three leaves in that residue class. It has
\(2N+N+h=20n\) vertices and \(5N=30n\) edges. It is connected: one ring
is connected, every leaf meets it, every vertex of the other ring meets a
leaf, and every centre meets three leaves.

Its two parts are given by the colour

\[
\chi(X_t)=\chi(Y_t)=t\bmod2,\quad
\chi(A_t)=1-t\bmod2,\quad \chi(Z_s)=s\bmod2. \tag{2}
\]

All edge types in (1) reverse this colour. Since \(B_n\) is connected,
this is its unique bipartition up to reversal.

## 2. Six-cycles intrinsically recover the three vertex types

### Lemma 1

No centre \(Z_s\) lies on a six-cycle when \(n\geq3\).

**Proof.** If a six-cycle contains \(Z_s\), its two neighbours on the cycle
are distinct leaves \(A_p,A_q\) with \(p\equiv q\pmod h\). The rest of the
cycle is a four-edge path from \(A_p\) to \(A_q\) avoiding \(Z_s\).
Its first and last internal vertices must be ring vertices, because each
of these leaves has only one centre neighbour. Its middle internal vertex
is either a ring vertex or a leaf; it cannot be a centre because ring
vertices are not adjacent to centres.

If that middle vertex is a ring vertex, the path between its two ring
neighbours stays in one ring, and \(q-p\equiv0,2,-2\pmod N\). Equality
\(q=p\) is excluded by distinct leaves. If the middle vertex is a leaf,
its two ring neighbours have the same index, giving \(q=p\), also
impossible. But distinct residues in the same class modulo \(h\) differ by
\(h\) or \(2h\) modulo \(N=3h\), neither of which is \(2\) or \(-2\) when
\(h\geq6\). This is a contradiction. \(\square\)

### Lemma 2

The six-cycles of \(B_n\) are exactly the \(N\) cycles

\[
Q_t=(X_t,X_{t+1},A_{t+1},Y_{t+1},Y_t,A_t,X_t).
\]

Every ring vertex and every leaf lies on exactly two such cycles.

**Proof.** By Lemma 1, a six-cycle avoids all centres. In the remaining
graph, moving from one ring to the other uses a two-edge path through a
leaf. Any cycle uses an even number of these paths. With no such path it
would be an entire ring, of length \(N\geq18\). Four or more paths already
use at least eight edges. With exactly two paths, four edges are used at
the leaves, so the two remaining ring segments must each be a single edge.
Their indices are consecutive, giving precisely \(Q_t\).
The incidence assertion follows from the displayed cycles. \(\square\)

Consequently the centres are exactly the vertices lying on no six-cycle.
Their neighbourhood is exactly the set of leaves. The remaining vertices
are exactly the ring vertices. These are intrinsic descriptions, preserved
by every automorphism. The subgraph induced by the ring vertices consists
of exactly two \(N\)-cycles.

For \(n=1\), this mechanism fails explicitly: with \(h=2,N=6\),

\[
Z_0,A_0,X_0,X_1,X_2,A_2,Z_0
\]

is a six-cycle through a centre. No conclusion below is extended to this
parameter. Mizzi identifies its cover as the Desargues graph and records
the known two-base classification separately.

## 3. The full automorphism group, including its upper bound

Define \(r,f,\tau\) by

\[
r:T_i\mapsto T_{i+1},\qquad f:T_i\mapsto T_{-i},
\]

for each indexed type, reducing centre indices modulo \(h\), and by
\(\tau(X_i)=Y_i,\tau(Y_i)=X_i\), with \(\tau\) fixing every leaf and centre.
Formula (1) shows directly that these are automorphisms. They satisfy

\[
r^N=f^2=\tau^2=1,\qquad frf=r^{-1},\qquad
[\tau,r]=[\tau,f]=1.
\]

These generate \(D_N\times C_2\), where \(D_N\) denotes the symmetry group
of an \(N\)-gon and has order \(2N\).

For the **upper bound**, let \(\alpha\in\operatorname{Aut}(B_n)\).
The intrinsic recovery above forces \(\alpha\) to send the \(X\)-ring to
one of the two ring components. Its restriction to that cycle has the form

\[
X_i\longmapsto X_{a+\epsilon i}\quad\hbox{or}\quad
X_i\longmapsto Y_{a+\epsilon i},\qquad
a\in\mathbb Z_N,\quad\epsilon\in\{1,-1\}.
\]

There are \(4N\) possibilities. Each determines the entire automorphism:
the unique leaf neighbour of each \(X_i\) determines the image of \(A_i\);
the other ring neighbour of \(A_i\) determines the image of \(Y_i\);
the unique centre neighbour of \(A_i\) determines the image of its centre.
All leaves and all centres occur this way. Thus the restriction is
injective and \(|\operatorname{Aut}(B_n)|\leq4N\). The explicit group above
attains every possibility. Therefore

\[
\boxed{\operatorname{Aut}(B_n)=\langle r,f\rangle\times\langle\tau\rangle
\cong D_{6n}\times C_2,\qquad |\operatorname{Aut}(B_n)|=24n.} \tag{3}
\]

In these coordinates the original deck involution is

\[
\delta=r^k\tau. \tag{4}
\]

For example, it sends \(X_i\) to \(Y_{i+k}\), and \(A_i\) to \(A_{i+k}\).

## 4. Exhaustive classification of strongly switching involutions

Call an automorphism *strongly switching* if it is an involution reversing
the bipartition and \(v\not\sim g(v)\) for every vertex \(v\). A part-reversing
map has no fixed vertices automatically.

Every group element is uniquely \(r^a f^e\tau^b\), with
\(a\in\mathbb Z_N\) and \(e,b\in\{0,1\}\). Formula (2) shows that it reverses
the bipartition exactly when \(a\) is odd.

If \(e=0\), involutivity means \(2a\equiv0\pmod N\), so \(a=0\) or \(a=k\).
Only \(a=k\) is odd. Thus the only two part-reversing rotational
involutions are

\[
r^k,\qquad r^k\tau.
\]

Both are strong: the first maps a ring vertex to its antipode, a distance
\(k\geq9\) along the ring, while the second maps it into the other ring.
Leaves and centres stay within their types, which contain no edges.

If \(e=1\), every \(r^af\tau^b\) is an involution; it is switching exactly
when \(a\) is odd. For \(b=0\), choose the integer representative
\(i=(a-1)/2\). Then

\[
r^af(X_i)=X_{i+1}\sim X_i,
\]

so it is not strong. For \(b=1\), ring vertices map into the other ring,
and leaves and centres again remain within their types. Consequently all
these involutions are strong. The complete set is

\[
\boxed{\{r^k,r^k\tau\}\;\cup\;
\{r^af\tau: a\in\mathbb Z_N\text{ odd}\}.} \tag{5}
\]

It has \(k+2=3n+2\) elements. The two rotational elements are central and
give singleton conjugacy classes. The remaining \(k\) elements form one
class, since

\[
r^t(r^af\tau)r^{-t}=r^{a+2t}f\tau
\]

runs through every odd exponent. There are exactly three classes, with
sizes

\[
\boxed{1,\quad1,\quad3n.} \tag{6}
\]

## 5. Why these classes count all finite simple bases

For completeness, the needed classical folding correspondence has a
direct proof in this setting. Let \(B\) be a connected bipartite graph and
\(g\) a strongly switching involution. Define \(Q_g\) to have the
two-element \(g\)-orbits as vertices, adjacent when representatives are
adjacent in \(B\). Each orbit has exactly one vertex of each colour.
Strongness excludes loops. If an orbit pair is adjacent, applying \(g\)
supplies the opposite cross edge too. The map

\[
x\longmapsto([x],\chi(x))
\]

is consequently an isomorphism \(B\cong\operatorname{CDC}(Q_g)\).
There is no loss from treating \(Q_g\) as simple: the two members of an
orbit have opposite colours and therefore cannot both be neighbours of
one vertex of \(B\).

Conversely, if a finite simple graph \(H\) has
\(\operatorname{CDC}(H)\cong B\), transporting its deck involution to \(B\)
produces a strongly switching involution. Connectedness of \(B\) forces
\(H\) to be connected and non-bipartite. Thus this converse covers all
finite simple \(H\), including the possibility of disconnected graphs
in the original quantifier, which the connected cover rules out.

Conjugate involutions give isomorphic quotients. Conversely an isomorphism
\(Q_g\cong Q_{g'}\) lifts canonically to an isomorphism of their CDCs which
commutes with the deck maps; conjugating by the displayed identifications
gives an automorphism of \(B\) sending \(g\) to \(g'\). Hence ordinary base
isomorphism classes are in bijection with these conjugacy classes.
This is the existing correspondence of Pacco–Scapellato, also discussed
in Mizzi's Theorem 4.6; the argument here supplies the hypotheses explicitly.

The cover is reduced as well. Different vertex types have different
neighbourhood-type profiles. Two ring vertices with equal neighbourhoods
would have the same unique leaf neighbour, hence the same index; the
two ring types at that index have disjoint ring-neighbour sets. Leaf
neighbourhoods determine their indices, and distinct centres have disjoint
leaf-neighbour sets. Thus there are no distinct vertices with the same
open neighbourhood. Any base with this CDC is reduced, since twins in a
base would give twins in one layer of its cover. Reducedness is therefore
available if one uses a version of the classical correspondence requiring it.

## 6. Identification and automorphism groups of the three bases

The fold of \(r^k\tau=\delta\) is the original \(\operatorname{CG}(n)\).
The fold of \(r^k\) identifies antipodal indices in each ring separately,
so its two ring subgraphs are both \(C_k\), while the remaining incidence
is exactly that in Definition 6.1. It is the known companion
\(\operatorname{CG}'(n)\).

Take \(g=rf\tau\) for the third class. Ring-orbit representatives can be
chosen as all \(X_i\), because \(Y_j\) is paired with \(X_{1-j}\).
The orbit of \(A_0\) contains \(A_1\) and is adjacent to both \(X_0\) and
\(X_1\), which are themselves adjacent. This gives a triangle. The same
construction at \(k,k+1\) gives a second triangle. These are the only
triangles: centres have only leaf neighbours, leaves have only ring and
centre neighbours, and a leaf connects consecutive ring positions only
when \(2i\equiv0\) or \(2\pmod N\). In contrast, both known bases are
triangle-free when \(n\geq3\).

For any strongly switching \(g\),

\[
\operatorname{Aut}(Q_g)\cong
C_{\operatorname{Aut}(B_n)}(g)/\langle g\rangle.
\]

Indeed a commuting automorphism descends to the quotient, every quotient
automorphism lifts canonically, and the kernel consists of identity and
\(g\). To see the kernel assertion, use the connected bipartition:
a quotient-trivial automorphism preserving parts fixes every vertex,
whereas one reversing parts acts by \(g\) everywhere.

By (3) and (6), the respective automorphism-group orders are

\[
\boxed{12n,\qquad12n,\qquad4.} \tag{7}
\]

Every base is cubic and connected by its canonical-cover representation.
Exactly one of the three classes is the original deck class. Therefore,
for every odd \(n\geq3\), the graph \(\operatorname{CG}(n)\) has exactly
two TF-cousins, up to ordinary graph isomorphism.

## Verification and limitations

The statements above are a full parameter proof, not deductions from a
finite enumeration. A separate checker should build the original edges,
form the CDC without using (1), check the coordinate bijection against all
edges, and compute small examples directly. Such checks can detect errors
in transcription or the model map; they are not substitutes for Lemmas
1–2 or the injective restriction argument.

This document makes no claim of Lean compilation, human peer review, or
historical priority. The \(n=1\) case is intentionally outside the theorem.
