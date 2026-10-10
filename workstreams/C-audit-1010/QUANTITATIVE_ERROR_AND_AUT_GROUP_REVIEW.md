# Independent audit: explicit exponential-rate remainder and generic automorphism groups

**2026-10-10 · C-audit-1010 · internal independent implementation, not an uninvolved ROOT acceptance.**

This note audits `GLOBAL_NONTRIVIAL_INSTABILITY_ASYMPTOTIC.md` at frozen commit `eb6d63dea62c4559f7d9deb6cdd5796255d7e150`, in the original connected, nonbipartite, twin-free class of Hujdurović–Mitrović, *Some conditions implying stability of graphs*, *Journal of Graph Theory* 105 (2024), Problem 5.3. The four-added-vertex construction is their pre-existing Construction 5.1; this is not a priority claim.

Set \(m=n-4\), \(E_n=\binom n2\), \(F_n=2^{\binom m2+2m-1}/m!\). The earlier full manuscript gives \(U_n\sim F_n\), where \(U_n\) counts unlabeled nontrivially unstable graphs. The additional quantitatively stronger statement supported by the same combinatorial method is

\[
\boxed{U_n=F_n\bigl(1+O(2^{-n/4})\bigr)}.
\]

Consequently, since \(g_n=2^{E_n}/n!\,(1+O(n^2 2^{-n}))\),
\[
\boxed{\frac{U_n}{g_n}=\frac{2(n)_4}{4^n}\bigl(1+O(2^{-n/4})\bigr)}.
\]

The Big-O here is a genuine asymptotic upper bound, *not* a claim that the displayed approximation is accurate for n=7–10 or that a small numerical sample proves it. A coarse derivation below is valid for all sufficiently large n (one may conservatively take n≥8192 before absorbing constants).

## 1. The independent-constraint entropy argument survives a direct attack

Let \((\alpha,\beta)\) be a non-diagonal TF pair, \(S\) its union support of size \(s\), and let the generated group have \(t\) orbits on \(S\), with \(t\le\lfloor s/2\rfloor\). Since external vertices are fixed by both permutations, all vertices of one orbit have equal adjacency to every \(w\notin S\). Exactly at least \((s-t)(n-s)\) of the free edge bits are constrained.

For \(s>n/4\), one permutation (take \(\alpha\)) moves \(a\ge n/8\) vertices. Put those a vertices first in an ordering and select the \(M=a(n-a)+\binom a2\) undirected edge variables incident with them, each once. The ordered TF equation for each selected variable is nontrivial except possibly on at most a source edges \(\{u,\alpha(u)\}\): since \(\alpha(u)\ne u\), a tautology requires \(\alpha(u)=v,\beta(v)=u\). In the remaining equations each edge bit is the selected **source** at most once and the **target** at most twice (the two possible orientations under the bijections). Hence the degree of every variable in the incidence hypergraph of equalities/forced zeros is ≤3. A greedy variable-disjoint family has at least \((M-a)/6\ge n(n-3)/96\) constraints. These constraints involve disjoint fair Bernoulli graph-edge bits and each halves the assignment count. Therefore

\[
\#\{G\text{ satisfying this TF pair}\}\le2^{E_n-n(n-3)/96}.
\]

There are at most \((n!)^2\) pairs, so the entire dense-support contribution is at most \((n!)^2 2^{E_n-n(n-3)/96}\), which is \(o(F_n2^{-n/4})\) by \(\log_2 n!\le n\log_2 n\). No assumption that equations are all independent *before matching* is made.

## 2. Quantify the sparse nonminimal remainder among unlabeled graphs

For \(4\le s\le n/4\) and a fixed abstract pair of permutations on s marked vertices, choose an arbitrary **unlabeled** induced old graph on the \(n-s\) outside vertices; for each outside vertex there are ≤\(2^t\) possible adjacency signatures into the s marked vertices; and there are ≤\(2^{\binom s2}\) internal graphs. Hence the total unlabeled graphs having *any* given non-diagonal TF pair of union support s is bounded by
\[
(s!)^2 g_{n-s}2^{t(n-s)+\binom s2}.
\]

This is an **upper** bound: choosing a representative of each unlabeled outside graph and adding a marking can only overcount target isomorphism classes. The standard Burnside/random-graph estimate can be made quantitative, uniformly for \(n-s\ge3n/4\): \(g_{n-s}\le 2\,2^{\binom{n-s}2}/(n-s)!\) when n is large.

Dividing by the candidate main term \(F_n=2^{E_n-2n+1}/(n-4)!\), the ratio for one s is at most
\[
2(s!)^2\frac{(n-4)!}{(n-s)!}
    2^{\,2n-1-\lceil s/2\rceil(n-s)}.
\]

For s=5 and 6 this is \(O(n^2 2^{-n})\). For s=4 and one generated orbit (t=1), it is \(O(2^{-n})\); s=4,t=2 with twin-free graphs has ONLY the leading two disjoint swaps, as confirmed both by the original finite classification and our separately written raw ordered-pair check. For 7≤s≤n/4, use \((s!)^2 (n-4)!/(n-s)!\le n^{3s}\), \(n-s\ge3n/4\) and, for sufficiently large n, \(3\log_2n\le n/32\). The logarithm of each ratio is at most
\[
2n+3s\log_2n-(s/2)(n-s)
\le 2n-\frac{11sn}{32}\le-\frac{13n}{32}.
\]

Summing at most n such terms gives \(O(2^{-n/3})\). Thus **all** nonminimal TF support types contribute \(O(F_n 2^{-n/4})\) unlabeled graphs.

## 3. Two distinct leading patterns: not assumed disjoint

A leading minimal unordered pattern is one partition of four vertices into disjoint 2-sets, with the TF pair swapping one 2-set in alpha and the other in beta. For two distinct patterns, the union of their supports has size s≤8, and the generated group has \(s-t\ge3\); this includes the delicate case of **the same four vertices but two different pair partitions**, when the combined group is transitive. The same abstract-marking count bounds all unlabelled overlaps by
\[
\sum_{s=4}^8 O\bigl(g_{n-s}2^{t(n-s)+\binom s2}\bigr)
  =O(n^4 2^{-n}F_n)
  =O(2^{-n/4}F_n).
\]

No claim of finite exact uniqueness is involved.

## 4. Old graphs and double counting are exponentially negligible

The classical random-graph asymmetry estimate admits the quantitative form
\[
g_m=\frac{2^{\binom m2}}{m!}(1+O(m^2 2^{-m})),
\]
by Burnside: a nontrivial ordinary permutation moving s vertices forces all external adjacency bits to be constant on its nontrivial orbits, and the sparse/dense estimates above sum to \(O(m^2 2^{-m})\) uniformly. The number of *unlabeled* m-vertex graphs with any ordinary automorphism is also \(O(m^2 2^{-m}g_m)\): in Burnside's sum every symmetric isomorphism class contributes \(1-1/|\operatorname{Aut}|\ge1/2\) to the nonidentity terms, so at most twice the sum bounds the number of such classes. Connectivity, nonbipartiteness, and twin-freeness additionally fail with probability \(O(m^2 2^{-m})\) in the labelled model; the same unlabelled order bound follows by separating asymmetric versus symmetric old classes.

For a good asymmetric old graph X, the number of unordered **distinct nonempty** pairs of attachment subsets is
\[
\binom{2^m-1}{2}=2^{2m-1}(1-O(2^{-m})).
\]
One graph arises from each pair unless it has a second minimal TF pattern; the overlap bound above removes at most \(O(F_n2^{-n/4})\) cases. Conversely any graph with a unique minimal TF pattern canonically exposes X and an unordered multiset of its two attachment subsets, giving at most \(g_m\binom{2^m+1}2=(1+O(2^{-m}))g_m2^{2m-1}\) possibilities. The difference between these two bounds is within \(O(F_n2^{-n/4})\), proving the announced exponential relative remainder.

## 5. Generic exact automorphism-group corollary

Outside the same exponentially negligible exceptional set, X is asymmetric, the two attachment sets A,B are distinct, and the resulting n-vertex graph G has **exactly one** minimal TF support pattern and *no* other non-diagonal TF pair. The support blocks and old vertex set W are intrinsic. Every ordinary automorphism restricts to Aut(X)=1 on W. Since A≠B, it cannot exchange the two blocks; since the cross edges form a perfect matching, it can only fix all four added vertices or swap both added pairs simultaneously. Thus
\[
\operatorname{Aut}(G)\cong C_2.
\]
Among the color-preserving automorphisms of CDC(G), the diagonal lifts of these two ordinary automorphisms plus the two off-diagonal TF pairs (alpha,beta),(beta,alpha) form precisely a Klein four group. The global deck flip exchanges the two TF generators, so
\[
\operatorname{Aut}(\operatorname{CDC}(G))\cong (C_2\times C_2)\rtimes C_2\cong D_8,
\]
where \(D_8\) has order eight. Hence an exponentially overwhelming proportion **within the unlabeled unstable class** has exactly these two group isomorphism types. This conclusion is conditional on the complete global support bound, **not** proved by a few examples.

## 6. New adversarial checks (separate code)

The Python file `independent_support_audit.py` **independently reconstructs** edge-bit orbit equations from all ordered pairs, treats diagonal target bits as forced zero, and checks the real entropy loss against the formula. Deterministic seed 20261010: 2,798 randomly generated permutation pairs over n=6,7,8,10,12,16,20,24. Every observed exact bit loss satisfies the sparse bound; every independent-constraint greedy extraction satisfies both the degree≤3 and \(6\cdot\text{picked}\ge M-a\) inequalities. Separately all 4!² permutations and all 2^6 simple graphs on the four moving vertices are considered; the precise survivors are 6 ordered leading disjoint-swap pairs (12 valid internal graph masks) **and** 30 valid nonleading transitive cases (36 masks), which confirms that entropy-only elimination of the transitive cases would be wrong.

The file `test_generic_cover_group.py` uses a **different graph-isomorphism algorithm (NetworkX 3.6.1 VF2)** to enumerate full automorphism groups of three concrete random augmented graphs with total sizes n=12,13,14. It finds |Aut(G)|=2 and |Aut(CDC(G))|=8 in every case, with group element-order multiset [1,2,2,2,2,2,4,4] (D8), and fixed-seed reproducible edge counts and attachment subsets. This checks the claimed group correspondence, but a finite sample cannot establish the asymptotic theorem.

**Commands actually run:**

```
python3 independent_support_audit.py
python3 test_generic_cover_group.py
sha256sum independent_support_audit.py test_generic_cover_group.py
```

Environment: CPython 3.13.5, Linux, NetworkX 3.6.1 for second checker; the first uses the Python standard library only. Original source definitions rechecked on the publisher site October 10, 2026. No ROOT acceptance, signed integration, Lean compilation, formal peer review or historical originality is claimed. 

**Next audit:** independently challenge the sparse **unlabelled** marking inequality and Burnside remainder; these determine the explicit relative-error exponent. If its proof fails, keep the earlier 1+o(1) result as a separate frozen object and record the exact gap. Do not overwrite the preceding manuscript or expand unrelated finite enumerations solely for volume.