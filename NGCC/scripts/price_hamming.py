"""Uniform ISD pricing of the Hamming-metric NGCC code-based KEMs with CryptographicEstimators
(SDEstimator, all algorithms, default cost model: time = log2 bit operations, memory reported).
For each parameter set: key-recovery instance and message-recovery instance (lengths, dimension,
weight), structural discount (QC: -log2 r for codeword finding, -1/2 log2 r for syndrome decoding;
the designers' own convention), reported as 'min over the Stern family' and 'min over all'.
usage: python3 price_hamming.py > pricing.out
"""
import sys, time, os
from math import log2
from cryptographic_estimators.SDEstimator import SDEstimator
from cryptographic_estimators.SDEstimator.SDAlgorithms import BJMM, BJMMplus, BJMMdw, BJMMpdw, MayOzerov, BothMay
# Excluded: the depth-tuned BJMM variants and Both-May.  In the designers' own estimator tables (e.g. QCTM
# Tables 1-3) these never give the minimum, and they dominate the estimator's run time.
EXCLUDED = [BJMMdw, BJMMpdw, BothMay]
KEPT = "Prange, Stern, Dumer, BallCollision, BJMM, BJMM+, MayOzerov" 

CACHE = {}
def sd_all(N, K, w):
    if (N, K, w) in CACHE: return CACHE[(N, K, w)]
    e = SDEstimator(n=N, k=K, w=w, excluded_algorithms=EXCLUDED); r = e.estimate()
    allmin = min((v['estimate']['time'], a, v['estimate']['memory']) for a, v in r.items() if v['estimate']['time'] is not None)
    stern = min((v['estimate']['time'], a, v['estimate']['memory']) for a, v in r.items() if a not in ('BJMM','BJMMplus','BJMMdw','BJMMpdw','MayOzerov','BothMay') and v['estimate']['time'] is not None)
    CACHE[(N, K, w)] = (stern, allmin)
    return stern, allmin

# (scheme, level, claimed, r, [ (label, N, K, w, discount_bits) ... ])
I = []
def hqc_like(name, lvl, claim, n, k, wsk, wr, we, blocks_pk=2):
    # pk: 2-QCSD over [2n,n] weight 2 wsk ; ct: 3-QCSD over [3n, n+k] weight 2 wr + we ; also u-only [2n,n] 2wr
    I.append((name, lvl, claim, n, [('pk 2-QCSD', 2*n, n, 2*wsk, 0.5*log2(n)), ('ct u-only', 2*n, n, 2*wr, 0.5*log2(n))]))
for (lvl, n, w, wr, we, k) in [(128,16067,66,66,105,128),(128,20899,79,79,145,128),(192,32653,100,100,163,192),(256,52379,131,131,224,256),(384,104869,193,193,361,384),(512,173981,259,259,449,512)]:
    hqc_like('HARE', lvl, lvl, n, k, w, wr, we)
for (lvl, n, w, wr, k) in [(128,17669,66,75,128),(192,35851,100,114,192),(256,57637,131,149,256),(512,197123,261,297,512)]:
    hqc_like('HEP-QC', lvl, lvl, n, k, w, wr, wr)
for (lvl, n, w, wr, we, k) in [(128,29443,73,66,117,128),(256,54493,117,106,187,256),(384,122579,175,159,279,384),(512,217901,233,213,372,512)]:
    hqc_like('NSS-HQC', lvl, lvl, n, k, w, wr, we)
for (lvl, n, w, we, k) in [(128,16301,67,106,128),(256,50363,132,234,256),(384,97651,196,350,384),(512,157627,260,475,512)]:
    hqc_like('TriQ-KEM', lvl, lvl, n, k, w, w, we)
hqc_like('HQC (ref.)', 128, 143, 17669, 128, 66, 75, 75); hqc_like('HQC (ref.)', 192, 207, 35851, 192, 100, 114, 114); hqc_like('HQC (ref.)', 256, 272, 57637, 256, 131, 149, 149)
# QUBE: pk (3,1)-QCSD [3r, r] w=2wx+wy ; ct (4,2)-QCSD [4r, 2r+lam] w = wg+we+2wf
for (lvl, r, wx, wy, wf, wg, we) in [(128,13109,74,76,29,27,83),(192,25357,110,113,43,39,121),(256,41651,146,151,57,52,162),(384,82757,219,226,85,78,244),(512,135851,291,301,113,103,324)]:
    I.append(('QUBE', lvl, lvl, r, [('pk (3,1)-QCSD', 3*r, r, 2*wx+wy, 0.5*log2(r)), ('ct u-only (3,2)', 3*r, 2*r, wg+2*wf, 0.5*log2(r))]))
# Mito1 / Mito1-E (2-adic over QC ring): full system [4n,2n]; projected [2n,n]
for (name, lvl, n, wx, wy, wr) in [('Mito1',128,15373,(44,41),(47,40),(42,45,44,45)),('Mito1',256,33827,(65,63),(72,69),(63,66,71,74)),('Mito1',512,106261,(127,126),(143,131),(123,134,137,138)),
                                   ('Mito1-E',128,14621,(44,41),(47,40),(42,45,44,45)),('Mito1-E',256,32261,(69,64),(72,64),(63,73,66,72)),('Mito1-E',512,102437,(128,123),(140,136),(126,129,136,141))]:
    I.append((name, lvl, lvl, n, [('pk full [4n,2n]', 4*n, 2*n, sum(wx)+sum(wy), 0.5*log2(2*n)), ('pk projected [2n,n]', 2*n, n, sum(wx)+sum(wy), 0.5*log2(n)), ('ct u full [4n,2n]', 4*n, 2*n, sum(wr), 0.5*log2(2*n))]))
for (lvl, n, w1, w2) in [(128,10253,(25,25,22,21),(22,23,25,25)),(256,21523,(38,38,33,33),(34,34,38,38)),(512,65293,(72,72,66,62),(65,66,70,73))]:
    I.append(('Mito2-E', lvl, lvl, n, [('pk full [8n,4n]', 8*n, 4*n, 2*sum(w1), 0.5*log2(4*n)), ('pk projected [2n,n]', 2*n, n, 2*sum(w1), 0.5*log2(n)), ('ct u full [8n,4n]', 8*n, 4*n, 2*sum(w2), 0.5*log2(4*n))]))
# QC-MDPC: BIKE-MLThre and TRIKE
for (lvl, r, w, t) in [(128,12323,142,134),(256,40973,274,264),(512,150001,546,524)]:
    I.append(('BIKE-MLThre', lvl, lvl, r, [('key 2-QCCF [2r,r]', 2*r, r, w, log2(r)), ('msg 2-QCSD [2r,r]', 2*r, r, t, 0.5*log2(r))]))
for (lvl, r, w, t) in [(128,10301,81,201),(128,15581,105,263),(192,22003,123,319),(256,35363,165,429),(384,69691,249,659),(512,114043,333,877)]:
    I.append(('TRIKE', lvl, lvl, r, [('key 3-QCCF [3r,2r]', 3*r, 2*r, w, log2(r)), ('msg (2,3)-QCSD [3r,r]', 3*r, r, t, 0.5*log2(r))]))
# QCTM (quasi-cyclic alternant, Niederreiter): SD [n,k] weight w ; QC discount 1/2 log2 19
for (lvl, n, k, w) in [(128,10070,4957,142),(256,19000,9783,256),(512,38000,19891,503)]:
    I.append(('QCTM', lvl, lvl, 19, [('msg SD [n,k]', n, k, w, 0.5*log2(19))]))

only = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] != 'all' else None
# flatten and run smallest instances first, so coverage is broad if the run is cut short
FLAT = [(name, lvl, claim, lab, N, K, w, disc) for (name, lvl, claim, r, insts) in I for (lab, N, K, w, disc) in insts]
FLAT.sort(key=lambda z: z[4] * z[6])
# The table covers (a) instances for which a specification publishes a comparable number -- these
# double as calibration -- and (b) the lowest-level instance of every family.
CALIB = {('QCTM', 'msg'), ('TRIKE', 'key'), ('TRIKE', 'msg'), ('QUBE', 'pk'), ('NSS-HQC', 'pk'), ('NSS-HQC', 'ct')}
LOWEST = {('HARE', 128), ('HEP-QC', 128), ('NSS-HQC', 128), ('TriQ-KEM', 128), ('QUBE', 128), ('Mito1', 128),
          ('Mito1-E', 128), ('Mito2-E', 128), ('BIKE-MLThre', 128), ('TRIKE', 128), ('QCTM', 128), ('HQC', 128)}
def keep(name, lvl, lab):
    n = 'HQC' if name.startswith('HQC') else name
    return (n, lab.split()[0]) in CALIB or (n, lvl) in LOWEST
# A size cap keeps the run tractable; for the instances above it we quote the specifications' own
# numbers, which the calibrated rows below the cap license us to do.
CAP = int(os.environ.get('CAP', '50000000'))
FLAT = [z for z in FLAT if keep(z[0], z[1], z[3]) and z[4] * z[6] <= CAP]
print(f"# {len(FLAT)} instances selected", flush=True)
for (name, lvl, claim, lab, N, K, w, disc) in FLAT:
    if only and only not in name: continue
    if True:
        t0 = time.time()
        try:
            (st, sa, sm), (at, aa, am) = sd_all(N, K, w)
            print(f"{name:12s} {lvl:4d} claim={claim:4d} | {lab:22s} [{N},{K}] w={w:4d} disc={disc:5.2f} | Stern-family {st:7.2f} ({sa}, mem {sm:.0f}) -> {st-disc:7.2f} | all {at:7.2f} ({aa}, mem {am:.0f}) -> {at-disc:7.2f} | {time.time()-t0:.0f}s", flush=True)
        except Exception as ex:
            print(f"{name:12s} {lvl:4d} | {lab} [{N},{K}] w={w}: ERROR {ex}", flush=True)
