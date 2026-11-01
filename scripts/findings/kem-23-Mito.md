# ngcc.dev/reports/kem-23.html — Mito (fetched 2026-10-31). 2 findings, no designer responses.

kem-23-1 Mito-E discards every erasure before RS decoding — Saarinen, 2026-09-21, Medium/Confirmed, implementation, Mito-1-E and
  Mito-2-E (all sets). Spec: errors-and-erasures RS decoding with 2nu+t <= N-K; all 12 E trees compute t,pos but call errors-only
  reed_solomon_decode -> shipped E variants do not implement the algorithm whose DFR the PDF claims. Some trees hard-code
  PARAM_ALPHA=7 while E-variant DFR tables use 9 or 11. DFR not measured.
kem-23-2 Mito uses the external DRBG as an XOF — Saarinen, 2026-10-03, Low/Confirmed, all nine reference implementations.
No design-level cryptanalysis published on the page.
