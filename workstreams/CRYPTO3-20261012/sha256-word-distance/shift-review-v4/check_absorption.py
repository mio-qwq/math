#!/usr/bin/env python3
"""New small check: conservative oracle absorbs before 63 in either direction."""
import argparse
import json
from pathlib import Path

from check_independent import HERE, ROOT, SUPPORT_HASH, digest, require, support_extension


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    source = ROOT / "supports-v2.json"
    require(digest(source) == SUPPORT_HASH, "support bytes changed")
    supports = [set(x) for x in json.loads(source.read_text())["supports"]]
    witnesses = []
    for index, support in enumerate(supports):
        for direction in (-1, 1):
            states, _ = support_extension(support, direction * 63)
            first = None
            for count in range(16, 64):
                terminal = list(range(64 + count - 16, 64 + count)) if direction > 0 else list(range(-count, -count + 16))
                if all(states[j] == "unknown" for j in terminal):
                    first = {"source": index, "direction": "left" if direction > 0 else "right",
                             "first_absorbing_offset_magnitude": count,
                             "sixteen_consecutive_old_indices": terminal,
                             "statuses": [states[j] for j in terminal]}
                    break
            require(first is not None, "no absorbing block found")
            witnesses.append(first)
    data = {
        "schema": "crypto3-independent-shift-oracle-absorption-v4",
        "support_sha256": digest(source),
        "checker_sha256": digest(Path(__file__).resolve()),
        "dependency_checker_sha256": digest(HERE / "check_independent.py"),
        "oracle": "zero or one active term determines status; any unknown or >=2 active terms gives unknown",
        "proof": "After sixteen consecutive unknown positions, every next recurrence in the relevant direction has unknown predecessors, so all later newly created positions stay unknown by induction. Every shifted window beyond that offset contains such a newly created unknown position and cannot be exactly classified by this oracle.",
        "absorbing_witnesses": witnesses,
        "number_of_safe_maps_in_INDEPENDENT_RUN": 24,
        "all_integer_offset_completeness": "For this conservative oracle and the frozen fifteen source/target supports only; not all mathematical cancellations or time-shift reductions.",
    }
    rendered = json.dumps(data, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
