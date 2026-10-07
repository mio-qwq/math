# The full five-term scalar character cochain

`TwentyDimFCharacterSparse.lean` proves that the attributed actual
f-character trilinear cochain, on arbitrary full inputs x,y,z, equals

```text
q² x₆ y₁₁ z₄ + q² x₆ y₄ z₁₉ + q x₁₉ y₆ z₄
  + q x₁₅ y₂ z₄ + q³ x₆ y₂ z₁₇.
```

The subscripts are the zero-based coordinate labels of the installed
twenty-coordinate basis. R is any commutative characteristic-two ring
and q is arbitrary. In particular, parameters can be zero and R can
have zero divisors.

The proof first checks a finite auxiliary certificate: filtering output
coordinate 8 in the original sparse table gives exactly the five listed
branches for all 8,000 finite basis-input triples. This is a Nat/List
statement proved by Lean `decide`, with kernel checking and no
`native_decide`. A general list-induction lemma shows that this filtering
preserves the actual polynomial output coefficient.

Ring-homomorphic specialization gives the q², q and q³ coefficients.
The existing full trilinear contraction then collapses symbolically to
those five terms on arbitrary algebra inputs. No original table branch
is changed, and the frozen four-input closure certificate is reused.
The finite auxiliary check and the resulting full-input semantic theorem
are separate proof steps.

The exact source hash, compilation, independent replay and printed
audits are recorded in the verification JSON. Replay in this folder:

```powershell
.\verify-cohomology.ps1 -Targets TwentyDimFCharacterSparse
```

This is a full-input formula for the already specified cochain. It is
not a classification of the entire cohomology or Ext group.
