# Independent review of the support-10/11 joint-valuation theorem

**Accepted scope: complete written local theorem and its two exact-support
applications, independently checked by a separate AI agent.** Both four-word
sharpness fixtures also pass direct definition-based verification. This is not
human peer review, Lean formalization, exclusion of either support, a full
message witness, an improved global SHA-256 distance bound, or an originality
claim.

The author snapshot is `supports10-11-v4/manifest.json`, SHA256
`e85f54f94e7ca95271bd09f48a39814b509599eccb531a697b76a60912bb3dc5`.
All thirteen listed author files matched their frozen hashes. The proof is
`311d4c078d9a6bf55a2d35c2aae19ad6b7f07932ee83dcc3629ba938bb1ba1da`;
the certificate is
`4ff0e86e9c8273484b19f1bcca13e6570702088292a1dd6c3c69d3d5f08c699d`.
The author checker hash is
`4f01716c910584caff09407a717fc9606b2644550c5ff7564e254bfaa12bc9e6`.
These author files were read only. A later change requires a new review.

## Exact quantifiers

Work in `Z/(2^32)`, with the true SHA-256 small sigmas:

```
f(z)=ROTR7(z) xor ROTR18(z) xor SHR3(z),
g(z)=ROTR17(z) xor ROTR19(z) xor SHR10(z).
```

For **every** ordered actual word pair `X=(x,x')` with `x != x'`,
**every** actual pair `Y=(y,y')`, and **each** `m in {1,2}`, suppose

```
dY + F(X) = 0,
F(Y) + m*dX + G(X) = 0,
```

where `dX=x'-x`, `dY=y'-y`, `F(X)=f(x')-f(x)` and
`G(X)=g(x')-g(x)`, with analogous actual `F(Y)`. Then `dX` and
`E=m*dX+G(X)` are not both divisible by `2^16`.

Thus for an actual schedule pair whose **exact support** is frozen pattern
10 or 11, `min(v2(d18),v2(d34)) <= 15`. Both differences are nonzero
because these coordinates belong to the support. The theorem is universal
over arbitrary base words. It does not rely on a fixed additive difference,
a zero base, or freely chosen independent values for `d,F,G`.

## Independent reconstruction and complete coverage

The reviewer rebuilt all 48 rows directly from

```
R_t=d_t-G_(t-2)-d_(t-7)-F_(t-15)-d_(t-16), 16<=t<64,
```

then filtered by the pinned support JSON. Before reading the author's
checker, certificate or proof, the reviewer independently derived:

| Support | Local multiplier | Exact row combinations |
|---:|---:|---|
| 10 | 1 | `-R33=d26+F18`; `-R41=d34+F26`; `R34+R27+R20=d34-d18-G18` |
| 11 | 2 | First two combinations as above; `R34+R27+R20-R18=d34-2*d18-G18` |

Taking X at 18 and Y at 26 produces the two actual-pair equations. These
are integer row combinations, so no invalid division occurs in the word
ring. The author bridge rows and all three stored combinations subsequently
matched this independent reconstruction.

Assuming both dX and E vanish in the low 16 bits forces G(X) to do so.
Equality of the low 16 input or output bits is equivalent to vanishing of
the corresponding low XOR mask. Row-based Gaussian elimination over the
original direct-input and sigma-output matrices gives rank 31 and the
unique nonzero possible input XOR mask

```
K=44ab0000, f(K)=c81c272a, g(K)=e0110000.
```

Since `F(Y)=-E`, every possible Y XOR mask L belongs to the kernel of the
low 16 output rows of f. Those rows have rank 16. The independent checker
constructs a 16-element basis, checks its membership, and generates all
65,536 distinct combinations including zero. The author's different basis
generates **exactly the same full mask set**. No subset or solver-selected
sample is used.

Every additive difference with XOR mask B has the form
`sum_(i:B_i=1) (+/-1)*2^i` modulo `2^32`. Treating the signs of input and
sigma-output bits independently enlarges the real solution set. Therefore
failure of this relaxation is a valid necessary contradiction even though
actual signs are correlated. Both negative and positive bit contributions
are retained, and carry out of bit 31 is unrestricted.

The first equation's complete 65,536-mask scan leaves exactly five L:

| L | f(L) | First impossible bit for second equation, m=1 | For m=2 |
|---|---|---:|---:|
| 4804ddd6 | 92e50000 | 16 | 27 |
| 5804fff6 | d84d0000 | 16 | 24 |
| c814ddf6 | c3ef0000 | 16 | 27 |
| d805eee6 | ad090000 | 16 | 22 |
| d814ffd6 | 89470000 | 16 | 29 |

The second masks are `f(L),K,g(K)` for m=1 and
`f(L),2*K modulo 2^32,g(K)` for m=2. Doubling a signed word expression
shifts it one bit; the discarded bit-32 contribution is zero in the word
ring. All ten relaxed second equations are impossible. The independent
full failure histogram and these ten first-failure positions also match
the author's certificate.

## Different second checking algorithm

`check_independent.py` reconstructs the binary kernels by row RREF and
uses the signed-carry recurrence derived independently before author
comparison. Its mandatory checks use only Python's standard library.

The supplementary `check_subsets.cpp` uses **no carry propagation**. It
enumerates exact relaxed differences via

```
D(B)={B-2*s modulo 2^32 : s is a submask of B}.
```

For a candidate delta, membership in D(B) is decided by solving
`2*s=B-delta modulo 2^32`: an even right-hand side has exactly two
candidate s values, differing by `2^31`, and either must be a submask of B.
There are 4,096 distinct differences for f(K). For all 65,536 complete
kernel masks, direct difference-set membership leaves the same five L.
Enumerating the 128 input differences for K and 16 output differences for
g(K) independently excludes both second equations for all five. This
confirms the necessary relaxation by a different algorithm.

The C++ source and run output are supplied as supplementary evidence. Its
compiled binary is a local cache excluded by this directory's `.gitignore`
and is not part of the frozen review manifest.

## Actual local sharpness and limits

The four actual operands in each author fixture were recomputed with direct
rotations and shifts, without importing author code:

| m | x | x' | y | y' | v2(dX) | v2(E) | Both modular residuals |
|---:|---|---|---|---|---:|---:|---|
| 1 | 95d39b84 | f32d1b84 | f1110800 | 9d1f33a7 | 15 | 20 | 0, 0 |
| 2 | 54cd8023 | 32330023 | 56112dbb | 021f616a | 15 | 15 | 0, 0 |

These establish that the minimum-valuation threshold 15 is sharp **for
each stated two-pair core**. They do not show that either full support
can attain these values, since the other original recurrences and the
common base-message constraints remain unfulfilled. Consequently trying
to strengthen this same two-pair universal theorem to 14 is blocked by
actual counterexamples. Additional original constraints are necessary.

The inherited support classification and inherited global lower bound are
not re-proved in this review. This result does not exclude supports 10 or
11 and does not establish global distance 14. No SAT/SMT UNSAT result,
solver timeout, human review, Lean compilation or novelty search is a
premise or claimed outcome of this review.

## Reproduction and damage controls

From the repository root:

```
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/supports10-11-review-v4/check_independent.py --save
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/supports10-11-review-v4/compare_author.py --save
```

Both commands pass. `--save` writes only to this review directory; without
it the checkers are read only. `compare_author.py` reads author JSON as
data, validates all frozen file hashes, and recomputes the fixtures and
bridges from the independent definitions. It imports only the reviewer's
own checker, never author code.

The mandatory negative controls reject a missing, duplicate or nonkernel
mask, an absent active X coordinate, and twelve altered author-certificate
fields covering ranks, sigma definition, support bridge, carry conclusion
and fixture operands/interfaces. The carry implementation is additionally
compared with brute-force signed choices for all 512 three-bit mask
triples, including acceptance of legitimate modular overflow.

The supplementary submask checker independently passes 65,536
mask/residue membership controls and rejects missing, duplicate and
nonkernel packets. `RESULTS.json`, `AUTHOR_COMPARISON.json`,
`SUBSET_RUN.json`, and `RUN.json` record the actual outputs and source
hashes. The complete ordered independent kernel packet has SHA256
`be3982ccf8df75f8ddc5466ea86185e6f1213f0ea63b5c5d10a925752ae8650e`.
