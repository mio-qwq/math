#!/usr/bin/env python3
"""Issue a standalone JSON certificate from a proper regular coloured graph.

This is the witness PRODUCER. Consumers should use the independent
verify_euler_certificate_json.py instead of trusting this issuer.
"""
import argparse
import json
import sys
from euler_root_edge_order import construct_euler_root_order


def issue(data):
    n=data['n'];d=data['d'];E=data['edges']
    if type(n) is not int or n<=0:
        raise ValueError('n must be a positive integer')
    V=set(range(n))
    edges=[]
    for entry in E:
        if len(entry)!=3 or any(type(v) is not int for v in entry):
            raise ValueError('edge must have three integer entries')
        edges.append(tuple(entry))
    result,certificate=construct_euler_root_order(V,edges,d)
    # Dictionary with integer keys would be converted to string keys by JSON;
    # encode an explicit, ordered list of (vertex,colour) records instead.
    cert=dict(certificate)
    cert['two_colour_map']=[[v,certificate['two_colour_map'][v]] for v in sorted(V)]
    return {
        'format':'mio-qwq/math/A/euler-root-order/1',
        'd':d,'vertices':list(sorted(V)),
        'edges':[list(t) for t in edges],
        'order':[list(t) for t in result],
        'certificate':cert,
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', nargs='?',help='JSON graph file (default stdin)')
    args=parser.parse_args()
    with (open(args.input,encoding='utf8') if args.input else sys.stdin) as f:
        data=json.load(f)
    json.dump(issue(data),sys.stdout,sort_keys=True,separators=(',',':'))
    sys.stdout.write('\n')

if __name__=='__main__':main()
