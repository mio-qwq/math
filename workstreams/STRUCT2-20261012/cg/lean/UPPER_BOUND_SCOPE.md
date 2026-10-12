# Universal actual-automorphism upper bound

`RingAction.lean` and `CycleRigidity.lean` close the automorphism **upper
bound** step for the original CG canonical double cover at every odd n>=3.
Their inputs are arbitrary actual adjacency automorphisms with genuine
inverse maps. Type preservation and a complete permutation list are not
assumed; the preceding six-cycle theorem supplies the former.

## Synchronized rings

`leafImage` is the actual index of the image of A_t. It is bijective, with
an inverse obtained from the actual inverse graph automorphism. Adjacency
to A_t forces the images of X_t and Y_t to have this same index. Injectivity
forces them into opposite rings. Adjacency between consecutive X vertices
then forces the ring-interchange bit to be constant on the whole ring.
Its constancy is proved by induction on the index, not finite BFS.

`inducedRingIso` is an actual adjacency automorphism of the cycle of length
6n, with both inverse laws. `centre_forward` determines the image of Z_s
from the ring index of the leaf with index s. Thus
`every_automorphism_synchronized` determines **every vertex image** from the
single induced cycle action and one global interchange bit.

## Rigidity and a finite encoding

The generic cycle lemma proves that an arbitrary cycle adjacency
automorphism is uniquely determined by the images of indices 0 and 1.
The induction uses the two-neighbour property and injectivity to exclude
backtracking. It applies to every cycle of length 2m with m>=2.

The image of 1 has only two possible orientations relative to the image
of 0. A Boolean `direction` records which one occurs. Consequently the
CG model automorphism is uniquely encoded by

```
(image of index 0 in Fin(6n), direction : Bool, ring interchange : Bool).
```

`packCode` encodes this triple as 4a+2d+s and proves injectivity. The final
model result is an injective map into **Fin(24*n)**. The graph-isomorphism
extensionality lemma identifies actual automorphism objects, including
their inverse maps; it does not merely identify a restricted test set.

`originalAutToModel` conjugates an arbitrary original CDC automorphism
through the already proved original graph isomorphism. The final theorem

```
Struct2.CycleRigidity.originalCDC_automorphism_embeds_in_24n
```

proves that the explicit `originalFiniteAutCode` into Fin(24*n) is injective
for **every odd n>=3**. This is a formal finite embedding giving
|Aut(CDC(CG(n)))| <= 24n. The n=1 exceptional group is excluded.

## Verification and remaining scope

```
python verify_odd_cover.py --include-ring-rigidity --lean /path/to/lean-4.34.1-linux/bin/lean --build-dir /tmp/struct2-ring-olean --output-dir /tmp/struct2-upper-bound-receipt
```

The seven-module dependency rebuild passed **94 printed axiom audits**:
12 in RingAction and 11 in CycleRigidity. No errors or warnings occurred.
The dependency chain uses only propext, Classical.choice and Quot.sound;
the two new model-only layers use propext and Quot.sound. Exact source,
driver, compiler and output hashes are under
`../../verification/20261013-cg-upper-bound/`.

This proves the full universal **upper bound**, but not by itself the
matching parameter-family construction or the isomorphism
Aut(CDC(CG(n))) = D_(6n) x C2. Those constructions are established in the
written proof and finite original-definition checks, with their earlier
review scope. Formal construction of every code, explicit group laws,
exhaustive strong-switch/conjugacy classes and the exactly-two TF-cousin
Lean theorem remain to be completed. No new independent human review is
claimed for these supporting formal layers.
