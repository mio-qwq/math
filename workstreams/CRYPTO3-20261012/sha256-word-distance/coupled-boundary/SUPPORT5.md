# Application to the differently oriented support 5

Candidate corollary to the local theorem in `PROOF.md`, with a separate
original-recurrence check because this support is not a translated row
of the six-support table there. Independent review is recorded separately.

Use the same actual ring, sigmas and d/F/G definitions. The frozen support
number 5 is

```
{2,8,14,16,17,19,26,28,29,34,42,43,57}.
```

The following six original recurrence substitutions are exact:

| Recurrence t | Reduced equation |
|---:|---|
| 24 | 0=d17+d8 |
| 19 | d19=G17 |
| 26 | d26=d19 |
| 33 | 0=d26+d17 |
| 23 | 0=d16+F8 |
| 32 | 0=F17+d16 |

The first four give

```
d17=-d8=D != 0,
G17=d19=d26=-D.
```

The last two give F8=F17. Now orient the word pairs as follows:

```
q=W17, q'=W'17,
p=W'8, p'=W8.
```

Swapping the pair at index 8 negates both its input difference and its
sigma0 difference. Therefore

```
q'-q=p'-p=D,
g(q')-g(q)=-D,
f(p')-f(p)=-F8=-F17=-(f(q')-f(q)).
```

These are precisely the local theorem's premises. If 4096 divided D,
the theorem would give a contradiction. Hence **v2(d17)<=11** for every
actual expansion pair with this support. The earlier signed-power
theorem in `../LOCAL_PROOF.md` also shows D is not +/-2^k for any k.

No new equation below t=16 has been introduced. The reversed orientation
is explicitly accounted for in both derivatives; reversing only the
input difference would be invalid. Nonzero D follows from 17 being
active. There is no zero-base assumption or restriction on the other
initial words.

This adds support 5 to the six supports already covered by the same local
theorem, for a total of seven. It does not exclude support 5 completely,
reduce the count of unresolved supports, or improve the global distance
lower bound beyond 13. The exact support copy and source commit are the
ones pinned in `provenance.json`.
