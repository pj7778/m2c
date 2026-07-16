glabel test
div $zero, $a0, $a1
bnez $a1, .L0
nop
break 7
.L0:
addiu $at, $zero, -1
bne $a1, $at, .L1
lui $at, 0x8000
bne $a0, $at, .L1
nop
break 6
.L1:
mflo $v0
jr $ra
nop
