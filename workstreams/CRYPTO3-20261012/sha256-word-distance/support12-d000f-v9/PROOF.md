# Fixed `D=000f0000`: selected core exclusion

Status: **complete author certificate; independent AI acceptance is pending**.

## Statement

All arithmetic below is in `Z/(2^32)`.  Put

```text
F_D(w) = sigma0(w+D) - sigma0(w),
G_D(w) = sigma1(w+D) - sigma1(w),
A      = F_D(x),
T      = G_D(x) + D.
```

For `D=0x000f0000`, there are no 32-bit words `x,y,z` satisfying

```text
F_D(y) = A,       G_D(y) = T+D,
F_D(z) = -A,      G_D(z) = -T.                 (1)
```

This is stronger than the requested fixed-`D` selected four-pair
exclusion.  That four-pair criterion is (1) together with the existence
of a word `u` satisfying `F_A(u)=D`.  Since (1) itself is impossible, the
additional reciprocal condition cannot restore a solution.

This theorem is only about this fixed `D` and this selected local system.
It is not an exclusion of the complete support-12 factor graph, not a
support-12 theorem, and not a statement about actual SHA-256 message
blocks or distance 13/14.

## Exact Boolean encoding

`generate.py` builds `fourpair.cnf`; despite the historical filename, the
CNF contains exactly the stronger necessary three-pair core (1).

The word functions are the SHA-256 small sigmas

```text
sigma0(w) = ROTR^7(w) xor ROTR^18(w) xor SHR^3(w),
sigma1(w) = ROTR^17(w) xor ROTR^19(w) xor SHR^10(w).
```

Every XOR is encoded by its complete local truth table.  Every modular
addition uses a 32-stage ripple-carry adder with carry-in zero and ignored
final carry.  Therefore it is addition modulo `2^32`; no integer or XOR
surrogate is used.  Word equalities use the two binary implication clauses
at every bit.

The frozen formula has:

```text
variables  1259
clauses    9683
SHA-256    f16a99ee064edc1d95e7a248af07262bfd2ddd4c605dd5a1ec8d7587aa727a08
```

`check.py` does not import the generator.  Its separately written circuit
builder reconstructs all 9,683 clauses and requires exact equality of the
parsed clause sequence before checking the proof.

## Certificate

Glucose4 as bundled by `python-sat 1.9.dev15` produced an UNSAT trace.
The generator removed 1,469 deletion commands and retained 3,951 clause
additions.  This is sound because retaining a clause rather than deleting
it can only strengthen the active database.  The resulting artifact is a
deletion-free DRUP proof:

```text
fourpair.drup SHA-256
1256df91a4d7d82865b39743943450f0adfdb2875c98cb55c4b1d8c1c68a7210
```

The standard-library checker verifies every addition by reverse unit
propagation and requires the last addition to be the empty clause.  It
checked all 3,951 additions and returned `PASS`.

The proof-producing native module is frozen by digest in
`CERTIFICATE.json`.  It is not part of the trusted checking base: replaying
`check.py` needs only Python's standard library, the frozen CNF, and the
frozen DRUP trace.

## Controls and failure boundary

The following independently evaluated assignment satisfies every core
identity except the last `G_D(z)=-T` equation:

```text
x = 5ff2e1be       y = 5ff2e1a6       z = 9ff20041
A = 398179ec       T = a000e3b9
G_D(z) = 5ff1e3b9  -T = 5fff1c47
```

Thus removing that final equation gives a concrete SAT near-miss; the
checker recomputes all six identities directly from 32-bit word functions.
It also rejects a trace with the final empty clause removed and detects a
one-byte mutation of the CNF by digest.

The original one-shot QF_BV `UNSAT` observation is not used as evidence.
The accepted author-side evidence is the frozen CNF, the independently
reconstructed formula, and the fully replayed deletion-free DRUP trace.

