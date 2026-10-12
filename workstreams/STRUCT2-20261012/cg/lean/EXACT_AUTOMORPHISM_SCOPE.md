# Universal explicit automorphism family and exact 24n count

`CycleActions.lean` and `ModelActions.lean` complete the formal construction
and exhaustion of the original CG CDC automorphisms at **every odd n>=3**.
The result is an actual two-sided bijection with Fin(24*n), not just a
finite experiment, a cardinality assumption or the preceding upper bound.

## Explicit cyclic actions

For a cycle of length N=2m the index maps are

```
rotation(a,t)   = a+t mod N
reflection(a,t) = a-t mod N.
```

The supplied natural-number definitions use bounded additions/subtractions
with explicit wrap cases. Both rotation inverse laws, reflection
involutivity and the full cyclic-adjacency iff are proved symbolically.
`cycle_iso_dihedral` proves that **every actual cycle automorphism** for
m>=2 equals the explicit rotation or reflection selected by its image of
0 and its direction. It uses the already proved cycle rigidity theorem.

## Compatibility with actual centres

The central construction obligation is proved, for all coordinate indices:

```
residue(rotation(a,t))   = rotation(residue(a),residue(t))
residue(reflection(a,t)) = reflection(residue(a),residue(t)),
```

where the outer residue reduces the ring cycle of length 6n to the centre
cycle of length 2n. The equations cover all three residue blocks, endpoint
wraps and subtraction cases. No modular compatibility hypothesis remains
in the final parameter-family theorem.

`compatibleModelIso` then constructs actual adjacency automorphisms, checks
all sixteen ordered vertex-type pairs, and supplies both inverse laws.
The global ring-interchange bit either exchanges X/Y everywhere or fixes
both rings. Leaves take the ring action and centres take its proved
residue action. Rotations and reflections each give actual such objects.

`every_model_automorphism_dihedral` exhausts arbitrary actual model
automorphisms. The inverse identities between `automorphismCode` and
`parametersToAut` prove a bijection with

```
Fin(6n) x Bool(direction) x Bool(ring interchange).
```

In particular all 24n parameters exist, and no two parameters give the
same automorphism. No exhaustive graph-automorphism search is imported.

## Original-definition transfer and exact finite bijection

`modelAutToOriginal` and `originalAutToModel` conjugate in opposite
directions through the compiled original CDC/model isomorphism. Their
two-sided inverse laws are proved as equalities of actual automorphism
objects, including the inverse maps.

`packCode` is the proved injective index 4a+2d+s. `unpackCode` uses quotient
by four and the last two bits; both inverse identities are proved. The
original numerical encoding/decoding consequently satisfy

```
originalFiniteAutCode(originalNumericToAut(c)) = c
originalNumericToAut(originalFiniteAutCode(g)) = g.
```

The final bundled result is

```
Struct2.ModelActions.originalCDC_exact_24n
```

Its type is a `FiniteParametrization` of **all actual original CDC
automorphisms** by Fin(24*n), with both inverse laws, for every odd n>=3.
This establishes the exact automorphism count 24n. The n=1 source/model
isomorphism remains valid, but its extra automorphisms prevent this count;
that parameter is excluded from the exhaustion/count theorem.

## Actual verification

```
python verify_odd_cover.py --include-model-actions --lean /path/to/lean-4.34.1-linux/bin/lean --build-dir /tmp/struct2-model-actions-olean --output-dir /tmp/struct2-exact-automorphism-receipt
python check_model_actions.py --output /tmp/struct2-model-actions-checks.json
```

The nine-module dependency chain passed **130 printed axiom audits**, with
12 in CycleActions and 24 in ModelActions. No errors or warnings occurred;
only propext, Classical.choice and Quot.sound are used. No sorry, custom
axioms or native_decide occur. Exact source, compiler, driver, output and
olean hashes are recorded under
`../../verification/20261013-cg-exact-automorphisms/`.

The supplementary original-edge program checked 656 explicit actual
actions at n=1,3,5,7,9,31,101, testing every shift at n<=9 and the wrap
boundaries at larger orders. It verified distinct images, all original
adjacencies, residue compatibility and recovery of the parameters. It also
checked 62,424 numerical pack/unpack codes for all odd n<=101 and rejected
a damaged vertex permutation. The n=1 tested family is explicitly marked
as a proper subgroup. The program does not search all automorphisms;
universal exhaustion comes from Lean. This is an independent computational
implementation, not independent human review of the new formal sources.

## Remaining classification scope

The full explicit automorphism-family classification and exact count are
now formalized. The abstract composition/group-law identification with
D_(6n) x C2 has not separately been packaged as a Lean group isomorphism.
Exhaustive **strong-switch** conditions, their three conjugacy classes and
the final exactly-two TF-cousin Lean theorem remain to be proved. The
earlier all-odd written proof and its review retain their separate scopes.
Classical cycle and folding facts retain their existing attribution; this
module asserts no historical firstness or new human peer-review status.
