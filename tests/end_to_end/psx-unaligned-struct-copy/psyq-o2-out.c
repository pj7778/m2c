void test(struct Dst *d, struct Src *s, void *vd, void *vs) {
    d->v = s->v;
    vd->unk0 = (unaligned s32) vs->unk0;
    vd->unk4 = (unaligned s32) vs->unk4;
}
