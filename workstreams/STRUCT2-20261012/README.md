# Structural and counting results

This directory contains two separate mathematical contributions and their
verification records. Neither package is a full Lean formalization or a
claim of human peer review. The written proofs, independently executed
finite checks, formalized statements, and literature comparisons have
separate scopes.

## Results

| Topic | Written result | Proof and evidence |
|---|---|---|
| Odd claw graphs | For every odd \(n\ge3\), exactly three finite simple bases have canonical double cover isomorphic to \(\operatorname{CDC}(\operatorname{CG}(n))\). Excluding the original graph gives exactly two TF-cousins. | [CG package](cg/README.md) |
| Symmetric edge polytopes, bicyclic graphs | For every \(n\ge5\), the maximum facet count among connected simple graphs with \(n\) vertices and \(n+1\) edges is the original Braun--Bruegge \(M(n)\). Every simple theta graph in this range has strictly fewer facets. | [Bicyclic proof](theta/PROOF.md) |
| Symmetric edge polytopes, theta maximizers | The four triples in Braun--Bruegge Conjecture 33 are the unique maximizing unordered path triples. The argument applies to every nonempty simple theta order \(n\ge4\), extending the original \(n\ge10\) range. | [Exact maximizer proof](theta/MAXIMIZERS.md), [theta package](theta/README.md) |

The CG result reviews and independently reconstructs an earlier project
candidate. The theta arguments supply the length-weighted geometric bound
and strict short-path compression beyond the previously proved scalar
comparisons. These topics are independent; they are not presented as one
combined paper.

## Provenance and contribution boundaries

The repository baseline inspected for this work is
`61488e05c9fe41984f483853f99e79f5715dc893`. The earlier CG source is the
12769-byte file
`workstreams/C-audit-1010/CG_ODD_COMPLETE_THEOREM.md` at
`9ad1f91d953060d01a504481eb857daf57758ab0\), with SHA256
`9544fbd1529f2815660d6f4b5ef5f52b6f114ef7682e0fa60997801c4a1255d8`.
The detailed [comparison](cg/independent/COMPARISON.md) binds the other
source files and explains the inconsistent historical digest without
inferring an unseen version.

The source papers already supply the known CG companion constructions,
the folding/conjugacy correspondence, the facet-labeling characterization,
cycle and theta counting formulas, and several same-parity and block
bounds. They retain their original attribution. Dated literature reports
state which subsequent sources were inspected and where access or coverage
was incomplete. They do not certify historical priority.

The earlier main-accepted scalar results and cycle conjectures are not
reopened or counted again here. All new files are confined to this
directory. No old mathematical source is replaced.

## Verification map

- CG's independent reconstruction precedes comparison with the frozen
  candidate. Its new original-definition checker exhaustively computes
  the finite cover automorphism groups rather than seeding the expected
  dihedral group.
- The theta bound has a review receipt bound to the exact source bytes.
  A separate checker counts actual graph facet labels and tests the
  Lipschitz and connected-saturation conditions.
- The exact theta maximizer has a separate source review and scalar
  regression. Finite checks supplement the universal compression and
  balancing proof; they do not establish it by extrapolation.
- Any Lean result is described at the statement actually compiled, with
  its toolchain, command, and axiom audit. Finite graph formalization does
  not imply a formal proof of the all-parameter classification.

See each topic's verification files for actual executions and hashes.
