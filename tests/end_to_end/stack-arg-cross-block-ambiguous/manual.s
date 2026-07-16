# Regression test: a stack-passed call argument stored differently along two
# incoming branches must still be reported as unresolved ("Unable to find
# stack arg") -- it must NEVER be resolved to either (or a merged) value,
# since that would silently compile a wrong argument into the output. The
# other stack arg slot (0x14), stored once and unconditionally in the
# branch's delay slot, is unambiguous and must still resolve fine, showing
# the two slots of the same call are judged independently.
# `foo` takes 6 int params: a-d in $a0-$a3, e at sp+0x10, f at sp+0x14.

glabel test
addiu $sp, $sp, -0x20
sw    $ra, 0x1c($sp)
bgez  $a1, .L_else
sw    $a2, 0x14($sp)
sw    $a0, 0x10($sp)
b     .L_merge
nop
.L_else:
sw    $a3, 0x10($sp)
.L_merge:
addiu $a0, $zero, 1
addiu $a1, $zero, 2
addiu $a2, $zero, 3
jal   foo
addiu $a3, $zero, 4
lw    $ra, 0x1c($sp)
addiu $sp, $sp, 0x20
jr    $ra
move  $v0, $zero
