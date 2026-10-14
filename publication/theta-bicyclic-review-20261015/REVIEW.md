# Independent written review: theta and bicyclic facet maxima

Review completed 15 October 2026 (Asia/Shanghai), against frozen commit `fcd8dbf1084bcca44d67fc0e6ba6d46d301bb9e5`.

**PASS for the frozen written mathematics and complete seven-page manuscript.** This is an independent AI review by a reviewer uninvolved in discovery or drafting, not human peer review, a universal Lean verification or historical-priority certification.

## Frozen sources

Paths are relative to `workstreams/STRUCT2-20261012/theta/` at the frozen commit.

| Source | SHA256 |
| --- | --- |
| PROOF.md | 81f7c5f4326828b16a34204e1a84b3dec136ea1d61c30cfb60b17e6395616655 |
| MAXIMIZERS.md | c0c02847ae525260d65dd5b11c1ee940b4b63aec6e2167c39fa8a9c12fc12fab |
| paper/main.tex | 594d42ceecb510bd79a1cc0df189819442d0976044743fd5a36909f4519029ec |
| paper/theta-facet-maximizers.pdf | b851a2b389a1b1afb7f79220b0937f150613776f1ca9b7192000b2eb8d6e599b |

[Frozen source package](https://github.com/mio-qwq/math/tree/fcd8dbf1084bcca44d67fc0e6ba6d46d301bb9e5/workstreams/STRUCT2-20261012/theta).

## Scope and reasoning checked

The review read both complete mathematical notes and the complete manuscript, compared the original journal statements and the Mori-Mori-Ohsugi follow-up, and inspected all seven frozen manuscript pages. Earlier PASS reports were not used as premises for the new judgment.

The accepted scope is the unique maximizing unordered path triple for every simple theta order n>=4; the strict theta bound and global connected simple n-vertex, n+1-edge maximum/equality data for n>=5; and the separately handled four-vertex graph K4-e with twelve facets. The source's undefined C1 convention is not imported. Two unit-length paths would duplicate an edge and are excluded.

The reviewer independently checked the original facet-labeling inequalities and connected saturation, both mixed-parity terms, the central-binomial/Vandermonde envelope with zero rows, strict short-path compression, exact balancing, exclusion of common-parity competitors and the cycle/bridge block reduction. Different even-order bridge attachment patterns remain legitimate ties; unique theta path lengths do not imply a unique general graph maximizer.

These resolve journal Conjectures 13/32 on the natural simple-graph domain and Conjecture 33 on its stated range, with a stronger theta range. The review does not establish the original global Conjecture 2, Conjecture 31 transfer inequalities, multigraph statements, larger multipath classes or a Lean graph/polytope theorem.

The later join-graph theorem adds all cross edges and concerns a different global bound. Mixed-parity simple theta graphs of order at least five have connected complement and fall outside that input class. This rules out that direct overlap; it does not prove that no other earlier solution exists. No inaccessible publisher version-of-record text is claimed to have been read.

## Actual independent finite checks

The supplied [checker](check_independent.py) is newly written from the original definitions, with no imports from candidate code. Its [actual receipt](INDEPENDENT_CHECKS.json) records:

- Fourteen actual graphs and 14,526 spanning-tree label assignments.
- All 132 legal unordered triples at orders 4 through 16.
- 165 compression orientations, 109 strict cases, 127 short-formula checks and 42 balancing transfers.
- 203 cycle/bridge data cases and 145 Vandermonde checks including zero rows.
- Rejection of duplicated unit paths and labelings with disconnected saturated subgraphs.

These checks challenge definitions and boundary cases; they do not prove a universal theorem by a cutoff. The universal acceptance rests on the complete written proof. The recorded execution is retained unchanged; rerun on a copy to preserve its date and hash.

Only minor editorial improvements remain for a subsequent author-identified revision: pin reproduction URLs, clarify that bridge/cycle comparisons compare realizable block data, and update the manuscript's old review-provenance sentence. No mathematical blocker was found. Any mathematical revision requires new source binding and review.
