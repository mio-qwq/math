# All-odd original CG cover/model isomorphism

This is a universal Lean theorem for every odd natural n, hence n>=1.
It is not a theorem obtained by checking finitely many graph orders.
Lean 4.34.1, Std only; no sorry, custom axioms or native_decide.

## Actual source graph and leaf names

`Base n` has a ring indexed by Fin(6n), n claw centres and 3n leaves.
The ring type writes 6n as (3n)+(3n), exposing the antipodal halves.
`baseAdj` has only the original edge types:

- cyclic successor edges between ring vertices;
- a leaf of index a attached at ring positions a and a+3n;
- the leaf of index a attached to centre a mod n.

`leafIndex n i j` is i+n*j for the original i in Fin n, j in Fin 3.
`leafName` is its actual inverse (a mod n, a/n), with bounds proved in
Lean. Both inverse theorems are compiled. `centre_named_leaf` recovers
centre i. `original_ring_leaf_incidence` gives the exact two ring positions.
`cycleNext_is_mod` proves the cyclic successor is the original modulo-6n
successor, so it is not an unspecified cycle relation.

`coverAdj` requires opposite Boolean layers and this actual `baseAdj`.
Thus it is the original canonical double cover rather than a separately
assumed model graph.

## Proved synchronized graph isomorphism

`Coord n` contains X_t,Y_t,A_t for t in Fin(6n) and Z_s for s in Fin(2n).
Its adjacency has exactly the two cyclic rings, X_t--A_t--Y_t, and
A_t--Z_(t mod 2n). All other type pairs are nonadjacent.

The maps `toCover` and `fromCover` are mutually inverse for every odd n.
The half-shift parity reversal, residue/parity uniqueness, third-block
centre reduction and all boundary wraps are proved using natural arithmetic.
`toCover_adjacency` checks all sixteen ordered vertex-type pairs and
proves an iff with the original CDC adjacency; no graph-isomorphism
assumption or finite adjacency table is supplied as a premise.

The bundled result is:

```
Struct2.OddCoverIso.originalCDCModelIso
```

It is an actual `StrongFold.GraphIso` with forward/backward maps, both
inverse laws and full adjacency equivalence.
`originalCDC_deck_intertwining` proves that the original layer-flip deck
becomes the coordinate half-turn with the two rings exchanged. Its
adjacency preservation is also internally derived.

## Reproduce and inspect scope

```
python verify_odd_cover.py --lean /path/to/lean-4.34.1-linux/bin/lean --build-dir /tmp/struct2-olean --output-dir /tmp/struct2-cover-receipt
```

The driver sequentially compiles StrongFold, OddCoordinates and OddCoverIso,
checks every printed audit and records source/compiler/log hashes. The
documented host adapter is optional on ordinary systems. The new receipt
is in `../../verification/20261013-cg-cover/verification.json`.
The 37 audit outputs use only propext, Classical.choice and Quot.sound.

The n=1 coordinate isomorphism is valid. Its exceptional automorphism
group does not invalidate these coordinate statements. The six-cycle
type invariant and all-odd exact cousin classification require n>=3
and remain separate.

## Remaining universal classification

The source/model semantic bridge is now proved. The remaining universal
CG-specific tasks are the six-cycle type invariant at n>=3, the full
automorphism upper bound, the exhaustive strong
guide/conjugacy classification, and composition with the generic fold theorem
to obtain precisely three ordinary base isomorphism classes. Those are not
claimed by this module or its successful compilation.

Actual model/CDC connectedness, strong decks and original fold recovery
are subsequently proved in `ModelStructure.lean`; see
`MODEL_STRUCTURE_SCOPE.md` and its separate dependency-chain receipt.

The source definition and known companion constructions retain Mizzi's
attribution. The generic folding correspondence retains its classical
attribution. This module does not make a historical firstness or human
peer-review claim.
