# Selected three-pair exclusion for every odd q=33..63

Let `D=q*2^16`, and define the actual joint derivative image through

```text
F_D(x)=sigma0(x+D)-sigma0(x),
G_D(x)=sigma1(x+D)-sigma1(x).
```

The exact selected three-pair core asks for 32-bit words `x,y,z,A,T` with

```text
F_D(x)=A,       G_D(x)=T-D,
F_D(y)=A,       G_D(y)=T+D,
F_D(z)=-A,      G_D(z)=-T.
```

For each odd `q=33,35,...,63`, `generate.py` bit-blasts these equations using
the original rotations, shifts, modular additions and carries.  Every CNF has
1,259 variables and 9,683 clauses.  Glucose4 was used only to generate a
deletion-free DRUP trace.  `check.py` independently reconstructs the CNF with
the frozen standard-library circuit implementation and verifies every proof
addition by reverse unit propagation, ending in the empty clause.  All
sixteen checks pass; `CERTIFICATE.json` and `RUN.json` freeze exact digests,
proof lengths, runtime provenance and negative controls.

For negative D, replace every word `w` by `w+D` and negate `A,T`.  The
identities `F_{-D}(w+D)=-F_D(w)` and
`G_{-D}(w+D)=-G_D(w)` give a bijection between positive and negative core
solutions.  Hence UNSAT holds for both orientations.

Together with independently accepted Stage 9 evidence for odd q through 31,
this author result extends the finite selected-core exclusion candidate to

```text
D = +/- q*2^16, every odd q in 1..63.
```

The result is finite: the exact valuation-16 layer has positive odd quotients
through 32,767.  It is not a complete support-12 exclusion, not a message
pair result, not a proof of distance at least 14, and not Lean formalisation.

Replay the certificate with only Python's standard library:

```sh
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-v16-core-q33-63-v10/check.py
```
