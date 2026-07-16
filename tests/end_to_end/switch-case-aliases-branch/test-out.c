s32 test(s32 arg0) {
    if (arg0 >= 0) {
        switch (arg0) {
        case 0:
            return 0x64;
        case 1:
            goto block_4;
        case 2:
            return 0xC8;
        default:
            return 0;
        }
    } else {
block_4:
        return -1;
    }
}
