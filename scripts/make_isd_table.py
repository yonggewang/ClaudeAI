#!/usr/bin/env python3
"""Build the focused single-instance ISD table: our costs next to the value the specification
publishes for the same quantity (where it publishes one).
usage: python3 make_isd_table.py <pricing.out> <out.tex>"""
import sys, re

# (scheme, n of the instance, first token of the label) -> (value the specification publishes, source)
SPEC = {}
for N, kv, mv in [(30903,'134.05','132.11'),(46743,'171.78','167.86'),(66009,'200.36','200.58'),
                  (106089,'266.61','264.86'),(209073,'398.81','398.77'),(342129,'531.41','526.21')]:
    SPEC[('TRIKE', N, 'key')] = (kv, 'T9'); SPEC[('TRIKE', N, 'msg')] = (mv, 'T10')
for N, v in [(10070,'150.87'),(19000,'272.90'),(38000,'530.30')]:
    SPEC[('QCTM', N, 'msg')] = (v, 'T1--3')
for N, v in [(39327,'144.77'),(76071,'208.68'),(124953,'273.19'),(248271,'402.58'),(407553,'530.55')]:
    SPEC[('QUBE', N, 'pk')] = (v, 'T6')
for N, v in [(58886,'188.2'),(108986,'256.0'),(245158,'384.0'),(435802,'512.0')]:
    SPEC[('NSS-HQC', N, 'pk')] = (v, 'S4.5')
for N, v in [(108986,'226.51'),(245158,'333.04'),(435802,'441.39')]:
    SPEC[('NSS-HQC', N, 'ct')] = (v, '26-3')

ORDER = ['QCTM', 'HQC', 'HEP-QC', 'HARE', 'NSS-HQC', 'TriQ-KEM', 'QUBE', 'Mito1', 'Mito1-E', 'Mito2-E', 'BIKE-MLThre', 'TRIKE']

rows = []
for line in open(sys.argv[1]):
    if '|' not in line: continue
    a = [x.strip() for x in line.split('|')]
    h = a[0].split()
    sch = h[0]
    if h[1] == '(ref.)': sch, h = 'HQC', [h[0]] + h[2:]
    lvl, claim = int(h[1]), h[3]
    m = re.match(r"(.+?)\s+\[(\d+),(\d+)\] w=\s*(\d+) disc=\s*([\d.]+)", a[1])
    if not m: continue
    lab, N, K, w, disc = m.group(1), m.group(2), m.group(3), m.group(4), float(m.group(5))
    st = float(re.search(r"Stern-family\s+([\d.]+)", a[2]).group(1))
    ma = re.search(r"all\s+([\d.]+) \((\w+)", a[3]); al, alg = float(ma.group(1)), ma.group(2)
    spec = SPEC.get((sch, int(N), lab.split()[0]), ('---', ''))
    rows.append((sch, lvl, claim, lab, N, K, w, disc, st, al, alg, spec))
rows.sort(key=lambda r: (ORDER.index(r[0]) if r[0] in ORDER else 99, r[1], r[3]))

with open(sys.argv[2], 'w') as f:
    f.write("\\begin{table}[t]\n\\centering\\tiny\n")
    f.write("\\caption{Single-instance decoding costs ($\\log_2$ bit operations, CryptographicEstimators 2.1.1): "
            "raw Stern cost; minimum over Prange, Stern, Dumer, ball-collision, BJMM, BJMM$^+$ and May--Ozerov, "
            "with the algorithm attaining it; the quasi-cyclic discount and the discounted minimum.  "
            "The last column is the value the specification publishes for the same quantity, where it publishes one.  "
            "Instances: \\emph{key} = codeword finding, \\emph{msg}/\\emph{ct} = syndrome decoding, "
            "\\emph{pk} = the $[2n,n]$ key instance, \\emph{ct u-only} = the ciphertext instance that discards $v$.  "
            "The table covers the instances for which a specification publishes a comparable number, "
            "together with the lowest-level instance of each family, up to a size cap; for the larger "
            "instances we quote the specifications' own values, which the agreement below licenses.}\n")
    f.write("\\label{tab:isd}\n\\begin{tabular}{llrlrrrrlrrl}\\toprule\n"
            "Scheme & Set & Claim & Instance & $n$ & $k$ & $w$ & Stern & min (alg.) & disc. & min$-$disc. & Spec.\\\\\\midrule\n")
    last = None
    for (sch, lvl, claim, lab, N, K, w, disc, st, al, alg, spec) in rows:
        name = sch if sch != last else ''
        sv = spec[0] if spec[0] == '---' else f"{spec[0]}\\,{spec[1]}"
        f.write(f"{name} & {lvl} & {claim} & {lab} & {N} & {K} & {w} & {st:.2f} & {al:.2f} ({alg}) & {disc:.2f} & {al-disc:.2f} & {sv}\\\\\n")
        last = sch
    f.write("\\bottomrule\n\\end{tabular}\n\\end{table}\n")
print(f"{len(rows)} rows written to {sys.argv[2]}")
