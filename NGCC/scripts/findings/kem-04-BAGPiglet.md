# ngcc.dev/reports/kem-04.html — BAG-Piglet (rank metric) (fetched 2026-10-31). 2 findings, no designer responses.

kem-04-1 Secret-dependent pivoting in the Gabidulin decoder — Saarinen, 2026-09-23, Medium/Confirmed, side-channel.
kem-04-2 Rejection key does not bind the received ciphertext — Saarinen, 2026-09-25, reclassified CRITICAL 2026-10-31,
  Confirmed, DESIGN, all sets; key recovery executed for -128 and -256. Algorithm 2 §1.4: rejection key from seed and ct'
  (re-encryption of decrypted message), not received ct -> plaintext-checking oracle when keys observable. Probes u=(u1,0) place
  chosen subspace in the suffix annihilated by augmented-Gabidulin decoder; decoding succeeds iff chosen subspace meets
  Supp(x u1) + offset; u1=1 tests Supp(x), u1=h1 tests Supp(y1); then s1 = x h1 + y1 linear system -> x. 57,057 queries
  (BAG-Piglet-128, ~5 min), 353,557–392,779 (BAG-Piglet-256, ~1 h); ~2^19 (-384), ~2^26 (-512) estimated. Implicit-rejection
  seed not recovered. KEM BROKEN (CCA key recovery) at design level.
Parameter sets: BAG-Piglet-128/256/384/512.
