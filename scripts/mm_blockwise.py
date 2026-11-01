#!/usr/bin/env python3
"""Blockwise MaxMinors attack cost (BRQC spec Theorems 7.6 / 7.7; Song–Zhang–Huang–Wu blockwise RD) re-implemented
independently, with an exhaustive search over the puncturing / hybrid / subsupport-guessing vectors (p, a, h).
Checks the designers' Table 6 (BRQC) and re-prices BRA and C-Multi-UR-AG with the same formula.
Complexity (Theorem 7.7):  q^{sum_i a_i (r_i - h_i) + h_i (n_i - h_i)} * E * (prod_i C(n_i-p_i-a_i-h_i, r_i-h_i))^(omega-1)
with E = Ebar(m, n', k-a, r', l, n', r'), n'_i = n_i - p_i - a_i - h_i, r'_i = r_i - h_i, subject to E >= prod C(n'_i, r'_i) - 1.
"""
import sys, itertools
from math import comb as _comb, log2
def comb(n, k):
    return _comb(n, k) if (n >= 0 and 0 <= k <= n) else 0

def Ebar(m, ns, rs, k):
    """Theorem 7.6: upper bound on the number of independent MM equations over F_q; blocks ns=(n_1..n_l), rs=(r_1..r_l)"""
    l = len(ns)
    n0 = [0] + list(ns); r0 = [0] + list(rs)          # 1-indexed with n_0 = r_0 = 0
    z = [sum(n0[:i + 1]) - (k + 1) for i in range(l + 1)]   # z_iota, iota = 0..l
    # find the block b = l-j+1 containing position k+1
    for b in range(1, l + 1):
        before = sum(n0[:b])
        if before < k + 1 <= before + r0[b]:
            case = 1; break
        if before + r0[b] < k + 1 <= before + n0[b]:
            case = 2; break
    else:
        return None   # k+1 beyond n: degenerate
    tail = list(range(b + 1, l + 1))
    if case == 1:
        S = sum(r0[:b]) - z[b - 1]
        def term(nu_b, nus):
            return comb(z[b], r0[b] + z[b - 1] + nu_b) * prod(comb(n0[i], r0[i] + nu) for i, nu in zip(tail, nus))
    else:
        S = sum(r0[:b + 1])
        def term(nu_b, nus):
            return comb(z[b], nu_b) * prod(comb(n0[i], r0[i] + nu) for i, nu in zip(tail, nus))
    total = 0
    for nus in compositions(S, len(tail) + 1):
        total += term(nus[0], nus[1:])
    return m * total

def prod(it):
    p = 1
    for x in it: p *= x
    return p

def compositions(S, parts):
    """all tuples of `parts` non-negative integers summing to S"""
    if parts == 1:
        yield (S,); return
    for first in range(S + 1):
        for rest in compositions(S - first, parts - 1):
            yield (first,) + rest

def cost(q, m, ns, rs, k, p, a, h, omega=2.0):
    l = len(ns)
    nn = [ns[i] - p[i] - a[i] - h[i] for i in range(l)]
    rr = [rs[i] - h[i] for i in range(l)]
    if any(x <= 0 for x in nn) or any(x < 0 for x in rr) or k - sum(a) < 0: return None
    if sum(nn) <= k - sum(a): return None
    E = Ebar(m, nn, rr, k - sum(a))
    if E is None: return None
    N = prod(comb(nn[i], rr[i]) for i in range(l))
    # the MM modelling has at most m*C(n'-k'-1, sum r') equations in total; Ebar bounds the INDEPENDENT ones
    Emax = m * comb(sum(nn) - (k - sum(a)) - 1, sum(rr))
    E = min(E, Emax)
    if E <= 0 or N <= 0 or E < N - 1: return None
    guess = sum(a[i] * (rs[i] - h[i]) + h[i] * (ns[i] - h[i]) for i in range(l))
    lg = guess * log2(q) + log2(E) + (omega - 1) * log2(N)
    return lg, guess * log2(q), log2(E), log2(N), E / N

def optimise(q, m, ns, rs, k, omega=2.0, amax=None, pmax=None, hmax=None, label=""):
    l = len(ns)
    amax = amax or [min(n, 80) for n in ns]; pmax = pmax or [min(n - 1, 80) for n in ns]; hmax = hmax or [r for r in rs]
    best = None
    for h in itertools.product(*[range(0, hm + 1) for hm in hmax]):
        for a in itertools.product(*[range(0, am + 1) for am in amax]):
            # puncturing: p only matters through n'_i; scan p_i in steps
            for p in itertools.product(*[range(0, pm + 1, 1) for pm in pmax]):
                c = cost(q, m, ns, rs, k, p, a, h, omega)
                if c and (best is None or c[0] < best[0][0]):
                    best = (c, p, a, h)
    (lg, g, lE, lN, xi), p, a, h = best
    print(f"{label}: min log2 TC = {lg:.2f}  [guess {g:.1f} + log2 E {lE:.1f} + (omega-1) log2 N {(omega-1)*lN:.1f}], xi'=E/N={xi:.3f}, p={p}, a={a}, h={h}", flush=True)
    return best

if __name__ == '__main__':
    omega = float(sys.argv[1]) if len(sys.argv) > 1 else 2.0
    # BRQC Table 6 check. Key (Attack-2n): l=2, n=(119,119), r=(5,5), k=119 ; designers: a=(0,22), p=0, TC=2^216, xi'=1.05
    print("BRQC-128 key, designers' point:", cost(2, 127, (119, 119), (5, 5), 119, (0, 0), (0, 22), (0, 0), omega))
    # Ciphertext (Attack-3n): l=3, n=(119,119,119), r=(wr1,we,wr2)=(5,8,5), k = n + k_G = 119+3 ; designers: p=(0,0,32), a=0 -> 2^181
    for kk in (119, 122):
        print(f"BRQC-128 ct (k={kk}), designers' point p=(0,0,32):", cost(2, 127, (119, 119, 119), (5, 8, 5), kk, (0, 0, 32), (0, 0, 0), (0, 0, 0), omega))
