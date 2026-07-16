void test(s32 a, s32 u) {
    Param sp10;
    s32 sp20;

    sp10.type = a;
    sp10.user = u;
    sp10.start = 0;
    sp10.end = 0;
    Use(&sp10);
    sp20 = 0;
    UseScalar(&sp20);
}
