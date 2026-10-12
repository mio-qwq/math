# Preserved v8 target-binding failure

The frozen `support12-full-factor-v8/` package is internally consistent but
is not a proof about support identifier 12.

It used

```
{10,11,15,18,20,26,27,28,29,34,42,43,57}=supports[11]
```

while labelling the certificate `support_index: 12`.  The independently
accepted object is the zero-based entry

```
supports[12]={10,11,13,15,18,20,26,28,29,34,42,43,57}.
```

Thus v8 made a `13 <-> 27` transcription/off-by-one object error.  Seven
rows change: `t=20,27,28,29,34,42,43`.  Its factor 27 is spurious and the
required factor 13 is absent.

All v8 internal checks passed because its generator, certificate and
checker shared the same mistaken `ACTIVE` constant, and the checker
explicitly asserted `supports[11] == ACTIVE`.  The wrong and correct objects
both happen to have 25 nonzero rows, 23 zero rows, integer rank 25 and free
rank 14.  Rank counts and mutation controls therefore could not distinguish
them.  The provenance file recorded reading the accepted support proof but
did not assert its active set against the certificate target.

The v8 directory is deliberately not modified.  Its manifest remains
SHA256

```
02a3729a66b7e474eb2abfeb33920160e2d60386f324ab5d4ef1b5c1e2bc0814.
```

V9 prevents recurrence by independently checking all of:

1. the identifier is explicitly zero-based and equals 12;
2. `supports-v2.json[12]` equals the certificate active set and entry 11
   does not;
3. the accepted actual-boundary proof contains the same exact set;
4. the base-lift structural JSON contains the same exact set;
5. the rejected v8 manifest is still byte-identical.

One negative control deliberately repeats the index-11 binding, and another
replaces position 13 by 27.  Both must be rejected.

