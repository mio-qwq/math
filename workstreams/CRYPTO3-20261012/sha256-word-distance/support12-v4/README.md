# Support-12 valuation improvement

The complete written finite proof in `PROOF.md` strengthens the
necessary bound for supports 12,6,7,13 from `v2(D)<=20` to
`v2(D)<=18`. This does not exclude any complete support or improve
the global distance bound 13.

`CERTIFICATE.json` includes every one of the 3,389 twin mask cases,
the remaining 32 third-pair masks, and 512 XOR contradiction receipts.
`check.py` rebuilds these cases from original input quotients and
Boolean carry truth tables, checks 28 original recurrence combinations,
and independently evaluates the four-word positive twin control.
This author replay passed; independent-agent review belongs in a
separate receipt and is not assumed by this header.

```sh
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-v4/check.py
```

The discovery files are supplementary and are not imported by the
proof checker. `manifest.json` freezes all files in this directory
except the manifest itself. No solver, external package, or Lean
installation is needed for replay.
