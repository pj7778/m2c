s32 test(void *p, void *q, void *r) {
    s32 temp_v0;

    temp_v0 = *(s32 *) p + *(u16 *) q + *(s8 *) r;
    *(s32 *) p = 0;
    *(u16 *) q = 0;
    *(s8 *) r = 0;
    p->unk4 = 0;
    return temp_v0;
}
