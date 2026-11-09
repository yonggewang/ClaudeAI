#!/usr/bin/env python3
"""Re-price BRQC/BRA blockwise MaxMinors using ONLY the designers' block order
(largest rank first = descending rank), the regime in which E-bar (Theorem 7.6 /
ePrint 2025/668) is a tight upper bound on the independent equations.  This
replaces the earlier free-permutation search, which applied E-bar to orderings
where it is not a valid tight bound (Yongcheng Song, NGCC forum, 2026-11).
"""
import sys
from mm_search import search_one

def descending(q, m, ns, rs, k, omega, label, designers):
    order = sorted(range(len(rs)), key=lambda i: (-rs[i], -ns[i]))  # largest rank first
    ns2 = tuple(ns[i] for i in order); rs2 = tuple(rs[i] for i in order)
    r = search_one(q, m, ns2, rs2, k, omega)
    (lg, g, lE, lN, xi), p, a, h = r
    print(f"{label}: descending-order min log2 TC = {lg:.2f} "
          f"(designers {designers})  xi'={xi:.3f} p={p} a={a} h={h} order {order} ranks {rs2}", flush=True)
    return lg

if __name__ == '__main__':
    omega = float(sys.argv[1]) if len(sys.argv) > 1 else 2.0
    for (lab, m, n, wx, wy, wr1, wr2, we, ck, cc) in [
        ("BRQC-128",127,119,5,5,5,5,8,216,181),("BRQC-256",163,161,5,6,6,7,8,309,295),
        ("BRQC-512",229,227,6,7,8,8,8,584,566)]:
        descending(2, m, (n, n), (wx, wy), n, omega, f"{lab} key", ck)
        descending(2, m, (n, n, n), (wr1, wr2, we), n, omega, f"{lab} ct", cc)
    for (lab, m, n, wx, wy, wr1, wr2, we, ck, cc) in [
        ("BRA-128",67,121,4,5,5,5,8,194,189),("BRA-256",83,161,5,5,6,6,8,304,321),
        ("BRA-512",127,221,6,6,7,8,8,556,567)]:
        descending(2, m, (n, n), (wx, wy), n, omega, f"{lab} key", ck)
        descending(2, m, (n, n, n), (wr1, wr2, we), n, omega, f"{lab} ct", cc)
