#!/usr/bin/env python3
"""Rank-metric re-pricing with CryptographicEstimators 2.1.1 RankSDEstimator (all algorithms incl. MaxMinors/SupportMinors
with hybrid/puncturing). Homogeneous RSD instances only: exact for C-Multi-UR-AG and BAG-Loong (merged support),
relaxation (upper bound on security) for the blockwise schemes BRQC / BRA / BAG-Piglet."""
import sys
from cryptographic_estimators.RankSDEstimator import RankSDEstimator

def price(label, q, m, n, k, r, claim, w=2.81):
    e = RankSDEstimator(q=q, m=m, n=n, k=k, r=r, w=w)
    res = e.estimate()
    best = min(((v['estimate']['time'], a, v['estimate']['memory']) for a, v in res.items() if v['estimate']['time'] is not None))
    mm = res.get('MaxMinors', {}).get('estimate', {}); sm = res.get('SupportMinors', {}).get('estimate', {})
    print(f"{label:28s} RSD(q={q},m={m},n={n},k={k},r={r}) w={w} | best {best[0]:7.2f} ({best[1]}, mem {best[2]:.1f}) | MM {mm.get('time', float('nan')):7.2f} (params {mm.get('parameters')}) | SM {sm.get('time', float('nan')):7.2f} | claimed {claim}", flush=True)
    return best

if __name__ == '__main__':
    w = float(sys.argv[1]) if len(sys.argv) > 1 else 2.81
    print("== C-Multi-UR-AG (homogeneous RSD; designers: MM with omega=2: key 172/296/530, ct 170/276/580)")
    for (lvl, m, n, N1, N2, w1, w2, claim) in [(128,79,35,11,16,8,9,170),(256,127,45,15,16,10,11,276),(512,181,67,19,21,12,14,530)]:
        price(f"CMultiURAG-{lvl} key (RSD w1)", 2, m, 2*n, n, w1, claim, w)
        price(f"CMultiURAG-{lvl} ct (RSD w2)", 2, m, 2*n+N1, n, w2, claim, w)
    print("== BAG-Loong (merged support r = t1+t2-g; kem-03-4 with omega=3: 243.3/333.3/432.9 for 256/384/512)")
    for (lvl, n, m, np_, t1, t2, g, claim) in [(128,42,47,46,5,5,4,128),(256,65,67,67,5,6,3,256),(384,83,83,83,6,6,3,384),(512,104,97,97,7,7,4,512)]:
        price(f"BAG-Loong-{lvl} key [2n,n]", 2, m, 2*n, n, t1+t2-g, claim, w)
        price(f"BAG-Loong-{lvl} key [2n',n']", 2, m, 2*np_, np_, t1+t2-g, claim, w)
    print("== BRQC relaxation (homogeneous r = sum of block ranks; blockwise attacks are cheaper)")
    for (lvl, m, n, wx, wy, wr1, wr2, we, claim) in [(128,127,119,5,5,5,5,8,181),(256,163,161,5,6,6,7,8,295),(512,229,227,6,7,8,8,8,566)]:
        price(f"BRQC-{lvl} key relax", 2, m, 2*n, n, wx+wy, claim, w)
        price(f"BRQC-{lvl} ct relax", 2, m, 3*n, n, wr1+wr2+we, claim, w)
    print("== BRA relaxation")
    for (lvl, m, n, wx, wy, wr1, wr2, we, claim) in [(128,67,121,4,5,5,5,8,189),(256,83,161,5,5,6,6,8,304),(512,127,221,6,6,7,8,8,556)]:
        price(f"BRA-{lvl} key relax", 2, m, 2*n, n, wx+wy, claim, w)
        price(f"BRA-{lvl} ct relax", 2, m, 3*n, n, wr1+wr2+we, claim, w)
