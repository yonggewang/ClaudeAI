#!/usr/bin/env python3
"""Verification of the Mito augmentation claim: in the group ring
    A = R_n[Z]/(Z^2 - 1)  (resp. R_n[Z1,Z2]/(Z1^2-1, Z2^2-1) for the 4-adic case),  R_n = F_2[x]/(x^n - 1),
the augmentation eps: Z -> 1 is a ring homomorphism onto R_n.  Applying it to the public relation
s = x + h*y of Mito therefore gives a PLAIN HQC relation  eps(s) = eps(x) + eps(h)*eps(y)  in R_n,
with wt(eps(x)) <= sum_i wt(x_i).  So Mito key recovery is never harder than an HQC key-recovery
instance of half (resp. a quarter of) the length with the same total weight.
usage: python3 mito_toy.py [n] [trials] [seed]"""
import sys, random

def rmul(a, b, n):
    """product in F_2[x]/(x^n - 1), elements as frozenset-like sorted lists of exponents -> set"""
    out = set()
    for i in a:
        for j in b:
            k = (i + j) % n
            out ^= {k}
    return out

def gmul(A, B, n, e):
    """product in R_n[Z_1..Z_e]/(Z_i^2 - 1): A, B are dicts {group element (tuple in {0,1}^e): set of exponents}"""
    out = {}
    for ga, pa in A.items():
        for gb, pb in B.items():
            g = tuple((x + y) % 2 for x, y in zip(ga, gb))
            out[g] = out.get(g, set()) ^ rmul(pa, pb, n)
    return out

def eps(A, n):
    """augmentation Z_i -> 1: sum the components"""
    out = set()
    for p in A.values(): out ^= p
    return out

def rnd(n, w, e, rng):
    """random element of the group ring with w nonzero coefficients spread over the 2^e components"""
    A = {}
    pos = rng.sample([(g, i) for g in [tuple((k >> j) & 1 for j in range(e)) for k in range(1 << e)] for i in range(n)], w)
    for (g, i) in pos: A.setdefault(g, set()).__ixor__({i})
    return A

def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 127
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    rng = random.Random(int(sys.argv[3]) if len(sys.argv) > 3 else 1)
    for e in (1, 2):
        ok = wsum = 0
        for _ in range(trials):
            h = rnd(n, rng.randint(n // 2, n), e, rng)          # dense public element
            x = rnd(n, rng.randint(4, 12), e, rng); y = rnd(n, rng.randint(4, 12), e, rng)
            wx = sum(len(p) for p in x.values()); wy = sum(len(p) for p in y.values())
            s = {g: p.copy() for g, p in gmul(h, y, n, e).items()}
            for g, p in x.items(): s[g] = s.get(g, set()) ^ p
            # the claim: eps(s) = eps(x) + eps(h) eps(y) in R_n, and wt(eps(x)) <= wx
            lhs = eps(s, n)
            rhs = eps(x, n) ^ rmul(eps(h, n), eps(y, n), n)
            ok += (lhs == rhs) and len(eps(x, n)) <= wx and len(eps(y, n)) <= wy
            wsum += wx - len(eps(x, n))
        print(f"2^{e}-adic (R_{n}[Z]^{e}): augmentation is a homomorphism and does not increase weight in "
              f"{ok}/{trials} random instances; mean weight lost to cancellation {wsum/trials:.2f}")

if __name__ == '__main__':
    main()
