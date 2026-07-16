glabel test
# Build a Param struct on the stack at sp+0x10 and pass its address to Use().
# The callee param is Param* (a 0x10-byte struct), so m2c should synthesize a
# single address-taken `Param` local instead of four loose spNN scalars.
# The sp20 slot is passed to UseScalar(int*) -- a scalar pointee -- and must
# stay a plain scalar local (negative control against over-firing).
addiu $sp, $sp, -0x28
sw    $ra, 0x24($sp)
sw    $a0, 0x10($sp)
sw    $a1, 0x14($sp)
sw    $zero, 0x18($sp)
sw    $zero, 0x1C($sp)
addiu $a0, $sp, 0x10
jal   Use
nop
sw    $zero, 0x20($sp)
addiu $a0, $sp, 0x20
jal   UseScalar
nop
lw    $ra, 0x24($sp)
addiu $sp, $sp, 0x28
jr    $ra
nop
