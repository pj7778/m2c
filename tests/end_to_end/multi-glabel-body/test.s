glabel test
addiu $sp, $sp, -8
beqz  $a0, .Lsecond
 nop
addiu $v0, $zero, 1
b     .Lend
 nop
glabel second_entry
.Lsecond:
addiu $v0, $zero, 2
.Lend:
addiu $sp, $sp, 8
jr    $ra
 nop
