"""Check this version's payload hashes before replaying any certificate."""
from pathlib import Path
import hashlib, json

root = Path(__file__).resolve().parent
manifest = json.loads((root/'manifest.json').read_text(encoding='utf-8'))
seen = set()
for record in manifest['files']:
    name = record['path']
    path = root/name
    resolved = path.resolve()
    if name in seen or not resolved.is_relative_to(root.resolve()):
        raise ValueError('Invalid or duplicate payload path')
    seen.add(name)
    data = path.read_bytes()
    if len(data) != record['bytes'] or hashlib.sha256(data).hexdigest() != record['sha256']:
        raise ValueError(f'Changed payload: {name}')
print(f'PASS: {len(seen)} exact payload files.')
