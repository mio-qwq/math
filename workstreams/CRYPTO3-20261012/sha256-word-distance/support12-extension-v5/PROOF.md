# Excluding the new valuation-18 layer of the irregular support core

**Complete finite proof with author replay; independent-agent acceptance
is separate.** Together with the exact width lemma and the frozen v4
proof, this yields the necessary ceiling **v2(D)<=17** for supports
12,6,7,13. It does not exclude any complete support, improve the global
distance lower bound 13, or construct actual message blocks.

## 1. Hypotheses and retained dependencies

For three actual 32-bit word pairs X,Y,R, let d denote the modular
input difference and F,G their actual SHA-256 sigma0,sigma1 differences.
The exact core is

    d(X)=d(Y)=D!=0, d(R)=-D,
    F(X)=F(Y)=F(R),
    G(Y)-G(X)=2D, G(Y)-G(R)=D.                         (1)

All additions are modulo N=2^32. Both sigmas act on the same actual
members of each pair. The original recurrence combinations and support
orientations are proved and hash-frozen in `../support12-v4/PROOF.md`;
there D is respectively `d18=d34`, `d19=d35`, `d21=d37`, `d20=d36`
for support indices 12,6,7,13.

The separately supplied `../width-reduction-v5/PROOF.md` proves that
`2^18 | D` in (1) forces exactly the residue list

    D = +/- q*2^18 mod N, 1<=q<=15.                     (2)

At valuation 18, sigma1 output bits 22..30 do not change. Its top-bit
contribution is the same half-word modulo N in all three pairs, so it
cancels in the two gaps. This is essential; an ordinary full-output
width bound without that cancellation would be invalid.

The even q values in (2) are precisely the values excluded in v4:
`q=2k`, `1<=k<=7`, gives `D=k*2^19`. This stage does not rerun those
old finite cases. It excludes only the eight new odd positive values.
The negative values follow by simultaneously reversing all three
actual pairs, which negates every d,F,G in (1) and preserves (1).

## 2. Finite proof for the eight new representatives

The input and output carry method is fully described in
`../support12-v4/PROOF.md`, Section 3. For clarity its exact logical
obligations remain:

* Enumerate every high quotient of `(x,x+D)` and of `(r,r-D)`; quotient
  classes are checked to equal their complete binary cubes. Lower input
  bits remain arbitrary and input carry wraparound is included.
* For each actual XOR mask alpha and linear map L, its derivative bit
  is `(u xor L(alpha)_j)-u`, where u is the original L output bit.
  Each derivative equality is branched over all Boolean assignments
  and all their integer next carries. Each local truth table is checked
  to equal its compressed binary affine equations.
* All f and g equations use the same original 32 bits per word. They
  are accumulated over F2 with explicit XOR receipts for contradictions.
  The final output carry is unrestricted, exactly as equality modulo N
  requires.

For each odd q, apply `F(Y)=F(X)` and `G(Y)-G(X)=2D` to all positive
mask pairs, retaining *every* surviving affine branch. For each such
branch, enumerate *every* negative-difference mask of R and impose
`F(R)=F(Y)` and `G(Y)-G(R)=D`. Every final branch is empty.

| q | D (hex) | Positive masks | Negative masks | Two-mask cases | Twin branches | Third masks tested | Final branches |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | 00040000 | 14 | 14 | 196 | 0 | 0 | 0 |
| 3 | 000c0000 | 25 | 25 | 625 | 0 | 0 | 0 |
| 5 | 00140000 | 35 | 35 | 1225 | 6 | 210 | 0 |
| 7 | 001c0000 | 34 | 34 | 1156 | 0 | 0 | 0 |
| 9 | 00240000 | 43 | 43 | 1849 | 0 | 0 | 0 |
| 11 | 002c0000 | 53 | 53 | 2809 | 0 | 0 | 0 |
| 13 | 00340000 | 52 | 52 | 2704 | 3 | 156 | 0 |
| 15 | 003c0000 | 41 | 41 | 1681 | 6 | 246 | 0 |

`CERTIFICATE.json` includes all 12,245 new two-mask cases and all 612
third-pair mask tests. It stores 1,253 distinct explicit XOR-of-row
contradictions. The full definition-based reconstruction traverses
2,696,541 Boolean carry edges and detects 12,370 binary conflicts.
The counts are replay evidence; the exhaustive truth tables, complete
mask coverage and exact row contradictions are the proof premises.

Thus the eight new odd representatives in (2) are impossible. V4
excludes the even representatives. Therefore (1) is impossible when
`2^18 | D`, and every actual pair on the four specified supports has
`v2(D)<=17`.

## 3. Byte binding, replay, and limits

The checker explicitly reuses the author definition-based v4 kernel,
and checks its file SHA256 before executing it:

    check.py: b159cb1a0190bc9d85062b30415ef55461b098ee2c6bf9ce522e7e5b34a55fff
    v4 manifest: 3f8fab844410d88aebc26afed62a186553e9127b4196424d334be6831698acdc

It only memoizes pure output-row evaluations; no transition, constraint,
or final-carry interpretation changes. It does not import either the
SMT probe or its outputs. Before checking it reconstructs the new
certificate in full from all new quotients and original bit rows and
compares every case and every XOR receipt.

```sh
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-extension-v5/check.py
```

Only the Python standard library is required for proof replay. The
eight recorded fixed-D SMT UNSAT answers are discovery observations
only; they are not premises and are never treated as certificates.
The `finite_discovery.py` files likewise document discovery, not an
additional theorem dependency. The author replay does not constitute
independent-agent acceptance; that requires a separately frozen receipt.

The width lemma's exact proof and checker hashes are recorded in
`AUTHOR-RECEIPT.json`. The v4 files remain unchanged. No fourth-pair
constraint is needed in this new exclusion. Nothing asserts that the
remaining valuation<=17 triples exist, that any 13-pair assignment
lifts to one genuine base expansion, or that a complete support has
been excluded. No Lean, historical-priority, hash-attack, DOI, Release,
or main-branch integration claim is made.
