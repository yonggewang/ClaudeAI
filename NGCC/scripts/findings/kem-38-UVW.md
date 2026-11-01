# ngcc.dev/reports/kem-38.html — UVW-KEM (fetched 2026-10-31). 8 findings, no designer responses.

kem-38-1 UVW-512 derives its encryption pair from only 256 bits — Saarinen, 2026-09-21, Critical/Confirmed, implementation.
  H1(m) hashed to 32-byte seed then expanded -> 2^256 seed trials recover (r,e), m, session key. Not in the PDF spec.
kem-38-2 Stable list-decoding failure oracle — Saarinen, 2026-09-21, High/Confirmed, design. Decaps returns -2 (list decoding
  fail, ~49.3 s) vs -1 (hash/re-encryption fail, ~0.81 s): 60x timing gap; constant-time fix would cost ~49 s per decaps.
kem-38-3 Stateful timing reactions recover UVW-KEM-128 shared secrets — Tianyuan Xie, Yamin Liu (openHiTLS), 2026-09-24, High/Probable,
  side-channel. Chosen ciphertexts reveal hidden column pairs and ratios; public projection gives a GRS image; decode fresh ct.
  uvw_rs_list_decode can return positive count without valid r2; primer ciphertext makes leftover state repeatable (0.12-0.17 s vs
  14.5-15.2 s). ~410,000 targets, ~1e6 calls, 2.8 h on 32 threads; success=1.
kem-38-4 Unused c1 bits make ciphertexts malleable — Saarinen, 2026-09-25, Critical/Confirmed, implementation (128, 512; not 256).
  4 unused packed bits ignored by decompress_gf_array -> byte-distinct ciphertext decapsulates to same key (IND-CCA violation).
kem-38-5 Final decryption failures expose hidden pairs — Zhenyu Xiong, Mingsheng Wang, 2026-09-30, High/Lead, implementation.
  Decoder caps information-set search at 1000 attempts; final-failure rates 2^-43.317 (128), 2^-42.144 (256), 2^-41.729 (512).
  Spec Alg. 5 has no limit. Conditioning on final failures: 1000 failures recover all 430 hidden pair/ratio triples at ~2^53.3
  honest encaps/decaps trials. Proposed: state overall DFR, include in FO bound.
kem-38-6 UVW-256/-512 leak retry matrices — Xiong, Wang, 2026-09-30, Low/Confirmed. 0.73 GB (k1=427) / 2.91 GB (k1=853) per
  1000-attempt decapsulation; free() of stack array in 256 (UB).
kem-38-7 Resets the external DRBG for key expansion and re-encryption — Saarinen, 2026-10-03, Low/Confirmed.
kem-38-8 Cubic-jet syzygies recover UVW's secret structure from the public key — Liping Wang (distinguishing route); Saarinen
  (syzygy key recovery, full-size decapsulation), 2026-10-26, Critical/Confirmed, design. Affected: UVW-KEM-128 (key recovery +
  decapsulation demonstrated), -256 (distinguishing confirmed on a submitted key), -512 (same structure, not run).
  Spec Theorem 3 assumes Generalized (U+V,U+W) Code Distinguishing hard (claimed exponential when k1=k2). Method: order-2,
  degree-3 multiplicity count on shortened public codes of dimension Theta(sqrt n). Cubic-form counts: UVW-128 k_l=53: 800 vs
  636 generic; UVW-256 (q=857, n=1708) k_l=74: 1983 vs 1628; excess = k2 - k_l + 2. Recovery: 430 twin pairs + ratios in 3
  adaptive rounds; each round solves 25,599 x 26,235 system for 164-dim dependency space in ~16 s. Subtracting twin pairs gives
  a [430,215] GRS code; Sidelnikov–Shestakov recovers it up to 8 Möbius maps. Decapsulation: w=116 errors, ~640 error-free
  coordinates, 0.4 s per ciphertext. 5 fresh key pairs: all 430 pairs/ratios correct; 18/18 fresh ciphertexts decapsulated.
  Cost estimates 2^53.68 / 2^57.75 / 2^61.56 (not verified); jet system Theta(n^1.5) rows/cols, O(n^4.5) per round.
  UVW-256 recovery (~68,672 rows) and UVW-512 (~186,000 rows) not run. Structure recovery < 1 min on 28 cores for UVW-128.
