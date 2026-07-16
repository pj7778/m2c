s32 test(void) {
    // GTE: lwc2 $0, ($a0)
    // GTE: lwc2 $1, 0x4($a0)
    // GTE: rtpt
    // GTE: nclip
    // GTE: avsz3
    // GTE: swc2 $16, ($a1)
    return M2C_ERROR(/* GTE_cfc2($31) */);
}
