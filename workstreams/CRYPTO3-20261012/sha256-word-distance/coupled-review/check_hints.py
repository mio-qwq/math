#!/usr/bin/env python3
"""Independent sequential unit-propagation verifier for explicit RUP hints.

No solver, watch lists, discoverer imports, clause deletion, or RAT rule.
Every hinted clause must be unit, or the final all-false conflict clause.
"""
import argparse
import hashlib
import json
from pathlib import Path
import time


class InvalidProof(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise InvalidProof(message)


def validate_clause(clause, n):
    require(isinstance(clause, list), 'clause must be a list')
    require(all(type(lit) is int and 1 <= abs(lit) <= n for lit in clause),
            'invalid clause literal')


def read_cnf(path):
    clauses = []
    header = None
    for line in path.read_text().splitlines():
        words = line.split()
        if not words or words[0] == 'c':
            continue
        if words[0] == 'p':
            require(header is None and not clauses and len(words) == 4 and words[1] == 'cnf',
                    'invalid or repeated CNF header')
            header = (int(words[2]), int(words[3]))
            require(header[0] > 0 and header[1] >= 0, 'invalid CNF dimensions')
        else:
            require(header is not None, 'CNF clause before header')
            values = list(map(int, words))
            require(values[-1] == 0, 'unterminated CNF clause')
            clause = values[:-1]
            validate_clause(clause, header[0])
            clauses.append(clause)
    require(header is not None and len(clauses) == header[1], 'CNF clause count mismatch')
    return header[0], clauses


def verify_rup(n, database, proposed, hints):
    validate_clause(proposed, n)
    require(isinstance(hints, list), 'hints must be a list')
    require(all(type(cid) is int and 1 <= cid <= len(database) for cid in hints),
            'unknown or future hint ID')
    assignment = [0] * (n+1)
    assumption_conflict = False
    for lit in proposed:
        var = abs(lit)
        forced = -1 if lit > 0 else 1
        if assignment[var] and assignment[var] != forced:
            assumption_conflict = True
        assignment[var] = forced
    if assumption_conflict:
        require(not hints, 'tautological target has unnecessary hints')
        return 0

    units = 0
    for step, cid in enumerate(hints):
        unseen = set()
        for lit in database[cid-1]:
            v = assignment[abs(lit)] * (1 if lit > 0 else -1)
            require(v <= 0, 'hint clause is already satisfied')
            if v == 0:
                unseen.add(lit)
        if not unseen:
            require(step == len(hints)-1, 'hints continue after conflict')
            return units
        require(len(unseen) == 1, 'hint is neither unit nor conflicting')
        literal = next(iter(unseen))
        assignment[abs(literal)] = 1 if literal > 0 else -1
        units += 1
    raise InvalidProof('no terminal conflict')


def verify_files(cnf, drup, hints_file):
    n, database = read_cnf(cnf)
    initial_count = len(database)
    require(all(database), 'this recorded proof must have no initial empty clause')
    additions = deletions = propagated = maximum_hints = 0
    last_clause = None
    with hints_file.open() as hints:
        for line_number, line in enumerate(drup.read_text().splitlines(), 1):
            parts = line.split()
            if not parts:
                continue
            deletion = parts[0] == 'd'
            values = list(map(int, parts[1:] if deletion else parts))
            require(bool(values) and values[-1] == 0, 'unterminated DRUP clause')
            clause = values[:-1]
            validate_clause(clause, n)
            if deletion:
                deletions += 1
                continue
            raw = hints.readline()
            require(bool(raw), 'missing hints row')
            row = json.loads(raw)
            require(isinstance(row, list) and len(row) == 3, 'invalid hint row')
            cid, hinted_clause, trail = row
            require(type(cid) is int and cid == len(database)+1, 'nonsequential clause ID')
            require(hinted_clause == clause, 'hinted addition differs from original DRUP')
            try:
                propagated += verify_rup(n, database, clause, trail)
            except InvalidProof as exc:
                raise InvalidProof(f'DRUP line {line_number}, clause {cid}: {exc}') from exc
            maximum_hints = max(maximum_hints, len(trail))
            database.append(list(clause))
            last_clause = clause
            additions += 1
        require(not hints.read().strip(), 'extra hints after DRUP')
    require(additions > 0 and last_clause == [], 'last addition is not an empty clause')
    return {'status': 'PASS', 'variables': n, 'original_clauses': initial_count,
            'checked_additions': additions, 'ignored_deletions': deletions,
            'unit_inferences': propagated, 'maximum_hint_count': maximum_hints,
            'last_addition_empty': True,
            'all_additions_match_original_drup': True}


def negative_controls():
    cases = [
        ('unknown_hint_id', 2, [[1]], [], [2]),
        ('satisfied_hint', 2, [[1]], [-1], [1]),
        ('nonunit_hint', 2, [[1, 2]], [], [1]),
        ('missing_terminal_conflict', 2, [[1]], [], [1]),
        ('hints_after_conflict', 2, [[1], [-1]], [], [1, 2, 1]),
        ('damaged_target_literal', 2, [[1], [-1, 2]], [-2], [1, 2]),
    ]
    result = []
    for name, n, database, clause, trail in cases:
        try:
            verify_rup(n, database, clause, trail)
        except InvalidProof:
            result.append({'case': name, 'rejected': True})
        else:
            raise AssertionError('accepted negative control: '+name)
    # A real implication succeeds, to distinguish rejection from a broken verifier.
    require(verify_rup(2, [[1], [-1, 2]], [2], [1, 2]) == 1,
            'positive unit-propagation control failed')
    return result


def main():
    parser = argparse.ArgumentParser()
    default = Path(__file__).resolve().parent.parent/'coupled-boundary'
    parser.add_argument('--cnf', type=Path, default=default/'boundary.cnf')
    parser.add_argument('--drup', type=Path, default=default/'boundary.drup')
    parser.add_argument('--hints', type=Path, default=default/'boundary.rup.jsonl')
    parser.add_argument('--record', type=Path)
    args = parser.parse_args()
    start = time.monotonic()
    result = verify_files(args.cnf, args.drup, args.hints)
    result['negative_controls'] = negative_controls()
    result['seconds'] = time.monotonic()-start
    result['source_hashes'] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                               for p in (args.cnf, args.drup, args.hints)}
    result['checker_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result['imports_discoverer_checker'] = False
    if args.record:
        args.record.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
