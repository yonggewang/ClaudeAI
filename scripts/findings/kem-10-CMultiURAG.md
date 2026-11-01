# ngcc.dev/reports/kem-10.html — C-Multi-UR-AG (rank metric) (fetched 2026-10-31). 6 findings, all implementation/side-channel. NO design-level cryptanalysis.

kem-10-1 Malformed ciphertexts crash the reference decapsulator — Saarinen, 2026-09-23, High/Confirmed (stack smash in rbc_elt_mul via
  rbc_qpoly_left_div2 signed/unsigned bound).
kem-10-2 Secret-derived decoder pivots select memory addresses — Saarinen, 2026-09-23, Low/Confirmed (augmented-Gabidulin decoder).
kem-10-3 Ignored padding bits make CMultiURAG-512 ciphertexts malleable — Saarinen, 2026-09-25 (ext. 10-17), Critical/Confirmed,
  implementation (m=181: 5 unused bits in U and V encodings -> 1023 byte-distinct variants per ciphertext).
kem-10-4 Secret-key expansion depends on the external DRBG — Saarinen, 2026-10-03, Low/Confirmed.
kem-10-5 Short ciphertexts reach the fixed-offset parser — LK-PQC-Hunter, 2026-10-06, Low/Confirmed. Designer response 2026-10-07
  acknowledges, plans input-length validation.
kem-10-6 Reference 79-bit field multiplication touches a fourth limb — LK-PQC-Hunter, 2026-10-06, Low/Confirmed.
Parameter sets: CMultiURAG-128 (m=79), -256, -512 (m=181).
