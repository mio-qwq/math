# Independent reconstruction of the coupled SHA-256 boundary

This reconstruction was written from the standard SHA-256 small-sigma
definitions and the three supplied equations, before reading any file in
`coupled-boundary/`. The reported CNF/proof sizes and claimed UNSAT result
were already communicated; no claim of ignorance of that result is made.

Let all words lie in (R=\mathbb Z/(2^{32})), with bit 0 least significant,
and put (C=\mathtt{0xfbca7000}). Let

\[
f(x)=\operatorname{ROTR}_7(x)\oplus\operatorname{ROTR}_{18}(x)
       \oplus\operatorname{SHR}_3(x),
\quad
g(x)=\operatorname{ROTR}_{17}(x)\oplus\operatorname{ROTR}_{19}(x)
       \oplus\operatorname{SHR}_{10}(x).
\]

These are FIPS 180-4 equations (4.6) and (4.7), respectively:
<https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf>.
The isolated question is whether arbitrary (p,p',q\in R), with
(q'=q\oplus C), can satisfy

\[
q+g(q)=q'+g(q'),\tag{A}
\]
\[
p'+q=p+q',\tag{B}
\]
\[
f(p')+f(q')=f(p)+f(q).\tag{C}
\]

Every equality is in (R). No base word is fixed to zero. No requirement
is imposed on a discarded carry out of bit 31. No actual schedule support
is inferred from this isolated question.

Writing Δ=q'-q, (B) gives (p'-p=Δ), while (A) and (C) require

\[
g(q')-g(q)=-Δ,\qquad
f(p')-f(p)=-\bigl(f(q')-f(q)\bigr).
\]

This subtraction is valid modulo (2^{32}), without sign, valuation, or
integer-overflow assumptions. Since (C\ne0), (q'\ne q); therefore
Δ is nonzero and (B) also forces (p'\ne p).

## Independent Boolean encoding

`reconstruct.py` allocates 96 free input bits for (p,p',q). The bits of
(q') are literal complements of the corresponding (q) bits exactly
where (C) has a 1. Each sigma output bit is an explicit three-input XOR
gate with its shifted source indices. Six independent ripple additions
encode the two sides of (A), (B), and (C). A full-adder sum is three-input
XOR and the next carry is Boolean majority. The carry out of bit 31 is
not allocated. The two output words of each equality are equated bitwise.

Each gate's CNF is constructed from its complete truth table: for each
input valuation, one clause requires the correct output. Thus a gate is
equivalent to its Boolean function, including signed and repeated input
literals. Gate order is acyclic. Induction along this order gives a unique
gate extension for every free input assignment. The usual full-adder
identity, (a+b+c=s+2c_{next}), proves the encoded addition modulo
(2^{32}) by induction on bit position. Consequently this independent
CNF is satisfiable if and only if (A)–(C) have a solution.

The program also evaluates its gate graph and compares all six sums with
a separate direct integer implementation on deterministic nonzero input
fixtures and sigma basis inputs. These are bounded encoding controls,
not a proof of unsatisfiability. A separate solver result is only a cross
check; the intended proof review will validate the discoverer's CNF
mapping and the complete RUP certificate after this reconstruction is
frozen.
