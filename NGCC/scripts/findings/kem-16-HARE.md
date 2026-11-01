# ngcc.dev/reports/kem-16.html — HARE (fetched 2026-10-31). 2 findings. Designer response 2026-10-11 (summarised only).

kem-16-1 Headline DFR values lack a reproducible HARE calculation — Zhenyu Xiong, Mingsheng Wang (IIE CAS; Claude Opus 5.5
  assistance), 2026-09-29, Medium/Proof gap, design, HARE-128 & HARE-256 (HARE-2, HARE-5). Table 2 claims DFR < 2^-130 (128) and
  < 2^-258 (256) from the dependent-coordinate Model 2 (§6); no HARE adaptation of the Bitzer et al. artifact was submitted.
  Independent Model-1 recomputation: 2^-121.4485 (HARE-128), 2^-239.2123 (HARE-256): 6.6 and 16.8 bits short of the security
  levels. Control: Model-1 reproduces Table 2 for HARE-384 (2^-384.9304) and HARE-512 (2^-519.4516). PARAMETER_MANIFEST.tsv labels
  HARE-256's value as Model 1 (metadata error). Designer response: revised Model-2 evaluator (README lists HARE-1, -3, -5, not -2);
  not evaluated; frozen submission remains the target.
kem-16-2 Same-key multi-instance decoding misses three HARE targets — Xiong, Wang (GLM-5.3 assistance), 2026-10-03,
  Critical/Confirmed, design, HARE-256/384/512 (HARE-5/7/9). u = r1 + h r2 exposed; Q ciphertexts x n shifts -> DOOM. Pinned
  heuristic estimator: HARE-256 Q=2^72 time 2^255.440 mem 2^103.356; HARE-384 Q=2^64 time 2^383.175 mem 2^97.358; HARE-512
  Q=2^75 time 2^511.699 mem 2^109.820. HARE-128 above target at the 2^80 ceiling. Margins 0.56/0.82/0.30 bits; one pinned
  estimator. Designer response: setting differs from IND-CCA2 analysis; will examine.
Parameter sets: HARE-1 (128, n=16067), HARE-2 (128, n=20899), HARE-3 (192), HARE-5 (256), HARE-7 (384), HARE-9 (512).
