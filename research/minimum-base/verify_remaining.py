#!/usr/bin/env python3
import sys
from pathlib import Path
from math import isqrt, gcd
from itertools import product

# Independently verify the extra exponent obstructions from sieve.cpp.
# Do not run with python -O (assertions are part of the checks).
lines = Path(sys.argv[1] if len(sys.argv)>1 else 'sieve_results.txt').read_text().splitlines()
bound = int(sys.argv[2]) if len(sys.argv)>2 else 10000000
counts = {1000000:78496, 5000000:348511, 10000000:664577}
assert __debug__
assert lines[0] == f'prime count={counts[bound]}'
expected = {114514: {7,19,31,67,317}, 364364: {5}}
remaining = {int(a):set(map(int,b.split())) for a,b in (line.split(':') for line in lines[1:])}
assert remaining.keys() == expected.keys()
assert all(expected[n] <= remaining[n] for n in expected)
def prime(n):
    return n > 1 and all(n % d for d in range(2,isqrt(n)+1))
for p in sorted(set.union(*(remaining[n]-expected[n] for n in expected))):
    left = {n for n in expected if p in remaining[n]-expected[n]}
    assert prime(p)
    for k in range(110,2002,2):
        q = k*p+1
        if not prime(q): continue
        for a in range(2,q):
            h=pow(a,p,q)
            r={pow(h,i,q) for i in range(k)}
            if len(r)==k: break
        assert len(r)==k and all(pow(t,k,q)==1 for t in r)
        for n in sorted(left):
            if not any((n-a-b)%q in r or (n-a-b)%q==0 for a in r for b in r):
                print('obstruction',n,p,q)
                left.remove(n)
        if not left: break
    assert not left
# Small-minimum exceptions: all signs and ordered magnitudes.
for n in expected:
    for p in [5,7,11,13,17]:
        X=17 if (n,p)==(364364,5) else p
        Y=1
        while (Y+1)**p-Y**p <= X**p+n: Y+=1
        Z=1
        while (Z+1)**p <= max(n,Y**p+X**p+n): Z+=1
        count=0
        for x in range(1,min(X,Z)+1):
            for y in range(x,Z+1):
                for z in range(y,Z+1):
                    if gcd(x,y)!=1 or gcd(x,z)!=1 or gcd(y,z)!=1: continue
                    for a,b,c in product([1,-1],repeat=3):
                        if a*x**p+b*y**p+c*z**p==n: count+=1
        assert count == 0
        print('small',n,p,'x<=',X,'z<=',Z,'solutions',count)
print('Supplemental exponent and small-base checks passed.')
