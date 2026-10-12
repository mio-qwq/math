# Independent review of the fixed-K affine carry proof

## 1. Decision and exact version

**Accepted for the stated local theorem. No mandatory mathematical
revision was identified.** The frozen `coupled-short-proof/` package
provides a complete written reduction and a small finite certificate
for the nonexistence of arbitrary 32-bit words satisfying

    q' = q xor K,              K = fbca7000,
    q + g(q) = q' + g(q'),
    p' + q = p + q',
    f(p') + f(q') = f(p) + f(q),

with the actual SHA-256 small sigmas and all additions modulo `2^32`.
This proof of the fixed-K local theorem does not require the earlier
SAT, CNF, DRUP or RUP work. Those earlier artifacts were not changed.

The exact files reviewed are:

| Author file | SHA256 |
|---|---|
| `PROOF.md` | `7b3fa0d70c8bb03401e8c1e0223d778650dc806a46fcfac477d2dbd1c753b22b` |
| `CERTIFICATE.json` | `1428cce8b31378b67db8de32e4480bfedad608b0d62b0bee21742f3f09fa6389` |
| `check.py` | `71c12525b4938650984a9c87394dcc0fdf5f65e848ec1b606732cd20ff0d0d4d` |
| `RUNS.json` | `a6ef783ddf1ae1871fa96972bdb65ad6f7fc5fd3019707ff20861649f8c67f4d` |
| `SHA256.json` | `9b0a2bd7fced9e3f8ccaf72ed5fc57a88db00ded403215e9d87d4a9c532bd13b` |

All 12 files in the author's manifest were checked for byte length and
SHA256. The exploration scripts and their large matrix output were
hashed for version integrity but were not replayed or used as proof
premises. The result above concerns the proof, certificate and checker
at the exact hashes shown, not future edits to those paths.

This was a separate AI-agent mathematical review. It is not external
human peer review and not a proof-assistant formalization.

## 2. Independence of the reconstruction

The reviewer did not participate in discovering this short proof. Before
opening the author directory, the reviewer was given the exact local
problem, the proposed carry-to-affine mechanism, and the reported count
of 132 masks. The reviewer was therefore not blind to the proposed
outcome. The derivation, candidate generation and binary systems were
nonetheless rebuilt from the original word definitions before inspecting
the author's proof, certificate or implementation.

That first reconstruction was frozen in
`PRE-AUTHOR-CHECKPOINT.json`. In particular:

| Independent pre-author file | SHA256 |
|---|---|
| `RECONSTRUCTION.md` | `ebbb1cfa7adae8b53a3f294247f95c77e4d7c0ae990f7ad824112befc077901b` |
| `reconstruct.py` | `627d452dea94af1ad06b3df75e48553f0a1154414a6a6b9d8cbefb8dcb15db75` |
| `INDEPENDENT-CERTIFICATE.json` | `d18c1461f641f510a8b67187b110c91c9e47b2cf1ffd8e296a283058a9b76d72` |

The independent reconstruction retained explicit carry-sign variables,
with q in the low 32 variable positions and p in the next 32. The
author instead substitutes carry signs by base-bit expressions as it
walks the bits, using p before q. These are distinct implementations
of the same proved carry identities. The comparison explicitly accounts
for the reversed p/q variable order.

The independent computation generated all 132 contradictions before
reading the author package. Each contradiction XORs 4 to 13 original
affine rows to obtain `0=1`; it does not depend on a solver verdict.

## 3. The signed-carry equivalence is valid

For fixed masks a,b, write the signed-bit sum of two modular
differences as

    sum_i [a_i(1-2u_i)+b_i(1-2v_i)] 2^i.

If it vanishes modulo `2^32`, each lower partial sum is divisible by the
corresponding power of two. Its quotient is the incoming signed carry.
The absolute partial sum is less than twice that power, so every such
integer carry is in `{-1,0,1}`. At a bit i its parity must equal
`a_i xor b_i`. Consequently an even carry is zero and an odd carry has
one sign bit, represented by `1-2s_i`.

The independently derived transition table in `RECONSTRUCTION.md`
agrees with the author's table. For two active masks the next carry is
`1-u_i-v_i`; for one active mask it is `1-s_i-u_i`. Requiring an even
next carry forces the two Boolean arguments to differ. Requiring an
odd next carry forces them to agree and makes their common value the
next carry sign. These are affine conditions on the actual base bits.
No branching on independent sigma signs is introduced.

For the input-difference equality, negating the q difference must turn
the q sign bit into `q_i xor 1`. Both reconstructions implement this
complement. Replacing it by q_i would prove a different statement.

The outgoing carry after bit 31 is correctly unrestricted. The last
transition need only make the bit-31 sum even; telescoping then gives
an integer multiple of `2^32`. The independent checks accept both a
final carry of +1 and a final carry of -1 in genuine modular-sum
examples. An erroneous zero-final-carry condition is rejected.

The reviewer checked 96 explicitly oriented local table cases against
ordinary integer arithmetic. The author's 18 entries quotient some
irrelevant orientations and duplicate sign choices; they are consistent
with the same table. As a boundary check of the general lemma, all
4,096 combinations of two masks and two starting words at width three
give the same answer under the affine table and direct modular
subtraction. This small check supports the implementation; the general
equivalence follows from the preceding carry argument.

The bit matrices used in the independent affine systems were checked
against the original output-bit formulas, including 128 matrix columns
covering both sigmas and both p/q variable positions.

## 4. Necessary-mask coverage is complete

The fixed mask K has valuation 12. The equality `p'-p=q'-q` therefore
forces `A=p xor p'` to have low 12 bits zero and bit 12 one. The
independent pre-author computation used this larger universe of
`2^19=524,288` masks.

For a zero sum of two signed-mask derivatives, the necessary mask
condition is

    (a xor b) & ~((a or b) << 1) & ffffffff = 0.

It follows from the same carry table: a 00 mask pair cannot send an
odd carry into the next bit, and the initial carry is zero. Applying
it to `(A,K)` and `(f(A),f(K))` leaves exactly 132 masks in the
independent reconstruction.

The author additionally proves two fixed mask bits before enumeration.
Since `f(K)=828ee412` has valuation 1, the opposite sigma0 difference
has the same valuation. Hence `f(A)[0]=0` and `f(A)[1]=1`. With the
known low 12 zero bits, the original sigma0 output rows reduce these
to `A[18]=0` and `A[19]=1`. This argument is correct and leaves 17
free bits, including the unrestricted top bit.

The review independently regenerated that reduced parameterization:
131,072 masks initially, 24,576 after the input-mask screen, and 132
after the sigma0-mask screen. Its final set is exactly the larger
pre-author reconstruction's set. Thus the two additional fixed bits
discard no feasible original mask. The certificate partition and the
complete hexadecimal list in the written Appendix A were checked
against the same independent set, with neither omissions nor duplicates.

## 5. The 10 templates follow from original word equations

The certificate has 26 distinct base-bit rows and 10 templates, with
36 template-row occurrences. The family sizes are

    22, 27, 1, 37, 18, 4, 12, 6, 2, 3.

For each of the 132 masks and each of the three modular equations,
the reviewer eliminated only the explicit auxiliary carry variables
from the independently constructed affine system. The resulting
constraints on the original 64 word bits were compared with the
author's carry-sign substitution. All `132*3=396` pairs of affine
systems have identical solution sets: each row in either projected
system follows from the other. Each individual modular subsystem was
also checked to be consistent.

This last separation matters. Because the full coupled system is
inconsistent, its linear span would prove every possible binary row.
That would not independently verify the author's particular premises.
Instead, for each of the 384 template-row applications, the review
derives the selected author row from **one individual modular
subsystem** of the independent reconstruction. The explicit XOR of
original row indices is retained in `COMPARISON.json`, together with
the subsystem name and the original matrix hash. XORing those original
rows reproduces the selected 64-bit row and its right-hand side.

All 10 selected template sums are exactly `0=1`. The identities used
in families 6, 7 and 8 agree with the original sigma0 bit equation

    f(p xor q)[10] = (p xor q)[17]
                       xor (p xor q)[28] xor (p xor q)[13].

The nine displayed equations for family 9 cancel every base-bit
coefficient and have odd total right side. These template
contradictions and the complete mask partition prove the stated
fixed-K nonexistence result.

The author checker performs row membership and XOR checks without
Gaussian elimination. The independent review used finite binary
elimination to reconstruct and compare the systems, then checked its
explicit row combinations. Neither path invokes SAT/SMT or relies on
CNF, DRUP or RUP evidence.

## 6. Actual execution and damaged controls

The independent reconstruction, independent verification, frozen-author
comparison and frozen author checker were actually executed. The
commands, exit codes, source hashes and stored-output hashes are in
`RUNS.json`. Reproduction is read-only with respect to both packages.

| Check | Result |
|---|---|
| Independent necessary masks and original affine systems | 132 of 132 explicit contradictions |
| General carry table and modular boundaries | Passed |
| Author versus independent subsystem projections | 396 of 396 equivalent |
| Author template premises derived from individual original subsystems | 384 of 384 checked |
| Author templates and mask partition | 10 contradictions; all 132 masks covered |
| Independent damaged controls | 8 rejected |
| Comparison damaged controls | 4 rejected |
| Frozen author `check.py --negative` replay | Exit 0; all 14 author controls rejected |

The damaged controls cover omitted masks, corrupted matrix hashes or
row coefficients, removed or repeated XOR premises, altered right
sides, wrong sigma constants, wrong word-coordinate descriptions and
an incorrect zero-final-carry restriction. The author checker replay
matches its frozen recorded JSON output. The author files and all
pre-author checkpoint files retained their frozen hashes.

## 7. Accepted scope and remaining dependencies

The accepted theorem is the fixed-K local four-word exclusion. The
review does not assert that every h collision at some valuation has
this XOR mask; that needs its own complete mask classification.
Likewise, deriving these local equations from an actual message
schedule requires the separately stated recurrence bridges. This
package alone excludes no entire support and proves neither a
distance-14 lower bound nor a real distance-13 equality pair.

The generic carry criterion is not claimed as novel. The author's
historical attribution to Lipmaa--Moriai is recorded in its proof;
this review's acceptance is based on the self-contained mathematical
derivation and exact checks above, not on a separate historical
priority audit. No new literature-priority, complete-algorithm attack,
external peer-review or Lean claim is made.
