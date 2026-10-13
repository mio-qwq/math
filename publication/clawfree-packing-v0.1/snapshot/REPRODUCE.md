# Reproduction: claw-free packing-coloring obstruction

Private manuscript v0.1. Mathematical source baseline:
`61488e05c9fe41984f483853f99e79f5715dc893`.

## Bounded package replay

Python 3.12.14 was actually used. These commands require only the standard
library. Run from the extracted archive root without Python's `-O` option:

```sh
python verify_manifest.py
python supplement/check_structural.py
python replay_independent_checks.py
```

The first command checks the exact manifest. The second reconstructs the
core and incidence expansion, checks the JSON certificate including types,
computes all BFS distances for k=3,4,5,7,9, and checks structural properties,
tip-neighbor formulas and every endpoint pair used in the short-walk bounds.
Controls reject a missing edge, a corrupted incidence, a changed palette,
a Boolean replacing an integer and equal low labels on adjacent vertices.
Frozen positive colorings for G_3 with radii (1,1,3,3,3) and G_4 with radii
(1,1,3,3,4) are independently tested against fresh BFS distances.

The third command executes the preserved independent review program without
changing its checking functions. It redirects only its input/output path
globals to the package-local frozen sources and a separate output directory.
It checks k=2,3,4,5,7, all 1296 fixed adjacency pairs against the JSON and
embedded Lean definitions, actual walks and BFS, locally compatible diamond
colorings, a distance-exactly-four control, and even-core necessary conditions.
Its k=2 test is an auxiliary control, not part of the k>=3 theorem statement.
Even-core necessary conditions alone do not prove a packing coloring exists.
New adapter output does not overwrite historical review JSON.

These finite checks guard implementation/semantic mistakes. The all-odd-k
noncolorability theorem is proved mathematically in the manuscript; it is
not inferred from the finite instances. Neither bounded command imports or
reruns the historical 531441-assignment enumeration.

## Fixed-instance Lean

Install Lean 4.34.1 with elan. In `supplement/`, use the supplied pinned Lake
configuration and manifest:

```sh
lake update
lake exe cache get
lake env lean frozen/ClawFree11334.lean
```

For a standalone explicit-root build in that environment:

```sh
lake env lean -R frozen -o ClawFree11334.olean frozen/ClawFree11334.lean
```

Mathlib is pinned to `d13f23b723b8a846827a245b89c10fc7d3f11612`.
The actual preparation run used the existing cached pinned environment and
an absolute `-R` path, produced a fresh object, exited 0 with no diagnostics,
and printed 18 audits using only propext, Classical.choice and Quot.sound.
See `verification/lean-fresh-object.json` and `.log` for the exact command,
source/object hashes and versions. An empty-cache installation was not tested.

The actual endpoint is `ClawFree11334.original_counterexample`: simplicity,
degree, connectivity, induced-claw exclusion, nonisomorphism to every
12-vertex graph, and failure of every Fin36-to-Fin5 packing coloring, using
actual graph Walk/edist. It does not formalize the infinite family or the
separate diamond-free lemma.

The optional historical checker can be run as
`python supplement/frozen/verify_counterexample.py`. It enumerates 531441
projected assignments. Its retained author output and older Lean receipts
are historical evidence, not new runs during this bounded preparation.
It is not required to understand or validate the manuscript's structural
proof and is deliberately excluded from the default replay commands.

## LaTeX and PDF

The manuscript is standalone and embeds its bibliography. The seven matching
BibTeX entries are supplied for journal adaptation, not required for the
current build. From `paper/`, use:

```sh
tectonic --keep-logs main.tex
```

Alternatively, run `pdflatex main.tex` twice with AMS, geometry, Latin Modern,
booktabs, TikZ, hyperref and microtype installed. Final preparation used
Tectonic 0.17.0+20260731 for two complete exports with exit code 0, no missing
references/characters or overfull/underfull boxes. Every one of seven pages
was rendered and visually inspected; all 20 fonts are embedded. PDF bytes
may vary by build timestamp even for identical TeX.

No native-editor compilation success or empty-machine toolchain test is
claimed for this paper. The existing 006 editor was left unchanged.

## Integrity and publication boundary

`manifest.json`, `SHA256SUMS` and `source-bindings.json` identify the exact
delivery/source versions. Archive replay runs from an actual extracted copy;
its external receipt binds the ZIP and checks damaged-payload rejection.
The package includes mathematical records only, no private instructions,
selection criteria, credentials, original third-party paper PDF or image.

This private draft has no approved new author/license metadata, external
submission, DOI, or external human peer review. AI assistance is disclosed;
human responsibility review and publication decisions remain pending.
