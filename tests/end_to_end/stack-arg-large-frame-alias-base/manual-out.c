s32 test(s32 arg0) {
    s32 saved_reg_ra;                               /* possibly uninitialized */
    s32 saved_reg_s0;                               /* possibly uninitialized */

    unksp1001C = saved_reg_ra;
    unksp10018 = saved_reg_s0;
    foo(1, 2, 3, 4, arg0 + 1);
    return 0;
}
