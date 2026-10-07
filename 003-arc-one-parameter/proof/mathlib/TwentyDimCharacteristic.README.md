# Characteristic two of the installed algebra

`TwentyDimCharacteristic.lean` proves that the actual scalar algebra map is injective by reading coordinate e. It then installs `CharP (TableAlgebra q) 2`, proving for every natural n that its cast is zero exactly when 2 divides n. This is stronger than merely proving that the cast of 2 is zero.

The actual algebra now directly satisfies the characteristic hypothesis of the generic low-degree differential theorem. Every full degree-two boundary, including every actual bilinear coboundary, has zero degree-three differential on all algebra quadruples.

All four audits compile without warnings and use standard axioms. No field assumption, new table enumeration or homological realization is introduced.
