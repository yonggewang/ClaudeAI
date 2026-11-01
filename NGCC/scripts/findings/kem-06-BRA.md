# ngcc.dev/reports/kem-06.html — BRA (rank metric) (fetched 2026-10-31). 6 findings, no designer responses. NO design-level cryptanalysis.

kem-06-1 Malformed inputs drive the decoder out of bounds — Dariia Porechna; remote-ciphertext extension Xiong & Wang (ePrint
  2026/2232 §6.5), 2026-09-22, Low/Confirmed, implementation (BRA-128/256 crash 30/30 malformed ciphertexts; BRA-512 no).
kem-06-2 Reference field multiplication touches one limb past its output — 2026-09-22, Low/Confirmed (GF(2^67), GF(2^83)).
kem-06-3 Decoder address trace gives a candidate-specific key-recovery route — Saarinen; recovery extension Sun Shuzhou (GLM-5.3,
  PKC Forum 2026-10-04), 2026-09-23, High/Lead, side-channel. Ciphertexts (u,v)=(1,t) reveal membership in secret support E_y;
  instrumented BRA-128 recovered E_y exactly 3/3 keys with 3,443 / 5,044 / 6,467 queries; modeled full-key costs ~2^49.9,
  2^57.4, 2^71.5 (guess x support + linear system). No physical channel demonstrated.
kem-06-4 Ignored padding bits make ciphertexts malleable — Saarinen, 2026-09-25 (ext. 10-17), Critical/Confirmed, implementation
  (u, v encodings each end with 5 unused bits -> 1023 byte-distinct variants). All sets, ref + opt.
kem-06-5 Secret-key expansion depends on external DRBG — Saarinen, Low/Confirmed.
kem-06-6 Short ciphertexts reach the fixed-offset parser — LK-PQC-Hunter, Low/Confirmed.
Parameter sets: BRA-128 (GF(2^67)? m=67?), BRA-256 (m=83?), BRA-512 (m=127?) — check spec: field sizes 67/83/127 bits mentioned.
