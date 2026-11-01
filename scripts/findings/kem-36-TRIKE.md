# ngcc.dev/reports/kem-36.html — TRIKE (fetched 2026-10-31). Designer response only on kem-36-2.

kem-36-1 Specified decoder rejects every tested honest ciphertext — Saarinen, 2026-09-21, High/Confirmed, design. PDF threshold
  max(Tnow,T') vs implementations min(Tnow,T'): literal max decoder 0/1000 (API still success), min decoder 1000/1000. Follow-up
  (Xiong, Wang): Algorithm 8 omits the original syndrome term the source retains.
kem-36-2 Withdrawn (binomial collision counts misread) — Xiong, Wang, 2026-09-30, withdrawn 2026-10-20.
kem-36-3 Decapsulation fails to free h0 buffer — Xiong, Wang, Low/Confirmed (2,064 B per TRIKE-2 call; 16,400 B per TRIKE-7/9).
kem-36-4 Boundary weak-key classes omitted from the DFR bound — Xiong, Wang, 2026-09-30, Medium/Proof gap. Tables 12–14 filter
  classes at/beyond boundary m0; adjacent class m0-1 unfiltered: zero failures in 1e7 (TRIKE-1/2/3/5) or 1e6 (TRIKE-7/9) ->
  95% UCL ~2^-21.67 / 2^-18.35, not 2^-128..2^-512.
kem-36-5 Weak-key reduction assumes secret parity checks public — Xiong, Wang, Medium/Proof gap (Theorem 4 starts from pk
  containing (h0,h1,h2); pk is actually (sigma, r2)).
kem-36-6 Decapsulation addresses depend on secret support — Xiong, Wang, Medium/Confirmed, side-channel (contradicts p.12 CT claim).
kem-36-7 Generic unsalted-FO multi-ciphertext loss — Xiong, Wang, 2026-10-03, Info/Confirmed: 2^l/(T+1) trials; T=2^32 ->
  2^224 (TRIKE-5), 2^480 (TRIKE-9).
kem-36-8 Resets external DRBG for deterministic re-encryption — Saarinen, Low/Confirmed.
Parameter sets named: TRIKE-1, -2, -3, -5, -7, -9 (six sets; r = 10301, 15581, 22003, 35363, 69691, 114043).
