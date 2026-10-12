# Uniform dyadic width screen

The complete author lemma reduces every exact valuation k=10,...,18
of the actual irregular three-pair core to

    D=+/-q*2^k+h*2^(k+14) mod2^32,
    q odd 1..2^(22-k)-1, h=0..2^(18-k)-1.

The new shared-term estimate also works at k=10. Both lifts and full
pair reversal are retained. There is no new exclusion of all these
representatives or of an entire support. Independent acceptance is
recorded separately, and the global word-distance bound remains 13.

```sh
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/dyadic-width-v7/check.py
```
