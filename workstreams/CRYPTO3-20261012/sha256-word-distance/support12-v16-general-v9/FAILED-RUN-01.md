# Failed certificate run 01

Command:

```sh
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-v16-general-v9/check.py --negative --write-certificate
```

Pre-fix checker SHA-256:
`dbba3c65fe32ad9e0cf8ae5022a7ddbacce42a37b708d0abe3e91a25c536291b`.

After about 197 seconds the run raised:

```text
ValueError: bit31 boundary control unexpectedly empty
```

The classification had completed, but the harness imposed an extra,
unjustified assertion that at least one excluded q must have a low-31
survivor.  `PRECOMMIT.md` requires only that such cases, if present, are
not confused with full 32-bit survivors.  No certificate was written.
The repair deletes only the nonemptiness assertion; it does not change
the class traversal, bit equations, survivor test, or certificate schema.

