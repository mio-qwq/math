#!/usr/bin/env python3
"""Exact checks of the finite examples in paper.md.

No dependencies or floating point. This script checks examples; it is not
the proof of the infinite theorem. Polynomials use low-to-high coefficients.
"""

from collections import Counter


def trim(poly):
    poly = list(poly)
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def divmod_monic(numerator, denominator):
    """Integer polynomial division by a monic integer polynomial."""
    numerator, denominator = trim(numerator), trim(denominator)
    assert denominator[-1] == 1
    quotient = [0] * max(1, len(numerator) - len(denominator) + 1)
    while len(numerator) >= len(denominator) and numerator != [0]:
        shift = len(numerator) - len(denominator)
        coefficient = numerator[-1]
        quotient[shift] = coefficient
        for index, value in enumerate(denominator):
            numerator[index + shift] -= coefficient * value
        numerator = trim(numerator)
    return trim(quotient), numerator


def cyclotomic(order):
    """Compute Phi_order from X^order-1 by exact monic divisions."""
    assert order >= 1
    polynomial = [-1] + [0] * (order - 1) + [1]
    for divisor in range(1, order):
        if order % divisor == 0:
            polynomial, remainder = divmod_monic(polynomial, cyclotomic(divisor))
            assert remainder == [0]
    return polynomial


def root_sum_is_zero(exponents, root_order):
    coefficients = [0] * root_order
    for exponent in exponents:
        coefficients[exponent % root_order] += 1
    return divmod_monic(coefficients, cyclotomic(root_order))[1] == [0]


def root_matrix_is_hadamard(exponents, root_order, power=1):
    """Check row AND column orthogonality exactly at a primitive root."""
    size = len(exponents)
    assert size > 0 and all(len(row) == size for row in exponents)
    for matrix in (exponents, list(zip(*exponents))):
        for first in range(size):
            for second in range(first):
                differences = [power * (a - b) for a, b in
                               zip(matrix[first], matrix[second])]
                if not root_sum_is_zero(differences, root_order):
                    return False
    return True


def uniform_row_differences(exponents, modulus, multiplicity):
    expected = Counter({residue: multiplicity for residue in range(modulus)})
    for first in range(len(exponents)):
        for second in range(first):
            differences = Counter((a - b) % modulus for a, b in
                                  zip(exponents[first], exponents[second]))
            if differences != expected:
                return False
    return True


def fourier_exponents(size):
    return [[row * column % size for column in range(size)]
            for row in range(size)]


def main():
    if not __debug__:
        raise RuntimeError("Run this checker without -O: its checks must remain enabled.")
    # These literal polynomials independently fix the arithmetic convention.
    assert cyclotomic(3) == [1, 1, 1]
    assert cyclotomic(4) == [1, 0, 1]
    assert cyclotomic(6) == [1, -1, 1]

    cubic = [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 1, 2, 2, 1],
        [0, 1, 0, 1, 2, 2],
        [0, 2, 1, 0, 1, 2],
        [0, 2, 2, 1, 0, 1],
        [0, 1, 2, 2, 1, 0],
    ]
    assert all(entry == 0 for entry in cubic[0])
    assert all(row[0] == 0 for row in cubic)
    assert uniform_row_differences(cubic, 3, 2)
    assert uniform_row_differences(list(zip(*cubic)), 3, 2)
    for power in (1, 2):
        assert root_matrix_is_hadamard(cubic, 3, power)
    print("PASS: cubic order-six example has uniform differences and both powers.")

    f4 = fourier_exponents(4)
    assert root_matrix_is_hadamard(f4, 4)
    # Its (1,1) entry is zeta_4; its square is zeta_4^2=-1 != 1.
    assert 2 * f4[1][1] % 4 != 0
    assert f4[0][0] == f4[0][1] == f4[1][0] == 0
    print("PASS: F4 is dephased Hadamard and violates m=2 root rigidity.")

    f6 = fourier_exponents(6)
    assert root_matrix_is_hadamard(f6, 6, 1)
    assert not root_matrix_is_hadamard(f6, 6, 2)
    assert 3 * f6[1][1] % 6 != 0
    assert [(2 * entry) % 6 for entry in f6[0]] == [
        (2 * entry) % 6 for entry in f6[3]]
    print("PASS: F6 shows why k=1 alone is insufficient at m=3.")
    print("All finite example checks passed using exact integer arithmetic.")


if __name__ == "__main__":
    main()
