#!/usr/bin/env python3
"""Verify the inherited Ed25519 SSHSIG Git commit without ssh-keygen.

Requires cryptography; mathematical verification does not. This parser is
restricted to the declared Ed25519/git/sha512 stage-one signature, not a general
SSH security library. It binds the exact public fingerprint and Git object hash.
"""
from __future__ import annotations
import argparse,base64,hashlib,json,struct,subprocess
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.exceptions import InvalidSignature

COMMIT='b45b04eeab0fc521b789d6d47b4d8b94119e8c90'
FINGERPRINT='SHA256:Sr3y91PKDXe5Mo3sJa1Z0Q0N/n51sL4N+up5LnUCT3c'


def field(x):return struct.pack('>I',len(x))+x


class Reader:
    def __init__(self,x):self.x=x;self.i=0
    def take(self,n):
        if n<0 or self.i+n>len(self.x):raise ValueError('truncated SSHSIG')
        v=self.x[self.i:self.i+n];self.i+=n;return v
    def u32(self):return struct.unpack('>I',self.take(4))[0]
    def string(self):return self.take(self.u32())
    def end(self):
        if self.i!=len(self.x):raise ValueError('trailing SSHSIG bytes')


def verify(raw:bytes,expected_commit=COMMIT):
    got=hashlib.sha1(b'commit '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    if got!=expected_commit:raise ValueError('wrong Git object binding')
    header,message=raw.split(b'\n\n',1);lines=header.splitlines(keepends=True)
    kept=[];sig=[];i=0;found=0
    while i<len(lines):
        if lines[i].startswith(b'gpgsig '):
            found+=1;sig.append(lines[i][7:]);i+=1
            while i<len(lines)and lines[i].startswith(b' '):sig.append(lines[i][1:]);i+=1
        else:kept.append(lines[i]);i+=1
    if found!=1:raise ValueError('expected exactly one signature field')
    # splitlines omits the final newline only on the last header line; restore
    # the canonical unsigned header delimiter after removing the sig field.
    unsigned=b''.join(kept).rstrip(b'\n')+b'\n\n'+message
    armor=b''.join(sig).strip().splitlines()
    if armor[0]!=b'-----BEGIN SSH SIGNATURE-----'or armor[-1]!=b'-----END SSH SIGNATURE-----':
        raise ValueError('wrong armor')
    r=Reader(base64.b64decode(b''.join(armor[1:-1]),validate=True))
    if r.take(6)!=b'SSHSIG'or r.u32()!=1:raise ValueError('wrong SSHSIG magic/version')
    public=r.string();namespace=r.string();reserved=r.string();alg=r.string();sigblob=r.string();r.end()
    if (namespace,reserved,alg)!=(b'git',b'',b'sha512'):raise ValueError('wrong signature namespace/hash binding')
    fp='SHA256:'+base64.b64encode(hashlib.sha256(public).digest()).decode().rstrip('=')
    if fp!=FINGERPRINT:raise ValueError('wrong public signing key')
    p=Reader(public);keytype=p.string();key=p.string();p.end()
    s=Reader(sigblob);sigtype=s.string();signature=s.string();s.end()
    if keytype!=b'ssh-ed25519'or sigtype!=keytype or len(key)!=32 or len(signature)!=64:
        raise ValueError('wrong Ed25519 encoding')
    payload=b'SSHSIG'+field(namespace)+field(reserved)+field(alg)+field(hashlib.sha512(unsigned).digest())
    Ed25519PublicKey.from_public_bytes(key).verify(signature,payload)
    # A negative cryptographic control, not just an object-hash rejection.
    try:Ed25519PublicKey.from_public_bytes(key).verify(signature,payload[:-1]+bytes([payload[-1]^1]))
    except InvalidSignature:pass
    else:raise ValueError('corrupt signed payload accepted')
    return {'commit':got,'public_fingerprint':fp,'namespace':namespace.decode(),
            'hash_algorithm':alg.decode(),'signature':'Ed25519 SSHSIG PASS',
            'corrupt_payload_rejected':True,'native_git_ssh_verification':'not executed: ssh-keygen absent in current runtime'}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',default=str(Path(__file__).resolve().parents[2]));args=ap.parse_args()
    raw=subprocess.run(['git','-C',args.repo,'cat-file','commit',COMMIT],check=True,capture_output=True).stdout
    print(json.dumps(verify(raw),indent=2,sort_keys=True))

if __name__=='__main__':main()
