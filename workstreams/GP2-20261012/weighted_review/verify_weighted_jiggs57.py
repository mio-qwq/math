#!/usr/bin/env python3
"""Independent exact algebra review of the literal Jiggs 57-word template.

Python standard library only. No floating-point arithmetic, imported discovery
code, graph-distance oracle, or claim about maximum dictionaries is used.
Run from any directory; optional --negative-controls tests deliberate damage.
The two pinned hashes identify the exact dictionary and candidate reviewed.
"""

from __future__ import annotations

import argparse
import copy
from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
WORD_SHA256 = "26d405621e125016c26edf662bd1d18cb721bb6b09976c421fa5093e531a1f14"
CANDIDATE_SHA256 = "6f1068bd29261ac4eea4cfc11b9392593900580498d087f3f7856cf04d334918"
ALPHABET = "ABCD"
FIXED_WEIGHTS = {"A": 5, "B": 5, "C": 3, "D": 3}
SCHEMA = "GP2-20261012-weighted-jiggs57-exact-review-v1"


class Rejected(Exception):
    pass


def require(condition, message):
    if not condition:
        raise Rejected(message)


class Poly:
    """Sparse exact multivariate polynomials with Fraction coefficients."""

    def __init__(self, n, terms=None):
        self.n = n
        self.terms = {}
        for powers, coefficient in (terms or {}).items():
            require(len(powers) == n and all(type(e) is int and e >= 0 for e in powers),
                    "invalid monomial")
            coefficient = Q(coefficient)
            if coefficient:
                self.terms[tuple(powers)] = coefficient

    @classmethod
    def const(cls, n, value):
        return cls(n, {(0,) * n: Q(value)})

    @classmethod
    def variable(cls, n, index):
        powers = [0] * n
        powers[index] = 1
        return cls(n, {tuple(powers): 1})

    def coerce(self, other):
        if not isinstance(other, Poly):
            return Poly.const(self.n, other)
        require(other.n == self.n, "incompatible polynomial variable counts")
        return other

    def __add__(self, other):
        other = self.coerce(other)
        terms = dict(self.terms)
        for powers, coefficient in other.terms.items():
            terms[powers] = terms.get(powers, Q(0)) + coefficient
        return Poly(self.n, terms)

    __radd__ = __add__

    def __neg__(self):
        return Poly(self.n, {powers: -c for powers, c in self.terms.items()})

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        other = self.coerce(other)
        terms = {}
        for a, ca in self.terms.items():
            for b, cb in other.terms.items():
                powers = tuple(x + y for x, y in zip(a, b))
                terms[powers] = terms.get(powers, Q(0)) + ca * cb
        return Poly(self.n, terms)

    __rmul__ = __mul__

    def __pow__(self, power):
        require(type(power) is int and power >= 0, "invalid polynomial power")
        result = Poly.const(self.n, 1)
        for _ in range(power):
            result = result * self
        return result

    def __eq__(self, other):
        other = self.coerce(other)
        return self.terms == other.terms

    def substitute(self, replacements):
        require(len(replacements) == self.n, "wrong substitution arity")
        target_n = replacements[0].n
        require(all(p.n == target_n for p in replacements), "inconsistent substitutions")
        result = Poly.const(target_n, 0)
        for powers, coefficient in self.terms.items():
            term = Poly.const(target_n, coefficient)
            for p, exponent in zip(replacements, powers):
                term = term * (p ** exponent)
            result = result + term
        return result

    def derivative(self, variable):
        terms = {}
        for powers, coefficient in self.terms.items():
            if powers[variable]:
                smaller = list(powers)
                smaller[variable] -= 1
                terms[tuple(smaller)] = coefficient * powers[variable]
        return Poly(self.n, terms)

    def evaluate(self, point):
        require(len(point) == self.n, "wrong evaluation arity")
        result = Q(0)
        for powers, coefficient in self.terms.items():
            term = coefficient
            for value, exponent in zip(point, powers):
                term *= Q(value) ** exponent
            result += term
        return result

    def records(self):
        return [{"powers": list(e), "coefficient": str(c)}
                for e, c in sorted(self.terms.items())]


def from_records(n, records):
    terms = {}
    for term in records:
        e = tuple(term["powers"])
        require(e not in terms, "duplicate monomial in certificate")
        terms[e] = Q(term["coefficient"])
        require(terms[e] != 0, "noncanonical zero coefficient in certificate")
    p = Poly(n, terms)
    require(p.records() == records, "noncanonical certificate polynomial")
    return p


def univariate(coefficients):
    return Poly(1, {(i,): Q(c) for i, c in enumerate(coefficients)})


def coefficients(p, degree):
    require(p.n == 1, "univariate coefficients requested from multivariate polynomial")
    require(all(e[0] <= degree for e in p.terms), "unexpected polynomial degree")
    return [str(p.terms.get((i,), Q(0))) for i in range(degree + 1)]


def rotations(word):
    return tuple(word[i:] + word[:i] for i in range(4))


def canonical(word):
    return min(rotations(word))


def density(words):
    p = Poly.const(4, 0)
    for word in words:
        monomial = tuple(word.count(letter) for letter in ALPHABET)
        p = p + Poly(4, {monomial: 1})
    return p


def exact_lift(words, weights):
    """Actual-letter choices, including every adjacent-equality correction."""
    q = Poly.variable(1, 0)
    total = Poly.const(1, 0)
    per_word = []
    for word in words:
        term = weights[word[0]] * q
        for i in range(1, 4):
            term = term * (weights[word[i]] * q - int(word[i] == word[i - 1]))
        total = total + term
        per_word.append({"word": word, "coefficients_ascending": coefficients(term, 4)})
    return total, per_word


def check(raw_words, candidate_bytes, cert, emit=print):
    require(cert["schema"] == SCHEMA, "unsupported certificate schema")
    require(hashlib.sha256(raw_words).hexdigest() == WORD_SHA256,
            "dictionary SHA256 does not match the reviewed literal input")
    require(cert["binding"]["dictionary_sha256"] == WORD_SHA256,
            "certificate dictionary SHA256 does not match the trusted pin")
    require(hashlib.sha256(candidate_bytes).hexdigest() == CANDIDATE_SHA256,
            "candidate SHA256 does not match the reviewed statement")
    require(cert["binding"]["candidate_sha256"] == CANDIDATE_SHA256,
            "certificate candidate SHA256 does not match the trusted pin")
    require(cert["binding"]["alphabet_order"] == list(ALPHABET),
            "alphabet order binding changed")
    require(cert["binding"]["candidate_algebra_sections"] == [3, 4, 5],
            "candidate review scope changed")
    words = raw_words.decode("ascii").split()
    require(len(words) == len(set(words)) == 57, "dictionary does not have 57 distinct words")
    require(all(len(w) == 4 and set(w) <= set(ALPHABET) for w in words),
            "malformed dictionary word")
    emit("PASS input binding: exact 57-word dictionary and candidate SHA256 pins")

    all_words = ["".join(t) for t in itertools.product(ALPHABET, repeat=4)]
    primitive = [w for w in all_words if len(set(rotations(w))) == 4]
    nonprimitive = set(all_words) - set(primitive)
    period_two = {a + b + a + b for a in ALPHABET for b in ALPHABET}
    require(nonprimitive == period_two and len(nonprimitive) == 16,
            "nonprimitive words are not exactly the period-dividing-two words")
    all_orbits = {canonical(w) for w in primitive}
    require(len(primitive) == 240 and len(all_orbits) == 60, "primitive orbit enumeration failed")
    require(all(len(set(rotations(w))) == 4 for w in words), "nonprimitive selected word")
    selected = [canonical(w) for w in words]
    require(len(set(selected)) == 57, "dictionary has two representatives of an orbit")
    missing = sorted(all_orbits - set(selected))
    require(missing == ["ADCB", "ADCD", "BCDC"], "unexpected missing primitive orbits")
    expected_orbits = {
        "all_words": 256, "period_dividing_two_words": 16,
        "primitive_words": 240, "primitive_orbits": 60,
        "selected_orbits": sorted(selected), "missing_orbits": missing,
    }
    require(cert["orbits"] == expected_orbits, "orbit certificate does not match enumeration")
    emit("PASS rotations: 256 words, 16 imprimitive, 240 primitive, 60 orbits, 57 selected")
    emit("PASS missing orbits: ADCB, ADCD, BCDC")

    a, b, c, d = [Poly.variable(4, i) for i in range(4)]
    F = density(words)
    all_primitive_weight = density(primitive)
    imprimitive_weight = density(sorted(period_two))
    require(imprimitive_weight == (a * a + b * b + c * c + d * d) ** 2,
            "imprimitive probability polynomial mismatch")
    require(all_primitive_weight == (a + b + c + d) ** 4 - imprimitive_weight,
            "primitive probability polynomial mismatch")
    orbit_formula = Q(1, 4) * all_primitive_weight - density(missing)
    compact_F = Q(1, 4) * ((a + b + c + d) ** 4 -
                          (a * a + b * b + c * c + d * d) ** 2)
    compact_F = compact_F - a * b * c * d - a * c * d ** 2 - b * c ** 2 * d
    require(F == orbit_formula and F == compact_F, "weighted density identity has a nonzero residual")
    require(cert["density"]["variables"] == ["a", "b", "c", "d"], "density variable order changed")
    require(F == from_records(4, cert["density"]["homogeneous_terms"]),
            "density certificate coefficient mismatch")
    require(F.evaluate([1, 1, 1, 1]) == 57, "density coefficient sum mismatch")
    emit(f"PASS density: all {len(F.terms)} nonzero monomial coefficients match literal words and orbit formula")
    emit("PASS simplex specialization: replace (a+b+c+d)^4 by 1 under the stated sum-one hypothesis")

    u, v, r, s = [Poly.variable(4, i) for i in range(4)]
    zero = Poly.const(4, 0)
    actual = F.substitute([Q(1, 2) * (u + r), Q(1, 2) * (u - r),
                           Q(1, 2) * (v + s), Q(1, 2) * (v - s)])
    balanced = F.substitute([Q(1, 2) * u, Q(1, 2) * u,
                             Q(1, 2) * v, Q(1, 2) * v])
    delta = 16 * (balanced - actual)
    require(cert["compression"]["variables"] == ["u", "v", "r", "s"], "SOS variable order changed")
    require(cert["compression"]["difference_factor"] == 16, "SOS difference factor changed")
    require(delta == from_records(4, cert["compression"]["difference_terms"]),
            "compression difference coefficient mismatch")
    sos = Poly.const(4, 0)
    parsed_squares = []
    for term in cert["compression"]["sos"]:
        multiplier = Q(term["multiplier"])
        square = from_records(4, term["square"])
        require(multiplier > 0, "SOS has a nonpositive multiplier")
        parsed_squares.append((multiplier, square))
        sos = sos + multiplier * square ** 2
    expected_squares = [(Q(2), u * r), (Q(1), (u - v) * s),
                        (Q(1), v * (r - s)), (Q(1), r ** 2),
                        (Q(2), r * s), (Q(1), r * s + s ** 2)]
    require(sos == delta, "SOS identity has a nonzero coefficient residual")
    require(parsed_squares == expected_squares, "SOS factors differ from the reviewed identity")
    # These are the explicit equality-forcing factors in the stated proof.
    require(parsed_squares[3][1] == r ** 2, "r^4 equality factor missing")
    require(parsed_squares[5][1].substitute([u, v, zero, s]) == s ** 2,
            "s^4 equality factor after r=0 missing")
    emit(f"PASS compression: all {len(delta.terms)} nonzero coefficients match six positive square terms")
    emit("PASS equality factors: r^4 forces r=0, then (rs+s^2)^2 forces s=0")

    y = Poly.variable(1, 0)
    x = Q(1, 2) - y
    f = F.substitute([x, x, y, y])
    uni = cert["univariate"]
    require(uni["variable"] == "y" and uni["domain"] == ["0", "1/2"],
            "univariate variable or domain changed")
    require(f == univariate(uni["f_coefficients_ascending"]), "univariate quartic coefficient mismatch")
    P = univariate(uni["critical_polynomial_coefficients_ascending"])
    require(P == 24 * y ** 3 - 24 * y ** 2 + 9 * y - 1, "critical cubic coefficient mismatch")
    require(f.derivative(0) == Q(-1, 2) * P, "critical cubic is not -2 f'(y)")
    require(P.derivative(0) == 72 * (y - Q(1, 3)) ** 2 + 1,
            "critical cubic strict-monotonicity identity failed")
    require(P.evaluate([0]) == -1 and P.evaluate([Q(1, 2)]) == Q(1, 2),
            "critical cubic endpoint signs failed")
    lo, hi = [Q(uni["rho_interval"][key]) for key in ("lower", "upper")]
    require(0 < lo < hi < Q(1, 2), "rho isolating interval outside domain")
    require(hi - lo <= Q(1, 10 ** 30), "rho isolating interval too wide")
    require(P.evaluate([lo]) < 0 < P.evaluate([hi]), "rho interval does not isolate the critical root")
    beta_reduction = univariate(uni["beta_reduction_coefficients_ascending"])
    require(beta_reduction == Q(11, 48) - Q(1, 8) * y ** 2, "beta reduction coefficients changed")
    quotient = univariate(uni["beta_reduction_quotient_coefficients_ascending"])
    require(f - beta_reduction == quotient * P, "beta reduction is not exact modulo the critical cubic")
    beta_lo, beta_hi = [Q(uni["beta_interval"][key]) for key in ("lower", "upper")]
    exact_lower = beta_reduction.evaluate([hi])
    exact_upper = beta_reduction.evaluate([lo])
    require(beta_lo < exact_lower < exact_upper < beta_hi,
            "beta rational interval is not implied by the rho interval")
    require(beta_hi - beta_lo <= Q(1, 10 ** 28), "beta isolating interval too wide")
    emit("PASS univariate: exact quartic, f'=-P/2, and P'=72(y-1/3)^2+1")
    emit("PASS unique maximizer: P(0)=-1, P(1/2)=1/2, strictly positive P' on all real y")
    emit(f"PASS rho interval (strict): {lo} < rho < {hi}")
    emit("PASS beta reduction: f(y)-(11/48-y^2/8) = (1/24-y/8) * P(y)")
    emit(f"PASS beta interval (strict): {beta_lo} < beta < {beta_hi}")

    lift = cert["lift"]
    require(lift["letter_weights"] == FIXED_WEIGHTS, "A:B:C:D weight binding differs from 5:5:3:3")
    require(lift["alphabet_size_coefficient"] == 16 and sum(FIXED_WEIGHTS.values()) == 16,
            "alphabet size binding differs from m=16q")
    total, per_word = exact_lift(words, lift["letter_weights"])
    require(total == univariate(lift["q_polynomial_coefficients_ascending"]),
            "5:5:3:3 lift polynomial coefficient mismatch")
    require(total == 14733 * y ** 4 - 2528 * y ** 3 + 94 * y ** 2,
            "5:5:3:3 lift does not match the reviewed claimed polynomial")
    require(per_word == lift["per_word_polynomials"], "per-word adjacent-equality count mismatch")
    require(Q(lift["leading_density"]) == Q(14733, 16 ** 4), "leading density normalization mismatch")
    weights = [Q(FIXED_WEIGHTS[k], 16) for k in ALPHABET]
    require(F.evaluate(weights) == Q(lift["leading_density"]), "product density and exact-lift leading coefficient disagree")
    require(f.evaluate([Q(3, 16)]) == Q(lift["leading_density"]), "rational proportions do not correspond to y=3/16")
    gap_bound = Q(lift["rational_density_error_upper_bound"])
    require(gap_bound == Q(1, 2500000), "rational approximation error claim changed")
    require(beta_lo > Q(lift["leading_density"]) and beta_hi - Q(lift["leading_density"]) < gap_bound,
            "the positive density gap is not certified below 4e-7")
    uniform, _ = exact_lift(words, {k: 1 for k in ALPHABET})
    histogram = {}
    for w in words:
        equalities = sum(w[i] == w[i - 1] for i in range(1, 4))
        histogram[str(equalities)] = histogram.get(str(equalities), 0) + 1
    require(histogram == {"0": 23, "1": 28, "2": 6}, "uniform adjacent-equality histogram mismatch")
    require(lift["uniform_adjacent_equalities_histogram"] == histogram, "uniform histogram certificate mismatch")
    require(uniform == univariate(lift["uniform_q_polynomial_coefficients_ascending"]),
            "uniform lift polynomial certificate mismatch")
    require(uniform == 57 * y ** 4 - 40 * y ** 3 + 6 * y ** 2,
            "uniform lift polynomial does not match the reviewed statement")
    emit("PASS exact lift: all 57 products give 14733q^4 - 2528q^3 + 94q^2")
    emit("PASS leading density: 14733/65536 = F(5/16,5/16,3/16,3/16) = f(3/16)")
    emit("PASS rational approximation: 0 < beta-14733/65536 < 1/2500000")
    emit("PASS uniform cross-check: histogram {0:23,1:28,2:6}, count 57q^4-40q^3+6q^2")
    emit("SCOPE: fixed-template exact algebra and counts; strict-window/GP bridge is separately certified")
    emit("SCOPE: no global optimum over dictionaries or original GP sets; no Lean or historical-maximality claim")


def negative_controls(raw_words, candidate_bytes, cert):
    cases = []
    # Rotating one template preserves its product monomial, so the source pin
    # must bind the actual ordered word rather than only the density polynomial.
    damaged_words = raw_words.replace(b"DBDD", b"BDDD", 1)
    cases.append(("word rotation with unchanged certificate", damaged_words, candidate_bytes, copy.deepcopy(cert)))
    rebound = copy.deepcopy(cert)
    rebound["binding"]["dictionary_sha256"] = hashlib.sha256(damaged_words).hexdigest()
    cases.append(("word rotation with forged certificate rebind", damaged_words, candidate_bytes, rebound))
    wrong_weights = copy.deepcopy(cert)
    wrong_weights["lift"]["letter_weights"] = {"A": 5, "B": 3, "C": 5, "D": 3}
    cases.append(("weight permutation preserving total and multiset", raw_words, candidate_bytes, wrong_weights))
    wrong_density = copy.deepcopy(cert)
    old = Q(wrong_density["density"]["homogeneous_terms"][0]["coefficient"])
    wrong_density["density"]["homogeneous_terms"][0]["coefficient"] = str(old + 1)
    cases.append(("density coefficient increment", raw_words, candidate_bytes, wrong_density))
    wrong_lift = copy.deepcopy(cert)
    wrong_lift["lift"]["q_polynomial_coefficients_ascending"][2] = "95"
    cases.append(("lift q^2 coefficient 94 to 95", raw_words, candidate_bytes, wrong_lift))
    wrong_sos = copy.deepcopy(cert)
    # (rs+s^2)^2 -> (rs-s^2)^2 reverses the critical 2rs^3 cross term.
    for term in wrong_sos["compression"]["sos"][-1]["square"]:
        if term["powers"] == [0, 0, 0, 2]:
            term["coefficient"] = "-1"
    cases.append(("SOS cross-term sign reversal", raw_words, candidate_bytes, wrong_sos))
    wrong_cubic = copy.deepcopy(cert)
    wrong_cubic["univariate"]["critical_polynomial_coefficients_ascending"][1] = "8"
    cases.append(("critical cubic coefficient 9 to 8", raw_words, candidate_bytes, wrong_cubic))
    wrong_interval = copy.deepcopy(cert)
    wrong_interval["univariate"]["rho_interval"] = {
        "lower": "186730853364600380000000000000000000/1000000000000000000000000000000000000",
        "upper": "186730853364600380000000000000000001/1000000000000000000000000000000000000",
    }
    cases.append(("narrow interval at obsolete erroneous rho decimal", raw_words, candidate_bytes, wrong_interval))
    wrong_beta = copy.deepcopy(cert)
    wrong_beta["univariate"]["beta_reduction_coefficients_ascending"][0] = "12/48"
    cases.append(("beta reduction constant corruption", raw_words, candidate_bytes, wrong_beta))
    for name, words, candidate, damaged in cases:
        try:
            check(words, candidate, damaged, emit=lambda _: None)
        except Rejected as error:
            print(f"PASS negative control [{name}]: REJECTED: {error}")
        else:
            raise Rejected(f"negative control was incorrectly accepted: {name}")
    print(f"PASS negative controls: {len(cases)}/{len(cases)} deliberate corruptions rejected")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--words", type=Path, default=HERE.parent / "literature_lifts" / "jiggs57_words.txt")
    parser.add_argument("--candidate", type=Path, default=HERE.parent / "literature_lifts" / "JIGGS57_WEIGHTED_LIFT_V2.md")
    parser.add_argument("--certificate", type=Path, default=HERE / "weighted_certificate.json")
    parser.add_argument("--negative-controls", action="store_true")
    args = parser.parse_args()
    print("Independent Jiggs-57 weighted exact-algebra checker")
    print("Arithmetic: Python standard-library integers and fractions.Fraction only")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Checker SHA256: {hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}")
    try:
        raw_words = args.words.read_bytes()
        candidate = args.candidate.read_bytes()
        cert_bytes = args.certificate.read_bytes()
        cert = json.loads(cert_bytes)
        print(f"Certificate SHA256: {hashlib.sha256(cert_bytes).hexdigest()}")
        check(raw_words, candidate, cert)
        if args.negative_controls:
            negative_controls(raw_words, candidate, cert)
    except (Rejected, ValueError, KeyError, TypeError, OSError) as error:
        print(f"REJECTED: {error}")
        return 1
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
