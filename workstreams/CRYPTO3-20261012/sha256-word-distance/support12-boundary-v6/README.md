# Valuation-17 support-core exclusion

The complete written finite proof in `PROOF.md` excludes the 32
positive representatives `D=q*2^17+h*2^31`, odd q=1..31, h=0 or1,
in the actual three-pair SHA-256 core. Together with accepted v4/v5
dependencies, it gives the necessary ceiling **v2(D)<=16** for
supports 12,6,7,13. Independent acceptance is separate.

All cases retain the original arithmetic modulo2^32; modulus2^31
appears only in the written screening lemma. The 32 lossless xz
certificates include 111,718 twin mask cases, 7,068 third-mask tests,
and 10,914 explicit XOR row receipts.

```sh
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-boundary-v6/check.py
```

The standard-library checker pins and reuses the frozen v4 finite
proof kernel. Solver observations are retained solely as discovery.
No entire support is excluded; global word-distance bound13 remains
unchanged, and no real message blocks are supplied.
