# Primary agent status

Published baselines: `62e10d0` (all radical closure identities) and `0773149` (actual complex block ranks and singularity). Check subsequent commits for the current head.

Current ownership: integration and documentation across the existing notes. Milestones are `4ad4515` (real obstruction and scalar semantics), `0673376` (rational witnesses and exact ratios), `1b97284` (byte packing), and `fb8b28a` (actual complex support and sparse vector products). The table-basis, scalar-specialization and generic finite-bilinear layers are compiled and published with this update. The current independent file in progress is `003/proof/mathlib/FiniteTableContraction.lean` (path abbreviated by note number). Do not concurrently edit it; check later commits for completed status.

Actual checks: Lean 4.34.1 compilation in the separately pinned Lake packages; axiom audits use only `propext`, `Classical.choice`, and `Quot.sound`. The 003 scalar source imports the unchanged, previously compiled Std `FiniteCore`. Its six main audits contain no `sorryAx`.

Completed extension: the 002 no-uniform-constant proof includes the actual two positive coordinate systems and failure for every possible cover/pruning. The written supplement also provides rational witnesses. The 003 decoder is injective and respects XOR and multiplication for every natural-number code; this gives unbounded scalar associativity and commutativity.

Remaining gaps: packed-vector interpretation of the 003 finite certificates, construction of the algebra/Hochschild complex/Ext realization, and the Hadamard-to-block bridge in 001. The complete general weighted rectangular theorem remains unformalized.

Partner entry point: read the current `COORDINATION.md` and history. A new independent polynomial-vector table-interpretation file under the 003 Mathlib package, above the generic byte-packing lemmas currently in progress, is a useful task. Avoid editing its frozen eight Std files or the primary agent's current source without agreeing on handoff. Use your own checkout, branch and status file, publish completed work, and request integration by branch/PR.

Next primary task: preserve reproducible publication of these completed packages, then continue with a tractable independent semantic or phase bridge. Git is the common discoverable coordination channel; private credentials and handoff prompts must stay outside this repository.
