"""Ring audit for the quasi-cyclic NGCC code-based KEMs: is n prime, is 2 primitive mod n (so that
X^n - 1 = (X+1) * irreducible over F_2), and if not, the degrees of the irreducible factors of
X^n-1 (= orbit sizes of multiplication by 2 on Z_n), which are the sub-ring projections available."""
from sympy import isprime, factorint, n_order
sets = {
 'HARE': [16067, 20899, 32653, 52379, 104869, 173981],
 'HEP-QC': [17669, 35851, 57637, 197123],
 'NSS-HQC': [29443, 54493, 122579, 217901],
 'QUBE': [13109, 25357, 41651, 82757, 135851],
 'TriQ-KEM': [16301, 50363, 97651, 157627],
 'Mito1': [15373, 33827, 106261], 'Mito1-E': [14621, 32261, 102437], 'Mito2-E': [10253, 21523, 65293],
 'BIKE-MLThre': [12323, 40973, 150001],
 'TRIKE': [10301, 15581, 22003, 35363, 69691, 114043],
 'HQC (reference)': [17669, 35851, 57637],
}
for name, ns in sets.items():
    for n in ns:
        p = isprime(n)
        if p:
            o = n_order(2, n); prim = (o == n - 1)
            print(f"{name:16s} n={n:7d} prime  ord_n(2)={o:7d} {'2 primitive: X^n-1=(X+1)*irred' if prim else 'NOT primitive: factors of degree '+str(o)+' x'+str((n-1)//o)}")
        else:
            f = factorint(n)
            # orbit sizes of x -> 2x on Z_n give the factor degrees
            seen=set(); degs={}
            for a in range(n):
                if a in seen: continue
                orb=[]; x=a
                while x not in seen: seen.add(x); orb.append(x); x=(2*x)%n
                degs[len(orb)]=degs.get(len(orb),0)+1
            print(f"{name:16s} n={n:7d} COMPOSITE {dict(f)}  factor degrees (count): {sorted(degs.items())[:8]}")
