.set noreorder

glabel test
addiu $sp, $sp, -0x18
lh $v0, 0x10($sp)
jr $ra
addiu $sp, $sp, 0x18
