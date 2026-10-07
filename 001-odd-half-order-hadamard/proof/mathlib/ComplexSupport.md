# Actual complex support phases

`ComplexSupport.lean` connects the abstract four-phase lemma in `../Support.lean` to actual complex numbers. Cancellation is instantiated on the subtype of nonzero complex numbers, with multiplication and its closure proved from the complex field laws.

For nonzero complex `x,y`, both different from `1`, if the list `[1,x,y,x*y]` has at most two distinct values, the file proves `x=y=-1` and `x*y=1`. In row-ratio notation, at most two values in `[1,phi,psi⁻¹,phi*psi⁻¹]`, for nonzero `phi,psi` different from `1`, force both `phi` and `psi` to equal `-1`.

It also proves that the actual complex value `1` has weighted multiplicity exactly `2*t` in the four classes with multiplicities `t,m-t,m-t,t`. For every odd `m`, this count cannot equal `m`. These theorems quantify over arbitrary inputs satisfying their displayed hypotheses; they are not bounded numerical checks.

The file compiled with Lean 4.34.1 and Mathlib commit `d13f23b723b8a846827a245b89c10fc7d3f11612`. All four printed axiom audits contain only `propext`, `Classical.choice`, and `Quot.sound`. There are no added axioms, `sorry`, or `native_decide` proofs.

The derivation of the at-most-two hypothesis and the four multiplicities from the original Hadamard matrix remains outside this file. In particular, this is not yet a complete formalization of the main rigidity theorem.

From this directory, after obtaining the already documented Mathlib cache:

```sh
lean -o ../Support.olean ../Support.lean
LEAN_PATH=.. lake env lean ComplexSupport.lean
```

For PowerShell, set `LEAN_PATH` to the absolute `../` proof directory before the second command. The imported `Support.olean` is an ignored build artifact; the public source remains `../Support.lean`.
