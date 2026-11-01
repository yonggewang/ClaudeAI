/*
 * BAG-Loong-128 FO decoding/plaintext-checking oracle demonstration (kem-03-2).
 *
 * Black-box: uses only the public KEM API (kem_keygen/kem_enc/kem_dec).
 *
 * Claim (ngcc.dev kem-03-2): the implicit-rejection shared secret is
 *   ss = KDF(xi, ct')   with ct' = Enc(pk, Decrypt(sk, ct.core), derive_g(..)),
 * i.e. it binds to the RE-ENCRYPTION of the decrypted message, not to the
 * received ciphertext.  Consequence: for a fixed salt, every received core
 * that decodes to the same message m yields the IDENTICAL reject-path ss.
 * That is a decoding / plaintext-checking oracle and breaks IND-CCA2.
 *
 * Experiment: take a valid (ss0, ct0); flip single bits of the core; submit
 * each variant; bucket the resulting shared secrets.  A correct FO KEM would
 * give (essentially) distinct pseudorandom secrets for distinct invalid
 * ciphertexts.  We expect instead one large collision bucket: all the
 * single-bit variants whose core still decodes to m0 share one secret.
 */
#include "KEM_AlgorithmInstance.h"
#include "loong_parameters.h"
#include "loong_status.h"
#include "parsing.h"
#include "drng.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* The scheme's global DRBG, defined and seeded by the test harness normally. */
DRNG_ctx drng_algorithm;
#define SEED_LEN_BYTES 64

static unsigned char PK[LOONG_PK_BYTES];
static unsigned char SK[LOONG_SK_BYTES];

static int ss_eq(const unsigned char *a, const unsigned char *b) {
    return memcmp(a, b, LOONG_SS_BYTES) == 0;
}

int main(void) {
    unsigned long long pkl = LOONG_PK_BYTES, skl = LOONG_SK_BYTES;
    unsigned long long ssl = LOONG_SS_BYTES, ctl = LOONG_CT_BYTES;
    unsigned char ss0[LOONG_SS_BYTES], ssv[LOONG_SS_BYTES], ssi[LOONG_SS_BYTES];
    unsigned char ct0[LOONG_CT_BYTES], ct[LOONG_CT_BYTES];
    int rc;

    unsigned char seed[SEED_LEN_BYTES];
    for (int i = 0; i < SEED_LEN_BYTES; i++) seed[i] = (unsigned char)(0xA5 ^ i);
    init_random_number(&drng_algorithm, seed, SEED_LEN_BYTES);

    rc = kem_keygen(PK, &pkl, SK, &skl);
    if (rc != 0) { fprintf(stderr, "keygen %d\n", rc); return 1; }

    rc = kem_enc(PK, LOONG_PK_BYTES, ss0, &ssl, ct0, &ctl);
    if (rc != 0) { fprintf(stderr, "enc %d\n", rc); return 1; }

    /* 1. valid decapsulation reproduces the encapsulation secret */
    memcpy(ct, ct0, LOONG_CT_BYTES);
    ssl = LOONG_SS_BYTES;
    rc = kem_dec(SK, LOONG_SK_BYTES, ct, LOONG_CT_BYTES, ssv, &ssl);
    printf("valid decap: status=%d  ss==enc_ss? %s\n", rc,
           ss_eq(ssv, ss0) ? "YES" : "NO");

    /* 2. flip single bits in the CORE region [0, PKE_CT_BYTES), keep salt */
    const int CORE_BYTES = LOONG_PKE_CT_BYTES;
    const int NPROBE = 4000;          /* 4000 distinct single-bit variants  */

    /* collision buckets: representative ss + count + one sample core byte idx */
    unsigned char rep[64][LOONG_SS_BYTES];
    long cnt[64];
    int bucket_firstbit[64];
    int nb = 0;

    long reject = 0, accept = 0, err = 0;
    for (int p = 0; p < NPROBE; p++) {
        memcpy(ct, ct0, LOONG_CT_BYTES);
        int byte = p >> 3, bit = p & 7;
        if (byte >= CORE_BYTES) break;
        ct[byte] ^= (unsigned char)(1u << bit);   /* one-bit-distinct core */

        ssl = LOONG_SS_BYTES;
        rc = kem_dec(SK, LOONG_SK_BYTES, ct, LOONG_CT_BYTES, ssi, &ssl);
        if (rc == LOONG_SUCCESS) { accept++; continue; }      /* re-enc matched */
        if (rc != LOONG_ERR_CRYPTO_REJECT) { err++; continue; }
        reject++;

        int found = -1;
        for (int b = 0; b < nb; b++) if (ss_eq(ssi, rep[b])) { found = b; break; }
        if (found < 0 && nb < 64) {
            memcpy(rep[nb], ssi, LOONG_SS_BYTES);
            cnt[nb] = 0; bucket_firstbit[nb] = p; found = nb; nb++;
        }
        if (found >= 0) cnt[found]++;
    }

    printf("\nprobes=%d  reject=%ld  accept(reenc-match)=%ld  other=%ld\n",
           NPROBE, reject, accept, err);
    printf("distinct reject-path shared secrets: %d\n", nb);

    /* sort buckets by count, show the top few */
    for (int i = 0; i < nb; i++)
        for (int j = i + 1; j < nb; j++)
            if (cnt[j] > cnt[i]) {
                long t = cnt[i]; cnt[i] = cnt[j]; cnt[j] = t;
                int tb = bucket_firstbit[i]; bucket_firstbit[i] = bucket_firstbit[j]; bucket_firstbit[j] = tb;
                unsigned char tmp[LOONG_SS_BYTES];
                memcpy(tmp, rep[i], LOONG_SS_BYTES); memcpy(rep[i], rep[j], LOONG_SS_BYTES); memcpy(rep[j], tmp, LOONG_SS_BYTES);
            }
    int show = nb < 6 ? nb : 6;
    printf("\ntop reject-path secret buckets (count : first 8 bytes of ss):\n");
    for (int i = 0; i < show; i++) {
        printf("  %5ld :", cnt[i]);
        for (int k = 0; k < 8; k++) printf(" %02x", rep[i][k]);
        printf("\n");
    }
    printf("\nlargest bucket = %ld distinct one-bit-different cores sharing ONE "
           "shared secret.\n", cnt[0]);
    printf("A sound FO KEM would give ~%d near-distinct secrets; the collision "
           "is the decoding oracle.\n", reject > 0 ? (int)reject : 0);
    return 0;
}
