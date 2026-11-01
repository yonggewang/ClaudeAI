# Our executed result — BAG-Loong kem-03-2 FO / implicit-rejection break

Executed on the official BAG-Loong-128 Reference_Implementation (Loong-Block-ms-128),
built with its own Makefile (cc -std=c99 -O2), driver linked against the package's
object files, using only the public API kem_keygen/kem_enc/kem_dec.
Scripts: break/loong/oracle_demo.c, oracle2.c, oracle3.c.

## Flaw (loong_kem.c, loong_kem_decapsulate, lines ~229-246)
  dec_status = decrypt(m, sk, ct.core); if fail -> m := 0
  g  = derive_g(pk, m, ct.salt)
  ct' = encrypt_derandomized(pk, m, g)          # re-encryption of DECRYPTED m
  valid = (dec_status==SUCCESS) && ct_equal(ct', ct.core)
  selected = valid ? g : xi                      # xi = per-key rejection secret
  ss = KDF(selected, ct')                         # <-- binds ct', NOT received ct
On the reject branch ss = KDF(xi, ct'); ct' is a function of (decrypted m, salt)
only. The received ciphertext core does not enter the shared secret. Matches
ngcc.dev kem-03-2 (Saarinen, reclassified down to Medium 2026-10-17) and the
sibling kem-04-2 (BAG-Piglet, executed, Critical).

## Executed measurements (seed 0xA5^i, one fresh keypair)
- Valid decap reproduces the encapsulation secret (status 0). [sanity]
- oracle_demo: 4000 distinct one-bit-corrupted cores (fixed salt) -> ALL return
  status = -1 (CRYPTO_REJECT) and the SINGLE identical shared secret
  f7 be 9c 4d 2c ba 65 b3 10 29 99 7d 3d 2d f0 a4.
  distinct reject-path secrets = 1 (a sound FO gives ~4000).
- oracle2: two distinct single-bit flips of ct0 -> equal (collision);
  ct1 (different message) single-bit flip -> DIFFERENT secret
  61 cb d8 d7 70 df ec 7e ... . So the reject secret is constant within a
  ciphertext/message family and varies across families -> plaintext-equality /
  decoding oracle.
- oracle3: corrupting 1..256 tail bytes of the core leaves the reject secret in
  the m0 family (decoder ignores the residual tail; cf. kem-03-5). Flipping the
  decoded message is what changes the secret.

## Status
IND-CCA2 broken at the design level: the implicit-rejection shared secret does
not bind the received ciphertext (4000 distinct ciphertexts -> 1 secret) and
leaks message equality. Reproduced by execution on the BAG-Loong reference
implementation, independent of the sampler bug kem-03-3. Upgrades kem-03-2 from
"Medium/design-concern" to a demonstrated CCA break; full key recovery follows
the kem-04-2 route (executed on BAG-Piglet). Verdict: NEW (executed).
