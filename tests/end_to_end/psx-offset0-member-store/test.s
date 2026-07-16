glabel test
# `test(int u)`: build a `struct Param` on the stack at sp+0x10 (declared as a
# known Param field via _m2c_stack_test in ctx.c) and pass its address to Use().
# The store to sp+0x10 is a scalar (sw) into Param.type at offset 0 -- it must
# resolve to the member `sp10.type = ...`, not elide to the whole aggregate.
addiu $sp, $sp, -0x20
sw    $ra, 0x1C($sp)
sw    $a0, 0x14($sp)
li    $t0, 0x13
sw    $t0, 0x10($sp)
addiu $a0, $sp, 0x10
jal   Use
nop
lw    $ra, 0x1C($sp)
addiu $sp, $sp, 0x20
jr    $ra
nop
