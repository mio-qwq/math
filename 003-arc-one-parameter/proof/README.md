# Lean kernel certificates for the fixed finite tables

The files here use **Lean 4.34.1 and Std only**. The proofs use ordinary
`decide`, whose proof terms are checked by Lean's kernel. They do not use
`sorry`, added axioms, `native_decide`, or a compiler-trust axiom.
`#print axioms` reports the dependencies of each main theorem; standard
`propext` occurs in some reductions.

## Verified first stage: `FiniteCore.lean`

```console
lean 003-arc-one-parameter/proof/FiniteCore.lean
```

Run from the repository root with its pinned `lean-toolchain`.

The file defines the complete ten-letter table for `C`, with basis order
`e,x,y,z,u,v,t,j,f,n`. Coefficients are natural-number bit sets: bit `i`
represents the coefficient of `q^i` over `F_2`. Its recursively defined
`pMul` is carryless polynomial convolution. Eight bits per output basis
coordinate are used to pack a finite vector.

The kernel proves the equality of the packed left and right products on
**every one of the 1000 basis triples**, verifies all output basis labels,
checks the left-path composed coefficient bound `<256`, and checks
`utu=(1+q)v` and `utut=(q+q^2)z` in this representation. The additional
right-path bound is included in the subsequent certificate when available.

**Formalization boundary:** these are equalities about the explicit Lean
definitions of bit-polynomial computations and packed vectors. This first
file does not construct the abstract ring `F_2[q]`, a scalar-extension
interpretation into arbitrary fields, a Lean algebra instance, or the
homological ARC construction. Its theorem is not a formal proof of the
complete Auslander--Reiten counterexample. The finite mathematical meaning
and upstream provenance are discussed in `../paper.md` and
`../ATTRIBUTION.md`.

The data source is OpenAI family 199 at commit
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`. The Lean table was transcribed
from the fixed `../data/arc-core.json`; its corresponding source hashes
are recorded there.

## Verified second stage: `FiniteCoreT.lean`

`FiniteCoreT.lean` proves the packed associativity identities on all **8000
twenty-letter basis triples**, both left-path and right-path coefficient
bounds `<256`, all output-label bounds, both actions of `e+f`, and the
complete **400-entry trace pairing**. The pairing equals one precisely
when the second letter is the star-dual of the first. It also proves that
the explicit fast table matches the specified dual-ideal recurrence on
all 400 input pairs, and supplies the missing right-path coefficient bound
for the first ten-letter table.

Compile the imported certificate first. From the repository root, a
PowerShell invocation is:

```powershell
$env:LEAN_PATH = (Resolve-Path '003-arc-one-parameter/proof').Path
lean -o 003-arc-one-parameter/proof/FiniteCore.olean 003-arc-one-parameter/proof/FiniteCore.lean
lean 003-arc-one-parameter/proof/FiniteCoreT.lean
```

The `.olean` build output is ignored by Git. This second stage has the
same explicit bit-polynomial scope and the same limits as the first.

## Verified third stage: `CochainData.lean`

This file contains the complete 179-entry cochain definition and verifies
its entry count and correspondence to the source rows. It checks output
labels and coefficient bounds on all 8000 possible basis triples, bounds
all algebra coefficients, and verifies that multiplying two coefficients
smaller than 16 fits in an eight-bit block. It also proves the concrete
cycle's internal differential is zero and its pairing is exactly `q^3 f`.
These are **finite certificate identities**, not a formal Ext or
cohomology statement.

Its imports require compiled `FiniteCore.olean` and `FiniteCoreT.olean`
in the proof directory. With `LEAN_PATH` set as above:

```console
lean -o 003-arc-one-parameter/proof/FiniteCoreT.olean 003-arc-one-parameter/proof/FiniteCoreT.lean
lean 003-arc-one-parameter/proof/CochainData.lean
```

## Verified fourth stage: `CochainBoundary.lean`

For all 324 radical input pairs, the kernel checks **both** the constant
coefficient and linear coefficient in `H` of the twisted boundary
identity. The definitions include every radical basis index in the sum;
there is no specialization of `q` or `H`. The theorems assert the exact
bit-polynomial coefficient identities, with the same limits on field and
homological interpretation.

Compile `CochainData.olean` first, then run
`lean 003-arc-one-parameter/proof/CochainBoundary.lean` with the same
`LEAN_PATH`.

## Source-data cross-check

`python 003-arc-one-parameter/proof/check_transcription.py` independently
compares the Lean corner tables, every nonunit `C` product, all 179 cochain
match clauses, and the `pEntries` list against the pinned JSON input. This
cross-check passed. It checks provenance and transcription; it does not
replace the kernel proofs or supply an arbitrary-field interpretation.

## Verified final stage: all 104976 Hochschild four-words

`CochainClosure0.lean`, `CochainClosure1.lean`, and
`CochainClosure2.lean` contain six first-index cases each. Every case checks
all `18^3` possibilities for the other three radical letters. **All three
files compiled successfully**, including all 18 case theorems. No
noncomposable words were filtered out. The final imported file
`CochainClosure.lean` proves the single full statement

```lean
theorem hochschild_closure_all :
    ∀ a b c d : Fin 18,
      hochschildClosure (radicalIndex a) (radicalIndex b)
        (radicalIndex c) (radicalIndex d) = 0
```

Its `#print axioms` output is exactly `[propext]`; it has no `sorryAx` or
compiler-trust dependency. Its coefficients are the exact explicit
bit-polynomial representation. The formal theorem does **not** construct
a Hochschild complex over an abstract field or identify this computation
with a formal arbitrary-field Ext statement. That semantic bridge and
the complete ARC homological realization remain outside this certificate.

## Replay the entire Lean certificate

From the repository root, with Lean 4.34.1 selected:

```powershell
& '003-arc-one-parameter/proof/verify.ps1'
```

If `lean` is not on `PATH`, supply the installed executable:

```powershell
& '003-arc-one-parameter/proof/verify.ps1' -LeanExecutable 'C:/Users/Administrator/.elan/bin/lean.exe'
```

The script builds each imported `.olean` from its public source and fails
on any nonzero Lean exit status. It temporarily sets `LEAN_PATH` to this
directory and restores the previous value afterward. It uses only Std,
no Mathlib download or binary proof shortcut. The three closure blocks
are independent after their prerequisite files have been compiled and
can also be replayed in three parallel processes before compiling the
final importing file. The largest blocks take materially longer than
the small table checks.

## Additional scalar semantics in pinned Mathlib

The separate [Mathlib scalar package](mathlib/README.md) now proves an injective interpretation of the natural-number bit codes as actual polynomials over `ZMod 2`, and proves that the frozen `pMul` corresponds to polynomial multiplication for every input. It adds a genuine scalar semantic bridge. The eight Std files above continue to state their exact packed-computation certificates; the packed-vector interpretation and the formal algebra/Hochschild/Ext constructions remain separate work.
