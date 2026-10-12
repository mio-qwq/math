# Independent mathematical review of the frozen odd claw classification

## Finding

The all-odd-parameter statement in C-audit's frozen
CG_ODD_COMPLETE_THEOREM.md is supported by a complete written proof.
The proof was reconstructed from Mizzi's original definition before that
candidate was read. The independent reconstruction and the subsequent
comparison agree on the full automorphism group, the exhaustive strong
involution list, the conjugacy classes, and the number of finite simple
bases. No counterexample or conclusion-changing gap was found.

The exact scope is every odd integer \(n\geq3\); there are precisely three
ordinary base isomorphism classes, including \(\operatorname{CG}(n)\), and
therefore precisely two TF-cousins. The \(n=1\) exception is outside the
argument. This finding is a mathematical review by a separate AI agent
that did not participate in discovery. It is not human peer review, a
Lean theorem, a publication decision, or a certificate of historical priority.

## 1. Exact object binding and historical scope

The following source identities were recomputed from Git object bytes in
this review, rather than copied from a status receipt.

| Source | Commit | Bytes | SHA256 |
|---|---|---:|---|
| C-audit, CG_ODD_COMPLETE_THEOREM.md | 9ad1f91d953060d01a504481eb857daf57758ab0 | 12769 | 9544fbd1529f2815660d6f4b5ef5f52b6f114ef7682e0fa60997801c4a1255d8 |
| C-audit, CG3_EXACT_CLASSIFICATION.md | 9ad1f91d953060d01a504481eb857daf57758ab0 | 8564 | ef5783e3810ee8824e96bdedc493a58d7ab1d3106675ca0e0170fbd593e85d31 |
| C, claw_graph_exact_cousin_count.md | 979598c300580b18b603b51ded9ccdf59f470faa | 17956 | d4c6463e5bc4066c1dcd4fb9c4d3a2fab7d9621d5c2fda91bfcf58eaf6c990bd |

The first file's Git blob is 3872429a687aa2401e9acc5eaf914f2f63cce079.
Its available path history has one content introduction, commit
1aa05de8804fbd5c1b4ecdba629d18022ad718e9. The bytes at that introduction
and at the reviewed freeze have the same 12769-byte length and the same
9544fbd... SHA256. An inconsistent historical digest does not bind this
version and has not been used as evidence that it was previously reviewed.
No unobserved intermediate version is inferred from that discrepancy.

The C-audit finite \(n=3\) file is a separate finite certificate. Its
historical scope does not restrict the later all-parameter proof, and its
reported finite runs were not treated as current runs.
The original C proof uses eight-cycle counts instead of the six-cycle
edge invariant. It reaches the same coordinate model and group
classification. Neither of these historical source files was modified.

The independently reconstructed proof was frozen before comparison:

    INDEPENDENT_RECONSTRUCTION.md
    SHA256 9d1133c9413b228b905189f0d5025d9027ed812ee34d338ce7f372ef3cf6c1e7

That file has remained byte-for-byte unchanged during this comparison.

## 2. Original source and what was checked

The original definition, switching definition, folding theorem and question
were read in Russell Mizzi, arXiv:2603.27559v3, dated 10 September 2026:

<https://arxiv.org/html/2603.27559v3>

The relevant locations are Definition 1.1, Definition 6.1, Theorem 4.6,
Remarks 4.7–4.8 and Section 7. The counting question is unnumbered and
separate from the two cycle conjectures in Section 7. It counts all ordinary
isomorphism classes of finite simple \(H\) with the specified CDC, excluding
the original graph when counting cousins.

The published companion is supplied by Proposition 6.1. Section 7 credits
the additional reflection fold to V. Rozhoň and R. Šámal using Bolzano.
The proposed additional mathematical content is the all-parameter upper
bound and complete classification. An overlap search of the Bolzano
paper and subsequent sources is a separate contribution-assessment task;
this review does not certify that an equivalent classification was absent
from all prior literature.

## 3. Comparison by proof obligation

| Obligation | Frozen candidate | Independent finding |
|---|---|---|
| Correct original graph | All ring edges, both antipodal leaf attachments, and all centre–leaf edges are listed. | Matches Definition 6.1 exactly. The checker begins with the original \(u_t,c_i,\ell_{i,j}\) names and only then constructs the CDC. |
| Cover coordinates and oddness | Two ring cycles are distinguished by \(t+\varepsilon\) parity. | An explicit bijection yields two synchronized \(6n\)-cycles with leaves \(A_t\) and centres indexed modulo \(2n\). Oddness is needed both for opposite-cycle leaf neighbours and for the centre/layer coordinate bijection. |
| Six-cycle invariant | Hexagonal-edge incidences are \(3,2,0\) on rings, leaves, centres. | All six-cycles are the adjacent-index rectangles of the synchronized model. Centres lie on none; their neighbours are exactly leaves. The two formulations recover the same intrinsic types. |
| Complete group upper bound | One selected ring cycle's image determines everything. | Fully justified: unique leaf neighbour determines every leaf; that leaf's other ring neighbour determines the other circle; its unique centre neighbour determines each centre. This injects the automorphism group into \(4(6n)\) cycle-image choices. |
| Group lower bound | Lift the source dihedral symmetries and multiply by deck flip. | Direct edge substitution gives all \(24n\) maps, matching the upper bound. The alternate generators produce the same \(D_{6n}\times C_2\). |
| All involutions, not a selected family | Every layer swap is deck times a source dihedral symmetry. | The complete group calculation makes this exhaustive. Rotational involutions and all reflections are covered, with no additional cosets. |
| Adjacent-image exclusion | Odd source reflection parameters produce loops; even parameters do not. | The congruence \(2i=t\mp1\pmod{6n}\) proves exactly that parity split. In synchronized coordinates the admissible reflection parameter is odd because the deck includes a half-turn. |
| Full conjugacy | Two central singleton classes and one reflection class. | Conjugating by a rotation changes a reflection parameter by \(2a\), which is transitive on the relevant parity class. Sizes are \(1,1,3n\). |
| All finite simple bases | Invoke the established folding/conjugacy theorem. | The hypotheses and both directions are supplied explicitly below and in the independent reconstruction. Connectedness and non-bipartiteness of every potential base follow automatically from the connected cover. |
| Base group orders | Quotient the centralizer by the involution. | The quotient has kernel of size two. This gives \(12n,12n,4\), also reproduced by direct base-automorphism searches in the finite checks. |

### The centre exclusion has no hidden second-centre route

In the candidate's six-cycle argument, remove a centre from a purported
simple six-cycle. The resulting path has four edges and joins two of that
centre's distinct leaf neighbours. Each endpoint leaf has exactly one
centre neighbour, namely the centre just removed. Consequently the first
and last internal vertices on this path must be ring vertices. The sole
middle internal vertex cannot be a centre, since a centre has no ring
neighbour. These facts exclude both a return to the removed centre and a
route through another centre.

In the original coordinates the two ring positions differ by one of
\(n,2n,4n,5n\) modulo \(6n\), whereas a two-step path between ring vertices
requires difference \(0,\pm2\), or \(3n\). None is possible for \(n\geq3\).
In the synchronized coordinates the endpoint leaves differ by \(2n\) or
\(4n\), and the middle-vertex analysis instead allows only \(0,\pm2\).
Both are complete versions of the same obstruction.

At \(n=1\), the explicitly displayed cycle
\(Z_0,A_0,X_0,X_1,X_2,A_2,Z_0\) defeats this type-recovery mechanism.
The independent checker also finds centre six-cycle incidence greater
than zero there and the larger Desargues automorphism group.

### Reflection parity is a change of coordinates, not a discrepancy

Let \(k=3n\), and let \(r,f,\tau\) have the meaning in the independent
reconstruction. The original deck is \(\delta=r^k\tau\). In the candidate's
original-coordinate notation, the relevant guides translate as

| Original-coordinate guide | Synchronized-coordinate guide |
|---|---|
| \(\delta\) | \(r^k\tau\) |
| \(\delta\widetilde{\rho}_k\) | \(r^k\) |
| \(\delta\widetilde{\mu}_{2j}\) | \(r^{k+2j}f\tau\) |

Because \(k\) is odd, \(k+2j\) runs through all odd exponents. Thus the
candidate's even-axis reflections and the independent proof's odd
exponents are exactly the same involutions.

## 4. Hypotheses for folding and the centralizer formula

The connected cover is bipartite, so its bipartition is unique up to
reversal. If a finite simple \(H\) has this cover, then \(H\) is connected:
different components cannot become joined by taking a CDC. It is
non-bipartite: the CDC of a connected bipartite graph is the disjoint union
of two copies of that graph.

The cover is vertex-determining. Different recovered types have different
neighbourhood-type profiles. Within the ring type, equal neighbourhoods
force the same unique leaf neighbour and hence the same index, while the
two ring vertices at that index have disjoint ring-neighbour sets. Leaves
are determined by their ring neighbours. Distinct centres have disjoint
triples of leaf neighbours. Twins in any base would give twins in a fixed
layer of its CDC, so all possible bases are vertex-determining as well.

Every strong switching involution is fixed-point-free, since it reverses
parts. Its orbits each contain one vertex of each colour. The quotient
has no loop by the adjacent-image test and its CDC is the original graph
under \(v\mapsto([v],\chi(v))\). The two members of an orbit cannot both
be neighbours of one vertex, because they lie in opposite parts; thus
there is no hidden multiple-edge collapse when passing to a simple base.
Conversely, transporting a simple base's deck map yields such an
involution. Isomorphisms between the quotients lift to cover isomorphisms
conjugating the involutions, establishing the converse direction of the
base/class correspondence.

A cover automorphism centralizing a guide descends to its quotient;
every quotient automorphism has its canonical lift. A quotient-trivial
cover automorphism preserves or reverses the unique bipartition. In the
first case it fixes every vertex; in the second it agrees with the guide
on every vertex. The kernel is therefore precisely \(\{1,g\}\), proving
\[
\operatorname{Aut}(Q_g)\cong C_{\operatorname{Aut}(B_n)}(g)/\langle g\rangle.
\]

These additions make the source hypotheses explicit. They do not alter
the frozen candidate's conclusion or require a new restriction on \(H\).

## 5. Actual independent finite execution

The new check_original_definition.py uses only the Python standard library.
It imports none of the historical discovery or checking programs.
It does not supply the proposed \(24n\) permutations to its search.
Instead, paired colour refinement and individualization enumerate every
automorphism of the literal CDC. At each branch a chosen vertex must map
into the corresponding target colour cell, and all members of that cell
are tried. Every discrete leaf is checked on complete adjacency lists.
Natural exhaustion is recorded, with no timeout or enumeration cap.

The code then finds every strong swapping involution, computes conjugacy
under the complete group, folds class representatives, verifies each
fold's entire CDC adjacency, enumerates each base's full automorphism
group, and exhaustively rules out pairwise isomorphisms of distinct folds.

Executed command on CPython 3.12.14, Linux:

    python check_original_definition.py 1 3 5 7

Actual stdout:

    n=1: Aut=240 strong=11 classes=[1, 10] base_Aut=[120, 12] C6=20 seconds=0.088974
    n=3: Aut=72 strong=11 classes=[1, 9, 1] base_Aut=[36, 4, 36] C6=18 seconds=0.180508
    n=5: Aut=120 strong=17 classes=[1, 15, 1] base_Aut=[60, 4, 60] C6=30 seconds=0.748128
    n=7: Aut=168 strong=23 classes=[1, 21, 1] base_Aut=[84, 4, 84] C6=42 seconds=1.979221

The three \(n=3\) deliberate failures were all rejected: removing an
original ring edge, swapping two images in the proposed coordinate map,
and attempting to fold an actual layer-reversing involution with an
adjacent image. The last failure is an automorphism and an involution;
it fails specifically because its quotient would have a loop.

| Execution artifact | SHA256 |
|---|---|
| check_original_definition.py | 5eee16b8d3ecd40d0319c8ff4c5bbc2c8758869d87db8a0e2798f8e9cc12277e |
| check_results.json | e6ba1f56e8d331172e2510ba737facc97f57ea54fe3d129d371b296bf412212d |

The JSON includes Python/platform metadata, the script hash, graph
adjacency hashes, search-node counts, natural-completion flags, class
representatives, base group orders, base triangle counts, complete
non-isomorphism checks, and negative-control results. This execution
provides finite regression evidence only. The all-parameter conclusion
rests on the structural proof.

## 6. Boundaries of this review

No historical checker was rerun and no old run was relabelled as current.
No Lean theorem or compilation was produced by this review. The original
\(n=3\) historical cycle-nine certificate was read as supporting history;
the new computation used a different complete isomorphism algorithm.
No claim about even \(n\), other claw degrees, arbitrary TF-cousin pairs,
or the two separate cycle conjectures follows from this classification.

The mathematical all-odd classification is suitable for acceptance as a
written result with the hypotheses and literature attribution above.
Independent literature assessment and any formalization have their own
scope and must be reported separately.
