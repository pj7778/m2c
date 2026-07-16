s32 test(s32 arg0, s32 arg1, s32 arg2, s32 arg3) {
    if (arg1 < 0) {

    }
    foo(1, 2, 3, 4, M2C_ERROR(/* Unable to find stack arg 0x10 in block */), arg2);
    return 0;
}
