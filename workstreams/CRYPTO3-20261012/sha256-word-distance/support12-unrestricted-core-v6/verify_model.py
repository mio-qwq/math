#!/usr/bin/env python3
"""Read-only actual-word verification, using only output-bit equations and stdlib."""
import argparse
import copy
import hashlib
import json
from pathlib import Path

MOD = 1 << 32


def need(ok, why):
    if not ok:
        raise ValueError(why)


def sigma(word, kind):
    left, right, shift = ((7, 18, 3), (17, 19, 10))[kind]
    output = 0
    for bit in range(32):
        value = ((word >> ((bit+left) % 32)) & 1) ^ ((word >> ((bit+right) % 32)) & 1)
        if bit+shift < 32:
            value ^= (word >> (bit+shift)) & 1
        output |= value << bit
    return output


def validate(model):
    words = model["words"]
    need(set(words) == {"x", "xp", "y", "yp", "r", "rp"}, "six actual words")
    need(all(type(v) is int and 0 <= v < MOD for v in words.values()), "unsigned word type/range")
    derivatives = {}
    for name in ("x", "y", "r"):
        before, after = words[name], words[name+"p"]
        derivatives[name] = {"d": (after-before) % MOD,
                             "F": (sigma(after, 0)-sigma(before, 0)) % MOD,
                             "G": (sigma(after, 1)-sigma(before, 1)) % MOD}
    d = derivatives["x"]["d"]
    need(d != 0, "D nonzero")
    need(type(model["derived_D"]) is int and model["derived_D"] == d, "reported derived D")
    need(derivatives["y"]["d"] == d, "Y input difference D")
    need(derivatives["r"]["d"] == (-d) % MOD, "R input difference -D")
    need(derivatives["x"]["F"] == derivatives["y"]["F"], "FX equals FY")
    need(derivatives["x"]["F"] == derivatives["r"]["F"], "FX equals FR")
    need((derivatives["y"]["G"]-derivatives["x"]["G"]) % MOD == 2*d % MOD,
         "GY minus GX equals 2D")
    need((derivatives["y"]["G"]-derivatives["r"]["G"]) % MOD == d,
         "GY minus GR equals D")
    return derivatives


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", type=Path)
    args = parser.parse_args()
    model = json.loads(args.model.read_text())
    derivatives = validate(model)
    reverse = copy.deepcopy(model)
    for name in ("x", "y", "r"):
        reverse["words"][name], reverse["words"][name+"p"] = (
            reverse["words"][name+"p"], reverse["words"][name])
    reverse["derived_D"] = (-model["derived_D"]) % MOD
    reversed_derivatives = validate(reverse)
    for name in derivatives:
        need(all(reversed_derivatives[name][kind] == (-value) % MOD
                 for kind, value in derivatives[name].items()), "actual full reversal")
    rejected = []
    controls = []
    for name in ("xp", "yp", "rp"):
        changed = copy.deepcopy(model)
        changed["words"][name] ^= 1
        controls.append(("alter "+name, changed))
    changed = copy.deepcopy(model)
    changed["words"]["x"] = True
    controls.append(("Boolean word", changed))
    for name, changed in controls:
        try:
            validate(changed)
        except ValueError as error:
            rejected.append({"control": name, "rejected_by": str(error)})
        else:
            raise ValueError("negative control accepted")
    d = derivatives["x"]["d"]
    result = {"schema": "CRYPTO3-direct-actual-three-pair-verification-v6",
              "accepted": True, "model_sha256": hashlib.sha256(args.model.read_bytes()).hexdigest(),
              "verifier_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "D_hex": f"{d:08x}", "v2_D": (d & -d).bit_length()-1,
              "actual_derivatives_hex": {name: {kind: f"{value:08x}" for kind, value in values.items()}
                                         for name, values in derivatives.items()},
              "full_reversal_checked": True, "rejected_controls": rejected,
              "scope": "Actual three-pair necessary-core witness only; not a full support or expanded message pair."}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
