# ngcc.dev/reports/kem-37.html — TriQ-KEM (fetched 2026-10-31). 2 findings, no designer responses. NO design-level cryptanalysis.

kem-37-1 Decapsulation re-expands private support with variable work — Saarinen, 2026-09-23, Medium/Confirmed, side-channel.
kem-37-2 FO re-encryption leaks the decrypted message through sampler timing — Xiong, Wang (GLM-5.3, Claude Opus 5.5), 2026-09-30,
  Medium/Lead, side-channel. Bounded-density sampler early exit -> iteration count depends on theta' (decrypted message);
  contradicts §III-B claim that the bounded-density condition is public/independent of secrets. 7.9% of re-encryptions need an
  extra draw; mean cycle gap 37,227 (z ~ 4.4; 5.6 on quieter host). Same mechanism as "Don't Reject This" (ePrint 2021/1485).
Parameter sets: TriQ-KEM-128/256/384/512.
