# Independent original-definition review

The discovery packet was frozen at `e6ff18129aadad59150473c2e5faca16c5435d42`.
Its universal proof has SHA256
`6d4d128f753600bbb43783ca9c7ecf42b2c1e64eb301099fe78d291aa635d8d1`;
its explicit certificate has SHA256
`d7989f129d3bacbd54928b518cba64c5607a6e93968e1cef5f819c159d6d44a3`.

A separate agent first read the original definitions and conjecture, then
independently proved and implemented the fixed 90-point counterexample, before
reading the discovery program or full proof. Actual standard-library integer
verification passes: 504 vertices, 3024 arcs, 504 certified BFS rows, 8010 selected
ordered pairs and 704880 ordered distinct triples, with zero geodesic violations.
The selected pair distances are 3:2880, 4:3780, 5:1350. Every pair also has an
explicit legal five-step walk checked from the actual arc relation.

Two corrupted controls were actually rejected. Allowing the dropped first
letter as a new letter adds an illegal arc and is rejected by the graph semantic
audit. Replacing one selected vertex with a geodesic midpoint preserves 90 valid
vertices but produces 706 geodesic violations, so it is rejected by the same
general-position test. These controls check both the graph convention and the
claimed conclusion.

The independently selected alphabet partition uses terminals `{0,1,2}`. Under
the bijection `x -> (x+6) mod 9` its selected list matches the discovery certificate
with terminals `{6,7,8}` exactly, including order. The remote certificate hash was
checked from the actual published bytes.

After freezing this calculation, the reviewer read the universal proof and
reconstructed buffer existence, every appended letter's legality, the bounds
`k<=dist<=2k-1`, and the positive improvement
`(d-2k+1)(d+k-3)_(k-2)`. No mathematical gap was found in the original range.
Finite checking was not used to infer that universal conclusion.

Frozen independent verifier hash:
`e55ef2ee7d502e44ee96383c44072b48c6ead2914c58c2cd8ff6fd477af716ae`.
Frozen original execution receipt hash:
`a172e425b7f3caefe90760b6fa73e0f67d7e16d550676991e7f4c75ac22508e3`.
The written review is an independent AI-agent review, not a claim of a human
journal referee decision. Lean compilation and its independent source-semantic
review are separate gates, recorded with their exact source in `verification.json`.
Historical novelty and formal human authorship are not established by this review.

## Final original-path Lean semantic review

The frozen final source has SHA256
`ec05b83390da70ca7c5e46d5eda3d24d282028c5ed6a38c35363399220e05f2a`.
An independent reader checked the actual vertices, the full old-word exclusion
in every arc, the finite 90-point set, and the single-shortest-simple-path
statement. The `SimplePath` constructors bind the ordered endpoints, vertex
list, actual arcs and length; its list is proved duplicate-free. Kernel loop
removal preserves endpoints and does not increase length. Kernel splitting at
an actual support vertex preserves the exact total length. Both bridges occur
in `selected_original_general_position` and the final original-counterexample
declarations, so the result does not depend on a prose-only walk/path bridge.

The actual successful ROOT3 execution ran on 2026-10-10 UTC from
05:46:40.1120630 to 05:46:54.6485770, with exit code zero and zero warnings,
errors or panics. The reviewer compared all 18 source audit commands, raw log
outputs and JSON declaration/axiom records in order; they agree and contain
only standard axioms. This was an independent source and actual-log review,
not a second Lean run. The final review hash is
`211e54ffa05c2742ca3e83f6360f4c3578fd8ef8fc3e52ef2559ceef6f110dbc`.

The accepted Lean scope is the original fixed Pe(6,3) counterexample, including
all shortest actual simple paths. The universal parameter extension remains
an independently checked written theorem. No exact maximum or minimum
counterexample size is claimed.
