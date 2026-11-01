# Our result — NSS-HQC key-recovery extrapolation is non-conservative

Script: work/nss_key.py (CryptographicEstimators 2.1.1, SDEstimator,
excluded_algorithms=[BJMMdw,BJMMpdw,BothMay]; discount = 0.5*log2(n), the
quasi-cyclic DOOM/decoding discount the designers use elsewhere).

NSS-HQC prices KEY recovery (not message recovery) with an extrapolation
formula T_key = 1.0969*sqrt(n) (Tables 7-8), fit to one HQC-128 point, giving
188.2 / 256.1 / 384.0 / 512.0 for levels 128/256/384/512 -> exactly on target at
256 and above. This is a curve fit, not an ISD computation.

Key instance = [2n, n] over F2, weight 2*w_sk; (n, w_sk):
  128: (29443, 73)   256: (54493,117)   384: (122579,175)   512: (217901,233)

Direct Stern estimate (raw | with 0.5 log2 n discount | spec formula | target):
  128: 167.89 | 160.46 | 188.2 | 128   -> +32.5  (clears)
  256: 255.87 | 248.00 | 256.1 | 256   -> -8.0   (below)
  384: 372.99 | 364.54 | 384.0 | 384   -> -19.5  (below)
  512: <pending>

Even with NO discount the formula overstates the true cost by ~11 bits at 384
(373.0 vs 384.0) and sits at target at 256 (255.9 vs 256.1). With the standard
QC discount the 256/384 key instances fall 8.0/19.5 bits below level.

Status: NEW, [Computed]. Independent of the message-side break (kem-26-3,
226.5/333.0/441.4). Shows the key-recovery extrapolation formula is not a
security computation and is non-conservative. NSS-HQC already PB/below-claim;
this compounds it.
