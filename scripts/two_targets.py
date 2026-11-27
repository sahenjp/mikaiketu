#!/usr/bin/env python3
"""Exact finite verification; no global nonexistence claim."""
import argparse
from math import gcd
from verify import is_prime, subgroup_residues, find_y

TARGETS = (114514, 364364)
CASES = {114514: (7, 19, 31, 67, 317), 364364: (5,)}
WITNESSES = [(114514,7,1,1,6),(114514,19,3,5,12),
             (114514,31,2,12,17),(114514,67,2,29,47),
             (114514,317,1,128,265),(364364,5,2,2,0)]

def valid(n,p,a,b,c):
    return all((a,b,c)) and gcd(a,b)==gcd(b,c)==gcd(c,a)==1 and a**p+b**p+c**p==n

def obstruction(n,p,q):
    r = subgroup_residues(p,q)
    units = r-{0}
    return not any((n-a-b)%q in r for a in units for b in units)

def small(n,p):
    # Same-sign largest terms imply z**p <= n.
    # Opposite-sign largest terms imply gap <= p**p+n if x<=p.
    z = 1
    while (z+1)**p <= n:
        z += 1
    y = 1
    while (y+1)**p-y**p <= p**p+n:
        y += 1
    limit = max(y,z,p)
    while (limit+1)**p <= y**p+p**p+n:
        limit += 1
    for a in range(-limit,limit+1):
        for b in range(-limit,limit+1):
            for c in range(-limit,limit+1):
                if min(abs(a),abs(b),abs(c))<=p and valid(n,p,a,b,c):
                    return (p,a,b,c)
    return None

def search(n,p,bound):
    for x in range(p+1,bound+1):
        for s in (-1,1):
            t=x**p+s*n
            if t<=0:
                continue
            for d in range(1,t//(p*(x+1)**(p-1))+1):
                if t%d:
                    continue
                y=find_y(p,x,d,t)
                if y is not None and valid(n,p,-s*x,-s*y,s*(y+d)):
                    return (p,-s*x,-s*y,s*(y+d))
    return None

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--bound',type=int,default=100)
    ap.add_argument('--max-k',type=int,default=108)
    args=ap.parse_args()
    if args.bound<5 or args.max_k<2:
        ap.error('bound >=5 and max-k >=2 required')
    for n,p,a,b,c in WITNESSES:
        assert a%p and b%p
        assert sum(pow(t,p,p*p) for t in (a,b,c))%(p*p)==n%(p*p)
    for n in TARGETS:
        for p in (5,7,11,13,17):
            result=small(n,p)
            if result:
                print(n,'SOLUTION',result)
                return
        remaining=[]
        for p in range(5,args.bound+1,2):
            if not is_prime(p):
                continue
            if any(is_prime(k*p+1) and obstruction(n,p,k*p+1)
                   for k in range(2,args.max_k+1,2)):
                continue
            remaining.append(p)
        print(n,'remaining',remaining,flush=True)
        for p in remaining:
            result=search(n,p,args.bound)
            if result:
                print(n,'SOLUTION',result)
                return
        print(n,'No solution with minimum absolute base <=',args.bound)
if __name__=='__main__':
    main()
