#!/usr/bin/env python3
"""Explicit witness only. Does not implement distances or verification."""
import json
from pathlib import Path

words = [[a,b,c] for a in range(6) for b in range(6) if a != b for c in (6,7,8)]
certificate = {
    'd': 6, 'k': 3, 'alphabet': list(range(9)),
    'source': 'https://arxiv.org/html/2604.15909v1#S3.SS3',
    'target': 'Unnumbered optimality conjecture immediately after Theorem 3.6',
    'conjectured_value': 84, 'selected_words': words,
    'construction': 'First two distinct letters in {0,1,2,3,4,5}; last letter in {6,7,8}.'
}
path = Path(__file__).with_name('certificate.json')
path.write_text(json.dumps(certificate,indent=2)+'\n')
print(f'Wrote {len(words)} explicit words to {path.name}')
