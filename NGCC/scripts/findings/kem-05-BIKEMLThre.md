# ngcc.dev/reports/kem-05.html — BIKE-MLThre (QC-MDPC) (fetched 2026-10-31). 2 findings, no designer responses.

kem-05-1 Default library deterministically generates a public secret key — Xiong, Wang (IIE CAS), 2026-09-30, Critical/Confirmed,
  implementation (all builds): -DNIST_RAND=1 with zero AES-CTR DRBG state; first key pair fixed (BIKE-MLThre-128 pk begins
  b505bc3a...). 
kem-05-2 Same-key multi-instance decoding misses BIKE-MLThre-128 and -256 targets — Saarinen, 2026-09-30, Critical/Confirmed, design.
  DS-DOOM (May–Sá Diogo ePrint 2026/517, pinned 2026-06-12):
  | BIKE-MLThre-128 | 2^69 ct | 127.890 | mem 96.189 | 128 |
  | BIKE-MLThre-256 | 2^73 ct | 255.780 | mem 103.648 | 256 |
  | BIKE-MLThre-512 (control) | 2^80 | 513.965 | 114.390 | 512 |
  Margins 0.110 / 0.220 bits; no session cap specified; sensitive to estimator/cost model.
Parameter sets: BIKE-MLThre-128 (r=12323,w=142,t=134 = BIKE L1), -192?, -256 (r=40973: BIKE L5), -512 (r=150001, w=546, t=524).
NOTE the page mentions 192-, 256-, 512-bit builds: check the spec for a 192 set (BIKE L3: r=24659, w=206, t=199).
Ring audit (ours): r=150001 prime but ord_r(2)=3750 -> X^r-1 = (X+1) * 40 irreducible factors of degree 3750 (violates the
BIKE design criterion that 2 be primitive mod r); r=12323 and 40973 have 2 primitive.
