# Source audit and correction: reproducibility record

The source audit and the bounded correction note are separate from any subsequent proof of the mixed-parity theta conjecture. This directory contains no full-paper Lean formalization and no claimed human peer review.

## Retrieved sources

`source_hashes.json` records SHA256 hashes and byte lengths of the actual JIS PDF and public TeX, all four observed Braun-Bruegge arXiv versions, and all three observed Mori-Mori-Ohsugi arXiv versions. These source documents were read outside the repository and are not redistributed here. The JIS PDF's hash is `52e4b28b4e4106af07768940e60bb06fdd76f638b288e0139ec7bc5c05dd397a`.

The journal-version access limitation for the Mori-Mori-Ohsugi paper is stated in `SOURCE_GATE.md`. A failed publisher download is not treated as full-text evidence. Comparing the v2 and v3 extracted preprint texts showed only the arXiv stamp and Kenta Mori's affiliation changed; this comparison does not prove equality with the publisher's version of record.

## Executed finite check

Executed on 2026-10-12 at 09:02 UTC with Python 3.12.14:

```sh
python check_boundary_correction.py
```

The process exited with status 0, emitted no stderr, and completed in approximately 0.26 seconds. `run_evidence.json` records the exact run time, command, interpreter, checker hash, and output hash. `boundary_correction_check.json` preserves the actual output.

| Simple theta | Direct facet count | Arithmetic M(n) | Ratio |
| --- | --- | --- | --- |
| CB(2,2,1) | 12 | 12 | 1 |
| CB(4,4,1) | 324 | 360 | 9/10 |
| CB(6,4,1) | 1560 | 1800 | 13/15 |
| CB(6,6,1) | 7600 | 8400 | 19/21 |

The first two cases are additional small-domain regressions. Only the last two fall within Proposition 30's stated n>=10 range. For all four, the output also evaluates the printed rational expression as an algebraic diagnostic; this does not attribute an n<10 theorem to the source.

The checker constructs the simple graph from three paths, enumerates normalized integer labels through all increments in {-1,0,1}, and retains exactly the labelings whose active edges span a connected graph. Its facet characterization is the source's Theorem 5. It neither evaluates nor imports F to generate the direct count. Exact binomial arithmetic is used only for comparison after the direct graph count.

Two controls are included. Admissible Lipschitz labelings with disconnected active-edge graphs are rejected rather than counted as facets. An attempted CB(2,1,1) construction is rejected because the two length-one paths would duplicate a simple edge. The actual counts disagree with the incorrect printed rational expressions and agree with the proved corrected formulas.

The all-parameter reasoning is in `PROPOSITION30_CORRECTION.md`. These finite checks validate the transcription diagnosis and the implementation on the displayed cases; they are not substitutes for its proof and do not prove Conjectures 32 or 33.

## Contribution boundary

`SOURCE_GATE.md` restores definitions, formulas, version numbering, and a precise exclusion of mixed-parity simple theta graphs from the cited join-graph theorem's domain. `PROPOSITION30_CORRECTION.md` repairs identities in an already proved proposition; its inequality conclusion and its underlying boundary facet formula were published previously. The literature search found no equivalent mixed-parity theta proof in the inspected material, with the explicitly recorded coverage and access limitations. No historical priority conclusion follows from a failed search.
