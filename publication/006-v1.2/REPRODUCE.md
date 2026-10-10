# Reproducing the 006 v1.2 materials

Extract the supplement into a new directory and preserve repository paths. Python 3.10 or later uses only its standard library for the exact checkers. Do not use python -O: the primary checker uses assertions. Use new output directories so that the frozen receipts remain intact.

## Exact graph and same-center certificate

Run these commands from the archive root, in order:

```sh
python 006-strong-product-packing-counterexample/verify_graph.py replay-primary
python 006-strong-product-packing-counterexample/verify_independent.py own --out replay-independent
python 006-strong-product-packing-counterexample/verify_independent.py compare --out replay-independent --root replay-primary
```

The primary output path is a positional argument; it does not accept --out. The second implementation reconstructs the graph before reading primary artifacts. Expected facts: 608 auxiliary vertices, 9168 edges, 64 centers, minimum center distance four, 2016 center pairs, 38912 product targets and zero violations. These programs do not prove the arbitrary-set cube obstruction or determine the numerical optimum.

## Pinned Lean environment and serial proof replay

Use the [ordinary Lean toolchain manager](https://lean-lang.org/install/). The supplied configuration pins Lean 4.34.1 and Mathlib d13f23b723b8a846827a245b89c10fc7d3f11612. It uses a Git requirement rather than a private local path. From the archive root:

```sh
cd 002-weighted-rectangular-pruning/proof/mathlib
lake update
lake exe cache get
cd ../../..
python 006-strong-product-packing-counterexample/verify_lean.py --out environment-only --check-environment
python 006-strong-product-packing-counterexample/verify_lean.py --out replay-lean
```

If Lake is not on PATH, pass its executable using --lake. The environment-only check reports proof_compiled=false and does not validate a proof. The ordinary replay compiles the factor, geometry and graph sources serially into new project objects and checks 12, 12 and 26 declaration axiom lists, respectively. It inspects actual Lean version, Mathlib Git root/HEAD, manifest pin, tracked dependency worktree and configuration hashes. A failed run is not accepted as a passing replay.

The supplement retains actual fresh-object proof runs from 2026-10-09, exact-program replays from 2026-10-10, and a new environment-only check. These dates and scopes are distinct. This publication revision does not repeat heavy compilation of unchanged mathematical sources. A new-machine rebuild with an entirely empty dependency cache has not been tested; network access to pinned dependencies and their artifacts is required.

## Standalone paper and references

```sh
cd 006-strong-product-packing-counterexample/paper
tectonic main.tex
```

Alternatively run pdflatex main.tex twice with standard AMS packages, geometry, array, booktabs, longtable, lmodern and hyperref. main.tex embeds the complete bibliography and needs no extra TeX input files. references.bib supplies matching reference data for later journal typesetting; it is not an input required by this standalone build.

The frozen PDF was successfully built with installed Tectonic 0.17.0+20260731, has 15 pages and 20 embedded fonts, and has no unresolved-reference, overflow or missing-character TeX diagnostic. The native editor compiler could not locate platform directories. The successful export was made with the existing bundled executable; the retained nonfatal Fontconfig startup message is distinct from a TeX error. Changing engine or creation date can change PDF bytes without changing the proof.

## Archive integrity and scholarly status

The manifest records the SHA256 and length of each payload file. External SHA256SUMS covers the ZIP, manifest, metadata, abstract, TeX, PDF and BibTeX, and the separately supplied final replay receipts. The archive does not recursively include itself or those final receipts. File-integrity validation is distinct from mathematical verification. An extraction replay of the three graph commands is recorded separately in [archive-replay.json](archive-replay.json).

The name, ORCID and affiliation are user-supplied author drafts. Human responsibility review, deposit license and external-publication approval remain pending. The included repository LICENSE preserves provenance for already released sources and selects no new paper license. AI-agent review and separate exact programs are not human peer review; historical firstness is not established. No DOI or external submission has been made.
