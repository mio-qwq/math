# Finite Lean verification of the original CG(3) graph

## Verified result and exact scope

Cg3.lean was compiled successfully with official Lean **4.34.1**, commit
5045d0056413266e57c625dcd7c365b10e377c52, importing **Std only**.
The measured successful run took **33.938429 seconds**, with exit code 0.
The complete stdout, stderr, command and version are in compile.log;
verification.json records source/tool hashes and every printed axiom audit.

The main graph-theoretic theorem is:

    Struct2.Cg3.actual_six_cycle_iff_not_centre

For every vertex of the actual canonical double cover of CG(3), it lies on
a simple six-cycle if and only if it is not a claw centre. The cycle
predicate requires six distinct vertices and all six original adjacency
relations. This is the finite original-graph instance of the type invariant
used in the all-odd written proof.

This file also proves the original edge-list length, original looplessness
and symmetry, CDC looplessness and symmetry, degree exactly three for every
CDC vertex, and three explicit strongly switching maps. It makes no Lean
claim about all odd n, the full cover automorphism upper bound, complete
conjugacy classification, or the exact number of isomorphism classes of
folded bases. Those conclusions remain supported by the separate universal
written proof and independently executed Python checks.

## 1. Original mathematical semantics

Source:

Russell Mizzi, *Lifting and Folding: A Framework for Unstable Graphs and
TF-Cousins*, arXiv:2603.27559v3, Definition 6.1:
<https://arxiv.org/html/2603.27559v3>.

The 30 original vertices are encoded by Fin 30:

| Original type | Integer label |
|---|---|
| Ring vertex \(u_t\), \(0\leq t<18\) | \(t\) |
| Centre \(c_i\), \(0\leq i<3\) | \(18+i\) |
| Leaf \(\ell_{i,j}\), \(0\leq i,j<3\) | \(21+3i+j\) |

The sourceEdges definition lists precisely the ring edges and, for each
pair \(i,j\), the three edges

\[
c_i\ell_{i,j},\quad \ell_{i,j}u_{i+3j},\quad
\ell_{i,j}u_{i+3j+9}.
\]

sourceAdj is membership in this edge list in either orientation. The CDC
encoding is \(2v+\varepsilon\), with \(\varepsilon\in\{0,1\}\). Its adjacency
requires opposite layer bits and adjacency of the corresponding original
vertices. Cover centre labels are exactly 36 through 41.

### Efficient adjacency with a proved semantic bridge

Repeatedly unfolding the entire 45-entry original edge list is unnecessary
for each step of a cycle search. nextBase explicitly computes three
candidate neighbours. The theorem fast_source_exact proves, on all
\(30^2\) original vertex pairs, that their adjacency test is exactly
sourceAdj. cdc_adjacency_is_original then identifies the computational CDC
adjacency with the literal definition above.

next_complete proves that each CDC adjacency is represented by one of the
three choices; next_distinct proves that these choices give distinct
vertices. The cubic theorem supplies this actual three-neighbour bijection.
No adjacency equivalence or regularity assumption is supplied as a theorem
hypothesis.

### The six-cycle search is complete for actual cycles

SixCycle is the ordinary six-vertex predicate: the vertex list is Nodup,
and each consecutive pair, including the closing pair, satisfies Adj.
HasSixCycle existentially quantifies the five vertices following a chosen
starting vertex.

IndexedSixCycle instead obtains the five subsequent vertices by five
choices in Fin 3, using the verified next function. This gives only
\(3^5\) walk candidates per starting vertex. The theorem indexed_iff_actual
proves both directions of its equivalence with HasSixCycle:

- A successful indexed walk supplies the five vertices of an actual cycle.
- Given any actual cycle, next_complete supplies its five neighbour choices.

Kernel reduction then proves indexed_six_cycle_classification over all
60 starting vertices. The main theorem transfers that result to the actual
six-cycle predicate through the proved equivalence. Thus the formalization
does not merely certify an unchecked search routine or a precomputed table.

## 2. Theorems and axiom audit

The successful file contains 16 explicitly audited results.

| Theorem | Verified meaning | Reported axioms |
|---|---|---|
| fast_source_exact | Efficient adjacency equals the original edge-list adjacency | propext |
| cdc_adjacency_is_original | Computational cover adjacency is the literal CDC | propext |
| original_edge_count | The defining edge list has length 45 | none |
| original_loopless | No original vertex is adjacent to itself | none |
| original_symmetric | Original adjacency is symmetric | propext |
| cdc_loopless | No CDC loop | propext |
| cdc_symmetric | CDC adjacency is symmetric | propext |
| next_complete | Three choices cover exactly all CDC neighbours | propext, Quot.sound |
| next_distinct | The three neighbours are distinct | none |
| cdc_cubic | Every CDC vertex has degree exactly three | propext, Quot.sound |
| indexed_iff_actual | Indexed search is equivalent to actual simple six-cycles | propext, Quot.sound |
| indexed_six_cycle_classification | Indexed six-cycle existence equals non-centre status | propext, Quot.sound |
| actual_six_cycle_iff_not_centre | Actual simple six-cycle existence equals non-centre status | propext, Quot.sound |
| deck_strong | The original deck is strongly switching | propext |
| companion_guide_strong | Deck composed with the original ring half-turn is strongly switching | propext |
| reflection_guide_strong | Deck composed with the even-axis source reflection is strongly switching | propext |

StrongSwitch explicitly asserts involutivity, preservation and reflection
of adjacency, reversal of the original CDC layers, and no adjacent image.
Bijectivity follows from its involutivity clause. These three maps are
explicit examples, not a formally proved exhaustive list.

The actual union of reported axioms is precisely:

    Quot.sound
    propext

The file uses decide +kernel for the finite computations. It does not use
native_decide, a native-evaluation correctness axiom, sorry, admit, or an
unproved custom axiom. The standard logical axioms printed above are
reported rather than hidden. The command's successful kernel checking and
the individual axiom audits are distinct pieces of evidence.

## 3. Reproduction on an ordinary host

Use the pinned toolchain in lean-toolchain and run:

    python verify.py --lean /absolute/path/to/lean-4.34.1-linux/bin/lean

The driver checks the reported version and release commit, invokes Lean
with one thread, writes an olean, preserves actual compiler output, and
audits every listed theorem. It records hashes in verification.json.
It does not download dependencies. No Mathlib checkout is required.

Official release:
<https://github.com/leanprover/lean4/releases/tag/v4.34.1>

Official Linux archive:
<https://github.com/leanprover/lean4/releases/download/v4.34.1/lean-4.34.1-linux.tar.zst>

The downloaded 580432872-byte archive was checked against the digest in the
official GitHub release metadata:

    47bf4bbd78f70c2e9670598ab7124d92b6efb7330ff33e5fbb4030f6fd72e4e4

Its observed compiler version is:

    Lean (version 4.34.1, x86_64-unknown-linux-gnu, commit 5045d0056413266e57c625dcd7c365b10e377c52, Release)

For a container that cannot preserve the archive's original numeric owner,
extract with tar's --no-same-owner option.

## 4. Explicit application-path adapter used by this execution host

The original, unmodified release binary initially exited with:

    error: failed to locate application

The official source identifies the cause. In src/runtime/io.cpp,
lean_io_app_path obtains the process ID and reads /proc/<pid>/exe.
In Lean/Util/Path.lean, initSearchPathInternal calls getBuildDir, which
uses IO.appDir, before command-line processing. Setting LEAN_SYSROOT alone
therefore does not repair this internal startup path.

Exact official source versions:

- <https://github.com/leanprover/lean4/blob/v4.34.1/src/runtime/io.cpp>
- <https://github.com/leanprover/lean4/blob/v4.34.1/src/Lean/Util/Path.lean>
- <https://github.com/leanprover/lean4/blob/v4.34.1/src/util/shell.cpp>

On this host, querying the numeric own-process executable path returned
EACCES. runtime_path.c is a narrow application-location adapter:
for exactly the readlink request /proc/<this process's ID>/exe, it copies
the already known path supplied in STRUCT2_LEAN_BIN. It performs no
filesystem access for that request. All other readlink calls retain their
normal implementation and permission checks. The adapter does not modify
permissions, Lean's kernel, proof rules, theorem contents, or the official
release binary.

An initial attempt to interpose Lean's IO.appPath symbol directly had no
effect on this release and was discarded. The checked-in adapter is the
explicit-path implementation described above.

If the same host compatibility issue occurs, build the adapter outside
the source directory and provide it explicitly:

    cc -shared -fPIC runtime_path.c -ldl -o /chosen/runtime/runtime_path.so
    python verify.py --lean /absolute/path/to/lean-4.34.1-linux/bin/lean --adapter /chosen/runtime/runtime_path.so

The driver limits the adapter environment to its compiler subprocesses.
Omit --adapter on a normal host. The adapter source and binary hashes used
in the successful run are recorded in verification.json.

Before the successful graph compilation, a minimal import Std / #check /
arithmetic theorem was compiled through this adapter. It exited 0 and
printed that the arithmetic theorem depended on no axioms. Initial graph
iterations exposed missing Decidable unfolding for StrongSwitch; those
failed iterations are not counted as successful formalization. The final
file unfolds that definition explicitly and compiles with all audits
shown above.

## 5. Frozen successful sources

Cg3.lean SHA256:

    781c9ddf9999c7645e03b2e3b9cd9fcf3f346b2128fd22472fbc420f1e5fb7e7

The verification metadata identifies the exact driver, adapter source,
adapter binary, compiler binary, generated olean and compile log. Generated
olean and shared-library files are excluded from version control; the
source and actual verification records suffice to reproduce this finite
result.

No claim of human peer review or full all-parameter Lean formalization is
made by this packet.
