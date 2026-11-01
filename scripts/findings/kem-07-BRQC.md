# ngcc.dev/reports/kem-07.html — BRQC (rank metric) (fetched 2026-10-31). 4 findings. NO design-level cryptanalysis.

kem-07-1 Decoder address trace gives a candidate-specific key-recovery route — Saarinen; extension Sun Shuzhou (GLM-5.3),
  2026-09-23, High/Lead, side-channel. Scaled BRQC: 3/3 keys recovered. Modeled adaptive-query costs at submitted dimensions
  ~2^71.4, 2^86.6, 2^119.8 vs claimed classical strengths 181, 295, 566 bits.
kem-07-2 Ignored padding bits make ciphertexts malleable — Saarinen, 2026-09-25 (ext. 10-17), Critical/Confirmed, implementation
  (u, v encodings end with 7, 5, or 1 unused bits per vector). ref + opt (BRQC-256 opt: RBC_163_ELT_SIZE four words).
kem-07-3 Secret-key expansion depends on external DRBG — Saarinen, Low/Confirmed.
kem-07-4 Short ciphertexts reach the fixed-offset parser — LK-PQC-Hunter, 2026-10-06, Low/Confirmed. Designer response 2026-10-07:
  acknowledges, will validate lengths.
Parameter sets: BRQC-128, -256 (m=163), -512. Claimed classical strengths 181 / 295 / 566 bits.
