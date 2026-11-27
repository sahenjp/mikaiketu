#!/usr/bin/env python3
"""Exact, bounded verification; never a proof of global nonexistence."""
import argparse
from functools import lru_cache
from itertools import product
from math import gcd, isqrt

N = 114514
KNOWN = {5: 11, 11: 67, 13: 53, 17: 103, 23: 47, 29: 59}


@lru_cache(maxsize=None)
def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    return all(n % d for d in range(3, isqrt(n) + 1, 2))


def prime_factors(n):
    return [d for d in range(2, n + 1) if n % d == 0 and is_prime(d)]


def residues(p, q):
    return {pow(a, p, q) for a in range(q)}


def subgroup_residues(p, q):
    if not is_prime(q) or (q - 1) % p:
        raise ValueError('q must be prime and q = 1 mod p')
    k = (q - 1) // p
    factors = prime_factors(k)
    for g in range(1, q):
        h = pow(g, p, q)
        if all(pow(h, k // r, q) != 1 for r in factors):
            result = {0} | {pow(h, j, q) for j in range(k)}
            if len(result) != k + 1:
                raise RuntimeError('incorrect subgroup size')
            return result
    raise RuntimeError('generator not found')


def obstructed(R, q):
    targets = {(N - r) % q for r in R}
    return not any((a + b) % q in targets for a in R for b in R)


def sieve(bound, max_k):
    excluded, remaining = {}, []
    for p in range(5, bound + 1, 2):
        if not is_prime(p):
            continue
        for k in range(2, max_k + 1, 2):
            q = k * p + 1
            if is_prime(q) and obstructed(subgroup_residues(p, q), q):
                excluded[p] = q
                break
        else:
            remaining.append(p)
    return excluded, remaining


def local7():
    cert = {}
    for q in range(2, 1000):
        if not is_prime(q) or q % 7 != 1:
            continue
        R = {pow(a, 7, q): a for a in range(1, q)}
        witness = next(((R[u], R[v], R[(N - u - v) % q])
                        for u in R for v in R if (N - u - v) % q in R), None)
        if witness is None:
            raise RuntimeError(f'no unit witness at {q}')
        cert[q] = witness
    return cert


def valid(p, a, b, c):
    return (p >= 5 and is_prime(p) and all((a, b, c)) and
            gcd(a, b) == gcd(b, c) == gcd(c, a) == 1 and
            a**p + b**p + c**p == N)


def small7():
    return [(a, b, c) for a, b, c in product(range(-7, 8), repeat=3)
            if valid(7, a, b, c)]


def find_y(p, x, d, target):
    """Find y>x with (y+d)^p-y^p=target, or return None."""
    def f(y):
        return (y + d)**p - y**p
    lo = x + 1
    if f(lo) > target:
        return None
    # Binomial bound: p*d*y**(p-1) <= target for any root.
    hi = lo
    while f(hi) < target:
        hi *= 2
    while lo <= hi:
        y = (lo + hi) // 2
        value = f(y)
        if value == target:
            return y
        if value < target:
            lo = y + 1
        else:
            hi = y - 1
    return None


def search_exponent(p, bound):
    """Uses the proved reduction p<x and p*d<x in docs/mathematics.md."""
    checked = 0
    for x in range(p + 1, bound + 1):
        xp = x**p
        for s in (-1, 1):
            target = xp + s*N
            for d in range(1, (x - 1)//p + 1):
                if target % d:
                    continue
                # No coprimality of x and d is assumed.
                checked += 1
                y = find_y(p, x, d, target)
                if y is not None:
                    a, b, c = -s*x, -s*y, s*(y+d)
                    if valid(p, a, b, c):
                        return (p, a, b, c), checked
    return None, checked


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('local7', 'sieve', 'search'))
    parser.add_argument('--bound', type=int, default=1000)
    parser.add_argument('--max-k', type=int, default=200)
    args = parser.parse_args()
    if args.bound < 5 or args.max_k < 2:
        parser.error('bound >= 5 and max-k >= 2 required')
    if args.mode == 'local7':
        cert = local7()
        for q, abc in cert.items():
            print(q, *abc)
        print(f'{len(cert)} unit witnesses; N mod 49 = {N % 49}')
        return
    for p, q in KNOWN.items():
        if not obstructed(residues(p, q), q):
            raise RuntimeError(f'known obstruction failed: {p}, {q}')
    excluded, remaining = sieve(args.bound, args.max_k)
    # Independently verified obstructions are usable even with a small max-k.
    remaining = [p for p in remaining if p not in KNOWN]
    excluded.update({p: q for p, q in KNOWN.items() if p <= args.bound and p not in excluded})
    print(f'bound={args.bound} max_k={args.max_k}; excluded={len(excluded)} remaining={remaining}', flush=True)
    if args.mode == 'sieve':
        for p, q in excluded.items():
            print(p, q)
        return
    if small7():
        print('SOLUTION', 7, *small7()[0])
        return
    for p in remaining:
        solution, checked = search_exponent(p, args.bound)
        print(f'p={p}: {checked} divisor candidates, solution={solution}', flush=True)
        if solution:
            return
    print(f'No solution with min(|a|,|b|,|c|) <= {args.bound}; not a global proof.')


if __name__ == '__main__':
    main()
