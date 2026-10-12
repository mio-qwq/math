# Full active-pair feasibility at the coupled boundary

This question is recorded before computation. For representative support 5,
can **all 48 original difference recurrences** hold on 13 independent,
unequal, actual 32-bit word pairs when the already derived common difference
`D=d17=-d8` has valuation exactly 11?

The previous four-word coupling has a valuation-11 witness, so its ceiling
cannot improve by itself. The new query retains every active pair and every
early and late difference recurrence for this support. It identifies no word
pairs, fixes no base word, and does not impose periodicity or fixed XOR masks.
All sigma values are computed on the actual pair supplying each derivative.

Subtracting the original recurrence is encoded without subtraction: move
primed active output and unprimed active inputs to one modular sum, and
unprimed active output and primed active inputs to the other. Inactive terms
cancel because their two base words agree. This is precisely the complete
independent-active-pair necessary model, not the full base expansion.

One deterministic Glucose3 run has a 50,000-conflict and 45-second limit.
SAT must be checked by direct evaluation of all 48 difference equations.
UNSAT requires an independently checked RUP proof before it supports a lemma.
Unknown ends this bounded mechanism; its budget will not be extended.
Any SAT object still needs a genuine base completion before it is a pair of
messages. The query alone cannot settle attainability at distance 13.

The standard recurrence is NIST FIPS 180-4, sections 4.1.2 and 6.2.2.
The support bytes are inherited from CRYPTO2 commit
`80b71cb3b6a67c8f8aae80d9cd8b6ed87d74bd51`. Generic SAT and carry methods are
established tools; no priority, hash attack, or Lean claim is made here.
