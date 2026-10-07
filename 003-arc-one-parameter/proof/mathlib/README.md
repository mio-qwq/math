# Genuine scalar polynomial semantics

`BitPolynomial.lean` connects the exact scalar operations imported from the frozen `../FiniteCore.lean` to `Polynomial (ZMod 2)` for **every natural-number code**, rather than a bounded test range.

The decoder assigns bit `i` to the coefficient of `X^i`. Lean proves:

- the decoder is injective;
- decoding XOR is polynomial addition;
- decoding twice a code is multiplication by `X`;
- with sufficient fuel, `pMulAux` is genuine polynomial multiplication;
- `decode (pMul a b) = decode a * decode b` without a bound on either input;
- consequently the encoded scalar multiplication is associative and commutative on all natural numbers.

All six printed axiom audits report only `propext`, `Classical.choice` and `Quot.sound`. The source compiled successfully with Lean 4.34.1 and the pinned Mathlib commit, without `sorry`, added axioms or `native_decide`.

This completes the **scalar** semantic bridge. It does not yet decode the eight-bit packed vectors, identify the finite multiplication table with a formal algebra instance, construct a Hochschild complex, or establish arbitrary-field Ext or the complete ARC realization. The eight Std certificates keep their original, separately documented scope. Associativity of the scalar polynomial operation also does not by itself prove associativity of the twenty-dimensional table.

The additional [BytePacking bridge](BytePacking.README.md) now supplies generic eight-bit coordinate extraction, coordinatewise XOR addition, and the exact interpretation of a single packed coefficient under its explicit `<256` bound. It does not yet interpret all table sums or construct an algebra instance; those are subsequent layers.

[TermSemantics](TermSemantics.README.md) supplies the next generic layer: arbitrary sparse-list sums, scaled sums and left/right triple products become actual polynomial vectors, with the necessary bounds on every composed coefficient. A formal finite algebra instance and the complete homological construction remain separate.

## Replay

From this directory, obtain the selectively cached Mathlib modules and compile the imported Std source:

```sh
lake exe cache get Mathlib/Algebra/Polynomial/Coeff.lean Mathlib/Data/ZMod/Basic.lean Mathlib/Tactic/Ring.lean
lean -o ../FiniteCore.olean ../FiniteCore.lean
LEAN_PATH=.. lake env lean BitPolynomial.lean
```

PowerShell equivalent for the last step:

```powershell
$previousLeanPath = $env:LEAN_PATH
try {
    $env:LEAN_PATH = (Resolve-Path '..').Path
    lake env lean BitPolynomial.lean
    if ($LASTEXITCODE -ne 0) { throw 'Lean rejected the scalar bridge.' }
} finally {
    $env:LEAN_PATH = $previousLeanPath
}
```

The package pins Mathlib, Lean and transitive dependency revisions. `.olean` and `.lake` outputs remain ignored. The bit-polynomial source data are attributed in `../../ATTRIBUTION.md`; this bridge is an additional proof about our publicly defined checker operations, using Mathlib's established polynomial and binary-digit facts. No historical priority claim is made.
