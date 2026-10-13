# Reproduction: lower general position in Cartesian products

This is a private working manuscript, version 0.1, dated 12 October 2026.
The supplement uses mathematical sources from public repository revision
`61488e05c9fe41984f483853f99e79f5715dc893`.
No new DOI, external submission or approved author/license metadata is claimed.

## Three exact Python replays

Python 3.12.14 was actually used; the scripts require only the standard library.
Run from the extracted package root, without Python's `-O` option (assertions
are part of the checker):

```sh
python supplement/fixed319/verify.py
python supplement/universal/verify_universal_five.py
python supplement/universal/verify_unbounded_gap.py
```

1. The fixed check derives actual adjacency and all BFS distances. It checks
   orders 11,29,319; edges 30,140,2410; 314 outside blocking paths; factor
   lower bounds; and four mathematical negative controls.
2. The universal check regenerates all 25 MET5 rays and 9484 equality patterns,
   then excludes sizes 1,2,3,4. Expected landmark types are 1,2,8,106;
   outside-profile totals 1,5,87,9101; surviving GP type pairs 1,2,14,2381.
   The code reads no supplied metric JSON or discovery result.
3. The family check verifies finite regression instances r=6,7,12,31 and the
   complete-factor equality cases r=1,...,5. The all-r theorem rests on the
   manuscript's written proof, not inference from finite samples.

New successful run logs and JSON outputs appear in `verification/`. The
historical fixed Lean receipts copied into `supplement/fixed319/` retain their
original dates. Hashes in `source-bindings.json` bind exact copied source bytes.

The preserved independent review controls use the original local repository
layout. For an optional package-local replay, run
`python replay_independent_controls.py`. This adapter replaces only four
top-level path assignments in memory and executes the preserved control
functions unchanged. It writes new output into a separate directory and does
not replace the reviewer's historical source or output. These bounded controls
cover smaller metric cones, repeated projections and Boolean search systems;
they are not a second full MET5 or Lean verification.

## Lean, with explicit scope

Install Lean 4.34.1 with elan. In `supplement/`, run:

```sh
lake update
lake exe cache get
lake env lean fixed319/LowerGPProduct319.lean
```

The supplied Lake file pins Mathlib to
`d13f23b723b8a846827a245b89c10fc7d3f11612`. The exact resolved manifest from
the actual successful environment is included as `lake-manifest.json`.

The new actual compilation was performed in the existing pinned Mathlib
environment with its cache and an explicit package-root flag, producing a
fresh object. `verification/lean-fresh-object.json` and `.log` contain the
real command, version, source/object hashes and fifteen standard-only audits.
A new empty-cache machine was not tested.

The Lean result is the actual fixed original-conjecture counterexample:
connected factors, both lower-GP numbers at least 6, and their actual
Cartesian product lower-GP number at most 5. It includes the original
shortest-path semantics and inclusion-maximality bridge. It does **not**
formalize the universal min5 bound, the infinite family or product equality 5.

## LaTeX and PDF

The paper is standalone: its bibliography is embedded. `references.bib`
contains the same four entries for adaptation to a journal template; it is
not an extra build input. From `paper/`, use:

```sh
tectonic --keep-logs main.tex
```

Or run `pdflatex main.tex` twice with the standard AMS, geometry, booktabs,
TikZ, listings, microtype, hyperref and Latin Modern packages installed.
Actual exported builds use bundled Tectonic 0.17.0+20260731. Built-in editor
compilation timed out and is not counted as successful compilation.
PDF bytes may vary by engine or timestamp even for identical TeX.

## Integrity and dependencies

`manifest.json` and `SHA256SUMS` bind the delivered files. Use
`python verify_manifest.py` from the extracted root to reject missing or
changed files before reproduction. File hashes identify versions; they do
not prove mathematical validity, novelty or priority. The manuscript's
mathematical reduction explains why the finite obstruction checks prove the
universal bound.

AI assistance includes construction, proof development, code, Lean, searches,
independent AI checks and manuscript writing. Independent AI review is not
external human peer review. Human authors, contribution declarations,
responsibility review, funding, competing interests and license remain pending.
