#!/usr/bin/env python3
"""
qctm_toy.py -- numerical verification of the structural claims about QCTM (NGCC kem-32)
on a scaled-down instance that follows the specification's key generation literally
(Algorithms 1, 3, 4 of the QCTM spec): twisted Goppa code Gamma(L, g, eta) with
g = M((x - 1/eta)^ell), support L = union of affine orbits {zeta^i a + 1/eta}.

Claims verified (all over exact finite-field arithmetic):
  (A) the 'twisted' last row (alpha^{t-1} + eta alpha^t)/g(alpha) equals eta*1 + (F_q-combination of
      the first t-1 ordinary rows alpha^i/g(alpha)), so the public code is the alternant code
      A_{t-1}(L, 1/g) intersected with the even-weight code  (no twisted structure survives);
  (B) the public code is invariant under the simultaneous cyclic shift of every orbit block;
  (C) the folded code (orbit sums) equals the binary Goppa code Gamma(X', M) ∩ E, X' = {a_O^ell};
  (D) LIFTING: from the quotient key (X', M) -- even after an unknown affine + Frobenius
      re-normalisation -- a full decoding key (U, y) for the public code is recovered by linear
      algebra over F_q (character-1 block projection), and the recovered key decodes w = (t-1)/2
      errors from the public syndrome.
usage: python3 qctm_toy.py [m] [ell] [t0] [nblocks] [seed]
"""
import sys, random, itertools
from math import log2

# ----------------------------------------------------------------------------- GF(2^m)
class GF:
    def __init__(self, m, poly):
        self.m, self.q, self.poly = m, 1 << m, poly
        self.exp = [0] * (2 * self.q); self.log = [0] * self.q
        x = 1
        for i in range(self.q - 1):
            self.exp[i] = x; self.log[x] = i
            x <<= 1
            if x & self.q: x ^= poly
        assert x == 1, "poly not primitive"
        for i in range(self.q - 1, 2 * self.q): self.exp[i] = self.exp[i - (self.q - 1)]
    def mul(self, a, b):
        if a == 0 or b == 0: return 0
        return self.exp[self.log[a] + self.log[b]]
    def inv(self, a):
        assert a != 0
        return self.exp[(self.q - 1) - self.log[a]]
    def div(self, a, b): return self.mul(a, self.inv(b))
    def pow(self, a, e):
        if e == 0: return 1
        if a == 0: return 0
        return self.exp[(self.log[a] * e) % (self.q - 1)]
    def order_elem(self, ell):
        """an element of multiplicative order ell"""
        assert (self.q - 1) % ell == 0
        return self.exp[(self.q - 1) // ell]
    def frob(self, a, k): return self.pow(a, 1 << k)
    def bits(self, a): return [(a >> i) & 1 for i in range(self.m)]

# polynomials over GF: list of coefficients, low degree first
def p_trim(p):
    while p and p[-1] == 0: p.pop()
    return p
def p_add(a, b):
    n = max(len(a), len(b)); return p_trim([(a[i] if i < len(a) else 0) ^ (b[i] if i < len(b) else 0) for i in range(n)])
def p_mul(F, a, b):
    if not a or not b: return []
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y: r[i + j] ^= F.mul(x, y)
    return p_trim(r)
def p_divmod(F, a, b):
    a = a[:]; b = p_trim(b[:]); q = [0] * max(0, len(a) - len(b) + 1)
    inv = F.inv(b[-1])
    while len(a) >= len(b) and a:
        c = F.mul(a[-1], inv); d = len(a) - len(b); q[d] = c
        for i, y in enumerate(b): a[d + i] ^= F.mul(c, y)
        p_trim(a)
    return p_trim(q), a
def p_mod(F, a, b): return p_divmod(F, a, b)[1]
def p_gcd(F, a, b):
    a, b = p_trim(a[:]), p_trim(b[:])
    while b: a, b = b, p_mod(F, a, b)
    return a
def p_eval(F, p, x):
    r = 0
    for c in reversed(p): r = F.mul(r, x) ^ c
    return r
def p_powmod(F, base, e, mod):
    r = [1]; b = p_mod(F, base, mod)
    while e:
        if e & 1: r = p_mod(F, p_mul(F, r, b), mod)
        b = p_mod(F, p_mul(F, b, b), mod); e >>= 1
    return r
def p_is_irreducible(F, g):
    """Ben-Or test over F_q: g irreducible iff gcd(g, x^{q^i} - x) = 1 for i <= deg/2"""
    d = len(g) - 1
    xq = [0, 1]
    for i in range(1, d // 2 + 1):
        xq = p_powmod(F, xq, F.q, g)
        if len(p_gcd(F, g, p_add(xq, [0, 1]))) > 1: return False
    return True
def p_compose(F, M, inner):
    """M(inner(x))"""
    r = []
    for c in reversed(M): r = p_add(p_mul(F, r, inner), [c])
    return r
def p_pow(F, p, e):
    r = [1]
    for _ in range(e): r = p_mul(F, r, p)
    return r

# ----------------------------------------------------------------------------- F_2 linear algebra on int bitsets
def rref_f2(rows, ncols):
    """returns (pivot_cols, reduced rows) of the row space; rows are ints (bit j = column j)"""
    rows = [r for r in rows if r]; piv = []; out = []
    for col in range(ncols):
        mask = 1 << col; pr = None
        for i, r in enumerate(rows):
            if r & mask: pr = i; break
        if pr is None: continue
        p = rows.pop(pr); rows = [r ^ p if r & mask else r for r in rows]
        out = [r ^ p if r & mask else r for r in out]; out.append(p); piv.append(col)
    return piv, out
def rank_f2(rows, ncols): return len(rref_f2(rows, ncols)[0])
def kernel_f2(rows, ncols):
    """basis of {c : rows . c = 0} as ints"""
    piv, red = rref_f2(rows, ncols)
    pivset = set(piv); free = [c for c in range(ncols) if c not in pivset]
    basis = []
    for f in free:
        v = 1 << f
        for p, r in zip(piv, red):
            if (r >> f) & 1: v |= 1 << p
        basis.append(v)
    return basis
def same_space_f2(A, B, ncols):
    return rank_f2(A, ncols) == rank_f2(B, ncols) == rank_f2(A + B, ncols)
def popcount(x): return bin(x).count('1')

# ----------------------------------------------------------------------------- F_q linear algebra (dense lists)
def rref_fq(F, rows, ncols):
    rows = [r[:] for r in rows]; piv = []; out = []
    for col in range(ncols):
        pr = None
        for i, r in enumerate(rows):
            if r[col]: pr = i; break
        if pr is None: continue
        p = rows.pop(pr); inv = F.inv(p[col]); p = [F.mul(inv, x) for x in p]
        def red(r):
            if r[col]:
                c = r[col]; return [x ^ F.mul(c, y) for x, y in zip(r, p)]
            return r
        rows = [red(r) for r in rows]; out = [red(r) for r in out]; out.append(p); piv.append(col)
    return piv, out
def kernel_fq(F, rows, ncols):
    piv, red = rref_fq(F, rows, ncols); pivset = set(piv)
    free = [c for c in range(ncols) if c not in pivset]; basis = []
    for f in free:
        v = [0] * ncols; v[f] = 1
        for p, r in zip(piv, red): v[p] = r[f]  # x_p = -r[f] x_f = r[f] (char 2)
        basis.append(v)
    return basis
def rank_fq(F, rows, ncols): return len(rref_fq(F, rows, ncols)[0])

# ----------------------------------------------------------------------------- the toy QCTM
def main():
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    ell = int(sys.argv[2]) if len(sys.argv) > 2 else 11
    t0 = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    nb = int(sys.argv[4]) if len(sys.argv) > 4 else 48
    seed = int(sys.argv[5]) if len(sys.argv) > 5 else 1
    jy0 = int(sys.argv[6]) if len(sys.argv) > 6 else 0   # extra Frobenius twist of the multiplier (e.g. 1: polynomial M''^2)
    random.seed(seed)
    prim = {8: 0x11d, 9: 0x211, 10: 0x409, 11: 0x805, 12: 0x1053}[m]
    F = GF(m, prim); q = F.q
    assert (q - 1) % ell == 0 and ell % 2 == 1
    t = ell * t0; n = ell * nb; w = (t - 1) // 2; u = m * (t - 1) + 1
    assert m * ell * t0 < n <= q and t0 % 2 == 1
    zeta = F.order_elem(ell)
    print(f"toy QCTM: m={m} q={q} ell={ell} t0={t0} t={t} n={n} w={w} u=m(t-1)+1={u} k=n-u={n-u}  zeta=exp[{(q-1)//ell}]")

    # --- Algorithm 1: eta, M irreducible of degree t0, g = M((x-1/eta)^ell) irreducible of degree t
    while True:
        eta = random.randrange(1, q)
        M = [random.randrange(q) for _ in range(t0)] + [1]
        if not p_is_irreducible(F, M): continue
        inner = p_pow(F, [F.inv(eta), 1], ell)          # (x - 1/eta)^ell  (char 2: x + 1/eta)
        g = p_compose(F, M, inner)
        if p_is_irreducible(F, g): break
    assert len(g) == t + 1 and g[-1] == 1
    print(f"eta={eta}  M=deg {t0} irreducible, g=M((x-1/eta)^ell) irreducible of degree {t}; g_(t-1)={g[t-1]}  1/eta={F.inv(eta)}  (equal: {g[t-1]==F.inv(eta)})")

    # --- Algorithm 3: support = nb disjoint affine orbits {zeta^i a + 1/eta}
    ieta = F.inv(eta); used = set(); reps = []
    while len(reps) < nb:
        a = random.randrange(1, q)
        if a in used: continue
        orb = [F.mul(F.pow(zeta, i), a) for i in range(ell)]
        used.update(orb); reps.append(a)
    a_rep = reps
    U = [F.mul(F.pow(zeta, i), a) for a in a_rep for i in range(ell)]   # u-coordinates: u = alpha - 1/eta
    L = [x ^ ieta for x in U]                                          # alpha = zeta^i a + 1/eta
    assert len(set(L)) == n and all(p_eval(F, g, al) != 0 for al in L)
    blk = lambda j: (j // ell, j % ell)

    # --- Algorithm 4: H_T over F_q (t x n): rows alpha^i/g(alpha), i<t-1, and (alpha^{t-1}+eta alpha^t)/g(alpha)
    ginv = [F.inv(p_eval(F, g, al)) for al in L]
    HT = []
    for i in range(t - 1): HT.append([F.mul(F.pow(al, i), gi) for al, gi in zip(L, ginv)])
    last = [F.mul(F.pow(al, t - 1) ^ F.mul(eta, F.pow(al, t)), gi) for al, gi in zip(L, ginv)]
    # (A): last - eta*1 in span of first t-1 rows
    tgt = [x ^ eta for x in last]
    rk1 = rank_fq(F, HT, n); rk2 = rank_fq(F, HT + [tgt], n)
    print(f"(A) rank(first t-1 rows)={rk1}, rank(with last-eta*1)={rk2} -> twisted row = eta*1 + combination of ordinary rows: {rk1==rk2}")
    # so the spec's H_T row space = span(first t-1 rows) + <all-ones>  (over F_q); binary expansion:
    Hbin = []
    for row in HT:
        for b in range(m):
            Hbin.append(sum(((x >> b) & 1) << j for j, x in enumerate(row)))
    Hbin.append((1 << n) - 1)
    rk = rank_f2(Hbin, n); print(f"binary expansion: {len(Hbin)} rows, rank {rk} (= u: {rk==u})")
    C = kernel_f2(Hbin, n); k = len(C); print(f"public code C: [n={n}, k={k}]")
    # also check the spec's own matrix (with the twisted row expanded instead) gives the same binary code
    Hbin_spec = Hbin[:-1] + [sum(((x >> b) & 1) << j for j, x in enumerate(last)) for b in range(m)]
    print(f"    code from the spec's twisted matrix (twisted row expanded, no explicit parity): same code? {same_space_f2(Hbin_spec, Hbin, n)} (rank {rank_f2(Hbin_spec, n)})")

    # (B): invariance under the simultaneous block shift sigma: (O,i) -> (O,i+1)
    def shift(c, s=1):
        r = 0
        for j in range(n):
            if (c >> j) & 1:
                O, i = blk(j); r |= 1 << (O * ell + (i + s) % ell)
        return r
    inv_ok = all(all(popcount(h & shift(c)) % 2 == 0 for h in Hbin) for c in C)
    print(f"(B) sigma(C) = C: {inv_ok}")

    # (C): folded code = Gamma(X', M) ∩ E,  X' = {a_O^ell}
    def fold(c):
        r = 0
        for O in range(nb):
            if popcount((c >> (O * ell)) & ((1 << ell) - 1)) % 2: r |= 1 << O
        return r
    folded = [fold(c) for c in C]
    Xp = [F.pow(a, ell) for a in a_rep]; Minv = [F.inv(p_eval(F, M, x)) for x in Xp]
    Hq = [[F.mul(F.pow(x, i), mi) for x, mi in zip(Xp, Minv)] for i in range(t0)]
    Hg = [sum(((x >> b) & 1) << j for j, x in enumerate(row)) for row in Hq for b in range(m)] + [(1 << nb) - 1]
    Goppa_E = kernel_f2(Hg, nb)
    print(f"(C) folded code: dim {rank_f2(folded, nb)};  Gamma(X',M)∩E: [{nb}, {len(Goppa_E)}];  equal: {same_space_f2(folded, Goppa_E, nb)}")

    # ------------------------------------------------------------------ (D) LIFTING ATTACK
    # public key: H_pub = Q * tau(Hbin) with random invertible Q and random block permutation tau
    tau = list(range(nb)); random.shuffle(tau)      # public block O' = tau[O]... we relabel columns
    def permute_cols(r):
        out = 0
        for j in range(n):
            if (r >> j) & 1:
                O, i = blk(j); out |= 1 << (tau[O] * ell + i)
        return out
    Hperm = [permute_cols(r) for r in Hbin]
    while True:
        Q = [random.getrandbits(u) for _ in range(u)]
        if rank_f2(Q, u) == u: break
    Hpub = []
    for i in range(u):
        r = 0
        for j in range(u):
            if (Q[i] >> j) & 1: r ^= Hperm[j]
        Hpub.append(r)
    print(f"public key: {u} x {n} binary matrix (random invertible row mixing, random block permutation)")

    # the quotient key handed to the attacker: (X'', M'') = equivalent Goppa key for the folded code,
    # i.e. X'' = (alpha0*X' + beta0)^(2^j0) in the *public* block order, M'' accordingly (unknown to attacker)
    alpha0, beta0, j0 = random.randrange(1, q), random.randrange(q), random.randrange(m)
    Xpp = [0] * nb; ypp = [0] * nb
    for O in range(nb):
        x = F.frob(F.mul(alpha0, Xp[O]) ^ beta0, j0); Xpp[tau[O]] = x
        ypp[tau[O]] = F.frob(Minv[O], (j0 + jy0) % m)   # 1/M(x_O) conjugated (+ optional extra twist jy0)
    print(f"attacker is given the folded Goppa key up to equivalence: X''=(alpha X'+beta)^(2^j0), (alpha,beta,j0)=({alpha0},{beta0},{j0}); multiplier twisted by extra 2^{jy0}")

    # character-1 projection of the public dual code (over F_q), with the public zeta: K1 = P_1(rowspace_Fq(Hpub))
    def proj1(r):
        out = []
        for O in range(nb):
            s = 0
            for i in range(ell):
                if (r >> (O * ell + i)) & 1: s ^= F.pow(zeta, (-i) % ell)
            out.append(s)
        return out
    K1 = [proj1(r) for r in Hpub]
    K1perp = kernel_fq(F, K1, nb)
    print(f"character-1 projection of the public dual: dim K1 = {rank_fq(F, K1, nb)} (predicted <= sum_k (d_k+1) = {sum((t-2-pow(2,-kk,ell))//ell + 1 for kk in range(m))}), dim K1^perp = {len(K1perp)}")
    # step 1: re-normalise so that the support consists of ell-th powers (find beta: all (x-beta) in one coset of the ell-th powers)
    e_ell = (q - 1) // ell
    is_pow = lambda x: x != 0 and F.pow(x, e_ell) == 1
    cands = []
    for beta in range(q):
        if beta in Xpp: continue
        x0 = Xpp[0] ^ beta
        if all(is_pow(F.div(x ^ beta, x0)) for x in Xpp[1:]): cands.append(beta)
    print(f"step 1: translations beta making X''-beta a single coset of (F_q^*)^ell: {cands}")
    # for each candidate beta and the scaling alpha = x0 (any representative of the coset): X_att = (X''-beta)/x0 subset of ell-th powers
    attacker_success = False
    for beta in cands:
        x0 = Xpp[0] ^ beta
        Xatt = [F.div(x ^ beta, x0) for x in Xpp]
        assert all(is_pow(x) for x in Xatt)
        # multiplier: y'' = c/M''(x'') ; after the affine change the multiplier is the same vector up to a constant (Goppa code unchanged)
        yatt = ypp[:]
        # the Frobenius twist j0 is unknown: try all j (hypothesis: support U^{2^j}); work with X_att^{2^(-j)} and y^{2^(-j)}
        for (j, jy) in ([(j, j) for j in range(m)] if jy0 == 0 else [(j, jy) for j in range(m) for jy in range(m)]):
            X = [F.frob(x, (m - j) % m) for x in Xatt]; y = [F.frob(x, (m - jy) % m) for x in yatt]
            # ell-th roots b_O of x_O (any choice)
            b = [F.exp[F.log[x] // ell] for x in X]           # (log x divisible by ell since x is an ell-th power)
            assert all(F.pow(bb, ell) == xx for bb, xx in zip(b, X))
            # E_1 = sum_k x^{(e_k 2^k - 1)/ell} y^{2^k} GRS_{d_k+1}(X^{2^k}),  e_k = 2^{-k} mod ell, d_k = floor((t-2-e_k)/ell)
            E1 = []
            for kk in range(m):
                ek = pow(2, -kk, ell); dk = (t - 2 - ek) // ell
                xe = (ek * (1 << kk) - 1) // ell
                for h in range(dk + 1):
                    E1.append([F.mul(F.mul(F.pow(x, xe), F.frob(yy, kk)), F.pow(F.frob(x, kk), h)) for x, yy in zip(X, y)])
            K2 = [[F.mul(bb, v) for bb, v in zip(b, row)] for row in E1]
            # solve for rho: sum_O rho_O v_O w_O = 0 for v in K2, w in K1perp
            eqs = [[F.mul(vO, wO) for vO, wO in zip(v, wv)] for v in K2 for wv in K1perp]
            sol = kernel_fq(F, eqs, nb) if eqs else []
            if len(sol) != 1:
                continue
            rho = sol[0]
            # normalise rho_0 = 1 and check all entries are ell-th roots of unity
            r0 = F.inv(rho[0]); rho = [F.mul(r0, x) for x in rho]
            roots_ok = all(F.pow(x, ell) == 1 for x in rho)
            print(f"  beta={beta} j={j} jy={jy}: dim K1={rank_fq(F,K1,nb)} dim K2={rank_fq(F,K2,nb)} -> unique rho; entries in mu_ell: {roots_ok}")
            if not roots_ok: continue
            # lifted key: U_att[(O,i)] = zeta^i * rho_O * b_O ; y_att[(O,i)] = y_O
            Uatt = [0] * n; Yatt = [0] * n
            for O in range(nb):
                for i in range(ell):
                    Uatt[O * ell + i] = F.mul(F.pow(zeta, i), F.mul(rho[O], b[O])); Yatt[O * ell + i] = y[O]
            # verify: the alternant code A_{t-1}(Uatt, Yatt) ∩ E equals the public code
            Hatt_q = [[F.mul(F.pow(uu, i), yy) for uu, yy in zip(Uatt, Yatt)] for i in range(t - 1)]
            Hatt = [sum(((x >> bb) & 1) << jj for jj, x in enumerate(row)) for row in Hatt_q for bb in range(m)] + [(1 << n) - 1]
            same = same_space_f2(Hatt, Hpub, n)
            print(f"     lifted key: A_(t-1)(U_att, y_att) ∩ E == public code: {same}")
            if not same: continue
            # decode: random error of weight w, public syndrome s = Hpub e^T ; attacker maps to its own syndromes
            e = 0
            for pos in random.sample(range(n), w): e |= 1 << pos
            s = sum((popcount(h & e) % 2) << i for i, h in enumerate(Hpub))
            # express Hpub rows in terms of Hatt rows: Hpub = Qp * Hatt  (solve over F_2)
            # we need Hatt e^T = Qp^{-1} s: solve Qp from Hpub = Qp Hatt via rref of Hatt with tracking
            piv, red = rref_f2(Hatt, n)
            # build transformation: do elimination on augmented rows [row | identity]
            aug = [(Hatt[i], 1 << i) for i in range(u)]; piv2 = []; out2 = []
            rows2 = aug[:]
            for col in range(n):
                mask = 1 << col; pr = None
                for ii, (r, tr) in enumerate(rows2):
                    if r & mask: pr = ii; break
                if pr is None: continue
                p = rows2.pop(pr)
                rows2 = [(r ^ p[0], tr ^ p[1]) if r & mask else (r, tr) for (r, tr) in rows2]
                out2 = [(r ^ p[0], tr ^ p[1]) if r & mask else (r, tr) for (r, tr) in out2]
                out2.append(p); piv2.append(col)
            # each Hpub row = sum over reduced rows with pivot bits set -> combination of Hatt rows (tr)
            # syndrome wrt Hatt: s_att_i = <Hatt_i, e>; we know <Hpub_r, e> = s_r. Hpub_r = sum_{reduced p: bit piv set} red_p = sum (tr_p) Hatt
            # so s_r = sum_p [Hpub_r has pivot p] * <red_p, e>, and <red_p, e> = sum_i tr_p[i] s_att_i. Solve for s_att (u unknowns, u equations).
            A = []; rhs = []
            for r_idx in range(u):
                hr = Hpub[r_idx]; comb = 0
                for (rr, tr), pc in zip(out2, piv2):
                    if (hr >> pc) & 1: comb ^= tr
                A.append(comb); rhs.append((s >> r_idx) & 1)
            # solve A * s_att = rhs over F_2
            aug3 = [A[i] | (rhs[i] << u) for i in range(u)]
            pv, rd = rref_f2(aug3, u + 1)
            assert u not in pv, "inconsistent"
            s_att = 0
            for pc, rr in zip(pv, rd):
                if (rr >> u) & 1: s_att |= 1 << pc
            # F_q syndromes S_i = sum_j e_j y_j u_j^i, i < t-1
            S = []
            for i in range(t - 1):
                val = 0
                for bb in range(m):
                    if (s_att >> (i * m + bb)) & 1: val |= 1 << bb
                S.append(val)
            # sanity: compare with true syndromes computed from e and (Uatt, Yatt)
            S_true = [0] * (t - 1)
            for j in range(n):
                if (e >> j) & 1:
                    for i in range(t - 1): S_true[i] ^= F.mul(Yatt[j], F.pow(Uatt[j], i))
            assert S == S_true, "syndrome mapping failed"
            # Berlekamp-Massey on S_0..S_{2w-1}
            Lam = [1]; B = [1]; Lc = 0; mm = 1; bconst = 1
            for r_ in range(2 * w):
                d = S[r_]
                for i in range(1, Lc + 1):
                    if i < len(Lam): d ^= F.mul(Lam[i], S[r_ - i])
                if d == 0:
                    mm += 1
                else:
                    T = Lam[:]
                    coef = F.div(d, bconst)
                    shiftB = [0] * mm + B
                    Lam = p_add(Lam, [F.mul(coef, x) for x in shiftB])
                    if 2 * Lc <= r_:
                        Lc = r_ + 1 - Lc; B = T; bconst = d; mm = 1
                    else:
                        mm += 1
            # Chien search: roots of Lam(z) at z = 1/u_j
            found = 0
            for j in range(n):
                if p_eval(F, Lam, F.inv(Uatt[j])) == 0: found |= 1 << j
            print(f"     decoding with the lifted key: error weight {w}, locator degree {len(Lam)-1}, recovered e == e: {found == e}")
            attacker_success = found == e
            if attacker_success: break
        if attacker_success: break
    print(f"(D) lifting + decoding succeeded: {attacker_success}")

if __name__ == '__main__':
    main()
