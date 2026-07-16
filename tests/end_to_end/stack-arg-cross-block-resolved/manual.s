# Regression test: a stack-passed call argument stored in an earlier block
# (here: one store before a conditional branch, one hoisted into the branch's
# delay slot) must still resolve at the call site below the merge point,
# instead of erroring with "Unable to find stack arg". Mirrors the real-world
# KPRINTF_OBJ_140 case (GCC hoisting outgoing-arg stores into free delay
# slots). `foo` takes 6 int params: a-d in $a0-$a3, e at sp+0x10, f at
# sp+0x14 (the first two stack-passed argument slots).

glabel test
addiu $sp, $sp, -0x20
sw    $ra, 0x1c($sp)
sw    $a0, 0x10($sp)
bgez  $a1, .L_merge
sw    $a2, 0x14($sp)
addiu $a1, $a1, 1
.L_merge:
addiu $a0, $a1, 2
addiu $a1, $zero, 3
addiu $a2, $zero, 4
jal   foo
addiu $a3, $zero, 5
lw    $ra, 0x1c($sp)
addiu $sp, $sp, 0x20
jr    $ra
move  $v0, $zero
