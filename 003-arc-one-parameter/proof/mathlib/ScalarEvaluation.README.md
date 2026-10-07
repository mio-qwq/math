# Specialization in every commutative characteristic-two ring

`ScalarEvaluation.lean` evaluates the decoded `Polynomial (ZMod 2)` at an arbitrary parameter q in an arbitrary commutative ring R with `CharP R 2`. This includes characteristic-two fields. The canonical map from `ZMod 2` and polynomial evaluation supply the interpretation; no new semantic axiom is assumed.

For all natural-number codes, XOR becomes ring addition, the frozen `pMul` becomes ring multiplication, and doubling the code becomes multiplication by q. Codes zero, one and two evaluate to zero, one and q. Byte-vector evaluation preserves coordinatewise XOR addition and interprets every coefficient below 256 in precisely its assigned coordinate.

Evaluation need not preserve distinctions or nonzero values. The file explicitly proves that evaluation at q=0 identifies codes zero and two and is not injective. The theorem transports the encoded identities; it does not establish that a specialized cycle pairing remains nonzero, construct a Hochschild complex, or prove the complete ARC realization.

All thirteen printed audits contain only the standard three axioms, and the file compiled successfully in the pinned package. The source hash is recorded in `ScalarEvaluation.verification.json`.

After the BytePacking prerequisites:

```sh
lake exe cache get Mathlib/Algebra/Polynomial/Eval/Defs.lean
LEAN_PATH=.:.. lake env lean ScalarEvaluation.lean
```

Use semicolon-separated absolute `LEAN_PATH` entries on Windows as in [BytePacking.README.md](BytePacking.README.md). The local imported modules must be built from their supplied public sources.
