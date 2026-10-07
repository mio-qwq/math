# Odd half-order power Hadamard rigidity

For every odd integer `m >= 3`, we prove that a complex matrix of order `2m` whose entrywise powers `1,...,m-1` are all complex Hadamard becomes an `m`th-root matrix after dephasing. In fact, its row differences give a generalized Hadamard matrix over the cyclic group of order `m`, with multiplicity two. This is an exact characterization, not a numerical observation.

- [Full theorem, definitions, and proof](paper.md)
- [Exact finite example checker](code/check_examples.py)

The proof extends the order-six support argument in OpenAI's *Exact Fourier certificates for complex Hadamard matrices of order six*, at pinned upstream commit [`adc7f1241b42e322a6451854ab7e4b4c146bf78a`](https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a). The general odd-half-order theorem, the projection argument, and the cyclic-group characterization are proved here. We make no claim of historical priority.

Run the dependency-free finite checker with Python 3:

```sh
python code/check_examples.py
```

It checks a positive example at `m=3`, the even-half-order counterexample `F_4`, and the failure of the hypothesis for `F_6` when its square is included. It uses polynomial arithmetic over the integers modulo cyclotomic polynomials, with no floating-point values. These checks validate the displayed examples; the all-parameter theorem is proved analytically in `paper.md`.

The exponent range `1,...,m-1` is sufficient. No minimality claim about that range is made. The order-four example shows that oddness cannot simply be removed from the theorem as stated.
