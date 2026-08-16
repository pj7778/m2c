void GTE_AVSZ3(void);                               /* m2c intrinsic; define it for your target */
s32 GTE_CFC2(s32);                                  /* m2c intrinsic; define it for your target */
void GTE_LWC2(s32, s32);                            /* m2c intrinsic; define it for your target */
s32 GTE_MFC2(s32);                                  /* m2c intrinsic; define it for your target */
void GTE_NCLIP(void);                               /* m2c intrinsic; define it for your target */
void GTE_RTPT(void);                                /* m2c intrinsic; define it for your target */
void GTE_SWC2(s32, s32);                            /* m2c intrinsic; define it for your target */

s32 test(void *arg0, void *arg1) {
    GTE_LWC2(0, arg0->unk0);
    GTE_LWC2(1, arg0->unk4);
    GTE_RTPT();
    GTE_NCLIP();
    GTE_AVSZ3();
    GTE_MFC2(2);
    GTE_SWC2(16, arg1->unk0);
    GTE_SWC2(17, arg1->unk4);
    GTE_SWC2(18, arg1->unk8);
    return GTE_CFC2(31);
}
