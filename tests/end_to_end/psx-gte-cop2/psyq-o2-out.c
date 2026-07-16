s32 test(void *arg1) {
    /* GTE: lwc2 $0, ($a0) */
    /* GTE: lwc2 $1, 0x4($a0) */
    /* GTE: rtpt */
    /* GTE: nclip */
    /* GTE: avsz3 */
    arg1->unk0 = (s32) GTE_MFC2(16);
    arg1->unk4 = (s32) GTE_MFC2(17);
    arg1->unk8 = (s32) GTE_MFC2(18);
    return GTE_CFC2(31);
}
