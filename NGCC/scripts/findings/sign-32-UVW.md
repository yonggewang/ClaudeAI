# ngcc.dev/reports/sign-32.html — UVW signature (Wave-type, F3) (fetched 2026-10-31). 4 findings, no designer responses.

sign-32-1 Every signature is accepted — Saarinen, 2026-09-21, Critical/Confirmed, implementation: API wrapper stores the verify
  result then unconditionally returns 0 (all six wrappers; LittleQ follow-up; Xiong–Wang ePrint 2026/2232 §15).
sign-32-2 All-zero signature crashes two verifier instances — Saarinen, Low/Confirmed (UVW-128, -256).
sign-32-3 Pair-correlated signatures recover an equivalent UVW-128 or UVW-256 signing key — Martin Feussner (OpenAI Codex
  assistance), 2026-09-27; extension Saarinen 2026-10-17; Critical/Confirmed, DESIGN. Forced-pair sampler (Alg. 5 step 3 p.10)
  mapped through the secret monomial transformation (Alg. 6 steps 16–18) contradicts the p.10 indistinguishability claim.
  r1 = 3250 / 3167 / 6434. UVW-128: 300 signatures -> high-confidence pairs spanning a 1,600-dim public subspace; quotienting
  the 9,700 public columns recovers all 4,850 hidden pairs and relative scales -> equivalent decoder, forgery of 1,244 bytes at
  weight 8,633. UVW-256: 308 signatures, all 9,600 hidden pairs from 19,200 columns, forgery accepted, 13 min on 28 cores.
  Pair statistics (both-zero, one-zero, equal, negated): 0.044, 0.133, 0.352, 0.472 vs uniform 0.012, 0.196, 0.396, 0.396.
  UVW-512 same distribution (28 signatures), recovery not attempted.
sign-32-4 Resets external DRBG for deterministic matrix expansion — Saarinen, Low/Confirmed.
