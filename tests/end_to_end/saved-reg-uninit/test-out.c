s32 test(s32 arg0) {
    s32 saved_reg_s2;                               /* possibly uninitialized */

    return saved_reg_s2 + arg0;
}
