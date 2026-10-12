#!/usr/bin/env python3
"""Validate a portable Euler-root JSON proof without importing any generator.

Accepts a frozen proof file including graph, original edge colours, proposed
complete global order and auxiliary balanced-root certificate. Rebuilds all
original graph semantics and the *exact* construction from scratch.
Exits nonzero on an invalid certificate. Standard-library Python only.
"""
import argparse
import json
import sys
from check_euler_order_certificate_strict import check_strict


def check_json(data):
    if not isinstance(data,dict):return False,'not a JSON object'
    if data.get('format') != 'mio-qwq/math/A/euler-root-order/1':
        return False,'wrong certificate version'
    c=data.get('certificate')
    if not isinstance(c,dict):return False,'missing certificate body'
    colour_records=c.get('two_colour_map')
    if not isinstance(colour_records,list) or any(not isinstance(x,list) or len(x)!=2 for x in colour_records):
        return False,'colour map not a list of pairs'
    mapping={}
    for v,col in colour_records:
        if type(v) is not int or type(col) is not int or v in mapping:
            return False,'invalid or duplicate vertex in colour map'
        mapping[v]=col
    cert=dict(c);cert['two_colour_map']=mapping
    return check_strict(data.get('vertices',[]),data.get('edges',[]),
                        data.get('d',0),data.get('order',[]),cert)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate',nargs='?',help='JSON proof file (default stdin)')
    args=parser.parse_args()
    try:
        with (open(args.certificate,encoding='utf8') if args.certificate else sys.stdin) as f:
            data=json.load(f)
        okay,reason=check_json(data)
    except (OSError,TypeError,ValueError,KeyError,IndexError) as exc:
        okay,reason=False,f'unreadable certificate: {type(exc).__name__}'
    print(('PASS' if okay else 'FAIL')+' '+reason)
    if not okay:sys.exit(1)

if __name__=='__main__':main()
