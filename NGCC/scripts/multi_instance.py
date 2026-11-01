#!/usr/bin/env python3
"""Same-key multi-instance (DS-DOOM, May–Sá Diogo ePrint 2026/517, pinned doom.py sha256 d53e8bb0...) message-recovery
pricing for the NGCC Hamming-metric KEMs. For each parameter set: the public syndrome-decoding instance exposed by one
ciphertext (n, k, w), the number of free rotations per ciphertext, and the first session exponent s (M = rot * 2^s
observed ciphertexts under one key, s <= 80) at which the DS-DOOM time drops below the claimed level.
usage: python3 -I multi_instance.py /path/to/doom.py
"""
import sys, importlib.util, hashlib
path = sys.argv[1]
src = open(path, 'rb').read()
assert hashlib.sha256(src).hexdigest() == "d53e8bb0b668f581d4fd9538446726760bdcb4898ca232dc24a64dd473018b1d", "doom.py hash mismatch"
spec = importlib.util.spec_from_file_location("doom", path); doom = importlib.util.module_from_spec(spec); spec.loader.exec_module(doom)
dsDOOM = doom.dsDOOM

# (scheme, set, target, n, k, w, rotations)
CASES = []
for (lvl, n, wr) in [(128,16067,66),(128,20899,79),(192,32653,100),(256,52379,131),(384,104869,193),(512,173981,259)]:
    CASES.append(("HARE", f"HARE-{lvl}(n={n})", lvl, 2*n, n, 2*wr, n))
for (lvl, n, wr) in [(128,17669,75),(192,35851,114),(256,57637,149),(512,197123,297)]:
    CASES.append(("HEP-QC", f"HEP-QC-{lvl}", lvl, 2*n, n, 2*wr, n))
for (lvl, n, wr) in [(128,29443,66),(256,54493,106),(384,122579,159),(512,217901,213)]:
    CASES.append(("NSS-HQC", f"NSS-HQC-{lvl}", lvl, 2*n, n, 2*wr, n))
for (lvl, n, wr) in [(128,16301,67),(256,50363,132),(384,97651,196),(512,157627,260)]:
    CASES.append(("TriQ-KEM", f"TriQ-{lvl}", lvl, 2*n, n, 2*wr, n))
for (lvl, r, wf, wg) in [(128,13109,29,27),(192,25357,43,39),(256,41651,57,52),(384,82757,85,78),(512,135851,113,103)]:
    CASES.append(("QUBE", f"QUBE-{lvl}", lvl, 3*r, 2*r, wg+2*wf, r))
for (lvl, n, wr) in [(128,15373,(42,45,44,45)),(256,33827,(63,66,71,74)),(512,106261,(123,134,137,138))]:
    CASES.append(("Mito1", f"Mito1-{lvl}", lvl, 4*n, 2*n, sum(wr), 2*n))
for (lvl, n, wr) in [(128,14621,(42,45,44,45)),(256,32261,(63,73,66,72)),(512,102437,(126,129,136,141))]:
    CASES.append(("Mito1-E", f"Mito1-E-{lvl}", lvl, 4*n, 2*n, sum(wr), 2*n))
for (lvl, n, w2) in [(128,10253,(22,23,25,25)),(256,21523,(34,34,38,38)),(512,65293,(65,66,70,73))]:
    CASES.append(("Mito2-E", f"Mito2-E-{lvl}", lvl, 8*n, 4*n, 2*sum(w2), 4*n))
for (lvl, r, t) in [(128,12323,134),(256,40973,264),(512,150001,524)]:
    CASES.append(("BIKE-MLThre", f"BIKE-MLThre-{lvl}", lvl, 2*r, r, t, r))
for (lvl, r, t) in [(128,10301,201),(128,15581,263),(192,22003,319),(256,35363,429),(384,69691,659),(512,114043,877)]:
    CASES.append(("TRIKE", f"TRIKE(r={r})", lvl, 3*r, r, t, r))
for (lvl, n, k, w) in [(128,10070,4957,142),(256,19000,9783,256),(512,38000,19891,503)]:
    CASES.append(("QCTM", f"QCTM{lvl}", lvl, n, k, w, 19))
for (lvl, n, wr) in [(128,17669,75),(192,35851,114),(256,57637,149)]:
    CASES.append(("HQC(ref)", f"HQC-{lvl}", {128:143,192:207,256:272}[lvl], 2*n, n, 2*wr, n))

only = sys.argv[2] if len(sys.argv) > 2 else None
print("scheme set target | n k w rot | single-instance DOOM (M=rot) time/mem | first s with time<target (M=rot*2^s), time, mem | time at s=64 | time at s=80")
for (sch, lab, target, n, k, w, rot) in CASES:
    if only and only not in sch: continue
    t1, m1, _ = dsDOOM(n, k, w, rot)
    first = None
    lo, hi = 0, 80
    t80_, m80_, _ = dsDOOM(n, k, w, rot * (1 << 80))
    if t80_ < target:
        # binary search the smallest s with time < target (time is non-increasing in M)
        while lo < hi:
            mid = (lo + hi) // 2
            t, m, _ = dsDOOM(n, k, w, rot * (1 << mid))
            if t < target: hi = mid
            else: lo = mid + 1
        t, m, _ = dsDOOM(n, k, w, rot * (1 << lo)); first = (lo, t, m)
    t64, m64, _ = dsDOOM(n, k, w, rot * (1 << 64)); t80, m80, _ = dsDOOM(n, k, w, rot * (1 << 80))
    fs = f"s={first[0]} t={first[1]:.3f} mem={first[2]:.2f}" if first else "none up to 2^80"
    print(f"{sch:12s} {lab:18s} {target:4d} | [{n},{k}] w={w} rot={rot} | {t1:.3f} / {m1:.2f} | {fs} | {t64:.3f} | {t80:.3f}", flush=True)
