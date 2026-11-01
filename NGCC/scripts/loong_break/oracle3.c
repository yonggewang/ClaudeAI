/* Locate the decode-fail transition: corrupt the TAIL of the core (the c2/word
 * region the Gabidulin decoder must correct) at increasing rank and watch when
 * the reject-path secret flips away from the m0 value.  Uses the internal
 * decrypt to report the decoded message/residual so the oracle is unambiguous. */
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
static int eq(const unsigned char*a,const unsigned char*b){return memcmp(a,b,LOONG_SS_BYTES)==0;}

int main(void){
    unsigned long long pkl=LOONG_PK_BYTES,skl=LOONG_SK_BYTES,ssl,ctl;
    unsigned char seed[SEED_LEN_BYTES];
    for(int i=0;i<SEED_LEN_BYTES;i++)seed[i]=(unsigned char)(0xA5^i);
    init_random_number(&drng_algorithm,seed,SEED_LEN_BYTES);

    unsigned char ct0[LOONG_CT_BYTES],ct[LOONG_CT_BYTES];
    unsigned char ss0[LOONG_SS_BYTES],base[LOONG_SS_BYTES],ss[LOONG_SS_BYTES];
    kem_keygen(PK,&pkl,SK,&skl);
    ssl=LOONG_SS_BYTES; ctl=LOONG_CT_BYTES; kem_enc(PK,LOONG_PK_BYTES,ss0,&ssl,ct0,&ctl);

    /* baseline reject secret: 1-bit flip in the tail */
    memcpy(ct,ct0,LOONG_CT_BYTES); ct[LOONG_PKE_CT_BYTES-1]^=1;
    ssl=LOONG_SS_BYTES; kem_dec(SK,LOONG_SK_BYTES,ct,LOONG_CT_BYTES,base,&ssl);

    printf("corrupting last K bytes of the core; distinct reject secrets seen:\n");
    unsigned char reps[32][LOONG_SS_BYTES]; int nb=0;
    int kset[]={1,2,4,8,16,24,32,48,64,96,128,192,256};
    for(unsigned ki=0; ki<sizeof(kset)/sizeof(kset[0]); ki++){
        int K=kset[ki];
        memcpy(ct,ct0,LOONG_CT_BYTES);
        for(int i=0;i<K;i++) ct[LOONG_PKE_CT_BYTES-1-i]^=0xFF;
        ssl=LOONG_SS_BYTES; int rc=kem_dec(SK,LOONG_SK_BYTES,ct,LOONG_CT_BYTES,ss,&ssl);
        int b=-1; for(int j=0;j<nb;j++) if(eq(ss,reps[j])){b=j;break;}
        if(b<0){memcpy(reps[nb],ss,LOONG_SS_BYTES);b=nb++;}
        printf("  tail %3dB corrupted: status=%d  secret#%d  %s\n",
               K,rc,b, eq(ss,base)?"(== m0 family)":"(DIFFERENT)");
    }
    printf("\n%d distinct reject secrets across corruption levels.\n",nb);
    printf("A change from the m0 family = a decode-outcome flip observed purely\n"
           "through the KEM output: a decoding oracle.\n");
    return 0;
}
