/*
 * BAG-Loong-128 kem-03-2, part 2: confirm the reject-path secret is a
 * function of the DECRYPTED MESSAGE (a decoding / plaintext-checking oracle),
 * not merely a constant.
 *
 * We compare reject-path shared secrets across controlled regimes:
 *   A: ct0 core perturbed by 1 bit        (expected: still decodes to m0)
 *   B: ct0 core corrupted heavily         (expected: decoding fails -> m:=0)
 *   C: a second ciphertext ct1 (msg m1) perturbed by 1 bit
 *   salt is held fixed within each family so only the decrypted message varies.
 *
 * Oracle property: secret(A) depends on m0, secret(B) on the failure branch,
 * secret(C) on m1.  Distinct decrypted outcomes -> distinct reject secrets.
 */
#include "KEM_AlgorithmInstance.h"
#include "loong_parameters.h"
#include "loong_status.h"
#include "parsing.h"
#include "drng.h"
#include <stdio.h>
#include <string.h>

DRNG_ctx drng_algorithm;
#define SEED_LEN_BYTES 64

static unsigned char PK[LOONG_PK_BYTES], SK[LOONG_SK_BYTES];
static void phex(const char*t,const unsigned char*s){printf("%s",t);for(int i=0;i<16;i++)printf(" %02x",s[i]);printf("\n");}
static int eq(const unsigned char*a,const unsigned char*b){return memcmp(a,b,LOONG_SS_BYTES)==0;}

static int decap(const unsigned char*ct,unsigned char*ss){
    unsigned long long l=LOONG_SS_BYTES;
    return kem_dec(SK,LOONG_SK_BYTES,(unsigned char*)ct,LOONG_CT_BYTES,ss,&l);
}

int main(void){
    unsigned long long pkl=LOONG_PK_BYTES,skl=LOONG_SK_BYTES,ssl,ctl=LOONG_CT_BYTES;
    unsigned char seed[SEED_LEN_BYTES];
    for(int i=0;i<SEED_LEN_BYTES;i++)seed[i]=(unsigned char)(0xA5^i);
    init_random_number(&drng_algorithm,seed,SEED_LEN_BYTES);

    unsigned char ct0[LOONG_CT_BYTES],ct1[LOONG_CT_BYTES],ct[LOONG_CT_BYTES];
    unsigned char ss0[LOONG_SS_BYTES],ss1[LOONG_SS_BYTES];
    unsigned char ssA[LOONG_SS_BYTES],ssB[LOONG_SS_BYTES],ssC[LOONG_SS_BYTES],tmp[LOONG_SS_BYTES];

    kem_keygen(PK,&pkl,SK,&skl);
    ssl=LOONG_SS_BYTES; ctl=LOONG_CT_BYTES; kem_enc(PK,LOONG_PK_BYTES,ss0,&ssl,ct0,&ctl);
    ssl=LOONG_SS_BYTES; ctl=LOONG_CT_BYTES; kem_enc(PK,LOONG_PK_BYTES,ss1,&ssl,ct1,&ctl);

    const int CORE=LOONG_PKE_CT_BYTES;

    /* A: ct0, 1-bit core flip */
    memcpy(ct,ct0,LOONG_CT_BYTES); ct[10]^=1; int rA=decap(ct,ssA);
    /* A': ct0, a DIFFERENT 1-bit core flip -> must equal A if both decode to m0 */
    memcpy(ct,ct0,LOONG_CT_BYTES); ct[20]^=2; int rAp=decap(ct,tmp);
    /* B: ct0, heavy corruption of the core (first 300 bytes) -> decode fails */
    memcpy(ct,ct0,LOONG_CT_BYTES); for(int i=0;i<300&&i<CORE;i++)ct[i]^=0xFF; int rB=decap(ct,ssB);
    /* C: ct1 (different message), 1-bit core flip */
    memcpy(ct,ct1,LOONG_CT_BYTES); ct[10]^=1; int rC=decap(ct,ssC);

    printf("statuses: A=%d A'=%d B=%d C=%d   (%d = reject)\n",rA,rAp,rB,rC,LOONG_ERR_CRYPTO_REJECT);
    phex("A  (ct0, 1-bit)      ss:",ssA);
    phex("A' (ct0, other bit)  ss:",tmp);
    phex("B  (ct0, 300B smash) ss:",ssB);
    phex("C  (ct1, 1-bit)      ss:",ssC);
    printf("\nA==A' (same family, same decrypted m)?  %s\n",eq(ssA,tmp)?"YES (collision)":"no");
    printf("A==B  (decode-ok vs decode-fail)?       %s\n",eq(ssA,ssB)?"yes":"NO (distinguished)");
    printf("A==C  (message m0 vs m1)?                %s\n",eq(ssA,ssC)?"yes":"NO (distinguished)");
    printf("\nInterpretation: the reject-path secret is constant within a family\n"
           "(fixed decrypted m) and changes across families -> decoding / PCO oracle.\n");
    return 0;
}
