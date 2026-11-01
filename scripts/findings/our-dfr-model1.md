# Our Model-1 (HQC independent-Bernoulli) DFR recomputation — dfr_model1.py (mpmath, 60 digits)
Validation: HQC-1/3/5 -> -132.892 / -193.861 / -260.597 (QUBE spec Table 8: 132.89/193.86/260.59)  [Computed]
QUBE-128/192/256/384/512 -> -137.545 / -200.136 / -264.313 / -392.436 / -520.668 (spec Table 7: 137.5/200.1/264.3/392.4/520.6)  [Computed, reproduces]
TriQ-KEM-128/256/384/512 natural DFR -> -121.902 / -173.354 / -209.571 / -230.003 (spec Table 6: 121.90/173.35/209.57/230.00)  [Computed, reproduces]
   => every TriQ set has natural DFR ABOVE 2^-lambda: shortfalls 6.1 / 82.6 / 174.4 / 282.0 bits. Spec substitutes an
      'attack-aware post-rejection CDFR' criterion (<= 2^-34.32 / 2^-85.63 / 2^-124.93 / 2^-146.56 over a 2^80 query budget).
      Standard FO bound: q_D * delta with q_D = 2^80 gives 2^-41.9 / 2^-93.4 / 2^-129.6 / 2^-150 -> IND-CCA2 claim not supported
      at the claimed levels by the standard criterion. (ngcc.dev kem-37 has only side-channel findings.)
HEP-QC-7 -> -574.372 (claimed < 2^-512): fine. HEP-QC-1/3/5 == HQC-1/3/5 parameters.
Mito1-128/256/512: from the spec's p* (0.3161/0.3335/0.3671): -173.447 / -272.508 / -515.614 (claimed 173.34/272.79/516.22; differences
   from 4-digit p* rounding). 2-adic sum model reproduces p*: components 0.31598 / 0.31656 for Mito1-128 (spec 0.3161).
   Mito1-E / Mito2-E use erasure decoding: not recomputed (and kem-23-1: shipped code does not implement erasure decoding).
HARE: Xiong–Wang kem-16-1 Model-1 recomputation 2^-121.45 (HARE-128) / 2^-239.21 (HARE-256) vs Model-2 claims; cite.
NSS-HQC: DFR analysis invalid (kem-26-2, measured failures 1.4e-4 at NSS-HQC-256); cite.
TRIKE: QC-MDPC, DFR extrapolated; boundary weak-key classes gap (kem-36-4); cite.
UVW-KEM: overall DFR 2^-43.3 (kem-38-5 / Xiong–Wang); cite.
BIKE-MLThre: ML-threshold BGF decoder, DFR claims <= 2^-128/-256/-512 by extrapolation (check spec section).
