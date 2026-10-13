# Hidden-set advice and repeated ROB gadgets: focused review

Literature role D. Retrieval: 2026-10-13 UTC / 2026-10-14 Asia/Singapore.
This is a finite follow-up to `NARROW_ONLINE_NOVELTY.md`, not a claim of
exhaustive historical coverage.

## Exact target and source snapshot

Read `subagents/theory/ONE_EXTRA_ENTRY_FAMILY.md`, including Theorem 3,
in the main worktree at `d0928e6f543d1cbfe59be060f3028f668ecc3902`.
For integers

`W>=2, 1<=m<=W-1, W<B<=2W-m, d>=1, W-m<=dm`,

the family has `N=B+m` instructions, first `B` roots, and a hidden
`(W-m)`-subset `A` of `{m+1,...,B}`. The suffix consists of `m` jobs
whose disjoint predecessor sets partition `A`, each of size at most `d`.
There are `M=binomial(B-m,W-m)` members. Every member has optimum two
and the unique successful first action `{1,...,m} union A`.
The exact randomized family ratio is `3/2-1/(2M)`; exactly
`ceil(log2 M)` initial fixed-length advice bits permit deterministic
optimality on every member. These are family equalities and global lower
bounds, not matching global upper bounds at arbitrary resources.

The family source explicitly records independent review, no Lean claim,
and **NOVELTY_UNCONFIRMED**. This audit concerns prior art, not a replay
of that verification. Its inspected SHA-256 is
`742567125c453fe317063a71692ff38ead1868d9a94d1dd91ac96022670d895e`.

Also read the then-uncommitted `REPEATED_GADGETS.md`, SHA-256
`8f34a14d72f6b3bab3d4098f17651dc0488896b90113af2ef502864b9f2c3341`.
It was a written proof awaiting the saved independent review at inspection.
Later review records, rather than this snapshot, determine its final status.

## What the information calculation adds

Once the scheduling construction and its unique-action property are proved,
the family is the elementary game of guessing one hidden symbol from an
alphabet of size `M`. A canonical guess has cost two if correct and three
otherwise. Noncanonical first actions cannot improve the success event.
Uniform guessing gives success `1/M` on every input; averaging gives the
matching lower bound. Zero-error advice requires one distinct message per
hidden symbol. Thus both numerical formulas are classical information
counting after the R1 embedding; neither is a new minimax or advice method.

The possible contribution is the **embedding**: in-order retirement forces
the prefix part of the first action, while hidden dependencies force its
remaining part. The issue limit makes their union unique. All suffix jobs
then fit in one cycle, and every incorrect canonical guess costs exactly
one additional cycle. The same argument works with true depth two and
outdegree at most one, and permits the stated indegree bound.

The `B=W+1` specialization has only `M=W+1-m` hidden choices, hence
logarithmic advice in the resource size. The earlier `W=2q,B=3q,m=q`
specialization has `M=binomial(2q,q)`, hence a different information scale.
The limit approaching `3/2` along `W=2q,B=2q+1,m=q,d=1` varies the
resources with `q`; it is not a length-asymptotic assertion at one fixed
resource pair. The repeated four-job construction below addresses the
separate fixed-resource additive-constant question.

## Primary sources inspected

### 1. String guessing: a general information-theoretic framework

Hans-Joachim Böckenhauer, Juraj Hromkovič, Dennis Komm, Sacha Krug,
Jasmin Smula and Andreas Sprock, *The String Guessing Problem as a
Method to Prove Lower Bounds on the Advice Complexity*.
Inspected [ECCC TR12-162 revision 1, 4 February 2013](https://eccc.weizmann.ac.il/report/2012/162/),
[full revision](https://eccc.weizmann.ac.il/report/2012/162/revision/1/download).
The later journal version is TCS 554 (2014), 95–108;
[publisher](https://www.sciencedirect.com/science/article/pii/S0304397514004307).
The theorem numbers below refer to the inspected ECCC revision.

Definitions 2–3 separate known and unknown feedback histories. Section 2.1
views `b` advice bits as a choice among `2^b` deterministic outputs and
uses covering-code counting, equation (1); Theorems 1–2 give stronger
error/advice trade-offs. The zero-error, one-symbol case with alphabet
size `M` already gives the information requirement here. Definition 5 and
Lemma 5 explicitly relate consecutive guessing instances to one longer
instance. This covers the generic counting and composition ideas, not
the ROB legality or two-cycle embedding.

### 2. A scheduling proof with the same common-prefix counting method

Marc P. Renault, Adi Rosén and Rob van Stee, *Online Algorithms with
Advice for Bin Packing and Scheduling Problems*,
[arXiv:1311.7589v2, 5 August 2015](https://arxiv.org/pdf/1311.7589),
[journal DOI](https://doi.org/10.1016/j.tcs.2015.07.050).
This pass advances the previous abstract-only inspection: read the model
in §§2.1–2.4 and the complete scheduling lower-bound argument in §5.

Theorem 6 requires `(n-2m) log2 m` advice bits for exact optimality in
its identical-machine allocation problems. Its proof fixes a common job
prefix, associates distinct required prefix assignments with different
suffix completions, and counts advice messages. It explicitly strengthens
the algorithm by supplying all advice in advance. This is the same
distinguishability technique used by ILP1. Jobs there have different
processing lengths and are assigned irrevocably to machines; no ROB
retirement or bounded admission is present. Its theorem therefore does
not imply the exact R1 family or its degree restrictions.

### 3. Asymmetric guessing and covering designs

Joan Boyar, Lene M. Favrholdt, Christian Kudahl and Jesper W. Mikkelsen,
*Advice Complexity for a Class of Online Problems*, STACS 2015,
LIPIcs 30, 116–129.
[Publisher](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.STACS.2015.116),
[full paper](https://drops.dagstuhl.de/storage/00lipics/lipics-vol030-stacs2015/LIPIcs.STACS.2015.116/LIPIcs.STACS.2015.116.pdf).
Inspected the introduction, Definitions 2–3 and Theorem 4.

In minimum asymmetric string guessing, the output must cover all hidden
one-bits; missing one makes the output infeasible, and excess ones increase
cost. The paper relates advice trade-offs to covering designs. This is a
relevant more general source for hidden-subset advice methods. Its stated
objective differs from the ROB family's finite penalty for an incorrect
subset, and no reduction establishing identical competitive ratios was
found. In particular, the presence of binomial coefficients by itself
is no evidence of a new information-theoretic bound.

### 4. A close title with different precedence semantics

Allan Borodin, Joan Boyar, Kim S. Larsen and Denis Pankratov,
*Advice Complexity of Priority Algorithms*, 2018 preprint, later
Theory of Computing Systems 64 (2020), 593–625.
[Primary preprint record](https://arxiv.org/abs/1806.06223),
[author manuscript inspected](https://www.cs.toronto.edu/~bor/Papers/advice-complexity.pdf).
Read §5.2, Theorem 12, and §6.5, Theorem 18; numbering is that manuscript's.

Theorem 12 gives a gadget lower-bound template for fixed-priority
algorithms with an additive objective and indistinguishable first items
requiring different decisions. This is established general methodology.
Theorem 18's “unit-time jobs with precedence constraints” concerns a
single machine selecting a maximum compatible subset when the directed
constraints may have cycles. Each revealed item includes its incoming
and outgoing neighbors. It is not the R1 problem of executing every job
of a forward DAG under partial successor information. Neither theorem
can be applied without a model-preserving reduction.

### 5. Fully online matching on paths: relevant but incompletely accessible

Hans-Joachim Böckenhauer, Lucia Di Caro and Walter Unger, *Fully Online
Matching with Advice on General Bipartite Graphs and Paths*, LNCS 11011
(2018), 172–190.
[Publisher](https://link.springer.com/chapter/10.1007/978-3-319-98355-4_11).
Publisher model and abstract inspected; the public PDF lead at
`https://www.cs.jhu.edu/~misha/DIReadingSeminar/Papers/Bockenhauer18.pdf`
failed to open. Do not claim its full proofs were audited.

The model reveals vertices with edges to earlier vertices and requires
an irrevocable choice among newly presented matching edges. Its abstract
reports tight path bounds and advice results. This provides another
established source for hidden-future graph information, but there is no
shown equivalence to ROB admission/retirement or the hidden-set program
family. A numerical `3/2` resemblance is insufficient.

## Repeated four-job construction and additive constants

The new local note joins four-job hidden-choice blocks at fixed `B=3,W=2`.
Its separation argument combines artificial ROB predecessors with two
true predecessors on the next block's first three jobs. It aims to make
block execution costs add without adding separator jobs or cycles, while
the next hidden bit remains unobserved until the decision that matters.

Product distributions, conditional expectation, and direct-sum reasoning
are classical. The string-guessing multi-instance lemma and the priority
gadget template above are useful citations for that methodology; their
theorems do not automatically certify this scheduling construction.
Ordinary makespan is not additive under disjoint union, so the R1
separation lemma is an essential extra obligation. Earlier visibility of
blocked next-block roots must also be checked against hidden-bit leakage.

If the stated separation and indistinguishability proofs pass independent
review, `T*=2q` and `E[T]>=5q/2` fill the additive-constant gap identified
in the preceding review. Then `c>=5/4` follows even in guarantees
`E[T]<=c T*+alpha` with fixed finite `alpha`; the deterministic repeated
construction similarly gives `c>=3/2`. This is no longer merely a
four-job strict-instance lower bound. Its two-input, separator-free
ordered-window implementation remains **NOVELTY_UNCONFIRMED**.

## Conclusion and bounded search record

The advice/minimax arithmetic is covered by classical guessing and
common-prefix methods. This pass did not locate an identical or directly
subsuming theorem for the R1 hidden-set embedding, its `B=W+1` disjoint-edge
specialization, or the exact no-extra-cycle two-input concatenation.
That absence is a search limitation, not a priority certificate.

Both search engines were used. Representative exact queries:

```text
online precedence scheduling advice complexity hidden successor
online scheduling bounded buffer precedence advice complexity
online matching advice complexity binomial subsets lower bound
"advice complexity" "binomial" scheduling
"string guessing" "advice complexity" Böckenhauer pdf
"online" "precedence" "advice" "buffer"
"Fully Online Matching with Advice on General Bipartite Graphs and Paths"
"ordered" "precedence" "online" "window" scheduling
"precedence" "bounded lookahead" scheduling
"reordering buffer" "precedence constraints" "advice"
"bounded window" "scheduling" "competitive"
```

No Lean compilation or new universal mathematical verification was
performed by this literature role during this pass. Previously inspected
hidden-successor scheduling sources remain relevant; their model
differences are already recorded in `LITERATURE_REVIEW.md` §§L12–L17.
