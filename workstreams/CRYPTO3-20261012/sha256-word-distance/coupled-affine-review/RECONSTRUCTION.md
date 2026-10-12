# Independent reconstruction before reading the short-proof package

The exact problem is the existence of 32-bit words q,q',p,p' with

    q' = q xor K, K = fbca7000,
    (q'-q) + (g(q')-g(q)) = 0,
    p'-p = q'-q,
    (f(p')-f(p)) + (f(q')-f(q)) = 0

in Z/(2^32), with the original SHA-256 small sigmas. No base-message
assumption is made. This reconstruction is performed from that problem
definition before inspecting the discoverer's short-proof files.

## General signed-carry equivalence

For two fixed XOR masks a,b, let u_i,v_i be the actual first-word
output bits. The zero sum of the corresponding two signed modular
differences is equivalent to

    C_0=0,
    2*C_(i+1) = C_i+a_i*(1-2*u_i)+b_i*(1-2*v_i)

for bits 0 through 31, with no restriction on C_32. Every reachable
integer carry is in {-1,0,1}. Its parity is necessarily
e_i=a_i xor b_i. Thus e_i=0 forces C_i=0, while e_i=1 allows the
representation C_i=1-2*s_i with one Boolean sign variable s_i.
Necessarily e_0=0.

For every bit i<31, the following table is exact:

| a_i,b_i | e_(i+1) | Required affine equations |
|---|---|---|
| 0,0 | 0 | none |
| 0,0 | 1 | contradiction |
| 1,1 | 0 | u_i xor v_i = 1 |
| 1,1 | 1 | u_i xor v_i = 0; s_(i+1) xor u_i = 0 |
| exactly one 1 | 0 | s_i xor w_i = 1, where w_i is the active sign bit |
| exactly one 1 | 1 | s_i xor w_i = 0; s_(i+1) xor s_i = 0 |

At bit 31 the parity e_31 is already imposed by the preceding row.
There is no equation constraining the outgoing carry. In particular,
adding a zero-final-carry condition would incorrectly strengthen the
original modular equation.

For an equation in which a difference is subtracted, replace that
difference's first-word sign bit u_i by u_i xor 1. Both signs and all
carry equations remain affine in the original word bits and the carry
sign variables.

## Complete necessary-mask screen

With the sign bits temporarily independent at each position, the table
has a solution exactly when

    (a xor b) & ~((a or b) << 1) & ffffffff = 0.          (M)

This includes e_0=0. It excludes precisely an odd incoming carry whose
preceding mask pair is 00. Along a run of odd carries, a freely chosen
sign at the preceding 11 position propagates unchanged; at an even
carry the displayed table supplies allowed sign bits. Thus (M) is also
sufficient in this temporary independent-sign model.

For the actual problem let A=p xor p'. Equality of nonzero modular
differences gives v2(A)=v2(K)=12. Enumerate exactly the 2^19 masks with
low 12 bits zero and bit 12 one, then retain only masks satisfying (M)
for (A,K) and for (f(A),f(K)). These are necessary conditions for the
original problem, not assumptions that the signs are independent in
the final linear system.

For every retained A, the final system uses the three exact zero sums

    delta(q) + delta(g(q)),
    delta(p) - delta(q),
    delta(f(p)) + delta(f(q)).

Their signs are the actual original q and p bits or their original
sigma output bits. A binary elimination contradiction will be recorded
as an explicit XOR of original affine rows equal to 0=1. The table,
mask screen and all row combinations are to be checked separately.
