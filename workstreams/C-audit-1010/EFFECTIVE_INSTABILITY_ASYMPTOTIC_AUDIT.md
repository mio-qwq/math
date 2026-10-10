# Independent support-rigidity audit and effective remainder for JGT Problem 5.3

**Agent C-audit-1010 / 2026-10-10 UTC.** This is a **new proof refinement of the frozen full asymptotic candidate**, not a different solution submitted as accepted. No ROOT acceptance, Lean compilation, human peer review or historical priority is claimed. Do not modify the original frozen source `GLOBAL_NONTRIVIAL_INSTABILITY_ASYMPTOTIC.md`.

## 0. Original scope and provenance

Hujdurović–Mitrović, *Some conditions implying stability of graphs*, *Journal of Graph Theory* 105 (2024), 98–109, DOI 10.1002/jgt.23018, §5 **Problem 5.3**, asks for an approximation of the number of **connected, nonbipartite, open-neighbourhood-twin-free graphs whose canonical double cover has an unexpected automorphism**. Their published **Construction 5.1 / Proposition 5.2** supplies the four-new-vertex gadget; this note neither invents it nor asserts priority over earlier random-graph arguments. The original wording, Construction 5.1 and all edge-definition assumptions were read directly on 2026-10-10: https://onlinelibrary.wiley.com/doi/full/10.1002/jgt.23018 .

Let \(L_n\) be the number of **labelled** graphs in this exact class, \(U_n\) the number of graph-isomorphism classes. Define

\[
K_n=3\binom n4,\qquad
M_n=2^{\binom n2-2n+3}.
\]

The earlier complete candidate predicted \(L_n\sim K_nM_n\) and \(U_n\sim 2^{\binom{n-4}{2}+2(n-4)-1}/(n-4)!\). This note makes two previously computer-supported steps elementary and upgrades the high-support entropy bound. Its **new quantitative theorem candidate** is

\[
\boxed{\quad
n\ge1024
\ \Longrightarrow\
\left|\frac{L_n}{K_nM_n}-1\right|
\le 2^{-9n/20}.
\quad}\tag{E}
\]

This bounds the **labelled** convergence rate. It does NOT supply the same explicit error bound for unlabelled \(U_n\); that still uses a separate classical unlabelled-graph asymptotic and the original marked-structure argument.

## 1. Elementary exclusion of support sizes 2 and 3

For a non-diagonal TF-automorphism \((\alpha,\beta)\), the exact original edge/nonedge condition is

\[
A(u,v)=A(\alpha u,\beta v)\quad\text{for every ordered }u,v.
\]

Set \(S=\operatorname{supp}(\alpha)\cup\operatorname{supp}(\beta)\), \(s=|S|\), and let \(\Gamma=\langle\alpha,\beta\rangle\) have \(t\) orbits on S. Outside S, both permutations fix each vertex. Taking the TF relation with one endpoint outside S, and then its transposed version, proves that all vertices in the **same \(\Gamma\)-orbit** have identical neighbours outside S. Moreover, **both** \(\alpha\) and \(\beta\) preserve the degree **within S** of every vertex: sum the TF equation over v∈S and use that \(\beta\) permutes S, and similarly for its transpose.

Every orbit on S has size≥2. For s=2 or 3, \(\Gamma\) therefore has **one transitive orbit**. The induced graph \(G[S]\) is regular. A simple regular graph on two or three vertices is **empty or complete**.

- If empty, all S vertices have identical complete neighbourhoods (their external neighbours agree), contradicting twin-freeness.
- If complete, the only *missing* ordered pairs inside S are diagonals. Since \(A(u,u)=A(\alpha u,\beta u)=0\) for every u∈S, necessarily \(\alpha(u)=\beta(u)\) throughout S. Both fix the complement, so \(\alpha=\beta\), contrary to unexpectedness.

Thus **no non-diagonal TF pair with s≤3 exists in any twin-free graph**. This replaces a prior finite exhaustive permutation check with an unrestricted elementary proof.

## 2. All twin-free four-support two-orbit cases are the authors' exact gadget

Suppose s=4 and t=2. Then the orbits are two disjoint pairs \(P=\{a_1,a_2\}\), \(Q=\{b_1,b_2\}\). On P,Q each of \(\alpha,\beta\) acts either as identity or the swap. Denote their four bits by
\(\alpha=(p,q)\), \(\beta=(r,s)\), with p,r for P and q,s for Q. Transitivity of the two separate group orbits means \(p\lor r=q\lor s=1\).

If either **entire** permutation is identity, its nontrivial counterpart makes two adjacency rows equal under the TF equation, contradicting twin-freeness. Otherwise consider the 2×2 cross-adjacency matrix \(C_{ij}=A(a_i,b_j)\). Symmetry and TF imply invariance of this matrix under both index translations \((p,s)\) and \((r,q)\) over \(\mathbb F_2^2\).

If p=r=1, then either q=s=1 (the diagonal pair \(\alpha=\beta\), excluded) or q≠s. In the latter case the translations \((1,s)\) and \((1,q)\) generate all of \(\mathbb F_2^2\), so **all four cross entries coincide**. Because exactly one of \(\alpha,\beta\) swaps Q, its internal edge is forbidden by applying TF to a diagonal. As the two Q vertices have identical neighbours outside S and the same cross-neighbours, they are twins. The case q=s=1 and p≠r is symmetric.

In the remaining case p≠r and q≠s. Since neither full permutation is identity, **one swaps P only and the other swaps Q only**, up to exchanging \(\alpha,\beta\). Hence the original TF equation reduces exactly to the prior four-vertex normal form:

- no edges within P or Q;
- both vertices in P attach to the same arbitrary subset A of the outside graph, likewise Q to B;
- the cross matrix is \(\begin{smallmatrix}x&y\\y&x\end{smallmatrix}\).
- twin-freeness **forces x≠y**, so the cross edges form **one of two perfect matchings**.

This completely identifies the only possible leading four-support pattern, directly from TF definitions and twin-freeness. The remaining s=4,t=1 cases lose at least 3(n−4) external edge bits and cannot contribute at the leading exponential scale.

## 3. Stronger functional-graph entropy lemma

**Lemma.** Let \(X_e\in\{0,1\}\) be Boolean variables indexed by unordered graph edges. Consider q *nontrivial* constraints

\[
X_e=X_{f(e)}\quad\text{or}\quad X_e=0
\]

whose q **source variables e are distinct**, and where \(f(e)\ne e\). Then these constraints eliminate at least **q/2 independent Boolean degrees of freedom**, regardless of how often a variable appears as a target.

*Proof.* Direct each constraint from its source variable to its target variable, adding a single distinguished zero sink for constant equations. Every ordinary variable has **outdegree≤1**. Each weak connected component of this finite functional directed graph has either (i) a directed path/tree into an unconstrained sink or into the zero sink, or (ii) exactly one directed cycle with trees entering it. In case (i), **all** its q_C equations are independent (after possibly grounding the sink). In case (ii), the cycle of length at least 2 has precisely one redundant equality, so the rank is q_C−1≥q_C/2. Summing components yields rank≥q/2. Distinct sources and deletion of self-equalities are essential; no unwarranted variable-disjointness assumption is made. ∎

Apply this directly to the original graph TF equations. Let \(a=|\operatorname{supp}(\alpha)|\). Order vertices so the a moved vertices of \(\alpha\) come first. Take the source variable \(\{u,v\}\) with u moved and u appearing before v, which yields exactly

\[
M(a)=a(n-a)+\binom a2
\]

**distinct source edge bits**. The corresponding target is \(\{\alpha(u),\beta(v)\}\), or zero if the two target endpoints coincide. Since u is moved, an equality is tautological only when \(\alpha(u)=v,\ \beta(v)=u\), at most once per moved u, hence at most a times. Therefore q≥M(a)−a, and the functional-graph lemma gives

\[
\Delta(\alpha,\beta)\ \ge\frac{M(a)-a}{2}
\ \ge\frac{a(n-3)}4
\tag{F}
\]

lost free-edge bits, **for all permutations \(\alpha,\beta\)**. If union support size s>n/4, at least one of α,β moves at least n/8 vertices. Interchange them if necessary (the TF relation is symmetric for undirected graphs). Thus

\[
\boxed{\Delta(\alpha,\beta)\ge\frac{n(n-3)}{32}.}
\tag{G}
\]

The earlier proof only extracted variable-disjoint equalities and obtained \(n(n-3)/96\). This is a rigorously stronger constant, requiring no maximum-incidence estimate at all. It yields the **global dense-support upper bound**

\[
\#\{\text{labelled graphs with some TF pair of support}>n/4\}
\le (n!)^2\,2^{\binom n2-\frac{n(n-3)}{32}}.
\tag{H}
\]

**Reproducible falsification:** `audit_functional_entropy.py` builds both full ordered-pair TF constraints and the selected partial functional system **independently** with separate disjoint-set structures. It verifies (F) on all non-diagonal pairs through five vertices, plus fixed-seed samples in dimensions 6,8,10,12,16,20,30,40. Actual Python 3.13.5/Linux run: **18,862 pairs PASS**. Source SHA256 `993269f7d52145e35ea86f4f9dbc5b30d0e50d471e7da03d3619c99ece8c2b5c`, Git blob `ade00258e474c8db10aaaf4747e98476913a1614`. A tight two-cycle shows that merely halving the number of constraints is the correct worst-case argument; the all-n lemma is proved above, not inferred from samples.

## 4. Effective labelled remainder bound, explicit n≥1024

Let \(E=\binom n2\), \(m=n-4\), \(K=3\binom n4\) and \(M=2^{E-2n+3}\). Each of the K unordered disjoint-transposition support partitions admits exactly M **labelled** configurations having a twin-free cross matching, before connectedness/old-base constraints. By the authors' Construction 5.1 / Proposition 5.2, every such configuration with a connected, nonbipartite, twin-free old m-vertex base and nonempty A,B is a qualifying nontrivially unstable n-vertex graph.

The exact Bernoulli union bound from the preceding lower-bound note implies that the proportion of these K*M occurrences not guaranteed to qualify is at most

\[
\varepsilon_n\le B(m)+2^{1-m}
\le(16n^2+48)2^{-n}, \tag{I}
\]

where \(B(m)=m2^{-(m-1)}+2^{4-m}+\binom m2\,2^{-(m-1)}+
2^{m+\lfloor m^2/4\rfloor-\binom m2}\).
The last term is ≤2^{-m} for m≥12; the others give the displayed elementary bound.

**Double-counting of minimal patterns.** Two **distinct** partitions each into two two-element pairs have union support S of size 4≤s≤8. If s=4 but the partitions differ, the four swaps generate a **transitive** group action; otherwise every orbit in S has at least 2 elements, so their joint orbit count t satisfies s−t≥3 in all cases. Consequently all old vertices outside S lose at least 3(n−s)≥3(n−8) independent incident bits. The relative overcount is at most

\[
R_{\mathrm{overlap}}
\le K\,2^{-n+21}.
\tag{J}
\]

The original disjoint-pattern proof already established this; the present note isolates it for the explicit error bound.

**Other four-support pairs.** All s=4,t=2 noncanonical cases have forbidden twins by §2, and s=4,t=1 has external-bit deficit 3(n−4). Their relative contribution is at most

\[
R_4\le192\,2^{-n+9}.\tag{K}
\]

**Sparse other pairs.** For 5≤s≤⌊n/4⌋, the joint \(\langle\alpha,\beta\rangle\)-orbit number is at most ⌊s/2⌋. At least \(\lceil s/2\rceil(n-s)\) outside-edge bits are lost; at most \(\binom ns(s!)^2\le n^{2s}\) TF pairs have union support s. Thus

\[
R_{\mathrm{sparse}}\le\frac1K\sum_{s=5}^{\lfloor n/4\rfloor}
n^{2s}2^{-\lceil s/2\rceil(n-s)+2n-3}.
\tag{L}
\]

**Dense pairs.** The new inequality (G) gives

\[
R_{\mathrm{dense}}\le\frac{(n!)^2}{K}\,
2^{-n(n-3)/32+2n-3}.\tag{M}
\]

Combining the upper and lower labelled counts (K*M is an upper bound for graphs with a minimal pattern, K*M(1−ε) minus pattern overlaps is a lower bound) yields the **finite-n rigorous expression**

\[
\left|\frac{L_n}{KM}-1\right|
\le\varepsilon_n+R_{\mathrm{overlap}}+
R_4+R_{\mathrm{sparse}}+R_{\mathrm{dense}}.
\tag{N}
\]

No sampling inference is involved.

For clarity, here is a **complete explicit analytic domination** for n≥1024:

- \(n^{100}\le2^n\) follows from the exact case n=1024 and the fact \(2>(1+1/n)^{100}\) for n≥1024. Hence \(\log_2 n\le n/100\).
- Using this bound in (I),(J),(K), and \(K\le n^4\), each of \(\varepsilon_n,R_{\mathrm{overlap}},R_4\) is ≤\(2^{-n/2}\).
- For s=5,6 in (L), each has \(\lceil s/2\rceil=3\), and their sum is at most \(2^{12\log_2 n-n+16}\le2^{-3n/4}\).
- For s≥7, using n−s≥3n/4, their whole sum is ≤\(n\,2^{-(97/200)n}\le2^{-19n/40}\).
- Since \((n!)^2\le n^{2n}\) and \(K\ge1\), (M) is ≤
  \(2^{-9n^2/800+(67/32)n}\le2^{-n^2/110}\le2^{-n/2}\).
  The middle inequality follows from \((19/8800)n\ge67/32\), true for every integer n≥1024.
- Add the **six** bounded terms: \(4\cdot2^{-n/2}+2^{-3n/4}+2^{-19n/40}\le6\,2^{-19n/40}\le2^{-9n/20}\), since \(6\le2^{n/40}\) when n≥1024.

This proves the effective bound (E) in full, assuming only the independently proved local TF classification, the functional-constraint lemma, and the published source construction. **The threshold 1024 is conservative**, chosen for elementary integer inequalities, not fitted to finite enumeration. It is explicitly a **labelled** estimate; no equally effective unlabelled error bound is being claimed.

**Independent arithmetic audit:** `audit_quantitative_threshold.py` uses exact integer powers and `Fraction` checks at 180 parameter values n≥1024, plus exact leading-power identities. Actual CPython 3.13.5 Linux run: PASS, with SHA256 `222d5f7b5c2d66cc616a3481ab91ad71ac4f9ad168a5c83976422eb690e4f4a1`, Git blob `7ad0c053153d12da3e95b16905f91943fe67c4b5`. Finite arithmetic sampling checks for coding errors only; every inequality for **all** n≥1024 is justified symbolically above.

## 5. What ROOT must independently check

1. The fixed-support four-vertex classification §2 includes the **twin-free** hypothesis at its only essential point; raw entropy alone fails for some nonminimal patterns, as C's earlier test showed.
2. In §3, distinguish **distinct source edge bits** from distinct target bits; outdegree≤1 makes the functional equalities almost independent. Zero targets must be handled with a unique fixed sink. A directed two-cycle contributes exactly one redundant equality, not zero.
3. The bound (F) holds even when β overlaps α, when αu=βv, and when nontrivial TF equations force other variables to zero.
4. Count unordered partitions K=3 binom(n,4), not the ordered pair twice; the overlap correction (J) covers different partitions sharing all four vertices.
5. Check exact (N) lower/upper decomposition before interpreting relative errors. Equations (H) and (M) are **labelled** bounds and must not be mistaken for unlabelled counts.
6. The source 2024 construction is prior work, and **historical novelty is not established** for either the global asymptotic or this quantitative refinement. No universal Lean compilation or independent reviewer approval is claimed in this packet.

**Deliverable classification:** self-contained written proof refinement with an effective labelled asymptotic remainder and two independently executed exact checkers; ROOT review pending. No modification of C's earlier frozen theorem, main or other workstreams; no PR, merge, new 007/008, author contact, external submission, or priority claim.
