# Window-excess hardness: independent review and prior-art boundary

Reviewer: ILP1 literature subagent D. Date: 2026-10-13 UTC.
Scope: a finite targeted audit of the new three-cycle balanced-biclique
reduction, not a claim of exhaustive coverage.

## Verdict

The supplied construction correctly reduces balanced k-Biclique to R1
three-cycle feasibility while setting c=B-W=k. Its extra supplied-order
property is real: all artificial ROB edges already occur among the true
precedences. Together with the explicitly imported biclique hardness theorem,
this establishes the claimed conditional W[1]-hardness for arbitrary fan-in.
It does not establish hardness for two-input instructions.

The scheduling/biclique equivalence, its three-cycle target, height-two
precedence restriction, nonedge construction, and 3-versus-4 approximation
gap all have very close prior art. Do not present any of these ingredients as
new. The honest provisional description is a **parameter-preserving R1
embedding of a known scheduling-hardness mechanism**. Historical novelty of
the exact supplied-order/c-parameter combination remains
**NOVELTY_UNCONFIRMED**.

## Primary sources actually read

### Jansen, Land, and Kaluza (2016)

Klaus Jansen, Felix Land, Maren Kaluza, *Precedence Scheduling with Unit
Execution Time is Equivalent to Parametrized Biclique*, SOFSEM 2016,
LNCS 9587, pp.329-343; first online 8 January 2016.
DOI: <https://doi.org/10.1007/978-3-662-49192-8_27>.
Publisher: <https://link.springer.com/chapter/10.1007/978-3-662-49192-8_27>.

Read: publisher abstract and its publicly exposed Appendices B and C,
including Appendix C, Lemma 1 and its proof. The main body remains
subscription-only; no main-body theorem number or parameter preservation is
asserted from an unread proof.

The abstract covers target makespan three, including precedence height at
most two, and a sub-4/3 approximation barrier. Appendix B normalizes a
k1-by-k2 bipartite instance using isolated and universal vertices to obtain
|V|-k1=k1+k2=|W|-k2 equal to the machine count. Its k1 can increase with input
size. Appendix C instead uses two job copies per vertex, nonedges as
precedences, and three layers of padding jobs to control the middle cycle.
This explicitly establishes the historical core of the new construction.
Neither accessible appendix verifies the particular R1 order with c=k.

### Bodlaender--Fellows (1995), and the precise 2016 width observation

Hans L. Bodlaender and Michael R. Fellows, *W[2]-hardness of precedence
constrained K-processor scheduling*, Operations Research Letters 18(2),
93-97 (1995), DOI <https://doi.org/10.1016/0167-6377(95)00031-9>.
Publisher abstract read:
<https://www.sciencedirect.com/science/article/pii/0167637795000319>.
The original proof was not obtained in this pass.

Rene van Bevern, Robert Bredereck, Laurent Bulteau, Christian Komusiewicz,
Nimrod Talmon, and Gerhard J. Woeginger, *Precedence-constrained scheduling
problems parameterized by partial order width*, DOOR 2016, pp.105-120.
Full author manuscript read, particularly the introduction:
<https://arxiv.org/html/1605.00901v1>.

The 2016 paper expressly observes that the 1995 unit-time reduction has
poset width w=m+1, while being W[2]-hard with parameter m. Thus hardness for
unrestricted posets near the width/machine boundary is already known even
with constant difference one. This observation is verified in the 2016
authors' primary exposition; the underlying 1995 construction has not been
independently reread here.

That statement does not contradict the R1 polynomial algorithm for c=1:
poset width at most B does not supply a program order in which every pair
at distance at least B is comparable in the prescribed direction. The
ordered restriction is additional information, not an alternative name
for width. It also prevents claiming that the present result is the first
hardness theorem for width minus machine count.

### Lin (2015; revised author manuscript 2019)

Bingkai Lin, *The Parameterized Complexity of k-Biclique*.
Author manuscript: <https://arxiv.org/abs/1406.3700v3>;
full text: <https://arxiv.org/pdf/1406.3700>.
Read Section 1.1, especially Theorem 1.1 and Corollaries 1.3 and 1.8.
The deterministic construction supports Corollary 1.3's W[1]-hardness of
balanced k-Biclique. Corollary 1.8's sharper exponent lower bound assumes
randomized ETH. Import the former for the present complexity claim; do not
silently replace the latter assumption by deterministic ETH.

### Later primary papers confirming the older reduction's continuing use

Jesper Nederlof and Celine M. F. Swennenhuis, *On the Fine-Grained
Parameterized Complexity of Partial Scheduling to Minimize the Makespan*,
IPEC 2020, Article 25, Section 1.2:
<https://drops.dagstuhl.de/opus/volltexte/2020/13328/pdf/LIPIcs-IPEC-2020-25.pdf>.
Its discussion explicitly uses the Jansen--Land--Kaluza biclique lower bound.
Its parameter is the number of jobs to select, not c; its FPT algorithm
therefore does not contradict or directly subsume this result.

Jesper Nederlof, Celine M. F. Swennenhuis, and Karol Wegrzycki,
*A Subexponential Time Algorithm for Makespan Scheduling of Unit Jobs
with Precedence Constraints*, SODA 2025, pp.535-552:
<https://research-portal.uu.nl/ws/portalfiles/portal/254249631/1.9781611978322.16.pdf>.
Read Sections 1.3, 1.4, and 9, including Theorem 9.1 and proof. It again
attributes the biclique connection to the 2016 paper, and gives a separate
three-cycle reduction from sparse Densest-k-Subgraph using padding layers.
Neither inspected passage supplies the current ordered-window parameter.

## Independent check of the actual R1 proof

Reviewed file in the primary worktree:
`workstreams/ILP1-20261014/EXCESS_HARDNESS.md`, SHA-256
`0e7f3bce538ed61791d429f45a0ca8bb415ca81adc297ffc3a7efa22c22a4940`
(read 2026-10-13T20:33:46Z). This review covers the mathematical text, not a
Lean formalization or independently rerun test suite.

For |U|=n, |V|=m and 1<=k<=min(n,m), set f=m+k, B=n+m+k,
W=n+m and N=2B. The first B jobs are f forced roots followed by U.
The next B are V-sinks followed by padding sinks. A V-sink requires all
forced roots and all its U-nonneighbors; padding requires all roots.

I checked the following possible failure points explicitly:

1. **ROB admission in the witness.** Issuing all roots except the k chosen
   U vertices retires at least f>=m initial jobs. Every represented V-sink
   is therefore admitted in cycle two, even if omitted U vertices are
   widely separated. The second batch has 2k<=W jobs. Once all roots finish,
   all remaining sinks are admitted in the third cycle.
2. **Underissuing and idle schedules.** No sink can issue first, and at
   least k sinks must issue second if completion occurs by cycle three.
   An unfinished forced root forbids every sink. Some roots must remain
   unfinished after cycle one, so padding sinks cannot be among the second
   batch. The omitted U roots and second-cycle V-sinks yield the biclique
   without any non-delay or exact-first-batch assumption.
3. **Exact optimum values.** Workload excludes two cycles. Issuing roots
   in consecutive batches W,k, then sinks W,k, is a legal four-cycle R1
   schedule. Thus YES and NO optima are exactly three and four.
4. **Artificial edges.** With zero-based indices, represented sink B+v
   has artificial predecessors i<=v<m, all forced roots. Padding sinks
   depend on every root. Neither B-job layer contains a distance-B pair.
5. **Poset width.** Both layers give width at least B. A mixed antichain
   can use only U-roots and V-sinks: forced roots and padding sinks exclude
   the opposite layer. Its size is at most n+m=W<B. Hence width is B.
6. **Parameters.** The construction is polynomial size and c=k exactly.
   For horizon three, S=3W-N=n+m-2k is nonnegative but not bounded by k.
   This is consistent with both XP(c) and FPT(c+S). The edge count and
   indegrees can be quadratic and unbounded respectively.

Status of the explicit reduction after this independent reading:
**WRITTEN_PROOF**, **INDEPENDENTLY_REVIEWED** for the statements above;
**not LEAN_VERIFIED** by this reviewer. The imported Lin theorem is not
reproved. Historical priority stays separate and unconfirmed.

## What can safely be presented

The result is useful as a matching qualitative barrier to seeking an FPT
algorithm in window excess alone, after obtaining an XP algorithm. That
scientific role survives even if the reduction is entirely a specialization
of prior work. The combination to compare against future sources is:

`unit jobs + supplied ROB order + B-W=k + height two + horizon three
 + all ROB artificial precedences redundant`.

Do not append any of these claims: a new solution to general precedence
scheduling; novelty of the complement-biclique trick; a first 3/4 hardness
gap; hardness at fixed c; an unconditional nonexistence theorem; or hardness
for fan-in two. The present finite audit neither establishes an exact
earlier theorem for the full combination nor justifies a claim that none
exists. The main body of Jansen--Land--Kaluza remains the most important
specific item to obtain through an authorized open manuscript or existing
subscription.

## Search and access log

Search date: 2026-10-13, approximately 20:28-20:35 UTC. Queries included:

- `"scheduling" "width" "machines" "biclique"`
- `"unit" "scheduling" "three" "biclique"`
- `"precedence" "width minus" machines`
- `"scheduling" "height two" "three" complexity`
- `"Precedence Scheduling with Unit Execution Time" pdf`
- `"Jansen" "Land" "Kaluza" "Biclique" filetype:pdf`
- `"Precedence Scheduling" "Biclique" "Theorem"`
- `"Maren Kaluza" site:uni-kiel.de`
- `"Biclique" site:informatik.uni-kiel.de`
- `"Bodlaender" "Fellows" "W[2]" 1995 pdf`

Both search engines were used; several engine-1 results ignored the academic
phrase and were discarded. Metadata/abstract mirrors were used only as
discovery leads. The decisive 2016 content was then obtained directly from
the publisher by opening the proceedings table of contents, page two, and
following its chapter link. Independent urllib retrieval confirmed the same
public text. A nominal PDF request returned the chapter preview HTML, not
the full PDF. No access wall was bypassed, no author contacted, and no
purchase made. No source PDF or extensive copied source text is committed.
