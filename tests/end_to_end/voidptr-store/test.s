glabel test
lw $v0, 0($a0)
lhu $v1, 0($a1)
addu $v0, $v0, $v1
lb $v1, 0($a2)
addu $v0, $v0, $v1
sw $zero, 0($a0)
sh $zero, 0($a1)
sb $zero, 0($a2)
jr $ra
sw $zero, 4($a0)
