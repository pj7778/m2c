struct _m2c_stack_test {
    /* 0x00 */ char pad0[0x10];
    /* 0x10 */ struct Param p;
    /* 0x18 */ char pad18[8];
};                                                  /* size = 0x20 */

void test(s32 u) {
    struct Param p;

    p.user = u;
    p.type = 0x13;
    Use(&p);
}
