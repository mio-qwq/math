# Reproduce the two-author public 006 preprint

This is the **first Zenodo V1 deposit candidate** for manuscript version **1.3**. Preserve the repository-relative paths after extracting the archive.

## Exact independent graph checks

Use Python 3.10+ (standard library), from the extracted archive root:

~~~sh
python 006-strong-product-packing-counterexample/verify_graph.py replay-primary
python 006-strong-product-packing-counterexample/verify_independent.py own --out replay-independent
python 006-strong-product-packing-counterexample/verify_independent.py compare --out replay-independent --root replay-primary
~~~

The primary checker accepts a POSITIONAL directory, not --out. Expected verified data: 608 auxiliary vertices; 9,168 edges; 64 candidate centers; 2,016 pairs separated by distance at least four; 38,912 same-center product targets and zero violations. Record the generated certificates in clean output directories.

## Lean source replay

The provided toolchain pins Lean 4.34.1 and a Mathlib Git manifest. Run from the extracted archive root:

~~~sh
cd 002-weighted-rectangular-pruning/proof/mathlib
lake update
lake exe cache get
cd ../../..
python 006-strong-product-packing-counterexample/verify_lean.py --out replay-lean
~~~

Network access and a working Lean installation are needed. The v1.3 editorial change does not claim a NEW Lean rerun. Historical logs are retained in the research repository, while the archived source and receipt are version locked.

## Manuscript build

~~~sh
cd 006-strong-product-packing-counterexample/paper
tectonic main.tex
~~~

The bibliography is embedded in the standalone LaTeX; references.bib is provided for journal workflows.

## Source and licenses

See LICENSES.md: paper PDF/TeX are CC BY 4.0; original source code and verification files remain under the repository's Apache-2.0 license. The external SHA256SUMS is the authoritative archive integrity index. This deposit is not peer-reviewed.
