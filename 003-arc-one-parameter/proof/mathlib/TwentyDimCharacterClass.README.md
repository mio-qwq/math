# A nonzero full character-valued degree-three class

`TwentyDimCharacterClass.lean` proves that the actual f-character projection
of the specified cochain defines a nonzero class in the full scalar-valued
degree-three character cochain quotient whenever q³ is nonzero.

The boundary obstruction quantifies over every actual scalar-valued
R-bilinear map on the algebra. Its own basis values determine its two
internal faces by bilinearity. On the cycle triples the f characters of
the two endpoint basis vectors are zero, so both outer faces vanish.
The weighted cycle functional annihilates every such full boundary but
pairs with the projected cochain to q³. This proof does not infer scalar
nonboundary from the earlier vector-valued nonboundary result.

Full-input closure is an equality of actual four-linear scalar cochains.
The class lies in ker(d3)/im(d2) formed from all scalar multilinear
cochains and the full character endpoint actions. The class is nonzero
and the quotient nontrivial when q³ is nonzero. Over a ring without zero
divisors, q nonzero suffices, including every characteristic-two field.

Lean 4.34.1 compilation and independent replay passed without warnings.
Ten printed audits use only `propext`, `Classical.choice` and `Quot.sound`.
No `sorry`, added axioms or `native_decide` is used; exact hashes are in
the verification JSON.

No projective resolution, exactness or comparison with a separate Ext
construction is proved. The complete ARC realization and all-degree
claims remain open. The data keep their original source attribution.
