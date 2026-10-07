# The low-degree differential composite

`HochschildLowDegrees.lean` defines the full four-term degree-two and five-term degree-three formulas on an actual associative ring. In characteristic two it proves that their composite is zero on every four inputs. The cancellation identity itself holds even for an arbitrary two-input function: expanding the formulas gives ten pairs, which cancel by associativity and characteristic two.

For an actual bilinear map over a commutative base ring, the degree-two formula is proved trilinear and packaged as three nested linear maps. Its degree-three differential therefore vanishes as well.

All three audits compiled without warnings. The raw cancellation theorem uses only `propext`; the packaged linear-map results also use `Quot.sound`. No finite table computation or added axiom is used. This establishes one actual differential-composition law; it does not construct all degrees of a cochain complex or identify the previously displayed radical-span cochain with a cohomology class.
