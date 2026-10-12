# New valuation-18 finite exclusions

`PROOF.md` excludes the eight new odd representatives
`D=q*2^18`, q=1,3,5,7,9,11,13,15, in the actual three-pair
support-12 core. Combined with `width-reduction-v5` and the unchanged
`support12-v4` proof, this gives **v2(D)<=17** for supports 12,6,7,13.

Author replay passes all 12,245 new twin mask pairs, 612 third-pair
mask tests, and 1,253 distinct XOR contradiction receipts. Independent
acceptance is separate. No complete support is excluded and no new
global distance bound or actual message pair is claimed.

```sh
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-extension-v5/check.py
```

The standard-library checker explicitly pins and reuses the v4 finite
proof kernel. SMT discovery observations are retained but not used as
proof premises. `manifest.json` freezes this directory without modifying
any v4 artifact.
