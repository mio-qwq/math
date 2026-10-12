# Support-12 factor-signature v9

This package proves two negative research results about the accepted corrected
ten-scalar/thirteen-factor normal form.

1. All thirteen factors are simultaneously satisfiable in the exact low-26
   quotient with `b=00010000`, using a real 32-bit pair per factor.  Therefore
   even same-mask joint `(v2(d),v2(F),v2(G))` constraints plus exact scalar
   addition valuations cannot eliminate the valuation-16 layer.
2. Factors 34 and 43 have an exact full-32-bit joint witness at
   `b=bfbf0000`, whose valuation is 16.  Their anti-symmetry alone is not an
   obstruction to the whole layer.

Replay:

```sh
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-factor-signature-v9/check.py --negative
```

The witness statements are complete and standard-library checked but have not
yet received independent-agent review.  They are not a full factor solution
and not a pair of SHA-256 messages.
