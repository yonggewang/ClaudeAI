#!/usr/bin/env python3
"""Toy experiment: MaxMinors modelling of the Rank Support Learning problem (N syndromes / received words with a common
support of dimension r). Stacks the MM equations of all N instances (same unknowns: the maximal minors c_T of the common
coefficient matrix C in F_q^{r x n}) and measures the F_q-rank of the system as a function of N, against the number of
unknowns C(n, r). If rank reaches C(n,r)-1 the support (hence the key) is recovered by linear algebra alone (no hybrid
guessing). usage: python3 rsl_toy.py m n k r Nmax [seed]"""
import sys, random, itertools
sys.path.insert(0, '/home/claude/ngcc/work')
from qctm_toy import GF, rref_fq, rank_fq, kernel_fq, rank_f2

def det(F, M):
    """determinant over GF via Gaussian elimination; M square list of lists"""
    M = [row[:] for row in M]; n = len(M); d = 1
    for c in range(n):
        p = next((i for i in range(c, n) if M[i][c]), None)
        if p is None: return 0
        if p != c: M[c], M[p] = M[p], M[c]
        d = F.mul(d, M[c][c]); inv = F.inv(M[c][c])
        for i in range(c + 1, n):
            if M[i][c]:
                f = F.mul(M[i][c], inv)
                M[i] = [x ^ F.mul(f, y) for x, y in zip(M[i], M[c])]
    return d

def main():
    m, n, k, r, Nmax = map(int, sys.argv[1:6]); seed = int(sys.argv[6]) if len(sys.argv) > 6 else 1
    random.seed(seed)
    prim = {8: 0x11d, 9: 0x211, 10: 0x409, 11: 0x805, 12: 0x1053, 13: 0x201b}[m]
    F = GF(m, prim); q = F.q
    # random [n,k] code over F_{q^m}: parity-check H ((n-k) x n), systematic
    H = [[1 if j == i else 0 for j in range(n - k)] + [random.randrange(q) for _ in range(k)] for i in range(n - k)]
    # common support: C in F_2^{r x n} full rank
    while True:
        C = [[random.randrange(2) for _ in range(n)] for _ in range(r)]
        if rank_fq(F, C, n) == r: break
    Ts = list(itertools.combinations(range(n), r))
    true_c = [det(F, [[C[i][j] for j in T] for i in range(r)]) for T in Ts]   # maximal minors of C (in F_2)
    assert any(true_c)
    rows_all = []
    print(f"RSL toy: q=2 m={m} n={n} k={k} r={r}; unknowns C(n,r)={len(Ts)}; equations per instance m*C(n-k-1,r)={m*len(list(itertools.combinations(range(n-k-1), r)))}")
    for inst in range(1, Nmax + 1):
        S = [random.randrange(1, q) for _ in range(r)]
        e = [0] * n
        for j in range(n):
            for i in range(r):
                if C[i][j]: e[j] ^= S[i]
        # received word y = codeword + e ; codeword: random message times generator (G = [R^T | I_k] since H = [I | R])
        msg = [random.randrange(q) for _ in range(k)]
        cw = [0] * n
        for j in range(k): cw[n - k + j] = msg[j]
        for i in range(n - k):
            v = 0
            for j in range(k):
                if H[i][n - k + j] and msg[j]: v ^= F.mul(H[i][n - k + j], msg[j])
            cw[i] = v                     # H cw^T = 0 : cw_i = sum_j R_ij msg_j (char 2)
        y = [a ^ b for a, b in zip(cw, e)]
        # parity-check H_y of C + <y>: rows of H orthogonal to y: solve for combinations of H rows with (sum lambda_i H_i) . y = 0
        Hy_vals = []
        for i in range(n - k):
            v = 0
            for j in range(n):
                if H[i][j] and y[j]: v ^= F.mul(H[i][j], y[j])
            Hy_vals.append(v)
        # kernel of the 1 x (n-k) row (Hy_vals) over F_{q^m}: combinations lambda with sum lambda_i Hy_vals_i = 0
        lam_basis = kernel_fq(F, [Hy_vals], n - k)      # (n-k-1) vectors
        Hy = []
        for lam in lam_basis:
            row = [0] * n
            for i in range(n - k):
                if lam[i]:
                    for j in range(n):
                        if H[i][j]: row[j] ^= F.mul(lam[i], H[i][j])
            Hy.append(row)
        assert len(Hy) == n - k - 1
        # sanity: Hy e^T = 0
        for row in Hy:
            v = 0
            for j in range(n):
                if row[j] and e[j]: v ^= F.mul(row[j], e[j])
            assert v == 0
        # MM equations: for each r-subset J of rows of Hy: sum_T c_T * det(Hy[J, T]) = 0 ; expand over F_2 basis
        for J in itertools.combinations(range(n - k - 1), r):
            coeffs = [det(F, [[Hy[i][j] for j in T] for i in J]) for T in Ts]
            for b in range(m):
                rows_all.append(sum(((coeffs[t] >> b) & 1) << t for t in range(len(Ts))))
        # check true solution satisfies the equations
        tc = sum((true_c[t] & 1) << t for t in range(len(Ts)))
        assert all(bin(rw & tc).count('1') % 2 == 0 for rw in rows_all), "true minors violate an MM equation"
        rk = rank_f2(rows_all, len(Ts))
        print(f"  N={inst}: stacked equations {len(rows_all)}, rank {rk} / {len(Ts)-1} needed -> {'SOLVED (unique up to scalar)' if rk >= len(Ts)-1 else 'underdetermined'}", flush=True)

if __name__ == '__main__':
    main()
