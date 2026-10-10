# Independent original-scope, mathematical and Lean-source review

An AI agent uninvolved in discovery and in this Lean implementation
independently reconstructed the argument, checked the original source
HTML and PDF, and then read the whole final Lean source and the actual
ROOT2 JSON and axiom log. Both reviews passed with no must-fix defect.
This is not human peer review or a priority certification.

The original Problem 1 has exactly the queried palette and no hidden
core-diamond or connectivity restriction beyond connectedness. The
exception H is the 12-vertex triangle expansion of K4. Independent
formula reconstruction matches all certificate core edges, incidence
labels and original edges. A one-time independent standard-library
check ran 2026-10-10T08:12:24.137626 to 08:12:24.360639 UTC, exit zero:
36 vertices, 54 edges, connected cubic claw-free; all 162 adjacent-core
endpoint pairs are within three edges and all 216 relevant port-to-other
triangle pairs within four edges. Its small 216-state diamond check
found 48 proper core labelings, none satisfying private-neighbour
necessity. It did not run or import B's verifier or discovery solver.

The independent mathematical review reconstructed the necessary
projection for every original coloring, arbitrary high choices,
proper core labels, radius-four private-neighbour requirement and the
diamond/odd-cycle contradiction. It did not assume one high point per
triangle, or replace necessity by sufficiency.

**Final reviewed and actually compiled source SHA256:**

`afad6d3313c93fd5681be0ba0e25d302c73d019448681cb4c6552f8a0e0765b2`.

Actual ROOT2: 2026-10-10T08:28:20.0309293+00:00 to 2026-10-10T08:29:15.2796926+00:00; exit zero,
zero warnings/errors/panics, 18 expected and observed audits, no
nonstandard axioms. Only subsets of `propext`, `Classical.choice`,
`Quot.sound` occur. The full source/log reviewer did not recompile or
repeat any enumeration. The public source is byte-identical to the
source before and after the actual run. Final review report SHA256:
`d30479b43e65c65396bac6c41af7d0e27ac735eda4b3e1cdcad964a3fc39d856`.

The final declaration contains actual connectedness, the definition
excluding every induced claw, degree exactly three, nonisomorphism to
every 12-vertex graph, and failure of every original five-color function.
The walks give real metric bounds; the extraction theorem quantifies
over arbitrary original colors. The core impossibility proof is
structural. Ordinary kernel `decide` checks fixed graph pairs and small
color lemmas (at most four Fin3 variables). No `native_decide`, admitted
proof, extra axiom or complete Fin12-color enumeration occurs.

Discovery input was frozen at B commit
`bf89129f2bf457f7a63292d559f5c279330c9b2c`. Certificate SHA256:
`7d1cdd61f032185728ffac6a6b0b6a79c611e0a36341a78eb35610df55b95ccd`.
The optional author's verifier remains byte-identical to its frozen
input, SHA256 `e9e7cb20a1b6989905563193bd92c388231e6e3a049caa27f6db1b33fdb7f573`;
the independent check and structural Lean theorem do not depend on its
finite enumeration result. The author-provenanced recorded output is
not presented as a fresh ROOT run.

The written odd-k theorem is independently checked but not universally
Lean-formalized. No minimum-order, exact packing number or historical
firstness conclusion is part of this acceptance.
