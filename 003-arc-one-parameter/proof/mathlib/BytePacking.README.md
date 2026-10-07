# Generic eight-bit coordinate bridge

`BytePacking.lean` imports the frozen scalar bridge and proves that the certificate's eight-bit packing has genuine coordinate semantics. All statements hold for arbitrary natural-number codes and coordinate indices; no new finite enumeration is used.

- `byte code i := (code / 2^(8*i)) % 2^8` extracts the allocated coordinate.
- `byte_xor` proves that extraction commutes with XOR.
- `byte_pack` proves `byte (pack j c) i = if i = j then c else 0`, with the explicit necessary hypothesis `c < 256`.
- `decodeVec` decodes each extracted byte as a `Polynomial (ZMod 2)`.
- `decodeVec_xor` identifies packed XOR with coordinatewise polynomial addition.
- `decodeVec_pack` identifies a packed coefficient with precisely one polynomial coordinate, under the same byte bound.

The proof of `byte_pack` checks every bit: bits above the byte vanish, a lower coordinate precedes the packed block, and a higher coordinate reads bits at least eight positions above the coefficient's first bit. The bound `c < 256` makes those latter bits zero. Thus neighboring-coordinate overlap is explicitly excluded.

`decodeVec` is a function `Nat → Polynomial (ZMod 2)`. This file does not supply a finitely supported vector structure, a finite-dimensional algebra instance, a Hochschild complex, or the complete ARC realization. The already proved left and right composed coefficient bounds can be used in the next layer to transfer the finite table equalities to actual polynomial vectors.

The four printed axiom audits contain only the standard axioms `propext`, `Classical.choice`, and `Quot.sound` (the first uses only `propext` and `Quot.sound`). No `sorry`, new axioms, `native_decide`, or compiler-trusted decision procedure is used. The underlying source tables and operations are attributed in `../../ATTRIBUTION.md`. No priority claim is made.

## Replay

Use Lean 4.34.1 and the package's pinned Mathlib revision. From this directory, after obtaining the cached dependencies and compiling `../FiniteCore.lean` as described in the scalar README:

```powershell
$priorLeanPath = $env:LEAN_PATH
try {
    $env:LEAN_PATH = ((Get-Location).Path + ';' + (Resolve-Path '..').Path)
    lake env lean -o BitPolynomial.olean BitPolynomial.lean
    if ($LASTEXITCODE -ne 0) { throw 'Scalar bridge rejected.' }
    lake env lean -o BytePacking.olean BytePacking.lean
    if ($LASTEXITCODE -ne 0) { throw 'Byte bridge rejected.' }
} finally {
    $env:LEAN_PATH = $priorLeanPath
}
```

The two `LEAN_PATH` entries retain both the local scalar module and the imported frozen Std module. Compilation artifacts remain ignored.
