void test(struct Holder *h) {
    TakeS16((s16 *) h->svp);
    TakeS16((s16 *) &h->mptr->rotate);
    TakeCoord((_GsCOORDINATE2 *) h->mptr);
    TakeSame(h->svp);
    TakeVoid(h->svp);
}
