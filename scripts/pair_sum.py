"""Exact fixed-sum fifth-power solver; not an unbounded solver.
All signed triples at a fixed t are returned up to permutation.
Trial-division divisor enumeration is intentionally simple, not scalable.
"""
from math import gcd, isqrt
from itertools import combinations_with_replacement


def signed_divisors(n):
    if not n:
        raise ValueError('zero has infinitely many divisors')
    n = abs(n)
    for d in range(1, isqrt(n) + 1):
        if n % d == 0:
            yield d
            yield -d
            if d * d != n:
                yield n // d
                yield -(n // d)


def fifth_at_sum(n, t):
    """Exact for n != t**5, any signed integer t, with pairwise gcd=1."""
    if n == t**5:
        raise ValueError('degenerate target n=t**5 is outside this routine')
    if (t**5 - n) % 5:
        return set()
    k = (t**5 - n) // 5
    out = set()
    for a_sum in signed_divisors(k):
        l = 2*t - a_sum
        h = a_sum*a_sum + l*l
        delta = h*h - 16*(k//a_sum)
        if delta < 0:
            continue
        v = isqrt(delta)
        if v*v != delta:
            continue
        for u in {v, -v}:
            if (h+u) % 4:
                continue
            r = (h+u)//4
            delta2 = l*l - 4*r
            if delta2 < 0:
                continue
            w = isqrt(delta2)
            if w*w != delta2 or (l+w)%2:
                continue
            b_sum, c_sum = (l+w)//2, (l-w)//2
            a,b,c = t-b_sum,t-c_sum,t-a_sum
            if not all((a,b,c)) or gcd(a,b)!=1 or gcd(b,c)!=1 or gcd(c,a)!=1:
                continue
            assert a+b+c==t and a**5+b**5+c**5==n
            out.add(tuple(sorted((a,b,c))))
    return out


def test():
    # Exact reconstruction and algebraic identities on all primitive triples
    # in the test cube; this is a regression test, not a global proof.
    checked=0
    for a,b,c in combinations_with_replacement(range(-8,9),3):
        if not all((a,b,c)) or gcd(a,b)!=1 or gcd(b,c)!=1 or gcd(c,a)!=1:
            continue
        t=a+b+c
        pprod=(a+b)*(b+c)*(c+a)
        q=t*t-a*b-b*c-c*a
        assert t**5-a**5-b**5-c**5==5*pprod*q
        assert t**7-a**7-b**7-c**7==7*pprod*(q*q+t*a*b*c)
        n=a**5+b**5+c**5
        if n==t**5:
            continue
        assert (a,b,c) in fifth_at_sum(n,t)
        checked+=1
    print('primitive nondegenerate reconstruction tests:',checked)
    # For both targets, examine every t in this bounded interval.
    for n in (114514,364364):
        hits=[]
        for t in range(-30,31):
            hits.extend(fifth_at_sum(n,t))
        print('target',n,'signed sum interval [-30,30], hits:',hits)
        assert not hits


if __name__ == '__main__':
    test()
