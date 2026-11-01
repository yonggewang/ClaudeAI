# ngcc.dev/reports/kem-32.html — QCTM (fetched 2026-10-31)

## kem-32-1 Debug path retains the secret error vector — Saarinen (AI-assisted), 2026-09-21, Low/Confirmed, implementation
Trace env var copies secret error positions into process-global storage; designers removed (2026-10-08).

## kem-32-2 Same-key multi-instance decoding misses QCTM-128/-256 targets — Saarinen, 2026-09-30, Critical/Confirmed
Public key reuse: each ciphertext C = H e^T gives 19 rotated targets (order-19 circulant part). Omitting the two non-circulant tail
checks gives effective dimensions 4958 / 9784 / 19892; fixed-weight parity restores the remaining check. Passive, < 2^80 observed
encapsulations, no decapsulation queries. Spec sets no per-key session cap.
May–Sá Diogo DS-DOOM model (ePrint 2026/517):
| Set | ciphertexts | log2 bitops | log2 mem | target |
| QCTM128 | 2^79 | 127.661 | 95.592 | 128 |
| QCTM256 | 2^76 | 255.336 | 96.271 | 256 |
| QCTM512 (control) | 2^80 | 524.342 | 124.253 | 512 |
Margins 0.339 / 0.664 bits, one heuristic cost model. Designer response 2026-10-08: n 10070 -> 10545 (QCTM128), 19000 -> 19551
(QCTM256), revised 2^136.294 / 2^264.170; QCTM512 unchanged.

## kem-32-3 Bundled RNG limits QCTM-512 keygen/encaps randomness to 384 bits — Saarinen, 2026-10-06 (ext. 10-17), Critical/Confirmed
AES256-CTR-DRBG 48-byte state; enumerate 2^384 states, ~2^424 cycles < 2^512. Extension: encapsulation also uses it -> shared
secret recovery from (pk, ct) in 2^384 state enumerations. No designer response.

## kem-32-4 Folding exposes an ordinary Goppa quotient of the public code — Liping Wang (original post); quotient audit Saarinen, 2026-10-08, Medium/Confirmed
Spec §6.3 claims the twist blocks folding; but the twist only affects the omitted final field row; published matrix = first t-1
ordinary syndrome rows + all-ones parity row. Supports = 19-element orbits. Folding across orbits exposes an ordinary degree-t/19
Goppa check space with one parity row; puncturing one coordinate gives an ordinary binary Goppa code.
| QCTM128 | quotient [530,259] | punctured Goppa [529,259] |
| QCTM256 | [1000,513] | [999,513] |
| QCTM512 | [2000,1045] | [1999,1045] |
Matches on archived KAT keys. Original post estimates quotient key recovery under Weis's heuristic GIJS model (ePrint 2026/1984)
but does not show how that yields a full QCTM decapsulation key. No full-scheme key recovery claimed.

## kem-32-5 Reported structural key recovery for QCTM256 and QCTM512 — Liping Wang, 2026-10-08, Critical/Lead (not confirmed)
Weis GIJS model on the quotient: 2^141.3 (QCTM256), 2^142.0 (QCTM512) bit ops; 2^176.7 / 2^177.7 with sqrt-memory charging.
Open: (1) GIJS/Weis assumptions not established at these quotient degrees; (2) quotient key recovery not shown on a real key;
(3) LIFTING a quotient key through the order-19 alignment and twist gauge to a full decapsulation key has not been implemented
or costed. Archived-key audit confirms only the quotient prerequisite. No designer response.

# Our additions (qctm_toy.py, verified on toy instances m=10..12):
(A) twisted row = eta*1 + F_q-combination of the t-1 ordinary rows (proof: g_{t-1} = 1/eta since t odd) -> public code is
    A_{t-1}(L,1/g) ∩ E, an alternant (not Goppa) code; corrects only (t-1)/2 errors with m(t-1)+1 redundancy.
(B) invariance under simultaneous block shift (u = alpha - 1/eta makes the action multiplicative).
(C) folded code = Gamma(X', M) ∩ E exactly, X' = {a_O^ell}, M = the degree-t0 polynomial with g = M((x-1/eta)^ell).
(D) LIFTING: quotient key (X'', M'') up to affine+Frobenius equivalence -> normalise (translation making X''-beta one coset of
    (F_q^*)^ell: unique), try the m Frobenius twists, ell-th roots b, character-1 block projection K1 = P_1(C^perp ⊗ F_q) and
    K2 = b * E_1 with E_1 = sum_k x^{(e_k 2^k-1)/ell} y^{2^k} GRS_{d_k+1}(X'^{2^k}); solve rho from rho*K2 = K1 (linear);
    unique solution with entries in mu_ell; lifted alternant key reproduces the public code and decodes w errors from the
    public syndrome (syndrome transfer by solving H_pub = Q' H_att). Polynomial time. Fills gap (3) of kem-32-5.
