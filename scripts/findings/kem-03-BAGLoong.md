# ngcc.dev/reports/kem-03.html — BAG-Loong (rank metric) (fetched 2026-10-31). 5 findings, no designer responses.

kem-03-1 Secret-dependent pivoting in the Gabidulin decoder — Saarinen, 2026-09-23, Medium/Confirmed, side-channel.
kem-03-2 Rejection key does not bind the received ciphertext — Saarinen, 2026-09-25, Medium/Confirmed (reclassified from High
  2026-10-17), design: Algorithm 2 §1.4 uses K(xi, ct') with ct' = re-encryption of decrypted message, not received ct ->
  rejection-key collisions, plaintext-checking / decoding-failure oracle; IND-CCA2 proof does not support construction.
kem-03-3 Public support spaces reduce secret-key recovery to linear algebra — Zihan Liu (ePrint 2026/2223), 2026-09-27,
  Critical/Confirmed, IMPLEMENTATION, all four sets: reference sampler ignores XOF when choosing supports, builds one public pool
  (1, beta, beta^2, ...) with the two supports as fixed overlapping slices -> S = H X + Y projected gives binary linear system for
  X; 0.049–0.988 s; 40/40 KATs; witness 5 fresh BAG-Loong-128 keys, rank 210/210.
kem-03-4 Merged support reduces rank-decoding costs below three claimed levels — Xiong, Wang (GLM-5.3), 2026-10-05,
  Critical/Confirmed, DESIGN, BAG-Loong-256/384/512. Eq. (1) p.11: error rank t1+t2-g (g-dim intersection); PRR analysis §3.3.2
  and Table 5 PRR column use t1+t2; OJ and MM columns (Thm 3.2, 3.4) already use t1+t2-g. Measured merged ranks 6, 8, 9, 10.
  Closed form (omega=2.807): 2^246.9, 2^330.7, 2^430.3; CryptographicEstimators 2.1.1 (omega=3): 2^243.3, 2^333.3, 2^432.9 —
  below 256/384/512. 128-bit set meets target. (The 2^403.5 figure for 512-bit ciphertext assumes message known.)
kem-03-5 Decoder rejects supports permitted by the specification — Xiong, Wang, 2026-10-05, Low/Confirmed, implementation:
  residual tail support dims 38/57/72/82 exceed epsilon 33/51/66/73 (Table 1 p.8); spec-conforming sampler -> 0/40 round trips.
Parameter sets: BAG-Loong-128/256/384/512 (Loong-Block-ms-*).
