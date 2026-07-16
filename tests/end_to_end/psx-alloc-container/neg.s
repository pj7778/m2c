glabel test
# Negative control: p = valloc(0x74); *(p + 0x50) = 0; Process(p); return p;
# Here the param evidence (Process takes Whole*, a complete 0x74 struct) already
# gives the local its full type. Because the leaf's size == the allocation size,
# the container heuristic must NOT rewrap it -- field/param evidence wins over
# size. The local stays Whole* and the 0x50 store resolves to Whole.b[0].
addiu $sp, $sp, -0x18
sw    $ra, 0x14($sp)
sw    $s0, 0x10($sp)
li    $a0, 0x74
jal   valloc
nop
move  $s0, $v0
sw    $zero, 0x50($s0)
move  $a0, $s0
jal   Process
nop
move  $v0, $s0
lw    $ra, 0x14($sp)
lw    $s0, 0x10($sp)
addiu $sp, $sp, 0x18
jr    $ra
nop
