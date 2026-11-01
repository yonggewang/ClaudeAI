# Rank-metric re-pricing — rank_pricing.py (CryptographicEstimators 2.1.1 RankSDEstimator, omega=2.81) [Computed]
C-Multi-UR-AG (homogeneous RSD; designers' MM with omega=2: key 172/296/530, ct 170/276/580):
  L128 key RSD(2,79,70,35,8): best 197.45 (MaxMinors a=14,p=0); ct RSD(2,79,81,35,9): 200.04 (MM a=11)   -> designers' a, p reproduced; gap = omega
  L256 key (2,127,90,45,10): 327.12 (MM a=22); ct (2,127,105,45,11): 312.57 (MM a=17,p=1)
  L512 key (2,181,134,67,12): 570.68 (MM a=36,p=1); ct (2,181,153,67,14): 628.43 (MM a=33)
  RSL (N1=11 / N2=16 same-support syndromes): naive stacking of MM equations saturates at ~ m*C(n-k,r) - m (toy rsl_toy.py:
  (m,n,k,r)=(10,16,8,4): ranks 350,550,650,690,690 = 10*C(8,4)-10; (11,14,7,3): 220,330,363=full) -> gain <= (n-k)/(n-k-r) ~ 0.4 bits.
  Bardet–Briaud RSL algebraic attack not evaluated (N << kr). Status: no design-level attack found; implementation findings only.
BAG-Loong merged support (kem-03-4; r = t1+t2-g = 6/8/9/10):
  128 [2n,n]=(2,47,84,42,6): 131.58 (MM a=9) / [2n',n'] 129.13 (GuessingEnhancedGRS)  -> meets 128 (barely)
  256 (2,67,130,65,8): 240.97 (GuessingEnhancedGRS!) vs claimed 256  [kem-03-4 reported 243.3 with omega=3]
  384 (2,83,166,83,9): 330.83 (GEGRS) vs 384 ; 512 (2,97,208,104,10): 430.37 (GEGRS) vs 512 [kem-03-4: 333.3 / 432.9]
  -> confirms kem-03-4 (our omega=2.81 numbers slightly lower: 241.0 / 330.8 / 430.4).
BRQC homogeneous relaxation (r = sum of block ranks): key 560 / 782 / 1312, ct 689 / 1036 / 1666 (GEGRS) vs claimed 181/295/566:
  the blockwise MM attack (designers' Thm 7.6/7.7) is the binding attack; re-implemented in mm_blockwise.py:
  BRQC-128 key designers' point a=(0,22): 216.84 (xi'=1.049) [Table 6: 2^216, 1.05]; ct with k=n=119, blocks (r1,r2,e)=(5,5,8),
  p=(0,0,32): 181.3 (xi'=1.009) [Table 6: 2^181, 1.01]  -> formula reproduced; exhaustive (p,a,h) search: see mm_search output.
BRA relaxation: key 275 / 376 / 683, ct 386 / 518 / 906 vs claimed 189 / 304 / 556 (blockwise MM binding; m < n for BRA).
BAG-Piglet: broken at design level by kem-04-2 (CCA plaintext-checking oracle via non-standard rejection key; key recovery in
  57k queries) — no re-pricing needed. BAG-Loong shares the same rejection-key design (kem-03-2); attack likely transfers (not run).
