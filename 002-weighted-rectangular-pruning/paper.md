# Product-weighted pruning for two rectangular relations

Research note, 8 October 2026.

## Scope and provenance

We prove a weighted vertex-cover inequality and an associated pruning theorem for two arbitrary finite rectangular relations. The weights on the four kinds of coordinate pairs are products of four independent coordinate weights. The conclusion includes a deterministic algorithm for rational data and a sharp universal constant.

The unweighted rank argument is adapted from the pruning lemma in OpenAI, *A proof of Seymour's second-neighborhood conjecture* (23 September 2026), specifically `build/source/02-pruning.tex`, at repository commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`:

[Pinned upstream source](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/A-proof-of-Seymours-second-neighborhood-conjecture-September-23-2026/build/source/02-pruning.tex).

The rectangular unweighted formulation is already a corollary of that lemma by using four disjoint coordinate types. We do not claim it separately as an original discovery. Our extension is the product-weighted cover bound, its pruning consequence, and an exact certificate workflow. To make the note independently checkable, we prove the requisite unweighted statement here rather than assume the upstream lemma or its asserted second-neighborhood theorem. Priority and equivalence with other literature have not been established. The computational examples verify instances; the proof below establishes the general theorem.

## 1. Definitions and statements

Let \(P,I,S,J\) be finite sets, possibly empty. Fix relations
\[
 E\subseteq P\times I,\qquad F\subseteq S\times J,
\]
and families
\[
 R\subseteq P\times J,\qquad C\subseteq I\times S.
\]
All occurrences of these sets in graphs are separate, tagged copies. A member \(r=(p,j)\in R\) conflicts with \(c=(i,s)\in C\) precisely when \((p,i)\in E\) and \((s,j)\in F\). Define the two sets of cross-corners
\[
 Z=\{(i,j):\exists p,s\ ((p,j)\in R,(i,s)\in C,(p,i)\in E,(s,j)\in F)\},
\]
\[
 H=\{(p,s):\exists i,j\ ((p,j)\in R,(i,s)\in C,(p,i)\in E,(s,j)\in F)\}.
\]
A member \((p,j)\in R\) covers \((i,j)\in Z\) if \((p,i)\in E\). A member \((i,s)\in C\) covers \((i,j)\in Z\) if \((s,j)\in F\).

Construct a bipartite graph \(\Gamma\) whose left side is \(R\sqcup Z_L\), and whose right side is \(C\sqcup Z_R\). Its edges are:

1. the pairs of conflicting members of \(R\) and \(C\);
2. \(r z_R\) whenever \(r\) covers \(z\);
3. \(z_L c\) whenever \(c\) covers \(z\).

There are no other edges, in particular none between the two copies of \(Z\).

Assign arbitrary nonnegative real coordinate weights
\[
 (a_p)_{p\in P},\quad(b_i)_{i\in I},\quad(c_s)_{s\in S},\quad(d_j)_{j\in J}.
\]
Give graph vertices the costs
\[
 w(p,j)=a_p d_j\quad(r\in R),\qquad
 w(i,s)=b_i c_s\quad(c\in C),\qquad
 w(z_L)=w(z_R)=b_i d_j\quad(z=(i,j)).
\]
For a vertex set \(K\), \(w(K)\) is the sum of its costs, counting the two copies of \(Z\) separately.

**Theorem 1 (weighted cover).** There is a vertex cover \(K\) of \(\Gamma\), containing no isolated vertex, such that
\[
 w(K)\leq \sum_{(p,s)\in H}a_p c_s+
                    \sum_{(i,j)\in Z}b_i d_j. \tag{1}
\]
The coefficient one on the right cannot be replaced by a smaller universal coefficient.

**Theorem 2 (weighted pruning).** There are conflict-free subfamilies \(R'\subseteq R\), \(C'\subseteq C\) retaining every member that initially conflicts with no opposite member. If
\[
 U=\{z\in Z:z\text{ is covered by no member of }R'\cup C'\},
\]
then
\[
 \sum_{(p,j)\in R\setminus R'}a_p d_j+
 \sum_{(i,s)\in C\setminus C'}b_i c_s
 \leq \sum_{(p,s)\in H}a_p c_s+
       \sum_{(i,j)\in U}b_i d_j. \tag{2}
\]
The product assumption applies to all four kinds of pair costs. We assert no version with independently assigned, arbitrary costs on individual pair vertices.

A separate [compatible pair-cost theorem](compatible-pair-costs.md)
allows nonnegative independent pair costs under a local multiplicative
constraint when one relation is a disjoint union of complete bipartite
blocks. Its finite-threshold proof and tight nonproduct example concern
that additional structural hypothesis; the theorems above retain their
arbitrary-relation product-cost scope.

## 2. A support-rank fact

**Lemma 3.** Let \(D:\mathbb Q^T\to\mathbb Q^Q\) have maximum rank among matrices with entries allowed only on a prescribed subset \(B\subseteq Q\times T\). For \(x\in\ker D\), \(y\in\ker D^{\mathsf T}\), and \((q,t)\in B\), one has \(x_t y_q=0\).

**Proof.** If both coordinates were nonzero, modify the allowed entry by a nonzero rational \(\lambda\), obtaining \(D_\lambda=D+\lambda e_q e_t^{\mathsf T}\). Since \(D_\lambda x=\lambda x_t e_q\), the new image contains \(e_q\). For every vector \(v\), \(Dv=D_\lambda v-\lambda v_t e_q\), so it contains the old image as well. But \(y_q\ne0\), and \(y\) annihilates the old image, hence \(e_q\) was outside that image. The rank has increased, contradicting maximality. This proof also covers rectangular matrices and empty kernels. \(\square\)

## 3. The unweighted matching bound

**Lemma 4.** Every matching of \(\Gamma\) has size at most \(|H|+|Z|\).

**Proof.** The case of no conflicts is immediate: \(H=Z=\varnothing\), and \(\Gamma\) has no edges. Otherwise choose a maximum matching \(M\) that uses the minimum possible number \(k\) of edges joining original members. Write \(\alpha\) for its \(R\)--\(Z_R\) edges and \(\beta\) for its \(Z_L\)--\(C\) edges, and set \(\ell=|\alpha|\), \(t=|\beta|\). Thus \(|M|=k+\ell+t\).

The matching \(\alpha\) is maximum in the \(R\)--\(Z_R\) subgraph. Indeed, an augmenting path for \(\alpha\) ends at a vertex of \(Z_R\) unmatched by \(M\). Its initial vertex in \(R\), unmatched by \(\alpha\), is either unmatched by \(M\) or belongs to an original conflict edge of \(M\). In the first case augmenting increases \(|M|\); in the second, removing that conflict edge before augmenting keeps \(|M|\) fixed and decreases \(k\). Either outcome is impossible. The symmetric argument proves maximality of \(\beta\).

Introduce independent rational indeterminates \(u_{pi}\) on \(E\) and \(v_{sj}\) on \(F\), treating other entries as zero. Consider four matrices
\[
 L:\mathbb Q^R\to\mathbb Q^Z,\quad
 N:\mathbb Q^Z\to\mathbb Q^C,\quad
 B:\mathbb Q^R\to\mathbb Q^H,\quad
 A:\mathbb Q^H\to\mathbb Q^C,
\]
with nonzero entries allowed exactly as follows:
\[
 L_{(i,j),(p,j)}=u_{pi},\quad
 N_{(i,s),(i,j)}=v_{sj},\quad
 B_{(p,s),(p,j)}=v_{sj},\quad
 A_{(i,s),(p,s)}=u_{pi}. \tag{3}
\]
For endpoints \((p,j)\in R,(i,s)\in C\), a product entry in \(NL\) can use only the intermediate index \((i,j)\), and one in \(AB\) can use only \((p,s)\). If the endpoints conflict, both intermediate indices are present and both products equal \(u_{pi}v_{sj}\). Otherwise both products are zero. Consequently
\[
 NL=AB. \tag{4}
\]

We select a single rational specialization for which:

* \(\operatorname{rank}L=\ell\), and the columns at the original endpoints of \(\alpha\) form a basis of its image;
* \(\operatorname{rank}N^{\mathsf T}=t\), and the columns at the original endpoints of \(\beta\) form a basis of its image;
* for every \((p,i)\in E\), the matrix
  \[
  D^{p,i}=(v_{sj})_{s\in S_i,\,j\in J_p},\quad
  S_i=\{s:(i,s)\in C\},\quad J_p=\{j:(p,j)\in R\},
  \]
  attains maximum rank on its allowed support.

Here is a justification that takes account of repeated variables in (3). The minor of \(L\) on the endpoints of \(\alpha\) is block diagonal by \(j\). Inside each block its allowed entries are distinct variables. A matching gives a determinant monomial that cannot cancel with a different permutation, so each block determinant is a nonzero polynomial. Their product is nonzero even if different blocks reuse variables. Conversely any nonzero minor supplies a matching in that subgraph, which bounds every specialization's rank by \(\ell\). This proves the first property whenever that selected minor is nonzero. The same reasoning applies to \(N^{\mathsf T}\), using blocks by \(i\). Each \(D^{p,i}\) uses distinct variables in its individual entries. Choose one minor that achieves its maximum support rank; its determinant is a nonzero polynomial, or the constant one if the rank is zero. The product of all these finitely many selected minors is nonzero over \(\mathbb Q\). A nonzero polynomial over the infinite field \(\mathbb Q\) has a rational point at which it is nonzero: induction on the number of variables reduces this to the fact that a nonzero univariate polynomial has finitely many roots. Choose such a point. All three properties then hold simultaneously.

At this specialization, each original matched edge \((r,c)\in M\) has lifts
\[
 x^r=e_r+\sum_{a\in R_\alpha}\lambda_a^r e_a\in\ker L,
 \qquad
 y^c=e_c+\sum_{b\in C_\beta}\mu_b^c e_b\in\ker N^{\mathsf T}, \tag{5}
\]
where \(R_\alpha,C_\beta\) denote original endpoints of those two matchings. The basis properties give (5), since the negative of any other column is a linear combination of the basis columns. Original conflict-edge endpoints are disjoint from these basis sets.

We claim that, for every conflict \(((p,j),(i,s))\), every \(x\in\ker B\), and every \(y\in\ker N^{\mathsf T}\),
\[
 x_{pj}y_{is}=0. \tag{6}
\]
Fix \((p,i)\in E\). Each nonzero-supported row \(s\) of \(D^{p,i}\) has some \(j\in J_p\) with \((s,j)\in F\); the resulting conflict places \((p,s)\) in \(H\). The equation \((Bx)_{(p,s)}=0\) is exactly
\(\sum_{j\in J_p}v_{sj}x_{pj}=0\). A zero-supported row satisfies it automatically. Hence the restriction \((x_{pj})_{j\in J_p}\) belongs to \(\ker D^{p,i}\). The analogous argument on columns uses \((i,j)\in Z\) and \(N^{\mathsf T}y=0\), and places \((y_{is})_{s\in S_i}\) in \(\ker(D^{p,i})^{\mathsf T}\). Lemma 3 now proves (6) on every allowed entry.

For a conflict edge \((r,c)\in M\), the coordinate \(y^c_c=1\). Equation (6) therefore says that every vector in \(\ker B\) vanishes at \(r\). It follows that the \(k\) vectors \(Bx^r\) are linearly independent: a linear combination with image zero has coefficients equal to its coordinates on those \(k\) endpoints, because the correction terms of (5) are supported on \(R_\alpha\). All those coordinates must vanish. By (4), every \(Bx^r\) belongs to \(\ker A\). Thus \(\dim\ker A\geq k\).

Rank-nullity and (4) yield
\[
 |H|\geq k+\operatorname{rank}A
       \geq k+\operatorname{rank}(NL)
       \geq k+\ell+t-|Z|.
\]
For the last inequality, the kernel of \(N\) has dimension \(|Z|-t\), so restriction of \(N\) to the \(\ell\)-dimensional image of \(L\) has rank at least \(\ell-(|Z|-t)\). Rearranging proves the claim. \(\square\)

**Lemma 5.** The unweighted graph \(\Gamma\) has a vertex cover, excluding isolated vertices, of cardinality at most \(|H|+|Z|\).

**Proof.** From a maximum matching, start at all unmatched left vertices. Traverse unmatched edges from left to right and matched edges from right to left. Let \(T_L,T_R\) be the reached vertices. No unmatched right vertex is reached, because that would provide an augmenting path. A matched edge has either both or neither endpoint reached. The set of unreached left vertices together with reached right vertices covers every edge and contains exactly one endpoint from every matched edge. It contains no isolated vertex. Its size is the matching size, which Lemma 4 bounds. This supplies the required cover without assuming any external matching theorem. \(\square\)

## 4. Product weights by a correlated cover and a random transversal

**Proof of Theorem 1.** First suppose all coordinate weights are positive integers. Replace each \(p\in P\) by \(a_p\) copies, each \(i\) by \(b_i\) copies, each \(s\) by \(c_s\) copies, and each \(j\) by \(d_j\) copies. Replace each relation pair and each family member by all pairs of the relevant copies. Apply Lemma 5 to the resulting rectangular instance. Its cross-corners are precisely the copies of the base cross-corners, so it supplies a cover \(\widehat K\) of size at most
\[
 \sum_H a_pc_s+\sum_Z b_id_j. \tag{7}
\]

Independently choose one uniform copy for each individual base coordinate in all four sets. A base graph vertex is included in \(K\) when its chosen pair of copies lies in \(\widehat K\). The same chosen copies of \(i,j\) are used for both \(z_L\) and \(z_R\). Then \(K\) is a cover of the base graph: for each of its edges, the chosen copies form an edge of the lifted graph, so at least one selected endpoint belongs to \(\widehat K\). In particular the argument respects the shared coordinate on every coverage edge; independently selecting copies for graph vertices would not suffice.

For \(r=(p,j)\), the probability of inclusion is the number of its copies in \(\widehat K\) divided by \(a_pd_j\). Its expected cost is therefore exactly that number. The same calculation holds for \(C\) and the two separate copies of \(Z\). Adding expectations gives
\[
 \mathbb E[w(K)]=|\widehat K|.
\]
Some transversal has cost at most (7). Remove any isolated vertices from its cover, which can only reduce its cost. This proves (1) for positive integer weights.

For positive rational weights, multiply every coordinate weight by one common denominator. All vertex costs and both right-hand sums are multiplied by the square of that denominator; the integer case therefore proves (1). For arbitrary nonnegative real weights, approximate them by positive rational weights. There are only finitely many covers of the fixed finite graph. One cover supplied along the approximating sequence occurs infinitely often. Along that subsequence, its cost and the bound converge to the corresponding costs for the original weights, since each is a finite sum of products. It thus satisfies (1). Isolated vertices can again be removed. Empty coordinate sets or families cause no difficulty; with no conflicts the empty cover suffices.

For sharpness, take one member in each of \(P,I,S,J\), with both relations and both families containing their unique possible pair, and put all four weights equal to one. Then \(|H|=|Z|=1\), and \(\Gamma\) is a four-vertex path. Its two disjoint endpoint edges force any cover to have at least two vertices. The right side of (1) is two. Thus no common coefficient below one works. \(\square\)

## 5. The pruning charge and its sharpness

**Proof of Theorem 2.** Choose the cover from Theorem 1, and delete its original \(R\)- and \(C\)-members. Since all conflict edges are covered, the survivors have no conflict.

Every initially conflict-free original member is isolated in \(\Gamma\). To verify this for \(r=(p,j)\), suppose it covers \(z=(i,j)\in Z\). A conflict witnessing membership of \(z\) supplies some \((i,s)\in C\) with \((s,j)\in F\); this conflicts with \(r\). The other side is analogous. Thus the chosen cover deletes none of the initially conflict-free members.

If \(z\in Z\setminus U\), some survivor covers it. The corresponding coverage edge forces the opposite copy of \(z\) into the cover. Distinct points charge distinct cover vertices, each with cost \(b_i d_j\). Consequently the cost of the deleted originals is at most
\[
 w(K)-\sum_{Z\setminus U}b_i d_j
 \leq\sum_H a_pc_s+\sum_U b_id_j,
\]
which is (2). The reasoning also holds when some costs are zero. \(\square\)

The pruning coefficient is sharp separately. For the same single-conflict, all-ones instance, deleting only one original costs one and leaves \(U=\varnothing\); deleting both costs two and leaves the one point uncovered. Thus every feasible pruning has deletion cost divided by \(|H|+|U|\) equal to one.

## 6. Exact construction for rational weights

For nonnegative rational weights, compute \(H,Z,\Gamma\) directly. Give a directed network a source \(s_0\), a sink \(t_0\), and the vertices of \(\Gamma\). Add source-to-left arcs of capacity \(w(v)\), right-to-sink arcs of capacity \(w(v)\), and left-to-right arcs for graph edges of capacity \(M\), where \(M\) is strictly larger than the sum of all vertex costs. Multiply all capacities by a common denominator to make them integers.

A minimum cut has capacity at most the total vertex cost, and therefore crosses no left-to-right arc of capacity \(M\). Its unreached left and reached right vertices give a minimum-cost cover. Removing isolated vertices is harmless. Theorem 1 bounds this minimum cost, and the deletion rule in Section 5 supplies Theorem 2. All graph sets have polynomial size in the explicit finite input. Edmonds-Karp uses \(O(VE^2)\) arithmetic operations on this network; the integer capacities have polynomial bit length in the rational input. Thus the construction has polynomial bit complexity.

The executable `code/solve.py` implements this procedure with `fractions.Fraction` and integer augmenting paths. It emits the cover, retained families, and a feasible integer flow. The separate `code/check_certificate.py` reconstructs the graph and network from the input and checks:

* input domains, relations, and nonnegative rational weights;
* every required cover edge and the preservation of initially conflict-free members;
* the flow's capacity bounds and conservation at every internal vertex;
* equality of flow value and cover cost after scaling;
* (1), the actual uncovered set, and (2), using exact fractions.

Capacity bounds and conservation show that every cut has capacity at least the flow value: sum conservation over the source side and discard nonnegative incoming flow. The checked cover provides a cut of equal value. Hence a successful certificate proves optimality of that instance's cover, in addition to its pruning inequality. No floating-point values or solver assumptions enter this certificate.

The included examples are a sharp four-vertex instance, a rational rectangular instance, and a zero-weight boundary instance. They illustrate and independently certify finite cases, rather than replace the proof in Sections 2-5. The stress program additionally enumerates all two-element rectangular instances and compares the solver to independent certificate checks; its finite range is stated in its output.

## 7. Limits and further questions

The theorem removes the requirement that both coordinate moves arise from a common relation, and allows four distinct weight systems, including zero weights. It does not permit arbitrary independently specified costs on pair vertices. We have given equality witnesses, rather than classified all equality cases. A characterization of those cases or a genuinely broader class of compatible nonproduct costs would be a further problem. This note makes no assertion that the underlying second-neighborhood conjecture has been independently formalized here.

Separate subsequent notes establish a [finite-threshold construction for
compatible pair costs when either relation is a union of complete
bipartite blocks](compatible-pair-costs.md) and [two complete-grid cost
families on reflexive relations](reflexive-cost-families.md). The latter
allows both relations to be nonblock, with proportional original tables
or a specified nonproportional exchange family. These are additional
written theorems with their own hypotheses and exact checks; the local
condition for arbitrary independently specified costs remains open.
