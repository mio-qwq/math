# Follow-up scope check after the local sigma results

Date: 2026-10-12. This is a narrow follow-up to `SOURCE_GATE.md`, not a
claim of historical novelty or a replacement for the remaining access
gaps recorded there.

The new objects are restrictions on an additive collision of
`x+sigma1(x)`, its compatibility with an opposite sigma0 derivative on
a second word pair, and their conditional application to seven fixed
13-word support patterns. These are neither linearized bit-weight
bounds nor reduced-step compression collisions.

Exact phrase searches included `"SHA-256" "word distance" "13"`,
`"SHA-256" "sigma" "modulo" "4096"`, and earlier searches involving
`"8192"`, `"additive"`, and `"carry"`. The returned material did not
supply a matching primary-source theorem. This is only a report of
those queries; absence of a matching search result establishes no
priority claim.

The latest publisher page for Li et al., *New Records in Collision
Attacks on SHA-2*, was reopened directly. It reports publication on
2026-07-27 and a 2026-09-22 affiliation correction. The abstract's
31-step SHA-256 collision and 39-step semi-free-start collision results
are distinct from this arbitrary-input, full-64-word schedule-distance
problem. Its full subscription text was not accessed.

Primary reference:
<https://link.springer.com/article/10.1007/s00145-026-09582-9>

The new finite contradiction uses standard gate encodings and reverse
unit propagation. This proof format and solver interface are prior
methods, documented by the original projects:

- <https://pysathq.github.io/docs/html/api/solvers.html>
- <https://github.com/marijnheule/drat-trim>

No novelty is claimed for signed carries, SAT encodings, DRUP/RUP
certificates, or the general practice of filtering a relaxed support
model through actual word constraints.

## Exact prior-art identification for the mask screen

The follow-up also directly inspected Helger Lipmaa and Shiho Moriai,
*Efficient Algorithms for Computing Differential Properties of Addition*,
FSE 2001. The IACR record identifies the current ePrint as the final
proceedings version and gives 2001-05-16 as the last of three revisions:

- <https://eprint.iacr.org/2001/001>
- Author-hosted full text: <https://kodu.ut.ee/~lipmaa/papers/lm01/dpa.pdf>

Algorithm 2 and Theorem 1 on PDF page 7 give an exact feasibility
condition for XOR differentials of modular addition. With zero output
XOR difference, their condition reduces to

```
(a xor b) & ~((a or b) << 1) = 0
```

on the retained word bits. To see the reduction directly, their equality
indicator on the preceding three mask bits, with the third mask zero,
is one precisely where the preceding a and b bits are both zero. The
remaining factor then tests the current a xor b bit. The initial missing
mask bits are zero, so the bit-zero condition is retained as well.

This is exactly the independent-sign feasibility screen used in the new
short proof. Its use here is a specialization of a classical condition,
not a new generic mask criterion. The new finite calculation additionally
keeps the signs coupled through the original sigma bit maps and proves
the specified SHA-256 local restriction. Historical priority for that
specific restriction is not established by this comparison.

The author's PDF formula was read visually because text extraction
corrupts mathematical glyphs. A further exact-phrase search for
`"SHA-256" "word distance" "sigma"` with a 365-day filter returned no
result. That narrow outcome is not evidence of nonexistence of prior
work. No contact with the authors or publication submission was made.
