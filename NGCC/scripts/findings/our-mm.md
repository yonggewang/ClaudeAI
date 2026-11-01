# Blockwise MaxMinors re-implementation (mm_blockwise.py, mm_search.py)  [Computed]
Ebar (Theorem 7.6) transcription validated:
 - single-block case l=1 reduces to m*C(n-k-1,r) exactly (4 test cases).
 - reproduces the designers' tabulated points:
   BRQC-128 key, blocks (119,119) ranks (5,5), k=119, a=(0,22): 216.84 (xi'=1.012) vs spec 2^216, xi'=1.05
   BRQC-128 ct, ranks (5,5,8), k=119, p=(0,0,32): 181.32 (xi'=1.009) vs spec 2^181, xi'=1.01
   BRQC-512 ct, ranks (8,8,8), k=227, a=(0,0,36): 566.79 (xi'=1.031) vs spec 2^566, xi=0.29 (unpunctured xi reproduced: 0.2897)
   BRA-128 ct, ranks ordered (8,5,5), k=121, p=(1,1,2): 189.15 (xi'=1.014) vs spec 2^189, xi=1.14 (our unpunctured xi=1.138)
   -> BLOCK ORDER matters for the Thm 7.6 counting; the designers order blocks with the largest rank first.
Added cap: E <= m*C(sum n' - k' - 1, sum r') (the modelling has no more equations than that).
OPEN ISSUE (our search): with aggressive per-block puncturing the SAME formula + the designers' own feasibility
  criterion (xi' = Ebar/N >= 1) gives points far below the tabulated minima, e.g. BRQC-512 ciphertext instance
  p=(179,2,219), a=(40,0,0): 414.10 bits (xi'=1.031) vs the tabulated 566. Note Ebar is an UPPER bound on the
  number of INDEPENDENT equations, so xi' >= 1 is necessary, not sufficient: either the designers' search was not
  exhaustive, or the criterion fails in the heavy-puncturing regime (n_i' close to r_i). Report as an open
  question about the cost model, NOT as an attack.
