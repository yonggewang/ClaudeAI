#!/usr/bin/env python3
"""Remediation analysis for the NGCC 'below claimed level' multi-instance findings.
For each case we report the DS-DOOM message cost at the full Q = 2^80 same-key
budget, the deficit (target - cost@2^80) = bits of single-instance margin that
must be added, and -- for TRIKE -- a concrete repaired length r that restores
message security >= target after 2^80 ciphertexts (error density held at the
scheme's level-1 value).
usage: python3 -I remediation.py /path/to/doom.py
"""
import sys, importlib.util, hashlib
path = sys.argv[1]
src = open(path, 'rb').read()
assert hashlib.sha256(src).hexdigest() == "d53e8bb0b668f581d4fd9538446726760bdcb4898ca232dc24a64dd473018b1d", "doom.py hash mismatch"
spec = importlib.util.spec_from_file_location("doom", path); doom = importlib.util.module_from_spec(spec); spec.loader.exec_module(doom)
dsDOOM = doom.dsDOOM

def cost(n, k, w, rot, s):
    t, m, _ = dsDOOM(n, k, w, rot * (1 << s)); return t

# multi-instance cases that cross within 2^80 (scheme, label, target, n, k, w, rot)
CASES = [
    ("TRIKE",       "TRIKE-1 (r=10301)", 128, 30903, 10301, 201, 10301),
    ("TRIKE",       "TRIKE-3 (r=22003)", 192, 66009, 22003, 319, 22003),
    ("TRIKE",       "TRIKE-5 (r=35363)", 256, 106089, 35363, 429, 35363),
    ("QUBE",        "QUBE-128",          128, 39327, 26218, 83, 13109),
    ("HARE",        "HARE-1 (n=16067)",  128, 32134, 16067, 132, 16067),
    ("BIKE-MLThre", "BIKE-MLThre-128",   128, 24646, 12323, 134, 12323),
    ("BIKE-MLThre", "BIKE-MLThre-256",   256, 81946, 40973, 264, 40973),
]
print("=== DS-DOOM cost at the full Q=2^80 budget, and the margin deficit ===")
print(f"{'case':22s} {'target':>6} {'single':>8} {'cost@2^64':>9} {'cost@2^80':>9} {'deficit':>8}")
for (sch, lab, tg, n, k, w, rot) in CASES:
    s1, _, _ = dsDOOM(n, k, w, rot)
    c64 = cost(n,k,w,rot,64); c80 = cost(n,k,w,rot,80)
    print(f"{lab:22s} {tg:6d} {s1:8.2f} {c64:9.2f} {c80:9.2f} {max(0,tg-c80):8.2f}")

print("\n=== concrete TRIKE repair: smallest length r (error density fixed at TRIKE-1's 201/10301) ===")
print("    keeping message security >= target after Q = 2^80 same-key ciphertexts")
dens = 201/10301
for (base_r, tg, name) in [(10301,128,"TRIKE-1")]:
    r = base_r
    # grow r until cost@2^80 >= target
    while True:
        t = max(1, round(dens*r))
        c = cost(3*r, r, t, r, 80)
        if c >= tg:
            break
        r = int(r*1.02)+1
    print(f"{name}: repaired r={r} (x{r/base_r:.2f}), t={round(dens*r)}, [3r,r]=[{3*r},{r}], "
          f"cost@2^80={c:.2f} >= {tg}; ciphertext/key grow ~x{r/base_r:.2f}")
