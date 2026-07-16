s32 test(s32 arg0, s32 arg1, s32 arg2) {
    s32 var_a1;

    var_a1 = arg1;
    if (var_a1 < 0) {
        var_a1 += 1;
    }
    foo(var_a1 + 2, 3, 4, 5, arg0, arg2);
    return 0;
}
