.set noreorder

# Reads callee-saved $s2 that is never written before use. m2c's dataflow
# cannot prove it is initialized, so it used to emit a bare `saved_reg_s2`
# identifier (undeclared -> invalid C). It must now be declared as an
# uninitialized local instead.
glabel test
addiu $sp, $sp, -0x18
sw    $ra, 0x14($sp)
sw    $s2, 0x10($sp)
addu  $v0, $s2, $a0
lw    $ra, 0x14($sp)
lw    $s2, 0x10($sp)
jr    $ra
addiu $sp, $sp, 0x18
