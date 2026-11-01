#!/usr/bin/env python3
"""Does the Schur square of the DUAL of the QCTM quotient code fill the whole space?
If dim((C^perp)^{*2}) = n, the square distinguisher of Faugere-Gauthier-Otmani-Perret-Tillich
sees nothing (the code behaves like a random one).  We build the quotient code
Gamma(X', M) cap E of a toy QCTM key (support inside the subgroup of ell-th powers, exactly as
in Theorem 2) and measure the dimension of the square of its dual.
usage: python3 square_toy.py m ell t0 n_b [seed]"""
import sys, random, itertools
sys.path.insert(0, '/home/claude/ngcc/work')
from qctm_toy import GF, p_is_irreducible, p_eval, rank_f2, kernel_f2, rref_f2

def main():
    m, ell, t0, nb = map(int, sys.argv[1:5]); seed = int(sys.argv[5]) if len(sys.argv) > 5 else 1
    random.seed(seed)
    prim = {8: 0x11d, 9: 0x211, 10: 0x409, 11: 0x805, 12: 0x1053}[m]
    F = GF(m, prim); q = F.q
    assert (q - 1) % ell == 0
    # support inside the subgroup of ell-th powers (as the QCTM quotient has)
    e_ell = (q - 1) // ell
    powers = [x for x in range(1, q) if F.pow(x, e_ell) == 1]
    assert nb <= len(powers)
    X = random.sample(powers, nb)
    while True:
        M = [random.randrange(q) for _ in range(t0)] + [1]
        if p_is_irreducible(F, M) and all(p_eval(F, M, x) != 0 for x in X): break
    y = [F.inv(p_eval(F, M, x)) for x in X]
    # parity-check rows of Gamma(X,M) cap E over F_2: Tr-expansion of x^i y, i<t0, plus all-ones
    rows_q = [[F.mul(F.pow(xx, i), yy) for xx, yy in zip(X, y)] for i in range(t0)]
    dual = [sum(((v >> b) & 1) << j for j, v in enumerate(row)) for row in rows_q for b in range(m)]
    dual += [(1 << nb) - 1]
    kdual = rank_f2(dual, nb)
    C = kernel_f2(dual, nb)
    # basis of the dual (reduced), then its Schur square
    _, dbasis = rref_f2(dual, nb)
    sq = []
    for i in range(len(dbasis)):
        for j in range(i, len(dbasis)):
            sq.append(dbasis[i] & dbasis[j])
    dsq = rank_f2(sq, nb)
    print(f"m={m} ell={ell} t0={t0} n_b={nb} (rate {(nb-kdual)/nb:.3f}): dim C={nb-kdual}, dim C^perp={kdual}, "
          f"dim (C^perp)^(*2) = {dsq} / {nb} -> {'FILLS (no square distinguisher)' if dsq == nb else 'DOES NOT FILL (distinguishable)'}"
          f"  [binom(dim+1,2)={kdual*(kdual+1)//2}]")

if __name__ == '__main__':
    main()
