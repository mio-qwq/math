# Precise-version independent local review

## Decision and scope

The two local theorems in the reviewed `LOCAL_PROOF.md` are supported by
an independent reconstruction from the standard sigma1 definition and
by independently rebuilt small finite certificates:

- `h(x)=h(y)` and `x=y mod 8192` imply `x=y`.
- No pair whose additive difference is a signed power of two can
  collide under `h(x)=x+sigma1(x) mod 2^32`.

The local modulus threshold is sharp: the discoverer's pair and a
different, independently found pair both have equal `h`, equal low
12 bits, and unequal low 13 bits. This review is an independent AI
review, not external human peer review. Project integration and any
claim of historical novelty remain separate questions. No Lean result
is claimed.

The exact reviewed proof has SHA256
`608752c21bbdc43ad5540a3b7f34ce1e2f55c0531df66864b68aa6c53943598b`.
`REVIEW_RECEIPT.json` binds it to the exact constructor, checker,
certificate, source support bytes, and prior actual run record.
Subsequent modifications are not covered merely because their filename
is unchanged.

## Order and independence of the work

The reconstruction began with the definition
`sigma1(x)=ROTR17(x) xor ROTR19(x) xor SHR10(x)` and the two statements.
The discoverer's proof, mechanism files, code, and certificate were not
read before the independent finite certificate and written argument
were completed. `RECONSTRUCTION.md` records that boundary. Only then
were the precise discoverer files read and compared.

The independent checker uses output-bit indexing for sigma1, column
elimination of the full low-input/low-output map, and a local necessary
mask obstruction derived from signed carries. It also checks that
obstruction by separate reachable-carry propagation. The discoverer
constructor uses integer rotations, row elimination, and carry-state
propagation. The kernel bases differ; comparison shows that the same
63 masks, their full sigma1 images, and their first impossible carry
bits occur in both implementations. Code was not imported from the
discoverer to establish this agreement.

Both power-of-two proofs independently reduce an additive increment
to a contiguous XOR interval. All 528 input intervals leave the same
single interval-image exception, and both wrap-boundary pairs reject
that exception directly. No UNSAT or timeout result is used as a proof.

## An additional independently reconstructed boundary classification

The low-12 kernel has dimension eight and 255 nonzero masks. Exactly
one survives the proved necessary signed-carry obstruction:

```
x xor y = fbca7000,
sigma1(x) xor sigma1(y) = sigma1(fbca7000) = 763e9000.
```

Thus every distinct local collision with equal low 12 bits has this
XOR difference. This is a necessary classification and is not a count
or parametrization of actual collisions. The full 255 rows are frozen
in `independent_certificate.json`, together with all 63 low-13 cases.
`INDEPENDENT_PROOF.md` supplies the mathematical reduction and scope.

The independently found boundary pair is
`cd027f2a / 36c80f2a`, with common `h=3d45fee8` and additive difference
`69c59000`. It was found before the discoverer's pair was supplied.
The discoverer's distinct pair `5d130376 / a6d97376` was subsequently
recomputed independently and has common `h=3ed5a561` and additive
difference `49c67000`. Both XOR differences are the required mask.
Each is a local two-word example; neither is a pair of expanded
16-word messages.

## Conditional schedule bridge check

After the blind reconstruction, the six conditional bridges in
Section 5 of the discoverer's proof were checked from the original
recurrence lag list against the supplied frozen support bytes. For
indices `0,1,2,4,8,9`, all 18 restricted recurrence identities are
correct, all claimed shared differences are nonzero under exact support,
and all recurrence indices lie in `[16,63]`.

This verifies an application of the local theorems conditional on
each listed support. It does not re-establish completeness of the old
15-support classification, does not rerun the old potential certificate,
and does not prove that any listed support is attainable or impossible.
The global distance lower bound is not raised by this review.

## Actual verification

`INDEPENDENT_RUN.json` records exit code zero for the independent
certificate build and check, including eight rejected damaged controls.
`COMPARISON_RUN.json` records exit code zero for the exact-version
comparison. That comparison also ran the discoverer's pinned checker
with `--negative`; it exited zero and rejected all eleven controls.
The latter is an actual rerun in addition to the independent comparison,
not a substitute for it. Both used Python 3.12.14.

From this directory:

```
python -B check_independent.py --selftest
python -B compare_discoverer.py
```

The first verifies the frozen independent certificate. The second
requires every discoverer hash listed in its source to match the
reviewed bytes, and writes a fresh exact-version receipt with actual
run timing. It does not edit the discoverer's files. `SHA256.json`
lists all files in this review package except itself.
