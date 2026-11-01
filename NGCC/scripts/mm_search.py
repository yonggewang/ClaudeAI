#!/usr/bin/env python3
"""Search over (p, a, h) for the blockwise MM cost (mm_blockwise.cost): for each (h, a) with at most two non-zero
hybrid blocks, greedy puncturing (puncture one column at a time in the block that lowers the cost most, while the
system stays overdetermined), then a local exhaustive refinement of p (+-4 per block) and a (+-3 per block)."""
import sys, itertools
from mm_blockwise import cost

import os
PMAX = int(os.environ.get('PMAX', '100000'))

def greedy_p(q, m, ns, rs, k, a, h, omega):
    l = len(ns); p = [0] * l
    c = cost(q, m, ns, rs, k, p, a, h, omega)
    if c is None: return None, None
    while True:
        best = None
        for i in range(l):
            if p[i] + 1 > PMAX: continue
            p2 = p[:]; p2[i] += 1
            c2 = cost(q, m, ns, rs, k, p2, a, h, omega)
            if c2 and (best is None or c2[0] < best[0][0]): best = (c2, p2)
        if best is None or best[0][0] >= c[0]: break
        c, p = best
    return c, p

def search(q, m, ns, rs, k, omega=2.0, label="", amax=90, hsearch=True):
    """searches over block ORDERINGS too: the attacker may order the blocks freely, and the
    counting of Theorem 7.6 is not symmetric in the blocks."""
    import itertools as _it
    if len(set(rs)) > 1 and len(rs) > 1:
        bestall = None
        seen = set()
        for perm in sorted(set(_it.permutations(range(len(rs))))):
            ns2 = tuple(ns[i] for i in perm); rs2 = tuple(rs[i] for i in perm)
            if (ns2, rs2) in seen: continue
            seen.add((ns2, rs2))
            r = search_one(q, m, ns2, rs2, k, omega, amax, hsearch)
            if r and (bestall is None or r[0][0] < bestall[0][0][0]): bestall = (r, perm)
        (c, p, a, h), perm = bestall
        (lg, g, lE, lN, xi) = c
        print(f"{label}: min log2 TC = {lg:.2f} [guess {g:.1f} + log2E {lE:.1f} + (w-1)log2N {(omega-1)*lN:.1f}] xi'={xi:.3f} p={p} a={a} h={h} block order {perm} (ranks {tuple(rs[i] for i in perm)})", flush=True)
        return bestall
    r = search_one(q, m, ns, rs, k, omega, amax, hsearch)
    (lg, g, lE, lN, xi), p, a, h = r
    print(f"{label}: min log2 TC = {lg:.2f} [guess {g:.1f} + log2E {lE:.1f} + (w-1)log2N {(omega-1)*lN:.1f}] xi'={xi:.3f} p={p} a={a} h={h}", flush=True)
    return r

def search_one(q, m, ns, rs, k, omega=2.0, amax=90, hsearch=True):
    l = len(ns); best = None
    def upd(c, p, a, h):
        nonlocal best
        if c and (best is None or c[0] < best[0][0]): best = (c, tuple(p), tuple(a), tuple(h))
    hs = [tuple([0] * l)]
    if hsearch:
        for i in range(l):
            for hv in range(1, min(3, rs[i]) + 1):
                h = [0] * l; h[i] = hv; hs.append(tuple(h))
    As = [tuple([0] * l)]
    for i in range(l):
        for av in range(1, amax + 1):
            a = [0] * l; a[i] = av; As.append(tuple(a))
    # two-block hybrid guessing is explored only coarsely: every point in the designers' tables, and
    # every minimum we found, puts the hybrid guess in a single block.
    for i, j in itertools.combinations(range(l), 2):
        for av in range(10, amax + 1, 10):
            for bv in range(10, amax + 1, 10):
                a = [0] * l; a[i] = av; a[j] = bv; As.append(tuple(a))
    for h in hs:
        for a in As:
            c, p = greedy_p(q, m, ns, rs, k, a, h, omega)
            if c: upd(c, p, a, h)
    # local refinement around the best
    (c0, p0, a0, h0) = best
    for a in itertools.product(*[range(max(0, a0[i] - 3), a0[i] + 4) for i in range(l)]):
        for p in itertools.product(*[range(max(0, p0[i] - 4), p0[i] + 5) for i in range(l)]):
            upd(cost(q, m, ns, rs, k, list(p), list(a), list(h0), omega), p, a, h0)
    return best

if __name__ == '__main__':
    omega = float(sys.argv[1]) if len(sys.argv) > 1 else 2.0
    which = sys.argv[2] if len(sys.argv) > 2 else "all"
    if which in ("all", "BRQC"):
        # BRQC: key: l=2 (n,n) r=(wx,wy) k=n ; ct: l=3 (n,n,n) r=(wr1,wr2,we) k=n  (designers' Table 6 conventions)
        for (lab, m, n, wx, wy, wr1, wr2, we, ck, cc) in [("BRQC-128",127,119,5,5,5,5,8,216,181),("BRQC-256",163,161,5,6,6,7,8,309,295),("BRQC-512",229,227,6,7,8,8,8,584,566)]:
            search(2, m, (n, n), (wx, wy), n, omega, f"{lab} key (designers {ck})")
            search(2, m, (n, n, n), (wr1, wr2, we), n, omega, f"{lab} ct (designers {cc})")
    if which in ("all", "BRA"):
        # BRA Table 6: key: (0.41,0,24,0,1.01,2^194), ct (1.14, a=0, p=(1,1,2), 2^189); BRA-256 key 304 ct 321; BRA-512 key 556 ct 567
        for (lab, m, n, wx, wy, wr1, wr2, we, ck, cc) in [("BRA-128",67,121,4,5,5,5,8,194,189),("BRA-256",83,161,5,5,6,6,8,304,321),("BRA-512",127,221,6,6,7,8,8,556,567)]:
            search(2, m, (n, n), (wx, wy), n, omega, f"{lab} key (designers {ck})")
            search(2, m, (n, n, n), (wr1, wr2, we), n, omega, f"{lab} ct (designers {cc})")
