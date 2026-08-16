s32 test(void *arg0, void *arg1) {
    GTE_LWC2(0, arg0->unk0);
    GTE_LWC2(1, arg0->unk4);
    GTE_RTPT();
    GTE_NCLIP();
    GTE_AVSZ3();
    GTE_MFC2(2);
    arg1->unk0 = (s32) GTE_MFC2(16);
    arg1->unk4 = (s32) GTE_MFC2(17);
    arg1->unk8 = (s32) GTE_MFC2(18);
    return GTE_CFC2(31);
}
