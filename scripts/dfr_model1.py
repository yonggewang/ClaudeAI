#!/usr/bin/env python3
"""HQC 'Model 1' DFR calculator (independent-Bernoulli coordinates), with HQC's Proposition 6.1.4 improved
bound for the duplicated RM[n_in, 8, n_in/2] internal code and the RS outer bound (HQC Theorem 6.1).
Validated against HQC-1/3/5 (QUBE spec Table 8: 132.89 / 193.86 / 260.59) and QUBE Table 7.
"""
from mpmath import mp, mpf, binomial, log, fsum
from math import comb
mp.dps = 60

def p_tilde(r, wu, wv):
    """Bernoulli parameter of a coordinate of u*v in F2[x]/(x^r-1), wt(u)=wu, wt(v)=wv (HQC Prop 6.1.1)"""
    num = mpf(0)
    for t in range(1, min(wu, wv) + 1, 2):
        num += binomial(r, t) * binomial(r - t, wu - t) * binomial(r - wu, wv - t)
    return num / (binomial(r, wu) * binomial(r, wv))

def p_odd(ps):
    """probability that a sum of independent Bernoulli(p_i) bits is 1"""
    prod = mpf(1)
    for p in ps: prod *= (1 - 2 * p)
    return (1 - prod) / 2

def rm_internal_dfr(n_in, p):
    """HQC Prop 6.1.4 upper bound, RM[n_in, 8, d=n_in/2] duplicated code"""
    d = n_in // 2; h = d // 2
    total = mpf(0)
    for i in range(h, n_in + 1):
        c1 = mpf(255) / 2 * binomial(d, h) * binomial(d, i - h) if 0 <= i - h <= d else mpf(0)
        c2 = mpf(0)
        for j in range(h + 1, d + 1):
            if 0 <= i - j <= d: c2 += binomial(d, j) * binomial(d, i - j)
        c2 *= 255
        c3 = mpf(0)
        for j in range(0, h + 1):
            if 0 <= i - d + j <= h: c3 += binomial(h, j) ** 3 * binomial(h, i - d + j)
        c3 *= binomial(255, 2) / 2
        Ci = min(binomial(n_in, i), c1 + c2 + c3)
        total += Ci * mpf(p) ** i * (1 - mpf(p)) ** (n_in - i)
    return total

def rs_external_dfr(n_e, delta, p_in):
    total = mpf(0)
    for j in range(delta + 1, n_e + 1):
        total += binomial(n_e, j) * p_in ** j * (1 - p_in) ** (n_e - j)
    return total

def model1(r, products, we, n1, k1, n2, label=""):
    ps = [p_tilde(r, wu, wv) for (wu, wv) in products] + [mpf(we) / r]
    p = p_odd(ps)
    pin = rm_internal_dfr(n2, p)
    delta = (n1 - k1) // 2
    dfr = rs_external_dfr(n1, delta, pin)
    print(f"{label:12s} r={r} products={products} we={we} RS[{n1},{k1}] delta={delta} RM n2={n2} | p*={float(p):.6e} log2 p_in={float(log(pin,2)):.3f} | log2 DFR = {float(log(dfr,2)):.3f}", flush=True)
    return dfr

if __name__ == '__main__':
    # HQC reference (QUBE spec Table 8 expects 132.89 / 193.86 / 260.59)
    model1(17669, [(66, 75), (66, 75)], 75, 46, 16, 384, "HQC-1")
    model1(35851, [(100, 114), (100, 114)], 114, 56, 24, 640, "HQC-3")
    model1(57637, [(131, 149), (131, 149)], 149, 90, 32, 640, "HQC-5")
    # QUBE Table 7 expects 137.5 / 200.1 / 264.3 / 392.4 / 520.6
    for (lab, r, wx, wy, wf, wg, we, n1, k1, n2) in [("QUBE-128", 13109, 74, 76, 29, 27, 83, 34, 16, 384), ("QUBE-192", 25357, 110, 113, 43, 39, 121, 66, 24, 384),
                                                       ("QUBE-256", 41651, 146, 151, 57, 52, 162, 108, 32, 384), ("QUBE-384", 82757, 219, 226, 85, 78, 244, 128, 48, 640),
                                                       ("QUBE-512", 135851, 291, 301, 113, 103, 324, 150, 64, 896)]:
        model1(r, [(wx, wf), (wx, wf), (wy, wg)], we, n1, k1, n2, lab)
