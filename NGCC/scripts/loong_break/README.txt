BAG-Loong kem-03-2 executed implicit-rejection / decoding-oracle demonstration.

Build (from the official BAG-Loong-128 Reference_Implementation directory,
Loong-Block-ms-128, after `make`):

  OBJS=$(ls build/src/*.o build/lib/rbc-47/*.o build/lib/api_pkc/*.o | grep -v KAT_KEM)
  cc -std=c99 -O2 -Isrc -Ilib/api_pkc -Ilib/rbc-47 oracle_demo.c $OBJS -o oracle_demo
  ./oracle_demo        # 4000 distinct ciphertexts -> 1 shared secret
  # oracle2.c: same-message collision vs different-message distinction
  # oracle3.c: reject secret invariant under tail corruption

Uses only the public API kem_keygen/kem_enc/kem_dec. The driver defines and
seeds the scheme's global DRBG exactly as the submission's KAT harness does.
