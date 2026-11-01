#!/usr/bin/env python3
"""Generate LaTeX tables for the paper from the script outputs.
usage: python3 make_tables.py <scratch_dir> <paper_dir>"""
import sys, re, os
S, P = sys.argv[1], sys.argv[2]

# ---------------------------------------------------------------- tab-multi.tex
rows = []
for line in open(os.path.join(S, 'multi.out')):
    if '|' not in line or line.startswith('scheme'): continue
    a = [x.strip() for x in line.split('|')]
    head = a[0].split(); sch, lab, target = head[0], head[1], head[2]
    inst = a[1]; single = a[2].split('/')[0].strip()
    first = a[3]; t64 = a[4]; t80 = a[5]
    m = re.match(r"s=(\d+) t=([\d.]+) mem=([\d.]+)", first)
    if m: fs = f"$2^{{{m.group(1)}}}$ & {float(m.group(2)):.1f} & {float(m.group(3)):.0f}"
    else: fs = "--- & --- & ---"
    rows.append((sch, lab, target, inst, single, fs, t64, t80))
# QUBE rows were recomputed with the corrected [3r,2r] instance: take them from multi_qube.out if present
qube_path = os.path.join(S, 'multi_qube.out')
if os.path.exists(qube_path):
    rows = [r for r in rows if r[0] != 'QUBE']
    for line in open(qube_path):
        if '|' not in line or line.startswith('scheme'): continue
        a = [x.strip() for x in line.split('|')]
        head = a[0].split(); sch, lab, target = head[0], head[1], head[2]
        m = re.match(r"s=(\d+) t=([\d.]+) mem=([\d.]+)", a[3])
        fs = f"$2^{{{m.group(1)}}}$ & {float(m.group(2)):.1f} & {float(m.group(3)):.0f}" if m else "--- & --- & ---"
        rows.append((sch, lab, target, a[1], a[2].split('/')[0].strip(), fs, a[4], a[5]))
order = ['HARE', 'HEP-QC', 'NSS-HQC', 'TriQ-KEM', 'QUBE', 'Mito1', 'Mito1-E', 'Mito2-E', 'BIKE-MLThre', 'TRIKE', 'QCTM', 'HQC(ref)']
rows.sort(key=lambda r: (order.index(r[0]) if r[0] in order else 99))
with open(os.path.join(P, 'tab-multi.tex'), 'w') as f:
    f.write("\\begin{table}[t]\n\\centering\\tiny\n")
    f.write("\\caption{Same-key multi-instance message recovery (DS-DOOM, pinned estimator).  Instance $[n,k]$, weight $w$, rotations per ciphertext; single-instance cost ($M=$rot); first session exponent $s$ with $M=\\mathrm{rot}\\cdot2^s$ targets below the claimed level, with the time and $\\log_2$ memory there; and the cost after $2^{64}$ sessions.  Boldface marks a crossing within $2^{80}$.}\n\\label{tab:multi}\n")
    f.write("\\begin{tabular}{llrrrrrrrr}\\toprule\nScheme & Set & Target & $n$ & $w$ & rot & Single & $s$ & Time (Mem) & at $2^{64}$\\\\\\midrule\n")
    last = None
    for (sch, lab, target, inst, single, fs, t64, t80) in rows:
        mi = re.match(r"\[(\d+),(\d+)\] w=(\d+) rot=(\d+)", inst)
        inst_t = f"{mi.group(1)} & {mi.group(3)} & {mi.group(4)}" if mi else inst
        cross = '---' not in fs
        LAB = {'HARE-128(n=16067)': 'HARE-1', 'HARE-128(n=20899)': 'HARE-2', 'HARE-192(n=32653)': 'HARE-3', 'HARE-256(n=52379)': 'HARE-5',
               'HARE-384(n=104869)': 'HARE-7', 'HARE-512(n=173981)': 'HARE-9', 'TRIKE(r=10301)': 'TRIKE-1 (not submitted)', 'TRIKE(r=15581)': 'TRIKE-2',
               'TRIKE(r=22003)': 'TRIKE-3 (not submitted)', 'TRIKE(r=35363)': 'TRIKE-5', 'TRIKE(r=69691)': 'TRIKE-7', 'TRIKE(r=114043)': 'TRIKE-9',
               'HEP-QC-128': 'HEP-QC-1', 'HEP-QC-192': 'HEP-QC-3', 'HEP-QC-256': 'HEP-QC-5', 'HEP-QC-512': 'HEP-QC-7'}
        lab_t = LAB.get(lab, lab)
        name = sch if sch != last else ''
        parts = fs.split(' & ')
        fs_t = (f"\\textbf{{{parts[0]}}} & \\textbf{{{parts[1]}}} ({parts[2]})" if cross else "--- & --- ")
        f.write(f"{name} & {lab_t} & {target} & {inst_t} & {float(single):.1f} & {fs_t} & {float(t64):.1f}\\\\\n")
        last = sch
    f.write("\\bottomrule\n\\end{tabular}\n\\end{table}\n")

# ---------------------------------------------------------------- tab-isd.tex (from pricing_stern.out, optional bjmm file)
isd_path = os.path.join(S, 'pricing_stern.out')
bjmm = {}
bj_path = os.path.join(S, 'pricing_bjmm.out')
if os.path.exists(bj_path):
    for line in open(bj_path):
        if '|' not in line: continue
        a = [x.strip() for x in line.split('|')]
        m = re.search(r"\[(\d+),(\d+)\] w=\s*(\d+)", a[1]); mm = re.search(r"all\s+([\d.]+)", a[3])
        if m and mm: bjmm[(m.group(1), m.group(2), m.group(3))] = float(mm.group(1))
if os.path.exists(isd_path):
    with open(os.path.join(P, 'tab-isd.tex'), 'w') as f:
        f.write("\\begin{table}[t]\n\\centering\\scriptsize\n")
        f.write("\\caption{Single-instance decoding costs (CryptographicEstimators 2.1.1, $\\log_2$ bit operations): raw Stern cost, quasi-cyclic discount, discounted Stern cost; minimum over all algorithms (Prange, Stern, Dumer, ball-collision, BJMM variants, Both--May, May--Ozerov) raw and discounted.}\n\\label{tab:isd}\n")
        f.write("\\begin{tabular}{llrlrrrrrr}\\toprule\nScheme & Set & Claim & Instance & $[n,k]$, $w$ & Stern & disc. & Stern$-$disc. & min (alg.) & min$-$disc.\\\\\\midrule\n")
        last = None
        for line in open(isd_path):
            if '|' not in line: continue
            a = [x.strip() for x in line.split('|')]
            head = a[0].split(); sch = head[0]; lvl = head[1]; claim = head[3]
            m = re.match(r"(.+?)\s+\[(\d+),(\d+)\] w=\s*(\d+) disc=\s*([\d.]+)", a[1])
            lab, N, K, w, disc = m.group(1), m.group(2), m.group(3), m.group(4), float(m.group(5))
            st = float(re.search(r"Stern-family\s+([\d.]+)", a[2]).group(1))
            ma = re.search(r"all\s+([\d.]+) \((\w+)", a[3]); al = float(ma.group(1)); alg = ma.group(2)
            name = sch if sch != last else ''
            f.write(f"{name} & {lvl} & {claim} & {lab} & $[{N},{K}]$, {w} & {st:.1f} & {disc:.1f} & {st-disc:.1f} & {al:.1f} ({alg}) & {al-disc:.1f}\\\\\n")
            last = sch
        f.write("\\bottomrule\n\\end{tabular}\n\\end{table}\n")
print("tables written")
