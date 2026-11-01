# ngcc.dev/reports/kem-26.html — NSS-HQC (fetched 2026-10-31). 5 findings, no designer responses.

kem-26-1 Fixed-weight parity falsifies DQCSD and JPCI — AMSS Information Security Center, 2026-09-30, Medium/Confirmed, design, all sets.
  parity(a*b) = parity(a)parity(b); -128/-256: r1, r2 even weight -> parity(u)=0; -384/-512: parity(u) = 1 + parity(h) public.
  Weights w_r: 66, 106, 159, 213. Invalidates proof route; no message/key recovery.
kem-26-2 NSS-HQC-256 failures enable reported equivalent-key recovery — AMSS; failure-oracle extension Sun Shuzhou (GLM-5.3),
  2026-09-30, Critical/Probable, design. DFR claim < 2^-128 (§3.6) uses BSC proxy for five-bit compressor; Eq. (68) counts only
  patterns matching nonzero RM codewords (7.53e-45 at crossover 1/4) but one omitted failure event has prob >= 4.59e-6; AMSS:
  7/50,000 honest NSS-HQC-256 sessions failed (1.4e-4). Failing seed 4201 found. Sun: ~1.3e8 (2^27) adaptive decapsulations
  recover both 117-position supports; reconstructed key decrypts fresh ciphertext. Not independently replayed.
kem-26-3 Ephemeral syndrome decoding misses the 256/384/512 targets — Saarinen, 2026-09-30, Critical/Confirmed, design.
  Spec extrapolates one HQC-128 value as 1.0969 sqrt(n) (§4.5.2). cryptographic-estimators 2.1.1 Stern:
  | NSS-HQC-256 | [108986,54493,212] | 234.38 | mem 46.20 | 226.51 after sqrt(n) | target 256 |
  | NSS-HQC-384 | [245158,122579,318] | 341.49 | 49.71 | 333.04 | 384 |
  | NSS-HQC-512 | [435802,217901,426] | 450.26 | 52.20 | 441.39 | 512 |
  NSS-HQC-128: 154.43 raw, 147.01 discounted (not affected). Compression does not prevent message recovery (Q(a xor 1^5) = 3-c);
  e weights 187/279/372 cause at most 5/8/11 bad outer symbols vs RS radii 19/26/33.
kem-26-4 256-bit decryption sub-seed caps NSS-HQC-384/-512 — Xiong, Wang (GLM-5.3), 2026-10-05, Critical/Confirmed, design.
  SHA3-512 output split into two 256-bit sub-seeds; decryption needs only y = f(seed_y) -> 2^255 candidates, recognised via
  wt(s + h y) = w_sk; ~2^279.4 / 2^280.6 bit ops.
kem-26-5 RS-decoder timing reportedly recovers an NSS-HQC-128 key — Sun Shuzhou (GLM-5.3), 2026-10-06, Critical/Probable,
  side-channel. RS decoder tries decreasing error counts, returns on first success; 1.1% timing separation; 912,733 chosen
  ciphertexts recover all 73 support positions. Not replayed.
