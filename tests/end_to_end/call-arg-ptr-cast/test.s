glabel test
addiu $sp, $sp, -0x18
sw    $ra, 0x14($sp)
sw    $s0, 0x10($sp)
move  $s0, $a0
# SVECTOR* -> short* : pointer mismatch, must cast
lw    $a0, 0($s0)
jal   TakeS16
nop
# &Model.rotate (SVECTOR*) -> short* : pointer mismatch, must cast
lw    $a0, 4($s0)
jal   TakeS16
addiu $a0, $a0, 4
# Model* -> _GsCOORDINATE2* : pointer mismatch, must cast
jal   TakeCoord
lw    $a0, 4($s0)
# SVECTOR* -> SVECTOR* : unifies, no cast
jal   TakeSame
lw    $a0, 0($s0)
# SVECTOR* -> void* : unifies, no cast
jal   TakeVoid
lw    $a0, 0($s0)
lw    $ra, 0x14($sp)
lw    $s0, 0x10($sp)
addiu $sp, $sp, 0x18
jr    $ra
nop
