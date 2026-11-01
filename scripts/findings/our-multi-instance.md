# Our same-key multi-instance (DS-DOOM, May–Sá Diogo 2026/517 pinned doom.py) pricing — multi_instance.py  [Computed]
Instance exposed by one ciphertext (public syndrome), rot = free cyclic rotations, M = rot * 2^s observed ciphertexts.
First s at which DS-DOOM time < claimed level (s <= 80), time, log2 memory:
HARE-1 (n=16067, 128):   s=66 -> 127.783 (mem 93.95)   [NEW: kem-16-2 reported HARE-128 above target; that referred to HARE-2 (n=20899), which stays above: 148.5 at 2^80]
HARE-3 (192): s=78 -> 191.605 ; HARE-5 (256): s=72 -> 255.440 ; HARE-7 (384): s=64 -> 383.175 ; HARE-9 (512): s=75 -> 511.699  [matches kem-16-2]
HEP-QC-1/3/5/7: none up to 2^80 (140.3 / 218.4 / 288.1 / 585.0 at 2^80) — HQC parameters with HQC's 143/207/272 targets relabelled 128/192/256.
NSS-HQC-128: s=77 -> 127.624 [NEW]; NSS-HQC-256/384/512: already below target at s=0 (237.1 / 344.6 / 454.0) [consistent with kem-26-3]
TriQ-KEM-128/256/384/512: s=73 -> 127.522 ; s=77 -> 255.557 ; s=77 -> 383.352 ; s=78 -> 511.537  [NEW: no design finding on kem-37 page]
QUBE-128/192/256/384: s=71 -> 127.846 ; s=72 -> 191.437 ; s=74 -> 255.933 ; s=80 -> 383.527 ; QUBE-512 none (512.465 at 2^80)  [NEW]
   (u = g + h1 f1 + h2 f2: [3r, 2r], w = wg + 2 wf; designers' own tables ignore DOOM entirely)
Mito1 / Mito1-E / Mito2-E: none up to 2^80 (e.g. Mito1-128: 168.0 at 2^80; Mito2-E-128: 183.1) — comfortable.
BIKE-MLThre-128: s=69 -> 127.905 ; -256: s=73 -> 255.789 ; -512: none (513.970 at 2^80)  [matches kem-05-2: 127.890 (k=r-1), 255.780, 513.965]
TRIKE-1 (r=10301, 128): s=31 -> 127.914 (mem 58.66); 2^64 -> 116.20  [NEW, large shortfall]
TRIKE-2 (r=15581, 128): none (146.7 at 2^80)
TRIKE-3 (r=22003, 192): s=46 -> 191.527 ; TRIKE-5 (256): s=47 -> 255.682 ; TRIKE-7 (384): s=63 -> 383.990 ; TRIKE-9 (512): s=63 -> 511.404  [NEW]
QCTM128: s=79 -> 127.623 ; QCTM256: s=76 -> 255.297 ; QCTM512: none (524.3 at 2^80)  [matches kem-32-2]
HQC-128 (target 143): s=74 -> 142.443 ; HQC-192/256: none.
Single-instance DS-DOOM (M = rot) times: HARE-1 154.4, HARE-2 180.8, HEP-QC-1 172.2, NSS-HQC-128 156.0, TriQ-128 156.5, QUBE-128 157.4,
Mito1-128 199.6, BIKE-MLThre-128 155.5, TRIKE-1 140.9, TRIKE-2 177.2, QCTM128 162.3, HQC-128 172.2.
