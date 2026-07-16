glabel test
# p = valloc(0x74); *(p + 0x50) = 0; InitCoord(p); return p;
# The 0x74 allocation size uniquely names the container `Model` (0x74, embedding
# Coord at 0). The only type evidence otherwise is the InitCoord(Coord*) param
# unify, so with --alloc-container-fn valloc the local is typed Model*: the
# 0x50 store lands in Model.tail and the InitCoord arg gets a Coord* cast.
addiu $sp, $sp, -0x18
sw    $ra, 0x14($sp)
sw    $s0, 0x10($sp)
li    $a0, 0x74
jal   valloc
nop
move  $s0, $v0
sw    $zero, 0x50($s0)
move  $a0, $s0
jal   InitCoord
nop
move  $v0, $s0
lw    $ra, 0x14($sp)
lw    $s0, 0x10($sp)
addiu $sp, $sp, 0x18
jr    $ra
nop
