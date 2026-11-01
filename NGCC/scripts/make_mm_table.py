#!/usr/bin/env python3
"""Build the blockwise-MaxMinors table from mm_search.py output.
usage: python3 make_mm_table.py <mm_restricted.out> <out.tex> [<mm_free.out>]"""
import sys, re

HOMOG = {  # homogeneous relaxation (CryptographicEstimators, omega=2.81), from rank_pricing.py
 ('BRQC-128', 'key'): '560.0', ('BRQC-128', 'ct'): '688.8',
 ('BRQC-256', 'key'): '782.3', ('BRQC-256', 'ct'): '1036.1',
 ('BRQC-512', 'key'): '1312.0', ('BRQC-512', 'ct'): '1665.8',
 ('BRA-128', 'key'): '275.5', ('BRA-128', 'ct'): '386.3',
 ('BRA-256', 'key'): '375.5', ('BRA-256', 'ct'): '518.3',
 ('BRA-512', 'key'): '682.5', ('BRA-512', 'ct'): '906.3',
}

def parse(path):
    out = {}
    for line in open(path):
        m = re.match(r"(\S+) (key|ct) \(designers (\d+)\): min log2 TC = ([\d.]+) .*xi'=([\d.]+) p=\(([^)]*)\) a=\(([^)]*)\) h=\(([^)]*)\)(.*)", line)
        if not m: continue
        order = ''
        mo = re.search(r"block order \([^)]*\) \(ranks \(([^)]*)\)\)", m.group(9))
        if mo: order = mo.group(1).replace(' ', '')
        out[(m.group(1), m.group(2))] = (m.group(3), float(m.group(4)), float(m.group(5)),
                                         m.group(6).replace(' ', ''), m.group(7).replace(' ', ''), order)
    return out

restricted = parse(sys.argv[1])
free = parse(sys.argv[3]) if len(sys.argv) > 3 else {}
order = [f"{s}-{l}" for s in ('BRQC', 'BRA') for l in (128, 256, 512)]
rows = [(s, i) for s in order for i in ('key', 'ct') if (s, i) in restricted]

with open(sys.argv[2], 'w') as f:
    f.write("\\begin{table}[t]\n\\centering\\footnotesize\n")
    f.write("\\caption{Blockwise MaxMinors costs ($\\log_2$, $\\omega=2$) from our independent search over block "
            "orderings, puncturing $\\mathbf p$ (restricted to $p_i\\le40$), hybrid guessing $\\mathbf a$ and "
            "sub-support guessing $\\mathbf h$ (\\texttt{mm\\_search.py}), against the minimum the specification "
            "tabulates.  $\\xi'=\\overline E/N$ is the feasibility ratio at our point; `ranks' is the block order "
            "attaining it.  The last column is the homogeneous relaxation (one error of rank $\\sum_ir_i$) under "
            "CryptographicEstimators with $\\omega=2.81$, for scale.}\n")
    f.write("\\label{tab:mm}\n\\begin{tabular}{llrrrlllr}\\toprule\n"
            "Scheme & Inst. & Spec. & Ours & $\\xi'$ & $\\mathbf p$ & $\\mathbf a$ & ranks & homog.\\\\\\midrule\n")
    last = None
    for (s, i) in rows:
        d, tc, xi, p, a, ordr = restricted[(s, i)]
        name = s if s != last else ''
        gap = f"\\textbf{{{tc:.1f}}}" if tc < float(d) - 0.5 else f"{tc:.1f}"
        f.write(f"{name} & {i} & {d} & {gap} & {xi:.3f} & $({p})$ & $({a})$ & {ordr or '---'} & {HOMOG.get((s, i), '---')}\\\\\n")
        last = s
    f.write("\\bottomrule\n\\end{tabular}\n\\end{table}\n")
print(f"{len(rows)} rows written")
