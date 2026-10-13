# The window-excess parameter already contains balanced biclique

Status: **WRITTEN_PROOF**, **INDEPENDENTLY_REVIEWED**, and finite independent
constraint checks completed. No Lean claim.
The primary agent derived this construction after the XP(c) algorithm.
Literature search immediately found a closely related SOFSEM2016 paper,
*Precedence Scheduling with Unit Execution Time is Equivalent to Parametrized
Biclique*. Its public abstract and appendices confirm substantial overlap.
This is a parameter-preserving R1 embedding of a known scheduling-hardness
mechanism, with **NOVELTY_UNCONFIRMED** for the exact combined assumptions.
This note makes **no novelty claim** for three-cycle scheduling/biclique reductions.

## Construction and exact equivalence

Input: a bipartite graph G=(U,V,F), with |U|=n, |V|=m and
1<=k<=min(n,m). The source question is whether it has k vertices on
each side with every cross edge present. Trivial instances with k larger
than a side can be rejected before the reduction.

Put f=m+k, B=n+m+k, W=n+m=B-k, N=2B. There are B consecutive roots:
first f forced roots, then n roots representing U. They are followed by
B sinks. The first m sinks represent V. Each such sink has every forced
root as a true parent, and also every U-root that is **not** adjacent to
its represented vertex in G. Each of the remaining B-m padding sinks
has all B roots as true parents. These are the only true edges.

Every edge is forward and the true DAG has height two. The construction
is polynomial size, with O((n+m)^2) edges, and its parameter B-W is
exactly k. Its operations have **unbounded true fan-in**. It proves no
hardness claim for the intended at-most-two-input instruction subclass.

**Theorem.** The R1 optimum of this constructed program is3 if G contains
a balanced k-biclique, and4 otherwise.

**Positive direction.** Select k biclique U-vertices S and k biclique
V-vertices T. In the first cycle issue all roots except S, exactly W
jobs. In particular all f forced roots retire, so the retired prefix
is at least f>=m. Consequently all first m sinks have been admitted by
cycle two. Their parents from U avoid S whenever they belong to T.
Issue the k roots S and k sinks T in cycle two. This respects width
because W=n+m>=2k; the sinks' parents were already complete in cycle
one, so no same-cycle dependency is used. Now every root is complete
and the whole sink block is admitted. Issue the remaining B-k=W sinks
in cycle three.

**Negative direction, including underissuing/idling.** Suppose a schedule
finishes within three cycles. No sink can execute in cycle one, since
every sink has a nonempty set of true parents. Since cycle three holds
at most W sinks, at least B-W=k sinks must execute in cycle two.
At most W roots issued in cycle one, leaving at least k roots unfinished
then. If any forced root were unfinished, no sink would be ready in
cycle two, a contradiction. Thus those at least k unfinished roots all
represent U. No padding sink can be ready in cycle two, because it
depends on every root. Therefore at least k represented V-sinks issue
in cycle two. Each is adjacent in G to every U-root omitted from cycle
one, because all of its non-neighbor roots are true parents and must
already be complete. Any k of these omitted roots and any k of these
cycle-two V-sinks give a balanced k-biclique.

Two cycles are impossible by the workload 2B>2W. Four cycles always
suffice: execute the roots in batches W,k and then the sinks in batches
W,k. Each batch is admitted, and all root-to-sink dependencies are
satisfied before sink execution. Thus the stated optima are exact.

## Additional structural checks

All artificial window edges are already true edges. For a represented
sink with relative position v<m, its artificial predecessors are roots
of index at most v, all among the forced roots. Padding sinks already
depend on every root. There are no artificial edges within either
B-job layer. Hence E_B=E for this construction.

The poset width is exactly B. Each pure layer is an antichain of size B.
A mixed antichain can contain neither a forced root (comparable to every
sink) nor a padding sink (comparable to every root). It can use only
U-roots and represented V-sinks, with total size at most n+m=W<B.
Thus c also equals poset width minus the number of processors.

## Parameterized consequence and attribution

The explicit deterministic reduction preserves k as c. Using the known
W[1]-hardness of balanced biclique, it implies W[1]-hardness of R1 horizon
feasibility parameterized by c=B-W, already for horizon3 and true height2.
Therefore an FPT(c) algorithm for arbitrary true DAGs would imply
FPT=W[1]. This is a conditional complexity consequence, not an unconditional
impossibility of all faster algorithms, nor a hardness result at fixed c.
It is consistent with the proved XP(c) algorithm and FPT(c+S), since here
S=3W-N=n+m-2k need not be bounded by c.

Imported source: Bingkai Lin, *The Parameterized Complexity of k-Biclique*,
[arXiv:1406.3700v3](https://arxiv.org/abs/1406.3700v3), revised8June2019,
Corollary1.3. The primary agent opened the full paper and checked that
its supporting main reduction is deterministic; this note does not
re-prove Lin's theorem. Stronger time lower bounds require their exact
additional assumptions and are not asserted here.

The independent audit in `subagents/literature/EXCESS_HARDNESS_NOVELTY.md`
read the2016 publisher abstract and public Appendices B/C, including
Appendix C Lemma1. Makespan-three/biclique equivalence, height-two
precedences, nonedge constructions and the3/4 gap are close prior art.
Its full main body remains inaccessible, so the exact c=k comparison is
not closed. The older general-poset width-minus-processors gap-one
hardness also does not imply a result for a supplied ROB order: that
class has the polynomial c1 algorithm R21. No historical-first claim
is made. The bounded-fan-in case remains a distinct question.

## Reproduction scope

`src/biclique_reduction.py` constructs the actual graph and witnesses.
The general equivalence above is a proof, not inferred from finite tests.
`tests/biclique_audit.py` compares the constructed graph against the
independent time-variable CSP and directly replays witnesses. The actual
run in `evidence/biclique-root.json` passes1890 cases:1850 covering every
bipartite graph with both sides1..3 and every admissible k, plus40 random
cases with sides3..6 and seed2026101414. It includes898 YES and992 NO
cases,898 CSP witness replays,2788 constructed-witness replays and65663
checks that artificial ROB edges are already true. Runtime2.778674 seconds
on Python3.12.14; source hashes are recorded. Independent written reviews
are `subagents/theory/EXCESS_HARDNESS_REVIEW.md` and the literature note.
