"""NSS-HQC key-recovery instances [2n, n] weight 2*w_sk, against the specification's
T_key = 1.0969*sqrt(n) extrapolation (Table 7 / Table 8 of the NSS-HQC specification)."""
import time
from math import log2, sqrt
from cryptographic_estimators.SDEstimator import SDEstimator
from cryptographic_estimators.SDEstimator.SDAlgorithms import BJMMdw, BJMMpdw, BothMay
EX = [BJMMdw, BJMMpdw, BothMay]
for (lvl, n, wsk) in [(128,29443,73),(256,54493,117),(384,122579,175),(512,217901,233)]:
    t0 = time.time()
    e = SDEstimator(n=2*n, k=n, w=2*wsk, excluded_algorithms=EX); r = e.estimate()
    best = min((v['estimate']['time'], a) for a, v in r.items() if v['estimate']['time'] is not None)
    disc = 0.5*log2(n); spec = 1.0969*sqrt(n)
    print(f"NSS-HQC-{lvl}: SD({2*n},{n},{2*wsk}) raw {best[0]:7.2f} ({best[1]}) | -disc {best[0]-disc:7.2f} "
          f"| spec 1.0969*sqrt(n) = {spec:6.1f} | target {lvl} | raw-spec {best[0]-spec:+7.2f} "
          f"| vs target {best[0]-disc-lvl:+7.2f} | {time.time()-t0:.0f}s", flush=True)
