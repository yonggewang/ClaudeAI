# ngcc.dev/reports/kem-17.html — HEP-QC (hep-qc-1/3/5/7) (fetched 2026-10-31). No designer responses.

kem-17-1 Publicly reproducible secret keys — Saarinen, 2026-09-21, Critical/Confirmed, implementation, all sets.
  File-scope SHAKE-256 PRNG never initialised; seeded DRNG declared but unused -> every fresh process gives the same key pair.
kem-17-2 HEP-QC-7 has at most 256 bits of key-generation support — Saarinen, 2026-09-21, Critical/Confirmed, DESIGN.
  seedKEM is 32 bytes; whole key pair derived from it -> 2^256 public keys; shared key K 32 bytes. Claimed 512-bit level.
kem-17-3 First encapsulation in each process is publicly reproducible — Saarinen 2026-09-21; consecutive-session extension by
  Hao Yan, Yuhang Cao, Yao Tong, Qiaosheng Zhang (Shanghai AI Lab) 2026-10-26, Critical/Confirmed, implementation.
  m and salt from the same uninitialised PRNG; 208-byte context, each update writes 26 bytes; 16-byte salt = first 16 bytes of
  next state -> 2^80 consistent states from two consecutive ciphertexts.
kem-17-4 Public column multiplicities break the EPC-P assumption — Tianyuan Xie (NGCC PKC Forum), 2026-09-22, High/Confirmed, DESIGN, all sets.
  Each column of the inner RM generator repeated MULT = n2/128 times; row mixing + column permutation preserve equality ->
  public G' has n1*128 column classes of multiplicity MULT plus 64 singleton columns (fresh HEP-QC-1 key: 3^5888 + 1^64 vs 1^17728
  uniform). Distinguisher advantage ~1; falsifies EPC-P assumption behind the first security bound. Xie reports recovering the
  affine blocks and the exact secret transformation T on 35/35 official keys; remaining "frame-label searches" estimated 2^84.1,
  2^131.0, 2^198.7 for HEP-QC-1/3/5 (below 128/192/256 claims); public attachment reproduces the distinguisher only.
  Also: Theorem 6.3.1 IND-CPA proof gap (replacing G' by uniform does not make the challenge statistically independent of m:
  noise has at most C(n,w_r)C(n,w_e) values; translates almost surely disjoint) — proof gap, not a break.
kem-17-5 Secret permutation and mixing matrix drive memory and control flow — Saarinen, 2026-09-23, Medium/Confirmed, side-channel.
