# Literature map and current-source boundary

Inspected on 13 October 2026 UTC / 14 October Asia/Singapore. The [independent full review](subagents/literature/LITERATURE_REVIEW.md) records 18 source groups, exact access limitations, authors, dates and inspected theorem scopes; [SEARCH_LOG.md](subagents/literature/SEARCH_LOG.md) records searches. This is an initial audit, not proof of exhaustive novelty clearance.

| Topic | Primary source | Consequence for ILP1 |
| --- | --- | --- |
| ILP limits and window definitions | D. W. Wall, [1993 report](https://davidwall.info/papers/WRL-TR-93.6.pdf) | Earlier trace/oracle measurements are not R1 global-optimality theorems |
| Window-size analysis | Dubey, Adams, Flynn (1994), [IBM record](https://research.ibm.com/publications/instruction-window-size-trade-offs-and-characterization-of-program-parallelism) | Full-text comparison remains required; institutional abstract inspected |
| Earlier window dependence edges | Tullsen, Calder (October1998), [UCSD technical report](https://cseweb.ucsd.edu/~calder/papers/UCSD-CSE98-CPProfile.pdf), §3 | Explicit ordered entry/exit and extra window-edge dependencies; earlier prior art than Fields2001 |
| ROB resource edges | Fields, Rubin, Bodík (ISCA 2001), [original paper](https://www.eecg.utoronto.ca/~moshovos/ACA06/readings/critical.pdf), Table 1 | In-order dispatch/commit and commit-to-dispatch capacity edges are established prior art |
| Explicit FIFO/ROB constraint | Navada, Choudhary, Rotenberg (PACT 2010), [paper](https://ericrotenberg.wordpress.ncsu.edu/files/2025/06/paper_PACT-19.pdf), §§5.1–5.2, Table 2 | Eager R1 execution-only elimination is a specialization, not a new idea of resource precedence |
| Two-wide offline optimum | Coffman, Graham (1972), [paper](https://fanchung.ucsd.edu/ron/papers/72_04_two_processors.pdf) | General two-machine unit-job optimum is polynomial; finite ROB constraints can be added first |
| Exact algorithms and classical complexity | Nederlof, Swennenhuis, Węgrzycki, [arXiv:2312.03495](https://arxiv.org/html/2312.03495v1), Theorems 1.1–1.2 | Distinguish variable machine count from historically unresolved fixed three-machine complexity |
| September 2026 three-machine claim | OpenAI, [family 124](https://github.com/openai/math/blob/main/lean/docs/124.md) | Preprint plus actual Lean proof entry found; not independently compiled/audited here |
| List-scheduling bound | Graham (1966), [DOI](https://doi.org/10.1002/j.1538-7305.1966.tb01709.x); Graham (1969), [DOI](https://doi.org/10.1137/0117039) | The standard factor 2−1/W transfers after ready-set equivalence |
| Unknown-successor online lower bounds | Epstein (2000), [DOI](https://doi.org/10.1016/S0020-0190(00)00141-1) | Generic adversarial method and constants are classical; observation model differs |
| Online precedences and advice/predictions | Lassota et al. (ICML 2023), [primary paper](https://proceedings.mlr.press/v202/lassota23a/lassota23a.pdf) | Hidden important successor constructions have prior art; task release/objective differ |
| Formal scheduling | [independent review L16–L18](subagents/literature/LITERATURE_REVIEW.md) | Existing Lean/Rocq work must be compared by statement and assumptions, not language alone |

The primary agent additionally opened the full original Fields et al. PDF and checked Table 1: DD in-order dispatch, CD finite ROB, DE dispatch-before-execution, EC execution-before-commit and CC in-order commit. This extends the literature subagent's recorded access, which reached the retrospective and the explicit 2010 source. The original paper describes a richer processor execution model; it does not alone establish every claimed R1 optimization consequence.

The September 2026 artifact was inspected at commit `1581d4cbdd69a0faf34b2089614fe2a814316a6a`. The actual Lean endpoint is `OAI/Computability/Scheduling/Main.lean`, separate from challenge scaffolding. A `sorry` in the challenge statement is not evidence of a hole in the solution. The entire dependency closure and its axioms have not been audited in ILP1. Therefore this workstream neither unconditionally accepts that result nor reports the three-machine question as simply still open. It does not claim to solve it.

For finite W, the resource-footprint formula still optimizes over schedules. For W=2, R2 plus Coffman–Graham gives a known polynomial route, including binary search for B_sat; that is an imported corollary and is not an implemented new algorithm here. Special interval-order theorems cannot automatically be applied after arbitrary program dependencies are added: a four-job 2+2 poset already defeats such a class-membership assumption when B>=4.

All online ratios in this workstream are **strict multiplicative ratios without an additive constant**. A finite gadget does not automatically prove an asymptotic competitive lower bound with an allowed additive term. Fixed-resource repetition and composability are open follow-up tasks.

The primary agent opened the original Tullsen–Calder report and checked §3, including ordered IW entry/exit and added dependencies for instructions blocked from admission by a full window. Its profiler includes variable latencies, caches and branch prediction. This is direct prior art for the window-edge idea; the inspected text does not establish all R1 optimum or threshold formulas. [THRESHOLD_REVIEW.md](subagents/literature/THRESHOLD_REVIEW.md) additionally compares statistical saturation models and register-saturation terminology, and explains the one-cycle limitation of the layered family. Missing Dubey1994 full text remains a material novelty-audit gap.


The sharp randomized result has a separate [targeted audit](subagents/literature/NARROW_ONLINE_NOVELTY.md): Fujii–Kasami–Ninomiya1969 with1971 correction, Kozen–Vazirani–Vazirani1985, ISAAC2025 degree-two bipartite matching, a2026 randomized-greedy framework, and lookahead/buffer variants. Primary sources were read to the recorded extent. The classical scheduling/matching identity is attributed; neither numerical equality of constants nor a two-choice random rule establishes model equivalence. R15 remains NOVELTY_UNCONFIRMED.

The follow-up HIDDEN_FAMILY_ADVICE_REVIEW.md in subagents/literature reads primary advice/string-guessing sources and explicitly attributes common-prefix message counting and product-instance methods. No checked source was found to imply the exact ROB hidden-subset implementation or the two-input separator-free composition. This limited negative search is not a novelty certification.
