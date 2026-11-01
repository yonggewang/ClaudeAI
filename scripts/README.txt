Scripts for "Fifteen Code-Based KEMs, One Framework: Structural and Parametric
Cryptanalysis of the NGCC Round-1 Code-Based Candidates"

Requirements: Python 3.11+, cryptographic-estimators==2.1.1, sympy, mpmath, numpy, scipy.
The May-Sa Diogo DS-DOOM estimator is NOT bundled: clone
  https://github.com/Gabsadio/Multi-Instance-KEM  at commit 39b78dcc077793cfa3ccdce8d032ece76825ca55
and pass the path to doom.py (its SHA-256 is checked by the script).

  ring_audit.py          factorisation of x^n-1 for every quasi-cyclic candidate (Sec. 3.1).
                         Finds BIKE-MLThre-512: r=150001 prime but ord_r(2)=3750.
  price_hamming.py       single-instance ISD costs, key and message, for every parameter set
                         (Table 2).  Calibrated: reproduces QCTM Table 1 and TRIKE Table 9 exactly.
                             python3 price_hamming.py all
  multi_instance.py      same-key multi-instance (DS-DOOM) crossings (Table 3).
                             python3 -I multi_instance.py /path/to/doom.py
  dfr_model1.py          HQC Model-1 decryption-failure rates (Table 4).  Reproduces the HQC,
                         QUBE and TriQ-KEM published values to the printed precision.
  qctm_toy.py            QCTM: verifies the cosmetic-twist lemma, the quasi-cyclic invariance,
                         the folding theorem, and the full lifting + decoding attack, on
                         scaled-down keys generated exactly as in the specification.
                             python3 qctm_toy.py m ell t0 n_blocks [seed] [extra-Frobenius-twist]
                             e.g. python3 qctm_toy.py 10 11 3 48 1
  square_toy.py          Schur square of the dual of the QCTM quotient code (Sec. 4.5).
                             python3 square_toy.py m ell t0 n_b [seed]
  mito_toy.py            Mito: the augmentation Z->1 is a weight-non-increasing ring
                         homomorphism onto a plain HQC instance (Proposition 1).
  mm_blockwise.py        blockwise MaxMinors cost (BRQC/BRA Theorems 7.6 and 7.7), independently
                         transcribed; validated against the single-block case and four of the
                         designers' own data points.
  mm_search.py           search over block orderings, puncturing, hybrid and sub-support guessing.
                             PMAX=40 python3 mm_search.py 2 all      (restricted puncturing)
                             python3 mm_search.py 2 all              (free puncturing)
  rank_pricing.py        rank-metric re-pricing with CryptographicEstimators (Table 6).
  rsl_toy.py             rank-support-learning: rank of the stacked MaxMinors system as a
                         function of the number of same-support syndromes (Sec. 5.3).
                             python3 rsl_toy.py m n k r Nmax [seed]
  make_tables.py         regenerates the LaTeX tables from the outputs above.

findings/                per-candidate transcripts of the ngcc.dev findings used in the paper,
                         fetched 2026-10-31, with our own additions marked.
