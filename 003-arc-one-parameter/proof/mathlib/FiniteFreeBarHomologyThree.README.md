# A nonzero class in the actual module-Hom quotient

`FiniteFreeBarHomologyThree.lean` uses every genuine A-linear map
`Pn →ₗ[A] CharacterModule eps`, with its existing R-module structure.
Precomposition with the actual boundary3 and boundary4 gives two
R-linear differentials. Their composite is zero by the proved
full-coefficient chain law, rather than a character separation argument.

The degree-three quotient is the actual kernel of the second Hom
differential modulo the image of the first differential inside that
kernel. A class is zero exactly when its representative is the
precomposition of some arbitrary degree-two A-linear map.

The fixed f-character Hom defines a nonzero class whenever q³ is
nonzero. Its closure holds on all of P4, and the nonboundary statement
excludes every degree-two Hom map. In a ring without zero divisors,
q nonzero suffices. This strengthens the earlier individual closed
and nonboundary statements to an actual module-Hom quotient class.

Eight printed audits use only standard Lean axioms. Exact source,
toolchain, compilation and independent replay records are in the
verification JSON. For dependency-ordered replay, run in this folder:

```powershell
.\verify-cohomology.ps1 -Targets FiniteFreeBarHomologyThree
```

This quotient has not yet been identified with Ext. Such a conclusion
still requires the relevant exact projective resolution and comparison.
