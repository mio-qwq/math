# Independent literature review: ILP1-20261014

Reviewer: literature subagent D. Search and source inspection: 2026-10-13 UTC
(2026-10-14 in UTC+08). Repository baseline:
`bf732c32f1b8cef32ebf69cac6fb232a8a5323a3`.

This is a first-pass primary-source audit, not an exhaustive survey. “Read” below
means the stated portions of the source were inspected; it does not mean that
every proof was independently verified. No external Lean/Rocq artifact was
compiled by this reviewer. See `NOVELTY_REVIEW.md` for mathematical scope and
`SEARCH_LOG.md` for reproducible queries and access limitations.

## Findings that affect the project immediately

1. Finite ROB capacity represented by precedence between retirement and later
   admission is established architecture modeling practice. The exact R1
   execution-only reduction should be presented as a specialized elimination
   theorem with a checked semantic bridge, not the invention of resource edges.
2. Two-machine unit-job precedence scheduling is classically polynomial. An R1
   reduction therefore makes two-wide offline optimal scheduling a corollary.
3. Calling the three-machine unit-job problem simply “still open” is unsafe in
   October 2026: a September 2026 preprint claims a polynomial algorithm and
   supplies a Lean artifact. The released endpoint was inspected, but this audit
   does not certify its dependency closure or theorem equivalence.
4. Online hidden-successor adversaries and advice lower bounds have substantial
   prior art. The precise ROB information model may distinguish our results;
   the adversarial method and numerical constant 3/2 alone do not.

## Primary sources and exact relevance

### L01. David W. Wall, 1991 and 1993: ILP limits

* *Limits of instruction-level parallelism*, ASPLOS IV (1991), pp. 176–188;
  [WRL TN-15](https://davidwall.info/papers/WRL-TN-15.pdf).
* Expanded report, WRL Research Report 93/6 (1993),
  [primary PDF](https://davidwall.info/papers/WRL-TR-93.6.pdf),
  [author publication page](https://davidwall.info/papers.html).
* Inspected: report §§2, 2.6, 2.7 and Appendix 1.

Wall studies trace-based ILP limits under oracle assumptions and several window
models. The continuous window counts instructions in pending execution cycles;
the implementation flushes early cycles to regain space. Unit-latency results
become usable in the next cycle. The simulation's greedy scheduling and window
semantics are not a theorem about globally optimal ROB scheduling. Cite this
work for the research lineage and for how strongly “window” definitions affect
an ILP claim; do not identify its measurements with R1's function `T*`.

### L02. Dubey, Adams and Flynn, 1994: window trade-offs

Pradeep K. Dubey, George B. Adams III, Michael J. Flynn,
*Instruction Window Size Trade-Offs and Characterization of Program Parallelism*,
IEEE Transactions on Computers 43 (1994), pp. 431–442.
[IBM primary publication record](https://research.ibm.com/publications/instruction-window-size-trade-offs-and-characterization-of-program-parallelism).

Inspected: institutional abstract only. It analyzes concurrency-detection scope,
resource limits and program parallelism. No theorem number or exact equivalence
to R1 has been verified. It is a required follow-up before claims about first
analytic window-size laws.

### L03. Fields, Rubin and Bodík, 2001: microarchitectural event DAGs

Brian A. Fields, Shai Rubin, Rastislav Bodík,
*Focusing processor policies via critical-path prediction*, ISCA 28 (2001),
pp. 74–85, [DOI](https://doi.org/10.1145/379240.379253).
[Author project page](https://homes.cs.washington.edu/~bodik/ucb/bafl/),
[author publication list](https://homes.cs.washington.edu/~bodik/papers.html).

The authors' [retrospective](https://bpb-us-w2.wpmucdn.com/sites.coecis.cornell.edu/dist/7/587/files/2023/06/Fields_2001_Focusing.pdf),
§§III–IV, explicitly explains representing hardware resource restrictions,
including finite ROB capacity, with event-level dependence graphs. It also
explains why a single node per instruction is inadequate for realistic pipelines.
The original full PDF could not be successfully retrieved here; indexed snippets
are not treated as a full-text proof inspection. The 2010 source below supplies
the directly inspected FIFO constraint.

### L04. Navada, Choudhary and Rotenberg, 2010: explicit FIFO/ROB edge

Sandeep Navada, Niket K. Choudhary, Eric Rotenberg,
*Criticality-driven Superscalar Design Space Exploration*, PACT 19 (2010).
[Primary PDF](https://ericrotenberg.wordpress.ncsu.edu/files/2025/06/paper_PACT-19.pdf),
[author publication record](https://sites.google.com/site/sandeepnavada/publications).
The 2025 directory date is an upload date, not the publication year.

Inspected: §§5.1–5.2, Table 2 (printed pp. 266–267).
For FIFO structure size `S`, entry of instruction `i` waits for departure of
`i-S`; the ROB example is a commit-to-entry edge `C_(i-S) → I_i`. In-order commit
edges are also explicit. The paper distinguishes this from an issue queue,
whose out-of-order removal does not admit that fixed predecessor rule. Its
critical path models represented executions; it is not a proof that an arbitrary
finite-width greedy execution is globally optimal. This is direct prior art for
R1's capacity-to-precedence modeling step.

### L05. Coffman and Graham, 1972: exactly two processors

Edward G. Coffman Jr., Ronald L. Graham,
*Optimal Scheduling for Two-Processor Systems*, Acta Informatica 1 (1972),
pp. 200–213, [DOI](https://doi.org/10.1007/BF00288685).
[Author-hosted scan](https://fanchung.ucsd.edu/ron/papers/72_04_two_processors.pdf),
[Coffman publication list](https://www.cs.columbia.edu/~coffman/publications.php).

The classical nonpreemptive unit-job, arbitrary-precedence, two-identical-machine
problem admits an optimal polynomial algorithm. Its lexicographic labeling and
scheduling rule must not be replaced by “longest remaining path first.” The scan
was retrieved but its text extraction was empty; bibliographic identity and
algorithm scope were cross-checked against L06's primary full text. No original
theorem number is claimed here. The algorithm requires the whole precedence
graph, so this is an offline result after R1's reduction.

### L06. Nederlof, Swennenhuis and Węgrzycki, 2023–2026: exact complexity

Jesper Nederlof, Céline M. F. Swennenhuis, Karol Węgrzycki,
*A Subexponential Time Algorithm for Makespan Scheduling of Unit Jobs with
Precedence Constraints*. [arXiv v1, 2023](https://arxiv.org/html/2312.03495v1),
[SODA 2025](https://doi.org/10.1137/1.9781611978322.16),
[ACM Transactions on Algorithms, online January 2026](https://doi.org/10.1145/3785365).

Inspected: arXiv full-text introduction, Theorems 1.1–1.2 and related work;
publisher metadata for later publication. Theorem 1.1 gives time
`(1+n/m)^{O(sqrt(nm))}`; Theorem 1.2 gives `O(1.997^n)` for arbitrary machine
count. The introduction records the historical unresolved complexity for three
machines, whereas variable machine count is NP-hard. These statements describe
the paper's date, not a verdict on the September 2026 claim in L07. Its survey of
special precedence classes is a useful route to original interval-order and
bounded-height papers.

### L07. OpenAI, September 24, 2026: three-machine claim under audit

*A Polynomial-Time Algorithm for Three-Machine Unit-Job Scheduling*,
[manuscript source at inspected commit](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/A-polynomial-time-algorithm-for-three-machine-unit-job-scheduling-September-24-2026/build/paper.tex).

Inspected: manuscript Theorem 1.1 and proof overview; release specification,
comparator configuration, actual Lean endpoint. The claim concerns arbitrary
finite explicit DAGs, nonpreemptive unit jobs, exactly three identical machines,
and a uniform polynomial-time algorithm with exponent 150020 in explicit binary
input length. The proof overview uses bounded-size descriptions of intervals in
a recursively organized decomposition. That structural argument has not been
independently reviewed in this workstream.

The [actual endpoint](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/lean/OAI/Computability/Scheduling/Main.lean)
contains a proof of `OAI.ThreeMachine.main_theorem`, importing `MachineBridge`.
The [comparator configuration](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/lean/ComparatorChallenges/ThreeMachine.json)
targets that declaration and permits `propext`, `Quot.sound`, `Classical.choice`.
The separate challenge's `sorry` is intentional statement scaffolding; it is not
evidence of a hole in the solution. We did not compile the dependency closure,
run comparator, or perform its axiom audit. Status: current preprint claim with
released formal artifact, not independently certified by this review.

### L08. Chardon and Moukrim, 2005: special poset classes

Marc Chardon, Aziz Moukrim,
*The Coffman–Graham Algorithm Optimally Solves UET Task Systems with Overinterval
Orders*, SIAM Journal on Discrete Mathematics 19(1), pp. 109–121.
[Publisher](https://doi.org/10.1137/S0895480101394999).

Inspected: primary publisher abstract only. It claims optimality for overinterval
orders on any machine count, extending previously treated classes. Do not apply
this to every R1 augmented DAG: adding arbitrary data edges to the base window
order can destroy interval-order structure. Recognizing a genuine preserved
subclass remains a reasonable research direction; a full theorem/definition
inspection is needed before importing this result.

### L09. van Bevern et al., 2016: width is not ROB capacity

René van Bevern, Robert Bredereck, Laurent Bulteau, Christian Komusiewicz,
Nimrod Talmon, Gerhard J. Woeginger,
*Precedence-constrained scheduling problems parameterized by partial order
width*, DOOR 2016. [Primary preprint](https://arxiv.org/pdf/1605.00901).

Inspected: abstract and introduction, especially the enumerated hardness results
and refined algorithm. Two-machine hardness here permits lengths 1 and 2;
another result permits unit jobs requiring two simultaneous machines. Neither
is the ordinary all-unit two-machine model. The paper gives an RCPSP algorithm
parameterized jointly by poset width and maximum start-time lag. R1 capacity `B`
is an ordered frontier restriction, not synonymous with arbitrary poset width.
These results neither refute nor establish a `B`-parameter algorithm.

### L10. Büsing, Draeger and Mathwieser, 2025: generalized precedences

Christina Büsing, Maurice Draeger, Corinna Mathwieser,
*Parameterized Complexity of Scheduling Unit-Time Jobs with Generalized
Precedence Constraints*, IPEC 2025, LIPIcs 358, article 7.
[Primary full text](https://drops.dagstuhl.de/storage/00lipics/lipics-vol358-ipec2025/LIPIcs.IPEC.2025.7/LIPIcs.IPEC.2025.7.pdf).

Inspected: §§1–3, Lemma 1, Theorem 2. Jobs carry positive Boolean formulas;
ordinary DAG precedence is the all-conjunction special case. Theorem 2's
parameter counts the total number of distinct jobs appearing as predecessors,
not maximum fan-in. Its bound is `O(k_p^{k_p} m n^2)` for makespan/sum of completion
times. The mixed AND/OR two-machine hardness does not contradict Coffman–Graham.
This is an important warning against importing hardness or FPT results under
incorrect instruction-graph parameter definitions.

### L11. Graham, 1966/1969: list-scheduling performance bounds

Ronald L. Graham, *Bounds for Certain Multiprocessing Anomalies*, Bell System
Technical Journal 45(9) (1966), pp. 1563–1581,
[DOI](https://doi.org/10.1002/j.1538-7305.1966.tb01709.x);
*Bounds on Multiprocessing Timing Anomalies*, SIAM Journal on Applied Mathematics
17(2) (1969), pp. 416–429, [DOI](https://doi.org/10.1137/0117039).

The standard work-conserving list-scheduling factor is `2-1/m`. Original theorem
number was not inspected here; publisher records and the subsequent primary
online literature were checked. R1's ready-set equivalence permits a classical
bound to be transferred without future knowledge. The transfer and an elementary
proof should be written explicitly rather than presented as a new ratio theorem.

### L12. Epstein, 1998/2000: online unknown precedences

Leah Epstein, *A note on on-line scheduling with precedence constraints on
identical machines*, Information Processing Letters 76(4–6) (2000), pp. 149–153,
[DOI](https://doi.org/10.1016/S0020-0190(00)00141-1),
[primary institutional abstract](https://cris.haifa.ac.il/en/publications/note-on-on-line-scheduling-with-precedence-constraints-on-identic/).
Conference predecessor: APPROX 1998, pp. 89–98;
[author publication list](https://math.haifa.ac.il/lea/papers.htm).

Inspected: institutional abstract, publication identity; full paper unavailable
through attempted publisher/author links. Jobs appear only once all predecessors
have finished. Reported lower bounds are `2-1/m` for deterministic and
`2-2/(m+1)` for randomized algorithms, even with unit jobs. The information and
admission model differs from R1: R1 reveals blocked admitted instructions and
can hide ready instructions beyond its ROB. Neither numerical coincidence nor
the shared word “online” supplies a reduction between the models.

### L13. Huo and Leung, 2005; Huo, Leung and Wang, 2008

Yumei Huo, Joseph Y. T. Leung,
*Online Scheduling of Precedence Constrained Tasks*, SIAM Journal on Computing
34(3) (2005), pp. 743–762,
[DOI](https://doi.org/10.1137/S0097539704444440),
[institutional record](https://digitalcommons.njit.edu/fac_pubs/19656/).
Yumei Huo, Joseph Y. T. Leung, Xin Wang,
*Online scheduling of equal-processing-time task systems*,
Theoretical Computer Science 401 (2008), pp. 85–95,
[DOI](https://doi.org/10.1016/j.tcs.2008.03.026),
[institutional record](https://digitalcommons.njit.edu/fac_pubs/12747/).

Inspected: primary institutional/publisher abstracts only. The 2005 model releases
tasks and precedences at external times; these are not retirement-controlled
releases. The later abstract reports list-scheduling and intree bounds. Exact theorem
assumptions require full-text retrieval before using them in an R1 comparison.

### L14. Canon et al., 2019/2020: explicit hidden-successor adversary

Louis-Claude Canon, Loris Marchal, Bertrand Simon, Frédéric Vivien,
*Online Scheduling of Task Graphs on Heterogeneous Platforms*, IEEE TPDS 31(3)
(2020), pp. 721–732, [DOI](https://doi.org/10.1109/TPDS.2019.2942909).
[Author-hosted full text](https://www.uni-bremen.de/fileadmin/user_upload/fachbereiche/fb3/infcon/CSLog/Publications/bsimon/papers/TPDS-final.pdf).

Inspected: online model and §3, Theorem 1 proof. An adversary reveals a later
phase depending on a last-completed earlier task. This is a direct methodological
antecedent for choosing an omitted visible root as a hidden suffix parent. The
paper's CPU/GPU platform, execution times and reveal-on-readiness model differ
from R1; its quantitative lower bound is not imported here.

### L15. Lassota et al., 2023: minimum future information

Alexandra Anna Lassota, Alexander Lindermayr, Nicole Megow, Jens Schlöter,
*Minimalistic Predictions to Schedule Jobs with Online Precedence Constraints*,
ICML 2023, PMLR 202, pp. 18563–18583.
[Primary record](https://proceedings.mlr.press/v202/lassota23a.html),
[full text](https://proceedings.mlr.press/v202/lassota23a/lassota23a.pdf).

Inspected: §§1–1.3, information model and introductory adversary. Indistinguishable
initial roots conceal the parent of an important successor; prediction models
then quantify useful future information. The objective is weighted completion,
processing times are unknown, preemption is allowed, and jobs appear when ready.
The exact R1 dichotomy is not obtained by substituting parameters in this paper.
Its hidden-parent example and research framing must nevertheless be acknowledged
before any originality claim about advice or future dependency information.

### L16. Advice and reordering-buffer terminology

Marc P. Renault, Adi Rosén, Rob van Stee,
*Online Algorithms with Advice for Bin Packing and Scheduling Problems*,
arXiv 2013, revised 2015;
[primary abstract](https://arxiv.org/abs/1311.7589),
[journal DOI](https://doi.org/10.1016/j.tcs.2015.07.050).
Inspected: abstract only; identical-machine allocation advice, not R1 precedences.

Anna Adamaszek, Marc P. Renault, Adi Rosén, Rob van Stee,
*Reordering Buffer Management with Advice*, WAOA 2013;
[author full text](https://mrenault.sites.cs.wisc.edu/papers/AdamaszekRenaultRosenVanSteeWAOA2013.pdf).
Inspected: abstract and §§1–2. Its buffer releases a chosen item immediately;
the cost counts color changes. The lower bound concerns advice per input item.
That buffer is not a processor ROB with completed instructions retained until
in-order retirement. The paper usefully distinguishes per-request advice from
a single advice tape; R1 must specify when bits arrive and what is counted.

### L17. Das and Sun, 2025: newer online resource scheduling

Rathish Das, Hao Sun,
*Almost Tight Approximation Hardness and Online Algorithms for Resource
Scheduling*, [arXiv 2509.01086v1](https://arxiv.org/abs/2509.01086),
[primary PDF](https://arxiv.org/pdf/2509.01086).

Inspected: introduction, model, theorem statements 3.3, 3.16, 5.1, 5.6, 6.1.
The online model reveals a job after all predecessors complete; jobs may have
different processing times and resource requirements throughout execution.
Logarithmic bounds in that general setting are not lower bounds for R1 unit
jobs with one execution slot each. This supplies current context and additional
references, not an R1 theorem.

### L18. Prosa / Rocq: verified scheduling is established

Prosa project,
[current proof-displaying EDF optimality module](https://prosa.mpi-sws.org/branches/master/with-proofs/prosa.results.optimality.edf.html).
Inspected declarations include `EDF_optimality`, `EDF_WC_optimality`,
`EDF_priority_compliant_WC_optimality`, `weak_EDF_optimality`.

The model is an ideal uniprocessor with arrivals, execution costs and absolute
deadlines, basic readiness and full preemption. Feasibility implies an EDF
schedule satisfying deadlines. This is neither ROB makespan optimality nor
an arbitrary multi-issue scheduler. Proof source was inspected, not locally
compiled. It prevents any broad claim that mechanized scheduling optimality
is new; R1's particular semantics and proof coverage must be stated separately.

## Leads not used as established results

* *Parameterized algorithms and complexity for scheduling with precedence
  constraints and time windows*, TCS (2026),
  [publisher record](https://www.sciencedirect.com/science/article/pii/S0304397526002069).
  External release/deadline windows are not R1 occupancy windows; full text was
  not inspected.
* Papadimitriou–Yannakakis interval-order scheduling and Bodlaender–Fellows
  parameterized hardness: identified through L06/L09/L10; original proofs were
  not inspected. Do not assign precise theorem numbers or transfer their bounds
  solely from secondary citations.
* Garg, Gupta, Kumar, Singla, *Non-Clairvoyant Precedence Constrained Scheduling*,
  ICALP 2019, [primary record](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICALP.2019.63).
  Abstract inspected; weighted completion/flow-time objectives and unknown
  processing lengths differ from R1.

## Recommended citation practice

Use L04 for the precise FIFO resource edge, L03 for its architectural lineage,
L05 for the two-wide offline corollary, L11 for a list-scheduling ratio transfer,
and L12/L14/L15 for hidden-successor online precedents. Keep L07 separate as a
current claim with an explicit verification boundary. A source not returning a
matching result is not evidence of novelty.
