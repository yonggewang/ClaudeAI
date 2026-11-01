# ngcc.dev/reports/kem-33.html — QUBE (fetched 2026-10-31). 4 findings, no designer responses. NO design-level cryptanalysis.

kem-33-1 Decapsulation re-expands the private seed with a variable-length sampler — Saarinen, 2026-09-23, Medium/Confirmed, side-channel.
kem-33-2 Decryption multiplication traverses secret support positions — Saarinen, 2026-09-23, Medium/Confirmed, side-channel.
kem-33-3 Optimized API generates predictable keys and encapsulations — Xiong, Wang (GLM-5.3), 2026-10-03, Critical/Confirmed,
  implementation (optimized only): zero-initialised file-scope SHAKE context; prng_init never called by the API wrapper.
kem-33-4 Optimized FO check compares word counts as byte counts — Saarinen, 2026-10-17, Critical/Confirmed, implementation
  (optimized only): u compared 256/1639 B (QUBE-128) ... -> one-query IND-CCA2 distinguisher, malleability.
Note: reference KAT mismatches (4) and one missing KAT.
Parameter sets: QUBE-128/256/384/512 (qube-1/3/4/5); unbuilt qube-6/7/8.
