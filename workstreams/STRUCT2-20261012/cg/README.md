# Exact TF-cousin count for odd claw graphs

## Theorem

Let \(\operatorname{CG}(n)\) be Mizzi's Definition 6.1 in
[arXiv:2603.27559v3](https://arxiv.org/html/2603.27559v3#S6).
For every odd integer \(n\ge3\),

\[
\operatorname{Aut}(\operatorname{CDC}(\operatorname{CG}(n)))
 \cong D_{6n}\times C_2,\qquad
\left|\operatorname{Aut}(\operatorname{CDC}(\operatorname{CG}(n)))\right|=24n,
\]

where \(D_{6n}\) is the dihedral group of a \(6n\)-gon, of order \(12n\).
The strongly switching involutions number \(3n+2\), with conjugacy class
sizes \(1,1,3n\). Their three folds have automorphism-group orders
\(12n,12n,4\).

Consequently exactly three ordinary isomorphism classes of finite simple
graphs \(H\) satisfy

\[
\operatorname{CDC}(H)\cong\operatorname{CDC}(\operatorname{CG}(n)).
\]

One is the original graph, so there are exactly **two TF-cousins**.
The cover is connected, forcing every such \(H\) to be connected and
non-bipartite. The quantifier over all finite simple \(H\) is therefore
fully covered. The \(n=1\) Petersen/Desargues exception is excluded.

## Proof mechanism and source

The [independent reconstruction](independent/INDEPENDENT_RECONSTRUCTION.md)
is a self-contained proof from the original edges. In synchronized cover
coordinates, six-cycles identify the centres, their leaf neighbours, and
the two remaining ring cycles. The image of one ring determines every
leaf, the other ring, and every centre. This gives the full automorphism
group upper bound. Classifying all part-reversing involutions and
excluding adjacent images then gives the complete fold list.

The [frozen-source review](independent/COMPARISON.md) compares that
reconstruction against C-audit's all-odd candidate at commit
`9ad1f91d953060d01a504481eb857daf57758ab0`. The reviewed candidate's
actual SHA256 is
`9544fbd1529f2815660d6f4b5ef5f52b6f114ef7682e0fa60997801c4a1255d8`.
No conclusion-changing gap was found. This is independent mathematical
review by a separate AI agent, not human peer review or main-branch
acceptance.

Mizzi's [Section 7](https://arxiv.org/html/2603.27559v3#S7) already credits
V. Rozhoň and R. Šámal, using Bolzano, with a reflection fold giving the
second cousin. Proposition 6.1 supplies the other known companion.
The contribution assessed here is the universal upper bound and full
classification, not the discovery of those companions. The existing
Pacco--Scapellato folding/conjugacy theory also retains its attribution.
The [prior-art report](literature/PRIOR_ART_2026-10-12.md) records the
Mizzi versions, both available Bolzano paper versions, public source
repository and later-work searches. It does not certify firstness.

## Actual original-definition regression

The standard-library
[checker](independent/check_original_definition.py) starts with the literal
Definition 6.1 adjacency and then forms its canonical double cover.
Paired colour refinement and exhaustive individualization compute the
entire automorphism group without inserting the expected group. It
enumerates all strongly switching involutions, conjugacy classes, folds,
and each base's entire automorphism group. It verifies complete cover
adjacency recovery and pairwise nonisomorphism.

Actual command:

```sh
python workstreams/STRUCT2-20261012/cg/independent/check_original_definition.py 1 3 5 7
```

| \(n\) | Cover automorphisms | Strong involutions | Class sizes, unordered | Base automorphism orders, unordered |
|---:|---:|---:|---|---|
| 1 | 240 | 11 | 1, 10 | 120, 12 |
| 3 | 72 | 11 | 1, 1, 9 | 36, 36, 4 |
| 5 | 120 | 17 | 1, 1, 15 | 60, 60, 4 |
| 7 | 168 | 23 | 1, 1, 21 | 84, 84, 4 |

[Run data](independent/check_results.json) records natural search completion,
Python/platform metadata, adjacency hashes and all fold checks. Removing
an original ring edge, corrupting the coordinate bijection, and using a
loop-producing fold were each detected. The \(n=1\) row demonstrates the
exception; it is not an instance of the all-odd theorem.

The all-parameter conclusion rests on the structural proof. These finite
computations and any finite Lean statements have their own narrower scope.
